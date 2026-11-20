import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import net from 'node:net';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const webRoot = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const reportPath = path.join(webRoot, 'test', 'live_build_report.json');
const checks = [];
let serverLog = '';

function check(name, ok, detail = '') {
  checks.push({ name, ok: Boolean(ok), detail });
  if (!ok) throw new Error(`${name}${detail ? `: ${detail}` : ''}`);
}

function localPathFromMap(value) {
  const clean = value.replace(/^\.\//, '');
  return '/' + clean;
}

function normalisePath(p) {
  return path.posix.normalize(p.replace(/\\/g, '/'));
}

function stripComments(source) {
  let output = '';
  let state = 'code';
  let quote = '';
  for (let i = 0; i < source.length; i += 1) {
    const ch = source[i];
    const next = source[i + 1];
    if (state === 'code') {
      if (ch === '/' && next === '/') {
        state = 'line-comment';
        i += 1;
      } else if (ch === '/' && next === '*') {
        state = 'block-comment';
        i += 1;
      } else {
        output += ch;
        if (ch === "'" || ch === '"' || ch === '`') {
          state = 'string';
          quote = ch;
        }
      }
    } else if (state === 'string') {
      output += ch;
      if (ch === '\\' && i + 1 < source.length) {
        output += source[i + 1];
        i += 1;
      } else if (ch === quote) {
        state = 'code';
      }
    } else if (state === 'line-comment') {
      if (ch === '\n') {
        state = 'code';
        output += '\n';
      }
    } else if (state === 'block-comment') {
      if (ch === '*' && next === '/') {
        state = 'code';
        i += 1;
      }
    }
  }
  return output;
}

function findImports(source) {
  const clean = stripComments(source);
  const lines = clean.split(/\r?\n/);
  const specifiers = [];
  for (let i = 0; i < lines.length; i += 1) {
    const trimmed = lines[i].trim();
    const isImport = /^import\s/.test(trimmed);
    const isReExport = /^export\b.*\bfrom\s/.test(trimmed);
    if (!isImport && !isReExport) continue;
    let statement = trimmed;
    while (!/;\s*$/.test(statement) && i + 1 < lines.length) {
      i += 1;
      statement += '\n' + lines[i].trim();
    }
    const match = statement.match(/\bfrom\s+(['"])([^'"]+)\1/)
      || statement.match(/^import\s+(['"])([^'"]+)\1/)
      || statement.match(/^import\s*\(\s*(['"])([^'"]+)\1/);
    if (match) specifiers.push(match[2]);
  }
  return specifiers;
}

async function freePort() {
  return new Promise((resolve, reject) => {
    const probe = net.createServer();
    probe.once('error', reject);
    probe.listen(0, '127.0.0.1', () => {
      const address = probe.address();
      const port = typeof address === 'object' && address ? address.port : 0;
      probe.close((err) => err ? reject(err) : resolve(port));
    });
  });
}

async function waitForServer(base, child) {
  let lastError = '';
  for (let i = 0; i < 80; i += 1) {
    if (child.exitCode !== null) throw new Error(`server exited early: ${serverLog}`);
    try {
      const res = await fetch(base + '/index.html');
      if (res.ok) return;
      lastError = `HTTP ${res.status}`;
    } catch (err) {
      lastError = err.message;
    }
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error(`server did not become ready: ${lastError}`);
}

async function fetchOk(base, urlPath, expectedType) {
  const res = await fetch(base + urlPath);
  const type = res.headers.get('content-type') || '';
  check(`serves ${urlPath}`, res.ok && (!expectedType || type.startsWith(expectedType)), `HTTP ${res.status}, ${type}`);
  return res;
}

async function main() {
  const port = await freePort();
  const base = `http://127.0.0.1:${port}`;
  const child = spawn(process.execPath, ['server.mjs'], {
    cwd: webRoot,
    env: { ...process.env, PORT: String(port) },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  child.stdout.on('data', (d) => { serverLog += d.toString(); });
  child.stderr.on('data', (d) => { serverLog += d.toString(); });

  try {
    await waitForServer(base, child);
    const indexRes = await fetchOk(base, '/', 'text/html');
    const html = await indexRes.text();
    check('index has local module entry', /<script[^>]+type="module"[^>]+src="\.\/main\.js"/i.test(html));
    check('index has local stylesheet', /href="\.\/styles\.css"/i.test(html));
    check('no external CDN script', !/<script[^>]+src="https?:/i.test(html));

    const importMapMatch = html.match(/<script[^>]+type="importmap"[^>]*>([\s\S]*?)<\/script>/i);
    check('index has import map', Boolean(importMapMatch));
    const importMap = JSON.parse(importMapMatch[1]);
    const threePath = localPathFromMap(importMap.imports.three);
    const addonsPrefix = localPathFromMap(importMap.imports['three/addons/']);
    check('import map maps three locally', threePath === '/vendor/three.module.js');
    check('import map maps addons locally', addonsPrefix === '/vendor/jsm/');

    const resolveSpecifier = (specifier, fromPath) => {
      if (/^https?:/i.test(specifier)) throw new Error(`external import ${specifier} in ${fromPath}`);
      if (specifier === 'three') return threePath;
      if (specifier.startsWith('three/addons/')) return normalisePath(addonsPrefix + specifier.slice('three/addons/'.length));
      if (specifier.startsWith('./') || specifier.startsWith('../')) {
        return normalisePath(path.posix.join(path.posix.dirname(fromPath), specifier));
      }
      if (specifier.startsWith('/')) return normalisePath(specifier);
      throw new Error(`unmapped bare import ${specifier} in ${fromPath}`);
    };

    const moduleQueue = ['/main.js'];
    const moduleSeen = new Set();
    while (moduleQueue.length) {
      const modulePath = normalisePath(moduleQueue.shift());
      if (moduleSeen.has(modulePath)) continue;
      moduleSeen.add(modulePath);
      const res = await fetchOk(base, modulePath, 'text/javascript');
      const source = await res.text();
      check(`no absolute localhost in ${modulePath}`, !/https?:\/\/localhost|https?:\/\/127\.0\.0\.1/i.test(source));
      for (const specifier of findImports(source)) {
        const resolved = resolveSpecifier(specifier, modulePath);
        if (!moduleSeen.has(resolved)) moduleQueue.push(resolved);
      }
    }
    check('recursive local ES-module graph resolves', moduleSeen.size >= 5, `${moduleSeen.size} modules`);

    const jsonPaths = ['/world.json', '/assets/materials.json', '/assets/production_manifest.json', '/test/integration_report.json', '/test/replay_frames.json', '/captures/capture_manifest.json'];
    for (const p of jsonPaths) {
      const res = await fetchOk(base, p, 'application/json');
      const value = JSON.parse(await res.text());
      check(`valid JSON ${p}`, typeof value === 'object' && value !== null);
      if (p === '/world.json') {
        check('world has 46 obstacles / 7 waypoints', value.obstacles?.length === 46 && value.route?.waypoints?.length === 7);
      }
      if (p === '/test/integration_report.json') {
        check('simulation integration report passes', value.overallPass === true);
      }
      if (p === '/test/replay_frames.json') {
        check('replay has 120 frames', Array.isArray(value.frames) && value.frames.length === 120, `frames=${value.frames?.length}`);
      }
      if (p === '/captures/capture_manifest.json') {
        check('capture manifest reports MP4', value.mp4_status === 'written' && value.frame_count === 120);
      }
    }

    for (const p of ['/assets/forbidden_forest_m1.glb', '/assets/adanna_m1_technical_proxy.glb']) {
      const res = await fetchOk(base, p, 'model/gltf-binary');
      const buf = Buffer.from(await res.arrayBuffer());
      check(`GLB magic ${p}`, buf.subarray(0, 4).toString('ascii') === 'glTF');
      check(`GLB length ${p}`, buf.readUInt32LE(8) === buf.length, `${buf.readUInt32LE(8)} vs ${buf.length}`);
    }

    const captureFiles = [
      'captures/frames/frame_000.png',
      'captures/frames/frame_119.png',
      'captures/playable_hero_frame.png',
      'captures/playable_hud_frame.png',
      'captures/playable_contact_sheet.png',
      'captures/PLAYABLE_M1_REVIEW_SHEET.png',
      'captures/playable_replay.gif',
      'captures/playable_replay.mp4',
    ];
    for (const p of captureFiles) {
      const stat = await fsp.stat(path.join(webRoot, p));
      check(`capture exists ${p}`, stat.isFile() && stat.size > 1000, `${stat.size} bytes`);
    }
    const frames = fs.readdirSync(path.join(webRoot, 'captures', 'frames')).filter((f) => /^frame_\d{3}\.png$/.test(f));
    check('120 replay PNG frames', frames.length === 120, `${frames.length} frames`);

    const ueFiles = [
      path.join(webRoot, '..', 'ue_project', 'TDD_GAME.uproject'),
      path.join(webRoot, '..', 'ue_project', 'Config', 'DefaultEngine.ini'),
      path.join(webRoot, '..', 'ue_project', 'Source', 'TDD_GAME.Target.cs'),
      path.join(webRoot, '..', 'ue_project', 'Source', 'TDD_GAME', 'TDD_GAME.Build.cs'),
      path.join(webRoot, '..', 'ue_project', 'Source', 'TDD_GAME', 'TDDForbiddenForestGameMode.cpp'),
      path.join(webRoot, '..', 'ue_project', 'Source', 'TDD_GAME', 'TDDForbiddenForestLevel.cpp'),
      path.join(webRoot, '..', 'ue_project', 'Source', 'TDD_GAME', 'TDDAdannaProxyCharacter.cpp'),
      path.join(webRoot, '..', 'ue_project', 'Source', 'TDD_GAME', 'TDDWorldData.h'),
      path.join(webRoot, '..', 'ue_project', 'Source', 'TDD_GAMEEditor.Target.cs'),
      path.join(webRoot, '..', 'ue_project', 'Tools', 'TDD_M1_Unreal_Setup_macOS.py'),
      path.join(webRoot, '..', 'ue_project', 'Tools', 'tdd_m1_macos_audit.json'),
      path.join(webRoot, '..', 'ue_project', 'README_MACOS_UE58.md'),
    ];
    for (const p of ueFiles) {
      const stat = await fsp.stat(p);
      check(`UE source file ${path.basename(p)}`, stat.isFile() && stat.size > 0);
    }

    const docFiles = [
      path.join(webRoot, '..', '..', '..', 'PLAYABLE_MILESTONE_TRACKER.md'),
      path.join(webRoot, '..', '..', '..', 'PHASE_2_PROGRESS.md'),
      path.join(webRoot, '..', 'PLAYABLE_MILESTONE_REPORT.md'),
      path.join(webRoot, '..', 'ue_project', 'UE_SOURCE_STATE.md'),
    ];
    for (const p of docFiles) {
      const text = await fsp.readFile(p, 'utf8');
      check(`durable record ${path.basename(p)}`, text.length > 500);
    }
    const trackerText = await fsp.readFile(docFiles[0], 'utf8');
    const progressText = await fsp.readFile(docFiles[1], 'utf8');
    check('tracker records incomplete final M1', /full production\/commercial M1 acceptance is \*\*not\*\* complete/i.test(trackerText));
    check('progress records playable integration proof', /Playable Adanna M1 real-time integration proof/i.test(progressText));

    // macOS / UE 5.8 target alignment: the project must not still advertise the provisional
    // 5.4 association now that the owner environment is known.
    const uproject = JSON.parse(await fsp.readFile(path.join(webRoot, '..', 'ue_project', 'TDD_GAME.uproject'), 'utf8'));
    check('uproject targets UE 5.8', uproject.EngineAssociation === '5.8', String(uproject.EngineAssociation));
    check('uproject targets Mac', (uproject.TargetPlatforms || []).includes('Mac'));
    const targetCs = await fsp.readFile(path.join(webRoot, '..', 'ue_project', 'Source', 'TDD_GAME.Target.cs'), 'utf8');
    check('target uses BuildSettingsVersion.V7', targetCs.includes('BuildSettingsVersion.V7'));
    check('target pinned to Unreal5_8 include order', targetCs.includes('EngineIncludeOrderVersion.Unreal5_8'));

    // UBT loads only Source/*.Target.cs. A rules file named otherwise is never read, so
    // asserting against it certifies settings that do not exist. That mistake let a
    // V5/Unreal5_4 editor target pass a green audit and fail the owner's first compile.
    const srcDir = path.join(webRoot, '..', 'ue_project', 'Source');
    const srcEntries = await fsp.readdir(srcDir);
    const csRules = [];
    for (const name of srcEntries.filter((n) => n.endsWith('.cs'))) {
      const body = await fsp.readFile(path.join(srcDir, name), 'utf8');
      if (/TargetRules/.test(body)) csRules.push(name);
    }
    check('every TargetRules file is loadable by UBT (*.Target.cs)',
      csRules.every((n) => n.endsWith('.Target.cs')), csRules.join(','));
    const editorCs = await fsp.readFile(path.join(srcDir, 'TDD_GAMEEditor.Target.cs'), 'utf8');
    const settingsOf = (t) => (t.match(/DefaultBuildSettings\s*=\s*([^;]+);/) || [])[1];
    check('game and editor targets share one BuildSettingsVersion (UBT shared environment)',
      settingsOf(targetCs) !== undefined && settingsOf(targetCs) === settingsOf(editorCs),
      `game=${settingsOf(targetCs)} editor=${settingsOf(editorCs)}`);
    check('editor target pinned to Unreal5_8 include order',
      editorCs.includes('EngineIncludeOrderVersion.Unreal5_8'));
    const audit = JSON.parse(await fsp.readFile(path.join(webRoot, '..', 'ue_project', 'Tools', 'tdd_m1_macos_audit.json'), 'utf8'));
    check('macOS static audit is green', audit.checksPassed === audit.checksTotal && audit.checksTotal >= 65,
      `${audit.checksPassed}/${audit.checksTotal}`);
    check('macOS audit does not claim compile', audit.compile_verified === false && audit.pie_verified === false && audit.package_verified === false);

    const report = {
      generated: new Date().toISOString(),
      overallPass: true,
      classification: 'Static/live HTTP delivery, recursive local ES-module resolution, generated asset integrity, capture presence, UE source-file presence and durable-record verification. NOT an automated WebGL rendering test or Unreal compile/cook/package test.',
      server: { command: 'node server.mjs', port, host: '0.0.0.0', requestedFrom: '127.0.0.1 sandbox loopback' },
      checks,
      moduleCount: moduleSeen.size,
      note: 'The same world.json and game.js shared simulation are used by the browser entry, Node integration test and CPU replay captures. Browser visual verification is available through the live preview; no browser binary is installed in this sandbox.',
    };
    await fsp.writeFile(reportPath, JSON.stringify(report, null, 2) + '\n', 'utf8');
    console.log(`live build verification: ${checks.length}/${checks.length} checks passed; ${moduleSeen.size} local ES modules resolved`);
  } catch (err) {
    const report = {
      generated: new Date().toISOString(),
      overallPass: false,
      classification: 'Verification failed; see error.',
      error: err.stack || String(err),
      checks,
      serverLogTail: serverLog.slice(-4000),
    };
    await fsp.writeFile(reportPath, JSON.stringify(report, null, 2) + '\n', 'utf8');
    console.error('live build verification FAILED:', err.message);
    process.exitCode = 1;
  } finally {
    child.kill('SIGTERM');
  }
}

main();

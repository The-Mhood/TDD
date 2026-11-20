/* Automated real-time integration test and deterministic replay capture.
 * The browser and this test import the exact same game.js simulation module.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { TDDGame, makeInput, defaultInput } from '../game.js';

const here = path.dirname(fileURLToPath(import.meta.url));
const webRoot = path.resolve(here, '..');
const world = JSON.parse(fs.readFileSync(path.join(webRoot, 'world.json'), 'utf8'));
const dt = 1 / 60;
const recordEvery = 4; // 15 fps replay from a 60 Hz fixed-step simulation
const replayFps = 60 / recordEvery;

const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
function angleDelta(a, b) {
  let d = (a - b + Math.PI) % (Math.PI * 2);
  if (d < 0) d += Math.PI * 2;
  return d - Math.PI;
}

function steerInput(game, run = false) {
  const idx = Math.min(game.state.route.index, world.route.waypoints.length - 1);
  const target = world.route.waypoints[idx];
  const dx = target.x - game.state.position.x;
  const dy = target.y - game.state.position.y;
  const desiredYaw = Math.atan2(dx, dy);
  const delta = angleDelta(desiredYaw, game.state.camera.yaw);
  return makeInput({
    forward: 1,
    right: 0,
    run,
    lookX: clamp(delta * 2.6, -2.0, 2.0),
    lookY: 0,
  });
}

const game = new TDDGame(world);
const replayFrames = [];
const checks = [];
let maxSpeed = 0;
let maxZ = 0;
let cameraYawStart = game.state.camera.yaw;
let cameraYawMaxDelta = 0;
let boundaryInteractionSeen = false;
let routeProgressMax = 0;

function record(phase, input) {
  const snap = game.snapshot();
  maxSpeed = Math.max(maxSpeed, snap.player.speed);
  maxZ = Math.max(maxZ, snap.player.position.z);
  cameraYawMaxDelta = Math.max(cameraYawMaxDelta, Math.abs(angleDelta(snap.camera.yaw, cameraYawStart)));
  boundaryInteractionSeen ||= game.usedInteractions.has('boundary_waymarker');
  routeProgressMax = Math.max(routeProgressMax, snap.route.progress);
  replayFrames.push({
    ...snap,
    phase,
    hud: {
      objective: snap.route.objectiveComplete ? 'ROUTE COMPLETE — objective acknowledged' : 'Follow white cloth to the Great Root Mother',
      controls: 'WASD move · Shift run · Space jump · E interact · drag/look to orbit',
      input: { ...input },
      classification: 'RIGGED TECHNICAL GAMEPLAY PROXY — NOT FINAL CHARACTER',
      engineStatus: 'UE source scaffold unverified; real-time browser integration verified',
    },
  });
}

function runPhase(name, seconds, inputFn) {
  const steps = Math.round(seconds / dt);
  for (let i = 0; i < steps; i += 1) {
    const input = inputFn(i, i * dt) || defaultInput();
    game.update(dt, input);
    if (game.stepIndex % recordEvery === 0) record(name, input);
  }
}

function check(name, pass, detail) {
  checks.push({ name, pass: !!pass, detail });
}

// 0. Deterministic third-person camera collision at spawn (probe tree behind player).
check('camera boom collision shortens distance', game.state.camera.distance < game.state.camera.desiredDistance, {
  desired: game.state.camera.desiredDistance,
  actual: Number(game.state.camera.distance.toFixed(3)),
  occluded: game.state.camera.occluded,
});

// 1. Idle, then walk forward and acknowledge the white-cloth boundary waymarker.
runPhase('idle / boundary approach', 0.5, () => makeInput());
runPhase('walk / interaction', 1.6, (i, t) => {
  const nearMarker = game.state.position.y > -15.4 && game.state.position.y < -13.6;
  return makeInput({ forward: 1, interact: nearMarker && i % 3 === 0 });
});

// 2. Run along the first route bend using shared camera-relative steering.
runPhase('run / camera-relative turn', 2.0, () => steerInput(game, true));

// 3. Explicit turning in place.
runPhase('turn in place', 0.6, () => makeInput({ forward: 0.18, right: 0.12, lookX: 1.25 }));

// 4. Jump and land while moving.
runPhase('jump / land', 1.3, (i, t) => makeInput({ forward: 0.55, jump: t < 0.10, lookX: 0 }));

// 5. Continue a coherent playable route.
runPhase('route continuation', 2.0, () => steerInput(game, true));

const replaySnap = game.snapshot();
check('walk produced displacement', replaySnap.player.position.y > world.spawn.position.y + 1.0, {
  spawnY: world.spawn.position.y,
  finalY: Number(replaySnap.player.position.y.toFixed(2)),
});
check('run exceeded 4.5 m/s proxy speed', maxSpeed > 4.5, { maxSpeed: Number(maxSpeed.toFixed(3)) });
check('camera yaw changed through input', cameraYawMaxDelta > 0.3, { maxDeltaRadians: Number(cameraYawMaxDelta.toFixed(3)) });
check('jump reached airborne height', maxZ > 0.25, { maxZ: Number(maxZ.toFixed(3)) });
check('landing returned to ground', replaySnap.player.grounded, { grounded: replaySnap.player.grounded, landCount: replaySnap.counters.landCount });
check('camera follows character', Math.hypot(replaySnap.camera.target.x - replaySnap.player.position.x,
  replaySnap.camera.target.y - replaySnap.player.position.y) < 0.001, { target: replaySnap.camera.target, player: replaySnap.player.position });
check('basic interaction registered', boundaryInteractionSeen && replaySnap.counters.interactCount >= 1, {
  used: [...game.usedInteractions], interactCount: replaySnap.counters.interactCount,
});
check('route progress advanced', routeProgressMax > 0.10, { maxProgress: Number(routeProgressMax.toFixed(3)) });

// 6. Isolated obstacle collision test: steer directly into a named tree.
const collisionGame = new TDDGame(world);
const tree = world.obstacles.find((o) => o.type === 'TREE');
collisionGame.state.position = {
  x: tree.x + tree.radius + world.character.radius + 0.06,
  y: tree.y,
  z: 0,
};
collisionGame.state.camera.yaw = 0;
collisionGame.updateCamera();
for (let i = 0; i < 60; i += 1) collisionGame.update(dt, makeInput({ right: -1, forward: 0 }));
const collisionSnap = collisionGame.snapshot();
const finalD = Math.hypot(collisionSnap.player.position.x - tree.x, collisionSnap.player.position.y - tree.y);
const minD = tree.radius + world.character.radius;
check('character collision resolves against tree', collisionSnap.counters.collisionCount > 0 && finalD >= minD - 0.02, {
  obstacle: tree.id,
  collisionCount: collisionSnap.counters.collisionCount,
  finalDistance: Number(finalD.toFixed(3)),
  minDistance: Number(minD.toFixed(3)),
});

// 7. Isolated jump/land test with fixed assertions.
const jumpGame = new TDDGame(world);
let jumpMaxZ = 0;
for (let i = 0; i < 12; i += 1) {
  jumpGame.update(dt, makeInput({ jump: true }));
  jumpMaxZ = Math.max(jumpMaxZ, jumpGame.state.position.z);
}
for (let i = 0; i < 120; i += 1) {
  jumpGame.update(dt, makeInput());
  jumpMaxZ = Math.max(jumpMaxZ, jumpGame.state.position.z);
}
const jumpSnap = jumpGame.snapshot();
check('isolated jump/land cycle', jumpSnap.counters.jumpCount >= 1 && jumpSnap.counters.landCount >= 1 && jumpMaxZ > 0.3 && jumpSnap.player.grounded, {
  jumpCount: jumpSnap.counters.jumpCount,
  landCount: jumpSnap.counters.landCount,
  maxZ: Number(jumpMaxZ.toFixed(3)),
  grounded: jumpSnap.player.grounded,
});

const overallPass = checks.every((c) => c.pass);
const report = {
  test: 'TDD Playable Adanna M1 — shared-simulation real-time integration test',
  date: '2026-11-19',
  overallPass,
  fixedStepHz: 60,
  replayFps,
  replayFrames: replayFrames.length,
  checks,
  finalSnapshot: replaySnap,
  events: game.events,
  classification: 'Automated fixed-step simulation of the same game.js module used by the live browser build; not a Unreal Engine cook/package test.',
  unrealStatus: {
    compileVerified: false,
    packageVerified: false,
    preciseBlocker: 'No Unreal Engine binary or recovered project version in this sandbox.',
  },
  nextAction: 'Run render_replay.py to produce frame captures/GIF/MP4 from these actual simulation states, then verify static/live build files.',
};
fs.writeFileSync(path.join(here, 'integration_report.json'), JSON.stringify(report, null, 2));
fs.writeFileSync(path.join(here, 'replay_frames.json'), JSON.stringify({
  worldVersion: world.worldVersion,
  fps: replayFps,
  frameCount: replayFrames.length,
  frames: replayFrames,
}, null, 2));
console.log(`[integration] ${checks.filter((c) => c.pass).length}/${checks.length} checks passed; ${replayFrames.length} replay frames at ${replayFps} fps`);
if (!overallPass) {
  for (const c of checks.filter((x) => !x.pass)) console.error('FAIL', c.name, c.detail);
  process.exitCode = 1;
}

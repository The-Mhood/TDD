import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { TDDGame, makeInput } from './game.js';

const canvas = document.getElementById('viewport');
const loading = document.getElementById('loading');
const loadingDetail = document.getElementById('loading-detail');
const hud = document.getElementById('hud');
const errorBox = document.getElementById('error');
const ui = {
  state: document.getElementById('state'),
  speed: document.getElementById('speed'),
  grounded: document.getElementById('grounded'),
  camera: document.getElementById('camera'),
  route: document.getElementById('route'),
  counters: document.getElementById('counters'),
  interaction: document.getElementById('interaction'),
  objective: document.getElementById('objective'),
  phase: document.getElementById('phase'),
};

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
renderer.setSize(window.innerWidth, window.innerHeight, false);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.18;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0d1512);
scene.fog = new THREE.FogExp2(0x2a332c, 0.018);
const camera = new THREE.PerspectiveCamera(64, window.innerWidth / window.innerHeight, 0.08, 300);
camera.up.set(0, 0, 1);

scene.add(new THREE.HemisphereLight(0x9fb4a2, 0x2b2018, 0.62));
scene.add(new THREE.AmbientLight(0x364038, 0.36));
const sun = new THREE.DirectionalLight(0xffdfad, 1.15);
sun.position.set(-12, -18, 28);
scene.add(sun);
const fill = new THREE.DirectionalLight(0x8fa8a0, 0.42);
fill.position.set(14, 10, 12);
scene.add(fill);

let game;
let characterRoot;
let mixer;
let actions = new Map();
let currentName = '';
let currentAction = null;
let lookAccumX = 0;
let lookAccumY = 0;
let dragging = false;
let lastMouseX = 0;
let lastMouseY = 0;
const keys = new Set();

function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

function configureMaterials(root) {
  root.traverse((obj) => {
    if (!obj.isMesh) return;
    obj.frustumCulled = false;
    const materials = Array.isArray(obj.material) ? obj.material : [obj.material];
    for (const mat of materials) {
      if (!mat) continue;
      mat.side = THREE.DoubleSide;
      if ('roughness' in mat) mat.roughness = Math.max(mat.roughness ?? 0.8, 0.82);
      if ('metalness' in mat) mat.metalness = Math.min(mat.metalness ?? 0, 0.15);
      mat.needsUpdate = true;
    }
  });
}

function buildActions(gltf) {
  mixer = new THREE.AnimationMixer(gltf.scene);
  for (const clip of gltf.animations || []) {
    const action = mixer.clipAction(clip);
    const oneShot = clip.name === 'jump' || clip.name === 'land';
    action.setLoop(oneShot ? THREE.LoopOnce : THREE.LoopRepeat, oneShot ? 1 : Infinity);
    action.clampWhenFinished = oneShot;
    action.enabled = true;
    actions.set(clip.name, action);
  }
  const idle = actions.get('idle');
  if (idle) {
    idle.play();
    currentAction = idle;
    currentName = 'idle';
  }
}

function chooseAnimation(snap) {
  let name = snap.player.animation;
  if (name === 'turn') name = snap.player.speed > 0.2 ? 'walk' : 'idle';
  if (!actions.has(name)) name = 'idle';
  if (name === currentName && currentAction) {
    if (name === 'walk' || name === 'run') {
      const base = name === 'walk' ? 2.8 : 5.6;
      currentAction.setEffectiveTimeScale(clamp(snap.player.speed / base, 0.55, 1.35));
    }
    return;
  }
  const next = actions.get(name);
  const previous = currentAction;
  if (previous) previous.fadeOut(0.12);
  next.reset();
  next.setEffectiveWeight(1);
  if (name === 'walk' || name === 'run') {
    const base = name === 'walk' ? 2.8 : 5.6;
    next.setEffectiveTimeScale(clamp(snap.player.speed / base, 0.55, 1.35));
  } else {
    next.setEffectiveTimeScale(1);
  }
  next.fadeIn(0.12).play();
  currentAction = next;
  currentName = name;
}

function inputState() {
  const forward = (keys.has('KeyW') || keys.has('ArrowUp') ? 1 : 0) - (keys.has('KeyS') || keys.has('ArrowDown') ? 1 : 0);
  const right = (keys.has('KeyD') || keys.has('ArrowRight') ? 1 : 0) - (keys.has('KeyA') || keys.has('ArrowLeft') ? 1 : 0);
  const input = makeInput({
    forward,
    right,
    run: keys.has('ShiftLeft') || keys.has('ShiftRight'),
    jump: keys.has('Space'),
    interact: keys.has('KeyE'),
    lookX: clamp(lookAccumX, -4, 4),
    lookY: clamp(lookAccumY, -3, 3),
  });
  lookAccumX = 0;
  lookAccumY = 0;
  return input;
}

function updateHud(snap) {
  ui.state.textContent = snap.player.animation.toUpperCase();
  ui.speed.textContent = `${snap.player.speed.toFixed(2)} m/s proxy`;
  ui.grounded.textContent = snap.player.grounded ? 'YES' : 'NO';
  ui.camera.textContent = `${snap.camera.distance.toFixed(2)} m / ${snap.camera.occluded ? 'OCCLUDED' : 'CLEAR'}`;
  ui.route.textContent = `${Math.round(snap.route.progress * 100)}%`;
  ui.counters.textContent = `${snap.counters.jumpCount} / ${snap.counters.landCount} / ${snap.counters.interactCount}`;
  ui.objective.textContent = snap.route.objectiveComplete
    ? 'ROUTE COMPLETE — Great Root Mother approach acknowledged'
    : 'Follow the white cloth to the Great Root Mother';
  if (snap.interaction.available) {
    ui.interaction.hidden = false;
    ui.interaction.textContent = snap.interaction.message;
  } else {
    ui.interaction.hidden = true;
  }
  ui.phase.textContent = document.pointerLockElement === canvas
    ? 'POINTER LOCKED · ESC RELEASES'
    : 'LIVE INPUT · CLICK TO CAPTURE MOUSE · DRAG ALSO LOOKS';
}

function onResize() {
  renderer.setSize(window.innerWidth, window.innerHeight, false);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
}
window.addEventListener('resize', onResize);

window.addEventListener('keydown', (e) => {
  if (['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.code)) e.preventDefault();
  keys.add(e.code);
});
window.addEventListener('keyup', (e) => keys.delete(e.code));
window.addEventListener('blur', () => keys.clear());

canvas.addEventListener('pointerdown', (e) => {
  dragging = true;
  lastMouseX = e.clientX;
  lastMouseY = e.clientY;
  if (canvas.requestPointerLock && document.pointerLockElement !== canvas) {
    canvas.requestPointerLock().catch(() => {});
  }
});
window.addEventListener('pointerup', () => { dragging = false; });
window.addEventListener('pointermove', (e) => {
  let dx = 0;
  let dy = 0;
  if (document.pointerLockElement === canvas) {
    dx = e.movementX || 0;
    dy = e.movementY || 0;
  } else if (dragging) {
    dx = e.clientX - lastMouseX;
    dy = e.clientY - lastMouseY;
    lastMouseX = e.clientX;
    lastMouseY = e.clientY;
  } else {
    return;
  }
  lookAccumX += dx * 0.06;
  lookAccumY += -dy * 0.04;
});
document.addEventListener('pointerlockchange', () => {
  if (document.pointerLockElement !== canvas) dragging = false;
});

async function loadJson(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url}: HTTP ${res.status}`);
  return res.json();
}

async function init() {
  const loader = new GLTFLoader();
  loadingDetail.textContent = 'Reading world and GLB assets…';
  const [world, forestGltf, characterGltf] = await Promise.all([
    loadJson('./world.json'),
    loader.loadAsync('./assets/forbidden_forest_m1.glb'),
    loader.loadAsync('./assets/adanna_m1_technical_proxy.glb'),
  ]);
  game = new TDDGame(world);

  const forest = forestGltf.scene;
  forest.name = 'FORBIDDEN_FOREST_M1_BLOCKOUT';
  configureMaterials(forest);
  scene.add(forest);

  characterRoot = new THREE.Group();
  characterRoot.name = 'ADANNA_M1_TECHNICAL_PROXY_ROOT';
  characterRoot.add(characterGltf.scene);
  configureMaterials(characterGltf.scene);
  scene.add(characterRoot);

  buildActions(characterGltf);
  loading.hidden = true;
  hud.hidden = false;
  console.info('[TDD M1] loaded', {
    forestNodes: Object.keys(forestGltf.parser?.json?.nodes || {}).length,
    characterAnimations: (characterGltf.animations || []).map((a) => a.name),
    worldVersion: world.worldVersion,
  });

  let last = performance.now();
  renderer.setAnimationLoop((now) => {
    const dt = Math.min(0.05, Math.max(1 / 240, (now - last) / 1000));
    last = now;
    const input = inputState();
    const snap = game.update(dt, input);
    characterRoot.position.set(snap.player.position.x, snap.player.position.y, snap.player.position.z);
    characterRoot.rotation.z = -snap.player.yaw;
    camera.position.set(snap.camera.eye.x, snap.camera.eye.y, snap.camera.eye.z);
    camera.up.set(0, 0, 1);
    camera.lookAt(snap.camera.target.x, snap.camera.target.y, snap.camera.target.z);
    chooseAnimation(snap);
    mixer.update(dt);
    updateHud(snap);
    renderer.render(scene, camera);
  });
}

init().catch((err) => {
  console.error(err);
  loading.hidden = true;
  hud.hidden = true;
  errorBox.hidden = false;
  errorBox.textContent = `Playable M1 failed to initialise.\n\n${err?.stack || err}\n\nConfirm the preview is serving web_build/ and that world.json plus both GLB assets are present.`;
});

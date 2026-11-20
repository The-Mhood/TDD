/* TDD — Playable Adanna M1 shared gameplay simulation.
 * Coordinate system: +X right, +Y forward, +Z up. Units are neutral gameplay
 * proxies, NOT approved story dimensions. This module is imported by the browser
 * build and by the Node integration/capture tests so both exercise the same code.
 */

export const FORWARD_ZERO = Object.freeze({ x: 0, y: 0 });

export function defaultInput() {
  return {
    forward: 0,
    right: 0,
    run: false,
    jump: false,
    interact: false,
    lookX: 0,
    lookY: 0,
  };
}

const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
const lerp = (a, b, t) => a + (b - a) * t;
const dist2 = (ax, ay, bx, by) => Math.hypot(ax - bx, ay - by);

function angleDelta(a, b) {
  let d = (a - b + Math.PI) % (Math.PI * 2);
  if (d < 0) d += Math.PI * 2;
  return d - Math.PI;
}

export class TDDGame {
  constructor(world) {
    this.world = world;
    this.time = 0;
    this.stepIndex = 0;
    this.events = [];
    this.usedInteractions = new Set();
    this.state = {
      position: { ...world.spawn.position },
      velocity: { x: 0, y: 0, z: 0 },
      yaw: world.spawn.yaw || 0,
      grounded: true,
      airborneTime: 0,
      landingTimer: 0,
      animation: 'idle',
      turning: false,
      speed: 0,
      limbPhase: 0,
      camera: {
        yaw: world.spawn.yaw || 0,
        pitch: 0.25,
        distance: world.camera.distance,
        desiredDistance: world.camera.distance,
        occluded: false,
        eye: { x: 0, y: 0, z: 0 },
        target: { x: 0, y: 0, z: 0 },
      },
      interaction: { available: false, target: null, message: '' },
      route: { index: 1, progress: 0, target: null, objectiveComplete: false },
      collisionCount: 0,
      cameraCollisionCount: 0,
      jumpCount: 0,
      landCount: 0,
      interactCount: 0,
    };
    this._prevJump = false;
    this._prevInteract = false;
    this.updateCamera();
    this.updateInteraction(false);
    this.updateRoute();
  }

  reset() {
    const world = this.world;
    this.time = 0;
    this.stepIndex = 0;
    this.events = [];
    this.usedInteractions = new Set();
    this.state = {
      position: { ...world.spawn.position },
      velocity: { x: 0, y: 0, z: 0 },
      yaw: world.spawn.yaw || 0,
      grounded: true,
      airborneTime: 0,
      landingTimer: 0,
      animation: 'idle',
      turning: false,
      speed: 0,
      limbPhase: 0,
      camera: {
        yaw: world.spawn.yaw || 0,
        pitch: 0.25,
        distance: world.camera.distance,
        desiredDistance: world.camera.distance,
        occluded: false,
        eye: { x: 0, y: 0, z: 0 },
        target: { x: 0, y: 0, z: 0 },
      },
      interaction: { available: false, target: null, message: '' },
      route: { index: 1, progress: 0, target: null, objectiveComplete: false },
      collisionCount: 0,
      cameraCollisionCount: 0,
      jumpCount: 0,
      landCount: 0,
      interactCount: 0,
    };
    this._prevJump = false;
    this._prevInteract = false;
    this.updateCamera();
    this.updateInteraction(false);
    this.updateRoute();
  }

  groundHeightAt(x, y) {
    const t = this.world.terrain;
    return t.amplitude * Math.sin(x * t.frequency + t.phase) * Math.cos(y * t.frequency * 0.87);
  }

  resolveCollision(px, py, pz) {
    const radius = this.world.character.radius;
    let hit = false;
    for (const o of this.world.obstacles) {
      if (pz > o.height - 0.15) continue;
      const dx = px - o.x;
      const dy = py - o.y;
      const d = Math.hypot(dx, dy);
      const minD = o.radius + radius;
      if (d < minD) {
        hit = true;
        const nx = d > 1e-5 ? dx / d : 1;
        const ny = d > 1e-5 ? dy / d : 0;
        px = o.x + nx * minD;
        py = o.y + ny * minD;
        const radial = this.state.velocity.x * nx + this.state.velocity.y * ny;
        if (radial < 0) {
          this.state.velocity.x -= radial * nx;
          this.state.velocity.y -= radial * ny;
        }
      }
    }
    const b = this.world.bounds;
    const bx = clamp(px, b.minX + radius, b.maxX - radius);
    const by = clamp(py, b.minY + radius, b.maxY - radius);
    if (bx !== px || by !== py) hit = true;
    if (hit) this.state.collisionCount += 1;
    return { x: bx, y: by, hit };
  }

  updateCamera() {
    const s = this.state;
    const c = s.camera;
    const w = this.world;
    c.yaw = (c.yaw + Math.PI * 2) % (Math.PI * 2);
    c.pitch = clamp(c.pitch, w.camera.minPitch, w.camera.maxPitch);
    const horizontal = Math.cos(c.pitch) * c.desiredDistance;
    const vertical = Math.sin(c.pitch) * c.desiredDistance + w.character.eyeHeight;
    const fx = Math.sin(c.yaw);
    const fy = Math.cos(c.yaw);
    const target = {
      x: s.position.x,
      y: s.position.y,
      z: s.position.z + w.character.eyeHeight,
    };
    let distance = c.desiredDistance;
    let occluded = false;
    // Sample the boom from target to desired eye; shorten at first obstacle hit.
    for (let i = 1; i <= 16; i += 1) {
      const t = i / 16;
      const sx = target.x - fx * horizontal * t;
      const sy = target.y - fy * horizontal * t;
      let blocked = false;
      for (const o of w.obstacles) {
        if (o.height < 1.0) continue;
        if (dist2(sx, sy, o.x, o.y) < o.radius + w.camera.collisionPadding) {
          blocked = true;
          break;
        }
      }
      if (blocked) {
        distance = c.desiredDistance * Math.max(0.28, (i - 1) / 16);
        occluded = true;
        s.cameraCollisionCount += 1;
        break;
      }
    }
    c.distance = distance;
    c.occluded = occluded;
    const h2 = Math.cos(c.pitch) * distance;
    const v2 = Math.sin(c.pitch) * distance + w.character.eyeHeight;
    c.eye = {
      x: target.x - fx * h2,
      y: target.y - fy * h2,
      z: target.z + v2 - w.character.eyeHeight,
    };
    c.target = target;
  }

  updateInteraction(pressed) {
    const s = this.state;
    let best = null;
    let bestD = Infinity;
    for (const it of this.world.interactables) {
      const d = dist2(s.position.x, s.position.y, it.x, it.y);
      if (d <= it.radius && d < bestD) {
        best = it;
        bestD = d;
      }
    }
    const edge = pressed && !this._prevInteract;
    s.interaction.available = !!best;
    s.interaction.target = best ? best.id : null;
    if (best && edge && !this.usedInteractions.has(best.id)) {
      this.usedInteractions.add(best.id);
      s.interactCount += 1;
      s.interaction.message = best.message;
      if (best.final) s.route.objectiveComplete = true;
      this.events.push({ time: Number(this.time.toFixed(3)), type: 'interaction', id: best.id, message: best.message });
    } else if (best) {
      const used = this.usedInteractions.has(best.id);
      s.interaction.message = used ? `${best.label}: acknowledged` : `${best.label}: press E`;
    } else {
      s.interaction.message = '';
    }
    this._prevInteract = pressed;
  }

  nearestRoute() {
    const pts = this.world.route.waypoints;
    const p = this.state.position;
    let best = { index: 1, distance: Infinity, t: 0 };
    for (let i = 0; i < pts.length - 1; i += 1) {
      const a = pts[i];
      const b = pts[i + 1];
      const vx = b.x - a.x;
      const vy = b.y - a.y;
      const len2 = vx * vx + vy * vy || 1;
      const t = clamp(((p.x - a.x) * vx + (p.y - a.y) * vy) / len2, 0, 1);
      const qx = a.x + vx * t;
      const qy = a.y + vy * t;
      const d = Math.hypot(p.x - qx, p.y - qy);
      if (d < best.distance) best = { index: i + 1, distance: d, t };
    }
    return best;
  }

  updateRoute() {
    const r = this.nearestRoute();
    const pts = this.world.route.waypoints;
    const idx = Math.min(r.index, pts.length - 1);
    const span = Math.max(1, pts.length - 1);
    const progress = clamp((idx - 1 + r.t) / span, 0, 1);
    this.state.route.index = idx;
    this.state.route.progress = progress;
    this.state.route.target = pts[idx];
    // Final waypoint counts as reached only when the interaction is used.
    this.state.route.objectiveComplete = this.usedInteractions.has('great_root_waymarker');
  }

  update(dt, input = defaultInput()) {
    dt = clamp(dt, 1 / 240, 1 / 20);
    const s = this.state;
    const w = this.world;
    const c = s.camera;
    this.time += dt;
    this.stepIndex += 1;

    c.yaw += (input.lookX || 0) * w.camera.lookSpeed * dt;
    c.pitch = clamp(c.pitch + (input.lookY || 0) * w.camera.lookSpeed * dt, w.camera.minPitch, w.camera.maxPitch);

    const fx = Math.sin(c.yaw);
    const fy = Math.cos(c.yaw);
    const rx = Math.cos(c.yaw);
    const ry = -Math.sin(c.yaw);
    let mx = fx * (input.forward || 0) + rx * (input.right || 0);
    let my = fy * (input.forward || 0) + ry * (input.right || 0);
    const mag = Math.hypot(mx, my);
    if (mag > 1) {
      mx /= mag;
      my /= mag;
    }
    const targetSpeed = (input.run ? w.character.runSpeed : w.character.walkSpeed) * Math.min(1, mag);
    const desiredVx = mx * targetSpeed;
    const desiredVy = my * targetSpeed;
    const accel = s.grounded ? w.character.groundAcceleration : w.character.airAcceleration;
    const alpha = Math.min(1, accel * dt);
    s.velocity.x = lerp(s.velocity.x, desiredVx, alpha);
    s.velocity.y = lerp(s.velocity.y, desiredVy, alpha);

    const jumpEdge = !!input.jump && !this._prevJump;
    if (jumpEdge && s.grounded) {
      s.velocity.z = w.character.jumpVelocity;
      s.grounded = false;
      s.airborneTime = 0;
      s.jumpCount += 1;
      this.events.push({ time: Number(this.time.toFixed(3)), type: 'jump' });
    }
    this._prevJump = !!input.jump;

    s.velocity.z -= w.character.gravity * dt;
    let px = s.position.x + s.velocity.x * dt;
    let py = s.position.y + s.velocity.y * dt;
    let pz = s.position.z + s.velocity.z * dt;

    const resolved = this.resolveCollision(px, py, pz);
    px = resolved.x;
    py = resolved.y;
    const ground = this.groundHeightAt(px, py);
    const wasGrounded = s.grounded;
    if (pz <= ground) {
      pz = ground;
      if (s.velocity.z < 0) s.velocity.z = 0;
      s.grounded = true;
      if (!wasGrounded) {
        s.landingTimer = 0.28;
        s.landCount += 1;
        this.events.push({ time: Number(this.time.toFixed(3)), type: 'land' });
      }
      s.airborneTime = 0;
    } else {
      s.grounded = false;
      s.airborneTime += dt;
      s.landingTimer = 0;
    }
    s.position = { x: px, y: py, z: pz };
    s.speed = Math.hypot(s.velocity.x, s.velocity.y);
    s.limbPhase = (s.limbPhase + dt * (2.2 + s.speed * 1.65)) % (Math.PI * 2);

    if (mag > 0.06) {
      const desiredYaw = Math.atan2(mx, my);
      const delta = angleDelta(desiredYaw, s.yaw);
      s.turning = Math.abs(delta) > 0.18;
      s.yaw += delta * Math.min(1, w.character.turnSpeed * dt);
    } else {
      s.turning = false;
    }

    if (s.landingTimer > 0) {
      s.landingTimer = Math.max(0, s.landingTimer - dt);
      s.animation = 'land';
    } else if (!s.grounded) {
      s.animation = 'jump';
    } else if (s.speed > w.character.walkSpeed * 1.35) {
      s.animation = 'run';
    } else if (s.speed > 0.18) {
      s.animation = 'walk';
    } else if (s.turning) {
      s.animation = 'turn';
    } else {
      s.animation = 'idle';
    }

    this.updateCamera();
    this.updateInteraction(!!input.interact);
    this.updateRoute();
    return this.snapshot();
  }

  snapshot() {
    const s = this.state;
    return {
      time: Number(this.time.toFixed(4)),
      step: this.stepIndex,
      player: {
        position: { ...s.position },
        velocity: { ...s.velocity },
        yaw: s.yaw,
        grounded: s.grounded,
        airborneTime: s.airborneTime,
        animation: s.animation,
        turning: s.turning,
        speed: Number(s.speed.toFixed(3)),
        limbPhase: s.limbPhase,
      },
      camera: {
        yaw: s.camera.yaw,
        pitch: s.camera.pitch,
        distance: s.camera.distance,
        desiredDistance: s.camera.desiredDistance,
        occluded: s.camera.occluded,
        eye: { ...s.camera.eye },
        target: { ...s.camera.target },
      },
      interaction: { ...s.interaction },
      route: { ...s.route },
      counters: {
        collisionCount: s.collisionCount,
        cameraCollisionCount: s.cameraCollisionCount,
        jumpCount: s.jumpCount,
        landCount: s.landCount,
        interactCount: s.interactCount,
      },
      events: this.events.slice(-6),
    };
  }
}

export function makeInput(partial = {}) {
  return { ...defaultInput(), ...partial };
}

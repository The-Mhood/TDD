#!/usr/bin/env python3
"""Render actual fixed-step gameplay states into screenshots, GIF and MP4.

The browser build and Node integration test both use game.js; this script reads
the resulting replay_frames.json and renders those exact camera/player states
with the same forest/character geometry exported to GLB/OBJ. These are frames
from the running simulation, not a Blender still or a GLB viewer screenshot.
"""
from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = HERE.parents[0]
WEB = BASE / "web_build"
CAP = WEB / "captures"
FRAMES = CAP / "frames"
sys.path.insert(0, str(ROOT / "TDD_PHASE3_PRODUCTION" / "HALL_OF_POSTS_M1" / "scripts"))
import build_hall_of_posts_m1 as m1  # noqa: E402

WIDTH, HEIGHT, FOV = 800, 450, 64.0


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'Bold' if bold else ''}.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def rot_x(a: float) -> np.ndarray:
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], dtype=float)


def rot_z(a: float) -> np.ndarray:
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)


def build_character_frame(parts_doc: dict, player: dict):
    phase = float(player["limbPhase"])
    anim = player["animation"]
    speed = float(player["speed"])
    if anim == "run":
        amp, crouch = 0.82, 0.0
    elif anim == "walk":
        amp, crouch = 0.44, 0.0
    elif anim == "jump":
        amp, crouch = 0.55, -0.03
    elif anim == "land":
        amp, crouch = 0.20, 0.14
    else:
        amp, crouch = 0.05, 0.0
    bob = (0.035 if anim == "walk" else 0.075 if anim == "run" else 0.0) * abs(math.sin(phase))
    yaw = -float(player["yaw"])  # forward +Y rotated by -yaw gives [sin(yaw), cos(yaw)]
    Rz = rot_z(yaw)
    p = np.asarray([player["position"]["x"], player["position"]["y"], player["position"]["z"]], dtype=float)

    V, F, C, E, S = [], [], [], [], []
    offset = 0
    for part in parts_doc["parts"]:
        v = np.asarray(part["vertices"], dtype=float)
        f = np.asarray(part["faces"], dtype=np.int64)
        origin = np.asarray(part["origin"], dtype=float)
        swing = float(part.get("swing", 0.0)) * amp * math.sin(phase + float(part.get("phase_offset", 0.0)))
        name = part["name"]
        if anim == "jump":
            if "UPPER_ARM" in name:
                swing = -0.95 if "LEFT" in name else 0.95
            elif "UPPER_LEG" in name:
                swing = 0.38 if "LEFT" in name else -0.38
        elif anim == "land":
            if "UPPER_LEG" in name:
                swing = 0.50 if "LEFT" in name else -0.50
        if abs(swing) > 1e-8:
            v = (v - origin) @ rot_x(swing).T + origin
        if part["bone"] == "Chest" and anim in ("walk", "run"):
            twist = 0.045 * amp * math.sin(phase)
            v = (v - origin) @ rot_z(twist).T + origin
        # Landing/crouch compresses about the feet.
        if crouch:
            v[:, 2] *= 1.0 - crouch * (0.25 + 0.75 * np.clip(v[:, 2] / 1.9, 0, 1))
        # Root yaw and world translation.
        v = v @ Rz.T + p + np.array([0.0, 0.0, bob - (0.08 if crouch else 0.0)])
        color = np.asarray(part["color"], dtype=np.uint8)
        V.append(v.astype(np.float32))
        F.append((f + offset).astype(np.int64))
        C.append(np.tile(color, (len(f), 1)))
        E.append(np.full(len(f), 0.0, dtype=float))
        S.append(np.full(len(f), 0.10 if "BRONZE" in name or "PENDANT" in name else 0.03, dtype=float))
        offset += len(v)
    return (
        np.vstack(V), np.vstack(F), np.vstack(C),
        np.concatenate(E), np.concatenate(S),
    )


def overlay_hud(image: Image.Image, frame: dict) -> Image.Image:
    img = image.convert("RGB")
    d = ImageDraw.Draw(img, "RGBA")
    p = frame["player"]
    c = frame["camera"]
    hud = frame.get("hud", {})
    counters = frame["counters"]
    # Top status strip.
    d.rectangle((0, 0, WIDTH, 54), fill=(8, 10, 13, 205))
    d.text((16, 10), "THE DISOBEDIENT DAUGHTER · PLAYABLE ADANNA M1", font=font(17, True), fill=(232, 205, 154, 255))
    d.text((16, 31), "REAL-TIME INTEGRATION · FORBIDDEN FOREST BLOCKOUT · TECHNICAL PROXY", font=font(10), fill=(170, 156, 132, 255))
    # Left state panel.
    d.rounded_rectangle((14, 66, 270, 186), radius=8, fill=(9, 12, 15, 175), outline=(110, 84, 48, 180), width=1)
    lines = [
        f"STATE      {p['animation'].upper()}",
        f"SPEED      {p['speed']:.2f} m/s proxy",
        f"GROUNDED   {'YES' if p['grounded'] else 'NO'}",
        f"CAMERA     {c['distance']:.2f} m / {'OCCLUDED' if c['occluded'] else 'CLEAR'}",
        f"ROUTE      {frame['route']['progress']*100:.0f}%",
        f"J/L/INT    {counters['jumpCount']}/{counters['landCount']}/{counters['interactCount']}",
    ]
    for i, line in enumerate(lines):
        d.text((26, 76 + i * 17), line, font=font(12, i == 0), fill=(222, 214, 190, 255))
    # Bottom objective / controls.
    d.rectangle((0, HEIGHT - 44, WIDTH, HEIGHT), fill=(8, 10, 13, 210))
    d.text((16, HEIGHT - 36), "OBJECTIVE  " + hud.get("objective", ""), font=font(12, True), fill=(230, 205, 154, 255))
    d.text((16, HEIGHT - 20), hud.get("controls", ""), font=font(10), fill=(165, 153, 132, 255))
    if frame["interaction"]["available"]:
        d.rounded_rectangle((WIDTH - 330, 68, WIDTH - 16, 110), radius=7, fill=(40, 29, 15, 220), outline=(190, 150, 82, 220), width=1)
        d.text((WIDTH - 316, 80), frame["interaction"]["message"], font=font(12, True), fill=(244, 218, 170, 255))
    # Phase badge.
    d.rounded_rectangle((WIDTH - 240, 12, WIDTH - 14, 42), radius=7, fill=(18, 24, 22, 210), outline=(90, 110, 88, 180), width=1)
    d.text((WIDTH - 228, 19), frame.get("phase", "").upper(), font=font(11, True), fill=(190, 210, 180, 255))
    return img


def make_contact_sheet(frames: list[Image.Image], labels: list[str], path: Path) -> None:
    tw, th = 480, 270
    pad, header = 14, 44
    sheet = Image.new("RGB", (tw * 2 + pad * 3, th * 2 + header * 2 + pad * 3), (10, 9, 8))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 10), "TDD — PLAYABLE ADANNA M1 · ACTUAL REAL-TIME SIMULATION FRAMES", font=font(19, True), fill=(232, 205, 154))
    for i, (img, label) in enumerate(zip(frames, labels)):
        x = pad + (i % 2) * (tw + pad)
        y = header + pad + (i // 2) * (th + header + pad)
        fitted = ImageOps.fit(img, (tw, th), Image.Resampling.LANCZOS)
        sheet.paste(fitted, (x, y))
        d.rectangle((x, y + th, x + tw, y + th + 30), fill=(16, 13, 11))
        d.text((x + 8, y + th + 7), label, font=font(13, True), fill=(218, 200, 165))
        d.rectangle((x, y, x + tw, y + th), outline=(90, 68, 40), width=1)
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


def make_review_sheet(source_paths: dict, hero: Image.Image, hud_frame: Image.Image, report: dict, path: Path) -> None:
    W, H = 1600, 1000
    sheet = Image.new("RGB", (W, H), (9, 8, 8))
    d = ImageDraw.Draw(sheet)
    d.text((34, 22), "THE DISOBEDIENT DAUGHTER — PLAYABLE ADANNA M1", font=font(30, True), fill=(232, 205, 154))
    d.text((34, 60), "APPROVED-SOURCE TECHNICAL PROXY · FORBIDDEN FOREST ROUTE · REAL-TIME INTEGRATION", font=font(13), fill=(170, 156, 132))
    d.line((34, 88, W - 34, 88), fill=(116, 84, 44), width=2)
    # Four panels: approved character, forest reference, actual frame, HUD/telemetry.
    panels = [
        ("SOURCE — APPROVED ADANNA MASTER", source_paths["adanna"]),
        ("SOURCE — FOREST REFERENCE", source_paths["forest"]),
        ("RESULT — ACTUAL SIMULATION FRAME", hero),
        ("RESULT — HUD / TELEMETRY", hud_frame),
    ]
    xs = [34, 820]
    ys = [112, 520]
    pw, ph = 746, 370
    for i, (label, img) in enumerate(panels):
        x, y = xs[i % 2], ys[i // 2]
        fitted = ImageOps.fit(img.convert("RGB"), (pw, ph), Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        sheet.paste(fitted, (x, y + 28))
        d.text((x, y), label, font=font(13, True), fill=(220, 195, 145))
        d.rectangle((x, y + 28, x + pw, y + 28 + ph), outline=(104, 76, 42), width=2)
    # Footer with verification.
    d.rectangle((34, 920, W - 34, 980), fill=(15, 12, 10), outline=(104, 76, 42), width=1)
    checks = report["checks"]
    passed = sum(1 for c in checks if c["pass"])
    d.text((48, 932), f"INTEGRATION: {passed}/{len(checks)} automated checks passed · 60 Hz shared simulation · {report['replayFrames']} replay frames at {report['replayFps']} fps", font=font(14, True), fill=(224, 205, 166))
    d.text((48, 956), "Verified: walk/run/turn/jump/land, camera follow + collision, character collision, ground detection, interaction, route progress.", font=font(12), fill=(168, 154, 132))
    d.text((1000, 932), "NOT VERIFIED: Unreal compile/cook/package", font=font(14, True), fill=(216, 140, 110))
    d.text((1000, 956), "Precise blocker: no UE binary/version in sandbox.", font=font(12), fill=(168, 154, 132))
    d.text((34, 982), "Adanna is a rigged technical gameplay proxy, not the final production character. Exploratory forest boards are not final approval.", font=font(11), fill=(135, 124, 108))
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path)


def main() -> int:
    started = time.time()
    FRAMES.mkdir(parents=True, exist_ok=True)
    for old in FRAMES.glob("frame_*.png"):
        old.unlink()
    replay = json.loads((WEB / "test" / "replay_frames.json").read_text(encoding="utf-8"))
    report = json.loads((WEB / "test" / "integration_report.json").read_text(encoding="utf-8"))
    world = json.loads((WEB / "world.json").read_text(encoding="utf-8"))
    parts_doc = json.loads((WEB / "internal" / "character_parts.json").read_text(encoding="utf-8"))
    static = np.load(WEB / "internal" / "render_scene.npz")
    Vs, Fs, Cs, Es, Ss = static["V"], static["F"], static["C"], static["E"], static["S"]
    shadows = [(o["x"], o["y"]) for o in world["obstacles"] if o["height"] >= 1.0]
    frames_out: list[Image.Image] = []
    print(f"[render] {len(replay['frames'])} frames from replay", flush=True)
    for i, frame in enumerate(replay["frames"]):
        Vc, Fc, Cc, Ec, Sc = build_character_frame(parts_doc, frame["player"])
        offset = len(Vs)
        V = np.vstack([Vs, Vc])
        F = np.vstack([Fs, Fc + offset])
        C = np.vstack([Cs, Cc])
        E = np.concatenate([Es, Ec])
        S = np.concatenate([Ss, Sc])
        renderer = m1.Renderer(V, F, C, E, S)
        eye = [frame["camera"]["eye"][k] for k in ("x", "y", "z")]
        target = [frame["camera"]["target"][k] for k in ("x", "y", "z")]
        img = renderer.render(eye, target, WIDTH, HEIGHT, supersample=1.0, fov=FOV)
        img = m1.postprocess(img, eye, target, WIDTH, HEIGHT, FOV, shadows, seed=i, shadow_strength=82)
        img = overlay_hud(img, frame)
        img.save(FRAMES / f"frame_{i:03d}.png")
        frames_out.append(img)
        if i % 20 == 0:
            print(f"[render] frame {i+1}/{len(replay['frames'])}", flush=True)

    # Hero and HUD stills.
    hero = frames_out[48] if len(frames_out) > 48 else frames_out[len(frames_out) // 2]
    hud_frame = frames_out[72] if len(frames_out) > 72 else frames_out[-1]
    hero.save(CAP / "playable_hero_frame.png")
    hud_frame.save(CAP / "playable_hud_frame.png")

    # Contact sheet from six representative simulation moments.
    indices = [0, 18, 42, 66, 90, min(119, len(frames_out) - 1)]
    labels = []
    for idx in indices:
        f = replay["frames"][idx]
        labels.append(f"t={f['time']:.2f}s · {f['phase']} · {f['player']['animation']} · {f['player']['speed']:.1f} m/s")
    make_contact_sheet([frames_out[i] for i in indices], labels, CAP / "playable_contact_sheet.png")

    # Source review sheet.
    make_review_sheet({
        "adanna": Image.open(BASE / "references" / "CHAR_ADANNA_MASTER_REFERENCE_V001.jpg"),
        "forest": Image.open(BASE / "references" / "forest_establishing.jpg"),
    }, hero, hud_frame, report, CAP / "PLAYABLE_M1_REVIEW_SHEET.png")

    # Animated GIF from the actual simulation frames.
    gif_frames = [f.resize((480, 270), Image.Resampling.LANCZOS) for f in frames_out]
    gif_frames[0].save(CAP / "playable_replay.gif", save_all=True, append_images=gif_frames[1:],
                       duration=int(1000 / replay["fps"]), loop=0, optimize=True)

    # MP4 via bundled imageio-ffmpeg binary.
    mp4_status = "written"
    try:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        proc = subprocess.run([
            ffmpeg, "-y", "-loglevel", "error", "-framerate", str(replay["fps"]),
            "-i", str(FRAMES / "frame_%03d.png"), "-c:v", "libx264", "-crf", "23",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(CAP / "playable_replay.mp4"),
        ], capture_output=True, text=True, timeout=180)
        if proc.returncode != 0:
            mp4_status = f"failed: {proc.stderr.strip()[:300]}"
    except Exception as exc:  # pragma: no cover
        mp4_status = f"failed: {exc}"

    capture_manifest = {
        "source": "web_build/test/replay_frames.json — actual fixed-step game.js states",
        "frame_count": len(frames_out),
        "fps": replay["fps"],
        "resolution": [WIDTH, HEIGHT],
        "frames": "captures/frames/frame_000.png … frame_%03d.png" % (len(frames_out) - 1),
        "hero": "captures/playable_hero_frame.png",
        "hud": "captures/playable_hud_frame.png",
        "contact_sheet": "captures/playable_contact_sheet.png",
        "review_sheet": "captures/PLAYABLE_M1_REVIEW_SHEET.png",
        "gif": "captures/playable_replay.gif",
        "mp4": "captures/playable_replay.mp4",
        "mp4_status": mp4_status,
        "classification": "frames/video from running gameplay simulation, not Blender render or GLB viewer screenshot",
    }
    (CAP / "capture_manifest.json").write_text(json.dumps(capture_manifest, indent=2), encoding="utf-8")
    # Also expose review sheet at milestone root for presentation.
    shutil.copy2(CAP / "PLAYABLE_M1_REVIEW_SHEET.png", BASE / "PLAYABLE_M1_REVIEW_SHEET.png")
    print(f"[render] complete in {time.time() - started:.1f}s; mp4={mp4_status}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

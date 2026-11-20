#!/usr/bin/env python3
"""Adanna movement clips V1 (2026-11-29) - production animation DATA for the
shared HUMAN_BASE_PROPOSED 11-joint skeleton (works for Guard AND Adanna).
Format: joint -> (axis, angle_rad) per keyframe, same convention as
pipeline/test_deformation.py POSES (validated through that skinning code).
Clips: idle, walk, run (loops), dodge_left (one-shot), crouch_recover,
look_back (hold). Poses follow ADANNA_MOVEMENT_COMBAT_POSE_REFERENCE_V1.jpg.
Weapon poses: NONE (CQ-9 deferred). Export: JSON alongside this script.
"""
import json, os
def K(t, **pose): return {"t": round(t,3), "pose": {j:[a,round(v,3)] for j,(a,v) in pose.items()}}
CLIPS = {
 "idle": {"loop": True, "fps": 30, "keys": [
   K(0.0, spine=('x',0.02), head=('x',0.03)),
   K(1.2, spine=('x',0.045), head=('x',0.05), **{"upperarm.L":('z',-0.06),"upperarm.R":('z',0.06)}),
   K(2.4, spine=('x',0.02), head=('x',0.03))]},
 "walk": {"loop": True, "fps": 30, "keys": [
   K(0.0, **{"thigh.L":('x',-0.4),"shin.L":('x',0.2),"thigh.R":('x',0.32),"upperarm.L":('x',0.25),"upperarm.R":('x',-0.25)}),
   K(0.35, **{"thigh.L":('x',0.0),"shin.L":('x',0.4),"thigh.R":('x',0.0),"upperarm.L":('x',0.0),"upperarm.R":('x',0.0)}),
   K(0.7, **{"thigh.R":('x',-0.4),"shin.R":('x',0.2),"thigh.L":('x',0.32),"upperarm.R":('x',0.25),"upperarm.L":('x',-0.25)}),
   K(1.05, **{"thigh.R":('x',0.0),"shin.R":('x',0.4),"thigh.L":('x',0.0),"upperarm.R":('x',0.0),"upperarm.L":('x',0.0)}),
   K(1.4, **{"thigh.L":('x',-0.4),"shin.L":('x',0.2),"thigh.R":('x',0.32),"upperarm.L":('x',0.25),"upperarm.R":('x',-0.25)})]},
 "run": {"loop": True, "fps": 30, "keys": [
   K(0.0, spine=('x',0.16), **{"thigh.L":('x',-0.85),"shin.L":('x',0.5),"thigh.R":('x',0.65),"shin.R":('x',0.9),"upperarm.L":('x',0.6),"forearm.L":('z',-0.9),"upperarm.R":('x',-0.6),"forearm.R":('z',1.2)}),
   K(0.28, spine=('x',0.18), **{"thigh.L":('x',0.1),"shin.L":('x',1.1),"thigh.R":('x',-0.2),"shin.R":('x',0.4),"upperarm.L":('x',0.0),"upperarm.R":('x',0.0)}),
   K(0.56, spine=('x',0.16), **{"thigh.R":('x',-0.85),"shin.R":('x',0.5),"thigh.L":('x',0.65),"shin.L":('x',0.9),"upperarm.R":('x',0.6),"forearm.R":('z',1.2),"upperarm.L":('x',-0.6),"forearm.L":('z',-0.9)}),
   K(0.84, spine=('x',0.18), **{"thigh.R":('x',0.1),"shin.R":('x',1.1),"thigh.L":('x',-0.2),"shin.L":('x',0.4),"upperarm.R":('x',0.0),"upperarm.L":('x',0.0)}),
   K(1.12, spine=('x',0.16), **{"thigh.L":('x',-0.85),"shin.L":('x',0.5),"thigh.R":('x',0.65),"shin.R":('x',0.9),"upperarm.L":('x',0.6),"forearm.L":('z',-0.9),"upperarm.R":('x',-0.6),"forearm.R":('z',1.2)})]},
 "dodge_left": {"loop": False, "fps": 30, "keys": [
   K(0.0),
   K(0.22, spine=('z',0.28), **{"thigh.L":('x',-0.5),"shin.L":('x',0.65),"thigh.R":('x',0.25),"shin.R":('x',0.3),"upperarm.L":('z',-1.0),"upperarm.R":('z',0.7)}),
   K(0.55, spine=('z',0.05), **{"thigh.L":('x',-0.2),"shin.L":('x',0.3)}),
   K(0.85)]},
 "crouch_recover": {"loop": False, "fps": 30, "keys": [
   K(0.0, spine=('x',0.5), **{"thigh.L":('x',-1.15),"shin.L":('x',1.35),"thigh.R":('x',-1.05),"shin.R":('x',1.3),"upperarm.L":('z',-0.5),"upperarm.R":('z',0.5)}),
   K(0.7, spine=('x',0.2), **{"thigh.L":('x',-0.5),"shin.L":('x',0.6),"thigh.R":('x',-0.45),"shin.R":('x',0.55)}), K(1.3)]},
 "look_back": {"loop": False, "fps": 30, "keys": [
   K(0.0), K(0.5, spine=('y',-0.4), head=('y',-0.55)), K(1.6, spine=('y',-0.4), head=('y',-0.55))]}
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ADANNA_MOVEMENT_CLIPS_V1.json")
json.dump({"skeleton":"HUMAN_BASE_PROPOSED (11 joints)","convention":"joint->[axis, angle_rad], as pipeline/test_deformation.py","clips":CLIPS}, open(out,"w"), indent=2)
print("wrote", out, list(CLIPS))

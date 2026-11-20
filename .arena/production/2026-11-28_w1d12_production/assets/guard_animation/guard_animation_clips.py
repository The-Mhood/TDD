#!/usr/bin/env python3
"""Guard animation clips V1 (2026-11-28) - production animation DATA for the
shared HUMAN_BASE_PROPOSED 11-joint skeleton (works for Guard AND Adanna).
Format: joint -> (axis, angle_rad) per keyframe, same convention as
pipeline/test_deformation.py POSES (validated through that skinning code).
Clips: idle (loop), patrol_walk (loop), alert (hold), hit_react (one-shot),
defeat (one-shot). Poses follow GUARD_POSE_REFERENCE_V1.jpg (approved set).
Weapon poses: NONE (CQ-9 deferred). Export: JSON alongside this script.
"""
import json, os
def K(t, **pose): return {"t": round(t,3), "pose": {j:[a,round(v,3)] for j,(a,v) in pose.items()}}
CLIPS = {
 "idle": {"loop": True, "fps": 30, "keys": [
   K(0.0, spine=('x',0.02), head=('x',0.03)),
   K(1.2, spine=('x',0.045), head=('x',0.05), **{"upperarm.L":('z',-0.06),"upperarm.R":('z',0.06)}),
   K(2.4, spine=('x',0.02), head=('x',0.03))]},
 "patrol_walk": {"loop": True, "fps": 30, "keys": [
   K(0.0, **{"thigh.L":('x',-0.55),"shin.L":('x',0.25),"thigh.R":('x',0.45),"upperarm.L":('x',0.35),"upperarm.R":('x',-0.35), "head":('y',0.18)}),
   K(0.4, **{"thigh.L":('x',0.0),"shin.L":('x',0.55),"thigh.R":('x',0.0),"shin.R":('x',0.1),"upperarm.L":('x',0.0),"upperarm.R":('x',0.0), "head":('y',0.18)}),
   K(0.8, **{"thigh.R":('x',-0.55),"shin.R":('x',0.25),"thigh.L":('x',0.45),"upperarm.R":('x',0.35),"upperarm.L":('x',-0.35), "head":('y',0.18)}),
   K(1.2, **{"thigh.R":('x',0.0),"shin.R":('x',0.55),"thigh.L":('x',0.0),"shin.L":('x',0.1),"upperarm.R":('x',0.0),"upperarm.L":('x',0.0), "head":('y',0.18)}),
   K(1.6, **{"thigh.L":('x',-0.55),"shin.L":('x',0.25),"thigh.R":('x',0.45),"upperarm.L":('x',0.35),"upperarm.R":('x',-0.35), "head":('y',0.18)})]},
 "alert": {"loop": False, "fps": 30, "keys": [
   K(0.0), K(0.25, spine=('x',0.14), head=('x',-0.06), **{"upperarm.L":('z',-0.85),"forearm.L":('z',-0.7),"upperarm.R":('z',0.85),"forearm.R":('z',1.4),"thigh.L":('x',-0.22),"shin.L":('x',0.3),"thigh.R":('x',0.18),"shin.R":('x',0.25)}),
   K(1.0, spine=('x',0.14), head=('x',-0.06), **{"upperarm.L":('z',-0.85),"forearm.L":('z',-0.7),"upperarm.R":('z',0.85),"forearm.R":('z',1.4),"thigh.L":('x',-0.22),"shin.L":('x',0.3),"thigh.R":('x',0.18),"shin.R":('x',0.25)})]},
 "hit_react": {"loop": False, "fps": 30, "keys": [
   K(0.0), K(0.18, spine=('x',-0.32), head=('x',-0.35), **{"upperarm.R":('z',1.5),"forearm.R":('z',0.5),"upperarm.L":('z',-0.5),"thigh.R":('x',0.3),"shin.R":('x',0.2)}),
   K(0.6, spine=('x',-0.1), head=('x',-0.1), **{"upperarm.R":('z',0.6),"thigh.R":('x',0.1)}), K(1.0)]},
 "defeat": {"loop": False, "fps": 30, "keys": [
   K(0.0), K(0.5, spine=('x',0.25), **{"thigh.L":('x',-0.5),"shin.L":('x',0.9),"thigh.R":('x',-0.3),"shin.R":('x',0.7)}),
   K(1.1, spine=('x',0.62), head=('x',0.45), **{"thigh.L":('x',-1.35),"shin.L":('x',1.45),"thigh.R":('x',-1.2),"shin.R":('x',1.4),"upperarm.L":('z',-0.4),"forearm.L":('z',-0.3),"upperarm.R":('z',0.45),"forearm.R":('z',0.35)})]}
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GUARD_ANIMATION_CLIPS_V1.json")
json.dump({"skeleton":"HUMAN_BASE_PROPOSED (11 joints)","convention":"joint->[axis, angle_rad], as pipeline/test_deformation.py","clips":CLIPS}, open(out,"w"), indent=2)
print("wrote", out, list(CLIPS))

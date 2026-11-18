# M1 — Adanna: First Playable Implementation

## Objective and scope

Deliver a verified playable Adanna who can be launched, controlled in a real 3D test space, navigate obstacles using implemented movement, and interact with the world. This is a gameplay/character milestone only; M2 environment production and M3 combat remain out of scope.

## Architecture reviewed before changes

- The canonical root project is the single-module `TheDisobedientDaughter` UE 5.8 project.
- `ATDDGameMode` previously declared no player classes. There was no project-owned player pawn, controller, input mapping, camera, interaction interface, authored map, or `Content/` asset tree.
- Existing dodge work consists of pure distance math and a capsule-sweep clearance preflight. The sweep does not move the character, validate/correct destination floor, or implement dodge state/cancellation.
- The module currently depends only on `Core`, `CoreUObject`, and `Engine`; this first increment uses the engine's legacy configurable input mappings and introduces no new module dependency.
- The owner reports M0 passed on commit `e71401b674ac5987b4eed6f46330b8b22c09e9b2`. That evidence applies to that commit, not to subsequent M1 changes.

## Dependency-ordered implementation sequence

| Increment | Work and dependency | Current status / exit evidence |
|---|---|---|
| **M1.1 Player foundation** | Adanna `ACharacter`, game-mode possession, player controller, keyboard/mouse/gamepad bindings, camera-relative locomotion input, jump, third-person collision-tested camera. No art asset required for the code contract. | **Implemented in source in this increment.** New Automation coverage checks class wiring, movement orientation, and camera setup. Awaiting owner-Mac compile and Automation evidence. |
| **M1.2 Movement actions** | Build on M1.1. Integrate dodge into CharacterMovementComponent rather than teleporting from the preflight sweep. Implement the M1 §3.5 destination-floor check/correction: safety margin only, walkable landing, >10 cm floor difference triggers up to three iterative distance reductions. Add interruption and collision/repeatability coverage. | Pending; current sweep remains a pre-movement query only. |
| **M1.3 Repeatable movement lab** | Requires the pawn and movement action contract. Add a real 3D graybox test space with PlayerStart, ground, slopes/steps, and blocking obstacles; test walk, jump, dodge, collision, and camera obstruction there. | Pending; no project-authored map or Content assets currently exist. |
| **M1.4 Adanna visual and animation integration** | Requires the approved Adanna mesh/rig and animation assets, with their source/status confirmed against the production Art Bible. Connect locomotion/jump/fall/land transitions without making animation authoritative for movement. | Pending; no character mesh or animation assets are present in the project checkout. Do not call a capsule, primitive, or unapproved mesh “Adanna complete.” |
| **M1.5 World interaction** | Define an interactable contract and player query/selection after basic movement and the lab route exist; validate range, visibility/occlusion, availability, and result. Add a real test actor and Automation coverage. | Pending; no interaction implementation exists. |
| **M1.6 Integrated M1 acceptance** | Use the approved character and repeatable lab to verify launch/possession, responsive controls, movement/traversal, camera, animation, grounding/collision, and interaction; record Mac build, Automation, and manual play evidence at the exact commit. | Pending. No M1 completion claim until this evidence exists. |

## Increment M1.1 deliverables in this change

- `ATDDAdannaCharacter`: camera-relative movement axes, jump press/release, orient-to-movement behavior, spring-arm follow camera with collision testing.
- `ATDDPlayerController`: game-only input mode and hidden cursor.
- `ATDDGameMode` now selects the project character and controller.
- `Config/DefaultInput.ini`: configurable WASD, mouse look, and Space jump mappings.
- `TDD.M1.Player.PlayableCharacterDefaults`: Unreal Automation coverage for GameMode wiring, camera setup, and movement orientation.

This is a playable-code foundation, not a first-playable build: no approved Adanna visual asset, movement lab, integrated dodge, interaction, Unreal compile, or post-M1 Mac verification is yet evidenced.

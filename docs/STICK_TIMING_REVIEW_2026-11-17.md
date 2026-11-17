# Timing pass: anticipation, loss of support and travel
Date: 2026-11-17. Status: internal, needs further review.

## Reference evidence
The creator's original Animator vs. Animation from https://www.newgrounds.com/portal/view/316541 was sampled locally over source intervals 3–9 and 16–22 seconds at 3 fps. The first interval mainly shows the character being drawn and a UI dialogue; it was not useful evidence of anticipation. The second sheet shows visibly different compressed, extended/airborne and landing poses, plus action involving an object. These are sampled frames, not continuous viewing or sound analysis. Filter frame-center timestamps were not separately verified. No reference frames, choreography or assets are included in the implementation.

## Prior defects
The source used the same smooth start/stop curve for every body segment. Consequently the root came nearly to rest at each stair contact and the slip decelerated into its endpoint. The head and reaching hands began together. Feet continued pointing right after the body turned left. Adding a preload revealed a knee–elbow overlap at 2.78 seconds in the displayed browser preview.

## Changes
- Delay the initial reach until 0.35 seconds while the head/body begin inspection.
- Add a loaded pose at 2.78 seconds, moving toward the gate before the backward pull.
- Accelerate the 3.8–4.15-second loss of support into its contact pose.
- During recovery, hold the head briefly, turn it over 6.0–6.2 seconds, then hold before body travel.
- Carry the root through stair contacts while feet keep their planted/lifted trajectories.
- Rotate toes toward the chosen route with constant foot length.
- Lower the bracing foot from y=720 to y=770 and adjust the strain pelvis to maintain reach. The displayed load/strain poses then separate the raised knee from the pulling elbows.

## Checks actually completed
All seven local Node tests passed, including 436 geometry samples, existing contact/length invariants, delayed reach, preload direction, acceleration into impact, nonzero root velocity through four stair boundaries, and fixed-length foot turns. A 1,451-sample reach check before the final lower-brace adjustment found no clamps; the final source passes all 436-frame Node checks. The offline builder ran.

Final bundled source HTML SHA-256: 75d4f3d8f6eefe87ad6583ec3a0d52b849fea46852c75f33c131da17fe710ce1. This is a source hash, not a video hash.

The final browser preview was displayed at 2.78 and 3.5 seconds after the brace correction. Running-preview screenshots showed clocks 2.63, 3.42, 4.13, 5.78, 8.91 and 14.05 seconds. Earlier candidate poses were also inspected at 4.0 and 6.4 seconds. This establishes selected silhouettes and observed running-preview states, not continuous encoded-video or auditory review.

## Next verification
CI now renders this exercise at 1920×1080 and 30 fps rather than the former half-size 15 fps. It verifies 435 frames, 14.5-second duration and successful full decoding, and extracts additional contact/turn review frames. CI results must be checked before claiming encoding success for this revision. Full temporal comparison, sound, other references, independent critique and the narrated pilot remain pending. The full-rate render does not grant creative approval.

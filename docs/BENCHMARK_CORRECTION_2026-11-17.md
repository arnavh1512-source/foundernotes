# Benchmark correction: performance before delivery
Owner feedback: 2026-11-17. The owner rejected the small motion studies and asked the studio to inspect benchmarks independently, identify missing qualities, and improve privately. Do not send another micro-test as a finished result.

## Newly accessed benchmark
The creator's original Animator vs. Animation was accessible on https://www.newgrounds.com/portal/view/316541 through its normal video option. Browser verification completed naturally; no puzzle was solved by the assistant and no access restriction was bypassed. The author account is noogai. The page identifies the original work and its author.

The public media was downloaded through the browser's documented media-download capability for internal analysis only. The file probe reported 988 x 720, 16 fps, 118.125 seconds with an audio stream. An overview sheet sampled the film at six-second intervals. These are decimated frame samples, not a continuous viewing or an audio review. The exact frame-center timestamps were not separately verified; do not invent them. No reference footage, frames, sound or project assets are committed to FounderNotes or reused in an output.

## Frame-supported comparison
The benchmark samples show substantially changing silhouettes: compressed, extended, airborne and braced poses; characters interact with interface objects rather than merely accompanying them. Objects and character positions change across the sampled situations. That is evidence of a much broader physical and narrative vocabulary than our gate test. It does not establish precise timing or sound quality.

Our own 12-second study keeps most of the spine/head arrangement nearly fixed while arms do the main work. Its closed gate supplies little consequential physical feedback. A second character points rather than the protagonist discovering an actionable solution. There is no meaningful escalation beyond a simple pull. Small facial cues, extra contact sounds and more frames do not solve these structural weaknesses.

## Required changes
1. Define readable intent in the main pose before interpolating limbs.
2. Give the protagonist agency: inspect, try, adapt, fail physically, recover, notice, choose.
3. Change the whole body's support and line of action during force, failure and recovery.
4. Keep contact points attached to the same moving prop and preserve planted support.
5. Make the obstacle respond visibly while remaining locked; do not imply that perception magically removes it.
6. Give a discovery and its payoff actual screen action.
7. Inspect the complete encoded motion and listen before judging either; retain reference limitations.
8. Keep work internal until the animation makes a substantial qualitative improvement. Do not equate unit tests with artistic progress.

## Implementation prepared
A new draft uses the existing motion HTML renderer contract and imports progress / solveArm from the repo's story-motion.mjs. It supplies a pose track for the pelvis, curved spine, head, hands and feet, with bracing, strain, slip, catch, reassessment and a step toward an alternative. The main support foot remains fixed through the force phase. Gate displacement is shared by the grip and brace contact. No reference choreography or assets are copied.

A pure JavaScript self-check executed in the tool orchestration runtime sampled 316 frames (30 fps over 10.5 seconds), checking 1,264 limbs for reach and lengths. Grip endpoints and support-foot positions were also checked. This is genuine geometry execution, not Node test-run or browser-render evidence.

The execution environment became unavailable after reference sampling. The HTML was not rendered, no soundtrack was created or heard, and the new scene is not creatively approved. Keep the implementation on a draft branch. Restore runtime access before any render, image inspection or full playback claim. The existing pilot, narrator, viewer-first and QC requirements remain in force.

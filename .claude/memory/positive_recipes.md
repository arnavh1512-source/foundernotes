# FounderNotes — tested positive recipes

This is a **newly initialized** learning file. Do not call a technique a winning recipe unless a concrete video or benchmark demonstrated its value, and an independent review was recorded. See `../skills/podcast-scout-skill/scripts/record_lesson.py`.

## Verified recipes

_No tested recipes recorded yet._

### night-1-part-2 — Natural talk acting: gestures start ~0.15 s before stressed words found in the real voice, hold, then relax to rest; listeners mostly still.

- Recorded (UTC): 2026-11-23T04:59:20+00:00
- Evidence: Frame sequences 0.3 s apart at 209-213 s and 785-791 s showed hold/change/rest pattern.
- Cause / rationale: Owner rejected looping gestures ('same gestures', then 'forced').
- Correction / recipe: tools/emph.py (RMS peaks with min spacing per character) + planFor/gestureAt in stick.html; spring in, slow relax, single damped beats instead of continuous shaking.
- Verification: Rendered 2026-11-22, QC 3.90% fast motion; awaiting owner viewing feedback.

### night-1-part-2 — Faces on the stick cast: 10 expressions, voice-driven mouths, blinking; philosopher mouth dark #2a1f3d so it shows on his white beard.

- Recorded (UTC): 2026-11-23T04:59:21+00:00
- Evidence: face-expressions-test.png reviewed by owner 2026-11-23; owner approved adding faces.
- Cause / rationale: Faceless figures could not show emotion; owner flagged the philosopher's smile as invisible in purple.
- Correction / recipe: engine/faces.js + LEXPR per line (speaker and listener) + SCENE_EXPR for narrator moments + ENV mouth envelope.
- Verification: Frame check of 16 times showed correct expressions; full render in progress.

### half-landing-a03-reel — Seamless Reel loop: end on the first frame and hide the reset inside the story

- Recorded (UTC): 2026-11-27T15:41:01+00:00
- Evidence: A03 Reel: last frame vs first frame 0.00% of pixels differ; A04/A06/A08 0.43-0.46%
- Cause / rationale: a loop shows a jump when the end state differs from the start (e.g. a fresh stain that wasn't there at frame 0)
- Correction / recipe: design the last shot to land on frame 0's exact pose and props; give the wardrobe an old stain where the new one appears (asset v2: it happens every sound check), so the fresh mark fades into it
- Verification: measured by ep_review.seam on all four Reels

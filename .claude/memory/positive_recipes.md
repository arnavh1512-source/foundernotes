# FounderNotes — tested positive recipes

This is a **newly initialized** learning file. Do not call a technique a winning recipe unless a concrete video or benchmark demonstrated its value, and an independent review was recorded. See `../skills/podcast-scout-skill/scripts/record_lesson.py`.

## Verified recipes

_No tested recipes recorded yet._

### stick-rebuild-cut-18 — Re-proportioning a keyed stick rig without breaking contacts

- Recorded (UTC): 2026-11-19T06:50:31+00:00
- Evidence: Cut 18: head 1/3.0 of height and legs 1.33x head (Alan AvA ~1/3 and ~1.25x) from a cut-14 baseline of 1/4 and 1.9x; 18 tests pass, 0 clamped limbs, 0 knee-below-floor frames
- Cause / rationale: Uniform scaling toward the feet left the stance as wide as before, so shorter legs could not reach; per-key narrowing would slide planted feet between keys
- Correction / recipe: Keep feet fixed; solve each key's hip along its original direction from the feet so the most-extended leg keeps its old extension; keep contact hands on their surface and lean the chest toward them; scale procedural pixel offsets and lift heights by the body factor; use hysteresis branch tracks for knees and elbows so joints switch sides only near full extension.
- Verification: Verified on cut 18 renders and tests. Owner review of the new proportions pending; wide-shot framing to be adjusted.

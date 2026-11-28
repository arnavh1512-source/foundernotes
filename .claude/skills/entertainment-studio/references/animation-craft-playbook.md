# Animation craft playbook (living document)

The owner's goal (2026-11-28): learn to make high-level animation by studying references and our own mistakes, and keep the
learning in this repo so each video starts from what the last one taught. Read this before planning or reviewing any
animation, together with `.claude/memory/mistakes_and_pitfalls.md` and `positive_recipes.md`.

## The learning loop (every reference the owner shares)

1. **Study at full size.** Frame sheets for the structure, then single frames at full resolution for the drawing:
   `ref_compare.py` (side by side at matched moments) and `rea-video` offline for cuts, sound and rhythm.
   Write down the *forms and tone planes*, not just the story beats.
2. **Recreate a short same-brief benchmark** (internal, never posted): same beats and timing, our own drawings.
3. **Compare at full size** with `ref_compare.py` at the key moments (opening, transitions, payoff, ending).
4. **List the gaps, biggest first,** fix one, re-render, compare again.
5. **Record** every verified mistake and recipe with `record_lesson.py` (evidence + whether the fix is verified), and update
   the scoreboard below. Push it, so the next session starts from here.
6. **Carry it into the real series** (Half Landing, Think! Shorts) and measure it there.

## Self-review before the owner sees anything

- Did I open the reference and our frames **at full size, side by side,** at the opening, every transition and the ending?
- Does the subject **stay continuous** across every cut (match cut, same silhouette, gradual state changes)?
- Is anything **frozen**? `ep_review.py` still_steps_pct (refs: 1.3%, ~1% over two frames). Every hold breathes.
- Is the face/character **built from forms** (ridge, socket, lids, planes) with light and shadow, or is it generic?
- Does every key action have **anticipation, contact and follow-through** (wind-up, impact frame, bounce)?
- Did precheck run clean (no page error) and are the frames I'm looking at **from this run**?
- Sound: each key moment audible on a phone and in sync (`ep_review.py`).

## What high-level animation does (measured from the owner's references)

**reference-ig-01, "inside a bump" (26 s, vertical, pixel art):**
- Payoff first (the bump), then rewind, slow replay, fast-forward with a ticking clock; one hard cut in 26 s.
- Transitions carry shape: the camera rolls so the bump dome *becomes* the cross-section dome; the healed dome becomes the
  forehead again and fades; a scan band reveals the inside.
- Faces are forms in tone planes: rim light, lit front, mid, terminator shadow, side plane, specular streaks; a brow ridge
  with a lit ledge and a shadow under it; the eye in its socket; **hard-edged planes** (cel), not airbrush.
- Something moves in 98.7% of frame steps (cells jitter, layers breathe).
- Labels: white noun + yellow verb, typed on, leader line to the actor.

**reference-ig-02, a studio's "five directing moves" promo (39 s):**
- Same drawing, directed vs undirected, split screen. The five moves: **light** (grade and glow), **camera** (framing that
  pushes in), **the breath** (idle life and anticipation before the action), **on twos** (hold each drawing two frames for a
  hand-made snap), **the hit** (an impact frame and shake on the key action).
- A 0/5 progress row keeps people watching; the fifth move is withheld as "?" for 4 s, then pays off with a flash and a
  full-screen launch. The narration stops for the payoff and the music changes section on the hit.
- Ends with a comment-a-keyword call to action (growth tactic; never fake view counts).

**reference-ig-03, a classic stick-fight scene (76 s, 1280x640):**
- Almost no holds: about 17% of frames repeat the previous one, but only ~1% stay still over two frames.
- Fast moves get **smears / ghost trails**; every 0.1 s the pose changes a lot (big spacing), with clear lines of action.
- Bodies and debris **persist** (fallen figures stay on the floor, dust and smoke linger): the world keeps its history.
- Long continuous takes with the camera panning across a line-art set; colour shifts (a teal grade) mark special moments;
  speech bubbles and small labels for jokes.

## Scoreboard (update after every benchmark)

| Date | Benchmark | Still steps (ref) | What improved | Biggest gap now |
|---|---|---|---|---|
| 2026-11-27 | bench-bump v1 | 7.3% (1.3%) | structure, clock, labels, loop | plain head; bump nearly invisible |
| 2026-11-28 | bench-bump v2 | 8.1% | bump grows from the outline; match-cut roll in/out | face still generic (owner) |
| 2026-11-28 | bench-bump v3 | 7.7% | face built from forms and tone planes; open/shut eye | soft gradients vs the reference's hard cel planes; section texture; upbeat music |

## Next practice items
1. Hard-edged cel planes (2-4 flat tones per form) for faces, the bump and the section layers.
2. Smears and ghost trails on fast Half Landing actions (from reference-ig-03).
3. Persistent world state: stains, debris and props stay where they land.
4. Anticipation, impact frame and follow-through on every gag beat.

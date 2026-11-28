# Animation craft playbook (living document)

The owner's goal (2026-11-28): learn to make high-level animation by studying references and our own mistakes, and keep the
learning in this repo so each video starts from what the last one taught. Read this before planning or reviewing any
animation, together with `.claude/memory/mistakes_and_pitfalls.md` and `positive_recipes.md`.

## The learning loop (every reference the owner shares)

1. **Study at full size.** Frame sheets for the structure, then single frames at full resolution for the drawing:
   `ref_compare.py` (side by side at matched moments), `ref_motion.py` (camera zoom/pan/roll with easing, holds, motion
   inside the picture, cuts; run it on ours too) and `rea-video` offline for cuts, sound and rhythm. Zoom into key actions
   at 30 fps (every frame) to see spacing, smears, contact holds and follow-through.
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


## Frame-level details (measured 2026-11-28 with `ref_motion.py` and full-frame close-ups)

**Camera grammar (reference-ig-01, 12 zoom/roll moves in 26 s; ours v3 had 9):**
- The camera never rests: slow push-ins and pull-backs alternate every 1.5-2.5 s during "holds" (1.27x in over 1.9 s while
  the clot forms; out to 0.6x over 1.4 s to reveal the pool; 2.9x in over 0.8 s to meet the macrophage; a slow 0.83x drift
  out; 0.37x pull-back over 1.2 s). Slow moves are ease in-out (half done at ~0.5).
- **Punch-in on impact:** 1.23x in 0.23 s right on the hit, easing out (slow end).
- **Into a transition, accelerate; out of it, decelerate:** the roll into the section turns 89 deg in 0.27 s while the zoom
  (3.9x) speeds up into the cut (half done at 77%); the roll back out decelerates (half done at 29%).
- A last small settle (0.89x over 0.7 s) before the loop.

**Impact anatomy (reference-ig-01, 0.0-0.6 s at 30 fps):** creep-in with small spacing (0-0.13 s) -> acceleration with a
hatched smear along the leading edge on the 2 fastest frames -> contact held for 3 frames with white and yellow spark rays
-> rebound -> two dotted rings expanding slowly over ~0.25 s -> visible dent -> the result (bump) starts ~0.3 s after contact,
with small tick marks pulsing around it.

**Fight anatomy (reference-ig-03, 26.1-27.0 s):** lunge in 4 frames -> contact -> grapple that is never still (bodies shift
every frame) -> a throw along an arc over ~6 frames -> **one translucent crescent smear** in the team colour on the fastest
frame -> dust puffs at the floor on landing that linger and fade over ~5 frames. Entrances arrive as a motion-blurred smear
for 3 frames, then snap sharp. Speech bubbles fade out over ~4 frames, never pop off. The camera nudges 60-130 px in
0.15-0.25 s bursts to follow the action and kicks back (zooms out ~0.86x) on big hits. No hold of 3+ frames in 76 s;
4.5% of frames repeat once (mostly on ones).

**The breath and on twos (reference-ig-02, rocket):** the rocket squats and rumbles with drifting smoke puffs for ~1 s, then
stretches up taller and settles; on the "on twos" step 11% of frames repeat (33 single repeats): each drawing held two frames.
Picture-wide local motion is only 1.7%: small, constant life is enough when the composition is calm.

**Where life lives (difference maps, `ref_compare.py --diff`):** in the reference every layer lights up between
frames t and t+2: each red cell moves a whole cell-width (a fast boil), fat outlines shimmer, marrow moves and the whole
section drifts. Shading measures (tone counts) are only valid on grain-free frames: our engine's film grain spreads flat
colours across many bins.

**Ours vs reference (same tool):** v3 local motion 2.3% vs 7.6%; v3 froze for up to 16 frames at the end vs a 9-frame max.

## Scoreboard (update after every benchmark)

| Date | Benchmark | Still steps (ref) | What improved | Biggest gap now |
|---|---|---|---|---|
| 2026-11-27 | bench-bump v1 | 7.3% (1.3%) | structure, clock, labels, loop | plain head; bump nearly invisible |
| 2026-11-28 | bench-bump v2 | 8.1% | bump grows from the outline; match-cut roll in/out | face still generic (owner) |
| 2026-11-28 | bench-bump v3 | 7.7% | face built from forms and tone planes; open/shut eye | soft gradients vs the reference's hard cel planes; section texture; upbeat music |
| 2026-11-28 | bench-bump v5-v6 | 5.6%; holds 3+: 0 | every element moves (cells tumble, fat shimmers, marrow jiggles, blood flows in vessels); flat tone planes; bump colour clipped to the swelling | local motion 3.7% vs 7.6%: reference cells 'boil' a whole cell-width per 2 frames and the frame drifts |
| 2026-11-28 | bench-bump v4 | 5.0%; holds 3+ frames: 0 (ref max 9) | measured camera grammar (10 moves vs 12) and impact anatomy copied in timing | motion inside the picture 2.8% vs 7.6%; hard cel planes; music |

## Next practice items
0. Raise motion inside the picture toward the reference (2.8% -> ~7%): more independent small movers (cells, particles, dust).
1. Hard-edged cel planes (2-4 flat tones per form) for faces, the bump and the section layers.
2. Smears and ghost trails on fast Half Landing actions (from reference-ig-03).
3. Persistent world state: stains, debris and props stay where they land.
4. Anticipation, impact frame and follow-through on every gag beat.

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

- **Directing first:** does every shot have a filled director's sheet (purpose, eye target, change, anticipation, key
  moment, camera motive, life, world memory, hand-over)? Does the shot still do its job if you mute it?

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



## Directing: the decisions behind the shots (owner focus, 2026-11-28)

What we are learning is **directing and details**. The measurements above are only a way to check them. For every shot, a
director decides: what the viewer should feel or ask, where their eye goes, what changes, why the camera moves, and how
the shot hands over to the next one.

### Shot-by-shot directing breakdown: reference-ig-01 ("inside a bump")
| Time | Shot | Director's decision | Why it works |
|---|---|---|---|
| 0-0.2 | Mallet looming top-left, eye open | Show the threat before the hit; the open eye is innocent | Anticipation: we know what will happen, so we lean in |
| 0.2-0.5 | Hit: smear, 3-frame contact, sparks, punch-in, eye shuts | Make one moment *hurt* with every tool at once | A single strong beat is remembered; the punch-in says "this matters" |
| 0.5-1.6 | Bump swells, throbs, clock ticks | Show the result the viewer recognises from life | The relatable payoff comes first, so the question "what's happening inside?" asks itself |
| 1.6-2.6 | Brackets lock on, camera rolls into the bump | Point at the subject, then go *into* it | Brackets tell the eye where to look; the roll turns outside into inside without a cut |
| 2.6-4.0 | REWIND, then SLOW replay inside | Answer "why" by replaying the cause | The same moment twice: first felt, then understood |
| 4-21 | One set, clock runs, one new actor at a time | Never two new things at once; each label is the next step of the story | The viewer is never lost; the clock gives a sense of progress |
| 7-17 | Push in to the actor, pull back to the result | The camera moves only to meet someone or to show consequences | Every camera move has a reason, so it never feels decorative |
| 21-23 | Back out to the face, small bump fading | Close the circle on the thing we first saw | Ending where we started makes the loop and the story feel complete |
| 23-24 | Scan band over the healed forehead | Prove the ending (inside is fixed too) | A last reveal rewards people who watched to the end |

### Directing principles drawn from the three references
1. **Show the result first, then explain it** (ref 1). A question beats a statement.
2. **One new thing at a time.** One actor, one label, one beat (ref 1, ref 2's 1/5...5/5).
3. **Every camera move has a motive:** meet someone, show a consequence, or punch a hit. No drifting for its own sake.
4. **Carry the subject across every transition** (the bump becomes the dome): the eye never has to search after a cut.
5. **Anticipation before every big action** (looming mallet; the rocket's rumbling squat; a fighter's wind-up).
6. **Make the key moment land with several tools at once:** smear, contact hold, sparks or dust, punch-in, sound, silence.
7. **Withhold the payoff** and make people wait for it (ref 2's "4/5 ?"; narration drops out for the launch).
8. **The world keeps its history** (ref 3): bodies, debris, stains stay where they land.
9. **Nothing is ever dead still**, but calm shots keep the motion small (ref 2's rocket breathes).
10. **End where you began,** changed: that is both the loop and the story.

### Director's sheet: fill in for every shot before drawing it
| Field | Question |
|---|---|
| Purpose | What should the viewer feel, ask or learn here? (one line) |
| Eye target | Where must the eye be, and what leads it there (contrast, motion, framing, brackets, a look)? |
| Change | What is different at the end of the shot from the start? |
| Anticipation | What warns us before the main action? |
| Key moment | Which frame must land, and which tools make it land (smear, hold, impact frame, punch-in, sound, silence)? |
| Camera motive | Why does the camera move (meet, reveal, punch) or why does it stay? |
| Life | What keeps moving in the background (steam, breath, cells, drips)? |
| World memory | What stays changed afterwards (stain, splat, debris)? |
| Hand-over | How does the shot pass the eye and the subject to the next one? |

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
| 2026-11-28 | bench-bump v7 + A04 rewind | bench 4.6% local motion (ref 7.6%); A04R 5.9%, holds 3+: 0 | boil on twos; impact grammar carried into Half Landing (punch-in, smear, landing kick) | full-frame drift; music; owner phone review |
| 2026-11-28 | bench-bump v5-v6 | 5.6%; holds 3+: 0 | every element moves (cells tumble, fat shimmers, marrow jiggles, blood flows in vessels); flat tone planes; bump colour clipped to the swelling | local motion 3.7% vs 7.6%: reference cells 'boil' a whole cell-width per 2 frames and the frame drifts |
| 2026-11-28 | bench-bump v4 | 5.0%; holds 3+ frames: 0 (ref max 9) | measured camera grammar (10 moves vs 12) and impact anatomy copied in timing | motion inside the picture 2.8% vs 7.6%; hard cel planes; music |

## Next practice items
0. Raise motion inside the picture toward the reference (2.8% -> ~7%): more independent small movers (cells, particles, dust).
1. Hard-edged cel planes (2-4 flat tones per form) for faces, the bump and the section layers.
2. Smears and ghost trails on fast Half Landing actions (from reference-ig-03).
3. Persistent world state: stains, debris and props stay where they land.
4. Anticipation, impact frame and follow-through on every gag beat.

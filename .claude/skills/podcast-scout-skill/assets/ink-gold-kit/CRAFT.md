# Craft sheet for animators (read before building a scene)

Distilled from the repos we studied (ClaudeAnimationBase, iart javascript-animation, anidoodle,
LottieFiles motion-design, stickman-director, OpenMontage ideas, manim/3b1b). Our own words.

## Timing = reads
- For every scene list the **reads** (what the viewer must understand, in order). Each read needs
  time to be found, understood, and to land before the next starts. One read at a time.
- **Fast actions, slow meanings.** Moves can be quick if anticipated; the meaning needs a hold.
- Lead the eye before an important read: the hunter looks at it, it lights up, or the camera moves to it.
- A line of on-screen text stays fully settled ≥ 0.3 s per word + 1 s.
- Cue every move to narration with `S.at("segment-id", fraction)` (fraction of that spoken line).

## Alive
- Nothing still for more than 2.5 s in the principal picture: something *meaningful* changes
  (a stroke draws a relationship, gold lands on the referent, a diagram step, a symbol transforms).
  Ambient (breath, camera drift ≤ 3 %/10 s) keeps holds alive but does not count as an event.
- Hunter always breathes (`K.alive(t, seed)`), blinks at uneven gaps (`K.blink`), and his eyes
  lead his head on turns.
- No twinning: left and right arms, multiple figures, multiple icons never move identically —
  offset by a few frames and vary amplitude.

## Motion
- Ease out on entry (`K.eo`), ease in on exit (`K.ei`), ease in-out for camera (`K.eio`). Never linear for movement.
- Anticipation before big moves (small opposite move ~25 %, 0.15–0.3 s). Settle after (overshoot ~6 %, at rest by 0.4 s) — `K.settle`.
- Follow-through: loose parts lag 2–3 frames.
- Stagger groups 80–120 ms; never more than 1/3 of elements moving at once; nothing travels > 1/3
  of the frame without a curve or a camera move.
- Three durations only: 0.45 s, 0.9 s, 1.4 s.

## Contacts & staging
- Held things touch the hand: place props with `hero.hand("F"|"B", S.world)`.
- Feet on the floor; objects rest on surfaces; nothing hovers unless that is the point.
- Hunter ≥ 40 % frame height in medium shots; use push-ins for emotion.
- Draw order back to front; nothing covers his face.

## Meaning of colour
- **Gold carries meaning**: the chase, the win, the one idea that matters in this shot. Never decoration.
- **Ember** = a cost or a warning (job two, crowding out). **Sea** = needs / well-being (sparingly).
- Cream for people and type. Fog for secondary text.
- Dust motes only where there is a real light beam, ≤ 25 particles.

## Explaining
- Show causality, not labels: things fill, fall, count, drift *because of* the previous thing.
- Progressive reveal: build a diagram in the order the narration names its parts.
- Transform rather than replace: morph the previous visual into the next idea where possible.
- Every on-screen claim has a source line (`K.source(S, "...")`) while it is visible.
- Charts: label "schematic — not real data" when they are illustrative; bars from zero.

## Seams
- Every scene opens on something already visible (no fade from black) and hands something
  over at its end (an object, a colour, a direction, a camera move) — listed in the storyboard.
- Vary transitions: match cut, push into an object, light change, hard cut on action. Dip only at chapter breaks.

## Text
- Labels: `K.label` (uppercase sans, gold or cream), ≤ 7 words. Quotes: `K.card` + serif. Titles: `K.title` + `K.words`.
- Keep y > 900 clear (soft captions sit there). Safe margins 96 px left/right.

## Check (mandatory)
- Render stills at the start, every read, every transition and the end; open them; fix overflow,
  collisions, floating props, faces covered, text too small, empty frames.
- Then render the clip and run `qc_video.py` on it with `--max-freeze 2.5`.

## Painted plates (p5.brush)
- Backgrounds (sky, walls, floors, hills) can be painted once with `K.paintPlate(S, (b, W, H) => {...}, seed)`
  — load `<script src="vendor/brush.js"></script>` before kit.js. Use `b.fill(col, opacity)` + `b.fillBleed(0.2–0.35)`
  + `b.fillTexture(0.4–0.6, 0.3–0.6)` for watercolour washes, `b.set("charcoal"|"HB"|"2B", col, w)` + `b.wiggle(1)` for lines.
- Paint darks and mid-tones only. Light sources stay SVG (`K.glow`, `K.beam`). Gold paint over blue turns green.
- A plate is static (painted once). Parallax/camera moves apply to the SVG layers only, so keep plates as far
  backgrounds and keep camera zoom on plates modest (≤ 5 %) — or apply the same CSS transform to the canvas.

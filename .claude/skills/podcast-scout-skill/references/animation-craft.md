# Animation craft for explainers

Numbers distilled from LottieFiles motion-design (MIT), manim_skill composer principles (MIT),
stickman-video-director QA, javascript-animation storyboard rules, and the motion skill's craft
reference. LottieFiles numbers are for UI; they are scaled here for 1080p video viewed on phones
and TVs (scaling is our editorial choice).

## Teaching rules (3Blue1Brown-style)

- Show, don't tell: every narrated mechanism has a visual that *does* the mechanism.
- Progressive revelation: build the diagram in the order the narration names its parts.
- Transform, don't replace: morph the old representation into the new one so the viewer sees
  the relationship (equation ↔ graph ↔ everyday example).
- Pose the question before the answer; give the viewer ~1 s to predict before the reveal.
- Pause for insight: a 0.8–1.5 s settled hold after an "aha" beat — with ambient motion only.
- One idea per shot; explainer shots 3–6 s; a scene = one storyboard beat = one narration segment.
- Recurring visual object or character carries continuity across scenes.

## Motion personality (pick one per channel; write it in channel-profile.md)

| Personality | Use for | Duration band (video) | Easing | Overshoot |
|---|---|---|---|---|
| Premium / calm (default for explainers) | science, ideas, history | 500–900 ms element moves, 900–1500 ms reveals | `cubic-bezier(0.4,0,0.2,1)` | 0 % |
| Corporate / clear | business, finance, tech | 400–700 ms | `cubic-bezier(0.2,0,0,1)` | 0–3 % |
| Playful | kids, light topics | 300–600 ms | ease-out-back | 10–20 % |
| Energetic | Shorts, hype intros | 200–450 ms | ease-out-expo | 15–30 % |

Brand motion identity: one signature easing for ~80 % of moves, exactly three durations
(quick / standard / slow), one entrance pattern.

## Hard rules

- Entrances decelerate (ease-out); exits accelerate (ease-in); on-screen moves ease-in-out;
  ambient loops sine in-out. **Never linear for spatial movement** (linear only for progress
  bars, timers, constant rotation).
- Entrances 30–50 % longer than exits. Distance scales duration (×1.3 at 2× distance, ×1.6 at 4×).
- Stagger lists 60–120 ms per item (video scale), total stagger ≤ 600 ms; same easing for all
  staggered items — vary only start time.
- 1/3 rules: nothing travels more than a third of the frame without an intermediate keyframe or
  camera move; with 3+ elements, at most a third move at once.
- Three layers per scene: primary (the teaching element), secondary (labels, arrows, underline
  50–100 ms after primary), ambient (subtle drift/boil) — a scene with only one layer reads as a slide.
- Hero leads and has the largest displacement; supporting elements enter from the same direction;
  dim non-hero elements to 40–60 % opacity when the hero speaks.
- Anticipation 10–20 % of the main action (a small counter-move first); settle holds 200–400 ms.
- Max **2.5 s** without meaningful change in the principal picture (qc_video flags freezes > 2.5 s).
- Hand-drawn lines "boil" by changing the wobble seed every ~4 frames at 30 fps, not every frame.
- Cuts and key moves land on narration word onsets or beat boundaries (use `timings.json`).

## Readability

- A line meant to be read stays fully settled for 0.3 s per word + 1 s.
- 1080p: body labels ≥ 40 px, titles 64–96 px; ≤ 7 words per label; max two typefaces.
- Safe margins: 5 % action-safe, 10 % title-safe on 16:9; Shorts keep text inside the central
  984×1500 area (120 px top, 300 px bottom, 96 px sides clear).
- Contrast ≥ 4.5:1 for text; never rely on colour alone; no flashing above 3 Hz.
- Captions sit in the bottom 15 %: keep that area free of key visuals in every scene.

## Data on screen

Exact numbers from the ledger, units labelled, source line (`Source: Org, Year`) for 3+ s, bars
from zero, count-ups end on the exact value and hold. A schematic diagram says "not to scale".

## Draft → polish loop

1. Draft the whole film: flat greys, one system font, boxes for art, correct timing.
2. Contact sheet (12–16 frames) + stills at each scene midpoint and mid-transition. Fix story first.
3. Polish one scene to final quality, approve the look, then apply it to the rest.
4. Two look-and-fix rounds minimum before final render.

# Craft library — what the studio learned from every repo

Our own synthesis (no copied text) of the projects the channel owner supplied: agency-agents,
anidoodle, huashu-art-motion, claude-drawing-skill, ClaudeAnimationBase, LunaAI motion-skill,
LottieFiles motion-design, HandDraw-Skill, manim_skill, javascript-animation-skills,
stickman-video-director, youtube-agent-skill, OpenMontage (ideas only, AGPL), voicebox, Obscura,
p5.brush and lemo-opuscar. Read the sections your stage needs. Numbers are starting points.

## 1. Direction (before any code)
- **Benchmark first.** Pick 1–2 reference works for *this* topic; write what to learn (pacing,
  camera grammar, colour logic, score shape) and what never to take (characters, shots, melodies).
- **Treatment with three structures.** Write three candidate shapes (journey, before/after,
  countdown, list that turns, myth → mechanism → truth), choose one and say why. The first idea
  for a style is usually its cliché.
- **Default psychology skeleton:** hook (≤ 15 % runtime) → the assumption/myth → hidden mechanism
  → the truth with its caveat → the usable takeaway. Hook ≤ 20 words, myth broken in one sentence.
- **One subject, one goal, one turn.** Every beat caused by the previous one ("but / therefore",
  never "and then").
- **One native move** at the emotional peak — something only this medium can do (in Ink & Gold:
  the gold thread becoming the transition, pooling when it stops, being unpicked and re-sewn).
- **The ending rhymes with the opening**: same place/pose/motif, changed.
- **Swap-the-title test**: if the video could belong to another topic by swapping the title, it is
  too generic. **Hero-spine test**: remove the signature device from a scene; if the scene still
  works, the device was decoration there.
- **Not the previous film**: at least 4 of 6 must differ from our last video and from any demo we
  learned from — structure, opening, signature shot, camera path, score shape, ending.

## 2. Timing and reads (the rule generated animation breaks most)
- Write the **reads** per shot (what the viewer must understand, in order). Each read needs time to
  be found, understood and to land; never two important reads at once.
- **Fast actions, slow meanings.** Moves may be quick if anticipated; meaning needs a hold.
- Lead the eye before a read (a look, light, a camera move, the element moving first).
- Text holds: ≥ 0.3 s/word + 1 s after it settles (≈ letters ÷ 15 + 1.5 s); title cards ≥ 4 s;
  subtitles ≥ 1.8 s and ≥ spoken line + 0.6 s.
- **Principal picture never inactive > 2.5 s** — a *meaningful* change (stroke, diagram step,
  symbol transform, gold landing on the referent). Ambient motion keeps holds alive but doesn't count.
- A visual change every 8–10 s at minimum; ≥ 3 scene types; never three same-type scenes in a row.
- Shot lengths: explainer 3–6 s per idea; story 2–5 s; contemplative 5–10 s.
- Vary pace: one clear acceleration, one deceleration, at least one held breath.

## 3. Camera, staging, seams
- ≥ 4 different camera moves per film (push, pull, pan, parallax drift, rack/blur focus, frame
  within frame) and one **signature shot** people remember. Zoom drift ≤ 3 % per 10 s on holds.
- Subject ≥ 1/3 frame height at key moments; ≥ 40 % in medium shots; clear silhouette.
- One world → screen function for anything that tracks a subject (iris, spotlight, follow cam).
- Every seam is designed: match cut, push into an object, light change, cut on action, J/L sound
  cut. Dip only at chapter breaks. Carry something across every cut; keep screen direction.
- Depth from overlap, scale and value (far = paler/bluer/smaller), never fake 3D on flat art.

## 4. Character performance
- Proportions: declare the canon (adult ≈ 7.5 heads; a stylised head may be enlarged, body stays
  real: thigh ≈ 24.5 %, shank ≈ 24.6 % of height). Short legs read as "weird" instantly.
- Joint limits: elbow 0–150°, knee 0–140°, hip −20…125°. Shoulder girdle rises as the arm lifts;
  don't outline where the arm overlaps the torso (it reads as a puppet seam).
- **Anticipation** ≈ 25 % of the move, 0.15–0.3 s, opposite direction. **Follow-through**: loose
  parts lag 2–3 frames per segment, each swinging ~15 % wider. **Settle**: overshoot 4–8 %, at rest
  by 0.3–0.5 s. Nothing stops dead.
- **Idle**: breathing period 3–4 s; blinks 0.1–0.15 s at uneven seeded gaps (2–5 s); eyes lead
  head turns; the head rides level through a stride.
- **No twinning**: arms, figures and icons never move identically — offset frames, vary amplitude.
- **Contacts**: held props sit between the palms, placed from hand anchors every frame; feet planted
  (walks built from footsteps, no sliding); objects rest on surfaces.
- Faces act, never snap: squint → swap → small take → settle. Check brow direction at final size
  ("worried" vs "angry" is one flip). Never draw a real person.

## 5. Motion design numbers
- Ease-out in, ease-in out, ease-in-out for camera; never linear for spatial movement.
- Personality: Premium/calm for our explainers — signature curve `cubic-bezier(.4,0,.2,1)`,
  three durations only (≈0.45 / 0.9 / 1.4 s), 0 % overshoot on type.
- Stagger 80–120 ms, total ≤ 600 ms; ≤ 1/3 of elements moving at once; nothing crosses > 1/3 of the
  frame without an arc or camera move. Three layers per scene: primary, secondary (50–100 ms late,
  30–50 % amplitude), ambient (10–20 %).
- Hand-drawn lines boil at ~7.5–12 changes/s with a seed per element — never every frame.
- Key-term entrance: arrive slightly large and soft, snap sharp in ~0.5 s.

## 6. Explaining visually
- Show causality, not labels: things fill, fall, count, drift *because of* the previous thing.
- Progressive reveal in the order the narration names parts; transform the previous visual into the
  next idea instead of replacing it; pose the question, give ~1 s to predict, then reveal.
- One persistent gauge/counter/motif across scenes turns a sequence into a chain.
- Metaphor in the picture, not a label beside it (concept → action → object).
- Charts: the question picks the chart; bars from zero; no dual axes or 3D; ≤ 7 colour-blind-safe
  colours; title states the takeaway; "schematic — not real data" on illustrative curves; source
  line visible with every claim. Never fake a study screenshot.

## 7. Look and texture
- One key light per scene; light is additive (glow) — in pigment media gold over blue turns green.
- Painted plates (p5.brush) for skies/walls/ground: watercolour fills with bleed 0.2–0.35 and texture
  0.4–0.6, charcoal/HB lines with a light wiggle. Value-ladder plates: pale far → near-black near.
- Rim light on the side facing the key (2–4 px, warm), never swallowing thin shapes.
- Grain is added in ffmpeg at assembly, not drawn per frame (page grain makes renders ~2× slower) — and only
  very lightly (`--grain 1–2`): per-frame random grain is incompressible and balloons file size (strength 5
  pushed a 5-minute 1080p master past 1.4 GB). Prefer painted texture in the plates over grain.
- Pitfalls: gold as decoration (if two things are gold, one is wrong); hard glints read as stickers;
  grey/violet skin under coloured light; a frozen frame reads as a bug; text on similar colours.

## 8. Voice
- Male narrator default; one voice per video and per channel; never clone a real person.
- Write for the ear: 8–20 words/sentence, numbers spelled out in the voice text and written as digits
  in captions, respell names in `text` and keep spelling in `display`.
- **ASR round-trip every line** (faster-whisper): re-take lines whose words drop. Short lines and
  names are often misheard by small models — pad 0.6 s or confirm by listening and record an override.
- Voice-performance plan per section (pace, pauses, emphasis); picture follows the voice, never the
  reverse; approve a ~20 s sample before the full render.

## 9. Music and sound
- Original score from real samples (lemo-opuscar sampler): VSCO 2 CE / VCSL (CC0), Salamander piano
  (CC BY 3.0 — exact credit line required). Write scores as events from the same timeline as the edit.
- Reflective explainers: piano motif, cello/viola pads, harp arpeggios, pizzicato walking bass,
  vibraphone/glockenspiel/hand chimes for insight beats. Avoid generic "piano and strings" washes;
  give each concept a recurring chord, replay them in the recap.
- **Two real silences** before the turn/peak; the first sound after a silence is one of the most
  important in the film. Use **J/L cuts** at least twice.
- Three layers: ambience bed, foley tied to actions, music. Voice compressed, then ~10 dB over music
  by RMS (score bed ≈ −20 dB under voice), music ducked −9 dB under voice (40 ms attack / 450 ms
  release). Master −14 LUFS, true peak ≤ −1 dBTP. Keep 20–120 Hz ≈ −3 dB vs the rest.
- Every visible action has a sound, matched to its material; SFX never louder than voice.

## 10. Captions, packaging, retention
- Captions: one line, semantic grouping (never split number+unit or before a preposition),
  0.7–7 s, ≤ 42 chars, appear ~0.15 s early; soft captions for long-form, burned-in for Shorts.
- First 15 s: confirm the title's promise, open a question the viewer can't close, prove a payoff.
  Score 5 hooks (`scripts/vendor/youtube-agent/hookscore.py`), keep the best honest one.
- Title + thumbnail are one unit; ≤ 60 chars; thumbnail ≤ 3 words that add to the title; build the
  thumbnail from a real frame style of the film.
- After publishing: diagnose retention as hook leak (first 30 s), cliffs (moments), or slide (pacing)
  with `yt-retention`-style analysis; fix one thing per video.

## 11. Review and delivery
- Look at real frames: contact sheet (1 frame / 1–2 s), stills at every read and transition, 0.2 s
  strips for key actions, crops of faces and hands. Two look-and-fix rounds minimum.
- Critic findings = location + problem + fix + severity (P0/P1/P2); "scan for the same class";
  max three rounds, then escalate. Reviewer defaults to NEEDS WORK; "cannot look" = FAIL.
- Viewer simulation: describe the film from the silent contact sheet alone — if the story isn't
  readable, the picture isn't doing its job.
- Deliver: MP4 + poster, .srt, TREATMENT.md, FACTS.md (claim → source → quoted wording), CREDITS
  (every asset and licence), and a one-command build script. The owner uploads.

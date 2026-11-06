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

- **Rotate backgrounds** (owner rule): no two adjacent scenes share a backdrop; ≥ 6 per film; pick by meaning. Presets in `assets/ink-gold-kit` (`K.backdrop`).

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
  0.7–7 s, ≤ 42 chars, appear ~0.15 s early. **Subtitles are burned in on every video** (channel rule; assemble.py does it by default, in the channel font) and the .srt sidecar is also uploaded as YouTube captions.
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

## 12. Lessons from collage-director (vox-ai-motion-graphics-generator, read in full)
Most of this costs nothing. It changes how we plan and direct, whatever the engine.
- **Two approval gates:** the beat map first, then the look. Before building a film, run a **style bake-off**: render the film's
  most important beat in 3–4 looks (backdrop × cast palette × type treatment, or collage themes) as stills, and let
  the owner pick. The look is locked before anything moves. Changing it after rendering costs a full re-render.
- **Arc library, as candidates for the treatment's three structures:**
  - `hook_payoff`: hook → context → build → payoff → wrap.
  - `pas`: problem → agitate → solve → proof → CTA.
  - `bab`: before → after → bridge.
  - `how_it_works`.
  - `timeline`.
  - `man_in_hole`: baseline → fall → deepening → ascent → resolution.
- **Hook in ≤ 3 s, on screen as well as spoken:** a bold headline, surprising statistic, mistake or direct question in the first shot.
- **Shot cadence:** cut or reframe every ~4–6 s.
  - Split each beat into 2 shots: a wide/establishing shot, then a close detail cut-in on the thing the narration names.
  - A scene longer than ~10 s needs internal cut-ins, i.e. camera reframes to the active element. This is more than fades within one framing.
- **Shot spec in the storyboard:** for every shot, record shot size, camera move, element motion and amplitude.
  - **Shot size:** `EST_WIDE`, `WIDE`, `MEDIUM`, `CLOSE`, `DETAIL`.
  - **Camera move:** exactly ONE per shot, from `static`, `push_in`, `pull_out`, `pan`, `tilt`, `parallax`. It is one continuous move that never loops, retracts or resets.
  - **Element motion:** what moves *inside* the frame, i.e. the energy. Several elements per shot.
  - **Amplitude:** `calm`, `punchy` or `max`. Pick by meaning and keep one per beat.
- **Designing for motion:**
  - high-contrast silhouettes on flat backgrounds;
  - text isolated on clean banners or cards, never over busy detail;
  - flat-safe camera moves only on flat art (no fake 3D rotation).
- **Mixed aspect ratios:** fill with a blurred, darkened copy of the clip instead of black bars (`assemble.py --fill blur`).
- **Cut-out compositing** (a real photo kept pixel-faithful as a "sticker" while the world around it is stylised; the "C-roll" mode):
  - use only for the owner's own photos or products we may show;
  - freeze the face or label layer;
  - put no print texture on faces.
- **Restyled talking head** ("A-roll" mode): if the owner ever records himself, ASR splits the take into ≤ 9.5 s beats at
  sentence ends or ≥ 0.35 s pauses (beats < 2 s are merged), then the world around him is restyled. His face and lip-sync stay untouched.

## 13. Lessons from pixelfx (patch-gg/pixelfx, MIT, read in full; ideas only, our own code)
- **An effect alone looks like a sticker. The body around it sells it.** Every action has a sequence (kit: `K.keys`, `K.act`):
  1. A wind-up the opposite way to the blow.
  2. A big silhouette change on the release frame ("snap").
  3. A **hit-stop** on contact that freezes the whole frame, with a small decaying shake. Heavier impacts freeze longer, 0.03–0.2 s.
  4. The target reacts.
  5. A follow-through that overshoots, then recovery.
  Use it for stamps, impacts, a counter landing on its number, a bar hitting its value, and doors.
- **Characters on twos.** Poses step at 12 fps (`K.onTwos(t)`) while light, particles and camera stay smooth.
  It reads as hand-animated instead of tweened. Use it per film as a style choice, and keep one cadence per film.
- **Separate colour from light.** Colour pixels and additive light are separate layers, so hot things look hot.
  Glow stays subtle (k 0.2–0.5), and white is only for the hottest core.
- **A 1–2 frame "hero frame"** of white or flash on the impact frame gives punch.
- **Motion symptom → fix:**
  - floaty → fast in, slow out, and a shorter total time;
  - stiff or mechanical → vary each element's size, speed, delay and life, and add secondary motion;
  - washed out → less glow and darker edge steps;
  - flat → light from one side;
  - a one-shot that pops off → let it shrink or dither out before it ends;
  - the action lands out of sync → put the key on the effect's own time constant, never on a time you eyeballed.
- **Drafts, not one-shots.** When direction is open, write 3–5 genuinely different takes, render all of them, and look before choosing.
- **Judge motion from consecutive frames** (12 fps steps or the MP4), not from a contact sheet's samples. Motion bugs don't show in samples.
- **Check before rendering.** `scripts/lint_scenes.py` checks the render contract (no Math.random, Date or rAF), that scene ids exist in timing,
  and the channel rules: no podcast names, a source line on numbers, the caption zone, rotating backdrops, and the film's cast.
- pixelfx itself (244 pixel-art effects, sprite sheets) suits a pixel-art or game-themed film. Running its code needs the
  owner's OK in this environment (external code).

## 14. Lessons from 703 viral code-made videos and a step-by-step motion tutorial
Sources: yihui-dev/awesome-opus5-5-videos (prompts and categories, analysed in full), and @janustiu's
"Claude motion videos, step by step" (7 styles, a base block, a fix table).

**What the best briefs have in common** (counts out of 703 prompts):
| Technique | Prompts |
|---|---|
| A beat grid ("something happens on every beat") | 49 |
| Springs with a tiny overshoot | 33 |
| A cursor or hand that drives the action | 31 |
| One continuous shot ("one shape, never cut") or match cuts | 31 |
| Morphing the same element between states | 29 |
| Real motion blur from averaged sub-frames | 28 |
| Sound synced to every action | 23 |
| Real data or a real simulation | 17 |

**How to apply them:**
- **One strong formal idea per scene, and one device for the film.** A recurring object or line carries every shot: our gold thread, or one ball. That object is what makes a film feel authored rather than like a list of effects.
- **Simulate the real thing where we can:** a random walk is an actual random walk, a distribution is drawn from data. State the uncertainty honestly.
- **Keep attention** with small gags, onomatopoeia and **callbacks** (an early image paying off late). A parallel timeline helps where it fits ("meanwhile on Earth…").
- **Transition grammar:**
  - content enters after its container starts moving, and leaves before the next move, so text never overlaps;
  - a short blur on transitions;
  - never fade black straight into the accent colour; move an accent element between states instead;
  - the camera zooms so each state fills the frame;
  - loops end on their first frame.
- **Springs:** closed-form, tiny overshoot. When a target changes again, add one spring per change rather than restarting.
- **Motion blur:** `motion/scripts/render.mjs --blur 3` renders 3 sub-frames across a 180° shutter and averages them. Use it on fast camera cut-ins, impacts and flights. It costs about 3× render time, so use it per scene, not by habit.
- **Write every style recipe the same way:**
  - **opening line:** what it is, its length and format;
  - **IDEA:** the one device;
  - **BEATS:** time ranges, what's on screen, the exact words;
  - **LOOK:** hex codes, type, texture;
  - **MOTION:** where it's fast, where it holds, how scenes hand over;
  - **SOUND:** tempo, instruments, and one sound per action.
- **Storyboard gate:** a beat map with timestamps plus 4 key stills before any build. Approve, then build.
- **Fix by timestamp, specifically:**
  - "Text at least 60 px tall at 1080 wide."
  - "Re-time the score so every hit lands on the exact frame."
  - "At 3 s only the top half is used: fill the frame."
  - "Too digital: add grain, line wobble and frame-to-frame jitter."
- **Before delivery:** watch on a phone; check the first second works with the sound off; make sure no text sits under the platform's buttons.

## 15. Lessons from "Claude Creative Skill Library Vol. 2" (landing page only; the skills themselves weren't included)
The six skills (3D animation, cartoon episodes, documentary, ad formats, paper-cut motion, commercial pipeline) drive
AI image and video generators. Their methods transfer to our code-made films:
- **Close a loop the brain needs closed.** Open a question in the first seconds and pay it off late. Plant one "remember this" mid-film.
- **Define the world once, then build every scene on it.** A series bible covers the channel's cast policy, palette, type,
  motifs, sound identity, chapter tracker and end card. The bible is `channel-profile.md` plus the kit; the per-film cast goes in CAST.md.
  Never redesign a character mid-film.
- **The documentary "case file":** chapters, an asset sheet for every character and location, one plan per scene *with its
  sound design*, and the narrator script. Our STORYBOARD rows should name each scene's sounds as well as its picture.
- **Lock one style and one character across every beat** of a format. A style change is a chapter-level decision, never a whim.
- **Paper-cut motion:** the scene assembles itself piece by piece (torn paper sliding in, layering, settling). `collage-director` covers this.
- **Lock every reference before assembling** (5–8 key frames). When something breaks, rewrite only that section; don't regenerate the whole film.
- **Finishing moves** in the cut: zoom-ins on the line that matters, and a small shake on impacts (`K.act`).

## 16. Lessons from two "studio-in-a-folder" packs (3D myth-buster shorts; cartoon episodes)
The owner shared each pack's CLAUDE.md, README and EXPLAINER, plus one finished production pack (a 30 s Trojan Horse
myth-buster). The skills themselves weren't included. Both packs write prompts for paid image/video generators that
the user runs; our channel draws in code, so we take the grammar, not the pipeline.
- **Four-beat myth script: MYTH → TWIST → MECHANISM (A, B) → KICKER.** 85 words carry a whole short. The kicker
  restates the myth's own words, turned ("Troy didn't fall to a horse. It fell to one silent night"). Use it for every
  Shorts cut, and as the spine of a long video's cold open.
- **Define once, reuse forever** ("whatever you don't define, the AI invents"). Their asset sheets are our CAST.md
  rigs, `K.FILM_BACKDROPS` and props built once in kit-loop.js. A **style formula pasted byte-identical** everywhere
  is our shared kit + palette; never restyle a prop per scene.
- **Shot lists with hard timecodes.** 9 hard cuts per 10 s, each ~0.6–1.4 s: macro → wide → low angle → close-up →
  x-ray → macro eye → POV pull-back. In our scenes that means a camera move or reframe every ~1 s inside a 5–8 s
  scene, not one static layout per sentence.
- **Glowing annotation that draws itself** around the hidden thing (the seam, the bar, the zero line), in ONE
  meaning-colour (green = "look here / evidence"), and a **red dashed path** for routes and sightlines →
  `K.trace(layer, d, {at})` and `K.dashPath(layer, d, {at})`.
- **Edit map: punch-ins and shakes on WORDS.** A draft map is written before voicing, then every punch moves to the
  twist/kicker word's timestamp once the narration exists → `K.punch(t, [{t: wordTime, z: 1.12}])` feeding
  `K.camera`; the ui layer stays still, so put zoomed annotations in `S.world`.
- **Open on motion, never a still** ("NEGATIVE: static freeze at start"); their first shot is a 0.6 s macro whip.
- **Characters emote, they don't lip-sync** in narrated films: acting and gesture carry the beat; the narrator talks.

## 17. Lessons from four prompt-pack skills (documentary, commercial pipeline, creative formats, paper-cut motion)
All four write prompts for paid image/video generators the user runs (Seedance, Nano Banana, GPT Image). We draw in
code, so the generation steps don't apply. The craft does, read in full and restated in our own words:
- **Documentary (case file).** Tell a myth test as a reconstructed TIMELINE: every scene carries a small monospaced
  stamp in a corner ("FILE · 2017 · N = 520", "2022 · REPLICATION", "2024 · 33 STUDIES") and the narration cites it.
  One accent colour per film marks what matters. **Withhold, then name** (call it "the result" until the reveal).
  Every non-final scene ends on an open loop; the last one closes the big loop and stamps it shut with a flat kicker.
  Narration for a clinical read runs ~2.4 words/s; budget under, never over ("the edit can breathe; it can't
  compress"). **Voice calibration sentence:** pick the most case-file line of the script and render it 3-5 ways,
  changing one dial at a time, before voicing the whole film. Our narrator stays warm (owner's pick), but the
  calibration habit applies to Parler descriptions. Real events: verified facts only, no lingering on victims.
- **Commercial pipeline (locks).** *If something keeps breaking between shots, stop describing it better inside
  every shot; give it its own lock.* For animators: anything that must hold across scenes (the desk position, the
  phone's facing, the Student's colours, the pin's corner) is a named rule in ANIMATOR-BRIEF, not repeated prose.
  **Lighting as named states** tagged per scene (our chapter looks), switching ON the word, not after it.
  **Edit acceleration:** cut-ins get faster toward the climax while the subject stays slow, with the two or three
  beats that must breathe named as exceptions (here: the held silence before "nothing"). **Start every segment on
  the action**; delete run-ups rather than shortening them. **Complexity budget:** once a scene reads clean, stop;
  revert rather than fixing forward. Judge each render on 3-4 named checks, never "looks nice".
- **Paper animation (5 lanes + transitions).** Paper reads as paper through grain, cast shadows, imperfect edges,
  PLANAR motion and stepped 12 fps timing; smooth easing kills it (our `K.onTwos` + `K.paper`). Paper's superpower
  is the **material as the transition**: page turn, layer peel, torn reveal, cut-through push into an opening,
  foreground wipe past a big paper element. Use one where the film changes setting; hard cuts inside a setting.
- **Paper-cut motion (assembly grammar).** Build back-to-front (backdrop from above/sides → ground from below → set
  pieces → crowd row by row → props → hero LAST, part by part, base-up), each piece with its hard shadow; one
  cause→effect action beat after assembly with a payoff of tiny scattered paper flecks; paper-only foley.
  Its bundled style reference shows a real footballer and real logos: not used.
- **Claymation (start/end frame transitions).** A **shared anchor object** sits at the same place and scale in
  the last frame of scene A and the first of scene B, and ONE physical action carries one into the other; anything
  that leaves must be removed by that action. A **carrier element** can travel the whole film (here: the phone).
- **Talking object (three-layer rule).** Every beat moves on at least two of three layers: camera, character,
  environment reacting. **The visual is the proof of the line**: with the sound off, the viewer still follows.
- **Skeleton ads (escalating spine).** One recurring character, a curiosity-gap question, rungs that escalate
  (Day 1 → Day 30 → Day 365; 1 → 5 → 25), one line = one beat = one rung. Good shape for Shorts and for myth
  escalation scenes (our sc07 retelling chain is exactly this ladder).
- **Song-style ad:** a music-video ad format; not used on this channel (no lip-sync, narrator-led).

## 18. Lessons from five repos (claude-youtube, Hypit, MoneyPrinterTurbo, yt-dlp, youtube-transcript-api)
Read the code and docs; nothing from them runs in our pipeline except the two PyPI tools named below.
- **claude-youtube (AgriciDaniel, MIT): packaging and retention rules.**
  - **Hook:** the first 5 s is now an extension of the thumbnail (home-feed autoplay), so it must answer the
    thumbnail's visual question at once. A value promise lands by 15 s. Never open on the channel.
  - **Open loops ("suspension bridge"):** these give the largest completion gain, so plant one early and pay it off
    late (our bookmark pin).
  - **Interrupts:** at least every 30 s in long-form, and every 2–3 s in Shorts.
  - **Dual CTA:** only ~16% of viewers reach the last 10%, so add an embedded visual CTA after the first payoff
    (~1 min) as well as the end card. Visual + verbal beats verbal-only.
  - **Thumbnail:** ≤3 words; one focal point; 30–40% empty space; strong emotion on any face. Never repeat the title's
    words on the thumbnail: the thumbnail is the emotion, the title the keyword + promise.
  - **Title:** keyword + hook inside the first 40–50 chars (mobile cut). Under 50 chars is safest.
  - **Description:** keyword in the first 25 words; 0:00 chapters (≥3, ≥10 s each); 3 hashtags; ends with subscribe +
    the comment question. Ship a manual SRT (better indexed than auto-captions).
  - **Shorts:** 15–30 s, hook in 1–3 s, a change every 3 s, a loopable ending, title 4–6 words.
  - **Synthetic voices:** the guide cites a big retention drop for AI narration. That is why we tuned Parler with
    earshot and why every word is animated; keep the delivery human-paced.
- **Hypit (Apache-2.0 with conditions; ideas only): anchor edits to WORDS, not seconds.** Every reveal, cut and caption
  change points at a spoken word, so a re-voice never breaks the edit. We have this as `K.word` + `film/words.js` and
  `make_words.py`. Its caption family keeps a whole readable phrase on screen while the CURRENT word changes colour:
  → `scripts/karaoke_ass.py` + `assemble.py --sub-karaoke` (cream → gold as each word is said). Review with
  frame grids as well as single frames, so handoffs and motion are judged, not just poses.
- **MoneyPrinterTurbo (MIT): stock-clip + TTS short generator.** Mostly paid-model plumbing; not our look. One piece
  taken: the **caption spring** (each line pops in at 86 % → 104 % → 100 % over 0.22 s), done as ASS transforms
  in `karaoke_ass.py`.
- **yt-dlp / youtube-transcript-api:** the right tools for the scout's transcript step, now installed in the studio
  venv. From this cloud machine YouTube blocks both ("sign in to confirm you're not a bot" / IpBlocked). The fix is
  the owner's own exported cookies file (`yt-dlp --cookies`), never pasted into chat, or the owner uploading the
  audio/transcript. Without it the scout falls back to uploaded files or the episode's own show notes.

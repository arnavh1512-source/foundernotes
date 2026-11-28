# Learnings from owner-supplied reference videos

Observations from reference videos the owner asked the studio to study. They describe what those videos do. They do not prove what causes views, and they do not override the viewer-first rule, the fact lock or the channel rules. Use them as candidates to test in a pilot.

Add a dated section for each new study. Record how the video was examined and what was not checked.

## 2026-11-11: two psychology explainers (stick-figure style)

**Studied:** "Psychology of Seduction" (15:23) and "Psychology of Discipline" (14:44), both apparently from one channel. The owner reports at least 3 million views each; the studio did not verify that. A third file would not decode and was not studied.

**Method:** Whisper transcript of each full video, ffmpeg scene-cut detection (threshold 0.25), contact sheets of the first minute of each and one mid-section, Earshot audio measurement of the first 62 seconds. Nobody at the studio listened to the audio.

### Measurements

| | Seduction | Discipline | Our first pilot (62 s) |
| --- | --- | --- | --- |
| Words | about 2,790 | about 2,770 | 198 |
| Pace (words/min) | 181 | 188 | 204 |
| Shots | 255 | 253 | 16, plus 8 punch-ins |
| Median shot length | 3.1 s | 2.9 s | about 3.9 s |
| Pictures in first 60 s | 18 | 17 | 16 |
| Studies cited by year | 7 | 5 | 2 |
| "you/your" per 100 words | 3.8 | 4.9 | not measured |
| First study named at | 0:55 | 1:13 | 0:09 |
| Loudness (LUFS) | -15.3 | -15.1 | -14.1 |
| Loudness range (LU) | 4.2 | 3.8 | 2.6 |
| Voice brightness | 1,290 Hz | 1,235 Hz | 877 Hz |
| "Air" band | -24.8 dB | -25.5 dB | -34.6 dB |

### What the references do

1. **Open on the viewer's private moment.** The first 55 to 75 seconds describe the viewer's own experience in second person (the alarm and the cold floor; being approved of and still not chosen). The first study comes after that.
2. **Remove blame.** Both tell the viewer the problem is not their character ("You were never broken. You were trained"). This reframe is what the share prompt at the end is built on.
3. **Carry one sharp distinction through every chapter.** Approved-of versus wanted. Forcing yourself versus barely needing to.
4. **Tell research as short stories.** Named researchers, a year, what they did, what happened, and at least one "the half of this study that gets left out".
5. **Show people in situations.** Almost every picture is a character acting out a moment. Diagrams are rare. On-screen words are rare and large (two or three words).
6. **Change the picture about every 3 seconds.** Ten or eleven shots per video run longer than 8 seconds.
7. **Keep one simple, warm look.** Expressive stick figures in painted rooms and landscapes, muted colours. Character designs vary between shots.
8. **End with three numbered actions, a call-back to the opening image, one specific comment question and a "send this to the friend who..." prompt.**
9. **Narration is brighter and more dynamic than ours** (see table). Their first minute is mostly voice alone.

### How our first pilot differed

Measured on `choking-under-pressure`, 62 s, QC status WARN.

- It reached the experiment at 9 seconds, after one sentence about the viewer.
- Most shots were diagrams (dial, bars, track, curve). The first render failed the motion gate at 2.4% fast-motion frames; punch-in cuts raised it to 3.55%, just above the 3.5% fail line.
- The narration measured duller and flatter than both references.
- It had no explicit blame-removing line.

### Candidates to test in the next pilot

- Spend 40 to 60 seconds on the viewer's own moment, in second person, before the first study.
- State the blame-removing reframe in plain words, with its evidence.
- Make character scenes the default shot and keep one recurring diagram.
- Aim for a new picture about every 3 seconds.
- Use two or three large on-screen words at key moments in place of many labels.
- Record from a cleaner voice reference, or brighten the narration, and check with `earshot measure` against the figures above.
- End with numbered actions, a call-back, one specific comment question and a share prompt.

### Limits

- Two videos from one channel. This is a description of one channel's approach.
- Visual notes come from sampled frames, not a full viewing.
- The look and characters are theirs. Borrow structure and pacing only; all artwork stays original (see `explanation-first-visual-direction.md`).
- Burned-in subtitles and on-screen citations remain channel rules even though the references use neither.

## 2026-11-27: four owner-supplied clips vs Night 1 Part 2

Files supplied by the owner (`studio-output/_references/clips/`, not committed): ref1 "DISCIPLINE" (2.6 min, dark short film, DayOne-like), ref2 "Psychology of Verbal…" (14.4 min) and ref3 "Psychology of Discipline" (14.7 min, no audio in the file) in a PsychToons/PsychDoodle-like hand-drawn style, ref4 "Trial Chamber" (31 s vertical, no audio, Alan Becker-like action). Measured with ffmpeg scene detection (threshold 0.30) and a frame-difference count at 4 fps, 160x90 px; visuals from sampled contact sheets.

| Clip | Cuts/min | Avg shot | Median moving area | Near-still frame pairs |
|---|---|---|---|---|
| ref1 | 1.9 | 32 s | 2.5% | 4% |
| ref2 | 21.0 | 2.9 s | 0% | 90% |
| ref3 | 15.1 | 4.0 s | 0% | 91% |
| ref4 | 0 (one moving camera) | 31 s | 54% | 0% |
| Night 1 Part 2 | 7.4 | 8.2 s | 1.3% | 10% |

What the frames show:
1. **ref2/ref3: one new drawing per idea, every 3–4 s.** The drawings barely move; the change of picture carries the attention. Each sentence gets its own visual metaphor (tangled yarn for a thought, a FIXABLE/BROKEN signpost, a tiny figure beside a giant bookshelf, a numbered checklist card, a name banner for a cited author, an A report card, a trophy).
2. **Framing varies on purpose:** wide shots with a tiny figure, mid shots, big head close-ups with the brain shown, object-only inserts (a sheet of paper, a pencil erasing words).
3. **Backgrounds are simple flat colour bands that change every shot**, not one detailed room reused. Faces are minimal and readable.
4. **Very little on-screen text:** one or two big words at the top (TRANSLATION, VERBAL INTELLIGENCE, a number). No visible burned captions in the sampled frames.
5. **ref1** builds a story arc with a day counter (DAY 1 … DAY 340), the inner critic drawn as a red shadow figure, a mirror as a recurring image, sparse lowercase red text for the critic's voice, and a closing title card. Long takes work because each frame is a staged moment with mood lighting.
6. **ref4** is one continuous camera move down a tall level with the whole frame active: action, particles, enemies. The lesson for our Shorts is to fill the vertical frame with motion.

Night 1 Part 2 by contrast: the same wide study shot recurs often, characters are small in frame, and abstract ideas mostly appear as gears and labelled blocks beside a standing figure.

Candidates to test on Night 2 (pilot first; not proof of what drives views):
- Aim for 15–20 shot changes a minute: one new picture per sentence or idea, average shot 3–4 s.
- Give each idea its own visual metaphor drawn for it, instead of reusing the room.
- Mix wide / mid / close-up / object-insert framings, and cut back to the room only for dialogue.
- For abstract beats, swap the detailed room for flat colour-band backgrounds that change per shot.
- Keep on-screen words to one or two big words per idea. Captions stay (channel rule).
- Give recurring images a story job (a day counter, an inner critic figure, a mirror) where the topic suits it.
- Shorts: action or camera movement across the whole vertical frame.

Limits: four clips from at most three channels; ref3 and ref4 files have no audio, so sound was not compared for them. Visual notes come from sampled frames, not full viewings. The rea-video breakdowns were still running at the time of writing. Borrow structure and pacing only; all artwork stays original.

## 2026-11-27: owner-supplied vertical clip, "inside a bump on the head" (pixel-art cross-section)

File: `studio-output/reference-ig-01/ref.mp4` (720x1280, 30 fps, 26.1 s, -14.1 LUFS, LRA 5 LU). Studied from frame sheets at
1 s and 0.25 s, full-size crops of the labels, scene-cut detection and per-second audio bands. Not a full watched viewing; speech
could not be checked (no transcription installed), so whether it has narration is unknown.

Structure (timestamps from the file):
- **0–2.0 s, the result first:** an object hits a head in profile; impact rings; the bump swells under a fast-forward timer
  (1 MIN, 6 MIN, 13 MIN); framing brackets lock onto the bump; a push-in carries the camera into it.
- **2.0–2.6 s, inside:** the push-in becomes a skin cross-section with the swelling already there. The only hard cut (2.57 s).
- **2.6–4 s, rewind and replay:** a rewind icon, then **SLOW** play: the impact again, seen inside (the object presses the layers
  against the bone). Labels: SKIN, SKULL, VESSELS TEAR.
- **4–21 s, one fixed set, time does the cutting:** a fast-forward counter ticks steadily (4 MIN, 11 MIN, 23 MIN, DAY 1 … DAY 14).
  Each new label is one actor and its job: PLATELETS …, FIBRIN / LOCKS THE CLOT, HEMATOMA / ABOVE THE SKULL, MACROPHAGE / EATS RED
  CELLS, LYMPH VESSEL / DRAINS FLUID, REPAIRED. The camera pushes in on the actor (the macrophage, day 1) and pulls back for the
  result. The pooled blood changes colour over the days (red, dark, olive), so the colour itself shows time passing.
- **21–26 s, back out:** a burst of speed lines, a pull back to the head in profile, now flat, then a scanline wipe. The last frame
  matches the opening framing, so it loops.

What makes it work:
1. **Payoff, then explanation:** it shows what you can see (a bump) before what you can't (the inside), so the question asks itself.
2. **A playback interface as the storyteller:** rewind / slow / fast-forward icons and a ticking clock tell the viewer where they
   are in time without a word. One set holds for 17 s and still moves forward, because time is the thing being cut.
3. **Labels in two parts:** white noun + yellow verb, at most 4 words, typed on letter by letter, with a leader line drawn to the
   actor. Each label is the next step of the story, not a glossary.
4. **The camera has a job:** push in to meet a new actor, pull back to show the effect.
5. **Vertical composition:** the clock and empty space at the top, the action in the middle band, the static bone layer at the
   bottom (where captions and UI sit).
6. **Sound:** heavy low-frequency hits on the impacts (0 s, 3 s: 84% of the energy below 150 Hz) and steady mid-range sound
   throughout. Per our phone rule, those hits would carry little on a phone speaker unless they have content above 150 Hz.

Candidates to test (pilot first; not proof of what drives views; borrow structure only, all artwork original):
- Think! Shorts: open on the visible result, rewind, replay slowly from inside, then fast-forward through the stages with a clock.
- A playback UI (rewind / slow / fast-forward + counter) as a recurring device in place of narration-heavy time jumps.
- Labels as white noun + yellow verb, typed on, at most 4 words, one per step.
- Half Landing: the rewind-and-slow-replay of the gag's cause (e.g. replay the thump that knocked the spoon), and the clock for
  time-skip episodes.
- One fixed set where time moves forward, instead of many cuts.

## 2026-11-28: two more owner-supplied clips (directing promo; stick-fight scene)

Full notes and measurements: `.claude/skills/entertainment-studio/references/animation-craft-playbook.md`.
- reference-ig-02 (39 s): the five directing moves (light, camera, the breath, on twos, the hit), a 0/5 progress row with
  the last item withheld, narration that stops for the payoff, music changing section on the hit. All five are now options
  in `entertainment-studio/engine/overlay.js` and the stick scenes.
- reference-ig-03 (76 s): frame-by-frame stick fight with almost no holds (~1% still over two frames), smears on fast moves,
  persistent bodies and debris, long panning takes and colour grades for special moments.
Limits: frames and measurements only; no transcription; inferences from rea-video are unconfirmed.

## 2026-11-28: owner-supplied clip reference-ig-04 ("funny bone"), same creator as reference-ig-01

Same 26.1 s, same beat grammar as the bump explainer with a new subject: a repeatable series template. New details: the
invisible shown on the surface first (a glowing zigzag nerve up the arm, fingers splay), floating motes in every frame,
a story-telling room, a target ring and brackets on the impact point. Measured with ref_motion.py: local motion 6.2%,
1.8% repeated frames; camera rolls at 2.5 s (in), 13.6 s and 21.3 s (out). Full notes: entertainment-studio playbook.
Candidates for Think! Shorts: a fixed series template; show the mechanism on the surface before going inside.

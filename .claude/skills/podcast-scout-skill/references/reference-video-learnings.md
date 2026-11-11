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

---
name: think-stick-engine
description: The Think! channel's production stick-animation engine (canvas + measured timings), built and owner-reviewed on Night 1 Part 2. Faces with expressions and voice-driven mouths, gestures timed to stressed words, character-led action beats instead of zoom pulses, CC0 music and sound effects, a motion-score estimator, and the full narrator + ElevenLabs build. Use for every new Think! long video and Short.
---

# Think! stick engine

The engine every Think! video is built with since Night 1 Part 2 (2026-11). It replaces the one-off `film/` folders copied between episodes. The owner reviewed each piece below; the reasons are in the "Owner rules" section, so don't undo them.

## Start an episode

```bash
bash .claude/skills/think-stick-engine/new_episode.sh <slug>
```

This creates `studio-output/<slug>/full/` with `film/` (engine, fonts, Think! logo) and the build tools, and downloads the CC0 music (checksummed; the mp3s are not in git).

Then, in `studio-output/<slug>/full/`:
1. `narration/script.json` (owner narrator, Voicebox) and `dialogue/script.json` (character lines, ElevenLabs via `podcast-scout-skill/scripts/elevenlabs_narrate.py`). Record both; ASR-check both.
2. `order.json`: the playback order of segment ids. If you split narrator segments into character lines (see `example/split.py`), also write `groups.json` (scene id → line ids) and `scene_order.json` (scene ids).
3. Scenes and `film/shots.js` (`window.SHOTS2=[{seg,a,b,n,args?,sfx}]`). `scenes.js`–`scenes5.js` are the library: reuse helpers (`fig`, `K`, `walk`, `block`, `S.duo`, `S.keys`, vignettes) and add new scenes in a new file loaded from `stick.html`.
4. `example/exprmap.py`: copy it, then map each character line to a speaker expression and a listener reaction (writes `film/expr.js`). `film/env.js` (mouth movement) is written by the snippet in "Faces" below.
5. `bash build.sh` (detached: `setsid nohup bash build.sh > build.log 2>&1 &`). After picture-only changes, `bash rerender.sh`.

Rendering a 14-minute video takes about 75 minutes on 6 chunks. Worker restarts kill attached jobs, so always launch detached.

## Owner rules (do not regress)

- **Characters speak their own lines** (2026-11-21). The narrator only tells the story. No "the philosopher says…" reported speech.
- **No zoom pulsing** (2026-11-22). Long explanations are carried by character action and new mini-scenes (`S.duo` study staging, `S.keys` keyword actions, vignettes), not by cutting between zoom levels of the same picture.
- **Varied, natural gestures** (2026-11-22). Gestures start on stressed words (`tools/emph.py` finds them in the real voice), hold, then relax to rest. No looping, no constant shaking. Listeners stay mostly still. Scenes opt in with `fig(...,{talk:1})`; prop-holding poses keep their hands.
- **Faces** (2026-11-23): `engine/faces.js`. There are ten expressions (neutral, happy, angry, shouting, shocked, smug, sad, thinking, worried, calm). The philosopher's mouth is drawn dark (`#2a1f3d`) so it shows on his beard. Expressions come from `window.LEXPR` per line, or from `SCENE_EXPR` in `stick.html` for narrator moments.
- **CC0 audio only** (2026-11-23): music `assets/music` (fetched), effects `assets/sfx` (in git). Credits are in `assets/CREDITS.md`, and the description credits them as a courtesy. Check the licence on the source page before adding anything new.
- Picture and voice must line up. After any timing change, check frames against captions (one per scene) before rendering.

## Faces: mouth movement data

After `mix/timings.json` exists, write `film/env.js` (per-frame mouth opening from the voice) with the snippet used on Night 1 Part 2: compute the 30 fps mean-absolute envelope of `mix/narration.wav`, normalise it per character line (85th percentile), and quantise it to digits 0–9 in `window.ENV`. See `example/` and the episode notes.

## Motion score before rendering

`qc_video.py` fails a video below 3.5% fast-motion frames. Estimate it in about 5 minutes instead of a 75-minute render:

```bash
bash tools/estall.sh /abs/path/to/film/stick.html
```

The estimator was calibrated on Night 1 Part 2: it predicted 2.83% where the real check measured 2.76%. Stick limbs alone barely register. What lifts the score is new pictures, big objects moving fast (blocks flying in, a car), a background change with meaning (seasons, spotlight, the study's warm wall) and impact jolts. Gestures don't. Never meet the score with zoom pulsing.

## Sound

`engine/sfx.py` reads the cues in `shots.js` (`thunk`, `whoosh`, `pop`, `ding`, `ting`) and rotates through the CC0 variants so repeats don't sound identical. `tools/music_cc0.py` builds the bed from `music.json` (`[[file,start,end],...]`) or, by default, piano, then contemplation, then lo-fi in thirds, with 3-second crossfades.

## Files

- `engine/`: `stick.html` (renderer, gestures, faces hookup), `scenes*.js` (library and Night 1 scenes), `faces.js`, `sfx.py`, `facetest.html` (expression sheet).
- `tools/`: `build.sh`, `rerender.sh`, `turns.py`, `emph.py`, `music_cc0.py`, `est.mjs` / `estall.sh` (motion estimate), `grab.mjs` (frame grabs).
- `example/`: Night 1 Part 2 `split.py` (narrator → character lines), `beats.py` (long shots → action beats), `exprmap.py`, and its `shots.js`.
- `tests/test_engine.py`: sound-effect bank and stressed-beat detection.

Everything in CLAUDE.md still applies: viewer-first gate, 60–90 s pilot, fact lock, owner narrator, burned captions, qc_video, the delivery package and claude-youtube.

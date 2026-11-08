# Founder Notes: YouTube explainer studio for Claude Code

Skills and subagents that turn a podcast episode (or a plain topic) into a researched, fact-checked,
animated educational video for **[Founder Notes](https://www.youtube.com/@FounderNotesin)**. Each video
comes with a male narrator, burned-in karaoke captions, an original score and a ready-to-upload package.
Nothing is ever uploaded automatically: the channel owner reviews and uploads every video.

## Channel rules (enforced by the skills; see `CLAUDE.md` and `channel-profile.md`)

| Rule | How it is enforced |
|---|---|
| Male narrator, human explainer delivery | Parler-TTS described male voice + earshot-tuned studio chain; Kokoro `am_michael` and Piper `en_US-ryan-high` as fallbacks; `narrate.py` refuses non-male voices |
| Never credit or name the source podcast, host or guest | Scriptwriter and packager rules; reality checker blocks it |
| Subtitles burned into every video | `assemble.py` burns captions by default; karaoke mode lights each word as it is spoken |
| Backgrounds rotate; a new cast every video | `K.backdrop` presets (no two adjacent scenes alike); `assets/ink-gold-kit/CAST.md` |
| Every video ends on the Founder Notes end card | `K.endCard`: logo, subscribe click, and the question "What topic should we ... next?", plus a closing CTA line |
| Facts locked before voicing | Reality checker fact lock (`FACTS.md`); every on-screen number must match it |
| No real people drawn, no brand logos, no voice cloning | Animator brief + `lint_scenes.py` |

## What's inside

| Path | What it is |
|---|---|
| `.claude/skills/podcast-scout-skill/` | Main skill. **Scout:** research → scored ideas → briefs. **Studio:** script → fact lock → storyboard → narration → scenes → score → edit → QC → upload package |
| `.claude/skills/podcast-scout-skill/assets/ink-gold-kit/` | The SVG scene kit: character rig (`K.Hunter`), backdrops, acting (`K.act` hit-stops, `K.keys` poses), chapter tracker, bookmark pin, torn-paper assembly (`K.paper`), self-drawing annotations (`K.trace`, `K.dashPath`), word-timed punch-ins (`K.punch`, `K.word`), end card |
| `.claude/skills/animation-styles/` | 17 looks drawn in code (flat vector, comic, chalkboard, glow sketch, pixel art, risograph, ink-in-water, one-line graph, Renaissance codex, ASCII terminal and more), with a render bridge |
| `.claude/skills/collage-director/` | Paper-collage motion graphics on MuAPI (needs credit; male voice allowlist, no cloning) |
| `.claude/skills/motion/` | Time-driven HTML → MP4 renderer (Chromium + ffmpeg), with optional sub-frame motion blur (`--blur N`) |
| `.claude/skills/design-me/` | Design/motion router |
| `.claude/agents/studio-*.md` | 8-role crew: researcher, scriptwriter, visual director, animator, sound engineer, editor, packager, reality checker. All run with `model: sonnet`, `effort: medium` |
| `.claude/skills/podcast-scout-skill/references/craft-library.md` | Everything learned from the repos, packs and tutorials the owner shared (§12–§18), rewritten as working rules |

## Quick start

```bash
bash .claude/skills/podcast-scout-skill/scripts/setup_studio.sh   # voices (Parler, Kokoro, Piper), ffmpeg/node checks
```

`channel-profile.md` already holds the Founder Notes settings. Then, in Claude Code:

> /podcast-scout-skill Use this podcast: &lt;URL, audio file or transcript&gt;. Find five well-supported video ideas, then make the best one end to end.

YouTube blocks transcript downloads from cloud machines. Upload the audio or transcript instead, or
use a cookies file exported from your own browser (`yt-dlp --cookies`). Never paste cookies into chat.

## How a video is made

1. **Scout:** read the episode, list its claims, check each against primary sources, and score topics.
2. **Script and fact lock:** the reality checker passes every line against `FACTS.md` before any voice is recorded.
3. **Narration:** `narrate.py` with Parler. Every take is transcribed back (`--asr`) and any take that dropped words is redone (`--retake`).
4. **Word map:** `make_words.py` writes the time of every spoken word. Scenes, punch-ins, sound effects and captions all land on words, not on hard-coded seconds, so a re-voice never breaks the edit.
5. **Scenes:** four animators build them in parallel from `STORYBOARD.md`, `LOOKS.md` and `ANIMATOR-BRIEF.md`, with fixed rules that hold across scenes (desk, pin, chapter looks, case-file stamps). Each scene is checked from stills and `lint_scenes.py`.
6. **Score:** an original score from real instrument samples, plus foley timed to the words.
7. **Edit:** `assemble.py` mixes the music ducked under the voice to −14 LUFS and burns in karaoke captions that spring in line by line.
8. **QC and package:** `qc_video.py`, the reality checker's final pass, thumbnail, titles, a description with sources and chapters, a pinned comment, and a Shorts plan, checked with `package_lint.py`.

## Studio scripts (`.claude/skills/podcast-scout-skill/scripts/`)

| Script | Does |
|---|---|
| `narrate.py` (+ `parler_worker.py`) | Script JSON → male narration, `timings.json`, SRT/VTT captions. Parler reads in short chunks of 14 words or fewer with natural breaths. `--asr --retake N` re-voices only the takes that dropped words |
| `karaoke_ass.py` | SRT + word times → ASS captions where each word turns gold as it is spoken, and each line springs in |
| `assemble.py` | Scene clips + narration + ducked music + captions → 1080p30 H.264/AAC master at −14 LUFS (`--sub-karaoke` for karaoke captions) |
| `qc_video.py` | Spec, loudness, black opening, freezes, dead air, sync, caption rules, contact sheet |
| `lint_scenes.py` | Pre-render checks on scene files (render contract, caption zone, sources on screen) |
| `package_lint.py` | Title, thumbnail text, description, chapters and tags rules before upload |
| `fetch_sfx.py` | Openly licensed sound effects from Openverse |
| `gen_media.py` | Images/clips through MuAPI (refuses placeholder output when the balance is 0) |
| `validate_report.py`, `obscura-research.mjs` | Scout report arithmetic + provenance checks; research reader |

Tests: `cd .claude/skills/podcast-scout-skill && python3 -m unittest discover -s tests && node --test scripts/obscura-research.test.mjs`

## Engineering checks and repair status

The studio is undergoing a coordinated engineering hardening pass on the
`audit/consolidated-pipeline-hardening` branch. **A green GitHub Actions run is not
proof that a complete video can be produced or that the studio is production-ready.**

### Local validation

From the repository root, run:

```bash
python3 -m compileall -q .claude/skills tests
python3 -m unittest discover -s tests -p "test_qc_video.py" -v
cd .claude/skills/podcast-scout-skill
python3 -m unittest discover -s tests -v
node --test scripts/obscura-research.test.mjs
```

The GitHub workflow `.github/workflows/python-qc.yml` currently checks Python
syntax, QC behavioral tests, and real FFmpeg decoding samples. The additional
studio and Node tests above are **manual checks**, not yet CI guarantees.

### Hardening changes on the repair branch

- Broader Python syntax checking exposed and corrected an invalid shell
  heredoc wrapper committed inside `lint_scenes.py`.
- `gen_media.py` now downloads into a temporary file, checks common media
  signatures, caps download size, and avoids modifying batch specifications.
  Signature checks are not equivalent to full image/video decoding.
- `assemble.py` validates key render parameters and media inputs before
  launching expensive FFmpeg processing.
- Earlier QC fail-closed and regression-test improvements remain in place.

### Before publishing

Verify a complete video run with representative narration, scenes, captions,
and music. Inspect the rendered master, audio sync, contact sheet, QC report,
asset provenance, and upload package manually. Do not merge repair work solely
because syntax checks pass.

## Credits and licences

Ideas and code adapted from open projects are listed in `.claude/skills/podcast-scout-skill/NOTICE.md`
and `references/production-stack.md`. Where a project had no licence, or a restrictive one, only its
ideas are used, rewritten in our own code. Sources include agency-agents, anidoodle, manim_skill,
Parler-TTS, earshot, lemo-opuscar, Openverse, vox (collage-director), pixelfx, Hypit,
MoneyPrinterTurbo, claude-youtube, yt-dlp and youtube-transcript-api.

Work in progress lives in `studio-output/<slug>/`, which is gitignored.

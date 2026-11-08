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

### Research tool: Agent-Reach replaces Obscura as the preferred adapter

[Agent-Reach](https://github.com/Panniantong/Agent-Reach) is now the **preferred optional research-channel integration** for supported web pages, social platforms and transcripts, replacing Obscura in the research workflow guidance. It is a multi-platform CLI, **not an animation engine** and not a direct API-compatible replacement for the old browser helper. Only use channels that have been installed, configured and authorized; otherwise fall back to host-native research tools. The old Obscura script and its tests remain available as **legacy code**, not the default workflow, until a verified migration removes them. See [Agent-Reach research integration](.claude/skills/podcast-scout-skill/references/agent-reach.md). No Agent-Reach install or end-to-end integration is claimed yet.

## FounderNotes 2.0 — creative production rebuild

**Direction:** The existing animation presets are no longer the target creative standard. The next system will prioritize purposeful, engaging motion, narrative clarity, voice-to-visual synchronization, and measurable improvement after each video. This is a **planned rebuild**, not a claim that the new engine is already implemented.

The full specification is in [FounderNotes 2.0: Motion Direction and Continuous Improvement](docs/FOUNDERNOTES_2_MOTION_SYSTEM.md).

### Five animation sources under evaluation

| Reference | Techniques to study and benchmark |
|---|---|
| [Bang Motion](https://github.com/bangtutorial/bang-motion) | Continuous visual worlds, camera choreography, persistent subjects, motion design briefs and deterministic previews |
| [Vox Director](https://github.com/Alisa0808/vox-director) | Narrative beat maps, visual style bake-offs, editorial collage keyframes, layered animation and sound |
| [Huashu Art Motion](https://github.com/alchaincyf/huashu-art-motion) | Art-specific animation grammars, parametric explainer scenes, timing grids and motion quality checks |
| [Claude Drawing Skill](https://github.com/cloveric/claude-drawing-skill) | Code-drawn illustration, reproducible compositions, staged draw-on animation and visual revision |
| [Code Animation Prompts](https://github.com/XiaoyeCodes/code-animation-prompts) | Searchable animation-style references, sample implementations and time-addressable browser rendering |

**Source status:** Repository documentation and published examples have been reviewed at a high level. Exhaustive code-level analysis, license-by-asset review, and comparative rendered benchmarks are still pending. Do not copy upstream assets or code without checking applicable licenses.

### Intended production workflow

1. Research and lock factual claims.
2. Generate narration using the proven Voicebox route where available, with pronunciation, transcription and timing checks.
3. Build a word-aligned narrative beat map; assign each shot a purpose, subject, camera movement, motion grammar and sound cue.
4. Present three different visual treatments of a representative beat for approval before full production.
5. Render deterministic scenes using the most suitable approved techniques, not a random mixture of presets.
6. Check decoded frames, transitions, missing/blank footage, audio gaps, clipping, synchronization and caption timing.
7. Have a separate **Sonnet / medium-effort** critic review the rendered video for repetition, visual coherence, clarity and pacing.
8. Record timecoded mistakes, root causes, corrections and regression tests so the next production can reuse verified lessons.

**Quality philosophy:** A technically valid video can still be boring. Motion must communicate; more movement is not automatically better. Audience views and retention can inform improvement when available, but they do not independently prove animation quality.

### Animation library: 17 existing styles + 5 external skill collections

The studio includes **17 documented animation techniques** under [`.claude/skills/animation-styles/`](.claude/skills/animation-styles/). All 17 style-reference documents have been reviewed as part of the FounderNotes 2.0 instruction audit:

| Family | Techniques |
|---|---|
| 2D illustration and editorial | Pixel Art, Chalkboard, Glow Sketch, Comic Art, Flat Vector, Dan Koe-inspired, Risograph Cutout, Renaissance Codex |
| 3D and physical worlds | PS2 Retro 3D, CGI Motion, Lego-inspired, ZackD-inspired |
| Experimental and transformation | One-Line Graph, One-Ball Showreel, ASCII Terminal, Pixel Dither, Ink in Water |

The [17-style audit report](docs/ANIMATION_STYLES_AUDIT.md) documents the distinctive mechanism, potential failure modes and appropriate storytelling uses of each style. The [animation skill instructions](.claude/skills/animation-styles/SKILL.md) now describe all 17 and prioritize narrative continuity over arbitrary style rotation.

**Verified so far:** all 17 Markdown style references reviewed; creative direction and continuity rules updated. **Not yet verified:** rendered samples for every style, full shared renderer and player inspection, comparative visual benchmarks, audio-to-action alignment, and complete integration tests. These must be completed before claiming the redesigned animation system is production-ready.


### Five additional animation skill collections

These **five external repositories are additional animation sources alongside the 17 built-in styles**, giving the studio **22 tracked style/skill sources in total**. They are **not merely five individual visual styles**: each contains multiple techniques, examples, workflows or style references. Their techniques should be selectively mastered, tested and integrated, not treated as automatically installed or production-ready.

| Added source | Animation capabilities to integrate |
|---|---|
| [Bang Motion](https://github.com/bangtutorial/bang-motion) | Continuous action, kinetic typography, camera-led explainer motion, persistent subjects and designed transitions |
| [Vox Director](https://github.com/Alisa0808/vox-director) | Editorial paper collage, layered cutouts, keyframe-driven motion, beat planning and visual style comparisons |
| [Huashu Art Motion](https://github.com/alchaincyf/huashu-art-motion) | Art-inspired animation, motion grammars, transformation sequences, parametric scenes and motion analysis |
| [Claude Drawing Skill](https://github.com/cloveric/claude-drawing-skill) | Procedural illustration, ink and paint treatments, staged drawing, reproducible visuals and iterative critique |
| [Code Animation Prompts](https://github.com/XiaoyeCodes/code-animation-prompts) | Broad animation-style reference library, code-rendered effects, deterministic timelines and searchable examples |

**Integration target:** one creative director should be able to choose from the 17 existing styles and relevant techniques from all five external sources according to the story, while maintaining a coherent visual world and sound design. First inspect licenses and dependencies, benchmark real rendered clips, then promote proven implementations into the pipeline. Listing a repository here does **not** mean its code has been installed or fully integrated.

### First acceptance milestone

Create a **30–60-second narrated pilot** with at least three different narrative functions. Compare it side by side with an existing FounderNotes sample, review it visually and aurally, measure production failures, and only then promote successful techniques into the default pipeline.

The new creative system is not production-ready until that pilot and the required integration checks pass.

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

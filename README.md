# FounderNotes

**An AI-assisted production studio for research-driven YouTube explainers.**

FounderNotes is the Claude Code workspace behind [Founder Notes](https://www.youtube.com/@FounderNotesin). It takes a topic, podcast, transcript, or reference material through research, editorial development, narration, scene production, sound, quality review, and YouTube packaging.

**One goal:** tell an accurate, engaging story with purposeful visuals—not a collection of disconnected effects.

[![Python QC Checks](https://github.com/arnavh1512-source/foundernotes/actions/workflows/python-qc.yml/badge.svg)](https://github.com/arnavh1512-source/foundernotes/actions/workflows/python-qc.yml)

> **Project maturity:** The repository has executable production tools, Claude Code skills and agents, and automated tests. A full episode produced and approved end-to-end has **not yet been verified**. External rendering engines, Voicebox and Agent-Reach require separate installation and live testing.

## Quick start

### 1. Open the repository

**Requirements:** Claude Code, Python 3, Node.js, FFmpeg/ffprobe, and a working shell. A suitable browser/runtime is needed for scene rendering. Some voice and rendering engines have additional dependencies. On Windows, use a compatible Bash environment such as WSL for the provided shell scripts.

```bash
git clone https://github.com/arnavh1512-source/foundernotes.git
cd foundernotes

# Inspect available tools without installing packages:
bash .claude/skills/podcast-scout-skill/scripts/setup_studio.sh --check

# Open Claude Code from the project root:
claude
```

The setup script's diagnostic mode is read-only. To install its supported local Python voice dependencies and models, **review the script first** and run it without `--check`. Some optional packages are large. Voicebox and other third-party engines still require their own setup; the script does not automatically make every backend available.

### 2. Give Claude Code a production brief

Claude Code reads the root [`CLAUDE.md`](CLAUDE.md). The primary entry point is [`podcast-scout-skill`](.claude/skills/podcast-scout-skill/SKILL.md), which you can invoke as `/podcast-scout-skill` when the skill is recognized by your Claude Code installation.

For a first run, paste this prompt:

```text
Read CLAUDE.md, channel-profile.md and
.claude/skills/podcast-scout-skill/SKILL.md.
You are operating the FounderNotes YouTube production studio.

Topic or source: [PUT YOUR TOPIC OR LINK HERE]
Mode: 45–60-second pilot

Follow the studio's stage gates and use the studio-* agents where available.
Attempt Agent-Reach first for public research; use authorized native tools
when its documented fallback applies. Log sources and fact-check claims.
Write an original script and use Humanizer for a natural spoken-English pass;
verify the revised script against the evidence before recording.
Use the established male Voicebox narrator. Add distinct original synthetic
male/female character voices only when dialogue serves the story.
Produce a coherent storyboard, source/rights manifest, narration-timed
scenes, captions and a mixed MP4. Run real technical and creative QC.
Record actual lessons and skill evaluations. Prepare the upload package.

Before installing extra tools, spending money, or using accounts, ask.
Do not publish, invent citations, fabricate tests, or call a prompt a render.
Show me the resulting files, remaining blockers, and what you verified.
```

**Recommended sequence:** finish and review a **30–60-second pilot** before commissioning the channel's **8+ minute** full-length format. You can also ask for **research only**, **script and storyboard**, **a dialogue scene**, **QC on an existing video**, or **YouTube packaging** without running the whole pipeline.

## How the studio works

| Stage | Responsibility | Main artifact |
| --- | --- | --- |
| **Research** | Establish an angle, retrieve primary sources, identify uncertainties | Source ledger and verified claims |
| **Script** | Explain the idea clearly; use Humanizer, then verify the edited facts | Original script with claim mapping |
| **Direction** | Design scene actions, continuity, camera decisions and timing | Storyboard and shot plan |
| **Voices & sound** | Generate approved narration or character dialogue; time and mix audio | WAV master, `timings.json`, SRT/VTT and sound cues |
| **Scene production** | Render meaningful motion using an available, suitable engine | Scene clips, assets and preview frames |
| **Editing** | Assemble synchronized video, sound and subtitles | MP4 master |
| **Independent review** | Inspect claims, continuity, audio, frames, rights and technical QC | QC report and corrective actions |
| **Publishing preparation** | Draft accurate titles, thumbnail concepts, chapters and description | Upload-ready package (**manual publishing**) |

The [eight core studio agents](.claude/agents/) handle these responsibilities under one production coordinator. The [model-routing policy](.claude/skills/podcast-scout-skill/references/model-routing.md) assigns **Opus** to judgment-heavy work, **Sonnet** to well-scoped production and **Haiku** to two optional read-only helper roles. The precise Claude model/version must be checked on your host; no unsupported model is required. Agent definitions are **workflow instructions**, not evidence that a production was run. The [production plan](.claude/skills/podcast-scout-skill/assets/production-plan.md) describes expected handoffs and output folders under `studio-output/<slug>/`.

## Key capabilities

**Research and editorial quality.** [Agent-Reach](.claude/skills/podcast-scout-skill/references/agent-reach.md) is the default *first attempt* for public web search, page reading, YouTube search and subtitles. When unavailable, Claude can use an authorized native research fallback. [Humanizer](.claude/skills/humanizer/SKILL.md) is included locally for script and packaging polish; it must preserve factual meaning, numbers, citations and qualifications. The [marketing-growth skill](.claude/skills/marketing-growth/SKILL.md) provides focused references for topics, honest packaging, distribution and analytics. The [i-have-adhd skill](.claude/skills/i-have-adhd/SKILL.md) is an **opt-in** formatting aid, never an assumed user characteristic.

**Voicebox casting.** The principal voice is the authorized, consistent male **Founder Notes Narrator**. An episode can also use distinct **male and female synthetic character voices**, selected per scripted segment for interviews, dramatized interactions or storytelling. Character profiles must exist and be approved in a **local Voicebox** installation. The system produces a sequential master with speaker-aware timings and captions; **simultaneous overlapping dialogue and automatic lip sync are not implemented**. See the [casting guide](.claude/skills/podcast-scout-skill/references/voice-casting.md) and [example cast](.claude/skills/podcast-scout-skill/assets/voice-cast.example.json).

**Visual production.** The original [animation-styles skill](.claude/skills/animation-styles/SKILL.md) now searches **592 indexed style, prompt, drawing and art-motion entries** across FounderNotes and upstream libraries, while the studio keeps its 17 native reference styles. See the [library and renderer guide](.claude/skills/animation-styles/references/community-animation-integration.md). A catalog entry is *not* an installed engine or proven render. The optional [Lemo adapter](.claude/skills/podcast-scout-skill/scripts/lemo_backend.py) routes local frame/video exports to a separately installed Lemo-Opuscar; [Raea](.claude/skills/raea-renderer/SKILL.md) remains a separate optional canary GPU renderer with license restrictions. [Anatomy](.claude/skills/anatomy-figures/SKILL.md) adds a separately installed **MIT-licensed isometric mechanism-figure workflow**: original SVG/WebGL cutaways and a [local PNG preview bridge](.claude/skills/podcast-scout-skill/scripts/anatomy_backend.py). It is not a video exporter; time-stepped motion still uses the studio renderer. Renderers are selected by story value, actual availability, cost and rights, not sheer style count.

### Animation library at a glance

The **original** `.claude/skills/animation-styles/SKILL.md` is the single entry point for these source-aware choices, not a second competing skill.

| Source | Indexed choices | What they provide |
| --- | ---: | --- |
| FounderNotes native styles | **17** | Built-in HTML visual techniques |
| [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) | **66** | Code-built film styles; optional local rendering adapter |
| [Code Animation Prompts](https://github.com/XiaoyeCodes/code-animation-prompts) | **341** | Metadata references; original mixed-source prompts and stills are not copied |
| [Anidoodle](https://github.com/alexgreensh/anidoodle) | **32** | Hand-drawn animation styles requiring its separate engine |
| [Huashu Art Motion](https://github.com/alchaincyf/huashu-art-motion) | **53** | Art-motion recipes, including 17 research-only cards |
| [Claude Drawing Skill](https://github.com/cloveric/claude-drawing-skill) | **83** | Procedural **still illustration** styles for later animation |
| **Total catalog entries** | **592** | Searchable creative references, not 592 render engines |

Nine more upstream sources are present in the [source registry](.claude/skills/animation-styles/references/community-animation-sources.json): Bang Motion, Vox Director, ClaudeAnimationBase, LunaAI Motion Skill, LottieFiles Motion Design, HandDraw, Manim, JavaScript Animation Skills, and Anatomy. Their skills and dependency-specific capabilities are selected from upstream as needed; no unsupported individual style counts are claimed.

**Run the selector locally:**

```bash
python3 .claude/skills/animation-styles/scripts/animation_library.py --sources
python3 .claude/skills/animation-styles/scripts/animation_library.py --search "investigation timeline"
python3 .claude/skills/animation-styles/scripts/animation_library.py --search "watercolor"
python3 .claude/skills/animation-styles/scripts/animation_library.py --show lemo-opuscar:visual-investigation
```

See the [integration and licensing guide](.claude/skills/animation-styles/references/community-animation-integration.md) for the Lemo frame/MP4 commands, rights limits, prerequisites, native fallbacks and QC. Anatomy's provider entry does not increase the 592 style count; its browser preview and real scene adaptation are still untested. The index and offline CI checks do not prove all 592 entries render successfully; no external engines or paid services are installed automatically.

**Learning and quality control.** The studio records verified defects, successful recipes and skill-specific reviews in [`.claude/memory/`](.claude/memory/). A skill is not considered evaluated merely because it appears in the repository. Technical tools include scene linting, video/audio QC, a creative-plan validator, skill-evaluation gates and lesson recording. Evidence from rendered output and human listening is required.

## Useful commands

Run these from the repository root after ensuring Python and any required dependencies are available.

```bash
# Check the configured public research gateway:
python3 .claude/skills/podcast-scout-skill/scripts/research_gateway.py status

# Search the original animation-styles library (592 index entries):
python3 .claude/skills/animation-styles/scripts/animation_library.py --sources
python3 .claude/skills/animation-styles/scripts/animation_library.py --search "documentary"

# Inspect the available creative routes and evaluation history:
python3 .claude/skills/podcast-scout-skill/scripts/creative_router.py --list
python3 .claude/skills/podcast-scout-skill/scripts/evaluate_skills.py status

# Check whether the optional GPU renderer is installed:
python3 .claude/skills/podcast-scout-skill/scripts/raea_backend.py status

# Run the repository's focused studio regression tests:
python3 -m unittest discover -s .claude/skills/podcast-scout-skill/tests -p 'test_voice_cast.py' -v
```

To use the optional character cast, first copy the [sample JSON](.claude/skills/podcast-scout-skill/assets/voice-cast.example.json) into an episode's `narration/script.json`. With Voicebox running locally, use [`provision_voicebox_cast.py`](.claude/skills/podcast-scout-skill/scripts/provision_voicebox_cast.py) for a **read-only preview** of missing profiles; adding `--create` explicitly authorizes creation of the selected approved synthetic profiles. See the casting guide for the exact workflow.

## Project map

| Path | What to read it for |
| --- | --- |
| [`CLAUDE.md`](CLAUDE.md) | Claude Code's standing project instructions |
| [`channel-profile.md`](channel-profile.md) | Audience, tone, voice identity and editorial constraints |
| [`.claude/skills/podcast-scout-skill/`](.claude/skills/podcast-scout-skill/) | Main end-to-end workflow, scripts, assets and references |
| [`.claude/agents/`](.claude/agents/) | The eight specialist roles |
| [`agency-production-system.md`](.claude/skills/podcast-scout-skill/references/agency-production-system.md) | Stage gates, handoffs and approval requirements |
| [`voice-casting.md`](.claude/skills/podcast-scout-skill/references/voice-casting.md) | Voice profiles, dialogue format and local setup |
| [`animation-styles/SKILL.md`](.claude/skills/animation-styles/SKILL.md) | Original animation skill with 592-entry catalog |
| [`community-animation-integration.md`](.claude/skills/animation-styles/references/community-animation-integration.md) | Upstream libraries, Lemo renderer bridge and source-rights gates |
| [`.claude/memory/`](.claude/memory/) | Verified lessons, production history and evaluations |
| [`docs/`](docs/) | Extended architecture and engineering reports |
| [`NOTICE.md`](.claude/skills/podcast-scout-skill/NOTICE.md) | Third-party references, license limitations and attribution |

## Production standards and readiness

- **Truth first:** Verify important facts against identifiable sources. Clearly label hypothetical or reconstructed scenes; do not invent quotes or evidence.
- **Consistent storytelling:** Keep characters, dialogue voices and visual worlds recognizable. Measure scene timing from the actual narration WAV rather than an estimated word count.
- **Rights and approval:** Respect source, audio, asset and engine licenses. No unapproved voice imitation, paid-generation calls, account connections or automatic publishing.
- **Real QC:** Review rendered frames, complete audio, captions, synchronization and output reports. Record deficiencies and rerun failed checks.
- **Honest status:** CI runs regression tests and a synthetic FFmpeg production smoke test. It does **not** prove that a local Voicebox cast, live Agent-Reach retrieval, optional Raea GPU engine, Anatomy figure preview or a complete real-world episode has been validated.

**Next milestone:** a reviewed 30–60-second pilot with real research, natural narration, coherent action, edited sound, accurate captions and evidence-backed QC. Only then scale up to an 8+ minute production.

---

FounderNotes is an independent creator project. External projects have their own terms and prerequisites; see the [third-party notices](.claude/skills/podcast-scout-skill/NOTICE.md).

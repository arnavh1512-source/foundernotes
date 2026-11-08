# FounderNotes

**An AI-assisted YouTube production studio for research-driven explainers.**

FounderNotes is the production system behind [Founder Notes](https://www.youtube.com/@FounderNotesin). Give it a topic, podcast, transcript, or source material; the studio helps turn that input into an original, evidence-led video, from research and scriptwriting through narration, scene production, review, and YouTube packaging.

**The goal is a compelling story that happens to use motion—not a slideshow of effects.**

> **Development status:** This repository contains real production scripts, Claude Code skills, specialist agent definitions, templates, and evaluation tools. The expanded production workflow is still being integrated and **has not been verified end to end on a completed pilot**. Referenced external tools are not automatically installed.

## What the studio does

| Production stage | Output |
| --- | --- |
| **Discover & research** | Topic opportunities, source notes, evidence and fact checks |
| **Write & direct** | Original script, visual treatment, timecoded storyboard and scene plan |
| **Narrate** | Consistent male voiceover, captions and measured narration timing |
| **Produce & edit** | Rendered scenes, sound effects, music, subtitles and MP4 master |
| **Review & improve** | Technical checks, independent creative critique, recorded defects and lessons |
| **Prepare for YouTube** | Thumbnail guidance, titles, description, chapters and upload checklist |

The eight specialist roles—researcher, scriptwriter, visual director, animator, sound engineer, editor, reality checker and packager—are defined in [`.claude/agents/`](.claude/agents/). The coordinator is responsible for handoffs, evidence, and approval gates. **Publishing is always manual.**

## Getting started with Claude Code

### 1. Open the project

Clone the repository, then open the project root in Claude Code. The current development work is on `audit/consolidated-pipeline-hardening`; `main` may not include these changes.

```bash
git clone https://github.com/arnavh1512-source/foundernotes.git
cd foundernotes
git switch audit/consolidated-pipeline-hardening
```

Before installing dependencies, check the available tools:

```bash
bash .claude/skills/podcast-scout-skill/scripts/setup_studio.sh --check
```

When you want to prepare the local voice and production dependencies, review the setup script and run:

```bash
bash .claude/skills/podcast-scout-skill/scripts/setup_studio.sh
```

The setup script uses a Python virtual environment and may download packages and voice models. Rendering also requires Node.js, a compatible Chromium environment, FFmpeg and the chosen scene engine; optional engines have separate prerequisites. **On Windows, use an appropriate Bash environment, such as WSL, for these shell scripts.**

### 2. Tell Claude what to do

Claude Code should load [`CLAUDE.md`](CLAUDE.md) from the repository root. The main workflow is [`podcast-scout-skill`](.claude/skills/podcast-scout-skill/SKILL.md). Start with:

```text
/podcast-scout-skill
```

You can also give Claude Code this complete project brief:

```text
You are working inside the FounderNotes repository.

Read CLAUDE.md, channel-profile.md, and
.claude/skills/podcast-scout-skill/SKILL.md first.
Read the studio crew and agency-production-system references before delegating.

Treat this repository as an end-to-end YouTube explainer studio,
not a collection of unrelated animation presets.

For my topic or source:
1. Find the strongest factual angle, with a source/evidence ledger.
2. Write an original script and obtain a fact-lock review.
3. Produce a clear treatment, storyboard, and narrator-aligned shot plan.
4. Use the established male channel narrator; confirm real audio timing.
5. Choose only story-appropriate, available and legally usable tools.
6. Build a short pilot and inspect rendered frames and the audible mix.
7. Correct concrete defects, then produce the full video if approved.
8. Run the technical checks and independent quality review.
9. Record verified lessons and skill evaluations.
10. Prepare the YouTube package; do not upload or publish.

Use the studio-* subagents where available (Sonnet, medium effort).
Verify the actual model/version at runtime; do not assume an alias
guarantees Sonnet 5.5. Ask before paid generation or installing extras.
Never invent citations, rendered outputs, test results or approvals.
Report what is complete, what failed and what remains.
```

### 3. Choose the production mode

| Goal | Ask Claude to do |
| --- | --- |
| **Research only** | Evaluate a topic or supplied transcript and return evidence-backed video ideas. |
| **Pre-production** | Take an approved idea through script, fact lock, narration and storyboard. |
| **Pilot** | Produce a **30–60-second** narrated sample with scene, sound and frame checks. **Recommended first run.** |
| **Full episode** | Once the pilot works, produce the channel's long-form video and upload package. The configured long-form minimum is **8 minutes**. |
| **Audit / repair** | Review existing scripts, scene clips or a finished MP4; provide timestamped defects, repair them and rerun checks. |

The [production-plan template](.claude/skills/podcast-scout-skill/assets/production-plan.md) describes the intended handoffs and file layout under `studio-output/<slug>/` (ignored by Git).

## Non-negotiable channel rules

- **Narration:** Use the channel's consistent **male narrator**, preferring the configured Voicebox profile when available. Do not clone another person's voice without rights and explicit authorization. Lock scene timing to measured audio, not guessed duration.
- **Evidence:** Verify factual claims and record sources. Present reconstructions or illustrative scenes accurately; do not manufacture documentary evidence.
- **Direction:** Maintain continuity of subjects, worlds and actions. The story decides which technique to use; visual novelty alone is not a reason to switch.
- **Sound and accessibility:** Include appropriate music/SFX, narration intelligibility and burned-in subtitles; inspect the actual audio and video, not just metadata.
- **Rights and spending:** Check commercial licenses and media attribution. Use paid generators or authenticated services only with approval.
- **Quality:** Run technical validation and an independent creative review before calling the video ready.
- **Owner control:** No automatic YouTube publishing.

Channel-specific requirements live in [`channel-profile.md`](channel-profile.md). If a reference technique conflicts with those requirements, the channel and production contracts take priority.

## How FounderNotes is organized

| Location | Purpose |
| --- | --- |
| [`CLAUDE.md`](CLAUDE.md) | Standing instructions for Claude Code |
| [`channel-profile.md`](channel-profile.md) | Audience, narration, format and editorial policy |
| [`.claude/skills/podcast-scout-skill/`](.claude/skills/podcast-scout-skill/) | Main research-to-video skill, scripts and production references |
| [`.claude/agents/`](.claude/agents/) | Eight specialist production roles |
| [`.claude/skills/motion/`](.claude/skills/motion/) | Time-driven scene rendering utilities |
| [`.claude/skills/animation-styles/`](.claude/skills/animation-styles/) | Native visual-technique reference library |
| [`.claude/skills/collage-director/`](.claude/skills/collage-director/) | Optional editorial collage workflow |
| [`.claude/memory/`](.claude/memory/) | Recorded lessons, production history and skill reviews |
| [`docs/`](docs/) | Detailed design and audit documents |
| [`tests/`](tests/) | Repository-level QC regression tests |

### Production tools

Useful scripts live under [`.claude/skills/podcast-scout-skill/scripts/`](.claude/skills/podcast-scout-skill/scripts/): `narrate.py` for narration/timings, `assemble.py` for the master, `lint_scenes.py` and `qc_video.py` for checks, `package_lint.py` for YouTube metadata, `creative_router.py` for proposed scene formats, `evaluate_skills.py` for skill reviews and `record_lesson.py` for verified learning.

For example, these commands **inspect or test** the project; they do not generate a complete video by themselves:

```bash
python3 .claude/skills/podcast-scout-skill/scripts/creative_router.py --list
python3 .claude/skills/podcast-scout-skill/scripts/evaluate_skills.py status
python3 -m unittest discover -s .claude/skills/podcast-scout-skill/tests -v
python3 -m unittest discover -s tests -v
```

For engine-specific render commands, consult the selected engine's instructions first. Do not assume all optional tools are installed.

## Continuous quality and improvement

The studio is designed to **evaluate every skill it uses**, not only animation. It records reviews by video, including clarity, continuity, motion, audio, reliability and rights; a tool that has never been tested must remain **unassessed**, not silently pass. Lessons are saved in `.claude/memory/` and should be read before subsequent productions.

The production gate includes actual render inspection, audio listening, technical QC, source/rights verification and owner sign-off. A validated JSON plan or passing metadata test is **not proof of a finished video**.

Read [the production system](.claude/skills/podcast-scout-skill/references/agency-production-system.md), [the skill router and dependencies](.claude/skills/podcast-scout-skill/references/production-stack.md), [sound production standards](.claude/skills/podcast-scout-skill/references/sound-design-and-listening.md) and [the FounderNotes 2.0 motion specification](docs/FOUNDERNOTES_2_MOTION_SYSTEM.md) for the deeper contracts. Detailed technique inventories—including the existing styles, external projects and user-supplied creative formats—are intentionally kept **in those references**, rather than repeated throughout this README.

### Recent engineering hardening

Scene preflight now validates storyboard time columns, scene manifests and rendered clip durations (`lint_scenes.py --require-clips`). Skill approval now checks for nonempty sample media and a genuine PASS JSON QC report (`evaluate_skills.py`). Openverse sound retrieval filters commercial-use licenses, validates HTTPS sources and file signatures, and bounds downloads. The GitHub workflow runs regression suites and a synthetic FFmpeg assembly/QC test. **These checks improve reliability but do not replace listening to and reviewing a real finished episode.**

## Readiness and limitations

**Implemented or present in the repository:** Claude Code role/skill definitions, narration and editing scripts, motion utilities, QC code, planning templates, a creative-format router, evaluation/lesson recorders and regression tests.

**Still requires real-world verification:** installing compatible dependencies, rendering a coherent pilot, checking the configured male voice, testing complete audio/visual synchronization, exercising the full multi-agent workflow, confirming specific Claude model versions, and resolving any remaining licensing/production issues.

The next meaningful milestone is a **complete, reviewed 30–60-second pilot**, followed by the first full-length Founder Notes episode.

---

*FounderNotes is an independent creator-production project. Third-party tools and references retain their own licenses; see [`NOTICE.md`](.claude/skills/podcast-scout-skill/NOTICE.md).*

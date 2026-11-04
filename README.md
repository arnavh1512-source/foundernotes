# hunting-titles — YouTube explainer studio for Claude Code

Skills and subagents that turn podcasts (or a topic) into researched, **male-narrated**, animated
educational YouTube videos.

| Path | What it is |
|---|---|
| `.claude/skills/podcast-scout-skill/` | Main skill. Scout (research → scored ideas → briefs) + Studio (script → fact lock → storyboard → male narration → scenes → edit → QA → upload package) |
| `.claude/skills/motion/` | Default scene engine: time-driven HTML → MP4 via Chromium + ffmpeg |
| `.claude/skills/design-me/` | Design/motion router (now routes YouTube explainers to podcast-scout-skill) |
| `.claude/agents/studio-*.md` | 8-role crew (researcher, scriptwriter, visual director, animator, sound engineer, editor, packager, reality checker) — all `model: sonnet`, `effort: medium` |
| `CLAUDE.md` | Session defaults: male voice, Sonnet/medium subagents, output folder |

## Quick start

```bash
bash .claude/skills/podcast-scout-skill/scripts/setup_studio.sh      # Kokoro + Piper male voices, checks ffmpeg/node
cp .claude/skills/podcast-scout-skill/assets/channel-profile.md channel-profile.md   # then edit
```

Then in Claude Code:

> /podcast-scout-skill Use this podcast: <URL or transcript>. Find five well-supported video ideas, then make brief 01 end to end.

## Studio scripts (`.claude/skills/podcast-scout-skill/scripts/`)

| Script | Does |
|---|---|
| `narrate.py` | Script JSON/text → male narration (Kokoro `am_michael` default; Piper, Edge, voicebox, own recordings), `timings.json`, SRT/VTT captions. Refuses non-male voices unless explicitly allowed |
| `assemble.py` | Scene clips + narration + ducked music + captions → 1080p30 H.264/AAC master at −14 LUFS |
| `qc_video.py` | Spec, loudness, black opening, freezes > 2.5 s, dead air, sync, caption rules, contact sheet |
| `package_lint.py` | Title / thumbnail text / description / chapters / tags rules before upload |
| `validate_report.py`, `obscura-research.mjs` | Scout report arithmetic + provenance checks; Obscura research reader |

Tests: `cd .claude/skills/podcast-scout-skill && python3 -m unittest discover -s tests && node --test scripts/obscura-research.test.mjs`

## Integrated projects

Animation engines and helpers are installed separately and routed per scene — see
`references/production-stack.md` and `NOTICE.md`: agency-agents, anidoodle, huashu-art-motion,
claude-drawing-skill, ClaudeAnimationBase, LunaAI motion-skill (paid, opt-in), LottieFiles
motion-design, HandDraw-Skill, manim_skill, javascript-animation-skills, stickman-video-director,
youtube-agent-skill, OpenMontage (AGPL, ideas only), voicebox, Obscura.

Nothing is ever uploaded; the channel owner reviews and uploads.

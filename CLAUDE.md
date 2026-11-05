# hunting-titles — YouTube video studio

This repo holds the skills and subagents used to research and produce animated educational
YouTube videos.

## Standing defaults for every session
- **Narration is always a male voice.** Default Kokoro blend `am_fenrir+am_puck` (speed 0.84) with the human-explainer performance layer (varied pace, pitch, level and pauses per sentence) via
  `.claude/skills/podcast-scout-skill/scripts/narrate.py`; fallback Piper `en_US-ryan-high`.
  Use a non-male voice only if the channel owner asks for it in their own words.
- **Subagents run on Sonnet at medium effort.** The crew in `.claude/agents/studio-*.md` sets
  `model: sonnet` and `effort: medium`; pass `model: "sonnet"`, `effort: "medium"` on any ad-hoc
  Agent call too.
- Main skill: `/podcast-scout-skill` (research → briefs → script → male narration → scenes →
  edit → QA → upload package). Companion skills: `/motion` (default HTML scene engine), `/collage-director` (paper-collage motion graphics on MuAPI) and
  `/design-me` (design/motion router).
- **Subtitles burned into every video** (assemble.py default). **Backgrounds rotate** and **every video gets a new cast** (CAST.md; no two adjacent scenes alike; kit in `.claude/skills/podcast-scout-skill/assets/ink-gold-kit`). Never credit or name source podcasts (see channel-profile.md).
- Work goes in `studio-output/<slug>/` (gitignored). Never upload or publish; the owner uploads.
- Channel settings live in `channel-profile.md` at the repo root (template in
  `.claude/skills/podcast-scout-skill/assets/channel-profile.md`).
- Setup per machine/session: `bash .claude/skills/podcast-scout-skill/scripts/setup_studio.sh`.

# hunting-titles — YouTube video studio

This repo holds the skills and subagents used to research and produce animated educational
YouTube videos.

## Standing defaults for every session
- **Narration is always a male voice, and always the SAME voice.** Default **Parler-TTS** with the owner-approved
  channel narrator (voice "C": calm, warm, low-pitched teacher; description `PARLER_DESC` in narrate.py) locked to
  `.claude/skills/podcast-scout-skill/assets/voice/founder-notes-narrator.wav`: every sentence is generated 3 ways,
  the take closest to that voice wins, and its pitch is settled to it, so the voice never switches mid-video. Then
  the earshot-tuned **studio chain**, via `.claude/skills/podcast-scout-skill/scripts/narrate.py`; fallbacks Kokoro
  `am_michael` + studio chain, then Piper `en_US-ryan-high`. Never replace the narrator file unless the owner asks.
  Use a non-male voice only if the channel owner asks for it in their own words.
- **Subagents run on Sonnet at medium effort.** The crew in `.claude/agents/studio-*.md` sets
  `model: sonnet` and `effort: medium`; pass `model: "sonnet"`, `effort: "medium"` on any ad-hoc
  Agent call too.
- Main skill: `/podcast-scout-skill` (research → briefs → script → male narration → scenes →
  edit → QA → upload package). Companion skills: `/motion` (default HTML scene engine), `/collage-director` (paper-collage motion graphics on MuAPI), `/animation-styles` (10 named looks drawn in code) and
  `/design-me` (design/motion router).
- **Subtitles burned into every video** (assemble.py default). **Backgrounds rotate** and **every video gets a new cast** (CAST.md; no two adjacent scenes alike; kit in `.claude/skills/podcast-scout-skill/assets/ink-gold-kit`). Never credit or name source podcasts. **Every video ends with the Founder Notes end card** (logo, subscribe, "What topic should we cover next?" comment question; `K.endCard`) and a closing CTA line (see channel-profile.md).
- Work goes in `studio-output/<slug>/` (gitignored). Never upload or publish; the owner uploads.
- Channel settings live in `channel-profile.md` at the repo root (template in
  `.claude/skills/podcast-scout-skill/assets/channel-profile.md`).
- Setup per machine/session: `bash .claude/skills/podcast-scout-skill/scripts/setup_studio.sh`.

# hunting-titles — YouTube video studio

This repo holds the skills and subagents used to research and produce animated educational
YouTube videos.

## Standing defaults for every session
- **Narration is always a male voice, and always the SAME voice: the Founder Notes narrator on voicebox.**
  Engine: **voicebox** (Chatterbox) with the profile "Founder Notes Narrator", cloned from the SYNTHETIC reference
  `.claude/skills/podcast-scout-skill/assets/voice/founder-notes-narrator-ref.wav` (owner-approved 2026-11-06; not a
  real person). Scripts use `"voice": {"engine": "voicebox", "name": "founder-notes", "chain": "studio"}`; narrate.py
  creates the profile on a new machine. Start the server first: `bash .claude/skills/podcast-scout-skill/scripts/voicebox_server.sh`.
  Each segment is generated in one pass (no voice switching); `--asr --retake 2` re-voices dropped words with a new seed.
  Fallbacks: Parler locked to `assets/voice/founder-notes-narrator.wav`, then Kokoro `am_michael`. Never replace the
  narrator unless the owner asks.
  Use a non-male voice only if the channel owner asks for it in their own words.
- **Subagents run on Sonnet at medium effort.** The crew in `.claude/agents/studio-*.md` sets
  `model: sonnet` and `effort: medium`; pass `model: "sonnet"`, `effort: "medium"` on any ad-hoc
  Agent call too.
- Main skill: `/podcast-scout-skill` (research → briefs → script → male narration → scenes →
  edit → QA → upload package). Companion skills: `/motion` (default HTML scene engine), `/collage-director` (paper-collage motion graphics on MuAPI), `/animation-styles` (10 named looks drawn in code) and
  `/design-me` (design/motion router).
- **Every long-form video runs at least 5:00** (owner rule, 2026-11-06). Plan ~880+ spoken words at the narrator's ~168 wpm (voice speed 0.94); reach it with researched, fact-locked beats, never padding or slowed filler.
- **Subtitles burned into every video** (assemble.py default). **Backgrounds rotate** and **every video gets a new cast** (CAST.md; no two adjacent scenes alike; kit in `.claude/skills/podcast-scout-skill/assets/ink-gold-kit`). Never credit or name source podcasts. **Every video ends with the Founder Notes end card** (logo, subscribe, "What topic should we cover next?" comment question; `K.endCard`) and a closing CTA line (see channel-profile.md).
- Work goes in `studio-output/<slug>/` (gitignored). Never upload or publish; the owner uploads.
- Channel settings live in `channel-profile.md` at the repo root (template in
  `.claude/skills/podcast-scout-skill/assets/channel-profile.md`).
- Setup per machine/session: `bash .claude/skills/podcast-scout-skill/scripts/setup_studio.sh`.

# ElevenLabs character dialogue — optional cloud adapter

The owner explicitly selected ElevenLabs for Youth/Philosopher dialogue. This
opt-in adapter does not replace the standing channel narrator, clone voices,
change providers automatically, publish, or assume an approved performance.

Install optional dependencies from the repository root:

```sh
python -m pip install -r requirements.txt
```

Set ELEVENLABS_API_KEY in environment secrets or private .env.local. The SDK
client reads the environment; dotenv loads the project .env.local without
printing it. Never commit keys. For SOCKS-proxied environments also install
`httpx[socks]`. An environment variable overrides a value in the local file.

Copy `assets/elevenlabs-philosopher.example.json` into studio-output/. The two
preset voice IDs were confirmed through the authenticated premade-voice catalog:
Liam for Youth and George for Philosopher. These are audition choices, not an
owner-approved performance. Availability and use rights depend on the account.
The model is explicit, with eleven_v4 the documented default; no automatic
model, voice, local-TTS or provider fallback occurs.

```sh
# No key needed, no API request and no output audio:
python .claude/skills/podcast-scout-skill/scripts/elevenlabs_narrate.py studio-output/philosopher/narration/script.json --out studio-output/philosopher/narration

# Explicit metered synthesis; use only with owner approval:
python .claude/skills/podcast-scout-skill/scripts/elevenlabs_narrate.py studio-output/philosopher/narration/script.json --out studio-output/philosopher/narration --model eleven_v4 --generate
```

The SDK requests PCM 24 kHz, wraps it in checked mono 16-bit WAVs, and invokes the
existing files narration engine for a measured 48 kHz master, captions and timing.
Speaker/scene metadata is preserved by ID with voice_source=elevenlabs. Cached
takes bind text/voice/model/output format and audio hash. --force explicitly
requests new takes. No recording or key is added to the repository.

The resulting timings.json feeds the painted-character builder; its picture then
uses studio_loop.py pilot/short-film/full assembly, technical QC and creative
review. Word timings from the native assembler are estimates, not phoneme lip
sync. The silent philosopher visual draft uses provisional shot times and needs
retiming to approved performances before any final export.

Tests use fake SDK PCM and real WAV validation, not synthesized speech. A valid
key or successful catalog lookup does not establish permission to generate.
Authentication, account, plan and provider restrictions must be resolved without
retrying around blocks. A failed request is never reported as generated audio.

# Voiceover: male narrator, voice first

## Policy

- Every video uses a **male narrator** unless the channel owner explicitly asks otherwise in
  their own words. Record the engine and voice in `timings.json` (narrate.py does this).
- One voice per video and, ideally, per channel. Change it only with the owner's approval.
- Synthetic preset voices only, or the owner's own recordings. **Never clone a podcast guest,
  host, celebrity or any real person.** Voice cloning is allowed only from the owner's own voice
  or a sample they hold a licence for.
- YouTube asks creators to disclose realistic altered or synthetic content; the upload checklist
  reminds the owner to decide on the disclosure for AI narration.

## Engines (in order of preference)

| Engine | Male voices | Runs | Notes |
|---|---|---|---|
| **Kokoro 82M** via `kokoro-onnx` | `am_michael` (default), `am_adam`, `am_fenrir`, `am_onyx`, `am_eric`, `am_liam`, `bm_george`, `bm_lewis` (British) | CPU, offline, Apache-2.0 | Best free quality; ~4× real time on 4 CPU cores. Speed 0.86–0.90 gives ~150–160 wpm (am_michael is brisk at 1.0). |
| **Piper** | `en_US-ryan-high` (default), `en_US-joe-medium`, `en_US-john-medium`, `en_GB-alan-medium` | CPU, offline, MIT | Fallback; very fast; slightly more robotic. |
| **Edge TTS** | `en-US-AndrewNeural`, `en-US-GuyNeural`, `en-US-BrianNeural`, `en-US-ChristopherNeural`, `en-GB-RyanNeural` | Network (Microsoft online service, no key) | Unofficial free endpoint; fails behind TLS-intercepting proxies (as in some cloud sandboxes). Local machines only. |
| **voicebox** (local server) | Kokoro presets above; Qwen CustomVoice `Ryan`, `Aiden` (accept delivery `instruct`); Qwen VoiceDesign from a text description of a male narrator | CPU ok for Kokoro; GPU for Qwen 1.7B | Use when you want instruct-controlled delivery. |
| **files** | the owner's own recordings, `<segment-id>.wav` | — | Highest quality if the owner records. |

Paid cloud TTS (ElevenLabs, Google Chirp3-HD `en-US-Chirp3-HD-Orus`, OpenAI `onyx`) is possible
only when the owner provides keys through the host's secret settings and approves the cost. Do
not ask for keys in chat.

## Commands

```bash
bash scripts/setup_studio.sh                     # once per machine/session
. "${STUDIO_VENV:-$HOME/.cache/studio-venv}/bin/activate"
python3 scripts/narrate.py --list-voices
python3 scripts/narrate.py narration/script.json --out narration            # Kokoro am_michael
python3 scripts/narrate.py narration/script.json --out narration --engine piper --voice en_US-ryan-high
VOICEBOX_ENGINE=qwen_custom_voice VOICEBOX_INSTRUCT="Calm, warm, clear educational narrator" \
  python3 scripts/narrate.py narration/script.json --out narration --engine voicebox --voice <PROFILE_ID>
```

voicebox one-time setup (local, no cloning):

```bash
docker compose up -d            # in a voicebox checkout; serves http://127.0.0.1:17493
curl -sX POST localhost:17493/models/download -H 'Content-Type: application/json' -d '{"model_name":"kokoro"}'
curl -sX POST localhost:17493/profiles -H 'Content-Type: application/json' -d '{"name":"Narrator-Michael","language":"en","voice_type":"preset","preset_engine":"kokoro","preset_voice_id":"am_michael","default_engine":"kokoro"}'
# → use the returned "id" as --voice. The API has no auth: keep it on localhost.
```

## Script format for the voice

`narration/script.json` — one segment per storyboard beat, IDs shared with scenes:

```json
{"voice": {"engine": "kokoro", "name": "am_michael", "speed": 0.88},
 "lead": 0.3, "tail": 0.8,
 "segments": [{"id": "s01-hook", "text": "…spoken…", "display": "…caption if different…", "pause_after": 0.5}]}
```

Writing for the ear:
- 8–20 words per sentence; one idea per sentence; put the key word last.
- Numbers as said: "about one in three", "twenty twenty-four", "three point two percent".
- Respell hard names in `text` (e.g. "Kah-neh-man"), keep the correct spelling in `display`.
- `pause_after` 0.3–0.5 s between beats, 0.8–1.2 s before a reveal or after a question you want
  the viewer to try. Never add pauses to stretch audio to fit an animation — fix the animation.
- Target 130–165 wpm measured on speech (`wpm_speech` in timings.json).

## After synthesis

1. Read `timings.json`: total duration, wpm, per-segment spans. These spans *are* the scene durations.
2. Spot-check takes you cannot hear: duration per word (≥0.25 s/word average), no segment
   shorter than expected (dropped words), no clipping (`qc_video.py` loudness).
3. If speech recognition (Whisper/whisper.cpp) is available, transcribe `narration.wav` and diff
   against the script to catch skipped words; otherwise state that the check was not run.
4. Captions come from the same timings; per-word timing inside a segment is an estimate.

# Voiceover: male narrator, voice first

## Policy

- Every video uses a **male narrator** unless the channel owner explicitly asks otherwise in
  their own words. Record the engine and voice in `timings.json` (narrate.py does this).
- One **principal narrator identity** per channel. Additional original synthetic character voices, including male and female voices, are allowed for scripted dialogue and character interactions. Preserve each character's profile consistently.
- Synthetic preset voices only, or the owner's own recordings. **Never clone a podcast guest,
  host, celebrity or any real person.** Voice cloning is allowed only from the owner's own voice
  or a sample they hold a licence for.
- YouTube asks creators to disclose realistic altered or synthetic content; the upload checklist
  reminds the owner to decide on the disclosure for AI narration.

## Founder Notes channel override

For **this channel**, the preferred narrator is the owner-authorized **Voicebox male profile `Founder Notes Narrator`** (alias `founder-notes`, normally selected by the narration script JSON). If the Voicebox server/profile is unavailable, use the approved male Parler reference and only then Kokoro `am_michael`. Do not silently substitute a generic default voice: record the actual engine/profile and flag the fallback for review. The generic Kokoro-first engine table below is historical/portable advice, **not the Founder Notes studio order**. Verify the generated WAV, intelligibility, measured timing and rights before visual production.

## Optional multi-character dialogue (Voicebox)

The principal narrator remains male and unchanged; **character** voices can be male or female and as numerous as a scene demands. The repository now supports per-segment Voicebox casting in `scripts/narrate.py`, with `assets/voice-cast.example.json` as a starting format and `references/voice-casting.md` as the canonical policy. Profiles must be owner-approved, original synthetic voices pre-existing in Voicebox; the optional `scripts/provision_voicebox_cast.py` can register them from approved original synthetic WAV references only on explicit `--create`. Do not equate a named cast profile with generated audio, and do not use `--allow-non-male` to change the main narrator simply because a female character is in dialogue. Keep the entire segment timeline and captions synchronized.

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

## Sounding human: what LISTENING showed (earshot, 2026-11)
Every candidate was rendered on the same passage, loudness-matched, and scored with earshot
(AudioSet "Speech synthesizer" vs "Speech" / "Narration", CLAP match, realness). ASR checked that every word survived.

| change | Speech synthesizer ↓ | Narration ↑ | verdict |
|---|---|---|---|
| am_michael, single take per segment (baseline) | 0.88 | 0.17 | the most human raw voice |
| "expressive" voices (fenrir, puck, liam, blends) | 0.93–0.94 | 0.05–0.06 | read MORE synthetic |
| sentence-by-sentence takes with varied pace | 0.92–0.94 | 0.05–0.10 | worse: breaks the engine's own phrasing |
| + per-sentence pitch shifting (rubberband) | 0.95 | 0.05 | "error buzz / digital glitch"; dropped |
| + breaths in long pauses | 0.61 | 0.21 | no gain over the chain alone; dropped |
| **+ studio chain** (small room, warm mic EQ, gentle compression, pink room tone ≈ −50 dBFS) | **0.33** | **0.30** | **adopted (default)** |
| the whole film narration, before → after | 0.80 → 0.30 | 0.18 → 0.31 | the final mix with music: 0.18 |

The defaults that follow from this:
- Kokoro `am_michael`, speed 0.88, one take per segment.
- `"chain": "studio"` is applied to narration.wav. The length is unchanged, so timings stay valid.
- Use `"chain": "dry"` for a lighter version, or `"none"`.
- The sentence-split performance layer remains as an opt-in (`"perform": "pace"`) but isn't recommended.

What makes it human is the writing, so write for the ear:
- vary sentence length;
- ask real questions;
- give a punchline its own short sentence;
- use "…" for a held beat;
- use commas where a speaker would breathe.

**Always listen before shipping:** `earshot describe`/`match` the narration and the final mix, and compare against the previous film.

## Parler-TTS: the default engine since 2026-11-06 (owner's choice after an A/B listen)
**The voice is a written description, so no one is cloned** (`PARLER_DESC` in narrate.py). It must describe a male
speaker; `narrate.py` refuses anything else.

**Engine checks:**
- Same three lines: pitch movement 8.6 st against 3.8 st for Kokoro, and it was the owner's pick by ear.
- Earshot on Parler's own output: AI-voice score 0.93 raw, 0.59 with `"chain": "studio"`; narration score 0.07 → 0.32. So the chain stays on.

**How generation works:**
- `scripts/parler_worker.py` runs in its own venv (`PARLER_PYTHON`; setup_studio.sh installs it).
- It voices each sentence separately with a fixed seed and adds natural pauses.
- It runs at about 5× real time on CPU, so allow about 30 minutes for a 5-minute film.

**Re-takes:** with `--asr --retake 2`, any segment that loses a negation or two or more words is re-generated on a new
seed. Word-versus-digit mismatches don't count.

**Writing for it:**
- Respell accented and unusual words in `text`, e.g. "résumé" → "resume"; it garbles them.
- Keep the correct spelling in `display`.

Kokoro (`"engine": "kokoro"`) stays the fast fallback.

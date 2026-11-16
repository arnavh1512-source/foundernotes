# VoiceStudio dialogue pilot — opt-in local voice source

**Status:** Integration code and an original pilot script are prepared. The VoiceStudio
backend has **not** been called on the owner's Windows machine, and no audio or
video has been rendered or approved by these changes.

VoiceStudio upstream: https://github.com/debpalash/VoiceStudio (AGPL-3.0).
FounderNotes does not vendor its source; this bridge calls its documented local
HTTP API, POST /generate, and receives a WAV response. Install/launch VoiceStudio
separately and review the licenses of the app, selected model and any references.

This is an **episode-specific exception** for dramatic two-person dialogue.
Do not silently replace the standing Founder Notes channel narrator or modify
the main Voicebox settings in CLAUDE.md.

## Why this route

- VoiceStudio can maintain separate saved profiles for Youth and Philosopher.
- The new voicestudio_narrate.py synthesizes one WAV per dialogue segment using
  VoiceStudio's local POST /generate (form data: text, profile_id, language, seed).
- It runs FounderNotes' existing narrate.py with --engine files to assemble
  narration.wav, captions.srt/.vtt and timings.json, then attaches per-speaker
  and scene metadata to the timings.
- Scene editors should time picture and effects from the **actual generated WAV**
  and recorded timings, never from the approximate shooting-script timestamps.
- The bridge does not clone a voice, create a profile, install models, publish,
  edit the channel, generate visuals, or render an MP4.

## 1. Prepare two original or properly authorized VoiceStudio voices

Open VoiceStudio, create/save distinct local profiles, listen to samples and
approve the voice identities for this episode.

- **Youth:** energetic, questioning, quick but intelligible.
- **Philosopher:** unhurried, warm, low-pressure, with intentional silence.
- Do not mimic a real speaker or use third-party recordings without consent.
- Delivery instructions differ by VoiceStudio engine. Its default engine does
  not support arbitrary emotion labels; use a compatible optional engine only
  if installed and tested. Avoid assuming tags such as [emotion:...] work in
  the basic one-shot /generate route.

With VoiceStudio running on its default local port, list IDs from PowerShell:

~~~powershell
Invoke-RestMethod http://127.0.0.1:3900/profiles | Select-Object name,id
~~~

If the backend uses another local port, use that port consistently. Do not
expose this backend to the public internet or paste a private API key in Git.

## 2. Prepare the original pilot

Use the repository example:

~~~text
.claude/skills/podcast-scout-skill/assets/voicestudio-philosopher-pilot.example.json
~~~

Copy it to a local path under studio-output/, e.g.:

~~~powershell
New-Item -ItemType Directory -Force studio-output/philosopher-pilot/narration
Copy-Item .claude/skills/podcast-scout-skill/assets/voicestudio-philosopher-pilot.example.json studio-output/philosopher-pilot/narration/script.json
notepad studio-output/philosopher-pilot/narration/script.json
~~~

In that local script, replace the two REPLACE_WITH_*_PROFILE_ID fields with IDs
from VoiceStudio. Do not commit private voice samples or credentials.

The pilot, **The Map on the Wall**, is an original story about two different
kinds of maps and an actual obstacle. It does not reuse the published book's
well-water, dark-glasses or characteristic dialogue scenes. Its roughly
60–90-second duration is an *editorial target*, not verified audio timing.

## 3. Generate the dialogue through VoiceStudio

First validate script structure without network access:

~~~powershell
python .claude/skills/podcast-scout-skill/scripts/voicestudio_narrate.py studio-output/philosopher-pilot/narration/script.json --out studio-output/philosopher-pilot/narration --dry-run
~~~

Then run it with VoiceStudio open and its speech model ready:

~~~powershell
python .claude/skills/podcast-scout-skill/scripts/voicestudio_narrate.py studio-output/philosopher-pilot/narration/script.json --out studio-output/philosopher-pilot/narration
~~~

The script outputs:

- voicestudio-raw/s01.wav, s02.wav, ... — the source voice takes
- narration.wav — the assembled 48 kHz mono master
- timings.json — measured start/end, with speaker and scene IDs
- captions.srt and captions.vtt — approximate subtitle timing from FounderNotes
- voicestudio-files-input.json — the sanitized local files-engine script

Rerunning normally reuses cached lines. Use --force if you changed the audio
identity under the **same VoiceStudio profile ID**, selected a different speech
model without changing the script, or need new expressive takes. Listen to every
regenerated line and check that VoiceStudio did not omit or repeat words.

The bridge intentionally accepts loopback HTTP only. It does not connect to
VoiceStudio Cloud or attempt to copy a private browser/session credential.

## 4. Turn the voice test into a visual pilot

**Aspect ratio:** 16:9. **Style:** original hand-painted 2D with restrained
amber, blue-grey and ink textures.

Illustrated storyboard targets, to be retimed from timings.json:

| Beat | Visual direction |
| --- | --- |
| Hook | The Youth unfolds a paper street map and traces a road to a shut gate |
| Study | Philosopher asks who drew the map; calm close-up and kettle ambience |
| Stairs | The map transforms into the real street: a narrow staircase a cart cannot use |
| Gates | Keep one locked gate plainly locked; do not pretend perception removes obstacles |
| Question | Paper map, real town and an alternate pedestrian sketch share the frame |
| Close | Youth folds the old map and starts sketching a new path; quiet hold |

Use one consistent visual world, purposeful cut-ins, expressive hands and
natural pauses. Atmosphere: soft room tone, rain outside, paper scrape, distant
market bell. Never drown dialogue with effects.

**Production gates:** viewer-first brief → evidence and source check → WAV
listening and ASR review → 20–40s visual comparison → complete 60–90s pilot →
human inspection of narration, visuals, captions, sources, licenses, and timing.

The existing FounderNotes channel policy requires **8+ minutes for long-form
publications**, and its normal final-video QC rejects shorter uploads. This
60–90s pilot is not presented as a publication-ready long-form episode. Do not
pad it to 8 minutes merely to pass QC. A 4:05 publicly released short film
would require an explicit project policy change and appropriately scoped QC.

## Known limits and safety

- This bridge has been statically inspected against VoiceStudio's generation.py
  API and FounderNotes' narrate.py files route. **No live synthesis, offline
  integration test, or real final film has been verified.**
- Never publish a near-verbatim adaptation of a copyrighted book simply because
  the book is credited. Request permission for an adaptation, or use this
  original narrative route and independently review creative rights.
- VoiceStudio's AGPL-3.0 terms, separately installed speech model licenses and
  any cloned voice rights need checking before commercial distribution.
- The existing subtitle tool estimates timing within each segment; sync by
  listening, and do not claim word-level lip synchronization.

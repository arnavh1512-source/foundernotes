# Sound direction, effects, music, and perceptual QA

Applies to **every** FounderNotes master. The consistent authorized **male** narrator remains the anchor; all other sounds must support comprehension, not mask speech. This is a procedure, not evidence that these tools are currently installed or that any audio passed QC.

## Tool assignments and provenance

| Tool | Specific job | Boundary |
|---|---|---|
| [earshot](https://github.com/Leonxlnx/earshot) | Listen and describe audio, match/find/rank candidate effects, generate procedural SFX when appropriate, produce timeline/sheet/critique/level measurements | Optional local CLI; audio models can be heavy; do not report a listening pass without running it |
| [Openverse](https://github.com/WordPress/openverse) | Discover recorded sounds and their metadata via Openverse search/API | **Every result has its own license**; filter and store license, original creator, landing page and download source; verify before use |
| [Lemo Opuscar](https://github.com/lemomo-ai/lemo-opuscar) | Procedural foley, score, mixing references, render/mux ideas | Instrument samples can have distinct licensing requirements; check each sample |
| Bundled `fetch_sfx.py` | Fetch and track approved SFX candidates, when available and authorized | Check resulting `sources.json`; no assumption every returned item is CC0 |
| Bundled `assemble.py`, `qc_video.py` | Master with narration, score, effects and captions; run objective checks | A successful command is not proof of strong creative sound design |

## Audio-first editorial workflow

1. **Lock the spoken performance.** Use the channel's approved male Voicebox profile when installed/authorized; otherwise choose an allowed male preset and flag the fallback. Check actual voice identity, legibility, missing words, pauses and measured WAV duration. Store engine, profile/preset, rights basis and actual output metadata.
2. **Create a sound intent map** for each timecoded beat: narrative purpose; exact visual action; sound category; cue anchor (impact or transition), intensity, stereo position, tail and whether silence is preferable. Distinguish deliberate silence from unintended dropouts.
3. **Choose the source:** human/physical recordings through Openverse when authenticity matters; procedural effects through earshot or existing SFX generators for stylized animation; a short music motif when it serves pacing. Never make every moving object beep or whoosh.
4. **Prove provenance:** asset manifest includes title, original creator, source URL, asset URL or local path, license type, attribution text, commercial-use decision, and whether modifications are allowed. No NC assets in a monetized upload. ND sources require special review before edits; prefer CC0, then CC BY with credits.
5. **Match and audition:** compare candidates against the intended action **and the final scene** using earshot if available; render short isolated tests and listen. Score timbre, weight, emotional tone, dynamics, repetition and unwanted frequencies.
6. **Sync by picture:** define the perceptual peak, not just the filename's start. Impact peak at contact, whoosh apex at camera midpoint, release/reverb tail after the motion. Check video timestamps with actual frames; preserve a note when choosing deliberate lead/lag.
7. **Mix around speech:** prioritize voice intelligibility, duck or arrange music under speech, avoid clipping and audible pumping, keep coherent dynamics. Use actual loudness and true-peak measurements. The project's -14 LUFS target is an export guideline, not permission to flatten music or narration.
8. **Review the finished program twice:** once at normal listening volume for storytelling and intelligibility; once using a technical pass for silences, clipping, synchrony, headphone mono compatibility, narration consistency and abrupt cuts. A listener or earshot-backed independent critic logs exact timestamps and proposed repairs.
9. **Record learning:** add the specific audible flaw, root cause, fixed sample and regression condition to the existing lessons ledger. Do not mark a sonic recipe as successful based on numbers alone.

## Required per-video output

`production/sound-map.json` (intent and cue frames), `production/sound-assets.json` (licenses and sources), `production/sound-review.json` (real checks/critic evidence) and the finished mix. These are **target artifacts** until production code implements them; creating this document does not imply they exist.

## Failure and acceptance rules

- Missing recordings, model availability, internet access or tool permissions: log the limitation; use a legitimate alternative; never invent a successful fetch or analysis.
- A static frame or an intended silent pause is not automatically a production error. Investigate context before applying numeric QC thresholds.
- Reject audible clipped speech, wrong narrator, absent or unverified attribution, voice buried in the mix, repeated generic SFX that cheapen the film, unintentional silent/black gaps, and significant unmotivated audio-to-action offsets.
- No private account scraping, copyrighted soundtracks, or third-party voice replication without the necessary rights and permission.

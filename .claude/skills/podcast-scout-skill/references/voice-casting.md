# Voicebox character casting: many voices, one recognizable narrator

The **main voice of Founder Notes remains the established male `Founder Notes Narrator`**. Scene storytelling can additionally use any number of original, approved synthetic Voicebox male or female characters. Examples: a founder/investor conversation, two historical actors in a clearly marked reenactment, an interviewer and guest, an argument between hypothetical perspectives, or one narrator alone. **Do not force a second voice when the script has no dramatic need.**

The integration is implemented in `../scripts/narrate.py` and works with its existing `assemble.py`, `captions.srt` and `timings.json` pipeline: each **sequential** script segment can select a different `speaker`. The result is **one narration.wav** with recorded per-segment speaker/scene/profile metadata. Full **simultaneous overlapping voices, performance-driven facial lip synchronization and voice-design generation from text prompts are not implemented**. Don't claim those work.

## 1. Design a cast (unlimited named speakers)

Copy `../assets/voice-cast.example.json` into your episode's `narration/script.json`. Each character is a **distinct** Voicebox profile:

```json
{
  "voice": {"engine": "voicebox", "name": "founder-notes", "speed": 1.0, "chain": "studio"},
  "cast": {
    "narrator": {
      "profile_name": "Founder Notes Narrator",
      "gender": "male", "synthetic_voice": true, "approved": true
    },
    "host": {
      "profile_name": "FN Character Host M1",
      "gender": "male", "synthetic_voice": true, "approved": true
    },
    "expert": {
      "profile_name": "FN Character Expert F1",
      "gender": "female", "synthetic_voice": true, "approved": true
    }
  },
  "segments": [
    {"id": "s01", "speaker": "narrator", "scene_id": "opening", "text": "Here is the central question."},
    {"id": "s02", "speaker": "host", "scene_id": "interview", "text": "What actually happened?"},
    {"id": "s03", "speaker": "expert", "scene_id": "interview", "text": "Let's look at the original records."}
  ]
}
```

The allowed `speaker` is a cast key, not a free-form prompt. All character voices are explicitly marked as owner-approved synthetic, with `gender` used solely to label the voice requested by the creator. Every character must use a unique Voicebox profile, even when two characters share the same gender. The narrator always uses `Founder Notes Narrator` and cannot be recast through the `cast` option.

For recurring characters, preserve the same `profile_name` between episodes. Store the **identity mapping** in the production memory; do not commit actual private voice recordings or private voicebox credentials to the public repository.

## 2. Create or select synthetic Voicebox profiles

Raea, marketing skills and the video engine do not create voices on their own. **Voicebox supports three ways to configure characters:** reusable built-in TTS presets, voice-design prompts, and synthetic-audio-reference profiles. The local profile setup is optional and **never runs without `--create`**.

**A. Built-in synthetic voices — easiest first pilot**

The sample `../assets/voice-cast.example.json` already specifies four distinct native Voicebox Kokoro presets: two male (`am_adam`, `am_fenrir`) and two female (`af_heart`, `af_bella`). Example character cast entry:

```json
{
  "profile_name": "FN Character Investor F1",
  "gender": "female",
  "voice_type": "preset",
  "preset_engine": "kokoro",
  "preset_voice_id": "af_heart",
  "synthetic_voice": true,
  "approved": true
}
```

This creates a named synthetic preset **without cloning any speaker**. The appropriate voice model must actually be installed in local Voicebox before synthesis. Preset profiles are routed to their native engine, **not** forced through Chatterbox.

**B. Voicebox-designed original voices — when an actor needs distinctive delivery**

For a locally supported Qwen VoiceDesign engine, replace the preset fields with:

```json
{
  "profile_name": "FN Character Original Expert F3",
  "gender": "female",
  "voice_type": "designed",
  "design_prompt": "An original adult female voice, thoughtful, mid-range pitch, warm clear English diction, measured rhythm.",
  "synthetic_voice": true,
  "approved": true
}
```

The design engine `qwen_voice_design` must be present and capable of running on the user's hardware. **A design prompt does not guarantee a unique, expressive or female-sounding outcome**; audition the result and revise/approve it. Do not request imitation of a named real person.

**C. Voicebox cloned-from-synthetic reference — only when an original sample exists**

For a character voice originally generated with properly licensed synthetic tools, the owner can supply a reference WAV and its accurate transcript:

```json
{
  "profile_name": "FN Character Narrator Alternate M3",
  "gender": "male",
  "voice_type": "cloned",
  "reference_wav": "synthetic-references/original-male-character.wav",
  "reference_text": "The exact words spoken in the original synthetic recording.",
  "synthetic_voice": true,
  "approved": true
}
```

Paths are relative to the episode's `script.json`. The provisioner checks a valid nonempty local WAV and a transcript. It cannot independently prove reference provenance; the owner must verify originality and commercial rights.

**Local setup**

```bash
bash .claude/skills/podcast-scout-skill/scripts/voicebox_server.sh

# Preview profiles that exist or need to be created; no writes:
python3 .claude/skills/podcast-scout-skill/scripts/provision_voicebox_cast.py \
  studio-output/pilot/narration/script.json

# Explicit local creation with the user's approved original choices:
python3 .claude/skills/podcast-scout-skill/scripts/provision_voicebox_cast.py \
  studio-output/pilot/narration/script.json --create
```

The provisioner avoids duplicate profile names and checks per-role approval. It does **not** install TTS models, log in, call remote servers, or pre-generate complete voice samples. The permanent `Founder Notes Narrator` is already managed by `narrate.py` from its own authorized synthetic reference, so the cast setup skips it.

**Voicebox exposes a local unauthenticated API**, so keep it bound to localhost. This provisioning script explicitly rejects remote URLs.


## 3. Render and verify an episode

```bash
python3 .claude/skills/podcast-scout-skill/scripts/narrate.py \
  studio-output/pilot/narration/script.json \
  --out studio-output/pilot/narration --asr --retake 2
```

The script checks all cast identities and profile availability before producing the audio. Female **character** voices are allowed without `--allow-non-male`, because that switch controls the default **narrator** policy. For casting, don't pass `--voice` or override `--engine`; those would bypass individual character assignments and are rejected.

Review:
- `segments/<id>.wav` for each character's actual sound, not just a label.
- `timings.json` for `speaker`, `voice_profile`, `scene_id`, start/end and actual total time.
- `narration.wav` for transitions, consistent loudness, believable delivery and whether characters are genuinely distinct by ear.
- `captions.srt` for correct words (timings are **estimated within segments**; do not claim frame-accurate lip sync).
- `asr.json` when ASR was run; check names, negations and quantities.
- Final `qc_video.py` and independent listening plus owner approval before release.

If the script or cast changes, invalidate and regenerate affected takes; the segment cache includes the speaker/profile name so switching cast assignments is not accidentally reused. A voicebox profile changed *under the same name* may require deleting that speaker's cached `segments/<id>.wav` and `segments/<id>.key` files before regenerating. A finalized scene uses the measured WAV timing, never the guessed word count.

## Creative direction and ethics

- The **channel narrator** introduces and concludes a story; characters have their own voices **only when useful**.
- Historical dialogue, hypothetical debate, dramatization and composite characters must be presented as such—don't invent authentic quotations or misleading historical recordings.
- Never imitate or clone a real person, podcast guest, celebrity or unauthorized third party. Do not use a real person's recognizable voice sample as a synthetic reference.
- Never automatically assign a stereotypical personality or credibility based on a voice's perceived gender. Cast by narrative function, clarity, delivery, and continuity.
- Humanizer may polish **all dialogue** before casting and final voice generation, but a real fact-lock review must follow. The male narrator's voice identity is preserved.
- The sound engineer may balance every speaker at consistent perceived loudness; the final music bed must duck for **all speech**, not only the narrator.
- Future shots can involve one, two, five, or more characters. *You do not need to predefine a fixed number of voices for the entire channel.*
- Continuously evaluate the capability under `external/voicebox` using genuine narrated samples and real QC reports.

**State of implementation:** Per-segment Voicebox routing, name/rights checks, profile lookup, master audio assembly, and speaker-annotated timing files are implemented. Real Voicebox hardware, casting quality, authentic dialogue performances, and local profile generation still require a pilot on the user's machine.

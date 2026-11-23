#!/usr/bin/env python3
"""
Audio stage: per-beat narration + instrumental BGM generation via MuAPI.
"""
import base64
import json
import os
import subprocess

import paid
from provider import get_provider, run_jobs

VOICE_MODEL = "minimax-speech-2.6-turbo"
MUSIC_MODEL = "suno-create-music"

CLONE_TEMPLATE = (
    "**Speaker A** @audio1 keeps their own vocal timbre and speaks fluent natural "
    "{language} with a neutral accent, upbeat pace, crisp articulation, friendly and "
    "energetic like a {persona}. Clean dry studio vocal only — no background music, "
    "no sound effects, no room noise or reverb. They say: \"{script}\""
)
LANG_NAMES = {"en": "English", "zh": "Mandarin Chinese", "ja": "Japanese",
              "ko": "Korean", "es": "Spanish", "fr": "French", "de": "German"}


def probe_dur(path: str) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    try:
        return float(out.strip())
    except ValueError:
        return 0.0


def run(project_dir: str, generate=False, max_jobs=paid.DEFAULT_MAX_JOBS, allow_clone_upload=False):
    bpath = os.path.join(project_dir, "beats.json")
    with open(bpath, encoding="utf-8") as f:
        doc = json.load(f)
    adir = os.path.join(project_dir, "audio")

    prov = get_provider(doc.get("provider"))
    voice = doc.get("voice", {})
    # Hunting Titles rule: male narrator only (minimax roster, references/voices.md); default documentary male.
    MALE = {"English_expressive_narrator", "English_magnetic_voiced_man", "English_Trustworth_Man",
            "English_ManWithDeepVoice", "English_Aussie_Bloke", "Deep_Voice_Man", "Casual_Guy", "Patient_Man"}
    voice_id = voice.get("voice_id", "English_expressive_narrator")
    if voice_id not in MALE and not voice.get("owner_approved_non_male"):
        raise SystemExit(f"audio: voice '{voice_id}' is not on the male allowlist (channel rule). Pick one of {sorted(MALE)}; "
                         "a non-male voice needs the owner's own request, recorded as voice.owner_approved_non_male.")
    language = voice.get("language", doc.get("language", "en"))
    speed = float(voice.get("speed", 1.0))

    clone_ref = voice.get("clone_ref")
    if clone_ref and not voice.get("clone_ref_is_owner_own_voice"):
        # never clone a real person's voice; the only allowed reference is the channel owner's own recording
        raise SystemExit("audio: voice cloning is disabled (channel rule: never clone a real person). Only the owner's "
                         "own recording may be used, recorded as voice.clone_ref_is_owner_own_voice = true.")
    persona = voice.get("persona", "YouTube tutorial creator")
    if clone_ref:
        with open(clone_ref, "rb") as f:
            ref_b64 = base64.b64encode(f.read()).decode()
        lang_name = LANG_NAMES.get(language, language)

    specs = {}
    for beat in doc["beats"]:
        existing = beat.get("audio_path")
        if existing and os.path.exists(existing):
            print(f"[narr_{beat['id']}] reuse existing {existing} (delete it to re-voice)")
            continue
        if clone_ref:
            specs[f"narr_{beat['id']}"] = (lambda t=beat["narration"]: prov.submit_audio(
                VOICE_MODEL,
                text=CLONE_TEMPLATE.format(language=lang_name, persona=persona, script=t),
                format="mp3", sample_rate=44100,
                references=[{"audio_data": ref_b64}]))
        else:
            specs[f"narr_{beat['id']}"] = (lambda t=beat["narration"]: prov.submit_audio(
                VOICE_MODEL, prompt=t, text=t, language=language, voice_id=voice_id,
                codec="mp3", sample_rate=44100, speed=speed))

    bgm_path = os.path.join(adir, "bgm.mp3")
    if not os.path.exists(bgm_path):
        music_prompt = doc.get("music", "cinematic paper-collage explainer BGM, energetic rhythmic beat")
        specs["bgm"] = (lambda mp=music_prompt: prov.submit_audio(
            MUSIC_MODEL, prompt=mp, style=mp, is_instrumental=True, format="mp3"))
    else:
        print(f"[bgm] reuse existing {bgm_path}")

    if clone_ref and not allow_clone_upload and any(k.startswith("narr_") for k in specs):
        # every cloned narration job carries the reference recording to MuAPI's cloud
        raise SystemExit("audio: voice.clone_ref sends the reference recording to MuAPI; "
                         "re-run with --allow-clone-upload to permit that.")
    plan = [(key, MUSIC_MODEL if key == "bgm" else VOICE_MODEL,
             bgm_path if key == "bgm" else os.path.join(adir, f"{key}.mp3")) for key in specs]
    if not paid.approve(plan, generate, max_jobs):
        return
    os.makedirs(adir, exist_ok=True)
    done = run_jobs(prov, specs, poll_s=4, stall_s=150, max_retries=2, deadline_s=600)

    for key, url in done.items():
        if not url:
            continue
        dest = os.path.join(adir, "bgm.mp3") if key == "bgm" else os.path.join(adir, f"{key}.mp3")
        prov.download(url, dest)
        if key.startswith("narr_"):
            bid = key.split("narr_")[1]
            for beat in doc["beats"]:
                if str(beat["id"]) == bid:
                    beat["audio_path"] = dest
                    beat["audio_duration"] = probe_dur(dest)
        print(f"[{key}] saved {dest}")

    with open(bpath, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print("Updated", bpath)


if __name__ == "__main__":
    ap = paid.parser(__doc__)
    ap.add_argument("--allow-clone-upload", action="store_true",
                    help="permit sending voice.clone_ref (the owner's own recording) to MuAPI for cloning")
    a = ap.parse_args()
    run(os.path.abspath(a.project_dir), a.generate, a.max_jobs, a.allow_clone_upload)

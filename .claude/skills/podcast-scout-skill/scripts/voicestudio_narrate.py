#!/usr/bin/env python3
"""Generate episode-specific dialogue through local VoiceStudio, then reuse
FounderNotes' existing files-engine for WAV assembly, captions and timings.

This tool NEVER installs engines, creates/clones voices, or sends the script to
a public endpoint. It accepts only local VoiceStudio addresses. No network
request is made with --dry-run. Keep generated recordings under studio-output/.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import wave


def fail(message: str) -> None:
    raise SystemExit("voicestudio_narrate: " + message)


def load_episode(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("episode must be a JSON object")
    roles, segments = data.get("speakers"), data.get("segments")
    if not isinstance(roles, dict) or not roles:
        fail("define speakers as a map of role names to VoiceStudio profile IDs")
    if not isinstance(segments, list) or not segments:
        fail("provide at least one spoken segment")
    seen = set()
    for segment in segments:
        if not isinstance(segment, dict):
            fail("every segment must be an object")
        sid = segment.get("id")
        if not isinstance(sid, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", sid):
            fail("segment id must be a safe 1-80 character filename")
        if sid in seen:
            fail(f"duplicate segment id {sid}")
        seen.add(sid)
        role = segment.get("speaker")
        if role not in roles:
            fail(f"segment {sid}: speaker {role!r} is missing from speakers")
        if not isinstance(segment.get("text"), str) or not segment["text"].strip():
            fail(f"segment {sid}: missing dialogue text")
    return data


def local_url(value: str) -> str:
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
        fail("only an HTTP loopback VoiceStudio backend is supported; no remote scripts or voice data")
    if parsed.username or parsed.password or parsed.query or parsed.fragment or parsed.path not in {"", "/"}:
        fail("VoiceStudio URL must be an HTTP loopback origin with no path, credentials or query")
    return value.rstrip("/")


def signature(fields: dict) -> str:
    return hashlib.sha256(json.dumps(fields, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def valid_wav(data: bytes) -> None:
    if not data.startswith(b"RIFF") or data[8:12] != b"WAVE":
        fail("VoiceStudio returned data that is not a RIFF/WAV recording")
    try:
        with wave.open(io.BytesIO(data), "rb") as wav:
            if wav.getnframes() <= 0 or wav.getframerate() <= 0:
                fail("VoiceStudio returned an empty WAV recording")
    except (wave.Error, EOFError) as exc:
        fail(f"VoiceStudio returned an invalid WAV recording: {exc}")


def synthesize(origin: str, fields: dict, timeout: int) -> bytes:
    body = urllib.parse.urlencode(fields).encode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Accept": "audio/wav"}
    key = os.environ.get("OMNIVOICE_API_KEY")
    if key:
        headers["Authorization"] = f"Bearer {key}"
    request = urllib.request.Request(origin + "/generate", body, headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            lost = response.headers.get("X-OmniVoice-Dropped-Chunks", "0")
            if lost.isdigit() and int(lost) > 0:
                fail(f"VoiceStudio dropped {lost} speech chunks; regenerate and listen before release")
            audio = response.read()
    except urllib.error.HTTPError as exc:
        fail(f"VoiceStudio /generate failed: HTTP {exc.code}. Check profile, model installation, and server logs")
    except (urllib.error.URLError, TimeoutError) as exc:
        fail(f"VoiceStudio not reachable on this machine: {exc}")
    valid_wav(audio)
    return audio


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path, help="original dialogue JSON using speakers and segments")
    parser.add_argument("--out", required=True, type=Path, help="episode narration directory")
    parser.add_argument("--url", default=os.environ.get("VOICESTUDIO_URL", "http://127.0.0.1:3900"))
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--dry-run", action="store_true", help="validate dialogue and show route without generating audio")
    parser.add_argument("--force", action="store_true", help="regenerate every VoiceStudio take")
    args = parser.parse_args(argv)
    origin = local_url(args.url)
    if not 10 <= args.timeout <= 7200:
        fail("timeout must be 10-7200 seconds")
    data = load_episode(args.script)
    speakers = data["speakers"]
    if not args.dry_run:
        for role, profile in speakers.items():
            if (not isinstance(profile, dict)
                or not isinstance(profile.get("profile_id"), str)
                or not profile["profile_id"].strip()
                or profile["profile_id"].startswith("REPLACE_")):
                fail(f"set a real profile_id for speaker {role!r} in {args.script}")
    out = args.out.resolve()
    raw = out / "voicestudio-raw"
    if args.dry_run:
        print(json.dumps({"status": "dry-run", "engine": "voicestudio",
                          "endpoint": origin + "/generate", "out": str(out),
                          "segments": [{"id": s["id"], "speaker": s["speaker"], "scene_id": s.get("scene_id")}
                                       for s in data["segments"]]}, indent=2))
        return 0
    raw.mkdir(parents=True, exist_ok=True)
    for idx, seg in enumerate(data["segments"]):
        sid, role = seg["id"], seg["speaker"]
        profile = speakers[role]
        # The base OmniVoice engine doesn't implement emotion instructions.
        # Only pass engine/delivery controls selected and tested by the owner.
        fields = {"text": seg["text"].strip(), "profile_id": profile["profile_id"],
                  "language": seg.get("language", "en"), "speed": "1.0",
                  "seed": str(seg.get("seed", 1200 + idx)), "wav_bits": "16"}
        for name in ("engine", "instruct", "emotion", "postprocess_output"):
            value = seg.get(name, profile.get(name))
            if value is not None:
                fields[name] = str(value).lower() if isinstance(value, bool) else str(value)
        wav_path = raw / f"{sid}.wav"
        key_path = raw / f"{sid}.key"
        key = signature(fields)
        if not args.force and wav_path.is_file() and key_path.is_file() and key_path.read_text() == key:
            print(f"[cached] {sid}: {role}")
            continue
        print(f"[VoiceStudio] {sid}: {role} ({len(seg['text'])} characters)", flush=True)
        audio = synthesize(origin, fields, args.timeout)
        temporary = raw / f"{sid}.wav.partial"
        temporary.write_bytes(audio)
        temporary.replace(wav_path)
        key_path.write_text(key, encoding="utf-8")

    # narrate.py's native cast validator is Voicebox-only. Strip cast metadata
    # for this existing files-engine path, then restore metadata in timings.json.
    clean = {
        "voice": {"engine": "files", "speed": 1.0, "chain": "none"},
        "lead": data.get("lead", 0.3),
        "tail": data.get("tail", 0.8),
        "segments": [
            {k: value for k, value in seg.items()
             if k in {"id", "text", "display", "pause_after", "scene_id"}}
            for seg in data["segments"]
        ],
    }
    input_path = out / "voicestudio-files-input.json"
    input_path.write_text(json.dumps(clean, indent=2, ensure_ascii=False), encoding="utf-8")
    native = Path(__file__).with_name("narrate.py")
    if not native.is_file():
        fail(f"missing FounderNotes narration tool: {native}")
    subprocess.run(
        [sys.executable, str(native), str(input_path), "--out", str(out),
         "--engine", "files", "--files-dir", str(raw)], check=True
    )
    timing_path = out / "timings.json"
    timings = json.loads(timing_path.read_text(encoding="utf-8"))
    # FounderNotes currently stores the timed list at meta.segments.
    for item, source in zip(timings.get("segments", []), data["segments"]):
        role = source["speaker"]
        item.update({"speaker": role, "scene_id": source.get("scene_id"),
                     "role": "character", "voice_profile": speakers[role]["profile_id"],
                     "voice_engine": "voicestudio"})
    timings["voice_source"] = "voicestudio"
    timing_path.write_text(json.dumps(timings, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Created {out / 'narration.wav'} and {timing_path}. Listen and review before video release.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

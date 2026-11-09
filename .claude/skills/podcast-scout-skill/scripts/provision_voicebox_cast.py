#!/usr/bin/env python3
"""Provision approved ORIGINAL SYNTHETIC character profiles in a local Voicebox.

No human voice cloning. No cloud service, auto-login, paid operations, or
automatic synthesis of reference voices. The owner first supplies and
approves reference WAVs generated for original characters.
Dry run is the default; --create explicitly authorizes local profile writes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.request
import wave
from pathlib import Path
from urllib.parse import urlsplit

DEFAULT_URL = "http://127.0.0.1:17493"
MAX_WAV_BYTES = 16 * 1024 * 1024


def local_base(url):
    parts = urlsplit(url)
    if parts.scheme != "http" or parts.hostname not in ("127.0.0.1", "localhost", "::1"):
        raise ValueError("Profile provisioning is allowed only to a local HTTP Voicebox server")
    if parts.path not in ("", "/") or parts.query or parts.fragment or parts.username or parts.password:
        raise ValueError("Invalid Voicebox base URL")
    return url.rstrip("/")


def read_cast(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("cast"), dict):
        raise ValueError("Script needs a cast object")
    cast = data["cast"]
    if not cast.get("narrator"):
        raise ValueError("Narrator entry is missing")
    return cast


def verify_reference(entry, path, root):
    if entry.get("approved") is not True or entry.get("synthetic_voice") is not True:
        raise ValueError(f"{path}: original synthetic voice and owner approval must be declared")
    name = entry.get("profile_name")
    if not isinstance(name, str) or not name.strip() or len(name) > 100:
        raise ValueError(f"{path}: profile_name is missing or too long")
    reference = entry.get("reference_wav")
    transcript = entry.get("reference_text")
    if not isinstance(reference, str) or not reference.strip():
        raise ValueError(f"{path}: reference_wav is required to create a new profile")
    if not isinstance(transcript, str) or not transcript.strip() or len(transcript) > 1000:
        raise ValueError(f"{path}: reference_text is required, max 1000 characters")
    sample = Path(reference)
    if not sample.is_absolute():
        sample = root / sample
    sample = sample.resolve()
    if not sample.is_file() or sample.suffix.lower() != ".wav":
        raise ValueError(f"{path}: expected an existing .wav reference")
    if sample.stat().st_size > MAX_WAV_BYTES:
        raise ValueError(f"{path}: WAV reference exceeds {MAX_WAV_BYTES} bytes")
    try:
        with wave.open(str(sample), "rb") as wav:
            if wav.getnframes() == 0 or wav.getframerate() <= 0 or wav.getnchannels() not in (1, 2):
                raise ValueError("empty/invalid WAV")
            duration = wav.getnframes() / wav.getframerate()
            if duration > 40:
                raise ValueError("reference WAV should be <=40 seconds")
    except (wave.Error, EOFError) as exc:
        raise ValueError(f"{path}: bad WAV format: {exc}") from exc
    return sample


def profiles(base):
    with urllib.request.urlopen(base + "/profiles", timeout=30) as response:
        result = json.loads(response.read())
    if not isinstance(result, list):
        raise ValueError("Local Voicebox /profiles returned unexpected data")
    return result


def create_profile(base, entry, sample):
    name = entry["profile_name"]
    data = json.dumps({
        "name": name, "language": "en", "voice_type": "cloned",
        "description": "Owner-approved original synthetic fictional character voice"
    }).encode()
    req = urllib.request.Request(base + "/profiles", data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as response:
        identity = json.loads(response.read())["id"]
    boundary = "----fncast" + hashlib.sha256((name + entry["reference_text"]).encode()).hexdigest()[:14]
    text = entry["reference_text"]
    prefix = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"reference_text\"\r\n\r\n{text}\r\n"
              f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"synthetic.wav\"\r\n"
              f"Content-Type: audio/wav\r\n\r\n").encode()
    body = prefix + sample.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(base + f"/profiles/{identity}/samples", data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=60) as response:
        response.read()
    return identity


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path)
    parser.add_argument("--url", default=os.environ.get("VOICEBOX_URL", DEFAULT_URL))
    parser.add_argument("--create", action="store_true",
                        help="Explicitly create missing original synthetic profiles in local Voicebox")
    args = parser.parse_args(argv)
    try:
        base = local_base(args.url)
        cast = read_cast(args.script)
        existing = profiles(base)
        pending = []
        for speaker, entry in cast.items():
            if speaker == "narrator":
                continue  # the regular narrator provisioner owns the permanent narrator
            matches = [x for x in existing if isinstance(x, dict)
                       and x.get("name") == entry.get("profile_name")]
            if len(matches) > 1:
                raise ValueError(f"{speaker}: ambiguous existing profile name")
            if matches and matches[0].get("sample_count", 1) != 0:
                print(f"EXISTS {speaker}: {entry['profile_name']}")
                continue
            sample = verify_reference(entry, speaker, args.script.parent.resolve())
            if matches:
                raise ValueError(f"{speaker}: profile already exists without a sample; "
                                 "repair it in Voicebox UI rather than creating a duplicate")
            pending.append((speaker, entry, sample))
            print(f"{'CREATE' if args.create else 'NEEDS_SETUP'} {speaker}: {entry['profile_name']} ({sample.name})")
        if not args.create:
            print("DRY RUN: no profiles created. Pass --create after reviewing original synthetic references.")
            return 0
        for speaker, entry, sample in pending:
            identity = create_profile(base, entry, sample)
            print(f"CREATED {speaker}: {entry['profile_name']} ({identity})")
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

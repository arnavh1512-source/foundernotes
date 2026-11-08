#!/usr/bin/env python3
"""Fetch candidate Openverse sound effects with license and file integrity checks.

Only media whose metadata explicitly allows commercial reuse (CC0 or CC BY)
is considered. A search result is NOT a rights guarantee: verify its source
and attribution again before publication. No downloaded clip is auto-approved.

Usage: python3 fetch_sfx.py roles.json --out DIR [--per 4] [--license cc0|by]
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import math
import os
import re
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

API = "https://api.openverse.org/v1/audio/"
MAX_BYTES = 24 * 1024 * 1024
EXTENSIONS = {".mp3", ".wav", ".ogg", ".oga", ".flac", ".m4a", ".webm"}
LICENSES = {"cc0": {"cc0"}, "by": {"cc0", "by"}}


def safe_url(url):
    if not isinstance(url, str):
        return False
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password:
        return False
    host = parts.hostname.lower().rstrip(".")
    if host in {"localhost", "localhost.localdomain"} or host.endswith((".local", ".internal")):
        return False
    try:
        address = ipaddress.ip_address(host)
        if not address.is_global:
            return False
    except ValueError:
        pass
    return True


class SafeRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not safe_url(newurl):
            raise ValueError("Refusing unsafe audio URL redirect")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def open_safe(url, timeout=30):
    if not safe_url(url):
        raise ValueError("Refusing unsafe/non-HTTPS audio URL")
    opener = urllib.request.build_opener(SafeRedirects())
    return opener.open(urllib.request.Request(url, headers={"User-Agent": "FounderNotes/1.0"}), timeout=timeout)


def licensed(record, mode):
    if not isinstance(record, dict):
        return False
    code = str(record.get("license") or "").strip().lower().replace("cc-", "")
    return code in LICENSES[mode] and safe_url(record.get("url"))


def safe_role(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", value):
        raise ValueError(f"Unsafe role identifier: {value!r}")
    return value


def duration_ms(value):
    try:
        result = float(value)
        return result if math.isfinite(result) and result > 0 else None
    except (TypeError, ValueError, OverflowError):
        return None


def audio_signature(data):
    if data.startswith(b"ID3") or (len(data) > 1 and data[0] == 0xFF and data[1] & 0xE0 == 0xE0):
        return "mp3"
    if data.startswith(b"RIFF") and data[8:12] == b"WAVE":
        return "wav"
    if data.startswith(b"OggS"):
        return "ogg"
    if data.startswith(b"fLaC"):
        return "flac"
    if len(data) >= 12 and data[4:8] == b"ftyp":
        return "m4a"
    if data.startswith(b"\x1a\x45\xdf\xa3"):
        return "webm"
    return None


def search(query, mode, n=20):
    params = {"q": query, "license": "cc0,by" if mode == "by" else "cc0",
              "page_size": n, "mature": "false"}
    url = API + "?" + urllib.parse.urlencode(params)
    with open_safe(url, timeout=30) as response:
        result = json.load(response)
    return result.get("results", []) if isinstance(result, dict) else []


def download_candidate(url, destination, max_bytes=MAX_BYTES):
    """Stream to a temp file and atomically publish only validated audio."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    digest = hashlib.sha256()
    total = 0
    try:
        with open_safe(url, timeout=60) as response:
            with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=".sfx-", delete=False) as output:
                temp_name = Path(output.name)
                prefix = b""
                for chunk in iter(lambda: response.read(65536), b""):
                    total += len(chunk)
                    if total > max_bytes:
                        raise ValueError("Audio exceeds maximum allowed size")
                    if len(prefix) < 16:
                        prefix += chunk[:16 - len(prefix)]
                    digest.update(chunk)
                    output.write(chunk)
        if not total or not audio_signature(prefix):
            raise ValueError("Missing or invalid audio file signature")
        os.replace(temp_name, destination)
        temp_name = None
        return {"bytes": total, "sha256": digest.hexdigest(), "detected_format": audio_signature(prefix)}
    finally:
        if temp_name is not None:
            temp_name.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--per", type=int, default=4)
    parser.add_argument("--license", choices=sorted(LICENSES), default="cc0")
    parser.add_argument("--max-mb", type=int, default=24)
    args = parser.parse_args(argv)
    if args.per < 1 or args.per > 20 or args.max_mb < 1 or args.max_mb > 100:
        parser.error("--per must be 1..20 and --max-mb must be 1..100")
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        if not isinstance(spec, dict):
            raise ValueError("spec must be an object")
        for role in spec:
            if not role.startswith("_"):
                safe_role(role)
        args.out.mkdir(parents=True, exist_ok=True)
    except (OSError, ValueError, AttributeError) as error:
        parser.error(str(error))

    sources = {}
    for role, details in spec.items():
        if role.startswith("_"):
            continue
        if not isinstance(details, dict) or not isinstance(details.get("q"), str) or not details["q"].strip():
            print(f"fetch_sfx: {role}: missing search query", file=sys.stderr)
            sources[role] = []
            continue
        try:
            results = search(details["q"], args.license)
        except Exception as error:
            print(f"fetch_sfx: {role}: search failed ({error})", file=sys.stderr)
            sources[role] = []
            continue
        limit_s = duration_ms(details.get("max_s", 12)) or 12.0
        ideal_s = duration_ms(details.get("ideal_s", 3)) or 3.0
        eligible = [item for item in results if licensed(item, args.license) and
                    (duration_ms(item.get("duration")) or float("inf")) <= limit_s * 1000]
        eligible.sort(key=lambda item: abs(float(item["duration"]) - ideal_s * 1000))
        folder = args.out / role
        folder.mkdir(parents=True, exist_ok=True)
        entries = []
        for item in eligible:
            if len(entries) >= args.per:
                break
            url = item["url"]
            extension = Path(urllib.parse.urlsplit(url).path).suffix.lower()
            if extension not in EXTENSIONS:
                continue
            target = folder / f"{len(entries)}{extension}"
            try:
                details_file = download_candidate(url, target, args.max_mb * 1024 * 1024)
            except (OSError, ValueError, urllib.error.URLError) as error:
                print(f"fetch_sfx: {role}: download failed ({error})", file=sys.stderr)
                continue
            entries.append({"file": str(target), "title": item.get("title"),
                            "creator": item.get("creator"), "license": item.get("license"),
                            "license_version": item.get("license_version"),
                            "license_url": item.get("license_url"),
                            "landing": item.get("foreign_landing_url"),
                            "duration_s": float(item["duration"]) / 1000, **details_file})
            time.sleep(0.3)
        sources[role] = entries
        print(f"{role:12s} {len(entries)} candidate(s)")
    (args.out / "sources.json").write_text(json.dumps(sources, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

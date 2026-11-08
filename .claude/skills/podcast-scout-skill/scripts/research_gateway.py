#!/usr/bin/env python3
"""FounderNotes default read-only research gateway.

Agent-Reach 1.6+ is the FIRST attempted provider for public web research
and YouTube discovery/subtitles. This wrapper NEVER installs dependencies,
logs in, copies browser state, invokes paid transcription, or bypasses
platform limits. If unavailable, it returns a structured directive for the
Claude Code researcher to use *authorized native tools* (it cannot invoke
host tools itself).

Examples (run from any directory):
    python3 research_gateway.py status
    python3 research_gateway.py search "What causes ..."
    python3 research_gateway.py read https://example.org/paper
    python3 research_gateway.py youtube-search "verified topic"
    python3 research_gateway.py transcript https://youtube.com/watch?v=...
"""
from __future__ import annotations

import argparse
import datetime as dt
import ipaddress
import json
import os
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path

MAX_RESPONSE_BYTES = 5_000_000
STOP_ERRORS = {"RATE_LIMITED", "PLATFORM_BLOCKED", "NEED_LOGIN", "BUSY", "BAD_INPUT", "NOT_FOUND"}
FALLBACK_ERRORS = {"NEED_SETUP", "UPSTREAM_BROKEN", "TIMEOUT"}
COMMANDS = {"status", "search", "read", "youtube-search", "transcript"}


def _public_url(value):
    if not isinstance(value, str):
        return False
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    try:
        port = parsed.port
    except ValueError:
        return False
    if parsed.username or parsed.password or port not in (None, 80, 443):
        return False
    hostname = parsed.hostname.lower().rstrip(".")
    if hostname in {"localhost", "localhost.localdomain"} or hostname.endswith((".localhost", ".local", ".internal")):
        return False
    try:
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        return True
    return ip.is_global


def _youtube_target(value):
    if not isinstance(value, str):
        return False
    if len(value) == 11 and all(x.isascii() and (x.isalnum() or x in "-_") for x in value):
        return True
    if not _public_url(value):
        return False
    hostname = (urllib.parse.urlsplit(value).hostname or "").lower()
    return hostname in {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


def _utc():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def _result(operation, *, ok=False, provider="agent-reach", channel=None, items=None,
            error_code=None, reason=None, hint=None, fallback=None, backend=None):
    return {
        "operation": operation, "ok": ok, "provider": provider if ok else None,
        "channel": channel, "backend": backend, "retrieved_at": _utc(),
        "items": items if isinstance(items, list) else [],
        "error": {"code": error_code, "message": reason, "hint": hint} if error_code else None,
        "fallback": fallback,
    }


def _fallback(operation, *, code, message, hint=""):
    # Do not route around access controls or rate limits; defer to the owner.
    allowed = code not in STOP_ERRORS
    instruction = (
        "Use the host's authorized native search/read/transcript tools; record the actual source "
        "and unavailable Agent-Reach channel. Do not claim Agent-Reach was used."
        if allowed else
        "Stop this retrieval; report the provider's restriction. Do not rotate accounts, "
        "bypass verification, or automatically retry another backend."
    )
    return _result(operation, error_code=code, reason=message, hint=hint,
                   fallback={"allowed": allowed, "instruction": instruction})


def _binary():
    override = os.environ.get("FOUNDERNOTES_AGENT_REACH_BIN")
    return override or shutil.which("agent-reach")


def _execute(arguments, *, executable=None, timeout=45):
    executable = executable or _binary()
    if not executable:
        return None, "NOT_INSTALLED", "Agent-Reach is not installed on this machine"
    try:
        completed = subprocess.run(
            [executable, *arguments], check=False, capture_output=True,
            text=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT", "Agent-Reach timed out (no automatic retry)"
    except OSError:
        return None, "NEED_SETUP", "Could not launch the installed Agent-Reach executable"
    if len(completed.stdout.encode("utf-8")) > MAX_RESPONSE_BYTES:
        return None, "TOO_LARGE", "Agent-Reach response exceeded the safe output limit"
    try:
        payload = json.loads(completed.stdout.strip())
    except (ValueError, TypeError):
        return None, "INVALID_RESPONSE", "Agent-Reach did not return its expected JSON envelope"
    if not isinstance(payload, dict):
        return None, "INVALID_RESPONSE", "Agent-Reach response was not a JSON object"
    if payload.get("ok") is not True or completed.returncode != 0:
        error = payload.get("error") if isinstance(payload.get("error"), dict) else {}
        return None, error.get("code") or "UPSTREAM_BROKEN", str(error.get("message") or "Agent-Reach reported a failure")[:300]
    return payload, None, None


def run(operation, value=None, *, limit=5, timeout=45, executable=None):
    if operation not in COMMANDS:
        return _fallback(operation, code="BAD_INPUT", message="Unsupported research operation")
    if operation in {"search", "youtube-search"} and (not isinstance(value, str) or not value.strip()):
        return _fallback(operation, code="BAD_INPUT", message="A search query is required")
    if operation == "read" and not _public_url(value):
        return _fallback(operation, code="BAD_INPUT", message="A public HTTP(S) URL is required")
    if operation == "transcript" and not _youtube_target(value):
        return _fallback(operation, code="BAD_INPUT", message="A public YouTube URL or video ID is required")
    if not 1 <= limit <= 10:
        return _fallback(operation, code="BAD_INPUT", message="Search limit must be between 1 and 10")
    routing = {
        "status": ["channels"],
        "search": ["web", "search", value or "", "--limit", str(limit)],
        "read": ["web", "read", value or ""],   # only the public web channel; never logged-in channels
        "youtube-search": ["youtube", "search", value or "", "--limit", str(limit)],
        "transcript": ["youtube", "subtitle", value or "", "--lang", "en,en-orig"],
    }
    payload, code, message = _execute(routing[operation], executable=executable, timeout=timeout)
    if code:
        return _fallback(operation, code=code, message=message)
    if operation == "status":
        channels = payload.get("channels")
        if not isinstance(channels, list):
            return _fallback(operation, code="INVALID_RESPONSE", message="Missing channel inventory")
        selected = [item for item in channels if isinstance(item, dict) and
                    item.get("name") in {"web", "youtube"}]
        return _result(operation, ok=True, channel="inventory", items=selected)
    items = payload.get("items")
    if not isinstance(items, list):
        return _fallback(operation, code="INVALID_RESPONSE", message="Missing structured source items")
    if not items or not any(isinstance(item, dict) and
                            (item.get("text") or item.get("url")) for item in items):
        return _fallback(operation, code="NO_CONTENT", message="No usable source content returned")
    if operation == "transcript" and not any(isinstance(item, dict) and
                                              isinstance(item.get("text"), str) and
                                              item["text"].strip() for item in items):
        return _fallback(operation, code="NO_TRANSCRIPT", message="Subtitle content unavailable")
    return _result(operation, ok=True, channel=payload.get("channel"),
                   backend=payload.get("backend"), items=items)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=sorted(COMMANDS))
    parser.add_argument("value", nargs="?")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--timeout", type=float, default=45)
    args = parser.parse_args(argv)
    if not (1 <= args.timeout <= 120):
        parser.error("--timeout must be 1 to 120 seconds")
    result = run(args.operation, args.value, limit=args.limit, timeout=args.timeout)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""FounderNotes default read-only research gateway.

Agent-Reach 1.6+ is the FIRST attempted provider for public web search and
reading. For YouTube (search and subtitles) yt-dlp is tried first (owner rule,
2026-11-19) and Agent-Reach is the backup when yt-dlp is missing, fails or
finds no subtitles. A rate limit or bot/login block STOPS the request; it is
never retried through another backend. This wrapper NEVER installs dependencies,
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
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

MAX_RESPONSE_BYTES = 5_000_000
STOP_ERRORS = {"RATE_LIMITED", "PLATFORM_BLOCKED", "NEED_LOGIN", "BUSY", "BAD_INPUT", "NOT_FOUND"}
FALLBACK_ERRORS = {"NEED_SETUP", "UPSTREAM_BROKEN", "TIMEOUT"}
COMMANDS = {"status", "search", "read", "youtube-search", "transcript"}


def _public_url(value, *, resolve=True):
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
        return ipaddress.ip_address(hostname).is_global
    except ValueError:
        pass
    # Legacy IPv4 spellings (2130706433, 127.1, 0x7f.0.0.1): a numeric last label is an address.
    if re.fullmatch(r"\d+|0x[0-9a-f]*", hostname.rsplit(".", 1)[-1]):
        return False
    if not resolve:
        return True
    # ponytail: checks DNS once; the reader re-resolves, so rebinding needs a pinned-IP fetch to close.
    try:
        infos = socket.getaddrinfo(hostname, port or (443 if parsed.scheme == "https" else 80),
                                   type=socket.SOCK_STREAM)
        return bool(infos) and all(ipaddress.ip_address(info[4][0]).is_global for info in infos)
    except (OSError, UnicodeError, ValueError):
        return False


def _youtube_target(value):
    if not isinstance(value, str):
        return False
    if len(value) == 11 and all(x.isascii() and (x.isalnum() or x in "-_") for x in value):
        return True
    # The YouTube host allowlist below makes a DNS check unnecessary.
    if not _public_url(value, resolve=False):
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


def _ytdlp_binary():
    override = os.environ.get("FOUNDERNOTES_YTDLP_BIN")
    if override:
        return override
    found = shutil.which("yt-dlp")
    if found:
        return found
    venv = Path(os.environ.get("STUDIO_VENV", Path.home() / ".cache" / "studio-venv"))
    venv = venv / ("Scripts/yt-dlp.exe" if os.name == "nt" else "bin/yt-dlp")
    return str(venv) if venv.is_file() and os.access(venv, os.X_OK) else None


def _watch_url(value):
    if value.startswith(("http://", "https://")):
        return value
    return "https://www.youtube.com/watch?v=" + value


def _ytdlp_error(stderr):
    text = (stderr or "").lower()
    if re.search(r"http error 429\b|too many requests", text):
        return "RATE_LIMITED", "YouTube rate-limited yt-dlp (HTTP 429)"
    if "not a bot" in text or "confirm you" in text:
        return "PLATFORM_BLOCKED", "YouTube asked yt-dlp to sign in to confirm it is not a bot"
    if "private video" in text or "members-only" in text or "sign in" in text:
        return "NEED_LOGIN", "This video needs a signed-in account"
    if "video unavailable" in text or "does not exist" in text:
        return "NOT_FOUND", "Video unavailable"
    return "UPSTREAM_BROKEN", "yt-dlp failed: " + (stderr or "").strip().splitlines()[-1][:200] if (stderr or "").strip() else "yt-dlp failed"


def _vtt_text(content):
    lines, previous = [], None
    for raw in content.splitlines():
        line = raw.strip()
        if (not line or line.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")) or "-->" in line
                or line.isdigit()):
            continue
        line = " ".join("".join(part.split(">")[-1] for part in line.split("<")).split())
        if line and line != previous:
            lines.append(line)
            previous = line
    return " ".join(lines)


def _run_ytdlp(arguments, executable, timeout):
    try:
        # --ignore-config: never pick up user/system config (cookies, browser state, proxies).
        return subprocess.run([executable, "--ignore-config", *arguments], check=False, capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=timeout), None
    except subprocess.TimeoutExpired:
        return None, ("TIMEOUT", "yt-dlp timed out (no automatic retry)")
    except OSError:
        return None, ("NEED_SETUP", "Could not launch yt-dlp")


def _ytdlp(operation, value, *, limit, timeout, executable=None):
    """Return (result, None) on success or (None, (code, message)) on failure."""
    executable = executable or _ytdlp_binary()
    if not executable:
        return None, ("NOT_INSTALLED", "yt-dlp is not installed (run setup_studio.sh)")
    if operation == "youtube-search":
        completed, err = _run_ytdlp(["--flat-playlist", "--dump-single-json", "--no-warnings",
                                     "--", f"ytsearch{limit}:{value}"], executable, timeout)
        if err:
            return None, err
        if completed.returncode != 0:
            return None, _ytdlp_error(completed.stderr)
        try:
            entries = json.loads(completed.stdout).get("entries") or []
        except (ValueError, AttributeError):
            return None, ("INVALID_RESPONSE", "yt-dlp did not return JSON")
        items = [{"title": e.get("title"), "url": e.get("url") or _watch_url(e.get("id", "")),
                  "channel": e.get("channel") or e.get("uploader"), "duration": e.get("duration"),
                  "view_count": e.get("view_count")}
                 for e in entries if isinstance(e, dict) and e.get("id")]
        if not items:
            return None, ("NO_CONTENT", "yt-dlp search returned no videos")
        return _result(operation, ok=True, provider="yt-dlp", channel="youtube",
                       backend="yt-dlp", items=items), None
    url = _watch_url(value)
    with tempfile.TemporaryDirectory() as tmp:
        completed, err = _run_ytdlp(["--skip-download", "--write-subs", "--write-auto-subs",
                                     "--sub-langs", "en,en-orig", "--sub-format", "vtt",
                                     "--no-playlist", "--no-warnings",
                                     "-o", str(Path(tmp) / "sub.%(ext)s"), "--", url],
                                    executable, timeout)
        if err:
            return None, err
        files = sorted(Path(tmp).glob("*.vtt"), key=lambda f: (not f.name.endswith(".en.vtt"), f.name))
        for subtitle in files:
            text = _vtt_text(subtitle.read_text(encoding="utf-8", errors="replace"))
            if text:
                language = subtitle.name.split(".")[-2]
                return _result(operation, ok=True, provider="yt-dlp", channel="youtube",
                               backend="yt-dlp", items=[{"url": url, "language": language,
                                                         "text": text}]), None
    if completed.returncode != 0:
        return None, _ytdlp_error(completed.stderr)  # a crash is not "no subtitles"
    return None, ("NO_TRANSCRIPT", "yt-dlp found no English subtitles")


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


def run(operation, value=None, *, limit=5, timeout=45, executable=None, ytdlp_executable=None):
    if operation not in COMMANDS:
        return _fallback(operation, code="BAD_INPUT", message="Unsupported research operation")
    if operation in {"search", "youtube-search"} and (not isinstance(value, str) or not value.strip()):
        return _fallback(operation, code="BAD_INPUT", message="A search query is required")
    if operation in {"search", "youtube-search"} and value.startswith("-"):
        # Agent-Reach takes the query positionally; a leading '-' would be parsed as an option.
        return _fallback(operation, code="BAD_INPUT", message="A search query must not start with '-'")
    if operation == "read" and not _public_url(value):
        return _fallback(operation, code="BAD_INPUT", message="A public HTTP(S) URL is required")
    if operation == "transcript" and not _youtube_target(value):
        return _fallback(operation, code="BAD_INPUT", message="A public YouTube URL or video ID is required")
    if not 1 <= limit <= 10:
        return _fallback(operation, code="BAD_INPUT", message="Search limit must be between 1 and 10")
    first_attempt = None
    if operation in {"youtube-search", "transcript"}:
        result, failure = _ytdlp(operation, value, limit=limit, timeout=timeout,
                                 executable=ytdlp_executable)
        if result:
            return result
        code, message = failure
        first_attempt = {"provider": "yt-dlp", "code": code, "message": message}
        if code in STOP_ERRORS:
            stopped = _fallback(operation, code=code, message=message)
            stopped["attempts"] = [first_attempt]
            return stopped
    routing = {
        "status": ["channels"],
        "search": ["web", "search", value or "", "--limit", str(limit)],
        "read": ["web", "read", value or ""],   # only the public web channel; never logged-in channels
        "youtube-search": ["youtube", "search", value or "", "--limit", str(limit)],
        # A bare ID may start with '-'; pass it as a URL so it can never read as an option.
        "transcript": ["youtube", "subtitle", _watch_url(value or ""), "--lang", "en,en-orig"],
    }
    result = _agent_reach(operation, routing[operation], executable=executable, timeout=timeout)
    if first_attempt:
        result["attempts"] = [first_attempt, {"provider": "agent-reach",
                                              "code": (result.get("error") or {}).get("code")}]
    return result


def _agent_reach(operation, arguments, *, executable, timeout):
    payload, code, message = _execute(arguments, executable=executable, timeout=timeout)
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

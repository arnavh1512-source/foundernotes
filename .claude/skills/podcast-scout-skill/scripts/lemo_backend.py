#!/usr/bin/env python3
"""Optional Lemo-Opuscar frame/scene exporter for FounderNotes.

Only an EXISTING installed upstream library is used. Never installs packages,
copies demo films, uses upstream voice/music, or performs an automatic upload.
A studio-authored project must contain index.html implementing window.READY,
window.DUR, and deterministic window.render(t) per upstream page contract.

Example:
  python3 lemo_backend.py status --library ~/lemo-opuscar
  python3 lemo_backend.py still --library ~/lemo-opuscar --style watercolor \
      --project studio-output/pilot/scenes/01-lemo --seconds 0 1.5 3
  python3 lemo_backend.py render --library ~/lemo-opuscar --style watercolor \
      --project studio-output/pilot/scenes/01-lemo \
      --output studio-output/pilot/scenes/01-lemo.mp4 --expect-seconds 5
The output is silent: narrate.py + assemble.py own all voices, audio and captions.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path

SCRIPT = Path(__file__).resolve()
CATALOG = SCRIPT.parents[2] / "animation-styles" / "references" / "lemo-opuscar-catalog.json"
DEFAULT_SIZE = "1920x1080"
DEFAULT_FPS = 30
MAX_SECONDS = 1800


def report(operation, ok, **values):
    return {"backend": "lemo-opuscar", "operation": operation, "ok": ok, **values}


def library_path(value=None):
    return Path(value or os.environ.get("FOUNDERNOTES_LEMO_HOME", "~/lemo-opuscar")).expanduser().resolve()


def validated_library(value=None):
    root = library_path(value)
    files = ("core/render/video.mjs", "core/render/still.mjs", "styles/README.md")
    return root if all((root / file).is_file() for file in files) else None


def known_styles():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    styles = {s["slug"]: s for s in data["styles"]}
    if len(styles) != 66 or len(styles) != len(data["styles"]):
        raise ValueError("Lemo style catalog must contain 66 unique styles")
    return styles


def guard_project(project, library):
    folder = Path(project).expanduser().resolve()
    if not (folder / "index.html").is_file():
        return None, "MISSING_INDEX_HTML"
    if folder == library or library in folder.parents:
        return None, "UPSTREAM_DEMO_FORBIDDEN"
    return folder, None


def run_command(argv, *, cwd, timeout):
    if not 1 <= timeout <= 3600:
        return None, "BAD_TIMEOUT"
    try:
        proc = subprocess.run(argv, cwd=cwd, check=False, capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"
    except OSError:
        return None, "COMMAND_UNAVAILABLE"
    if proc.returncode:
        return None, "PROCESS_FAILED: " + (proc.stderr or proc.stdout)[-600:]
    return proc, None


def status(library=None):
    root = validated_library(library)
    return report(
        "status", bool(root and shutil.which("node") and shutil.which("ffmpeg")
                       and shutil.which("ffprobe")),
        installed=bool(root), library=str(root or library_path(library)),
        node_available=bool(shutil.which("node")),
        ffmpeg_available=bool(shutil.which("ffmpeg")),
        ffprobe_available=bool(shutil.which("ffprobe")),
        note="Requires Node 20+, FFmpeg 7+, Chromium, upstream npm/Python deps; status does not test rendering.",
    )


def check_output(path, *, expected_seconds=None):
    proc, error = run_command(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height,r_frame_rate,duration:format=duration",
         "-of", "json", str(path)],
        cwd=path.parent, timeout=45,
    )
    if error:
        return report("inspect", False, error="FFPROBE_FAILED", detail=error)
    try:
        streams = json.loads(proc.stdout)["streams"]
        stream = streams[0]
        width, height = int(stream["width"]), int(stream["height"])
        fps = Fraction(stream["r_frame_rate"])
        data = json.loads(proc.stdout)
        duration = float(stream.get("duration") or data["format"]["duration"])
    except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError):
        return report("inspect", False, error="INVALID_VIDEO_METADATA")
    if (width, height) != (1920, 1080) or fps != 30 or not math.isfinite(duration) or duration <= 0:
        return report("inspect", False, error="WRONG_EXPORT_SPEC",
                      actual={"width": width, "height": height, "fps": str(fps), "seconds": duration})
    if expected_seconds is not None and abs(duration - expected_seconds) > max(0.15, 1 / DEFAULT_FPS):
        return report("inspect", False, error="DURATION_MISMATCH",
                      measured_seconds=duration, expected_seconds=expected_seconds)
    return report("inspect", True, width=width, height=height, fps=30, duration_seconds=duration)


def execute(action, *, library=None, style=None, project=None, output=None, seconds=None,
            expected_seconds=None, workers=3, timeout=900):
    root = validated_library(library)
    if root is None:
        return report(action, False, error="LEMO_NOT_INSTALLED",
                      message="Install upstream separately with permission; do not treat the style catalog as an engine")
    if not shutil.which("node") or not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        return report(action, False, error="MISSING_DEPENDENCIES",
                      message="Node, ffmpeg and ffprobe must be present")
    if style not in known_styles():
        return report(action, False, error="UNKNOWN_STYLE")
    if not (root / "styles" / style / "STYLE.md").is_file():
        return report(action, False, error="MISSING_STYLE_GUIDE")
    folder, err = guard_project(project, root)
    if err:
        return report(action, False, error=err)
    if not 1 <= workers <= 6:
        return report(action, False, error="BAD_WORKER_COUNT")
    if expected_seconds is not None and (not math.isfinite(expected_seconds) or not 0 < expected_seconds <= MAX_SECONDS):
        return report(action, False, error="BAD_EXPECTED_DURATION")
    if action == "still":
        if seconds is None or not isinstance(seconds, list) or not (1 <= len(seconds) <= 12):
            return report(action, False, error="BAD_STILL_TIMES")
        if any(not math.isfinite(t) or t < 0 or t > MAX_SECONDS for t in seconds):
            return report(action, False, error="BAD_STILL_TIMES")
        # Generate stills in the project directory, as upstream default.
        command = ["node", str(root / "core/render/still.mjs"), str(folder),
                   *[str(t) for t in seconds], "--size", DEFAULT_SIZE]
    elif action == "render":
        if not output:
            return report(action, False, error="OUTPUT_REQUIRED")
        path = Path(output).expanduser().resolve()
        if path.suffix.lower() != ".mp4" or not path.parent.is_dir():
            return report(action, False, error="BAD_OUTPUT_PATH")
        if path.exists():
            return report(action, False, error="OUTPUT_EXISTS")
        command = ["node", str(root / "core/render/video.mjs"), str(folder),
                   "--fps", str(DEFAULT_FPS), "--workers", str(workers),
                   "--size", DEFAULT_SIZE, "--out", str(path)]
    else:
        return report(action, False, error="BAD_OPERATION")
    process, problem = run_command(command, cwd=root, timeout=timeout)
    if problem:
        return report(action, False, error="RENDER_FAILED", detail=problem)
    if action == "still":
        return report(action, True, project=str(folder), style=style,
                      note="Inspect actual stills visually; generated files remain in project/stills")
    if not path.is_file() or path.stat().st_size == 0:
        return report(action, False, error="NO_VIDEO_OUTPUT")
    checked = check_output(path, expected_seconds=expected_seconds)
    if not checked["ok"]:
        return report(action, False, error=checked["error"],
                      inspection=checked, output=str(path))
    return report(action, True, style=style, source_library=str(root),
                  output=str(path), inspection=checked, audio="none",
                  note="Still requires FounderNotes linter, assembly, final video QC and creative review")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("status", "still", "render"):
        p = sub.add_parser(name)
        p.add_argument("--library")
        if name != "status":
            p.add_argument("--style", required=True)
            p.add_argument("--project", required=True)
            p.add_argument("--timeout", type=int, default=900)
            p.add_argument("--workers", type=int, default=3)
            if name == "still":
                p.add_argument("--seconds", nargs="+", type=float, required=True)
            else:
                p.add_argument("--output", required=True)
                p.add_argument("--expect-seconds", type=float)
    a = parser.parse_args(argv)
    result = status(a.library) if a.command == "status" else execute(
        a.command, library=a.library, style=a.style, project=a.project,
        output=getattr(a, "output", None), seconds=getattr(a, "seconds", None),
        expected_seconds=getattr(a, "expect_seconds", None),
        workers=a.workers, timeout=a.timeout)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

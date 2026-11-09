#!/usr/bin/env python3
"""Optional raea (Render Anything Engine) backend for FounderNotes.

Works only when a compatible raea executable has been installed by the owner.
Never downloads or installs the engine. All operations run with RAEA_OFFLINE=1
by default, and no shell is invoked.

Quick start:
  python3 raea_backend.py status
  python3 raea_backend.py frame scene.tsx still.png --frame 30
  python3 raea_backend.py render scene.tsx scene.mp4 --manifest scene-manifest.json
  python3 raea_backend.py check scene.mp4 --report raea-check.json
Run the studio's own qc_video.py and human review as well.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

VALID_SOURCES = {".tsx", ".html"}
MAX_RUNTIME = 1800


def installed(executable=None):
    return executable or shutil.which("raea")


def result(action, ok, **extras):
    return {"backend": "raea", "action": action, "ok": bool(ok), **extras}


def _run(args, *, binary=None, timeout=MAX_RUNTIME, allow_network=False):
    cli = installed(binary)
    if not cli:
        return None, result("invoke", False, error="RAEA_NOT_INSTALLED",
                            message="Install raea from its official release after reviewing its license.")
    if timeout <= 0 or timeout > MAX_RUNTIME:
        return None, result("invoke", False, error="BAD_TIMEOUT",
                            message=f"Timeout must be between 1 and {MAX_RUNTIME} seconds.")
    env = os.environ.copy()
    if not allow_network:
        env["RAEA_OFFLINE"] = "1"
    try:
        p = subprocess.run([cli, *[str(x) for x in args]], capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           timeout=timeout, check=False, env=env)
    except subprocess.TimeoutExpired:
        return None, result("invoke", False, error="TIMEOUT", message="raea execution exceeded its time limit.")
    except OSError as exc:
        return None, result("invoke", False, error="EXECUTION_ERROR", message=str(exc)[:300])
    return p, None


def status(*, binary=None):
    process, failure = _run(["--version"], binary=binary, timeout=20)
    if failure:
        return result("status", False, **{k: v for k, v in failure.items() if k not in {"backend", "action", "ok"}})
    return result("status", process.returncode == 0, version=process.stdout.strip()[:180],
                  message=process.stderr.strip()[:250] if process.returncode else "")


def _paths(source, output, *, source_extensions, output_suffix):
    source, output = Path(source).resolve(), Path(output).resolve()
    if not source.is_file() or source.suffix.lower() not in source_extensions:
        return None, None, result("validate", False, error="BAD_SOURCE",
                                  message="Source must be an existing TSX or HTML composition / MP4 file.")
    if output.suffix.lower() != output_suffix:
        return None, None, result("validate", False, error="BAD_OUTPUT",
                                  message=f"Output must end in {output_suffix}.")
    if not output.parent.is_dir():
        return None, None, result("validate", False, error="MISSING_OUTPUT_DIR",
                                  message="Create the output folder before invoking the renderer.")
    if source == output:
        return None, None, result("validate", False, error="OVERWRITE_SOURCE")
    return source, output, None


def render(source, output, *, frame=None, manifest=None, binary=None,
           timeout=MAX_RUNTIME, allow_network=False):
    extension = ".png" if frame is not None else ".mp4"
    src, out, err = _paths(source, output, source_extensions=VALID_SOURCES,
                           output_suffix=extension)
    if err:
        return result("render", False, error=err["error"], message=err.get("message"))
    if frame is not None and (not isinstance(frame, int) or frame < 0):
        return result("render", False, error="BAD_FRAME")
    if out.exists():
        return result("render", False, error="OUTPUT_EXISTS",
                      message="Refusing to overwrite an existing file.")
    args = ["render", str(src), "-o", str(out)]
    if frame is not None:
        args += ["--frame", str(frame)]
    if manifest is not None:
        path = Path(manifest).resolve()
        if frame is not None or not path.parent.is_dir() or path.suffix.lower() != ".json":
            return result("render", False, error="BAD_MANIFEST")
        if path.exists():
            return result("render", False, error="MANIFEST_EXISTS")
        args += ["--manifest", str(path)]
    process, failure = _run(args, binary=binary, timeout=timeout, allow_network=allow_network)
    if failure:
        return result("render", False, error=failure["error"], message=failure.get("message"))
    if process.returncode != 0:
        return result("render", False, error="RENDER_FAILED", exit_code=process.returncode,
                      detail=process.stderr[-1200:])
    if not out.is_file() or out.stat().st_size == 0:
        return result("render", False, error="MISSING_RENDER",
                      message="Renderer exited successfully but no nonempty output was produced.")
    return result("render", True, output=str(out), bytes=out.stat().st_size,
                  manifest=str(Path(manifest).resolve()) if manifest else None,
                  offline=not allow_network)


def check(video, *, report, manifest=None, binary=None, timeout=MAX_RUNTIME):
    src, out, err = _paths(video, report, source_extensions={".mp4"},
                           output_suffix=".json")
    if err:
        return result("check", False, error=err["error"], message=err.get("message"))
    if out.exists():
        return result("check", False, error="OUTPUT_EXISTS")
    args = ["check", str(src)]
    if manifest is not None:
        path = Path(manifest).resolve()
        if not path.is_file() or path.suffix.lower() != ".json":
            return result("check", False, error="MISSING_MANIFEST")
        args += ["--manifest", str(path)]
    args += ["-o", str(out)]
    process, failure = _run(args, binary=binary, timeout=timeout)
    if failure:
        return result("check", False, error=failure["error"], message=failure.get("message"))
    if process.returncode != 0:
        return result("check", False, error="RAEA_CHECK_FAILED", exit_code=process.returncode,
                      detail=process.stderr[-1200:], report=str(out) if out.exists() else None)
    if not out.is_file() or out.stat().st_size == 0:
        return result("check", False, error="MISSING_REPORT")
    try:
        data = json.loads(out.read_text(encoding="utf-8"))
        if not isinstance(data, (dict, list)):
            raise ValueError("report must be JSON object or array")
    except (OSError, ValueError) as exc:
        return result("check", False, error="INVALID_REPORT", message=str(exc))
    return result("check", True, report=str(out), bytes=out.stat().st_size,
                  note="Raea check passed; FounderNotes film QC and human review are still required.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", help="Installed raea executable; default: PATH")
    commands = parser.add_subparsers(dest="operation", required=True)
    commands.add_parser("status")
    for op in ("render", "frame"):
        p = commands.add_parser(op)
        p.add_argument("source")
        p.add_argument("output")
        if op == "frame":
            p.add_argument("--frame", type=int, required=True)
        else:
            p.add_argument("--manifest")
        p.add_argument("--timeout", type=int, default=MAX_RUNTIME)
        p.add_argument("--allow-network", action="store_true",
                       help="Explicitly opt into raea fetching external dependencies/assets.")
    p = commands.add_parser("check")
    p.add_argument("video")
    p.add_argument("--report", required=True)
    p.add_argument("--manifest")
    p.add_argument("--timeout", type=int, default=MAX_RUNTIME)
    args = parser.parse_args(argv)
    if args.operation == "status":
        outcome = status(binary=args.binary)
    elif args.operation in ("render", "frame"):
        outcome = render(args.source, args.output,
                         frame=args.frame if args.operation == "frame" else None,
                         manifest=getattr(args, "manifest", None),
                         binary=args.binary, timeout=args.timeout,
                         allow_network=args.allow_network)
    else:
        outcome = check(args.video, report=args.report, manifest=args.manifest,
                        binary=args.binary, timeout=args.timeout)
    print(json.dumps(outcome, indent=2, ensure_ascii=False))
    return 0 if outcome["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

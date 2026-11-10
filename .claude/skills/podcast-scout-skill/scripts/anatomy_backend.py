#!/usr/bin/env python3
"""Optional preview bridge for separately installed wheresryan22/anatomy.

No automatic installs, remote URLs, demo reuse, overwrite, video-render claims,
or publishing. Local HTML may execute code and access networks; review sources.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REQUIRED = ("SKILL.md", "kit/iso-kit.mjs", "scripts/capture.mjs")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def report(action, ok, **fields):
    return {"backend": "anatomy", "action": action, "ok": bool(ok), **fields}


def library_path(home=None):
    home = (home if home is not None else
            os.environ.get("FOUNDERNOTES_ANATOMY_HOME", str(Path.home() / "studio-tools" / "anatomy")))
    return Path(home).expanduser().resolve()


def installed(home=None):
    root = library_path(home)
    return root if root.is_dir() and all((root / x).is_file() for x in REQUIRED) else None


def node_binary():
    return shutil.which("node")


def node_supported(version):
    match = re.search(r"\bv?(\d+)\.(\d+)\.(\d+)\b", version or "")
    return bool(match and (int(match[1]), int(match[2])) >= (20, 10))


def status(home=None):
    root = installed(home)
    if root is None:
        return report("status", False, installed=False, error="ANATOMY_NOT_INSTALLED",
                      expected_home=str(library_path(home)),
                      message="Install the separate upstream checkout only after owner approval.")
    node = node_binary()
    if not node:
        return report("status", False, installed=True, error="NODE_NOT_FOUND", library=str(root))
    try:
        result = subprocess.run([node, "--version"], capture_output=True, text=True,
                                timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return report("status", False, installed=True, error="NODE_CHECK_FAILED",
                      message=str(exc), library=str(root))
    version = result.stdout.strip()
    if result.returncode != 0 or not node_supported(version):
        return report("status", False, installed=True, error="NODE_UNSUPPORTED",
                      node_version=version, library=str(root))
    return report("status", True, installed=True, node_version=version,
                  library=str(root),
                  note="Only upstream files and Node were checked; Chrome, WebGL and rendering are unverified.")


def still(source, output, *, home=None, width=1920, height=1080,
          scale=1, wait_ms=2500, theme="light", runner=None):
    root = installed(home)
    if root is None:
        return report("still", False, error="ANATOMY_NOT_INSTALLED")
    node = node_binary()
    if not node:
        return report("still", False, error="NODE_NOT_FOUND")
    source, output = Path(source).expanduser().resolve(), Path(output).expanduser().resolve()
    if not source.is_file() or source.suffix.lower() not in (".html", ".svg"):
        return report("still", False, error="INVALID_LOCAL_SOURCE",
                      message="Use an existing trusted local HTML or SVG source.")
    if root == source or root in source.parents:
        return report("still", False, error="UPSTREAM_DEMO_FORBIDDEN",
                      message="Author a new figure outside the Anatomy checkout.")
    if output.suffix.lower() != ".png" or not output.parent.is_dir() or source == output:
        return report("still", False, error="INVALID_OUTPUT")
    if output.exists():
        return report("still", False, error="OUTPUT_EXISTS")
    if not (320 <= width <= 3840 and 240 <= height <= 2160
            and 1 <= scale <= 3 and 0 <= wait_ms <= 30000
            and theme in ("light", "dark")):
        return report("still", False, error="INVALID_OPTIONS")
    command = [node, str(root / "scripts" / "capture.mjs"), str(source),
               "--out", str(output), "--width", str(width), "--height", str(height),
               "--scale", str(scale), "--wait", str(wait_ms), "--theme", theme]
    execute = runner or subprocess.run
    try:
        result = execute(command, capture_output=True, text=True,
                         timeout=120, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return report("still", False, error="CAPTURE_FAILED", message=str(exc))
    if result.returncode:
        return report("still", False, error="CAPTURE_FAILED",
                      exit_code=result.returncode, stderr=(result.stderr or "")[-1200:])
    try:
        with output.open("rb") as fp:
            sig = fp.read(8)
        size = output.stat().st_size
    except OSError:
        return report("still", False, error="MISSING_OUTPUT")
    if sig != PNG_SIGNATURE or size <= 8:
        return report("still", False, error="INVALID_PNG")
    return report("still", True, source=str(source), output=str(output), bytes=size,
                  width=width, height=height,
                  note="Captured a still only; inspect PNG and run independent video QC.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path,
                        help="Separate upstream checkout; else FOUNDERNOTES_ANATOMY_HOME or ~/studio-tools/anatomy")
    actions = parser.add_subparsers(dest="action", required=True)
    actions.add_parser("status")
    preview = actions.add_parser("still")
    preview.add_argument("source", type=Path)
    preview.add_argument("output", type=Path)
    preview.add_argument("--width", type=int, default=1920)
    preview.add_argument("--height", type=int, default=1080)
    preview.add_argument("--scale", type=int, default=1)
    preview.add_argument("--wait-ms", type=int, default=2500)
    preview.add_argument("--theme", choices=("light", "dark"), default="light")
    args = parser.parse_args(argv)
    answer = (status(home=args.home) if args.action == "status"
              else still(args.source, args.output, home=args.home,
                         width=args.width, height=args.height, scale=args.scale,
                         wait_ms=args.wait_ms, theme=args.theme))
    print(json.dumps(answer, indent=2))
    return 0 if answer["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

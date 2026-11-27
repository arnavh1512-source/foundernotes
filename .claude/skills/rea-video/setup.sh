#!/bin/bash
# Install rea-video (Apache-2.0, github.com/JuneYaooo/rea-video) at a pinned commit into its own venv.
# Safe to re-run. Override REA_VIDEO_REF=<sha> to move the pin deliberately.
set -euo pipefail
REF="${REA_VIDEO_REF:-78160e053d378018e970d802d7bb7fa976c649f3}"
SRC="${REA_VIDEO_HOME:-$HOME/studio-tools/rea-video}"
VENV="${REA_VIDEO_VENV:-$HOME/.cache/venv-rea}"
command -v ffmpeg >/dev/null || { echo "rea-video needs ffmpeg"; exit 1; }
if [ ! -d "$SRC/.git" ]; then
  git init -q "$SRC"; git -C "$SRC" remote add origin https://github.com/JuneYaooo/rea-video
fi
if [ "$(git -C "$SRC" rev-parse HEAD 2>/dev/null)" != "$REF" ]; then
  GIT_LFS_SKIP_SMUDGE=1 git -C "$SRC" fetch -q --depth 1 origin "$REF"
  GIT_LFS_SKIP_SMUDGE=1 git -C "$SRC" checkout -q FETCH_HEAD
fi
PY="$(command -v python3 || command -v python)"
[ -x "$VENV/bin/python" ] || "$PY" -m venv "$VENV"
"$VENV/bin/python" -m pip install -q --disable-pip-version-check "$SRC"
"$VENV/bin/rea-video" --help >/dev/null && echo "rea-video ready: $VENV/bin/rea-video (commit ${REF:0:7})"

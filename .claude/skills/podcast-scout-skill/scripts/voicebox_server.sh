#!/usr/bin/env bash
# Install (once) and start the local voicebox server that voices the Founder Notes narrator.
#   bash voicebox_server.sh            -> http://127.0.0.1:17493 (narrate.py's default VOICEBOX_URL)
# voicebox: github.com/jamiepine/voicebox (MIT). Slim install: the server + the Chatterbox/Qwen engines only.
# narrate.py creates the narrator profile from the owner clip in assets/voice/local/ (synthetic fallback:
# assets/voice/founder-notes-narrator-ref.wav).
set -euo pipefail
ROOT="${VOICEBOX_HOME:-$HOME/studio-tools/voicebox}"
VENV="${VOICEBOX_VENV:-$HOME/.cache/venv-voicebox}"
DATA="${VOICEBOX_DATA:-$HOME/.cache/voicebox-data}"
# Pinned upstream commit (main on 2026-11-22). Override with VOICEBOX_REF=<sha> to move it deliberately.
REF="${VOICEBOX_REF:-8af7efe62fab8d33e2a5dfbedabaa45f68a5184f}"
if [ ! -d "$ROOT" ]; then
  git init -q "$ROOT"
  git -C "$ROOT" fetch -q --depth 1 https://github.com/jamiepine/voicebox.git "$REF"
  git -C "$ROOT" checkout -q FETCH_HEAD
fi
BIN="$VENV/bin"; [ -d "$VENV/Scripts" ] && BIN="$VENV/Scripts"     # Windows venvs use Scripts/
PY="$(command -v python3 || command -v python)"
if [ ! -x "$BIN/python" ] && [ ! -x "$BIN/python.exe" ]; then
  "$PY" -m venv "$VENV"
  BIN="$VENV/bin"; [ -d "$VENV/Scripts" ] && BIN="$VENV/Scripts"
  "$BIN/python" -m pip install -q --upgrade pip
  "$BIN/python" -m pip install -q torch torchaudio --index-url https://download.pytorch.org/whl/cpu
  REQ="$(mktemp)"
  grep -v -E "^#|^$|linacodec|Zipvoice|find-links|en_core_web_sm|kokoro|misaki|unidic" "$ROOT/backend/requirements.txt" > "$REQ"
  "$BIN/python" -m pip install -q -r "$REQ"
  rm -f "$REQ"
  "$BIN/python" -m pip install -q --no-deps chatterbox-tts
  "$BIN/python" -m pip install -q -U "ml_dtypes>=0.5"
fi
cd "$ROOT"
exec "$BIN/python" -m backend.main --port "${VOICEBOX_PORT:-17493}" --data-dir "$DATA"

#!/usr/bin/env bash
# Install (once) and start the local voicebox server that voices the Founder Notes narrator.
#   bash voicebox_server.sh            -> http://127.0.0.1:17493 (narrate.py's default VOICEBOX_URL)
# voicebox: github.com/jamiepine/voicebox (MIT). Slim install: the server + the Chatterbox/Qwen engines only.
# The narrator profile is created automatically by narrate.py from assets/voice/founder-notes-narrator-ref.wav.
set -euo pipefail
ROOT="${VOICEBOX_HOME:-$HOME/studio-tools/voicebox}"
VENV="${VOICEBOX_VENV:-$HOME/.cache/venv-voicebox}"
DATA="${VOICEBOX_DATA:-$HOME/.cache/voicebox-data}"
[ -d "$ROOT" ] || git clone -q --depth 1 https://github.com/jamiepine/voicebox.git "$ROOT"
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q --upgrade pip
  "$VENV/bin/pip" install -q torch torchaudio --index-url https://download.pytorch.org/whl/cpu
  grep -v -E "^#|^$|linacodec|Zipvoice|find-links|en_core_web_sm|kokoro|misaki|unidic" "$ROOT/backend/requirements.txt" > /tmp/vb-req.txt
  "$VENV/bin/pip" install -q -r /tmp/vb-req.txt
  "$VENV/bin/pip" install -q --no-deps chatterbox-tts
  "$VENV/bin/pip" install -q -U "ml_dtypes>=0.5"
fi
cd "$ROOT"
exec "$VENV/bin/python" -m backend.main --port "${VOICEBOX_PORT:-17493}" --data-dir "$DATA"

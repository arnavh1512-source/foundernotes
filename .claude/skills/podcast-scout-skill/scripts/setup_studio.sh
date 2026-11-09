#!/usr/bin/env bash
# setup_studio.sh — install the free, offline production stack for Podcast Scout Studio.
# Safe to re-run: installs only what is missing.
#
#   bash setup_studio.sh            core: ffmpeg check, Python venv with Kokoro + Piper, male voices
#   bash setup_studio.sh --manim    also Manim Community Edition (maths/diagram scenes)
#   bash setup_studio.sh --check    report only
#
# Voices land in $STUDIO_VOICES_DIR (default ~/.cache/studio-voices). The venv lands in
# $STUDIO_VENV (default ~/.cache/studio-venv). Activate it before running narrate.py:
#   . ~/.cache/studio-venv/bin/activate
set -uo pipefail
VOICES="${STUDIO_VOICES_DIR:-$HOME/.cache/studio-voices}"
VENV="${STUDIO_VENV:-$HOME/.cache/studio-venv}"
want_manim=false; check_only=false
for a in "$@"; do case "$a" in --manim) want_manim=true;; --check) check_only=true;; esac; done
missing=0
ok()  { printf '  ok    %s\n' "$1"; }
bad() { printf '  MISS  %s\n' "$1"; missing=1; }
have(){ command -v "$1" >/dev/null 2>&1; }
fetch(){ # url dest
  [ -s "$2" ] && return 0
  curl -fsSL --retry 3 -o "$2.part" "$1" && mv "$2.part" "$2"
}

echo "studio setup"
have ffmpeg && have ffprobe && ok "$(ffmpeg -version | head -1 | cut -d' ' -f1-3)" || bad "ffmpeg/ffprobe (apt-get install ffmpeg | brew install ffmpeg)"
have node && ok "node $(node -v)" || bad "node 20+ (needed for HTML/Canvas scene rendering)"
have python3 && ok "$(python3 --version)" || { bad "python3"; exit 1; }

if [ ! -x "$VENV/bin/python" ]; then
  $check_only && bad "venv $VENV" || { python3 -m venv "$VENV" && ok "venv created $VENV"; }
fi
if [ -x "$VENV/bin/python" ]; then
  if "$VENV/bin/python" -c "import kokoro_onnx, soundfile, piper" 2>/dev/null; then ok "kokoro-onnx + piper-tts"
  elif $check_only; then bad "python TTS packages"
  else "$VENV/bin/pip" install -q --disable-pip-version-check kokoro-onnx soundfile piper-tts edge-tts jsonschema \
         && ok "installed kokoro-onnx, piper-tts, edge-tts" || bad "pip install failed (network?)"; fi
fi

if ! $check_only; then
  mkdir -p "$VOICES"
  echo "  ...   fetching male voices into $VOICES"
  K=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
  fetch "$K/kokoro-v1.0.onnx" "$VOICES/kokoro-v1.0.onnx" || bad "kokoro model download"
  fetch "$K/voices-v1.0.bin"  "$VOICES/voices-v1.0.bin"  || bad "kokoro voices download"
  PV=https://huggingface.co/rhasspy/piper-voices/resolve/main/en
  for v in en_US/ryan/high/en_US-ryan-high en_GB/alan/medium/en_GB-alan-medium; do
    n=$(basename "$v")
    fetch "$PV/$v.onnx" "$VOICES/$n.onnx" && fetch "$PV/$v.onnx.json" "$VOICES/$n.onnx.json" || bad "piper voice $n"
  done
fi
[ -s "$VOICES/kokoro-v1.0.onnx" ] && ok "kokoro male voices (am_michael default)" || bad "kokoro model files"
[ -s "$VOICES/en_US-ryan-high.onnx" ] && ok "piper en_US-ryan-high (male fallback)" || bad "piper ryan voice"

if $want_manim; then
  if "$VENV/bin/python" -c "import manim" 2>/dev/null; then ok "manim"
  elif $check_only; then bad "manim"
  else
    if have apt-get && [ "$(id -u)" = 0 ]; then
      apt-get install -y -qq libcairo2-dev libpango1.0-dev pkg-config texlive-latex-extra texlive-fonts-recommended dvisvgm >/dev/null 2>&1 \
        || echo "  note  apt could not install cairo/pango/LaTeX; MathTex scenes may fail"
    else
      echo "  note  install cairo + pango dev libs and LaTeX with your package manager for MathTex"
    fi
    "$VENV/bin/pip" install -q manim && ok "manim" || bad "manim (needs cairo/pango dev libs; LaTeX for MathTex)"
  fi
fi

# Parler-TTS: the expressive narration engine (default when present). Separate venv so its torch pins
# don't fight the studio venv. CPU wheels; torch and torchaudio must match (2.11 CPU tested).
PARLER_VENV="${PARLER_VENV:-$HOME/.cache/venv-parler}"
if ! $check_only && [ "${SKIP_PARLER:-0}" != 1 ]; then
  if [ ! -x "$PARLER_VENV/bin/python" ]; then python3 -m venv "$PARLER_VENV"; fi
  "$PARLER_VENV/bin/pip" install -q --upgrade pip >/dev/null 2>&1
  "$PARLER_VENV/bin/pip" install -q parler-tts soundfile >/dev/null 2>&1
  "$PARLER_VENV/bin/pip" install -q --force-reinstall --no-deps "torch==2.11.0+cpu" "torchaudio==2.11.0+cpu" \
      --index-url https://download.pytorch.org/whl/cpu >/dev/null 2>&1
  if "$PARLER_VENV/bin/python" -c "import parler_tts, torchaudio" >/dev/null 2>&1; then
    ok "parler-tts (expressive male narrator; first run downloads ~3.5 GB model)"
  else
    echo "  note  parler-tts not available: narration falls back to Kokoro"
  fi
fi

echo
export_line="export STUDIO_VOICES_DIR=\"$VOICES\" PARLER_PYTHON=\"$PARLER_VENV/bin/python\"; . \"$VENV/bin/activate\""
if [ "$missing" = 0 ]; then echo "studio ready. Before narrating run:"; echo "  $export_line"; else echo "NOT ready: fix the MISS lines above"; fi
exit "$missing"

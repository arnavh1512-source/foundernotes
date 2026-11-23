#!/usr/bin/env bash
# setup_studio.sh — install the free local production stack for Podcast Scout Studio.
# (edge-tts is installed too, but it is a Microsoft cloud service: narrate.py uses it only with --engine edge.)
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
sha256_of(){ if have sha256sum; then sha256sum "$1" | cut -d' ' -f1; else shasum -a 256 "$1" | cut -d' ' -f1; fi; }
fetch(){ # url dest [sha256]
  [ -s "$2" ] && return 0
  curl -fsSL --proto '=https' --retry 3 -o "$2.part" "$1" || return 1
  if [ -n "${3:-}" ] && [ "$(sha256_of "$2.part")" != "$3" ]; then
    echo "  FAIL  checksum mismatch for $(basename "$2"); download discarded" >&2; rm -f "$2.part"; return 1
  fi
  mv "$2.part" "$2"
}

echo "studio setup"
have ffmpeg && have ffprobe && ok "$(ffmpeg -version | head -1 | cut -d' ' -f1-3)" || bad "ffmpeg/ffprobe (apt-get install ffmpeg | brew install ffmpeg)"
have node && ok "node $(node -v)" || bad "node 20+ (needed for HTML/Canvas scene rendering)"
PY="$(command -v python3 || command -v python)"
[ -n "$PY" ] && ok "$("$PY" --version)" || { bad "python3"; exit 1; }
venv_bin(){ [ -d "$1/Scripts" ] && echo "$1/Scripts" || echo "$1/bin"; }   # Windows venvs use Scripts/
BIN="$(venv_bin "$VENV")"

if [ ! -x "$BIN/python" ] && [ ! -x "$BIN/python.exe" ]; then
  $check_only && bad "venv $VENV" || { "$PY" -m venv "$VENV" && ok "venv created $VENV"; BIN="$(venv_bin "$VENV")"; }
fi
if [ -x "$BIN/python" ] || [ -x "$BIN/python.exe" ]; then
  if "$BIN/python" -c "import kokoro_onnx, soundfile, piper" 2>/dev/null; then ok "kokoro-onnx + piper-tts"
  elif $check_only; then bad "python TTS packages"
  else "$BIN/python" -m pip install -q --disable-pip-version-check kokoro-onnx soundfile piper-tts edge-tts \
         && ok "installed kokoro-onnx, piper-tts, edge-tts" || bad "pip install failed (network?)"; fi
  # faster-whisper: the ASR round-trip behind narrate.py --asr --retake 2 (the documented default).
  if "$BIN/python" -c "import faster_whisper" 2>/dev/null; then ok "faster-whisper (narration ASR check)"
  elif $check_only; then bad "faster-whisper (narrate.py --asr)"
  else "$BIN/python" -m pip install -q --disable-pip-version-check faster-whisper "av<19" \
         && ok "installed faster-whisper" || bad "faster-whisper install failed (network?)"; fi
  # yt-dlp: subtitles/metadata for the scout's transcript step (see references/yt-dlp.md).
  # Left unpinned and upgraded on each run because YouTube changes break old releases.
  if "$BIN/python" -c "import yt_dlp" 2>/dev/null; then ok "yt-dlp $("$BIN/python" -m yt_dlp --version 2>/dev/null)"
  elif $check_only; then bad "yt-dlp (transcript fallback)"
  else "$BIN/python" -m pip install -q -U --disable-pip-version-check yt-dlp \
         && ok "installed yt-dlp $("$BIN/python" -m yt_dlp --version 2>/dev/null)" || bad "yt-dlp install failed (network?)"; fi
fi

if ! $check_only; then
  mkdir -p "$VOICES"
  echo "  ...   fetching male voices into $VOICES"
  K=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
  fetch "$K/kokoro-v1.0.onnx" "$VOICES/kokoro-v1.0.onnx" || bad "kokoro model download"
  fetch "$K/voices-v1.0.bin"  "$VOICES/voices-v1.0.bin"  || bad "kokoro voices download"
  # Pinned piper-voices revision (2026-11-22) and the voices' sha256 (Hugging Face LFS ids).
  PV=https://huggingface.co/rhasspy/piper-voices/resolve/e9c8a39444359388adaa94255becb37a5a2b8e51/en
  for spec in "en_US/ryan/high/en_US-ryan-high b3990d7606e183ec8dbfba70a4607074f162de1a0c412e0180d1ff60bb154eca" \
              "en_GB/alan/medium/en_GB-alan-medium 0a309668932205e762801f1efc2736cd4b0120329622adf62be09e56339d3330"; do
    v=${spec% *}; sum=${spec#* }; n=$(basename "$v")
    fetch "$PV/$v.onnx" "$VOICES/$n.onnx" "$sum" && fetch "$PV/$v.onnx.json" "$VOICES/$n.onnx.json" || bad "piper voice $n"
  done
fi
[ -s "$VOICES/kokoro-v1.0.onnx" ] && ok "kokoro male voices (am_michael default)" || bad "kokoro model files"
[ -s "$VOICES/en_US-ryan-high.onnx" ] && ok "piper en_US-ryan-high (male fallback)" || bad "piper ryan voice"

if $want_manim; then
  if "$BIN/python" -c "import manim" 2>/dev/null; then ok "manim"
  elif $check_only; then bad "manim"
  else
    if have apt-get && [ "$(id -u)" = 0 ]; then
      apt-get install -y -qq libcairo2-dev libpango1.0-dev pkg-config texlive-latex-extra texlive-fonts-recommended dvisvgm >/dev/null 2>&1 \
        || echo "  note  apt could not install cairo/pango/LaTeX; MathTex scenes may fail"
    else
      echo "  note  install cairo + pango dev libs and LaTeX with your package manager for MathTex"
    fi
    "$BIN/python" -m pip install -q manim && ok "manim" || bad "manim (needs cairo/pango dev libs; LaTeX for MathTex)"
  fi
fi

# Parler-TTS: the expressive narration engine (default when present). Separate venv so its torch pins
# don't fight the studio venv. CPU wheels; torch and torchaudio must match (2.11 CPU tested).
PARLER_VENV="${PARLER_VENV:-$HOME/.cache/venv-parler}"
if ! $check_only && [ "${SKIP_PARLER:-0}" != 1 ]; then
  PBIN="$(venv_bin "$PARLER_VENV")"
  if [ ! -x "$PBIN/python" ] && [ ! -x "$PBIN/python.exe" ]; then "$PY" -m venv "$PARLER_VENV"; PBIN="$(venv_bin "$PARLER_VENV")"; fi
  "$PBIN/python" -m pip install -q --upgrade pip >/dev/null 2>&1
  "$PBIN/python" -m pip install -q parler-tts soundfile >/dev/null 2>&1
  "$PBIN/python" -m pip install -q --force-reinstall --no-deps "torch==2.11.0+cpu" "torchaudio==2.11.0+cpu" \
      --index-url https://download.pytorch.org/whl/cpu >/dev/null 2>&1
  if "$PBIN/python" -c "import parler_tts, torchaudio" >/dev/null 2>&1; then
    ok "parler-tts (expressive male narrator; first run downloads ~3.5 GB model)"
  else
    echo "  note  parler-tts not available: narration falls back to Kokoro"
  fi
fi

echo
export_line="export STUDIO_VOICES_DIR=\"$VOICES\" PARLER_PYTHON=\"$(venv_bin "$PARLER_VENV")/python\"; . \"$(venv_bin "$VENV")/activate\""
if [ "$missing" = 0 ]; then echo "studio ready. Before narrating run:"; echo "  $export_line"; else echo "NOT ready: fix the MISS lines above"; fi
exit "$missing"

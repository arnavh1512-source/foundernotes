#!/usr/bin/env bash
# setup.sh — make sure this machine can render: Node, Playwright + Chromium, ffmpeg + ffprobe.
# Safe to run every time: it only installs what is missing. Needed in fresh cloud sessions,
# where the uploaded skill ships without node_modules or a browser.
#
#   bash setup.sh          check and install
#   bash setup.sh --check  check only, exit 1 if anything is missing
set -uo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
check_only=false; [ "${1:-}" = "--check" ] && check_only=true
missing=0

ok()   { printf '  ok    %s\n' "$1"; }
bad()  { printf '  MISS  %s\n' "$1"; missing=1; }
have() { command -v "$1" >/dev/null 2>&1; }
sudo_() { if [ "$(id -u 2>/dev/null || echo 0)" = 0 ]; then "$@"; elif have sudo; then sudo "$@"; else "$@"; fi; }

pw_found() { (cd "$here" && node -e 'require("playwright")' 2>/dev/null) || node -e 'require(require("child_process").execSync("npm root -g").toString().trim()+"/playwright")' 2>/dev/null; }
chromium_found() { (cd "$here" && node -e 'const {chromium}=require("playwright");require("fs").accessSync(chromium.executablePath())' 2>/dev/null) || [ -n "${MOTION_CHROMIUM:-}" ]; }

install_ffmpeg() {
  if have apt-get; then sudo_ apt-get update -qq && sudo_ apt-get install -y -qq ffmpeg
  elif have dnf; then sudo_ dnf install -y ffmpeg
  elif have apk; then sudo_ apk add --no-cache ffmpeg
  elif have brew; then brew install ffmpeg
  elif have winget; then winget install --silent --accept-source-agreements --accept-package-agreements Gyan.FFmpeg
  else return 1; fi
}

echo "motion setup ($here)"

if have node; then ok "node $(node -v)"; else bad "node — install Node 18+ first"; echo; exit 1; fi

if pw_found; then ok "playwright"
elif $check_only; then bad "playwright"
else echo "  ...   installing playwright"; (cd "$here" && npm i --no-audit --no-fund --silent playwright) && ok "playwright" || bad "playwright (npm i failed — no network?)"; fi

if chromium_found; then ok "chromium"
elif $check_only; then bad "chromium"
else
  echo "  ...   installing chromium"
  (cd "$here" && { npx --yes playwright install --with-deps chromium >/dev/null 2>&1 || npx --yes playwright install chromium; }) \
    && chromium_found && ok "chromium" || bad "chromium (set MOTION_CHROMIUM=/path/to/chrome to use an existing browser)"
fi

if have ffmpeg && have ffprobe; then ok "$(ffmpeg -version | head -1 | cut -d' ' -f1-3)"
elif $check_only; then bad "ffmpeg/ffprobe"
else
  echo "  ...   installing ffmpeg"
  install_ffmpeg >/dev/null 2>&1; hash -r
  if have ffmpeg && have ffprobe; then ok "ffmpeg"; else bad "ffmpeg/ffprobe — install it with the system package manager"; fi
fi

echo
[ "$missing" = 0 ] && echo "ready to render" || echo "NOT ready: fix the MISS lines above"
exit "$missing"

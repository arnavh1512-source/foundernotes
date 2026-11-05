#!/usr/bin/env bash
# install_obscura.sh — install the pinned, checksum-verified Obscura v0.2.6 research browser.
#   bash install_obscura.sh            → ~/studio-tools/obscura/obscura   (prints: export OBSCURA_BIN=...)
# Digests were read from the official release page on 2026-11-04 and cross-checked against the
# Windows digest already pinned in references/obscura.md. Never run an archive whose digest differs.
set -euo pipefail
VER=v0.2.6
DIR="${OBSCURA_DIR:-$HOME/studio-tools/obscura}"
case "$(uname -s)-$(uname -m)" in
  Linux-x86_64)  A=obscura-x86_64-linux.tar.gz;  SUM=eed986e478c5ec5439f531f2d7fb6b0e36a356f1df7a6c44a8e8fd4f2486bd76 ;;
  Linux-aarch64) A=obscura-aarch64-linux.tar.gz; SUM=e12aff8bbe40326386a471060083e9cec5255b67048996b84f649efef10cac39 ;;
  Darwin-arm64)  A=obscura-aarch64-macos.tar.gz; SUM=19faa248ac762f466ddb822dbb03ed4f097312d10d1a4d5b2143e6040a9bebd0 ;;
  Darwin-x86_64) A=obscura-x86_64-macos.tar.gz;  SUM=897f03df4e3d704f946c5e14c6a90a34e0d4e4ef898c4b3201771712962cd7fb ;;
  *) echo "unsupported platform $(uname -s)-$(uname -m); see references/obscura.md (Windows: PowerShell steps)"; exit 2 ;;
esac
mkdir -p "$DIR"; cd "$DIR"
if [ -x ./obscura ] && ./obscura --version 2>/dev/null | grep -q "0.2.6"; then echo "already installed"; else
  curl -fsSL --retry 3 -o "$A" "https://github.com/h4ckf0r0day/obscura/releases/download/$VER/$A"
  echo "$SUM  $A" | sha256sum -c - >/dev/null 2>&1 || echo "$SUM  $A" | shasum -a 256 -c - >/dev/null \
    || { echo "CHECKSUM MISMATCH for $A — not extracting"; rm -f "$A"; exit 1; }
  tar xzf "$A"; rm -f "$A"
fi
./obscura --version
echo "export OBSCURA_BIN=\"$DIR/obscura\""

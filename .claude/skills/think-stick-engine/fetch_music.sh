#!/bin/bash
# Download the CC0 music beds from OpenGameArt and verify checksums (kept out of git to keep the repo small).
set -e; D="$(cd "$(dirname "$0")" && pwd)/assets/music"; mkdir -p "$D"; cd "$D"
get(){ [ -f "$1" ] && echo "$3  $1" | sha256sum -c --quiet 2>/dev/null && return 0; curl -fsSL -m 180 -o "$1" "$2"; echo "$3  $1" | sha256sum -c --quiet || { echo "checksum mismatch: $1"; rm -f "$1"; exit 1; }; }
get vaporware.mp3     "https://opengameart.org/sites/default/files/003_Vaporware_2.mp3" 1697fa1b7ed6f3fe1eca4daa4f9d1a2eb3db8fe40a0f3c283529ab47e57b5b38
get contemplation.mp3 "https://opengameart.org/sites/default/files/Contemplation.mp3" 283962d3a975c93613c46cda30c9f0816176ae3e2899f961591a49e2d41b4bf3
get november.mp3      "https://opengameart.org/sites/default/files/155%20November_snow-33_tape_leveled.mp3" 7e4675f6fbc86b97603d620dc54b0753eb5fe773ccc2fab99bc863cb7afde32c
echo "CC0 music ready in $D"

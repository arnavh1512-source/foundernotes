#!/usr/bin/env bash
# check.sh — read what an encoded video really is, flag dead holds and black frames, and write a
# contact sheet of the encoded file next to it.
#
#   bash check.sh video.mp4                 print the spec
#   bash check.sh video.mp4 1080x1920 30    also assert size and frame rate (exit 1 on mismatch)
set -euo pipefail
v="${1:?usage: check.sh <video> [WxH] [fps]}"
want_res="${2:-}"
want_fps="${3:-}"

q() { ffprobe -v error -select_streams "$1" -show_entries "$2" -of csv=p=0 "$v" | head -1; }
w=$(q v:0 stream=width)
h=$(q v:0 stream=height)
codec=$(q v:0 stream=codec_name)
fps=$(awk -v r="$(q v:0 stream=r_frame_rate)" 'BEGIN { split(r, a, "/"); printf "%.4g", a[2] ? a[1] / a[2] : a[1] }')
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v")
audio=$(q a:0 stream=codec_name)
echo "$(basename "$v"): ${w}x${h} ${codec} ${fps} fps ${dur}s, audio: ${audio:-none}"

fail=0
if [ -n "$want_res" ] && [ "${w}x${h}" != "$want_res" ]; then echo "✗ size ${w}x${h}, wanted ${want_res}"; fail=1; fi
if [ -n "$want_fps" ] && ! awk -v a="$fps" -v b="$want_fps" 'BEGIN { exit !((a - b) ^ 2 < 0.01) }'; then
  echo "✗ ${fps} fps, wanted ${want_fps}"; fail=1
fi
case "$codec" in h264|prores) ;; *) echo "⚠ codec ${codec}: check the target platform plays it" ;; esac

echo "dead holds (nothing moves for 1.5s or more):"
ffmpeg -nostats -i "$v" -map 0:v:0 -vf "freezedetect=n=0.001:d=1.5" -f null - 2>&1 \
  | grep -oE 'freeze_(start|duration): [0-9.]+' | paste -d' ' - - | sed 's/^/  /' || echo "  none"

echo "black frames:"
ffmpeg -nostats -i "$v" -map 0:v:0 -vf "blackdetect=d=0.05:pix_th=0.05" -f null - 2>&1 \
  | grep -oE 'black_start:[0-9.]+ black_end:[0-9.]+' | sed 's/^/  /' || echo "  none"

sheet="${v%.*}-sheet.png"
ffmpeg -y -loglevel error -i "$v" -vf "fps=$(awk -v d="$dur" 'BEGIN { printf "%.5f", 12 / d }'),scale=-2:360,tile=6x2:padding=8:color=0x808080" \
  -frames:v 1 "$sheet"
echo "contact sheet (12 frames) → ${sheet}"
exit "$fail"

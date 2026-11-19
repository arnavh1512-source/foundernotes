#!/usr/bin/env bash
# Mix the stick exercise's original effects onto a silent render.
# Synthesises SOUND_EVENTS, compresses gently and two-pass normalises to the
# benchmark level (Alan Becker AvA measured about -16.5 LUFS), then muxes.
# Usage: stick-mix.sh silent.mp4 out.mp4
set -euo pipefail
in=$1; out=$2
here=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
node -e "import('$here/../assets/stick-performance.mjs').then(m=>console.log(JSON.stringify(m.SOUND_EVENTS)))" > "$tmp/events.json"
python3 "$here/stick-sfx.py" "$tmp/events.json" "$tmp/sfx.wav" >/dev/null
ffmpeg -v error -y -i "$tmp/sfx.wav" -af "acompressor=threshold=-30dB:ratio=3:attack=5:release=120:makeup=8dB" "$tmp/comp.wav"
m=$(ffmpeg -nostats -i "$tmp/comp.wav" -af loudnorm=I=-16.5:TP=-1.5:LRA=14:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
f=$(python3 -c "import json,sys;d=json.loads(sys.argv[1]);print(f\"loudnorm=I=-16.5:TP=-1.5:LRA=14:measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true\")" "$m")
ffmpeg -v error -y -i "$in" -i "$tmp/comp.wav" -filter_complex "[1]$f,aresample=48000[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest "$out"
echo "$out"

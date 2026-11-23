#!/bin/bash
set -e; cd "$(dirname "$0")"; R=$(git rev-parse --show-toplevel); S=$R/.claude/skills/podcast-scout-skill/scripts; P=$(python3 -c "import os;print(os.path.relpath(os.getcwd(),'$R'))"); . ~/.cache/studio-venv/bin/activate
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 mix/narration-bright.wav)
N=${CHUNKS:-6}; rm -f scenes/part*.mp4 film/part*.html
for i in $(seq 0 $((N-1))); do
  A=$(python3 -c "print(round($DUR*$i/$N*30)/30)"); B=$(python3 -c "print(round($DUR*($i+1)/$N*30)/30 if $i<$N-1 else $DUR)")
  sed "s#const T0=+(Q.get('from')||0), T1=+(Q.get('to')||window.DUR);#const T0=$A, T1=$B;#" film/stick.html > film/part$i.html
  (cd $R && node .claude/skills/motion/scripts/render.mjs $P/film/part$i.html --out $P/scenes/part$i.mp4 > $P/scenes/part$i.log 2>&1) &
done
wait; ls scenes/part*.mp4
python3 $S/assemble.py --scenes $(ls scenes/part*.mp4 | sort) --narration mix/narration-bright.wav --music mix/bed.wav --music-db -14 --captions mix/captions.srt --sub-font "Instrument Sans" --sub-fonts-dir film/fonts --out final/video.mp4
python3 $S/qc_video.py final/video.mp4 --timings mix/timings.json --captions mix/captions.srt --sheet final/sheet.jpg --json final/qc.json || true
ffmpeg -loglevel error -y -i final/video.mp4 -vf scale=1280:-2 -c:v libx264 -crf 24 -preset veryfast -c:a aac -b:a 128k final/video-720p.mp4
echo BUILD_DONE

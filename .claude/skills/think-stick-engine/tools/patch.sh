#!/bin/bash
set -e; cd "$(dirname "$0")"; R=$(git rev-parse --show-toplevel); S=$R/.claude/skills/podcast-scout-skill/scripts; . ~/.cache/studio-venv/bin/activate
rm -rf splice; python3 patch_splice.py
python3 $S/assemble.py --scenes $(cat splice/list.txt) --narration mix/narration-bright.wav --music mix/bed.wav --music-db -14 --captions mix/captions.srt --sub-font "Instrument Sans" --sub-fonts-dir film/fonts --out final/video.mp4
python3 $S/qc_video.py final/video.mp4 --timings mix/timings.json --captions mix/captions.srt --json final/qc.json || true
ffmpeg -loglevel error -y -i final/video.mp4 -vf scale=1280:-2 -c:v libx264 -crf 24 -preset veryfast -c:a aac -b:a 128k final/video-720p.mp4
echo PATCH_DONE

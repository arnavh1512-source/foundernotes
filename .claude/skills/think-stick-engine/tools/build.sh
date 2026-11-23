#!/bin/bash
# Think! stick engine build: merge narrator (Voicebox) + character lines (ElevenLabs) in order.json -> timings -> sfx/music -> parallel render -> assemble -> QC.
# Run from the episode folder (studio-output/<slug>/full) after new_episode.sh. Expects order.json, narration/, dialogue/, film/shots.js.
set -e
cd "$(dirname "$0")"; R=$(git rev-parse --show-toplevel); S=$R/.claude/skills/podcast-scout-skill/scripts; P=$(python3 -c "import os;print(os.path.relpath(os.getcwd(),'$R'))")
. ~/.cache/studio-venv/bin/activate
rm -rf mix; mkdir -p mix/files scenes final
python3 - <<'P'
import json,subprocess
order=json.load(open('order.json'))
for i in order:
    src=f'narration/segments/{i}.wav'; af="highpass=f=80,equalizer=f=220:t=q:w=1:g=-2,highshelf=f=5000:g=9,loudnorm=I=-20:TP=-2:LRA=7"
    import os
    if not os.path.exists(src) or '_' in i: src=f'dialogue/elevenlabs-raw/{i}.wav'; af="loudnorm=I=-20:TP=-2:LRA=7"
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',src,'-af',af,'-ar','48000','-ac','1',f'mix/files/{i}.wav'],check=True)
n={s['id']:s for s in json.load(open('narration/script.json'))['segments']}; d={s['id']:s for s in json.load(open('dialogue/script.json'))['segments']}
segs=[{'id':i,'text':(n.get(i) or d[i])['text'],'pause_after':min((n.get(i) or d[i]).get('pause_after',.5),.6)} for i in order]
json.dump({'voice':{'engine':'files','speed':1.0,'chain':'none'},'lead':0.3,'tail':1.0,'segments':segs},open('mix/script.json','w'),indent=1)
P
python3 $S/narrate.py mix/script.json --out mix --engine files --files-dir mix/files | tail -1
python3 - <<'P'
import json
j=json.load(open('mix/timings.json')); t={s['id']:[s['start'],s['end']] for s in j['segments']}
import os
if os.path.exists('groups.json'):  # scenes keyed by original segment ids, each spanning its split lines
    groups=json.load(open('groups.json')); seg={g:[t[groups[g][0]][0],t[groups[g][-1]][1]] for g in json.load(open('scene_order.json'))}
else: seg={i:t[i] for i in json.load(open('order.json'))}
open('film/timing.js','w').write('window.SEG='+json.dumps(seg)+'; window.DUR='+str(j['duration'])+';');print('duration',j['duration'])
P
python3 turns.py
python3 emph.py
ffmpeg -loglevel error -y -i mix/narration.wav -af "volume=-3dB,apad=pad_dur=3.6" mix/narration-bright.wav
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 mix/narration-bright.wav); sed -i "s/window.DUR=[0-9.]*;/window.DUR=$DUR;/" film/timing.js; echo "padded duration $DUR"
(cd film && python3 sfx.py ../mix/sfx.wav)
python3 music_cc0.py mix/music.wav
ffmpeg -loglevel error -y -i mix/music.wav -i mix/sfx.wav -filter_complex "[0]volume=-11dB[m];[1]volume=-1dB[s];[m][s]amix=inputs=2:normalize=0" mix/bed.wav
N=${CHUNKS:-6}; rm -f scenes/part*.mp4 film/part*.html
for i in $(seq 0 $((N-1))); do
  A=$(python3 -c "print(round($DUR*$i/$N*30)/30)"); B=$(python3 -c "print(round($DUR*($i+1)/$N*30)/30 if $i<$N-1 else $DUR)")
  sed "s#const T0=+(Q.get('from')||0), T1=+(Q.get('to')||window.DUR);#const T0=$A, T1=$B;#" film/stick.html > film/part$i.html
  (cd $R && node .claude/skills/motion/scripts/render.mjs $P/film/part$i.html --out $P/scenes/part$i.mp4 > $P/scenes/part$i.log 2>&1) &
done
wait; ls scenes/part*.mp4
python3 $S/assemble.py --scenes $(ls scenes/part*.mp4 | sort) --narration mix/narration-bright.wav --music mix/bed.wav --music-db -14 --captions mix/captions.srt --sub-font "Instrument Sans" --sub-fonts-dir film/fonts --out final/video.mp4
python3 $S/qc_video.py final/video.mp4 --timings mix/timings.json --captions mix/captions.srt --sheet final/sheet.jpg --json final/qc.json || true

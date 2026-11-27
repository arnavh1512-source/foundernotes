#!/bin/bash
# Mandatory before any full render: grab a frame every STEP seconds (default 3) from film/stick.html and build
# labelled contact sheets in precheck/ to review for missing, clipped or overlapping elements.
# Grabs run in small batches so one browser crash cannot blank the check; a black frame is reported, not ignored.
set -e; cd "$(dirname "$0")"; STEP=${STEP:-3}; D=precheck; rm -rf $D; mkdir -p $D
DUR=$(python3 -c "import re;print(re.search(r'DUR=([\d.]+)',open('film/timing.js').read()).group(1))")
python3 -c "import math;d=$DUR;s=$STEP;print('\n'.join(f'{s/2+i*s:.1f}' for i in range(int(d//s))))" | xargs -n 10 > $D/batches.txt
while read -r line; do node grab.mjs "$PWD/film/stick.html" "$PWD/$D" $line > /dev/null 2>&1 || true; done < $D/batches.txt
python3 - "$D" <<'P'
import os,sys,subprocess
from PIL import Image
d=sys.argv[1]; fs=sorted(f for f in os.listdir(d) if f.startswith('t') and f.endswith('.png'))
bad=[f for f in fs if Image.open(os.path.join(d,f)).convert('L').resize((64,36)).getextrema()[1]<10]
print(len(fs),'frames grabbed;', 'BLACK (re-grab or investigate):'+' '.join(bad) if bad else 'none black')
for k in range(0,len(fs),24):
    grp=fs[k:k+24]; ins=sum([['-i',os.path.join(d,f)] for f in grp],[]); n=len(grp)
    fc=''.join(f"[{i}]scale=320:-1,drawtext=text='{grp[i][1:-4]}':x=4:y=4:fontsize=18:fontcolor=red:box=1:boxcolor=white@0.7[s{i}];" for i in range(n))
    fc+=''.join(f"color=c=white:s=320x180[s{i}];" for i in range(n,24))
    fc+=''.join(''.join(f"[s{r*6+c}]" for c in range(6))+f"hstack=6[r{r}];" for r in range(4))+"[r0][r1][r2][r3]vstack=4"
    subprocess.run(['ffmpeg','-loglevel','error','-y',*ins,'-filter_complex',fc,'-frames:v','1',os.path.join(d,f'sheet_{k//24:02d}.png')],check=True)
print('review every sheet in',d)
P

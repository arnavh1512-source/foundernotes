"""Re-render only changed shots and splice them into the rendered parts. Writes splice/list.txt of clips in order."""
import json, subprocess, os, sys
from concurrent.futures import ThreadPoolExecutor
R=os.popen('git rev-parse --show-toplevel').read().strip(); P=os.path.relpath(os.getcwd(),R); FPS=30
cfg=json.load(open('patch_ranges.json')); DUR=cfg['dur']; N=6
bounds=[round(round(DUR*i/N*FPS)/FPS*FPS) for i in range(N)]+[None]
nfr=[int(subprocess.check_output(['ffprobe','-v','error','-count_packets','-select_streams','v','-show_entries','stream=nb_read_packets','-of','csv=p=0',f'scenes/part{i}.mp4']).decode()) for i in range(N)]
bounds[N]=bounds[N-1]+nfr[N-1]
rngs=sorted([(round(a*FPS),round(b*FPS)) for a,b,_ in cfg['ranges']])
os.makedirs('splice',exist_ok=True); html=open('film/stick.html').read(); jobs=[]; pieces=[]
def enc(src,s,e,out): subprocess.run(['ffmpeg','-loglevel','error','-y','-i',src,'-vf',f"trim=start_frame={s}:end_frame={e},setpts=PTS-STARTPTS,scale=iw:ih:out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv",'-an','-c:v','libx264','-crf','16','-preset','medium','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-r','30',out],check=True)
def rnd(a,b,out):
    h=f'film/patch_{a}.html'; open(h,'w').write(html.replace("const T0=+(Q.get('from')||0), T1=+(Q.get('to')||window.DUR);",f"const T0={a/FPS}, T1={b/FPS};"))
    subprocess.run(['node','.claude/skills/motion/scripts/render.mjs',f'{P}/{h}','--out',f'{P}/{out}'],cwd=R,check=True,stdout=subprocess.DEVNULL)
cur=0; k=0
for a,b in rngs+[(bounds[N],bounds[N])]:
    # original frames cur..a, split on part boundaries
    for i in range(N):
        s,e=max(cur,bounds[i]),min(a,bounds[i+1])
        if e>s: out=f'splice/{k:03d}_orig.mp4'; jobs.append(('enc',f'scenes/part{i}.mp4',s-bounds[i],e-bounds[i],out)); pieces.append(out); k+=1
    if b>a: out=f'splice/{k:03d}_patch.mp4'; jobs.append(('rnd',a,b,out)); pieces.append(out); k+=1
    cur=b
with ThreadPoolExecutor(6) as ex:
    list(ex.map(lambda j: enc(*j[1:]) if j[0]=='enc' else rnd(*j[1:]), jobs))
tot=sum(int(subprocess.check_output(['ffprobe','-v','error','-count_packets','-select_streams','v','-show_entries','stream=nb_read_packets','-of','csv=p=0',p]).decode()) for p in pieces)
print('pieces',len(pieces),'frames',tot,'expected',bounds[N]); assert tot==bounds[N], 'frame count mismatch'
open('splice/list.txt','w').write('\n'.join(pieces)+'\n')

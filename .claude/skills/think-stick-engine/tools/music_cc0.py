"""Music bed from CC0 tracks: piano (opening), contemplation (middle), lo-fi (second half + tips), 3 s crossfades, level-matched."""
import json,re,subprocess,sys
import os
ROOT=subprocess.run(['git','rev-parse','--show-toplevel'],capture_output=True,text=True).stdout.strip()
A=os.environ.get('THINK_MUSIC',os.path.join(ROOT,'.claude/skills/think-stick-engine/assets/music'))+'/'
tj=open('film/timing.js').read(); DUR=float(re.search(r'DUR=([\d.]+)',tj).group(1))
# music.json (optional): [["file.mp3", start_s, end_s], ...]; default: piano / contemplation / lo-fi in thirds
SEC=json.load(open('music.json')) if os.path.exists('music.json') else [('vaporware.mp3',0,DUR/3),('contemplation.mp3',DUR/3,2*DUR/3),('november.mp3',2*DUR/3,DUR)]
SEC[-1]=(SEC[-1][0],SEC[-1][1],DUR); X=3.0; parts=[]
for i,(f,a,b) in enumerate(SEC):
    L=(b-a)+(X if i<len(SEC)-1 else 0)
    subprocess.run(['ffmpeg','-v','error','-y','-stream_loop','-1','-i',A+f,'-t',f'{L:.2f}','-ac','2','-ar','48000','-af','loudnorm=I=-20:TP=-3:LRA=11',f'mix/m{i}.wav'],check=True); parts.append(f'mix/m{i}.wav')
chain=''; prev='[0]'
for i in range(1,len(parts)): chain+=f'{prev}[{i}]acrossfade=d=3:c1=tri:c2=tri[x{i}];'; prev=f'[x{i}]'
fc=chain+f'{prev}afade=t=in:d=1.5,afade=t=out:st={DUR-4:.2f}:d=4[o]'
subprocess.run(['ffmpeg','-v','error','-y']+sum([['-i',p] for p in parts],[])+['-filter_complex',fc,'-map','[o]','-t',f'{DUR:.2f}',sys.argv[1]],check=True)
print('cc0 music bed',DUR,'s ->',sys.argv[1])

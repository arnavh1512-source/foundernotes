"""Stressed beats per character line from the voice track (RMS peaks with min spacing), appended to film/turns.js as window.EMPH."""
import json,re,wave,numpy as np
w=wave.open('mix/narration.wav'); sr=w.getframerate(); n=w.getnframes(); ch=w.getnchannels()
a=np.frombuffer(w.readframes(n),dtype='<i2').astype(np.float32); a=a.reshape(-1,ch).mean(1) if ch>1 else a
hop=sr//100; fr=len(a)//hop; env=np.convolve(np.sqrt((a[:fr*hop].reshape(fr,hop)**2).mean(1)+1e-9),np.ones(9)/9,'same')
s=open('film/turns.js').read(); SP=json.loads(re.search(r'SPEAK=(\[.*?\]);',s).group(1)); E={}
for st,en,r in SP:
    seg=env[int(st*100):int(en*100)]
    if len(seg)<30: E[f'{st:.3f}']=[st+.05]; continue
    thr=np.percentile(seg,60); gap={'youth':90,'mother':110}.get(r,130)
    pk=sorted([i for i in range(3,len(seg)-3) if seg[i]>=seg[i-3:i+4].max() and seg[i]>thr],key=lambda i:-seg[i]); keep=[]
    for i in pk:
        if all(abs(i-j)>=gap for j in keep): keep.append(i)
    E[f'{st:.3f}']=[round(st+i/100,2) for i in sorted(keep)]
open('film/turns.js','a').write('window.EMPH='+json.dumps(E)+';'); print(sum(map(len,E.values())),'stressed beats')

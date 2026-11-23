"""Synthesised SFX for the stick pilot (NumPy only). Reads shots.js cues and timing.js."""
import json, re, sys, numpy as np, wave
SR=48000; tj=open('timing.js').read(); SEG=json.loads(re.search(r'window\.SEG=(\{.*?\});',tj).group(1)); DUR=float(re.search(r'window\.DUR=([\d.]+)',tj).group(1))
SH=json.loads(open('shots.js').read().split('=',1)[1].rstrip().rstrip(';'))
ids=list(SEG); span={k:[(SEG[k][0] if i else 0),(SEG[ids[i+1]][0] if i<len(ids)-1 else DUR)] for i,k in enumerate(ids)}
rng=np.random.default_rng(7); t=lambda d:np.arange(int(SR*d))/SR
def env(n,a=.004,d=.2): x=np.arange(n)/SR; return np.minimum(1,x/a)*np.exp(-x/d)
def thunk(): x=t(.45); f=np.linspace(95,48,len(x)); return .9*np.sin(2*np.pi*np.cumsum(f)/SR)*env(len(x),.002,.12)+.25*rng.standard_normal(len(x))*env(len(x),.001,.025)
def whoosh(): n=int(SR*.5); w=rng.standard_normal(n); k=np.convolve(w,np.ones(40)/40,'same'); e=np.sin(np.linspace(0,np.pi,n))**2; return .5*k*e*4
def pop(): x=t(.14); return .45*np.sin(2*np.pi*560*x)*env(len(x),.002,.035)
def ding(): x=t(.9); return .3*(np.sin(2*np.pi*1320*x)+.4*np.sin(2*np.pi*1980*x))*env(len(x),.003,.28)
def ting(): x=t(.6); return .22*np.sin(2*np.pi*1760*x)*env(len(x),.002,.18)
import glob, os
import subprocess as _sp
_A=os.environ.get('THINK_SFX') or os.path.join(_sp.run(['git','rev-parse','--show-toplevel'],capture_output=True,text=True,cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip(),'.claude/skills/think-stick-engine/assets/sfx')
def _load(f):
    with wave.open(f) as w: y=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float32)/32768
    return y/max(1e-6,np.abs(y).max())
GAIN={'thunk':.8,'whoosh':.45,'pop':.4,'ding':.3,'ting':.25}
SAMP={k:[_load(f) for f in sorted(glob.glob(os.path.join(_A,k+'*.wav')))] for k in GAIN}
_ctr={k:0 for k in GAIN}
def _pick(k):  # rotate through the CC0 variants so repeated actions never sound identical
    L=SAMP[k]; i=_ctr[k]; _ctr[k]+=1; return GAIN[k]*L[(i*7)%len(L)]
BANK={k:(lambda k=k:_pick(k)) if SAMP[k] else f for k,f in {'thunk':thunk,'whoosh':whoosh,'pop':pop,'ding':ding,'ting':ting}.items()}
out=np.zeros(int(SR*(DUR+1))); n=0
for s in SH:
    a,b=span[s['seg']]; t0=a+(b-a)*s['a']; t1=a+(b-a)*s['b']
    for u,name in s['sfx']:
        y=BANK[name](); i=int((t0+(t1-t0)*u)*SR); out[i:i+len(y)]+=y[:len(out)-i]; n+=1
out=out[:int(SR*DUR)]; out/=max(1,np.abs(out).max()/0.9)
with wave.open(sys.argv[1],'wb') as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype('<i2').tobytes())
print(n,'cues ->',sys.argv[1])

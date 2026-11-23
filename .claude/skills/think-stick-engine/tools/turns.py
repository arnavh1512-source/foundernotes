import json
t={s['id']:s['start'] for s in json.load(open('mix/timings.json'))['segments']}
T=sorted(t[i] for ids in json.load(open('groups.json')).values() if len(ids)>1 for i in ids[1:])
open('film/turns.js','w').write('window.TURNS='+json.dumps(T)+';'); print(len(T),'turns')
d={s['id']:s['speaker'] for s in json.load(open('dialogue/script.json'))['segments']}
SP=[[s['start'],s['end'],d[s['id']]] for s in json.load(open('mix/timings.json'))['segments'] if s['id'] in d]
open('film/turns.js','a').write('window.SPEAK='+json.dumps(SP)+';'); print(len(SP),'spoken character lines')

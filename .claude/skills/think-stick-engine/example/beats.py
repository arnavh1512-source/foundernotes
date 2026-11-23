"""Split long shots into character-led beats. Reads film/shots-orig.js + timings, writes film/shots.js."""
import json, re
R='#d8342b'; GRN='#2f6f4f'; INKC='#1c1c1f'
seg=json.loads(re.search(r'SEG=(\{.*?\});',open('film/timing.js').read()).group(1)); DUR=float(re.search(r'DUR=([\d.]+)',open('film/timing.js').read()).group(1))
order=list(seg); span={k:[seg[k][0] if i else 0, seg[order[i+1]][0] if i<len(order)-1 else DUR] for i,k in enumerate(order)}
T={s['id']:(s['start'],s['end']) for s in json.load(open('mix/timings.json'))['segments']}
shots=json.loads(open('film/shots-orig.js').read().split('=',1)[1].rstrip().rstrip(';'))
D=lambda **a:a
B={
 ('n02','phone'):[('phone',0),('keys','n02e',D(w=['CALM','POLITE'],act='point',who='mom'))],
 ('n03','hangup'):[('hangup',0),('keys',.6,D(w=['OUT OF CONTROL?','A TOOL?'],act='slam'))],
 ('n04','study2'):[('study2',0),('duo',.5,D(mode='wide',act='point'))],
 ('n05','loop'):[('loop',0),('keys',.5,D(w=['NOT STUCK','CHOOSING'],act='stack'))],
 ('d01','coffeeAgain'):[('coffeeAgain',0),('duo',.55,D(mode='yo',act='headgrab'))],
 ('n06','whereGoal'):[('whereGoal',0),('duo','n06b_y',D(mode='wide',act='pace')),('duo',('n06b_y',.55),D(mode='yo',act='shrug'))],
 ('n07','blameAll'):[('blameAll',0),('duo',.45,D(mode='ph',pact='raise'))],
 ('n07','toolbox'):[('toolbox',0),('duo',.5,D(mode='wide',act='cross',pact='lean'))],
 ('n08','split'):[('keys',0,D(w=['FABRICATED','REAL ANGER'],act='slam',who='ph')),('duo',('n08a_p',.55),D(mode='ph',pact='raise')),('split','n08b'),('keys',('n08b',.62),D(w=['FASTER?'],act='kick'))],
 ('n09','momRecap'):[('momRecap',0),('angerSwitch','n09b_p'),('duo',('n09b_p',.62),D(mode='ph',pact='open')),('keys',('n09b_p',.8),D(w=['TAKE OUT','PUT AWAY'],act='point',who='ph'))],
 ('n10','ask'):[('ask',0),('goalBubble',.33),('keys',.78,D(w=['A BETTER WAY'],act='push'))],
 ('d05','accuse'):[('accuse',0),('duo',.5,D(mode='yo',act='point'))],
 ('n11','feelings'):[('feelings',0),('coldMachine','n11b_y'),('duo',('n11b_y',.55),D(mode='yo',act='point'))],
 ('d06','philCalm'):[('philCalm',0),('duo',.55,D(mode='wide',pact='open',act='cross'))],
 ('n12','gearsPuppet'):[('duo',0,D(mode='ph',pact='lean')),('dominoRun','n12b_p'),('gearsPuppet',('n12b_p',.42)),('duo',('n12b_p',.78),D(mode='wide',act='stepback',pact='raise'))],
 ('n13','lookStudy'):[('lookStudy',0),('keys',.28,D(w=['BOOKS','PEN','MANUSCRIPT'],act='point')),('duo',.55,D(mode='yo',act='headgrab')),('duo',.8,D(mode='wide',act='pace'))],
 ('n14','wellBoth'):[('duo',0,D(mode='ph',pact='raise')),('wellSeasons','n14b_p'),('wellBoth',('n14b_p',.8))],
 ('n15','divorce'):[('divorce',0),('meaningDial',.38),('duo','n15b',D(mode='yo',act='point'))],
 ('n16','timeMachine'):[('timeMachine',0),('keys',.5,D(w=['STUCK','PESSIMISM','GIVING UP'],act='slam',who='ph'))],
 ('n16','roadAhead'):[('wallRoad',0),('roadAhead',.72)],
 ('n17','subscribe'):[('subscribe',0),('duo',.78,D(mode='wide',act='point'))],
 ('n18','ysun'):[('ysun',0),('copyY',.45),('duo','n18b_y',D(mode='yo',act='point'))],
 ('n19','agora'):[('duo',0,D(mode='ph',pact='raise')),('agoraWalk','n19b'),('agora',('n19b',.6))],
 ('n19','cafeVienna'):[('cafeVienna',0),('duo','n19d',D(mode='wide',act='cross'))],
 ('n20','bookpile'):[('bookpile',0),('bookAvalanche','n20b_p'),('keys','n20c',D(w=['READING ≠ CHANGING'],act='kick'))],
 ('n21','mirror'):[('mirror',0),('mirrorY','n21b_p'),('duo',('n21b_p',.62),D(mode='yo',act='headgrab'))],
 ('n22','likeSelf'):[('likeSelf',0),('handPoll','n22b_p'),('duo','n22c_y',D(mode='yo',act='point')),('likeSelf','n22d_p')],
 ('n23','footsteps'):[('duo',0,D(mode='ph',pact='open')),('footsteps',('n23b_p',.3)),('stairsUp',('n23b_p',.65)),('duo','n23c',D(mode='wide',pact='raise',act='cross'))],
 ('n24','equipment'):[('equipment',0),('keys',.55,D(w=['WHAT YOU HAVE'],act='stack'))],
 ('d13','fairness'):[('fairness',0),('duo',.5,D(mode='yo',act='slam'))],
 ('n25','renewal'):[('duo',0,D(mode='ph',pact='calm')),('renewal','n25b_p'),('repaint',('n25b_p',.5)),('duo','n25c',D(mode='wide',pact='lean',act='stepback'))],
 ('n26','greek'):[('greek',0),('greekGood','n26b_p'),('greek','n26c'),('keys',('n26c',.5),D(w=['GOOD','BENEFICIAL'],act='slam',col=[INKC,GRN]))],
 ('n27','cage'):[('cage',0),('duo',('n27a_p',.55),D(mode='ph',pact='open')),('duo','n27b_y',D(mode='yo',act='shrug'))],
 ('n27','glare'):[('glare',0),('duo',('n27d',.5),D(mode='wide',act='slam'))],
 ('n28','ifonly2'):[('ifonly2',0),('keys',.55,D(w=['IF ONLY'],act='slam',col=[R]))],
 ('n29','lifestyleDef'):[('duo',0,D(mode='ph',pact='raise')),('lifestyleDef',.25),('glassesTint',.6)],
 ('n30','relabel'):[('duo',0,D(mode='wide',pact='lean',act='cross')),('relabel','n30b_p'),('keys','n30c',D(w=['FIXED?','A VIEW'],act='kick'))],
 ('n31','age10'):[('duo',0,D(mode='ph',pact='lean')),('age10','n31b_p'),('kidCross',('n31b_p',.35)),('keys',('n31b_p',.8),D(w=['CHOSEN','CHOOSE AGAIN'],act='stack',who='ph'))],
 ('n32','decide'):[('decide',0),('duo',('n32a_p',.5),D(mode='ph',pact='raise')),('duo','n32b',D(mode='wide',act='slam'))],
 ('n33','twoCars'):[('twoCars',0),('carDrive',('n33b_p',.2)),('twoCars',('n33b_p',.6)),('duo',('n33b_p',.85),D(mode='yo',act='cross'))],
 ('n34','twoDoors'):[('twoDoors',0),('keys',.6,D(w=['ANXIETY','DISAPPOINTMENT'],act='point',who='ph'))],
 ('n34','courage'):[('courage',0),('duo','n34c_p',D(mode='ph',pact='lean'))],
 ('n35','ifonlyList'):[('duo',0,D(mode='wide',act='shrug')),('ifonlyList','n35b_p'),('ifOnlyFlood',('n35b_p',.55))],
 ('n36','novelist'):[('novelist',0),('novelistClock',.45)],
 ('n37','drawerLock'):[('judged',0),('drawerLock',.5)],
 ('n37','excuses'):[('excuses',0),('keys',.55,D(w=['NOT YOUNG','FAMILY'],act='slam'))],
 ('d19','phtalk'):[('phtalk',0),('duo',.5,D(mode='wide',pact='open',act='stand'))],
 ('n38','selfComplicates'):[('keys',0,D(w=['SIMPLE TASK'],act='push')),('selfComplicates',.45)],
 ('n39','choiceBack'):[('choiceBack',0),('forkRoad',.3),('duo','n39b_p',D(mode='ph',pact='raise')),('keys',('n39b_p',.5),D(w=['LIFESTYLE','BEHAVIOUR'],act='stack',who='ph'))],
 ('n40','hereNow'):[('duo',0,D(mode='ph',pact='calm')),('spotNow',('n40a_p',.35)),('hereNow','n40b'),('keys',('n40b',.74),D(w=['DECIDED','HERE & NOW'],act='stack'))],
 ('n41','tip1'):[('tip1',0),('goalBubble',.5)],
 ('n43','headBurst'):[('headBurst',0),('duo',('n43b_y',.25),D(mode='yo',act='headgrab')),('duo',('n43b_y',.6),D(mode='yo',act='stepback'))],
}
SFX={'angerSwitch':[[.35,'pop'],[.72,'pop']],'dominoRun':[[.25,'pop'],[.42,'pop'],[.58,'pop'],[.74,'thunk']],'wellSeasons':[[.5,'whoosh']],'wallRoad':[[.22,'thunk'],[.5,'ding']],
 'bookAvalanche':[[.66,'thunk']],'copyY':[[.6,'thunk']],'glassesTint':[[.4,'ting'],[.74,'ting']],'spotNow':[[.08,'whoosh']],'judged':[[.42,'pop'],[.55,'pop'],[.68,'pop']],
 'goalBubble':[[.3,'pop'],[.45,'pop'],[.6,'pop']],'greekGood':[[.52,'whoosh']],'kidCross':[[.68,'whoosh']],'mirrorY':[[.72,'ting']],'coldMachine':[[.2,'whoosh']],'repaint':[[.1,'whoosh']]}
def sfx_for(n,a):
    if n=='keys':
        k=len(a['w']); act=a['act']
        if act=='slam': return [[(i+.4)/(k+.6)+.06,'thunk'] for i in range(k)]
        if act=='kick': return [[.45,'whoosh'],[.5,'thunk']]
        if act=='point': return [[(i+.25)/(k+.3),'whoosh'] for i in range(k)]
        if act=='stack': return [[(i+.3)/(k+.4),'whoosh'] for i in range(k)]
        return []
    if n=='duo': return {'slam':[[.42,'thunk']],'stepback':[[.12,'whoosh']],'point':[[.15,'whoosh']]}.get(a.get('act'),[])
    return SFX.get(n)
out=[]; used=set()
for s in shots:
    key=(s['seg'],s['n'])
    if key not in B: out.append(s); continue
    used.add(key); a0,b0=span[s['seg']]; t0=a0+(b0-a0)*s['a']; t1=a0+(b0-a0)*s['b']
    starts=[]
    for b in B[key]:
        st=b[1]
        T0=t0 if st==0 else (T[st][0] if isinstance(st,str) else (T[st[0]][0]+st[1]*(T[st[0]][1]-T[st[0]][0]) if isinstance(st,tuple) else t0+st*(t1-t0)))
        starts.append(T0)
    starts[0]=t0
    for i,b in enumerate(B[key]):
        e=starts[i+1] if i+1<len(starts) else t1
        assert e-starts[i]>=1.4, (key,b[0],round(e-starts[i],2))
        n=b[0]; args=b[2] if len(b)>2 else None
        sh={'seg':s['seg'],'a':round((starts[i]-a0)/(b0-a0),5),'b':round((e-a0)/(b0-a0),5),'n':n}
        if n==s['n']: sh['sfx']=s['sfx']
        else: sh['sfx']=sfx_for(n,args) or []
        if args: sh['args']=args
        out.append(sh)
assert used==set(B), set(B)-used
open('film/shots.js','w').write('window.SHOTS2='+json.dumps(out)+';')
print(len(shots),'->',len(out),'shots')

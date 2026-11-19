// Original whole-body exercise. Reuses the existing FounderNotes motion geometry.
// Draft: pure geometry checked; browser rendering and audiovisual review still required.
import {progress, solveArm, layerMatrix} from './story-motion.mjs';
export const DURATION = 14.5;
export const HEAD_R = 62, LINE = 20; // master study: Alan's head is ~1/3 of height; step toward it
const keys = [
  // Benchmark: start in motion. Two strides into frame, overshoot into a lean at the lock, then inspect.
  {t:0, hip:[410,632], chest:[445,492], head:[462,408], feet:[[350,830],[470,830]], hands:[[515,640],[385,642]], label:'walkin'},
  {t:.3, hip:[530,628], chest:[566,488], head:[582,404], feet:[[590,830],[470,830]], hands:[[500,640],[636,636]], label:'stride'},
  {t:.6, hip:[650,630], chest:[690,490], head:[708,406], feet:[[590,830],[710,830]], hands:[[760,632],[625,640]], label:'stride2'},
  {t:.82, hip:[668,620], chest:[718,478], head:[746,392], feet:[[590,830],[710,830]], hands:[[660,600],[740,598]], label:'settle'},
  {t:1.0, hip:[650,610], chest:[690,470], head:[710,385], feet:[[590,830],[710,830]], hands:[[665,630],[720,630]], label:'inspect'},
  {t:1.2, hip:[650,625], chest:[705,490], head:[735,405], feet:[[590,830],[710,830]], hands:[[790,560],[790,530]], label:'grip'},
  {t:1.8, hip:[645,650], chest:[690,515], head:[695,425], feet:[[590,830],[710,830]], hands:[[790,560],[790,530]], label:'test'},
  {t:2.5, hip:[600,650], chest:[690,530], head:[690,440], feet:[[590,830],[770,770]], hands:[[790,560],[790,530]], label:'brace'},
  {t:2.78, hip:[610,655], chest:[705,535], head:[710,450], feet:[[590,830],[770,770]], hands:[[790,560],[790,530]], label:'load'},
  {t:3.5, hip:[580,640], chest:[650,520], head:[630,435], feet:[[590,830],[770,770]], hands:[[790,560],[790,530]], label:'strain'},
  {t:3.8, hip:[580,640], chest:[650,520], head:[630,435], feet:[[590,830],[770,770]], hands:[[790,560],[790,530]], label:'limit'},
  // Benchmark (Alan Becker, AvA 2026-11-19): the failure is a full-body event: grip snaps, airborne, impact, bounce.
  {t:3.95, hip:[560,650], chest:[600,530], head:[585,445], feet:[[590,830],[740,790]], hands:[[700,470],[680,450]], label:'release'},
  {t:4.2, hip:[540,700], chest:[445,612], head:[388,552], feet:[[640,690],[670,640]], hands:[[392,520],[520,520]], label:'airborne'},
  {t:4.35, hip:[520,800], chest:[470,680], head:[450,595], feet:[[680,825],[720,800]], hands:[[430,820],[470,830]], label:'impact'},
  {t:4.42, hip:[520,802], chest:[480,700], head:[465,618], feet:[[680,825],[720,800]], hands:[[430,820],[470,830]], label:'squash'},
  // Master study: hold the landing squash ~0.19 s (Alan holds about 3 drawings) before the bounce.
  {t:4.54, hip:[520,802], chest:[480,700], head:[465,618], feet:[[680,825],[720,800]], hands:[[430,820],[470,830]], label:'squashhold'},
  {t:4.64, hip:[520,798], chest:[468,672], head:[448,588], feet:[[680,825],[720,800]], hands:[[430,820],[470,830]], label:'bounce'},
  {t:4.8, hip:[520,800], chest:[470,680], head:[452,596], feet:[[680,825],[720,800]], hands:[[430,820],[470,830]], label:'sit'},
  {t:4.95, hip:[520,800], chest:[478,676], head:[470,592], feet:[[680,825],[720,800]], hands:[[430,820],[525,580]], label:'raise'},
  {t:5.1, hip:[520,800], chest:[488,692], head:[502,612], feet:[[680,825],[720,800]], hands:[[430,820],[560,826]], label:'slam'},
  {t:5.45, hip:[545,700], chest:[548,565], head:[560,480], feet:[[470,830],[650,830]], hands:[[505,720],[600,720]], label:'push'},
  {t:5.8, hip:[560,613], chest:[550,475], head:[570,390], feet:[[470,830],[650,830]], hands:[[480,620],[610,625]], label:'recover'},
  {t:6.4, hip:[560,612.9171747926382], chest:[550,475], head:[535,390], feet:[[470,830],[650,830]], hands:[[480,620],[610,625]], label:'turn'},
  {t:7.0, hip:[550,620], chest:[530,480], head:[495,395], feet:[[470,830],[650,830]], hands:[[470,635],[590,635]], label:'notice'},
  // Decided: each stair step is brisk (~0.6 s) instead of a slow ~1 s shuffle.
  {t:7.6, hip:[520,620], chest:[500,480], head:[470,390], feet:[[470,830],[580,830]], hands:[[385,600],[550,640]], label:'choose'},
  {t:8.2, hip:[450,640], chest:[445,500], head:[425,415], feet:[[420,800],[580,830]], hands:[[370,640],[510,650]], label:'step'},
  {t:8.8, hip:[410,590], chest:[410,450], head:[390,365], feet:[[420,800],[350,770]], hands:[[340,590],[475,600]], label:'continue'},
  {t:9.4, hip:[340,560], chest:[335,420], head:[315,335], feet:[[280,740],[350,770]], hands:[[275,565],[390,570]], label:'climb'},
  {t:10.0, hip:[280,530], chest:[280,390], head:[260,305], feet:[[280,740],[210,740]], hands:[[215,540],[345,540]], label:'approach'},
  {t:10.6, hip:[190,520], chest:[195,380], head:[180,295], feet:[[170,740],[210,740]], hands:[[155,540],[245,540]], label:'arrive'},
  // Payoff: breathe, look back at the still-locked gate (eyeline insert), release, walk into the light.
  {t:11.0, hip:[190,516], chest:[195,370], head:[183,284], feet:[[170,740],[210,740]], hands:[[160,522],[235,522]], label:'breathe'},
  {t:11.8, hip:[194,518], chest:[214,382], head:[244,302], feet:[[170,740],[210,740]], hands:[[165,532],[272,540]], label:'lookback'},
  {t:13.0, hip:[194,518], chest:[214,382], head:[244,302], feet:[[170,740],[210,740]], hands:[[165,532],[272,540]], label:'hold'},
  {t:13.4, hip:[190,526], chest:[198,398], head:[206,320], feet:[[170,740],[210,740]], hands:[[165,548],[250,548]], label:'release'},
  {t:13.8, hip:[190,520], chest:[193,380], head:[176,295], feet:[[170,740],[210,740]], hands:[[155,532],[232,532]], label:'enter'},
  {t:14.5, hip:[190,520], chest:[193,380], head:[176,295], feet:[[170,740],[210,740]], hands:[[155,532],[232,532]], label:'through'}
];
const blendPoint = (a,b,k) => a.map((v,i)=>v+(b[i]-v)*k);
// Timing curves (benchmark: Alan's snap-and-hold and anticipation, AvA 56-57 s and 96-97 s).
const backIn=u=>u*u*(2.7*u-1.7);                       // dips back ~10% before travelling
const snap=u=>u<.5?4*u*u*u:1-Math.pow(-2*u+2,3)/2;     // slow start, fast middle, firm stop
const SNAP=new Set(['grip','test','brace','load','recover','turn','notice','breathe','lookback','release','raise']);
// Stay with the failed tactic, then reveal the route after the head turns toward it.
// Edited coverage: hard cuts frame the object or reaction the viewer needs at each beat.
// kind 'full' keeps the whole figure in frame; 'close' and 'insert' crop on purpose.
const MEDIUM={center:[810,560],zoom:1.9}, WIDE={center:[570,470],zoom:1.3}, ARCH={center:[450,500],zoom:1.55};
export const SHOTS=[
  {start:0, name:'medium', kind:'full'},
  {start:2.9, name:'grip-close', kind:'close', center:[815,545], zoom:3.0},
  {start:3.8, name:'medium', kind:'full'},                     // cut on the slip
  {start:6.2, name:'reveal', kind:'full'},                     // continuous widen after the head turn
  {start:8.8, name:'arch-push', kind:'full'},
  {start:11.5, name:'face-close', kind:'close', center:[215,410], zoom:2.6},
  {start:12.4, name:'lock-insert', kind:'insert', center:[895,520], zoom:2.4}, // what he is looking at
  {start:13.0, name:'arch', kind:'full'}
];
export function shotAt(time) {
  if (!Number.isFinite(time)) throw new TypeError('time must be finite');
  const t=Math.max(0,Math.min(DURATION,time));
  return SHOTS.filter(s=>s.start<=t).pop();
}
export function cameraAt(time) {
  const shot=shotAt(time), t=Math.max(0,Math.min(DURATION,time));
  // Retention lens (claude-youtube Shorts guide: a visual change every 2-3 s): follow the climb with a slow push.
  const reveal=progress(t,6.2,1), push=progress(t,8.8,1.9);
  let view;
  if(shot.center)view=shot;
  else if(shot.name==='reveal'||shot.name==='arch-push'||shot.name==='arch'){
    const c=blendPoint(blendPoint(MEDIUM.center,WIDE.center,reveal),ARCH.center,push);
    view={center:c,zoom:MEDIUM.zoom+(WIDE.zoom-MEDIUM.zoom)*reveal+(ARCH.zoom-WIDE.zoom)*push};
  } else view=MEDIUM;
  return {shot:shot.name,kind:shot.kind,reveal,push,
    matrix:layerMatrix({x:view.center[0]-960,y:view.center[1]-540,zoom:view.zoom},1,1920,1080)};
}
// Walking into the arch reads as depth: the figure scales about its arch-floor contact.
export const DEPTH_ANCHOR=[190,740];
export function depthAt(time) {
  if (!Number.isFinite(time)) throw new TypeError('time must be finite');
  return 1-.45*progress(Math.max(0,Math.min(DURATION,time)),13.8,.7);
}
export function poseAt(time) {
  if (!Number.isFinite(time)) throw new TypeError('time must be finite');
  const t=Math.max(0,Math.min(DURATION,time));
  let i=keys.findIndex(k=>k.t>t)-1;
  if(i<0)i=t>=DURATION?keys.length-2:0;
  const a=keys[i], b=keys[i+1], u=(t-a.t)/(b.t-a.t);
  // Losing support accelerates into impact; walking carries the body through foot plants.
  const k=['limit','airborne'].includes(a.label)?u*u:a.label==='release'?1-(1-u)*(1-u):SNAP.has(a.label)?snap(u):progress(t,a.t,b.t-a.t);
  const moving=['walkin','stride','choose','step','continue','climb','approach'].includes(a.label);
  const bodyK=moving?u:k;
  const p={time:t,label:a.label};
  for(const field of ['hip','chest','head']){
    const lead=field==='head'&&a.label==='recover'?backIn(progress(t,a.t+.2,.2)):bodyK;
    p[field]=blendPoint(a[field],b[field],lead);
  }
  for(const field of ['feet','hands']){
    const reach=field==='hands'&&a.label==='inspect'?backIn(Math.max(0,Math.min(1,(t-a.t-.06)/(b.t-a.t-.06)))):k;
    p[field]=a[field].map((v,j)=>blendPoint(v,b[field][j],reach));
  }
  // Effort comes in heaves (2.9-3.8 s); each stair plant loads the hips (benchmark: Alan's weight and rhythm).
  if(t>2.9&&t<3.8){const h=Math.sin((t-2.9)/.3*Math.PI);const d=Math.max(0,h)*16;
    p.hip=[p.hip[0]-d*.35,p.hip[1]+d*.3];p.chest=[p.chest[0]-d*1.2,p.chest[1]+d*.2];p.head=[p.head[0]-d*1.4,p.head[1]+d*.2];}
  {const e=t-7.38;if(e>0&&e<.3){const c=Math.sin(e/.3*Math.PI)*16;p.hip=[p.hip[0],p.hip[1]+c];p.chest=[p.chest[0],p.chest[1]+c*.9];p.head=[p.head[0],p.head[1]+c*.8];}}
  for(const plant of [8.2,8.8,9.4,10,10.6]){const e=t-plant;if(e>0&&e<.22){const dip=Math.sin(e/.22*Math.PI)*12;
    p.hip=[p.hip[0],p.hip[1]+dip];p.chest=[p.chest[0],p.chest[1]+dip*.8];p.head=[p.head[0],p.head[1]+dip*.7];}}
  // Walk bob: the body rises as the swing leg passes and sinks onto each contact.
  if(['walkin','stride','choose','step','continue','climb','approach'].includes(a.label)){
    const bob=Math.sin(Math.PI*u)*10;p.hip=[p.hip[0],p.hip[1]-bob];p.chest=[p.chest[0],p.chest[1]-bob];p.head=[p.head[0],p.head[1]-bob];
    p.hands=p.hands.map(h=>[h[0],h[1]-bob]);}
  // Whole-body acting on holds (frozen hip/torso/knee frames were 23%; Alan's pose changes nearly every drawing).
  {const add=(dx,dy,hipK=1,chestK=1,headK=1)=>{p.hip=[p.hip[0]+dx*hipK,p.hip[1]+dy*hipK];p.chest=[p.chest[0]+dx*chestK,p.chest[1]+dy*chestK];p.head=[p.head[0]+dx*headK,p.head[1]+dy*headK];};
   const bump=(t0,d)=>t>t0&&t<t0+d?Math.sin(Math.PI*(t-t0)/d):0;
   // brushing off: huffy weight shift back, body bobs with each rub
   if(t>5.78&&t<6.28){const w=bump(5.78,.5);add(-9*w,0,0,1.1,1.1);add(0,Math.abs(Math.sin((t-5.78)*22))*5*w,0,1,1);}
   // arrival: a real breath (shoulders rise, knees give on the exhale)
   {const b=bump(10.85,.55);add(0,-11*b,0,1,1);const g=bump(11.2,.4);add(0,6*g,1,.8,.6);}
   // look back: weight drifts toward the gate, head tilts, then a sigh (shoulders up, then down) before turning away
   if(t>11.6&&t<13.1){const lean=Math.sin(Math.PI*Math.min(1,(t-11.6)/1.5)/2);add(9*lean,2*lean,1,1.2,1.4);}
   {const up=bump(12.15,.45),down=bump(12.6,.45);add(0,-10*up+8*down,.2,1,1);add(5*down,0,0,0,1);}
  }
  // Acting beat (owner QC "still stiff"): after getting up he angrily brushes the dust off his hands.
  if(t>5.78&&t<6.18){const w=Math.sin(Math.PI*(t-5.78)/.4),rub=Math.sin((t-5.78)*44)*12;
    const tgt=[[p.chest[0]+40+rub*.8,p.chest[1]+150],[p.chest[0]+60-rub*.8,p.chest[1]+144]];
    p.hands=p.hands.map((h,j)=>[h[0]+(tgt[j][0]-h[0])*w,h[1]+(tgt[j][1]-h[1])*w]);}
  const lifts={walkin:[44,0],stride:[0,44],test:[0,28],limit:[20,0],notice:[0,48],choose:[48,0],step:[0,70],continue:[70,0],climb:[0,70],approach:[60,0],enter:[0,26]}[a.label]||[0,0];
  p.feet.forEach((v,j)=>{v[1]-=Math.sin(Math.PI*k)*lifts[j];});
  return p;
}
// Head follows the spine direction through a damped spring: it lags, overshoots and settles.
let headTrack=null;
function headDirection(time){
  if(!headTrack){
    const dt=1/240,n=Math.ceil(DURATION/dt)+1,w=2*Math.PI*3.2,z=.42;
    const dir=t=>{const p=poseAt(t);const v=[p.head[0]-p.chest[0],p.head[1]-p.chest[1]];const l=Math.hypot(...v);return [v[0]/l,v[1]/l];};
    let x=dir(0),v=[0,0];headTrack=[x.slice()];
    for(let i=1;i<n;i++){const g=dir(Math.min(DURATION,i*dt));
      for(const k of [0,1]){const a=w*w*(g[k]-x[k])-2*z*w*v[k];v[k]+=a*dt;x[k]+=v[k]*dt;}
      headTrack.push(x.slice());}
  }
  const f=Math.max(0,Math.min(DURATION,time))*240,i=Math.min(headTrack.length-2,Math.floor(f)),u=f-i;
  const d=[headTrack[i][0]+(headTrack[i+1][0]-headTrack[i][0])*u,headTrack[i][1]+(headTrack[i+1][1]-headTrack[i][1])*u];
  const l=Math.hypot(...d);return [d[0]/l,d[1]/l];
}
// Impacts that make the world react: dust and a short camera shake.
export const IMPACTS=[{t:4.35,at:[520,830],shake:9},{t:5.1,at:[560,830],shake:5}];
export function shakeAt(time){let x=0,y=0,r=0;for(const m of IMPACTS){const e=time-m.t;if(e>=0&&e<.3){const a=m.shake*Math.exp(-e*14);x+=a*Math.sin(e*90);y+=a*Math.cos(e*70);r+=a*.004*Math.sin(e*40);}}return [x,y,r];}
// Owner QC 2026-11-19: "still stiff". Systemic looseness, from Alan's footage (every drawing moves the arms):
// free hands follow through on a damped spring (relative to the chest), travel in arcs, and holds keep breathing.
// Hands in contact (gate grip, floor, slam, arch jamb) stay exact, with 0.12 s blends in and out.
const CONTACTS=[[[1.2,3.8],[4.35,5.45]],[[1.2,3.8],[5.04,5.16],[11.8,13.0]]];
function freeWeight(t,j){let w=1;for(const [a,b] of CONTACTS[j]){if(t>=a&&t<=b)return 0;const e=t<a?a-t:t-b;w=Math.min(w,Math.min(1,e/.12));}return w*w*(3-2*w);}
let handTrack=null;
function handSpring(time){
  if(!handTrack){
    const dt=1/240,n=Math.ceil(DURATION/dt)+1,w=2*Math.PI*2.0,z=.22;
    const local=t=>{const p=poseAt(t);return p.hands.map(h=>[h[0]-p.chest[0],h[1]-p.chest[1]]);};
    let x=local(0),v=[[0,0],[0,0]];handTrack=[x.map(q=>q.slice())];
    for(let i=1;i<n;i++){const g=local(Math.min(DURATION,i*dt));
      for(const j of [0,1])for(const k of [0,1]){const acc=w*w*(g[j][k]-x[j][k])-2*z*w*v[j][k];v[j][k]+=acc*dt;x[j][k]+=v[j][k]*dt;}
      handTrack.push(x.map(q=>q.slice()));}
  }
  const f=Math.max(0,Math.min(DURATION,time))*240,i=Math.min(handTrack.length-2,Math.floor(f)),u=f-i;
  return [0,1].map(j=>[0,1].map(k=>handTrack[i][j][k]+(handTrack[i+1][j][k]-handTrack[i][j][k])*u));
}
// Moving hold: slow breathing and a small weight shift, so no pose is ever frozen.
export function breathAt(t){return [Math.sin(t*1.9)*2.2,Math.sin(t*2.3+1)*3.2];}
// Elbow branch track: each elbow keeps its bend side and switches only near full extension (invisible), toward hanging down.
let branchTrack=null;
function elbowBranch(time,j){
  if(!branchTrack){
    const dt=1/120,n=Math.ceil(DURATION/dt)+1;branchTrack=[];
    let cur=null;
    for(let i=0;i<n;i++){const both=geometryAt(Math.min(DURATION,i*dt),'both');
      if(!cur)cur=both.map(([a,b])=>b.elbow[1]>a.elbow[1]?-1:1);
      cur=cur.map((c,k)=>{const [a,b]=both[k],mine=c===1?a:b,other=c===1?b:a;
        const near=Math.hypot(mine.elbow[0]-other.elbow[0],mine.elbow[1]-other.elbow[1])<14;
        return near&&other.elbow[1]>mine.elbow[1]+1?-c:c;});
      branchTrack.push(cur.slice());}
  }
  return branchTrack[Math.min(branchTrack.length-1,Math.round(Math.max(0,Math.min(DURATION,time))*120))][j];
}
export function geometryAt(time, mode) {
  const p=poseAt(time);
  const gripping=p.time>=1.2&&p.time<=3.8;
  const envelope=progress(p.time,1.8,.3)*(1-progress(p.time,3.5,.3));
  const rattle=Math.sin(p.time*42)*2.5*envelope;
  // The gate springs back when the grip snaps, then settles (still locked).
  const since=p.time-3.95, swing=since>0?16*Math.exp(-since*5)*Math.sin(since*28):0;
  const gateOffset=rattle+swing;
  const dx=p.head[0]-p.chest[0],dy=p.head[1]-p.chest[1],length=Math.hypot(dx,dy);
  const normal=[-dy/length,dx/length];
  const shoulders=[-1,1].map(side=>[p.chest[0]+normal[0]*side*5,p.chest[1]+normal[1]*side*5]);
  const [sway,breath]=breathAt(p.time), still=1-Math.min(1,Math.hypot(...['hip'].map(()=>0)));
  p.chest=[p.chest[0]+sway*.5,p.chest[1]+breath];p.head=[p.head[0]+sway*.6,p.head[1]+breath];
  const sp=handSpring(p.time);
  const hands=p.hands.map((v,j)=>{
    const w=freeWeight(p.time,j);if(w===0)return [v[0]+(gripping?rattle:0),v[1]];
    // spring follow-through plus a small arc bulge and idle drift, faded in away from contacts
    const target=[p.chest[0]+sp[j][0],p.chest[1]+sp[j][1]];
    const idle=[Math.sin(p.time*2.1+j*2)*8,Math.sin(p.time*1.7+j)*9+breath];
    return [v[0]+(target[0]-v[0]+idle[0])*w,v[1]+(target[1]-v[1]+idle[1])*w];});
  // Master study: relaxed arms are near-straight strokes. Free hands extend toward ~95% of arm length,
  // except during a deliberate hand action (the dust-brush), so elbows never fold into odd shapes at rest.
  const brushing=p.time>5.72&&p.time<6.24;
  shoulders.forEach((s,j)=>{const w=freeWeight(p.time,j)*(brushing?0:1);if(!w)return;
    const dx=hands[j][0]-s[0],dy=hands[j][1]-s[1],r=Math.hypot(dx,dy)||1,want=(84+90)*.985,L=r+(want-r)*w*.9;
    hands[j]=[s[0]+dx*L/r,s[1]+dy*L/r];});
  // hands never pass through the floor (spring overshoot on impacts)
  hands.forEach((h,j)=>{if(h[1]>826)hands[j]=[h[0],826];});
  // never ask the arm for more than it can reach (spring overshoot)
  shoulders.forEach((s,j)=>{const dx=hands[j][0]-s[0],dy=hands[j][1]-s[1],r=Math.hypot(dx,dy),m=(84+90)*.988;
    if(r>m)hands[j]=[s[0]+dx*m/r,s[1]+dy*m/r];});
  // Owner QC "hands are odd": elbows must hang down and back, never jut out sideways. Pick the IK branch whose elbow is lower.
  if(mode==='both')return shoulders.map((s,i)=>[solveArm(s,hands[i],84,90,1),solveArm(s,hands[i],84,90,-1)]);
  const arms=shoulders.map((s,i)=>solveArm(s,hands[i],84,90,elbowBranch(time,i)));
  // Change facing only at the extended-leg passing pose; mirrored knees must not cross.
  const kneeBend=p.time<6.4?-1:1;
  const legs=p.feet.map(f=>solveArm(p.hip,f,115,120,kneeBend));
  // During bracing, foot contact follows the same gate displacement as the hands.
  const braceWeight=progress(p.time,1.8,.7)*(1-progress(p.time,3.8,.35));
  if(braceWeight>0){
    p.feet[1]=[p.feet[1][0]+rattle*braceWeight,p.feet[1][1]];
    legs[1]=solveArm(p.hip,p.feet[1],115,120,kneeBend);
  }
  const prev=poseAt(Math.max(0,p.time-1/30)),vel=[(p.chest[0]-prev.chest[0])*30,(p.chest[1]-prev.chest[1])*30];
  const dragX=Math.max(-40,Math.min(40,-vel[0]*.12)),dragY=Math.max(-24,Math.min(24,-vel[1]*.07));
  const spineControl=[(p.hip[0]+p.chest[0])*.5-22+dragX,(p.hip[1]+p.chest[1])*.5+8+dragY];
  const toeAngle=Math.PI*progress(p.time,6.1,.6);
  const toeTargets=legs.map(a=>[a.wrist[0]+19*Math.cos(toeAngle),a.wrist[1]-19*Math.sin(toeAngle)]);
  // Proportions (owner note 2026-11-19 "stick insect"; Alan benchmark): big head sitting on the shoulders, no neck.
  const hd=headDirection(p.time);
  const head=[p.chest[0]+hd[0]*(HEAD_R+4),p.chest[1]+hd[1]*(HEAD_R+4)];
  return {pose:p,arms,legs,shoulders,handTargets:hands,spineControl,gateOffset,gripping,toeTargets,head};
}


// Minimal face (benchmark 2026-11-19: DayOne storyboards carry emotion with dot eyes, brow strokes and a mouth line).
// eye: 0 closed .. 1 open .. 1.3 wide; brow: -1 worried (inner up) .. 1 angry (inner down); lift: brow height;
// smile: -1 frown .. 1 smile; open: mouth opening 0..1.
const faceKeys = [
  {t:0, eye:1, brow:-.2, lift:.4, smile:0, open:0, label:'curious'},
  {t:1.2, eye:.85, brow:.15, lift:.1, smile:0, open:0, label:'focused'},
  {t:1.8, eye:.15, brow:1, lift:-.3, smile:-.4, open:.35, label:'strain'},
  {t:3.85, eye:1.3, brow:-.6, lift:1, smile:0, open:.8, label:'shock'},
  {t:4.3, eye:.1, brow:.6, lift:-.2, smile:-.5, open:.5, label:'ouch'},
  {t:4.8, eye:.7, brow:1, lift:-.2, smile:-.7, open:0, label:'frustrated'},
  {t:6.1, eye:1.15, brow:-.3, lift:1, smile:0, open:.3, label:'noticing'},
  {t:7.4, eye:.9, brow:.5, lift:0, smile:.25, open:0, label:'determined'},
  {t:11.0, eye:0, brow:0, lift:.2, smile:.1, open:.15, label:'breathing'},
  {t:11.8, eye:.85, brow:-.6, lift:.5, smile:-.1, open:0, label:'wistful'},
  {t:13.2, eye:0, brow:-.2, lift:.3, smile:.75, open:0, label:'relieved'},
  {t:13.8, eye:1, brow:-.1, lift:.3, smile:.5, open:0, label:'content'}
];
const BLINKS=[.9,9.1];
// Expressions change faster than the body: blend into each key over 0.18 s, then hold.
export function faceAt(time) {
  if (!Number.isFinite(time)) throw new TypeError('time must be finite');
  const t=Math.max(0,Math.min(DURATION,time));
  let i=faceKeys.findIndex(k=>k.t>t)-1; if(i<0)i=faceKeys.length-1;
  const b=faceKeys[i], a=faceKeys[Math.max(0,i-1)], k=i===0?1:progress(t,b.t,.18);
  const f={label:b.label};
  for(const field of ['eye','brow','lift','smile','open'])f[field]=a[field]+(b[field]-a[field])*k;
  for(const at of BLINKS){const d=Math.abs(t-at);if(d<.08)f.eye*=d/.08;}
  return f;
}

// Sound events on contacts (benchmark: AvA ~2.4 hits/s during action, silence between; no music).
// type: step | clank | rattle | twang | whoosh | thud | slam | pluck | chime. gain 0..1.
// Owner 2026-11-19: no footstep sounds; effects only on the gate, the fall, the slam and the two story beats.
export const SOUND_EVENTS = [
  {t:1.2,type:'clank',gain:.8},{t:1.8,type:'rattle',gain:.5,dur:1.15},
  {t:3.05,type:'clank',gain:.85},{t:3.65,type:'clank',gain:.9},
  {t:3.95,type:'twang',gain:.9},{t:3.97,type:'whoosh',gain:.6,dur:.38},
  {t:4.35,type:'thud',gain:1},{t:4.64,type:'thud',gain:.5},{t:5.1,type:'slam',gain:.9},
  {t:6.3,type:'pluck',gain:.5},{t:13.4,type:'chime',gain:.35}
];

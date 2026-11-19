// Original whole-body exercise. Reuses the existing FounderNotes motion geometry.
// Draft: pure geometry checked; browser rendering and audiovisual review still required.
import {progress, solveArm, layerMatrix} from './story-motion.mjs';
export const DURATION = 14.5;
const keys = [
  {t:0, hip:[650,610], chest:[690,470], head:[710,385], feet:[[590,830],[710,830]], hands:[[665,630],[720,630]], label:'inspect'},
  {t:1.2, hip:[650,625], chest:[705,490], head:[735,405], feet:[[590,830],[710,830]], hands:[[790,560],[790,530]], label:'grip'},
  {t:1.8, hip:[645,650], chest:[690,515], head:[695,425], feet:[[590,830],[710,830]], hands:[[790,560],[790,530]], label:'test'},
  {t:2.5, hip:[600,650], chest:[690,530], head:[690,440], feet:[[590,830],[770,770]], hands:[[790,560],[790,530]], label:'brace'},
  {t:2.78, hip:[610,655], chest:[705,535], head:[710,450], feet:[[590,830],[770,770]], hands:[[790,560],[790,530]], label:'load'},
  {t:3.5, hip:[580,640], chest:[650,520], head:[630,435], feet:[[590,830],[770,770]], hands:[[790,560],[790,530]], label:'strain'},
  {t:3.8, hip:[580,640], chest:[650,520], head:[630,435], feet:[[590,830],[770,770]], hands:[[790,560],[790,530]], label:'limit'},
  {t:4.15, hip:[560,700], chest:[575,590], head:[590,500], feet:[[470,830],[650,830]], hands:[[700,650],[670,675]], label:'slip'},
  {t:4.8, hip:[550,680], chest:[540,550], head:[550,460], feet:[[470,830],[650,830]], hands:[[640,680],[590,700]], label:'catch'},
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
  {t:11.8, hip:[194,518], chest:[214,382], head:[244,302], feet:[[170,740],[210,740]], hands:[[165,532],[272,500]], label:'lookback'},
  {t:13.0, hip:[194,518], chest:[214,382], head:[244,302], feet:[[170,740],[210,740]], hands:[[165,532],[272,500]], label:'hold'},
  {t:13.4, hip:[190,526], chest:[198,398], head:[206,320], feet:[[170,740],[210,740]], hands:[[165,548],[250,548]], label:'release'},
  {t:13.8, hip:[190,520], chest:[193,380], head:[176,295], feet:[[170,740],[210,740]], hands:[[155,532],[232,532]], label:'enter'},
  {t:14.5, hip:[190,520], chest:[193,380], head:[176,295], feet:[[170,740],[210,740]], hands:[[155,532],[232,532]], label:'through'}
];
const blendPoint = (a,b,k) => a.map((v,i)=>v+(b[i]-v)*k);
// Stay with the failed tactic, then reveal the route after the head turns toward it.
// Edited coverage: hard cuts frame the object or reaction the viewer needs at each beat.
// kind 'full' keeps the whole figure in frame; 'close' and 'insert' crop on purpose.
const MEDIUM={center:[810,560],zoom:1.9}, WIDE={center:[570,470],zoom:1.3}, ARCH={center:[450,500],zoom:1.55};
export const SHOTS=[
  {start:0, name:'medium', kind:'full'},
  {start:2.9, name:'grip-close', kind:'close', center:[815,545], zoom:3.0},
  {start:3.8, name:'medium', kind:'full'},                     // cut on the slip
  {start:6.2, name:'reveal', kind:'full'},                     // continuous widen after the head turn
  {start:10.6, name:'arch-push', kind:'full'},
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
  const reveal=progress(t,6.2,1), push=progress(t,10.6,.9);
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
  const k=a.label==='limit'?u*u:progress(t,a.t,b.t-a.t);
  const moving=['choose','step','continue','climb','approach'].includes(a.label);
  const bodyK=moving?u:k;
  const p={time:t,label:a.label};
  for(const field of ['hip','chest','head']){
    const lead=field==='head'&&a.label==='recover'?progress(t,a.t+.2,.2):bodyK;
    p[field]=blendPoint(a[field],b[field],lead);
  }
  for(const field of ['feet','hands']){
    const reach=field==='hands'&&a.label==='inspect'?progress(t,.35,.85):k;
    p[field]=a[field].map((v,j)=>blendPoint(v,b[field][j],reach));
  }
  const lifts={test:[0,28],limit:[20,0],notice:[0,48],choose:[48,0],step:[0,70],continue:[70,0],climb:[0,70],approach:[60,0],enter:[0,26]}[a.label]||[0,0];
  p.feet.forEach((v,j)=>{v[1]-=Math.sin(Math.PI*k)*lifts[j];});
  return p;
}
export function geometryAt(time) {
  const p=poseAt(time);
  const gripping=p.time>=1.2&&p.time<=3.8;
  const envelope=progress(p.time,1.8,.3)*(1-progress(p.time,3.5,.3));
  const gateOffset=Math.sin(p.time*42)*2.5*envelope;
  const dx=p.head[0]-p.chest[0],dy=p.head[1]-p.chest[1],length=Math.hypot(dx,dy);
  const normal=[-dy/length,dx/length];
  const shoulders=[-1,1].map(side=>[p.chest[0]+normal[0]*side*5,p.chest[1]+normal[1]*side*5]);
  const hands=p.hands.map(v=>[v[0]+(gripping?gateOffset:0),v[1]]);
  const arms=shoulders.map((s,i)=>solveArm(s,hands[i],84,90,1));
  // Change facing only at the extended-leg passing pose; mirrored knees must not cross.
  const kneeBend=p.time<6.4?-1:1;
  const legs=p.feet.map(f=>solveArm(p.hip,f,115,120,kneeBend));
  // During bracing, foot contact follows the same gate displacement as the hands.
  const braceWeight=progress(p.time,1.8,.7)*(1-progress(p.time,3.8,.35));
  if(braceWeight>0){
    p.feet[1]=[p.feet[1][0]+gateOffset*braceWeight,p.feet[1][1]];
    legs[1]=solveArm(p.hip,p.feet[1],115,120,kneeBend);
  }
  const spineControl=[(p.hip[0]+p.chest[0])*.5-22,(p.hip[1]+p.chest[1])*.5+8];
  const toeAngle=Math.PI*progress(p.time,6.1,.6);
  const toeTargets=legs.map(a=>[a.wrist[0]+19*Math.cos(toeAngle),a.wrist[1]-19*Math.sin(toeAngle)]);
  return {pose:p,arms,legs,shoulders,handTargets:hands,spineControl,gateOffset,gripping,toeTargets};
}


// Minimal face (benchmark 2026-11-19: DayOne storyboards carry emotion with dot eyes, brow strokes and a mouth line).
// eye: 0 closed .. 1 open .. 1.3 wide; brow: -1 worried (inner up) .. 1 angry (inner down); lift: brow height;
// smile: -1 frown .. 1 smile; open: mouth opening 0..1.
const faceKeys = [
  {t:0, eye:1, brow:-.2, lift:.4, smile:0, open:0, label:'curious'},
  {t:1.2, eye:.85, brow:.15, lift:.1, smile:0, open:0, label:'focused'},
  {t:1.8, eye:.15, brow:1, lift:-.3, smile:-.4, open:.35, label:'strain'},
  {t:3.85, eye:1.3, brow:-.6, lift:1, smile:0, open:.8, label:'shock'},
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

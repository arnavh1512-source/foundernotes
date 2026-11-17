// Original whole-body exercise. Reuses the existing FounderNotes motion geometry.
// Draft: pure geometry checked; browser rendering and audiovisual review still required.
import {progress, solveArm} from './story-motion.mjs';
export const DURATION = 10.5;
const keys = [
  {t:0, hip:[650,660], chest:[715,510], head:[740,425], feet:[[590,830],[710,830]], hands:[[735,590],[750,570]], label:'inspect'},
  {t:1.2, hip:[650,660], chest:[715,510], head:[740,425], feet:[[590,830],[710,830]], hands:[[790,560],[790,530]], label:'grip'},
  {t:1.8, hip:[645,680], chest:[690,535], head:[695,445], feet:[[590,830],[710,830]], hands:[[790,560],[790,530]], label:'test'},
  {t:2.5, hip:[650,665], chest:[690,530], head:[690,440], feet:[[590,830],[770,720]], hands:[[790,560],[790,530]], label:'brace'},
  {t:3.5, hip:[620,690], chest:[650,560], head:[630,475], feet:[[590,830],[770,720]], hands:[[790,560],[790,530]], label:'strain'},
  {t:3.8, hip:[620,690], chest:[650,560], head:[630,475], feet:[[590,830],[770,720]], hands:[[790,560],[790,530]], label:'limit'},
  {t:4.15, hip:[560,725], chest:[575,620], head:[590,530], feet:[[470,830],[650,830]], hands:[[700,650],[670,675]], label:'slip'},
  {t:4.8, hip:[550,720], chest:[540,610], head:[550,520], feet:[[470,830],[630,830]], hands:[[640,680],[590,700]], label:'catch'},
  {t:5.8, hip:[560,680], chest:[550,560], head:[570,465], feet:[[470,830],[630,830]], hands:[[470,665],[620,670]], label:'recover'},
  {t:7.0, hip:[550,675], chest:[530,545], head:[495,455], feet:[[470,830],[630,830]], hands:[[450,655],[600,660]], label:'notice'},
  {t:8.3, hip:[520,670], chest:[500,535], head:[470,445], feet:[[470,830],[580,830]], hands:[[370,600],[560,660]], label:'choose'},
  {t:9.4, hip:[450,660], chest:[445,520], head:[425,435], feet:[[420,800],[580,830]], hands:[[370,640],[510,650]], label:'step'},
  {t:10.5, hip:[410,630], chest:[410,490], head:[390,405], feet:[[350,770],[490,830]], hands:[[340,610],[475,620]], label:'continue'}
];
const blendPoint = (a,b,k) => a.map((v,i)=>v+(b[i]-v)*k);
export function poseAt(time) {
  if (!Number.isFinite(time)) throw new TypeError('time must be finite');
  const t=Math.max(0,Math.min(DURATION,time));
  let i=keys.findIndex(k=>k.t>t)-1;
  if(i<0)i=t>=DURATION?keys.length-2:0;
  const a=keys[i], b=keys[i+1], k=progress(t,a.t,b.t-a.t);
  const p={time:t,label:a.label};
  for(const field of ['hip','chest','head'])p[field]=blendPoint(a[field],b[field],k);
  for(const field of ['feet','hands'])p[field]=a[field].map((v,j)=>blendPoint(v,b[field][j],k));
  const lifts={test:[0,28],limit:[20,0],choose:[48,0],step:[0,48]}[a.label]||[0,0];
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
  const shoulders=[-1,1].map(side=>[p.chest[0]+normal[0]*side*14,p.chest[1]+normal[1]*side*14]);
  const hands=p.hands.map(v=>[v[0]+(gripping?gateOffset:0),v[1]]);
  const arms=shoulders.map((s,i)=>solveArm(s,hands[i],84,90,1));
  const legs=p.feet.map((f,i)=>solveArm(p.hip,f,115,120,i===0?-1:1));
  // During bracing, foot contact follows the same gate displacement as the hands.
  const braceWeight=progress(p.time,1.8,.7)*(1-progress(p.time,3.8,.35));
  if(braceWeight>0){
    p.feet[1]=[p.feet[1][0]+gateOffset*braceWeight,p.feet[1][1]];
    legs[1]=solveArm(p.hip,p.feet[1],115,120,1);
  }
  const spineControl=[(p.hip[0]+p.chest[0])*.5-22,(p.hip[1]+p.chest[1])*.5+8];
  return {pose:p,arms,legs,shoulders,handTargets:hands,spineControl,gateOffset,gripping};
}

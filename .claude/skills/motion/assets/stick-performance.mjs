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
  {t:8.3, hip:[520,620], chest:[500,480], head:[470,390], feet:[[470,830],[580,830]], hands:[[385,600],[550,640]], label:'choose'},
  {t:9.4, hip:[450,640], chest:[445,500], head:[425,415], feet:[[420,800],[580,830]], hands:[[370,640],[510,650]], label:'step'},
  {t:10.5, hip:[410,590], chest:[410,450], head:[390,365], feet:[[420,800],[350,770]], hands:[[340,590],[475,600]], label:'continue'},
  {t:11.4, hip:[340,560], chest:[335,420], head:[315,335], feet:[[280,740],[350,770]], hands:[[275,565],[390,570]], label:'climb'},
  {t:12.3, hip:[280,530], chest:[280,390], head:[260,305], feet:[[280,740],[210,740]], hands:[[215,540],[345,540]], label:'approach'},
  {t:13.3, hip:[190,520], chest:[195,380], head:[180,295], feet:[[170,740],[210,740]], hands:[[155,540],[245,540]], label:'arrive'},
  {t:14.5, hip:[190,520], chest:[195,380], head:[180,295], feet:[[170,740],[210,740]], hands:[[155,540],[245,540]], label:'settle'}
];
const blendPoint = (a,b,k) => a.map((v,i)=>v+(b[i]-v)*k);
// Stay with the failed tactic, then reveal the route after the head turns toward it.
export function cameraAt(time) {
  if (!Number.isFinite(time)) throw new TypeError('time must be finite');
  const reveal=progress(Math.max(0,Math.min(DURATION,time)),6.2,1);
  const center=blendPoint([810,560],[570,470],reveal);
  const zoom=1.9+(1.3-1.9)*reveal;
  return {reveal,matrix:layerMatrix({x:center[0]-960,y:center[1]-540,zoom},1,1920,1080)};
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
  const lifts={test:[0,28],limit:[20,0],notice:[0,48],choose:[48,0],step:[0,70],continue:[70,0],climb:[0,70],approach:[60,0]}[a.label]||[0,0];
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


// Original performances for the existing 64.5-second dialogue; no voice or source artwork.
import {progress, solveArm} from './story-motion.mjs';
import {geometryAt} from './stick-performance.mjs';
export const PILOT_DURATION=64.5;
export const PILOT_SHOTS=[
 {start:0,end:14.5,name:'gate'},
 {start:14.5,end:29,name:'study'},
 {start:29,end:41,name:'burden'},
 {start:41,end:46,name:'cup'},
 {start:46,end:56,name:'views'},
 {start:56,end:64.5,name:'exit'}
];
const pilotBlend=(a,b,k)=>a.map((v,i)=>v+(b[i]-v)*k);
export function pilotShotAt(time){
 if(!Number.isFinite(time))throw new TypeError('time must be finite');
 const t=Math.max(0,Math.min(PILOT_DURATION,time));
 return PILOT_SHOTS.find(s=>t>=s.start&&t<s.end)||PILOT_SHOTS.at(-1);
}
export function pilotCupAt(time){
 const lift=time>=41&&time<46?1-progress(time,41.4,.6):progress(time,23,.6)*(1-progress(time,26,.7));
 const center=[1200+80*lift,597-122*lift];
 return {center,grip:[center[0]+30,center[1]+1]};
}
// One attempted task, interrupted by a phone, followed by a missed paper catch.
export function pilotTaskAt(time){
 if(!Number.isFinite(time))throw new TypeError('time must be finite');
 const lift=progress(time,33.7,.6)*(1-progress(time,36.3,.7));
 const phoneCenter=pilotBlend([865,583],[815,490],lift);
 const phoneGrip=[phoneCenter[0]+22,phoneCenter[1]+15];
 const gripWeight=progress(time,33.1,.6)*(1-progress(time,37.1,.3));
 const writing=1-progress(time,32.6,.4);
 const spill=progress(time,37.4,1.2);
 const delivery=progress(time,35.6,1.2),deliveryX=1820-590*delivery;
 const pages=[0,1].map(i=>{const k=progress(time,37.4+i*.2,1.0);return {center:pilotBlend([deliveryX+i*30,603-i*6],[1250+i*80,805],k),angle:(i===0?-.45:.6)*Math.sin(Math.PI*k),fallen:k===1};});
 return {phoneCenter,phoneGrip,gripWeight,writing,spill,pages,deliveryX,deliveryVisible:time>=35.6,deliveryHand:progress(time,35.6,.3)*(1-progress(time,36.9,.4))};
}
export function pilotActorAt(time,role,mode='study'){
 if(!Number.isFinite(time))throw new TypeError('time must be finite');
 if(!['youth','philosopher'].includes(role))throw new TypeError('unknown actor');
 let p;
 if(role==='philosopher'){
  p={hip:[1320,650],chest:[1320,520],head:[1310,435],feet:[[1240,830],[1400,830]],hands:[pilotCupAt(time).grip,[1370,678]],facing:-1,intent:'listen'};
 }else if(mode==='burden'){
  const task=pilotTaskAt(time),notice=progress(time,32.6,.35)*(1-progress(time,35.5,.5));
  const miss=progress(time,37.5,.5),settle=progress(time,39.2,1.0);
  p={hip:pilotBlend(pilotBlend([690,640],[700,660],miss),[690,680],settle),
   chest:pilotBlend(pilotBlend([750,510],[780,540],miss),[750,550],settle),
   head:pilotBlend(pilotBlend([775+15*notice,425+6*notice],[815,455],miss),[770,475],settle),
   feet:[[590,830],[710,830]],hands:[[810,620],[825+40*progress(time,29,3.6),597+2*Math.cos((time-29)*9)*task.writing]],facing:1,intent:time<32.6?'work':'strain'};
  p.hands[1]=pilotBlend(p.hands[1],task.phoneGrip,task.gripWeight);
  p.hands[1]=pilotBlend(p.hands[1],[910,650],miss);
  p.hands[1]=pilotBlend(p.hands[1],[835,615],settle);
 }else{
  const lean=progress(time,14.5,1.2)*(1-progress(time,22,.8));
  const point=progress(time,15.2,.4)*(1-progress(time,17.5,.5))+.65*progress(time,20,.4)*(1-progress(time,21.4,.4));
  p={hip:pilotBlend([650,610],[690,640],lean),chest:pilotBlend([690,470],[745,510],lean),head:pilotBlend([710,385],[775,425],lean),feet:[[590,830],[710,830]],hands:[pilotBlend([665,630],[810,620],lean),pilotBlend([720,630],[820+50*point,570-80*point],lean)],facing:1,intent:lean>.3?'argue':'listen'};
  p.head[1]+=6*Math.sin(Math.PI*progress(time,24.5,.8));
  const recoil=progress(time,43.1,.45)*(1-progress(time,45.2,.6));
  p.hip[0]-=12*recoil;p.chest[0]-=18*recoil;p.head[0]-=28*recoil;
  p.hands[0]=pilotBlend(p.hands[0],[650,600],recoil);p.hands[1]=pilotBlend(p.hands[1],[770,550],recoil);
 }
 const normalSide=p.facing===1?-1:1;
 const shoulders=[-5,5].map(d=>[p.chest[0]+d,p.chest[1]]);
 const arms=shoulders.map((a,i)=>solveArm(a,p.hands[i],84,90,role==='philosopher'&&i===0?-1:1));
 const legs=p.feet.map(f=>solveArm(p.hip,f,115,120,normalSide));
 return {pose:p,shoulders,arms,legs,toeTargets:legs.map(a=>[a.wrist[0]+p.facing*19,a.wrist[1]]),spineControl:[(p.hip[0]+p.chest[0])/2-16*p.facing,(p.hip[1]+p.chest[1])/2+8]};
}
export function pilotExitAt(time){
 const t=Math.max(56,Math.min(PILOT_DURATION,time)),phase=(t-56)*6;
 const source=geometryAt(14.5),p=JSON.parse(JSON.stringify(source.pose));
 p.facing=-1;p.intent='walk';
 p.hip[1]=550+3*Math.sin(phase)**2;p.chest[1]+=30;p.head[1]+=30;
 const depthAt=u=>{const d=progress(Math.max(0,Math.min(8.5,u)),0,8.5);return {scale:1-.55*d,anchor:[190+5*d,740-170*d]};};
 const depth=depthAt(t-56);
 p.feet=[0,1].map(i=>{
  const offset=i*.55,local=t-56+offset,cycle=Math.floor(local/1.1),fraction=local/1.1-cycle;
  const start=cycle*1.1-offset;
  const ground=u=>{const d=depthAt(u);return [d.anchor[0]+(i===0?-20:20)*d.scale,d.anchor[1]];};
  let world=ground(start);
  if(fraction>=.5){const k=progress(fraction,.5,.5);world=pilotBlend(world,ground(start+1.1),k);world[1]-=18*depth.scale*Math.sin(Math.PI*k);}
  return [190+(world[0]-depth.anchor[0])/depth.scale,740+(world[1]-depth.anchor[1])/depth.scale];
 });
 p.hands=[[155+15*Math.sin(phase),570],[245-15*Math.sin(phase),570]];
 const shoulders=[-5,5].map(d=>[p.chest[0]+d,p.chest[1]]);
 const arms=shoulders.map((a,i)=>solveArm(a,p.hands[i],84,90,1));
 const legs=p.feet.map(f=>solveArm(p.hip,f,115,120,1));
 return {pose:p,shoulders,arms,legs,toeTargets:legs.map(a=>[a.wrist[0]-19,a.wrist[1]]),spineControl:[170,480],depth};
}


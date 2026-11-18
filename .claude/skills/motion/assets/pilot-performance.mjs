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
// Framing follows changes of intention, with one room axis throughout the exchange.
export function pilotRoomCameraAt(time){
 if(!Number.isFinite(time))throw new TypeError('time must be finite');
 if(time>=41&&time<42.7)return {scale:2.6,x:1240,y:550};
 if(time>=42.7&&time<44.5)return {scale:2.05,x:760,y:465};
 if(time>=44.5&&time<46)return {scale:1.6,x:1030,y:530};
 if(time>=32.6&&time<34.5)return {scale:2,x:825,y:525};
 if(time>=29&&time<41)return {scale:1.25,x:930,y:520};
 if(time>=22.5&&time<29)return {scale:1.65,x:1190,y:530};
 if(time>=17.7&&time<20.3)return {scale:2,x:760,y:465};
 if(time>=16.4&&time<22.5)return {scale:1.7,x:850,y:520};
 return {scale:1,x:960,y:450};
}
export function pilotEndingViewAt(time){
 if(!Number.isFinite(time))throw new TypeError('time must be finite');
 if(time<58.6)return {mode:'constraint',crop:[932,389,900,421.875]};
 if(time<61.7)return {mode:'context',scale:1,x:960,y:450};
 return {mode:'route',scale:1.4,x:540,y:450};
}
export function pilotCupAt(time){
 // Keep the cup down while replying; the raised cup at41 follows the intervening vignette.
 const lift=time>=41&&time<46?1-progress(time,41.4,.6):0;
 const center=[1200+80*lift,597-92*lift];
 return {center,grip:[center[0]+30,center[1]+1]};
}
// One attempted task, interrupted by a phone, followed by a missed paper catch.
export function pilotTaskAt(time){
 if(!Number.isFinite(time))throw new TypeError('time must be finite');
 const lift=progress(time,33.7,.6)*(1-progress(time,36.3,.7));
 const phoneCenter=pilotBlend([925,583],[815,490],lift);
 const phoneGrip=[phoneCenter[0]+22,phoneCenter[1]+15];
 const gripWeight=progress(time,33.1,.6)*(1-progress(time,37.1,.3));
 const writing=1-progress(time,32.6,.4);
 const spill=progress(time,37.4,1.2);
 const delivery=progress(time,35.6,1.2),deliveryX=1820-745*delivery;
 const pages=[0,1].map(i=>{const fall=Math.max(0,Math.min(1,time-37.4-i*.2)),k=fall*fall;return {center:pilotBlend([deliveryX+i*30,634-i*6],[1040+i*80,805],k),angle:(i===0?-.45:.6)*Math.sin(Math.PI*k),fallen:k===1};});
 const release=progress(time,37.3,.35),deliveryWrist=[deliveryX+34+600*release,646];
 return {phoneCenter,phoneGrip,gripWeight,writing,spill,pages,deliveryX,deliveryVisible:time>=35.6,deliveryWrist,deliveryHand:progress(time,35.6,.3)*(1-release)};
}
export function pilotActorAt(time,role,mode='study'){
 if(!Number.isFinite(time))throw new TypeError('time must be finite');
 if(!['youth','philosopher'].includes(role))throw new TypeError('unknown actor');
 let p;
 if(role==='philosopher'){
  p={hip:[1320,680],chest:[1320,550],head:[1310,465],feet:[[1185,830],[1260,830]],hands:[pilotCupAt(time).grip,[1370,708]],facing:-1,intent:'listen'};
  if(time>=14.5&&time<29){
   const attention=progress(time,15.4,.65)*(1-progress(time,21.7,.65));
   const reply=progress(time,22.9,.55),invite=progress(time,26.1,.65);
   p.chest[0]-=14*attention+14*reply;p.chest[1]+=5*attention+5*reply;
   p.head[0]-=18*attention+20*reply;p.head[1]+=8*attention+5*reply;
   p.hands[1]=pilotBlend(p.hands[1],[1145,510],invite);p.hands[1][1]-=55*Math.sin(Math.PI*invite);
   p.intent=invite>.2?'invite':reply>.1?'reply':'listen';
  }
  if(time>=41&&time<46){
   const respond=progress(time,44.5,.65);
   p.chest[0]-=12*respond;p.head[0]-=18*respond;p.head[1]+=5*respond;
   p.hands[1]=pilotBlend(p.hands[1],[1145,510],respond);p.hands[1][1]-=55*Math.sin(Math.PI*respond);
   p.gaze=time<42.2?pilotCupAt(time).center:[710,385];
   if(respond>.2)p.intent='explain';
  }
 }else if(mode==='burden'){
  const task=pilotTaskAt(time),notice=progress(time,32.6,.35)*(1-progress(time,35.5,.5));
  const miss=progress(time,37.35,.5),settle=progress(time,39.2,1.0);
  p={hip:pilotBlend(pilotBlend([690,640],[730,660],miss),[690,680],settle),
   chest:pilotBlend(pilotBlend([750,510],[850,540],miss),[750,550],settle),
   head:pilotBlend(pilotBlend([775+15*notice,425+6*notice],[880,455],miss),[770,475],settle),
   feet:[[590,830],[710,830]],hands:[[810,620],[825+40*progress(time,29,3.6),597+2*Math.cos((time-29)*9)*task.writing]],facing:1,intent:time<32.6?'work':'strain'};
  p.hands[1]=pilotBlend(p.hands[1],task.phoneGrip,task.gripWeight);
  p.hands[1]=pilotBlend(p.hands[1],[1005,615],miss);
  p.hands[1]=pilotBlend(p.hands[1],[835,615],settle);
  p.hip[0]+=15*task.gripWeight;p.chest[0]+=45*task.gripWeight;p.head[0]+=40*task.gripWeight;
  // The failed reach lands in a supported, specific reaction rather than another generic strain.
  p.hands[0]=pilotBlend(p.hands[0],[790,465],settle);p.hands[0][0]-=30*Math.sin(Math.PI*settle);p.head[1]+=10*settle;
  if(settle>.8)p.intent='defeated';
  p.gaze=time<32.6?p.hands[1]:time<35.5?task.phoneCenter:task.pages[0].center;
 }else{
  const lean=progress(time,14.5,1.2)*(1-progress(time,22,.8));
  const point=progress(time,15.2,.4)*(1-progress(time,17.5,.5))+.65*progress(time,20,.4)*(1-progress(time,21.4,.4));
  p={hip:pilotBlend([650,610],[690,640],lean),chest:pilotBlend([690,470],[745,510],lean),head:pilotBlend([710,385],[775,425],lean),feet:[[590,830],[710,830]],hands:[pilotBlend([665,630],[810,620],lean),pilotBlend([720,630],[820+50*point,570-80*point],lean)],facing:1,intent:lean>.3?'argue':'listen'};
  if(time>=14.5&&time<22.8){
   const claim=progress(time,17.7,.4)*(1-progress(time,19.7,.5));
   const release=1-progress(time,22.1,.65),prepare=progress(time,19.95,.18)*(1-progress(time,20.2,.18));
   const insist=progress(time,20.3,.45)*release,headLead=progress(time,20.22,.38)*release,handFollow=progress(time,20.45,.3)*release;
   p.chest[0]-=8*claim;p.head[0]-=12*claim;
   p.hands[1]=pilotBlend(p.hands[1],[790,565],claim);
   p.hip[0]+=18*insist-6*prepare;p.chest[0]+=26*insist-10*prepare;p.head[0]+=34*headLead-10*prepare;
   p.hands[1][0]+=30*handFollow-24*prepare;p.hands[1][1]+=-25*handFollow+15*prepare;
   if(claim>.3)p.intent='claim';if(insist>.3)p.intent='challenge';
  }
  const listening=progress(time,22,.8);
  if(time<29){
   p.hip=pilotBlend(p.hip,[675,640],listening);p.chest=pilotBlend(p.chest,[715,500],listening);p.head=pilotBlend(p.head,[740,420],listening);
   p.hands[0]=pilotBlend(p.hands[0],[810,620],listening);p.hands[1]=pilotBlend(p.hands[1],[755,640],listening);
   const withhold=progress(time,25.2,.35)*(1-progress(time,26.1,.5)),ready=progress(time,27.8,.6);
   p.chest[0]+=6*withhold+10*ready;p.head[0]+=12*withhold+14*ready;p.head[1]-=4*withhold;
   p.hands[1]=pilotBlend(p.hands[1],[805,560],withhold);p.hands[1]=pilotBlend(p.hands[1],[800,610],ready);
   if(listening>.9)p.intent=withhold>.2?'withhold':ready>.2?'ready':'listen';
  }
  const recoil=progress(time,43.1,.45)*(1-progress(time,45.2,.6));
  p.hip[0]-=12*recoil;p.chest[0]-=18*recoil;p.head[0]-=28*recoil;
  p.hands[0]=pilotBlend(p.hands[0],[650,600],recoil);p.hands[1]=pilotBlend(p.hands[1],[770,550],recoil);
  if(time>=42.7&&time<46){
   const check=progress(time,44.2,.8);p.hands[1]=pilotBlend(p.hands[1],[745,590],check);
   p.intent=recoil>.2?(check>.5?'skeptical':'defensive'):'listen';
  }
  p.gaze=[1290,470];
 }
 const normalSide=p.facing===1?-1:1;
 const shoulders=[-5,5].map(d=>[p.chest[0]+d,p.chest[1]]);
 const arms=shoulders.map((a,i)=>solveArm(a,p.hands[i],84,90,role==='philosopher'?-1:1));
 const legs=p.feet.map(f=>solveArm(p.hip,f,115,120,normalSide));
 return {pose:p,shoulders,arms,legs,toeTargets:legs.map(a=>[a.wrist[0]+p.facing*19,a.wrist[1]]),spineControl:[(p.hip[0]+p.chest[0])/2-16*p.facing,(p.hip[1]+p.chest[1])/2+8]};
}
export function pilotExitAt(time){
 const t=Math.max(56,Math.min(PILOT_DURATION,time)),travel=Math.max(0,t-60.2),phase=travel*Math.PI*2/.7;
 const lookback=progress(t,58.6,.4)*(1-progress(t,59.8,.4));
 const source=geometryAt(14.5),p=JSON.parse(JSON.stringify(source.pose));
 p.facing=lookback>.5?1:-1;p.intent=travel>0?'walk':lookback>.2?'consider':'pause';
 p.hip[1]=550+3*Math.sin(phase)**2;p.chest[1]+=30;p.head[1]+=30;p.head[0]+=35*lookback;
 if(lookback>.1)p.gaze=[895,537];
 const depthAt=u=>{const d=progress(Math.max(0,Math.min(4.3,u)),0,4.3);return {scale:1-.55*d,anchor:[190+5*d,740-170*d]};};
 const depth=depthAt(travel);
 p.feet=[0,1].map(i=>{
  const offset=i*.35,local=travel+offset,cycle=Math.floor(local/.7),fraction=local/.7-cycle;
  const start=cycle*.7-offset;
  const ground=u=>{const d=depthAt(u);return [d.anchor[0]+(i===0?-20:20)*d.scale,d.anchor[1]];};
  let world=ground(start);
  if(fraction>=.5){const k=progress(fraction,.5,.5);world=pilotBlend(world,ground(start+.7),k);world[1]-=18*depth.scale*Math.sin(Math.PI*k);}
  return [190+(world[0]-depth.anchor[0])/depth.scale,740+(world[1]-depth.anchor[1])/depth.scale];
 });
 p.hands=[[155+15*Math.sin(phase),570],[245-15*Math.sin(phase),570]];
 const shoulders=[-5,5].map(d=>[p.chest[0]+d,p.chest[1]]);
 const arms=shoulders.map((a,i)=>solveArm(a,p.hands[i],84,90,1));
 const legs=p.feet.map(f=>solveArm(p.hip,f,115,120,1));
 return {pose:p,shoulders,arms,legs,toeTargets:legs.map(a=>[a.wrist[0]-19,a.wrist[1]]),spineControl:[170,480],depth};
}


// The external event is shared exactly; only the authored character response differs.
export function pilotSharedEventAt(time){
 if(!Number.isFinite(time))throw new TypeError('time must be finite');
 return {bird:[-30+(time-46)*84,120],wing:9+5*Math.sin(time*6)};
}
export function pilotViewActorAt(time,role){
 if(!Number.isFinite(time))throw new TypeError('time must be finite');
 if(!['youth','philosopher'].includes(role))throw new TypeError('unknown actor');
 const notice=progress(time,48.7,.5),follow=progress(time,49.8,.7)*(1-progress(time,54.3,.7));
 const duck=progress(time,49,.28),peek=progress(time,51.6,.7),rise=progress(time,53.2,1.1);
 const startle=role==='youth'?duck*(1-.6*rise):0;
 const p={hip:pilotBlend([690,610],[680,680],startle),chest:pilotBlend([700,470],[680,550],startle),head:[710,385],feet:[[620,830],[760,830]],hands:[[690,630],[745,625]],facing:1,intent:'observe'};
 // The eyes locate the same panel-space event before the body reacts.
 const bird=pilotSharedEventAt(time).bird,target=[690+(bird[0]-240)/.66,830+(bird[1]-535)/.66];
 p.gaze=pilotBlend([p.head[0]+80,p.head[1]-35],target,notice);
 if(role==='youth'){
  const flinch=progress(time,48.9,.22)*(1-.55*rise),shield=progress(time,49.05,.24);
  p.head=pilotBlend(p.head,[690,465],flinch);p.head[0]+=12*peek;
  p.hands[0]=pilotBlend(p.hands[0],[650,410],shield);
  p.hands[0]=pilotBlend(p.hands[0],[665,455],rise);
  p.hands[1]=pilotBlend(p.hands[1],[730,410],shield);
  p.hands[1]=pilotBlend(p.hands[1],[765,535],peek);
  p.intent=duck<.2?'observe':peek<.2?'startle':'guarded';
 }else{
  const turn=progress(time,48.7,2);
  p.chest[0]-=8*notice;p.chest[1]-=6*notice;p.head[0]+=(-15+25*turn)*notice;p.head[1]-=15*notice;
  p.hands[1]=pilotBlend(p.hands[1],[810,395],follow);p.intent=follow>.2?'curious':'observe';
 }
 const shoulders=[-5,5].map(d=>[p.chest[0]+d,p.chest[1]]);
 const arms=shoulders.map((a,i)=>solveArm(a,p.hands[i],84,90,i===0?-1:1));
 const legs=p.feet.map(f=>solveArm(p.hip,f,115,120,-1));
 return {pose:p,shoulders,arms,legs,toeTargets:legs.map(a=>[a.wrist[0]+19,a.wrist[1]]),spineControl:[(p.hip[0]+p.chest[0])/2-16,(p.hip[1]+p.chest[1])/2+8]};
}

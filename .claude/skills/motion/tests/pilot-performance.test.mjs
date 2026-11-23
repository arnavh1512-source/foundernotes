import test from 'node:test';
import {progress} from '../assets/story-motion.mjs';
import assert from 'node:assert/strict';
import {PILOT_DURATION,PILOT_SHOTS,pilotShotAt,pilotCupAt,pilotActorAt,pilotExitAt,pilotTaskAt,pilotSharedEventAt,pilotViewActorAt,pilotRoomCameraAt,pilotEndingViewAt} from '../assets/pilot-performance.mjs';
const distance=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
test('pilot shots cover the measured take with no gaps',()=>{
 assert.equal(PILOT_SHOTS[0].start,0);assert.equal(PILOT_SHOTS.at(-1).end,PILOT_DURATION);
 PILOT_SHOTS.slice(1).forEach((s,i)=>assert.equal(s.start,PILOT_SHOTS[i].end));
 for(let f=0;f<1935;f++)assert.ok(pilotShotAt(f/30));
 assert.throws(()=>pilotShotAt(NaN),/finite/);
});
test('new performances preserve limbs, planted support and the actual cup handle',()=>{
 assert.equal(pilotCupAt(20).center[1]+23,620);
 assert.equal(pilotCupAt(42).center[1]+23,620);
 for(let f=0;f<=1935;f++){
  const t=f/30,shot=pilotShotAt(t);
  let actors=[];
  if(['study','cup'].includes(shot.name))actors=[pilotActorAt(t,'youth'),pilotActorAt(t,'philosopher')];
  if(shot.name==='burden')actors=[pilotActorAt(t,'youth','burden')];
  if(shot.name==='exit')actors=[pilotExitAt(t)];
  for(const g of actors){
   for(const [limbs,lengths]of [[g.arms,[84,90]],[g.legs,[115,120]]])for(const a of limbs){
    assert.equal(a.clamped,false,'unreachable pose '+t);
    assert.ok(Math.abs(distance(a.shoulder,a.elbow)-lengths[0])<1e-6);
    assert.ok(Math.abs(distance(a.elbow,a.wrist)-lengths[1])<1e-6);
   }
  }
  if(shot.name==='study'||(shot.name==='cup'&&t<=42.08))assert.ok(distance(actors[1].arms[0].wrist,pilotCupAt(t).grip)<1e-6);
  if(shot.name==='cup'&&t>=42.54)assert.ok(distance(actors[1].arms[0].wrist,pilotCupAt(t).grip)>60,'wrist releases the handle after set-down');
 }
});

test('the exit keeps stance feet planted after perspective projection',()=>{
 const ground=(t,i)=>{const g=pilotExitAt(t),p=g.legs[i].wrist;return [g.depth.anchor[0]+(p[0]-190)*g.depth.scale,g.depth.anchor[1]+(p[1]-740)*g.depth.scale];};
 for(const [a,b,i]of [[56.1,56.4,0],[58.7,59.9,1],[60.25,60.5,0],[60.6,60.8,1],[62.4,62.6,0]])assert.ok(distance(ground(a,i),ground(b,i))<1e-6);
});


test('the cup arm stays below the face throughout the set-down',()=>{
 for(let f=0;f<=30;f++){
  const g=pilotActorAt(41+f/30,'philosopher');
  assert.ok(g.arms[0].elbow[1]>=g.pose.head[1]+60,`elbow invades the face at ${41+f/30}`);
 }
});


test('the task interruption preserves phone grip, planted support and an unfinished consequence',()=>{
 for(let f=0;f<360;f++){
  const t=29+f/30,g=pilotActorAt(t,'youth','burden'),task=pilotTaskAt(t);
  assert.deepEqual(g.pose.feet,[[590,830],[710,830]]);
  if(t<=39.2)assert.deepEqual(g.pose.hands[0],[810,620]);
  if(t>=33.7&&t<=37.1)assert.ok(distance(g.arms[1].wrist,task.phoneGrip)<1e-6,'phone detached '+t);
 }
 for(const t of [29,30,31,32,32.6])assert.ok(Math.abs(pilotActorAt(t,'youth','burden').arms[1].wrist[0]-(825+40*progress(t,29,3.6)))<1e-6);
 assert.equal(pilotTaskAt(33.1).writing,0);
 assert.ok(pilotTaskAt(35.6).pages.every(p=>p.center[0]-52>1700),'incoming work must enter from outside the frame');
 assert.deepEqual(pilotTaskAt(37.1).phoneCenter,[925,583]);
 assert.ok(pilotTaskAt(29).phoneCenter[0]-20>868,'phone must leave the complete writing stroke visible');
 assert.ok(pilotTaskAt(40.9).pages.every(p=>p.fallen));
 assert.deepEqual(pilotTaskAt(40.5).pages,pilotTaskAt(40.9).pages);
});


test('conversation beats distinguish listening, withheld interruption and invitation',()=>{
 const young=t=>pilotActorAt(t,'youth'),mentor=t=>pilotActorAt(t,'philosopher');
 for(let f=0;f<435;f++){
  const t=14.5+f/30;
  assert.deepEqual(mentor(t).pose.hip,[1320,680]);
  assert.deepEqual(mentor(t).pose.feet,[[1185,830],[1260,830]]);
  assert.deepEqual(pilotCupAt(t).center,[1200,597]);
  if(t>=22.8)assert.deepEqual(young(t).pose.hands[0],[810,620]);
 }
 assert.equal(young(25.8).pose.intent,'withhold');assert.equal(young(27).pose.intent,'listen');
 assert.ok(distance(mentor(27).arms[1].wrist,pilotCupAt(27).center)>100,'invitation must clear the cup and steam');
 assert.equal(young(28.7).pose.intent,'ready');assert.equal(mentor(27).pose.intent,'invite');
 assert.ok(mentor(17).pose.head[0]<mentor(14.5).pose.head[0]-15);
 assert.ok(mentor(27).arms[1].wrist[0]<mentor(23).arms[1].wrist[0]-100);
 assert.ok(young(25.8).arms[1].wrist[1]<young(27).arms[1].wrist[1]-60);
});


test('paired views preserve the external event while reactions and planted supports differ',()=>{
 for(let f=0;f<=300;f++){
  const t=46+f/30;
  for(const role of ['youth','philosopher']){
   const g=pilotViewActorAt(t,role);assert.deepEqual(g.pose.feet,[[620,830],[760,830]]);
   for(const [limbs,lengths]of [[g.arms,[84,90]],[g.legs,[115,120]]])for(const a of limbs){
    assert.equal(a.clamped,false,role+' unreachable at '+t);
    assert.ok(Math.abs(distance(a.shoulder,a.elbow)-lengths[0])<1e-6);
    assert.ok(Math.abs(distance(a.elbow,a.wrist)-lengths[1])<1e-6);
   }
  }
  assert.equal(pilotSharedEventAt(t).bird[1],120);
 }
 assert.equal(pilotViewActorAt(50,'youth').pose.intent,'startle');
 assert.equal(pilotViewActorAt(51,'philosopher').pose.intent,'curious');
 assert.ok(pilotViewActorAt(50,'youth').pose.hip[1]>pilotViewActorAt(48,'youth').pose.hip[1]+50);
 assert.ok(pilotViewActorAt(51,'philosopher').pose.head[1]<pilotViewActorAt(48,'philosopher').pose.head[1]);
 assert.throws(()=>pilotSharedEventAt(NaN),/finite/);
});


test('the attempted catch reaches toward the paper and lands in a specific defeat pose',()=>{
 const before=pilotActorAt(37.3,'youth','burden'),reach=pilotActorAt(37.9,'youth','burden');
 assert.ok(reach.pose.chest[0]>before.pose.chest[0]+75,'whole torso must commit to the catch');
 assert.ok(reach.arms[1].wrist[0]>990,'catch cannot remain beside the phone');
 const page=pilotTaskAt(37.9).pages[0];
 assert.ok(Math.abs(page.center[0]-52-reach.arms[1].wrist[0])<30,'failed catch must approach the actual paper edge');
 assert.ok(page.center[1]>reach.arms[1].wrist[1]+30,'paper has already fallen below the late hand');
 const end=pilotActorAt(40.5,'youth','burden');
 assert.ok(distance(end.arms[0].wrist,end.pose.head)<35,'reaction hand must reach the forehead');
 assert.equal(end.pose.intent,'defeated');
 assert.deepEqual(end.arms[1].wrist,[835,615]);
});


test('challenge, rebuttal and attention have distinct supported intentions',()=>{
 const young=t=>pilotActorAt(t,'youth'),mentor=t=>pilotActorAt(t,'philosopher');
 assert.equal(young(18.8).pose.intent,'claim');assert.equal(young(21.3).pose.intent,'challenge');
 assert.ok(young(21.3).pose.chest[0]>young(18.8).pose.chest[0]+30);
 assert.equal(young(43.8).pose.intent,'defensive');assert.equal(young(44.9).pose.intent,'skeptical');
 assert.equal(mentor(45).pose.intent,'explain');
 assert.ok(distance(mentor(45.2).arms[1].wrist,pilotCupAt(45.2).center)>100);
 assert.deepEqual(mentor(45).pose.hip,[1320,680]);
 for(const t of [31,34.4,36.5,38.3]){
  const g=pilotActorAt(t,'youth','burden'),task=pilotTaskAt(t);
  assert.deepEqual(g.pose.gaze,t<32.6?g.pose.hands[1]:t<35.5?task.phoneCenter:task.pages[0].center);
 }
});

test('room framing and ending separate claim, reaction, unchanged lock and chosen route',()=>{
 assert.equal(pilotRoomCameraAt(18.8).scale,2);assert.equal(pilotRoomCameraAt(21.3).scale,1.7);
 assert.deepEqual(pilotRoomCameraAt(43.8),{scale:2.05,x:700,y:465});
 assert.equal(pilotRoomCameraAt(45).scale,1.6);
 assert.equal(pilotEndingViewAt(56).mode,'constraint');assert.equal(pilotEndingViewAt(57.35).mode,'context');
 const route=pilotEndingViewAt(64.4);
 const roomX=worldX=>160+(1.3*worldX+219)*1600/1920;
 assert.ok(route.x+960/route.scale<roomX(758),'the closing crop excludes the edge of the spent obstacle');
 assert.ok(route.x-960/route.scale<roomX(95)&&route.x+960/route.scale>roomX(295),'the complete arch stays in frame');
 assert.equal(pilotEndingViewAt(64.4).mode,'route');
 const [x,y,w,h]=pilotEndingViewAt(57).crop;
 assert.ok(x>=0&&y>=0&&x+w<=1920&&y+h<=1080);
 const lock=[(1.3*895+219-x)*1920/w,(1.3*537-71-y)*900/h];
 assert.ok(lock[0]>800&&lock[0]<1120&&lock[1]>350&&lock[1]<650,'actual closed lock stays central');
 assert.throws(()=>pilotRoomCameraAt(NaN),/finite/);assert.throws(()=>pilotEndingViewAt(NaN),/finite/);
});


test('close claim excludes mentor face fragments and explanation arm clears his face',()=>{
 const view=pilotRoomCameraAt(18.8),mentor=pilotActorAt(18.8,'philosopher');
 assert.ok(mentor.pose.head[0]-31>view.x+960/view.scale+10,'exclude the entire offscreen face');
 for(let f=0;f<90;f++){const t=43+f/30,g=pilotActorAt(t,'philosopher');
  assert.ok(distance(g.arms[1].elbow,g.pose.head)>75,'free elbow invades head '+t);
 }
});


test('the work is visibly supported until release and accelerates into its consequence',()=>{
 for(const t of [36.8,37,37.2]){const task=pilotTaskAt(t);
  assert.equal(task.pages[0].center[1]+12,task.deliveryWrist[1]);
  assert.ok(task.deliveryWrist[0]>=task.pages[0].center[0]&&task.deliveryWrist[0]<task.pages[0].center[0]+52);
  assert.equal(task.deliveryHand,1);
 }
 const a=pilotTaskAt(37.4).pages[0].center[1],b=pilotTaskAt(37.6).pages[0].center[1],c=pilotTaskAt(37.8).pages[0].center[1];
 assert.ok(c-b>2*(b-a),'the released page must gain downward speed');
 assert.equal(pilotTaskAt(37.7).deliveryHand,0);
 assert.deepEqual(pilotTaskAt(40.5).pages,pilotTaskAt(40.9).pages);
});

test('the ending shows a planted reconsideration before committed travel',()=>{
 const a=pilotExitAt(58.7),b=pilotExitAt(59.3),c=pilotExitAt(60.1),walk=pilotExitAt(61);
 assert.deepEqual(a.pose.feet,b.pose.feet);assert.deepEqual(b.pose.feet,c.pose.feet);
 assert.equal(b.pose.intent,'consider');assert.deepEqual(b.pose.gaze,[895,537]);assert.equal(b.pose.facing,1);
 assert.equal(c.depth.scale,1);assert.ok(walk.depth.scale<1);assert.equal(walk.pose.intent,'walk');
 assert.equal(walk.pose.facing,-1);assert.ok(Math.abs(pilotExitAt(64.5).depth.scale-.45)<1e-9);
});


test('shared-event attention tracks the actual panel bird and retains different consequences',()=>{
 for(const role of ['youth','philosopher'])for(const t of [49.3,50,52,54,55.9]){
  const g=pilotViewActorAt(t,role),bird=pilotSharedEventAt(t).bird;
  assert.ok(distance(g.pose.gaze,[690+(bird[0]-240)/.66,830+(bird[1]-535)/.66])<1e-6);
 }
 const early=pilotViewActorAt(48.98,'youth'),duck=pilotViewActorAt(50,'youth'),peek=pilotViewActorAt(52.5,'youth'),end=pilotViewActorAt(55.9,'youth');
 assert.ok(early.pose.head[1]>400,'head flinch leads the duck');
 assert.ok(early.pose.hip[1]<615,'body has not yet completed the reaction');
 assert.ok(peek.pose.hands[1][1]>duck.pose.hands[1][1]+100,'one hand lowers to expose a guarded check');
 assert.equal(end.pose.intent,'guarded');assert.ok(end.pose.hip[1]>635,'do not reset to the opening pose');
 assert.ok(end.pose.hands[0][1]<end.pose.head[1]+40,'one shielding hand remains up');
 const mentor=pilotViewActorAt(55.9,'philosopher');assert.ok(mentor.pose.hip[1]<end.pose.hip[1]-20);
});


test('the demand prepares, commits the body and lets the hand follow without losing its brace',()=>{
 const prepared=pilotActorAt(20.15,'youth'),leading=pilotActorAt(20.4,'youth'),arrived=pilotActorAt(20.9,'youth');
 assert.ok(prepared.pose.chest[0]<leading.pose.chest[0]);
 assert.ok(leading.pose.head[0]>prepared.pose.head[0]+15);
 assert.ok(arrived.pose.hands[1][0]>leading.pose.hands[1][0]+20);
 for(const t of [20.15,20.4,20.9])assert.deepEqual(pilotActorAt(t,'youth').pose.hands[0],[810,620]);
});


test('the seated mentor has forward knees, floor support and a reachable cup at mouth height',()=>{
 for(let f=0;f<435;f++){
  const g=pilotActorAt(14.5+f/30,'philosopher');
  for(const leg of g.legs){
   assert.ok(leg.elbow[0]<g.pose.hip[0]-100,'thighs must extend toward the desk');
   assert.ok(Math.abs(leg.elbow[1]-g.pose.hip[1])<45,'seated knees stay near chair height');
   assert.equal(leg.wrist[1],830,'feet must stay on the room floor');
  }
 }
 const drinking=pilotActorAt(41.3,'philosopher'),cup=pilotCupAt(41.3);
 assert.ok(Math.abs(cup.center[1]-20-(drinking.pose.head[1]+13))<10,'cup rim must meet the mouth, not the forehead');
 assert.ok(distance(drinking.arms[0].wrist,cup.grip)<1e-6);
});


test('the Youth close-up excludes the reblocked mentor knees and toes',()=>{
 for(const t of [18.8,43.8]){
 const view=pilotRoomCameraAt(t),right=view.x+960/view.scale,bottom=view.y+450/view.scale;
 const g=pilotActorAt(t,'philosopher');
 for(let i=0;i<2;i++)for(const [a,b] of [[g.legs[i].shoulder,g.legs[i].elbow],[g.legs[i].elbow,g.legs[i].wrist],[g.legs[i].wrist,g.toeTargets[i]]]){
  for(let j=0;j<=100;j++){const k=j/100,x=a[0]+(b[0]-a[0])*k,y=a[1]+(b[1]-a[1])*k;assert.ok(x>right+6||y>bottom+6,'mentor leg fragment enters the Youth close-up');}
 }
 }
});


test('the free invitation and explanation hand travels above the held cup',()=>{
 for(const [start,end] of [[26.1,26.75],[44.5,45.15]])for(let i=0;i<=100;i++){
  const t=start+(end-start)*i/100,g=pilotActorAt(t,'philosopher'),hand=g.arms[1].wrist,cup=pilotCupAt(t);
  assert.ok(distance(hand,cup.grip)>40,'free hand must not appear to take the cup handle '+t);
  assert.ok(distance(g.arms[1].elbow,g.pose.head)>75,'arc must not crowd the face '+t);
 }
});


test('mentor explanation begins on the return shot rather than intruding into the Youth close-up',()=>{
 for(const t of [43.9,44.1,44.26,44.49]){
  const g=pilotActorAt(t,'philosopher'),view=pilotRoomCameraAt(t);
  assert.deepEqual(g.pose.hands[1],[1370,708]);
  assert.ok(g.pose.hands[1][0]>view.x+960/view.scale+20);
 }
 assert.equal(pilotRoomCameraAt(44.5).scale,1.6);
 assert.equal(pilotActorAt(45.2,'philosopher').pose.intent,'explain');
});

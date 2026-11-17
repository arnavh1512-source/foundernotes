import test from 'node:test';
import {progress} from '../assets/story-motion.mjs';
import assert from 'node:assert/strict';
import {PILOT_DURATION,PILOT_SHOTS,pilotShotAt,pilotCupAt,pilotActorAt,pilotExitAt,pilotTaskAt} from '../assets/pilot-performance.mjs';
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
  if(['study','cup'].includes(shot.name))assert.ok(distance(actors[1].arms[0].wrist,pilotCupAt(t).grip)<1e-6);
 }
});

test('the exit keeps stance feet planted after perspective projection',()=>{
 const ground=(t,i)=>{const g=pilotExitAt(t),p=g.legs[i].wrist;return [g.depth.anchor[0]+(p[0]-190)*g.depth.scale,g.depth.anchor[1]+(p[1]-740)*g.depth.scale];};
 for(const [a,b,i]of [[56.1,56.4,0],[56.65,56.9,1],[60.45,60.8,0]])assert.ok(distance(ground(a,i),ground(b,i))<1e-6);
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
  assert.deepEqual(g.pose.hands[0],[810,620]);
  if(t>=33.7&&t<=37.1)assert.ok(distance(g.arms[1].wrist,task.phoneGrip)<1e-6,'phone detached '+t);
 }
 for(const t of [29,30,31,32,32.6])assert.ok(Math.abs(pilotActorAt(t,'youth','burden').arms[1].wrist[0]-(825+40*progress(t,29,3.6)))<1e-6);
 assert.equal(pilotTaskAt(33.1).writing,0);
 assert.ok(pilotTaskAt(35.6).pages.every(p=>p.center[0]-52>1700),'incoming work must enter from outside the frame');
 assert.deepEqual(pilotTaskAt(37.1).phoneCenter,[865,583]);
 assert.ok(pilotTaskAt(40.9).pages.every(p=>p.fallen));
 assert.deepEqual(pilotTaskAt(40.5).pages,pilotTaskAt(40.9).pages);
});

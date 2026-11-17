import test from 'node:test';
import assert from 'node:assert/strict';
import {PILOT_DURATION,PILOT_SHOTS,pilotShotAt,pilotCupAt,pilotActorAt,pilotExitAt} from '../assets/pilot-performance.mjs';
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


import test from 'node:test';
import assert from 'node:assert/strict';
import {geometryAt,poseAt,DURATION} from '../assets/stick-performance.mjs';
const distance=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
test('whole-body pose track preserves limbs, grips and planted support',()=>{
 for(let f=0;f<=Math.round(DURATION*30);f++){
  const g=geometryAt(f/30);
  for(const [limbs,lengths] of [[g.arms,[84,90]],[g.legs,[115,120]]]){
   for(const a of limbs){
    assert.equal(a.clamped,false);
    assert.ok(Math.abs(distance(a.shoulder,a.elbow)-lengths[0])<1e-6);
    assert.ok(Math.abs(distance(a.elbow,a.wrist)-lengths[1])<1e-6);
   }
  }
  if(g.gripping)g.arms.forEach((a,i)=>assert.ok(distance(a.wrist,g.handTargets[i])<1e-6));
  if(g.pose.time<=3.8)assert.equal(g.pose.feet[0][0],590);
  assert.deepEqual(geometryAt(f/30),g);
 }
});
test('time boundaries clamp and invalid time is rejected',()=>{
 assert.deepEqual(poseAt(-1),poseAt(0));
 assert.deepEqual(poseAt(999),poseAt(DURATION));
 assert.throws(()=>geometryAt(NaN),/finite/);
});

test('recovery holds contacts and stair steps alternate support feet',()=>{
 for(let f=0;f<=315;f++){
  const t=f/30,p=poseAt(t);
  if(t>=4.15&&t<=8.3)assert.deepEqual(p.feet[0],[470,830]);
  if(t>=4.15&&t<=7)assert.deepEqual(p.feet[1],[650,830]);
  if(t>=8.3&&t<=9.4)assert.deepEqual(p.feet[1],[580,830]);
  if(t>=9.4)assert.deepEqual(p.feet[0],[420,800]);
 }
 assert.ok(poseAt(7.65).feet[1][1]<800);
 assert.ok(poseAt(8.85).feet[0][1]<800);
 assert.ok(poseAt(9.95).feet[1][1]<770);
 assert.deepEqual(poseAt(DURATION).feet,[[420,800],[350,770]]);
});

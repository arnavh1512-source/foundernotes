import test from 'node:test';
import assert from 'node:assert/strict';
import {geometryAt,poseAt,cameraAt,DURATION} from '../assets/stick-performance.mjs';
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
 for(let f=0;f<=Math.round(DURATION*30);f++){
  const t=f/30,p=poseAt(t);
  if(t>=4.15&&t<=8.3)assert.deepEqual(p.feet[0],[470,830]);
  if(t>=4.15&&t<=7)assert.deepEqual(p.feet[1],[650,830]);
  if(t>=8.3&&t<=9.4)assert.deepEqual(p.feet[1],[580,830]);
  if(t>=9.4&&t<=10.5)assert.deepEqual(p.feet[0],[420,800]);
 }
 assert.ok(poseAt(7.65).feet[1][1]<800);
 assert.ok(poseAt(8.85).feet[0][1]<800);
 assert.ok(poseAt(9.95).feet[1][1]<770);
 assert.deepEqual(poseAt(10.5).feet,[[420,800],[350,770]]);
});

test('neutral silhouette and facing turn avoid crossed knees and folded rest arms',()=>{
 const rest=geometryAt(0);
 assert.ok(rest.legs[0].elbow[0]<rest.legs[1].elbow[0]);
 rest.arms.forEach(a=>assert.ok(distance(a.shoulder,a.wrist)>150));
 const before=geometryAt(6.4-.0001),after=geometryAt(6.4);
 before.legs.forEach((a,i)=>assert.ok(distance(a.elbow,after.legs[i].elbow)<1));
});
test('the selected route reaches the arch with alternating supports',()=>{
 for(let f=0;f<=Math.round(DURATION*30);f++){
  const t=f/30,g=geometryAt(t),p=g.pose;
  g.legs.forEach(a=>assert.ok(a.elbow[1]<=830));
  if(t>=10.5&&t<=11.4)assert.deepEqual(p.feet[1],[350,770]);
  if(t>=11.4&&t<=12.3)assert.deepEqual(p.feet[0],[280,740]);
  if(t>=12.3)assert.deepEqual(p.feet[1],[210,740]);
  if(t>=13.3)assert.deepEqual(p.feet[0],[170,740]);
 }
 assert.deepEqual(poseAt(DURATION).feet,[[170,740],[210,740]]);
});

test('acting separates a delayed reach, accelerating fall and continuous stair travel',()=>{
 assert.deepEqual(poseAt(.2).hands,poseAt(0).hands);
 assert.notDeepEqual(poseAt(.2).head,poseAt(0).head);
 assert.ok(poseAt(2.78).hip[0]>poseAt(2.5).hip[0]);
 const early=distance(poseAt(3.85).hip,poseAt(3.8).hip);
 const late=distance(poseAt(4.15).hip,poseAt(4.1).hip);
 assert.ok(late>early*5);
 assert.deepEqual(poseAt(6).head,poseAt(5.8).head);
 assert.deepEqual(poseAt(6.2).head,poseAt(6.3).head);
 for(const t of [9.4,10.5,11.4,12.3]){
  assert.ok(distance(poseAt(t-.001).hip,poseAt(t).hip)/.001>20);
  assert.ok(distance(poseAt(t).hip,poseAt(t+.001).hip)/.001>20);
 }
});

test('feet turn toward the chosen route without changing foot length',()=>{
 for(let f=0;f<=Math.round(DURATION*30);f++){
  const g=geometryAt(f/30);
  g.legs.forEach((a,i)=>assert.ok(Math.abs(distance(a.wrist,g.toeTargets[i])-19)<1e-6));
 }
 assert.ok(geometryAt(0).toeTargets[0][0]>geometryAt(0).legs[0].wrist[0]);
 assert.ok(geometryAt(8).toeTargets[0][0]<geometryAt(8).legs[0].wrist[0]);
});

test('the route is revealed after reassessment while the complete figure stays in frame',()=>{
 const project=(m,p)=>[m[0]*p[0]+m[2]*p[1]+m[4],m[1]*p[0]+m[3]*p[1]+m[5]];
 assert.ok(project(cameraAt(0).matrix,[295,500])[0]<0);
 assert.deepEqual(cameraAt(0),cameraAt(6.2));
 assert.ok(project(cameraAt(7.2).matrix,[95,500])[0]>0);
 for(let f=0;f<=Math.round(DURATION*30);f++){
  const t=f/30,g=geometryAt(t),m=cameraAt(t).matrix;
  const points=[g.pose.hip,g.pose.chest,...g.pose.feet,...g.toeTargets,
   [g.pose.head[0]-34,g.pose.head[1]-34],[g.pose.head[0]+34,g.pose.head[1]+34],
   ...g.arms.flatMap(a=>[a.shoulder,a.elbow,a.wrist]),...g.legs.map(a=>a.elbow)];
  for(const p of points){const [x,y]=project(m,p);assert.ok(x>=12&&x<=1908&&y>=12&&y<=1068,`clipped pose at ${t}`);}
  assert.deepEqual(cameraAt(t),cameraAt(t));
 }
 assert.deepEqual(cameraAt(-1),cameraAt(0));
 assert.deepEqual(cameraAt(999),cameraAt(DURATION));
 assert.throws(()=>cameraAt(NaN),/finite/);
});


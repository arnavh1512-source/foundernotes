import test from 'node:test';
import assert from 'node:assert/strict';
import {geometryAt,poseAt,cameraAt,depthAt,shotAt,faceAt,shakeAt,IMPACTS,SOUND_EVENTS,SHOTS,DURATION,HEAD_R} from '../assets/stick-performance.mjs';
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
  if(g.pose.time>=.6&&g.pose.time<=3.8)assert.equal(g.pose.feet[0][0],590);
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
  if(t>=5.45&&t<=7.6)assert.deepEqual(p.feet[0],[470,830]);
  if(t>=5.45&&t<=7)assert.deepEqual(p.feet[1],[650,830]);
  if(t>=4.35&&t<=5.1)assert.deepEqual(p.feet,[[680,825],[720,800]]);
  if(t>=7.6&&t<=8.2)assert.deepEqual(p.feet[1],[580,830]);
  if(t>=8.2&&t<=8.8)assert.deepEqual(p.feet[0],[420,800]);
 }
 assert.ok(poseAt(7.3).feet[1][1]<800);
 assert.ok(poseAt(7.9).feet[0][1]<800);
 assert.ok(poseAt(8.5).feet[1][1]<770);
 assert.deepEqual(poseAt(8.8).feet,[[420,800],[350,770]]);
});

test('neutral silhouette and facing turn avoid crossed knees and folded rest arms',()=>{
 const rest=geometryAt(1.0);
 assert.ok(rest.legs[0].elbow[0]<rest.legs[1].elbow[0]);
 rest.arms.forEach(a=>assert.ok(distance(a.shoulder,a.wrist)>150));
 const before=geometryAt(6.4-.0001),after=geometryAt(6.4);
 before.legs.forEach((a,i)=>assert.ok(distance(a.elbow,after.legs[i].elbow)<1));
});
test('the selected route reaches the arch with alternating supports',()=>{
 for(let f=0;f<=Math.round(DURATION*30);f++){
  const t=f/30,g=geometryAt(t),p=g.pose;
  g.legs.forEach(a=>assert.ok(a.elbow[1]<=830));
  if(t>=8.8&&t<=9.4)assert.deepEqual(p.feet[1],[350,770]);
  if(t>=9.4&&t<=10)assert.deepEqual(p.feet[0],[280,740]);
  if(t>=10&&t<=13.8)assert.deepEqual(p.feet[1],[210,740]);
  if(t>=10.6)assert.deepEqual(p.feet[0],[170,740]);
 }
 assert.deepEqual(poseAt(DURATION).feet,[[170,740],[210,740]]);
});

test('acting separates a delayed reach, accelerating fall and continuous stair travel',()=>{
 assert.deepEqual(poseAt(1.04).hands,poseAt(1.0).hands);
 assert.ok(distance(poseAt(.3).hip,poseAt(0).hip)>60,'enters walking');
 assert.ok(poseAt(.15).feet[0][1]<800&&poseAt(.45).feet[1][1]<800,'strides lift alternate feet');
 assert.ok(poseAt(2.78).hip[0]>poseAt(2.5).hip[0]);
 const early=distance(poseAt(3.85).hip,poseAt(3.8).hip);
 const late=distance(poseAt(4.3).hip,poseAt(4.25).hip);
 assert.ok(late>early*5);
 assert.deepEqual(poseAt(6).head,poseAt(5.8).head);
 assert.deepEqual(poseAt(6.2).head,poseAt(6.3).head);
 for(const t of [8.2,8.8,9.4,10]){
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
 assert.deepEqual(cameraAt(0).matrix,cameraAt(6.2).matrix);
 assert.ok(project(cameraAt(7.2).matrix,[95,500])[0]>0);
 for(let f=0;f<=Math.round(DURATION*30);f++){
  const t=f/30,g=geometryAt(t),m=cameraAt(t).matrix;
  const points=[g.pose.hip,g.pose.chest,...g.pose.feet,...g.toeTargets,
   [g.head[0]-HEAD_R-8,g.head[1]-HEAD_R-8],[g.head[0]+HEAD_R+8,g.head[1]+HEAD_R+8],
   ...g.arms.flatMap(a=>[a.shoulder,a.elbow,a.wrist]),...g.legs.map(a=>a.elbow)];
  if(cameraAt(t).kind==='full')for(const p of points){const [x,y]=project(m,p);assert.ok(x>=12&&x<=1908&&y>=12&&y<=1068,`clipped pose at ${t}`);}
  assert.deepEqual(cameraAt(t),cameraAt(t));
 }
 assert.deepEqual(cameraAt(-1),cameraAt(0));
 assert.deepEqual(cameraAt(999),cameraAt(DURATION));
 assert.throws(()=>cameraAt(NaN),/finite/);
});

test('arrival pays off: look back at the locked gate, release, then recede into the arch',()=>{
 const facing=t=>poseAt(t).head[0]-poseAt(t).chest[0];
 assert.ok(facing(10.6)<0);
 assert.ok(facing(12)>25);
 assert.ok(facing(13.8)<0);
 const jamb=geometryAt(12).arms[1].wrist;
 assert.ok(jamb[0]>=262&&jamb[0]<=282&&jamb[1]>=330&&jamb[1]<=740,'hand rests on the arch frame');
 assert.ok(poseAt(13.4).chest[1]>poseAt(12).chest[1]+12);
 assert.ok(poseAt(13.4).head[1]>poseAt(12).head[1]+12);
 assert.equal(depthAt(13.8),1);
 assert.ok(depthAt(DURATION)<.6);
 assert.ok(cameraAt(11.5).push===1&&cameraAt(10.6).push===0);
});

test('no stretch after the reveal stays visually still for 2 s',()=>{
 const points=t=>{const g=geometryAt(t),d=depthAt(t);
  return [g.pose.head,...g.arms.map(a=>a.wrist),...g.pose.feet].map(([x,y])=>[x*d,y*d]);};
 for(let t=7;t+2<=DURATION;t+=.25){
  let moved=0;
  for(let u=t;u<t+2;u+=1/30){const a=points(u),b=points(u+1/30);moved=Math.max(moved,...a.map((p,i)=>distance(p,b[i])*60));}
  const travel=Math.max(...points(t).map((p,i)=>distance(p,points(t+2)[i])));
  assert.ok(travel>12||moved>40,`still from ${t.toFixed(2)} s`);
 }
});

test('coverage cuts on action and frames what each beat needs',()=>{
 const project=(m,p)=>[m[0]*p[0]+m[2]*p[1]+m[4],m[1]*p[0]+m[3]*p[1]+m[5]];
 const inside=(t,p)=>{const [x,y]=project(cameraAt(t).matrix,p);return x>=0&&x<=1920&&y>=0&&y<=1080;};
 assert.ok(SHOTS.length>=7);
 for(let i=1;i<SHOTS.length;i++)assert.ok(SHOTS[i].start-SHOTS[i-1].start>=.5,'no flash cuts');
 assert.ok(Math.max(...SHOTS.map((s,i)=>(SHOTS[i+1]?.start??DURATION)-s.start))<=4.4);
 for(let t=2.9;t<3.8;t+=1/30){const g=geometryAt(t);g.handTargets.forEach(h=>assert.ok(inside(t,h)));assert.ok(inside(t,[895,514]));}
 for(let t=11.5;t<12.4;t+=1/30){const h=geometryAt(t).head;assert.ok(inside(t,[h[0]-HEAD_R,h[1]-HEAD_R])&&inside(t,[h[0]+HEAD_R,h[1]+HEAD_R]));}
 for(let t=12.4;t<13;t+=1/30){assert.ok(inside(t,[874,514])&&inside(t,[917,560]));assert.ok(Math.abs(geometryAt(t).gateOffset)<1e-9);}
 assert.equal(shotAt(3.8).name,'medium');
 for(let t=0;t<6.2;t+=1/30){assert.ok(!inside(t,[195,330]),`arch visible before reveal at ${t}`);}
});

test('face expression follows each acting beat and stays in drawable ranges',()=>{
 for(let f=0;f<=Math.round(DURATION*30);f++){
  const e=faceAt(f/30);
  assert.ok(e.eye>=0&&e.eye<=1.3&&Math.abs(e.brow)<=1&&Math.abs(e.smile)<=1&&e.open>=0&&e.open<=1);
  assert.deepEqual(faceAt(f/30),e);
 }
 const at=t=>faceAt(t);
 assert.ok(at(3).eye<.3&&at(3).brow>.8,'strain squeezes eyes and lowers brows');
 assert.ok(at(4.2).eye>1.1&&at(4.2).open>.5,'slip reads as shock');
 assert.ok(at(5.3).smile<-.5,'frustration after the fall');
 assert.ok(at(4.55).eye<.2&&at(4.55).open>.3,'impact reads as pain');
 assert.ok(at(6.6).lift>.8,'brows rise on noticing');
 assert.ok(at(13.6).smile>.6,'relief at the end');
 assert.ok(at(.9).eye<.1&&at(1.05).eye>.8,'a quick blink, not a long close');
 assert.throws(()=>faceAt(NaN),/finite/);
});

test('the failure is a full-body event: airborne, rotated, impact, and the gate springs back',()=>{
 const tilt=t=>{const p=poseAt(t);return Math.atan2(p.chest[0]-p.hip[0],p.hip[1]-p.chest[1])*180/Math.PI;};
 assert.ok(tilt(4.2)<-40,'spine tips well back while airborne');
 const air=poseAt(4.2);assert.ok(air.feet.every(f=>f[1]<760),'both feet leave the floor');
 assert.ok(poseAt(4.42).chest[1]>poseAt(4.35).chest[1],'impact squashes the torso');
 assert.ok(poseAt(4.55).chest[1]<poseAt(4.42).chest[1],'then bounces');
 assert.ok(geometryAt(5.1).arms[1].wrist[1]>800,'fist reaches the floor on the slam');
 const v=t=>distance(poseAt(t).hip,poseAt(t+1/30).hip)*30;
 assert.ok(v(4.3)>v(4.0)*1.5,'the fall accelerates into impact');
 let peak=0;for(let u=3.95;u<4.3;u+=1/30)peak=Math.max(peak,Math.abs(geometryAt(u).gateOffset));
 assert.ok(peak>8,'gate visibly springs back');
 assert.ok(Math.abs(geometryAt(5.5).gateOffset)<1,'and settles');
});

test('proportions: big head on the shoulders, not a stick insect',()=>{
 for(const t of [0,3,6.4,10.6,14]){
  const g=geometryAt(t);
  assert.ok(Math.abs(distance(g.head,g.pose.chest)-(HEAD_R+4))<1e-6,'head sits on the chest with no neck');
  const top=g.head[1]-HEAD_R, feet=Math.max(...g.pose.feet.map(f=>f[1]));
  if(t===0)assert.ok((2*HEAD_R)/(feet-top)>1/5.5,'head is at least ~1/5.5 of standing height');
 }
});

test('motion energy: heaves, springy head, step weight and impact reactions',()=>{
 // two distinct heaves in the strain
 const xs=[];for(let t=2.9;t<3.8;t+=1/60)xs.push(poseAt(t).chest[0]);
 let peaks=0;for(let i=1;i<xs.length-1;i++)if(xs[i]<xs[i-1]&&xs[i]<=xs[i+1]&&xs[i]<poseAt(2.9).chest[0]-8)peaks++;
 assert.ok(peaks>=2,'at least two heaves');
 // head lags the spine then overshoots after the head turn
 const ang=t=>{const g=geometryAt(t);return Math.atan2(g.head[0]-g.pose.chest[0],g.pose.chest[1]-g.head[1]);};
 const target=t=>{const p=poseAt(t);return Math.atan2(p.head[0]-p.chest[0],p.chest[1]-p.head[1]);};
 let lag=0,over=0;for(let t=4.0;t<4.6;t+=1/60){const d=ang(t)-target(t);lag=Math.max(lag,Math.abs(d));}
 for(let t=6.4;t<7.0;t+=1/60)over=Math.max(over,Math.abs(ang(t)-target(t)));
 assert.ok(lag>.12,'head whips behind the body in the fall');
 assert.ok(over>.02,'head overshoots and settles after the turn');
 assert.ok(Math.abs(ang(2.0)-target(2.0))<.05,'head settles on holds');
 // weight lands on stair plants
 assert.ok(poseAt(8.31).hip[1]>poseAt(8.2).hip[1]+6||poseAt(8.31).hip[1]-poseAt(8.2).hip[1]>-30,'plant dips the hips');
 // impacts shake briefly, then stop
 for(const m of IMPACTS){assert.ok(Math.hypot(...shakeAt(m.t+.02))>1);assert.deepEqual(shakeAt(m.t+.3),[0,0]);}
 assert.deepEqual(shakeAt(2),[0,0]);
});

test('sound events sit on the animation contacts they belong to',()=>{
 const at=(type,t)=>SOUND_EVENTS.some(e=>e.type===type&&Math.abs(e.t-t)<1/30);
 for(const m of IMPACTS)assert.ok(at(m.shake>6?'thud':'slam',m.t),`impact sound at ${m.t}`);
 for(const plant of [8.2,8.8,9.4,10,10.6])assert.ok(at('step',plant),`stair step at ${plant}`);
 assert.ok(at('clank',1.2),'grip contact');assert.ok(at('twang',3.95),'grip snaps');
 for(const e of SOUND_EVENTS){assert.ok(e.t>=0&&e.t<DURATION&&e.gain>0&&e.gain<=1);}
 const action=SOUND_EVENTS.filter(e=>e.t<10.7).length/10.7;
 assert.ok(action>1.5&&action<3.5,`about 2 hits per second during action (benchmark AvA 2.4/s), got ${action.toFixed(2)}`);
});


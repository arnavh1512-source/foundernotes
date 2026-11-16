import {test} from 'node:test';
import assert from 'node:assert/strict';
import {progress, solveArm, gripTransform, layerMatrix, shotAt, wordCue} from '../assets/story-motion.mjs';
const distance = (a,b) => Math.hypot(a[0]-b[0],a[1]-b[1]);
test('arm keeps both bone lengths through a reach, including unreachable and coincident targets', () => {
  for (const target of [[100,110],[900,0],[0,0],[0,90],[-130,-20]]) for (const bend of [-1,1]) {
    const a=solveArm([0,0],target,100,80,bend);
    assert.ok(Math.abs(distance(a.shoulder,a.elbow)-100)<1e-6);
    assert.ok(Math.abs(distance(a.elbow,a.wrist)-80)<1e-6);
  }
  assert.equal(solveArm([0,0],[900,0],100,80).clamped,true);
});
test('held prop follows actual wrist, not an unreachable requested target', () => {
  const a=solveArm([0,0],[900,0],100,80);
  assert.match(gripTransform(a,45),new RegExp(`^translate\\(${a.wrist[0]} ${a.wrist[1]}\\)`));
  assert.throws(()=>solveArm([0,0],[1,2],0,80));
  assert.throws(()=>solveArm([NaN,0],[1,2],100,80));
});
test('camera moves foreground more than the far plane', () => {
  const c={x:100,y:0,zoom:1,roll:0};
  assert.equal(layerMatrix(c,0,1920,1080)[4],0);
  assert.equal(layerMatrix(c,1,1920,1080)[4],-100);
  assert.equal(layerMatrix(c,1.5,1920,1080)[4],-150);
  assert.throws(()=>layerMatrix({zoom:-1},1,1920,1080));
});
test('cut boundaries select exactly one shot, including final time and lead-in', () => {
  assert.equal(shotAt([0,2,5],2).index,1);
  assert.equal(shotAt([0,2,5],5).index,1);
  assert.equal(shotAt([0,2,5],-1).local,0);
  assert.throws(()=>shotAt([0,2,2],1));
});
test('word cues disambiguate repeated words and retain estimated provenance', () => {
  const words=[{word:'Now,',start:.2,end:.4},{word:'now',start:2,end:2.4}];
  assert.equal(wordCue(words,'NOW',{source:'asr',occurrence:2}).time,2);
  assert.equal(wordCue(words,'now',{source:'estimated'}).estimated,true);
  assert.throws(()=>wordCue(words,'missing',{source:'asr'}));
  assert.throws(()=>wordCue(words,'now'));
});
test('sampling an earlier time after a later time has no accumulated state', () => {
  const pose=t=>solveArm([0,0],[100+50*progress(t,0,2),80],100,100);
  const first=pose(.7);pose(2);assert.deepEqual(pose(.7),first);
});

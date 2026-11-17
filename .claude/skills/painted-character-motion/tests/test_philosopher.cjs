const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const context={window:{}};vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(__dirname,'../engine.js'),'utf8'),context);
let pilotPath=path.join(__dirname,'../productions/philosopher/pilot.js');
if(fs.existsSync(pilotPath))vm.runInContext(fs.readFileSync(pilotPath,'utf8'),context);
const pilot=context.window.FNPhilosopher;
test('75 second pilot covers every cut and final time',()=>{
 assert.ok(pilot,'philosopher pilot is missing');
 for(let t=0;t<=75;t+=.5){const shot=pilot.shotAt(t);assert.ok(shot.id);assert.ok(shot.local>=0);}
 assert.equal(pilot.shotAt(75).id,'perspectives');
 assert.equal(pilot.shotAt(47).id,'cup');
});
test('cup contact reaches the table and stays there after release',()=>{
 assert.ok(pilot);
 const contact=pilot.cupPose(3.2),released=pilot.cupPose(5.5);
 assert.equal(contact.y,740);assert.equal(released.y,740);assert.equal(contact.x,released.x);
 assert.equal(pilot.cupPose(2).held,true);assert.equal(released.held,false);
});
test('frames are deterministic, finite and distinct across meaningful action',()=>{
 assert.ok(pilot);
 const a=pilot.render(16);pilot.render(61);assert.equal(pilot.render(16),a);
 assert.notEqual(pilot.render(15),pilot.render(17));
 for(let t of [0,6,14,21,29,39,47,50.2,54,62,68,74.99]){
  let svg=pilot.render(t);assert.match(svg,/<svg/);assert.doesNotMatch(svg,/NaN|Infinity|undefined/);
 }
});
test('preview explicitly identifies missing narration',()=>{
 assert.ok(pilot);assert.match(pilot.render(20),/VISUAL DRAFT/);assert.match(pilot.render(20),/dialogue not recorded/);
});

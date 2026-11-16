const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const {test} = require('node:test');
const sandbox = {window:{}};
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(path.join(__dirname,'../engine.js'),'utf8'),sandbox);
const kit = sandbox.window.FNPaintedMotion;
test('exports landscape frame specs',()=>{assert.equal(kit.WIDTH,1920);assert.equal(kit.HEIGHT,1080);});
test('short scenes are valid and timed',()=>{assert.equal(kit.validate([{id:'gate',duration:2},{id:'study',duration:3}]),5);});
test('reject unsupported shots and negative timing',()=>{assert.throws(()=>kit.validate([{id:'unknown',duration:4}]));assert.throws(()=>kit.validate([{id:'study',duration:-1}]));});
test('same time yields exactly same SVG (including procedural details)',()=>{
  const a=kit.draw(kit.DEFAULT_BEATS[0],2,4.2,2);const b=kit.draw(kit.DEFAULT_BEATS[0],2,4.2,2);
  assert.equal(a,b);assert.match(a,/fn-night/);
});
test('caption text is escaped for SVG safety',()=>{
  const a=kit.draw({id:'study',duration:2,speaker:'A < B',text:'Hello & <script>alert(1)<\/script>'},0.5,2,1);
  assert.match(a,/A &lt; B/);assert.doesNotMatch(a,/<script>/);assert.match(a,/&amp;/);
});
test('props are attached to hand-relative coordinate group',()=>{
  const markup=kit.character({x:100,y:200,t:1,prop:'pencil',right:[10,-5]});
  assert.match(markup,/translate\(10 -5\)/);assert.match(markup,/scale\(1\)/);
});
test('mount uses same input and time for equal frames',()=>{
  const svg={tagName:'svg',setAttribute(){},innerHTML:''};const film=kit.mount(svg);
  film.seek(3);const one=svg.innerHTML;film.seek(3);assert.equal(svg.innerHTML,one);
  assert.ok(film.duration>20);
});
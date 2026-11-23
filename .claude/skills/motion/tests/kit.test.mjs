// Pure helpers of the Ink & Gold scene kit (podcast-scout-skill/assets/ink-gold-kit), loaded without a DOM.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const sandbox = {window: {}, console};
vm.createContext(sandbox);
for (const f of ['kit.js', 'kit-loop.js']) vm.runInContext(readFileSync(new URL(`../../podcast-scout-skill/assets/ink-gold-kit/${f}`, import.meta.url), 'utf8'), sandbox);
const K = sandbox.window.K;

test('K.keys is continuous at keys when a pose leaves out fields the previous one set', () => {
  const keys = [[0, K.POSE.stand], [1, K.POSE.think], [2, K.POSE.point], [3, {shF: 10}, 'line']];
  for (const tk of [1, 2, 3]) {
    const a = K.keys(tk - 1e-6, keys), b = K.keys(tk + 1e-6, keys);
    for (const f of ['elB', 'look', 'lookY', 'shF', 'elF']) assert.ok(Math.abs((a[f] ?? 0) - (b[f] ?? 0)) < 1e-3, `${f} jumps at ${tk}`);
  }
  assert.equal(K.keys(2, keys).elB, K.POSE.think.elB);   // think's back arm carries through point
  assert.equal(K.keys(9, keys).shF, 10);
});
test('K.lag rests on the driver value and K.anticipate settles at 1', () => {
  const driver = (t) => K.eo(K.prog(t, 0, 1));
  for (const i of [1, 2, 3]) assert.equal(K.lag(driver, 5, 3, i), 1);
  assert.equal(K.anticipate(2, 0.5, 0.6), 1);
  assert.ok(Math.abs(K.anticipate(0.5 - 1e-9, 0.5, 0.6) - K.anticipate(0.5, 0.5, 0.6)) < 1e-6);
});
test('K.word finds cue times and throws on a miss unless a fallback is given', () => {
  sandbox.window.TIMING = {scenes: {sc1: {start: 10, end: 20}}, seg: {s1: [10, 15]}};
  sandbox.window.WORDS = {s1: [['the', 10.2, 10.4], ['loop', 10.5, 10.9], ['the', 11, 11.2]]};
  assert.ok(Math.abs(K.word({name: 'sc1'}, 'loop') - 0.5) < 1e-9);
  assert.ok(Math.abs(K.word({name: 'sc1'}, 'the', {n: 1, edge: 'end'}) - 1.2) < 1e-9);
  assert.throws(() => K.word({name: 'sc1'}, 'spiral', {seg: 's1'}), /"spiral" not found in segment s1/);
  const warn = console.warn; console.warn = () => {};
  try { assert.equal(K.word({name: 'sc1'}, 'spiral', {fallback: 3}), 3); } finally { console.warn = warn; }
});

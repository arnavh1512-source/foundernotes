import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {videoFilter} from '../scripts/render.mjs';
const skip = spawnSync('ffmpeg', ['-version']).status === 0 ? false : 'ffmpeg not on PATH';
const W = 16, H = 16, fps = 30;
// pipe solid RGB frames through render.mjs's -vf at the sub-frame rate; return [Y, Cb, Cr] of each output frame
function encode(colors, blur) {
  const r = spawnSync('ffmpeg', ['-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', `${W}x${H}`, '-framerate', String(fps * blur), '-i', '-',
    '-vf', videoFilter(fps, blur), '-r', String(fps), '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-'],
  {input: Buffer.concat(colors.map((c) => Buffer.alloc(W * H * 3, Buffer.from(c))))});
  assert.equal(r.status, 0, String(r.stderr));
  const size = W * H * 3 / 2;
  return Array.from({length: r.stdout.length / size}, (_, i) => [0, W * H, W * H * 5 / 4].map((o) => r.stdout[i * size + o]));
}
test('motion blur frame k is the mean of sub-frames kN..kN+N-1', {skip}, () => {
  const N = 3, greys = Array.from({length: 4 * N}, (_, n) => n * 20);
  const ys = encode(greys.map((g) => [g, g, g]), N).map((p) => p[0]);
  assert.equal(ys.length, 4);
  ys.forEach((y, k) => {
    const mean = greys.slice(k * N, k * N + N).reduce((a, b) => a + b) / N;
    assert.ok(Math.abs(y - (16 + 219 * mean / 255)) <= 1, `frame ${k}: Y ${y}, mean grey ${mean}`);
  });
});
test('RGB converts with the BT.709 matrix at limited range', {skip}, () => {
  const [[y, cb, cr]] = encode([[0xF2, 0xB1, 0x34]], 1);  // channel gold; BT.601 would give Cb 63, Cr 165
  assert.ok(Math.abs(y - 172) <= 1 && Math.abs(cb - 67) <= 1 && Math.abs(cr - 162) <= 1, `${y} ${cb} ${cr}`);
});

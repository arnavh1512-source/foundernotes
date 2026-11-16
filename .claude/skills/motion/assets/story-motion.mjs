// Original, renderer-independent geometry and cue helpers. No upstream artwork.
const finite = (n, name) => {
  if (!Number.isFinite(n)) throw new TypeError(`${name} must be finite`);
  return n;
};
const point = (p) => {
  if (!Array.isArray(p) || p.length !== 2) throw new TypeError('Expected [x, y]');
  p.forEach((n) => finite(n, 'coordinate'));
  return p;
};
export function progress(time, start, duration) {
  [time, start, duration].forEach((n) => finite(n, 'time'));
  if (duration <= 0) throw new RangeError('duration must be positive');
  const x = Math.max(0, Math.min(1, (time - start) / duration));
  return x * x * x * (10 + x * (-15 + 6 * x));
}
export const mix = (a, b, k) => a + (b - a) * k;

/** A two-bone arm, including the actual wrist when the target is out of reach. */
export function solveArm(shoulder, target, upper, lower, bend = 1) {
  point(shoulder); point(target);
  [upper, lower].forEach((n) => finite(n, 'limb length'));
  if (upper <= 0 || lower <= 0 || ![-1, 1].includes(bend)) throw new RangeError('Invalid arm');
  const dx = target[0] - shoulder[0], dy = target[1] - shoulder[1];
  const distance = Math.hypot(dx, dy);
  const epsilon = Math.min(upper, lower) * 1e-7;
  const reach = Math.max(Math.abs(upper - lower) + epsilon, Math.min(upper + lower - epsilon, distance));
  const ux = distance ? dx / distance : 0, uy = distance ? dy / distance : 1;
  const along = (upper * upper + reach * reach - lower * lower) / (2 * reach);
  const across = Math.sqrt(Math.max(0, upper * upper - along * along)) * bend;
  return {
    shoulder: [...shoulder],
    elbow: [shoulder[0] + along * ux - across * uy, shoulder[1] + along * uy + across * ux],
    wrist: [shoulder[0] + reach * ux, shoulder[1] + reach * uy],
    clamped: Math.abs(reach - distance) > epsilon / 2,
  };
}

/** Use the same group for hand and prop; its origin is the grip, not a guessed screen point. */
export function gripTransform(arm, angle = 0) {
  point(arm.wrist); finite(angle, 'angle');
  return `translate(${arm.wrist[0]} ${arm.wrist[1]}) rotate(${angle})`;
}

/** SVG matrix for a camera looking through flat layers; depth 0 is the far plane. */
export function layerMatrix(camera, depth, width, height) {
  const { x = 0, y = 0, zoom = 1, roll = 0 } = camera;
  [x, y, zoom, roll, depth, width, height].forEach((n) => finite(n, 'camera'));
  if (zoom <= 0 || depth < 0 || width <= 0 || height <= 0) throw new RangeError('Invalid camera');
  const scale = zoom ** depth, r = roll * depth * Math.PI / 180;
  const a = Math.cos(r) * scale, b = Math.sin(r) * scale, c = -b, d = a;
  const cx = width / 2, cy = height / 2;
  return [a, b, c, d, cx - a * (cx + x * depth) - c * (cy + y * depth), cy - b * (cx + x * depth) - d * (cy + y * depth)];
}
export const svgMatrix = (m) => {
  if (!Array.isArray(m) || m.length !== 6) throw new TypeError('Expected six matrix values');
  m.forEach((n) => finite(n, 'matrix'));
  return `matrix(${m.join(' ')})`;
};

/** Never leave a blank picture at an exact cut, the lead-in, or the final frame. */
export function shotAt(boundaries, time) {
  finite(time, 'time');
  if (!Array.isArray(boundaries) || boundaries.length < 2 || boundaries[0] !== 0) throw new RangeError('Timeline must start at zero');
  boundaries.forEach((n, i) => {
    finite(n, 'boundary');
    if (i && n <= boundaries[i - 1]) throw new RangeError('Boundaries must increase');
  });
  const t = Math.max(0, Math.min(time, boundaries.at(-1)));
  let index = boundaries.findIndex((end, i) => i > 0 && t < end) - 1;
  if (index < 0) index = t >= boundaries.at(-1) ? boundaries.length - 2 : 0;
  return { index, local: t - boundaries[index], duration: boundaries[index + 1] - boundaries[index] };
}

/** Word timing provenance is explicit: estimated captions do not become exact action cues. */
export function wordCue(words, token, { occurrence = 1, source, start = 0, end = Infinity } = {}) {
  if (!['asr', 'forced-alignment', 'manual', 'estimated'].includes(source)) throw new TypeError('Declare cue source');
  if (!Number.isInteger(occurrence) || occurrence < 1) throw new RangeError('occurrence starts at 1');
  finite(start, 'cue range');
  if (!(Number.isFinite(end) || end === Infinity) || end <= start) throw new RangeError('Invalid cue range');
  const normalize = (s) => String(s).normalize('NFKC').toLowerCase().replace(/[^\p{L}\p{N}]/gu, '');
  const wanted = normalize(token);
  if (!wanted || !Array.isArray(words)) throw new TypeError('Expected words and a spoken token');
  const matches = words.filter((w) => {
    finite(w.start, 'word start'); finite(w.end, 'word end');
    if (w.start < 0 || w.end < w.start) throw new RangeError('Invalid word time');
    return w.start >= start && w.start < end && normalize(w.word ?? w.w) === wanted;
  });
  const found = matches[occurrence - 1];
  if (!found) throw new RangeError(`Missing cue: ${token} #${occurrence}`);
  return { time: found.start, end: found.end, source, estimated: source === 'estimated' };
}

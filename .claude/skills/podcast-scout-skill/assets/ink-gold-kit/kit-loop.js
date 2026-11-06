/* "One year, twenty times" additions to the Ink & Gold kit. Load after kit.js.
 * Gold rule for this film: gold = learning that compounds. The Looper's thread starts gold and greys
 * as it repeats; the Climber's spiral stays gold. Keep y > 900 clear for captions.
 */
(function () {
  const K = window.K;
  // the two men (rig colours). Climber = kit default teal coat. Looper = rust coat, so they read apart.
  // CAST for this film (owner rule: new characters every video — see CAST.md; After the Win's lead was
  // wavy hair, teal jacket, medium skin, no glasses/beard, build 1).
  // Climber: deep skin, close crop, glasses, slim, navy overcoat-blue jacket, olive trousers.
  K.CLIMBER = { hairStyle: "crop", glasses: true, facialHair: "none", build: 0.94,
    skin: "#7B4A2E", skinDk: "#5C3420", skinLt: "#9A6342", hair: "#15100D",
    jacket: "#2F4D7A", jacketDk: "#203657", tee: "#EDE2CB", pants: "#4A4A36", pantsDk: "#35352A", shoe: "#E9E2D2" };
  // Looper: light-olive skin, curly hair, full beard, broad build, rust jacket, grey trousers.
  K.LOOPER = { hairStyle: "curly", glasses: false, facialHair: "full", build: 1.1,
    skin: "#D7A47C", skinDk: "#B07D58", skinLt: "#EBC29E", hair: "#3B2A1E",
    jacket: "#8A4A2E", jacketDk: "#62321E", tee: "#E8DCC4", pants: "#3E4246", pantsDk: "#2C2F33", shoe: "#D9D2C4" };
  K.DEFAULT_CAST = K.CLIMBER;
  K.grey = "#8A949C";

  // closed loop retraced `laps` times; each lap drifts a hair so the groove thickens (one year, repeated)
  K.loopPath = (cx, cy, rx, ry, laps = 1, drift = 2.5, steps = 72, a0 = -Math.PI / 2) => {
    let d = "";
    for (let l = 0; l < laps; l++) for (let i = 0; i <= steps; i++) {
      const a = a0 + (i / steps) * Math.PI * 2, j = Math.sin(l * 1.7 + i * 0.21) * drift;
      const x = cx + (rx + j) * Math.cos(a), y = cy + (ry + j * 0.6) * Math.sin(a);
      d += (l === 0 && i === 0 ? "M" : "L") + x.toFixed(1) + " " + y.toFixed(1) + " ";
    }
    return d;
  };
  // opening spiral that also climbs (each year wider and higher). Starts at (cx, cy) heading up.
  K.spiralPath = (cx, cy, r0 = 18, grow = 26, turns = 4, rise = 60, squash = 0.55, steps = 60) => {
    let d = "";
    for (let i = 0; i <= turns * steps; i++) {
      const u = i / steps, a = -Math.PI / 2 + u * Math.PI * 2, r = r0 + grow * u;
      const x = cx + r * Math.cos(a), y = cy + r * squash * Math.sin(a) - rise * u;
      d += (i ? "L" : "M") + x.toFixed(1) + " " + y.toFixed(1) + " ";
    }
    return d;
  };
  // recolour a K.thread from gold toward grey (k 0..1): learning draining out
  K.threadGrey = (g, k) => {
    const mix = (a, b) => { const pa = parseInt(a.slice(1), 16), pb = parseInt(b.slice(1), 16), c = (s) => Math.round(K.lerp((pa >> s) & 255, (pb >> s) & 255, k)); return `rgb(${c(16)},${c(8)},${c(0)})`; };
    g._line.setAttribute("stroke", k <= 0 ? "url(#goldG)" : mix("#E8B34A", K.grey));
    g._paths[0].setAttribute("stroke", mix("#E8B34A", K.grey)); g._paths[0].setAttribute("opacity", (0.22 * (1 - k)).toFixed(3));
    g._tip.setAttribute("fill", mix("#FFD98A", "#B8C0C6"));
  };
  // small calendar page ("YEAR 7")
  K.page = (parent, label, o = {}) => {
    const g = K.g(parent, 0, 0);
    K.el("rect", { x: -34, y: -40, width: 68, height: 80, rx: 6, fill: o.fill || K.C.cream, stroke: K.C.ink, "stroke-width": 3 }, g);
    K.el("rect", { x: -34, y: -40, width: 68, height: 20, rx: 6, fill: o.band || K.C.ember }, g);
    const t = K.text(g, label, 0, 22, { size: 30, fill: K.C.ink, weight: 700 }); g._t = t;
    return g;
  };
  // zero-based horizontal or vertical bar chart. items: [{label, value, color, note}] → returns {g, draw(t-ish k array or number)}
  K.bars = (parent, o) => {
    const { x, y, w, h, items, max, vertical = true, unit = "%", fmt } = o;
    const g = K.g(parent, x, y), n = items.length, gap = o.gap ?? 0.32;
    // axis at zero
    const axis = K.el("path", { d: vertical ? `M-20 0 L${w + 20} 0` : `M0 -20 L0 ${h + 20}`, stroke: K.C.fog, "stroke-width": 3 }, g);
    const zero = K.text(g, "0", vertical ? -44 : 0, vertical ? 10 : h + 52, { size: 26, fill: K.C.fog, weight: 400 });
    const slot = (vertical ? w : h) / n, bw = slot * (1 - gap);
    const bars = items.map((it, i) => {
      const bg = K.g(g, 0, 0);
      const r = K.el("rect", { rx: 6, fill: it.color || K.C.gold }, bg);
      const v = K.text(bg, "", 0, 0, { size: o.valueSize || 44, fill: it.vcolor || K.C.cream, weight: 700 });
      const l = K.text(bg, it.label, 0, 0, { size: o.labelSize || 30, fill: K.C.cream, weight: 700, anchor: vertical ? "middle" : "end" });
      return { it, bg, r, v, l, i };
    });
    const draw = (ks) => bars.forEach((b) => {
      const k = Array.isArray(ks) ? ks[b.i] : ks, val = b.it.value * K.clamp(k), len = (val / max) * (vertical ? h : w);
      const c0 = slot * b.i + (slot - bw) / 2;
      if (vertical) {
        K.attr(b.r, { x: c0, y: -Math.max(len, 0.01), width: bw, height: Math.max(len, 0.01) });
        K.tf(b.v, c0 + bw / 2, -len - 18); K.tf(b.l, c0 + bw / 2, 48);
      } else {
        K.attr(b.r, { x: 0, y: c0, width: Math.max(len, 0.01), height: bw });
        K.tf(b.v, len + 16, c0 + bw / 2 + 15); b.v._t.setAttribute("text-anchor", "start"); K.tf(b.l, -24, c0 + bw / 2 + 11);
      }
      b.v._t.textContent = k > 0.02 ? (fmt ? fmt(b.it.value, k) : (b.it.shown ?? (b.it.value * (k >= 1 ? 1 : k)).toFixed(o.dp ?? 0) + unit)) : "";
      K.op(b.v, K.prog(k, 0.15, 0.5)); K.op(b.l, K.prog(k, 0, 0.3) || (o.labelsFirst ? 1 : 0));
    });
    return { g, bars, draw, axis, zero };
  };
  // the open-question marker: a gold "?" on a pin. Carried from sc03 to sc13.
  K.qmark = (parent, x, y, s = 1) => {
    const g = K.g(parent, x, y);
    K.el("circle", { cx: 0, cy: 0, r: 46, fill: K.C.ink, stroke: K.C.gold, "stroke-width": 4 }, g);
    K.text(g, "?", 0, 22, { font: "serif", size: 66, fill: K.C.gold });
    K.tf(g, x, y, s); g._s = s; return g;
  };
  // ground line + soft floor for two-shots
  K.floor = (parent, y = 860, col = K._floorCol || "#132230") => { K.el("rect", { x: -400, y, width: 2720, height: 600, fill: col }, parent); return K.el("path", { d: `M-400 ${y} L2320 ${y}`, stroke: K._floorLine || "#22384A", "stroke-width": 3 }, parent); };
  // simple bow for the archer, drawn in the hand group (held). k = draw (0 rest .. 1 full)
  K.bow = (parent) => {
    const g = K.el("g", {}, parent);
    const limb = K.el("path", { d: "M0 -110 C46 -60 46 60 0 110", fill: "none", stroke: "#6B4A2E", "stroke-width": 8, "stroke-linecap": "round" }, g);
    const string = K.el("path", { d: "", stroke: K.C.cream, "stroke-width": 2, fill: "none" }, g);
    g._set = (k) => string.setAttribute("d", `M0 -110 L${-60 * k} 0 L0 110`);
    g._set(0); return g;
  };
})();

/* ---------- backdrops: rotate them (owner rule — never the same background all the time) ----------
 * K.backdrop(S, name) recolours the sky, adds the preset's texture in S.far and returns {ink, text, sub, light}
 * colours to use for type on it. Rule: no two adjacent scenes share a backdrop; ≥ 6 different per film.
 * Light backdrops ("paper", "sunrise") need dark type: use the returned .text / .sub, never cream.
 */
(function () {
  const K = window.K;
  const P = {
    night:     { top: "#0E1822", bot: "#1E3446", glow: "warm", text: "#F3E8D2", sub: "#6F8899" },
    teal:      { top: "#0B2326", bot: "#1F4A47", glow: "warm", text: "#F3E8D2", sub: "#8FB7B0", spot: true },
    paper:     { top: "#EFE3C8", bot: "#D9C7A2", glow: "warm", text: "#1B2630", sub: "#6B5B45", light: true, fibres: true },
    dawn:      { top: "#1B2A44", bot: "#C9805A", glow: "warm", text: "#FFF4E2", sub: "#E9C9AE", horizon: "#F2B279" },
    chalk:     { top: "#1C2B26", bot: "#24362F", glow: "cool", text: "#EEF0E6", sub: "#9DB3A6", smudge: true },
    clinic:    { top: "#16262A", bot: "#3C5A5C", glow: "cool", text: "#EAF4F2", sub: "#9CC0BC", tiles: true },
    ember:     { top: "#1E1110", bot: "#4A2418", glow: "warm", text: "#FBE9DA", sub: "#D79A7E" },
    violet:    { top: "#16122A", bot: "#3A2A55", glow: "warm", text: "#F1E9FA", sub: "#A99BC4" },
    fog:       { top: "#2B3740", bot: "#5B6B74", glow: "cool", text: "#F4F6F7", sub: "#C3CDD2", mist: true },
    blueprint: { top: "#0C2340", bot: "#123761", glow: "cool", text: "#EAF2FF", sub: "#8FB0DA", grid: true },
    sunrise:   { top: "#F6D9A8", bot: "#E59A6A", glow: "warm", text: "#2A1E1A", sub: "#7A4B36", light: true, horizon: "#FFF1CF" },
  };
  K.BACKDROPS = Object.keys(P);
  K.backdrop = (S, name) => {
    const p = P[name]; if (!p) throw new Error("unknown backdrop " + name);
    const id = "bd_" + name;
    K.el("linearGradient", { id, x1: 0, y1: 0, x2: 0, y2: 1 }, K.defs).innerHTML = `<stop offset="0" stop-color="${p.top}"/><stop offset="1" stop-color="${p.bot}"/>`;
    S.bg.setAttribute("fill", `url(#${id})`);
    const g = K.el("g", {}, S.far); S.far.insertBefore(g, S.far.firstChild);
    if (p.horizon) K.el("ellipse", { cx: 960, cy: 820, rx: 1500, ry: 300, fill: p.horizon, opacity: 0.35, filter: "url(#soft)" }, g);
    if (p.spot) K.el("ellipse", { cx: 960, cy: 420, rx: 760, ry: 520, fill: "#3E7C76", opacity: 0.35, filter: "url(#soft)" }, g);
    if (p.grid) for (let x = 0; x <= 1920; x += 60) { K.el("path", { d: `M${x} -200 L${x} 1280`, stroke: "#5D8BC4", "stroke-width": x % 240 ? 1 : 2, opacity: x % 240 ? 0.12 : 0.22 }, g); }
    if (p.grid) for (let y = 0; y <= 1080; y += 60) { K.el("path", { d: `M-200 ${y} L2120 ${y}`, stroke: "#5D8BC4", "stroke-width": y % 240 ? 1 : 2, opacity: y % 240 ? 0.12 : 0.22 }, g); }
    if (p.tiles) for (let x = -60; x <= 1980; x += 120) K.el("path", { d: `M${x} 560 L${x} 1280`, stroke: "#8DB3B0", "stroke-width": 2, opacity: 0.12 }, g);
    if (p.smudge) for (let i = 0; i < 14; i++) K.el("ellipse", { cx: K.rand(i * 3) * 1920, cy: K.rand(i * 7) * 900, rx: 120 + K.rand(i) * 260, ry: 30 + K.rand(i * 5) * 60, fill: "#DDE6DA", opacity: 0.035 + K.rand(i * 9) * 0.03, transform: `rotate(${(K.rand(i * 11) - 0.5) * 30})`, filter: "url(#soft)" }, g);
    if (p.mist) for (let i = 0; i < 6; i++) { const m = K.el("ellipse", { cx: K.rand(i * 4) * 1920, cy: 300 + i * 110, rx: 700, ry: 70, fill: "#E8EEF1", opacity: 0.08, filter: "url(#soft)" }, g); m._p = i; (S._mist = S._mist || []).push(m); }
    if (p.fibres) for (let i = 0; i < 220; i++) { const x = K.rand(i * 1.3) * 1920, y = K.rand(i * 2.7) * 1080, a = K.rand(i * 5.1) * 180; K.el("path", { d: `M${x} ${y} l${Math.cos(a) * 14} ${Math.sin(a) * 14}`, stroke: "#8A7552", "stroke-width": 1, opacity: 0.12 }, g); }
    if (p.light) { const v = document.querySelector('rect[fill="url(#vig)"]'); if (v) v.setAttribute("opacity", 0.35); }
    K._floorCol = {'night': ['#132230', '#22384A'], 'teal': ['#0E2A2B', '#2A5150'], 'paper': ['#CDB98F', '#A8916A'], 'dawn': ['#2E2430', '#5A4048'], 'chalk': ['#16221E', '#2F4239'], 'clinic': ['#1E3335', '#3E5C5D'], 'ember': ['#24120E', '#4E2A1E'], 'violet': ['#1C162E', '#3E3160'], 'fog': ['#36424A', '#56656E'], 'blueprint': ['#0A1C34', '#24497A'], 'sunrise': ['#D9A57A', '#B98058']}[name][0]; K._floorLine = {'night': ['#132230', '#22384A'], 'teal': ['#0E2A2B', '#2A5150'], 'paper': ['#CDB98F', '#A8916A'], 'dawn': ['#2E2430', '#5A4048'], 'chalk': ['#16221E', '#2F4239'], 'clinic': ['#1E3335', '#3E5C5D'], 'ember': ['#24120E', '#4E2A1E'], 'violet': ['#1C162E', '#3E3160'], 'fog': ['#36424A', '#56656E'], 'blueprint': ['#0A1C34', '#24497A'], 'sunrise': ['#D9A57A', '#B98058']}[name][1];
    S.look = Object.assign({ name }, p);
    return S.look;
  };
  // call from draw(t) to drift mist on "fog" backdrops
  K.backdropTick = (S, t) => (S._mist || []).forEach((m) => K.tf(m, Math.sin(t * 0.08 + m._p) * 120, 0));
  // the assignment for this film (keep adjacent scenes different)
  K.FILM_BACKDROPS = { "sc01-threads": "night", "sc02-identical": "teal", "sc03-quote": "paper", "sc04-myth": "dawn", "sc05-review": "chalk",
    "sc06-hospital": "clinic", "sc07-surgery": "ember", "sc08-kk": "violet", "sc09-archer": "fog", "sc10-practice": "blueprint",
    "sc11-arrested": "night", "sc12-turn": "sunrise", "sc13-gap": "fog", "sc14-check": "teal", "sc15-close": "dawn" };
})();

/* ---------- acting timing (ideas from pixelfx's "acts" — our own code) ----------
 * K.onTwos(t, fps)   character poses step on 12 fps like hand-drawn animation, while light, particles
 *                    and camera stay smooth: pose(K.onTwos(t)) — use for characters only.
 * K.act(t, hits)     hit-stop + shake: hits = [{ t, stop: 0.03–0.2, shake: 0.18, amp: 6 }]. Returns
 *                    { t: effective time (frozen during each stop), sx, sy: shake offset for the frame }.
 *                    Drive the WHOLE scene from the returned t so everything freezes together on contact.
 * K.keys(t, keys)    pose keys [[time, poseObj, mode]] with modes "snap" (hold, jump on the key),
 *                    "out" (fast in, settle), "in" (slow start), "line"; returns the interpolated pose.
 * Recipe that sells an action: wind-up the opposite way (≈25 % of the move) → a big silhouette change on
 * the release frame ("snap") → freeze on contact (heavier = longer, 0.03–0.2 s) with a small shake →
 * the target reacts → overshooting follow-through → recovery to rest.
 */
(function () {
  const K = window.K;
  K.onTwos = (t, fps = 12) => Math.floor(t * fps + 1e-6) / fps;
  K.act = (t, hits = []) => {
    let lost = 0, sx = 0, sy = 0;
    for (const h of hits) {
      if (t > h.t) lost += Math.min(t - h.t, h.stop || 0);
      const since = t - h.t;
      if (since >= 0 && since < (h.shake || 0)) {
        const k = 1 - since / h.shake, a = (h.amp ?? 6) * k * k;
        sx += a * Math.sin(since * 97 + h.t * 13); sy += a * 0.6 * Math.cos(since * 83 + h.t * 7);
      }
    }
    return { t: t - lost, sx, sy };
  };
  const EASE = { out: (x) => 1 - Math.pow(1 - x, 4), in: (x) => x * x * x, line: (x) => x };
  K.keys = (t, keys) => {
    if (t <= keys[0][0]) return Object.assign({}, keys[0][1]);
    for (let i = 1; i < keys.length; i++) {
      const [t1, p1, mode] = keys[i], [t0, p0] = keys[i - 1];
      if (t < t1) {
        if (mode === "snap") return Object.assign({}, p0);
        const e = (EASE[mode] || K.eio)((t - t0) / (t1 - t0));
        return K.mix(Object.assign({}, K.POSE.stand, p0), p1, e);
      }
    }
    return Object.assign({}, keys[keys.length - 1][1]);
  };
})();

/* ---------- channel end card (owner rule: EVERY video ends with it) ----------
 * K.endCard(S, { name, handle, logo, question, sub }) builds it in S.ui; call card.draw(t, t0, tq) from draw():
 *   t0 = when the card starts (start of the closing CTA line), tq = when the question is spoken.
 * Logo (channel/logo.png, the channel's own avatar), "Subscribe to FOUNDER NOTES", a subscribe button that a cursor
 * clicks (hit-stop pop → "SUBSCRIBED ✓" + bell), then the comment question card. Everything stays above y = 900.
 */
(function () {
  const K = window.K;
  K.CHANNEL = { name: "FOUNDER NOTES", handle: "@FounderNotesin", logo: "channel/logo.png",
                question: "What topic should we cover next?", sub: "Tell us in the comments" };
  K.endCard = (S, o = {}) => {
    const c = Object.assign({}, K.CHANNEL, o), ui = S.ui, C = K.C, id = K.id("logoclip");
    const g = K.g(ui, 0, 0); K.op(g, 0);
    // a dark backdrop so the card reads over any scene (the scene stays faintly visible behind it)
    K.el("rect", { x: -20, y: -20, width: 1960, height: 1120, fill: "#081018", opacity: 0.8 }, g);
    K.el("ellipse", { cx: 960, cy: 470, rx: 760, ry: 330, fill: "#16283A", opacity: 0.55, filter: "url(#soft)" }, g);
    K.el("clipPath", { id }, K.defs).innerHTML = `<circle cx="0" cy="0" r="128"/>`;
    const lg = K.g(g, 610, 400);
    const ring = K.el("circle", { cx: 0, cy: 0, r: 140, fill: "none", stroke: C.gold, "stroke-width": 4, opacity: 0.9 }, lg);
    K.el("circle", { cx: 0, cy: 0, r: 131, fill: "#000" }, lg);
    K.el("image", { href: c.logo, x: -128, y: -128, width: 256, height: 256, "clip-path": `url(#${id})`, preserveAspectRatio: "xMidYMid slice" }, lg);
    const halo = K.el("circle", { cx: 0, cy: 0, r: 150, fill: "none", stroke: C.goldLt, "stroke-width": 3, opacity: 0 }, lg);
    const t1 = K.text(g, "Subscribe to", 800, 330, { size: 40, weight: 400, anchor: "start", fill: C.cream });
    const t2 = K.text(g, c.name, 800, 410, { size: 74, weight: 700, anchor: "start", ls: 6, fill: C.cream });
    const t3 = K.text(g, c.handle, 802, 456, { size: 28, weight: 400, anchor: "start", fill: C.fog });
    // button
    const btn = K.g(g, 930, 532);
    const pill = K.el("rect", { x: -130, y: -36, width: 260, height: 72, rx: 36, fill: "#E8353B" }, btn);
    const bl = K.text(btn, "SUBSCRIBE", 0, 12, { size: 30, weight: 700, ls: 3, fill: "#FFFFFF" });
    const bell = K.g(g, 1100, 532);
    K.el("path", { d: "M-16 10 C-16 -4 -12 -16 0 -18 C12 -16 16 -4 16 10 L20 14 L-20 14 Z M-5 18 C-4 24 4 24 5 18 Z", fill: C.cream }, bell);
    // cursor (an arrow pointer)
    const cur = K.g(g, 0, 0);
    K.el("path", { d: "M0 0 L0 38 L10 29 L17 45 L24 42 L17 26 L30 26 Z", fill: "#FFFFFF", stroke: "#0E1822", "stroke-width": 2.5, "stroke-linejoin": "round" }, cur);
    const click = K.el("circle", { cx: 930, cy: 532, r: 10, fill: "none", stroke: "#FFFFFF", "stroke-width": 3, opacity: 0 }, g);
    // question card
    const qc = K.card(g, 960, 760, 1060, 170); K.op(qc, 0);
    const bub = K.g(qc, -440, 0);
    K.el("path", { d: "M-46 -34 H46 A14 14 0 0 1 60 -20 V16 A14 14 0 0 1 46 30 H-6 L-30 50 L-24 30 H-46 A14 14 0 0 1 -60 16 V-20 A14 14 0 0 1 -46 -34 Z", fill: C.gold }, bub);
    [-24, 0, 24].forEach((x) => K.el("circle", { cx: x, cy: -2, r: 6, fill: "#1A2D3E" }, bub));
    const q1 = K.text(qc, c.question, 60, -12, { font: "serif", size: 50, fill: C.cream });
    const q2 = K.text(qc, c.sub + " ↓", 60, 44, { size: 32, weight: 400, fill: C.gold });
    const card = { g };
    card.draw = (t, t0, tq) => {
      tq = tq ?? t0 + 3.2;
      K.op(g, K.eo(K.prog(t, t0, 0.6)));
      const lk = K.settle(t, t0 + 0.1, 0.7, 0.08); K.tf(lg, 610, 400, 0.85 + 0.15 * lk);
      K.op(halo, 0.5 * (1 - K.prog(t, t0 + 0.3, 1.2)) * (t > t0 + 0.3 ? 1 : 0)); K.attr(halo, { r: 140 + 60 * K.eo(K.prog(t, t0 + 0.3, 1.2)) });
      [t1, t2, t3].forEach((e, i) => K.rise(e, K.eo(K.prog(t, t0 + 0.3 + i * 0.15, 0.6)), 22));
      // cursor glides in, presses on the button (hit-stop + pop), button flips to SUBSCRIBED
      const tc = t0 + 1.9, h = K.act(t, [{ t: tc, stop: 0.1, shake: 0.18, amp: 3 }]);
      const mv = K.eio(K.prog(h.t, t0 + 0.8, 1.1)), cx = K.lerp(1500, 940, mv), cy = K.lerp(820, 540, mv);
      const press = t >= tc && t < tc + 0.16 ? 0.85 : 1;
      K.tf(cur, cx + h.sx, cy + h.sy, press); K.op(cur, K.eo(K.prog(t, t0 + 0.7, 0.3)) * (1 - K.prog(t, tc + 0.9, 0.4)));
      const on = t >= tc;
      K.op(btn, K.eo(K.prog(t, t0 + 0.5, 0.5)));
      K.tf(btn, 930 + h.sx, 532 + h.sy, on ? K.settle(t, tc, 0.45, 0.12) * 0.12 + 0.88 + (t < tc + 0.1 ? 0 : 0) : 1);
      pill.setAttribute("fill", on ? "#3A4A58" : "#E8353B"); bl._t.textContent = on ? "SUBSCRIBED ✓" : "SUBSCRIBE";
      K.op(click, on ? 1 - K.prog(t, tc, 0.5) : 0); K.attr(click, { r: 10 + 50 * K.eo(K.prog(t, tc, 0.5)) });
      K.op(bell, on ? K.eo(K.prog(t, tc + 0.1, 0.3)) : 0); K.tf(bell, 1100, 532, 1, on ? 18 * Math.sin((t - tc) * 22) * Math.exp(-(t - tc) * 3) : 0);
      // the question arrives when it is spoken, the bubble dots bounce like typing
      const qk = K.eo(K.prog(t, tq - 0.3, 0.7)); K.op(qc, qk); K.tf(qc, 960, 760 + (1 - qk) * 30);
      bub._x = -440; K.tf(bub, -440, 0, 1 + 0.04 * Math.sin(t * 3));
      Array.from(bub.querySelectorAll("circle")).forEach((d, i) => d.setAttribute("cy", (-2 - 5 * Math.max(0, Math.sin(t * 6 - i * 0.7))).toFixed(1)));
    };
    return card;
  };
})();

/* ---------- paper-cut self-assembly (our own code; grammar adapted from a paper-cut motion prompt kit) ----------
 * Every piece is a flat pre-cut torn-paper shape with a hard drop shadow that ENTERS FROM OUTSIDE THE FRAME and locks
 * into place. Build far-to-near: backdrop → ground → set pieces → crowd → props → hero (base-up: feet … head, hair last).
 * Motion is stop-motion: stepped "on threes" (~10 fps) with tiny per-piece misalignment, then settles with micro-adjusts.
 * Allowed verbs: slide, drop, rotate, tumble, lift, scatter, tip, snap. Never morph, fold or bend.
 * Sound: paper-only foley on each landing (slides, taps, drops).
 *
 *   const P = K.paper(S, layer)                       // one assembler per scene
 *   P.piece(svgOrPathD, { fill, from: "top|bottom|left|right|tl|tr|bl|br", at: t0, dur: 0.5, x, y, rot })
 *   P.text("CHAPTER 2 · THE SPREAD", x, y, { size, fill, from, at })   // a torn-paper label strip with text
 *   P.draw(t)                                         // call every frame; returns landing times for foley
 */
(function () {
  const K = window.K;
  let fid = 0;
  K.paper = (S, layer) => {
    const id = "torn" + (++fid);
    // rough torn edge: displace the shape's outline with turbulence; paper grain via a second noise
    K.el("filter", { id, x: "-10%", y: "-10%", width: "120%", height: "120%" }, K.defs).innerHTML =
      `<feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="${fid * 7}" result="n"/>
       <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G" result="d"/>
       <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="${fid * 3}" result="g"/>
       <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.10 0" result="ga"/>
       <feComposite in="ga" in2="d" operator="in" result="gr"/>
       <feMerge><feMergeNode in="d"/><feMergeNode in="gr"/></feMerge>`;
    const pieces = [];
    const FROM = { top: [0, -1], bottom: [0, 1], left: [-1, 0], right: [1, 0], tl: [-1, -1], tr: [1, -1], bl: [-1, 1], br: [1, 1] };
    const P = {
      piece(d, o = {}) {
        const g = K.g(layer, 0, 0);
        const sh = K.el("path", { d, fill: "#000", opacity: 0.32, transform: "translate(7 9)" }, g);      // hard shadow
        const p = K.el("path", { d, fill: o.fill || "#E9DFC9", filter: `url(#${id})`, stroke: "#FFFFFF", "stroke-width": o.edge ?? 3, "stroke-opacity": 0.55 }, g);
        const n = pieces.length;
        pieces.push(Object.assign({ g, p, sh, n, x: o.x || 0, y: o.y || 0, rot: o.rot || 0, from: FROM[o.from || "top"], at: o.at || 0, dur: o.dur || 0.5,
          jx: (K.rand(n * 3.1 + fid) - 0.5) * 5, jr: (K.rand(n * 5.7 + fid) - 0.5) * 3 }));
        return g;
      },
      text(str, x, y, o = {}) {
        const w = (o.size || 44) * 0.62 * str.length + 60, h = (o.size || 44) * 1.6;
        const g = P.piece(`M${-w / 2} ${-h / 2} H${w / 2} V${h / 2} H${-w / 2} Z`, Object.assign({ x, y }, o, { fill: o.bg || "#F1E7D2" }));
        K.text(g, str, 0, (o.size || 44) * 0.36, { size: o.size || 44, weight: 700, fill: o.fill || "#1B2630", ls: o.ls ?? 4 });
        return g;
      },
      draw(t) {
        const land = [];
        pieces.forEach((q) => {
          const ts = Math.floor((t - q.at) * 10) / 10;                // stepped on threes (~10 fps)
          const k = K.clamp(ts / q.dur), e = K.eo(k);
          const off = (1 - e) * 1300;                                  // starts outside the frame
          const settle = k >= 1 ? K.settle(t, q.at + q.dur, 0.35, 0.06) : 1;
          const mis = (1 - K.clamp((t - q.at - q.dur) / 0.4)) * (k >= 1 ? 1 : 0);   // tiny misalignment then lock
          K.tf(q.g, q.x + q.from[0] * off + q.jx * mis, q.y + q.from[1] * off + q.jr * mis, 0.98 + 0.02 * settle, q.rot + q.jr * (1 - e) * 4 + q.jr * mis);
          K.op(q.g, t >= q.at ? 1 : 0);
          land.push(q.at + q.dur);
        });
        return land;
      },
    };
    return P;
  };
})();

/* ---------- annotations + punch-ins (from the 3D myth-buster pack's edit grammar, our own code) ----------
 * K.trace(layer, d, { color, width, at, dur, glow })  a glowing outline that DRAWS ITSELF around the thing that
 *   matters (the hidden seam, the zero line, the one number). Call tr.draw(t). Default neon green = "look here".
 * K.dashPath(layer, d, { color, at, dur })  a red dashed route/sightline that extends, then marches. dp.draw(t).
 * K.punch(t, punches)  -> zoom factor for K.camera. punches: [{ t, z = 1.12, hold = 0.5, x, y }]; snaps in over
 *   2 frames on the twist WORD (take t from timings.json word times), holds, eases back. Returns { z, x, y }.
 * Rule: one annotation colour per meaning across a film (green = evidence/look here, red = path/claim).
 */
(function () {
  const K = window.K;
  const NS = "http://www.w3.org/2000/svg";
  let fid = 0;
  const glowFilter = (layer, color) => {
    const svg = layer.ownerSVGElement || layer;
    let defs = svg.querySelector("defs") || svg.insertBefore(document.createElementNS(NS, "defs"), svg.firstChild);
    const id = "kglow" + (++fid);
    const f = document.createElementNS(NS, "filter");
    f.setAttribute("id", id); f.setAttribute("x", "-50%"); f.setAttribute("y", "-50%");
    f.setAttribute("width", "200%"); f.setAttribute("height", "200%");
    f.innerHTML = `<feGaussianBlur stdDeviation="7" result="b"/><feFlood flood-color="${color}" flood-opacity="0.9"/>` +
      `<feComposite in2="b" operator="in" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge>`;
    defs.appendChild(f);
    return id;
  };
  K.trace = (layer, d, o = {}) => {
    const color = o.color || "#39FF88", at = o.at ?? 0, dur = o.dur ?? 0.6;
    const p = K.el("path", { d, fill: "none", stroke: color, "stroke-width": o.width || 6,
      "stroke-linecap": "round", "stroke-linejoin": "round", opacity: 0 }, layer);
    if (o.glow !== false) p.setAttribute("filter", `url(#${glowFilter(layer, color)})`);
    const L = p.getTotalLength ? p.getTotalLength() : 1000;
    p.setAttribute("stroke-dasharray", L);
    return { el: p, draw(t) {
      const k = Math.max(0, Math.min(1, (t - at) / dur)), e = 1 - Math.pow(1 - k, 3);
      p.setAttribute("opacity", t < at ? 0 : 1);
      p.setAttribute("stroke-dashoffset", L * (1 - e));
      // a soft pulse once drawn, so the eye keeps returning to it
      if (k >= 1) p.setAttribute("stroke-width", (o.width || 6) * (1 + 0.12 * Math.sin((t - at - dur) * 6)));
    } };
  };
  K.dashPath = (layer, d, o = {}) => {
    const color = o.color || "#E8353B", at = o.at ?? 0, dur = o.dur ?? 0.8;
    const g = K.el("g", {}, layer);
    const mask = K.el("path", { d, fill: "none", stroke: color, "stroke-width": o.width || 6, "stroke-linecap": "round",
      "stroke-dasharray": "18 14", opacity: 0 }, g);
    const L = mask.getTotalLength ? mask.getTotalLength() : 1000;
    return { el: mask, draw(t) {
      const k = Math.max(0, Math.min(1, (t - at) / dur)), e = 1 - Math.pow(1 - k, 3);
      mask.setAttribute("opacity", t < at ? 0 : 1);
      // reveal by growing the visible length, then let the dashes march
      mask.setAttribute("stroke-dasharray", k < 1 ? `${(L * e).toFixed(1)} ${L}` : "18 14");
      mask.setAttribute("stroke-dashoffset", k < 1 ? 0 : -((t - at - dur) * 60) % 32);
    } };
  };
  K.punch = (t, punches = []) => {
    let z = 1, x = 960, y = 540;
    for (const p of punches) {
      const s = t - p.t, hold = p.hold ?? 0.5, zz = p.z ?? 1.12;
      if (s < 0 || s > hold + 0.5) continue;
      const k = s < 0.066 ? s / 0.066 : s < hold ? 1 : 1 - K.eio((s - hold) / 0.5);
      if (k * (zz - 1) + 1 > z) { z = 1 + k * (zz - 1); x = p.x ?? 960; y = p.y ?? 540; }
    }
    return { z, x, y };
  };
})();

/* ---------- chapter tracker, bookmark pin (from the phone film) ---------- */

/* ---------- retention helpers for this film ---------- */
(function () {
  const K = window.K;
  // chapter tracker, top-left: "2/4 · THE SPREAD" (gold number, fog title); fades in over 0.5 s
  K.chapter = (S, n, title, total = 4) => {
    const g = K.g(S.ui, 64, 70); const L = S.look || {};
    const a = K.text(g, `${n}/${total}`, 0, 0, { size: 26, weight: 700, anchor: "start", fill: K.C.gold, ls: 2 });
    const b = K.text(g, "·  " + title.toUpperCase(), 62, 0, { size: 24, weight: 700, anchor: "start", fill: L.sub || K.C.fog, ls: 5 });
    const bar = K.el("rect", { x: 0, y: 14, width: 0, height: 3, rx: 1.5, fill: K.C.gold, opacity: 0.8 }, g);
    g._tick = (t) => { const k = K.eo(K.prog(t, 0.1, 0.5)); K.op(g, k); bar.setAttribute("width", (200 * n / total * k).toFixed(1)); };
    return g;
  };
  // the "remember this" bookmark pin that rides in the top-right corner from sc06 to sc12
  K.pin = (parent, x = 1840, y = 70, s = 1) => {
    const g = K.g(parent, x, y);
    K.el("path", { d: "M-16 -24 H16 V22 L0 10 L-16 22 Z", fill: K.C.gold, stroke: "#0E1822", "stroke-width": 2.5, "stroke-linejoin": "round" }, g);
    K.el("circle", { cx: 0, cy: -8, r: 5, fill: "#0E1822" }, g);
    K.tf(g, x, y, s); return g;
  };
})();
/* ---------- word cues ----------
 * K.word(S, "nothing", { seg: "s10-nothing", n: 0, edge: "start" }) -> scene-local time of that spoken word.
 * Reads window.WORDS (film/words.js, rebuilt by make_words.py after every re-voice) and window.TIMING.
 * Use it for every punch, stamp, hit and reveal that should land ON a word. Never hard-code seconds for those.
 */
(function () {
  const K = window.K;
  K.word = (S, word, o = {}) => {
    const W = window.WORDS || {}, T = window.TIMING, name = S.name || S;
    const sc = T.scenes[name], want = word.toLowerCase().replace(/[^a-z0-9' ]/g, "").split(" ");
    const segs = o.seg ? [o.seg] : Object.keys(W).filter((k) => { const g = T.seg[k]; return g && g[0] >= sc.start - 0.05 && g[1] <= sc.end + 0.05; });
    let hits = 0;
    for (const k of segs) {
      const ws = W[k] || [];
      for (let i = 0; i + want.length <= ws.length; i++) {
        if (want.every((w, j) => ws[i + j][0] === w)) {
          if (hits++ === (o.n || 0)) return (o.edge === "end" ? ws[i + want.length - 1][2] : ws[i][1]) - sc.start;
        }
      }
    }
    console.warn("K.word: not found", word, name);
    return (o.fallback ?? 0);
  };
})();

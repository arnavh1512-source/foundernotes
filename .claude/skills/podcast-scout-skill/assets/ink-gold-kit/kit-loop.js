/* "One year, twenty times" additions to the Ink & Gold kit. Load after kit.js.
 * Gold rule for this film: gold = learning that compounds. The Looper's thread starts gold and greys
 * as it repeats; the Climber's spiral stays gold. Keep y > 900 clear for captions.
 */
(function () {
  const K = window.K;
  // the two men (rig colours). Climber = kit default teal coat. Looper = rust coat, so they read apart.
  K.LOOPER = { jacket: "#7A4A32", jacketDk: "#57321F", pants: "#33302E", pantsDk: "#24211F", hair: "#2A1C14", skin: "#C98B62", skinDk: "#9C6542", skinLt: "#E2AC80" };
  K.CLIMBER = {};
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

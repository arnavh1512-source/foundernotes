/* Hunting Titles — "Ink & Gold" film kit (v2). See STYLE.md.
 * Render contract: every frame is a pure function of t (no Date, rAF, Math.random).
 * Scene file:
 *   <link rel="stylesheet" href="kit.css"><script src="timing.js"></script><script src="kit.js"></script>
 *   <script>K.scene("sc03-promise", { build(S) {...}, draw(t, S) {...} });</script>
 *   S.dur, S.at(segId, frac), S.end(segId); layers S.far, S.world, S.near, S.fx, S.ui
 */
(function () {
  const K = (window.K = {});
  K.C = {
    ink: "#0E1822", night: "#17293A", slate: "#2A4052", fog: "#6F8899", cream: "#F3E8D2",
    gold: "#E8B34A", goldLt: "#FFD98A", goldDk: "#A8761E", ember: "#E0703A", sea: "#4FA3A0",
    skin: "#B9774F", skinDk: "#8E5636", skinLt: "#D59A6E", hair: "#1C1512",
    jacket: "#2E5C58", jacketDk: "#1F403D", tee: "#EDE2CB", pants: "#2C3238", pantsDk: "#1E2328", shoe: "#F1ECE2",
  };
  // ---------- math ----------
  K.clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  K.prog = (t, s, d) => K.clamp((t - s) / d);
  K.lerp = (a, b, x) => a + (b - a) * x;
  K.eo = (x) => 1 - Math.pow(1 - x, 3);
  K.ei = (x) => x * x * x;
  K.eio = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
  K.back = (x) => { const c = 1.3; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
  K.rand = (seed) => { const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453; return x - Math.floor(x); };
  K.wob = (t, seed, amp = 1, hz = 0.3) => amp * (0.6 * Math.sin(t * hz * 6.283 + seed) + 0.4 * Math.sin(t * hz * 2.3 * 6.283 + seed * 1.7));
  K.env = (t, a, b, din = 0.9, dout = 0.45) => K.eo(K.prog(t, a, din)) * (1 - K.ei(K.prog(t, b - dout, dout)));
  // ---------- svg ----------
  const NS = "http://www.w3.org/2000/svg";
  K.el = (tag, attrs = {}, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  K.attr = (e, a) => { for (const k in a) e.setAttribute(k, a[k]); return e; };
  K.tf = (e, x = 0, y = 0, s = 1, r = 0, sx) => e.setAttribute("transform", `translate(${(+x).toFixed(2)} ${(+y).toFixed(2)}) rotate(${(+r).toFixed(2)}) scale(${(sx ?? s).toFixed(4)} ${(+s).toFixed(4)})`);
  K.op = (e, o) => e.setAttribute("opacity", K.clamp(o).toFixed(3));
  K.g = (parent, x = 0, y = 0) => { const g = K.el("g", {}, parent); g._x = x; g._y = y; K.tf(g, x, y); return g; };
  let uid = 0; K.id = (p) => `${p}${++uid}`;

  // ---------- stage ----------
  K.stage = function () {
    const svg = K.el("svg", { id: "stage", viewBox: "0 0 1920 1080", width: 1920, height: 1080 });
    document.body.appendChild(svg);
    const defs = (K.defs = K.el("defs", {}, svg));
    defs.innerHTML = `
      <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="11"/>
        <feColorMatrix values="0 0 0 0 1  0 0 0 0 0.95  0 0 0 0 0.85  0 0 0 0.07 0"/></filter>
      <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
      <filter id="blur6" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
      <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      <radialGradient id="vig" cx="50%" cy="48%" r="72%"><stop offset="55%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#05090D" stop-opacity="0.6"/></radialGradient>
      <radialGradient id="warm"><stop offset="0" stop-color="#FFD98A" stop-opacity="0.55"/><stop offset="0.45" stop-color="#E8B34A" stop-opacity="0.16"/><stop offset="1" stop-color="#E8B34A" stop-opacity="0"/></radialGradient>
      <radialGradient id="cool"><stop offset="0" stop-color="#CFE3EA" stop-opacity="0.35"/><stop offset="1" stop-color="#CFE3EA" stop-opacity="0"/></radialGradient>
      <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE7B0" stop-opacity="0.28"/><stop offset="1" stop-color="#FFE7B0" stop-opacity="0"/></linearGradient>
      <linearGradient id="goldG" x1="0" x2="1"><stop offset="0" stop-color="#FFE29A"/><stop offset="0.5" stop-color="#E8B34A"/><stop offset="1" stop-color="#A8761E"/></linearGradient>
      <linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0E1822"/><stop offset="1" stop-color="#1E3446"/></linearGradient>
      <linearGradient id="cardG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A2D3E" stop-opacity="0.96"/><stop offset="1" stop-color="#101C27" stop-opacity="0.96"/></linearGradient>`;
    const bg = K.el("rect", { x: -200, y: -200, width: 2320, height: 1480, fill: "url(#skyG)" }, svg);
    const far = K.el("g", {}, svg), world = K.el("g", {}, svg), near = K.el("g", {}, svg), fx = K.el("g", {}, svg), ui = K.el("g", {}, svg);
    K.el("rect", { x: 0, y: 0, width: 1920, height: 1080, fill: "url(#vig)" }, svg);
    // film grain is added in ffmpeg at assembly (assemble.py --grain), not per frame here: page grain is slow
    if (new URLSearchParams(location.search).has("grain")) K.el("rect", { x: 0, y: 0, width: 1920, height: 1080, filter: "url(#grain)" }, svg);
    return { svg, defs, bg, far, world, near, fx, ui };
  };
  // camera with parallax: far layer moves 35 %, near layer 140 %
  K.camera = (S, z = 1, fx = 960, fy = 540) => {
    const T = (k) => `translate(960 540) scale(${1 + (z - 1) * k}) translate(${-(960 + (fx - 960) * k)} ${-(540 + (fy - 540) * k)})`;
    S.far.setAttribute("transform", T(0.35)); S.world.setAttribute("transform", T(1)); S.near.setAttribute("transform", T(1.4));
  };
  // ---------- light ----------
  K.glow = (parent, x, y, r, kind = "warm", o = 1) => { const e = K.el("circle", { cx: x, cy: y, r, fill: `url(#${kind})`, opacity: o }, parent); return e; };
  K.beam = (parent, x, y, w1, w2, h, ang = 0) => {
    const g = K.g(parent, x, y);
    K.el("path", { d: `M${-w1 / 2} 0 L${w1 / 2} 0 L${w2 / 2} ${h} L${-w2 / 2} ${h} Z`, fill: "url(#beam)" }, g);
    K.tf(g, x, y, 1, ang); return g;
  };
  K.dust = (parent, n, box, seed = 1) => {
    const g = K.el("g", {}, parent);
    const ps = Array.from({ length: n }, (_, i) => {
      const c = K.el("circle", { r: 1.2 + K.rand(seed * 31 + i) * 2.4, fill: "#FFE7B0" }, g);
      c._x = box[0] + K.rand(seed * 7 + i) * box[2]; c._y = box[1] + K.rand(seed * 13 + i) * box[3]; c._p = K.rand(seed + i * 3) * 6.28; c._s = 0.3 + K.rand(i * 5 + seed) * 0.7;
      return c;
    });
    g._tick = (t) => ps.forEach((c) => { const y = c._y + ((t * 14 * c._s) % box[3]) * -1, x = c._x + Math.sin(t * 0.5 + c._p) * 24; K.tf(c, x, y < box[1] ? y + box[3] : y); K.op(c, 0.25 + 0.45 * (0.5 + 0.5 * Math.sin(t * 1.3 + c._p))); });
    return g;
  };
  // ---------- gold thread ----------
  K.thread = (parent, d, o = {}) => {
    const g = K.el("g", {}, parent);
    const halo = K.el("path", { d, fill: "none", stroke: K.C.gold, "stroke-width": (o.w || 6) * 3.2, "stroke-linecap": "round", opacity: 0.22, filter: "url(#blur6)", pathLength: 1, "stroke-dasharray": 1, "stroke-dashoffset": 1 }, g);
    const line = K.el("path", { d, fill: "none", stroke: o.color || "url(#goldG)", "stroke-width": o.w || 6, "stroke-linecap": "round", "stroke-linejoin": "round", pathLength: 1, "stroke-dasharray": 1, "stroke-dashoffset": 1 }, g);
    const tip = K.el("circle", { r: (o.w || 6) * 1.4, fill: K.C.goldLt, filter: "url(#glow)" }, g);
    g._paths = [halo, line]; g._line = line; g._tip = tip;
    return g;
  };
  K.drawThread = (g, k, showTip = true) => {
    k = K.clamp(k); g._paths.forEach((p) => p.setAttribute("stroke-dashoffset", (1 - k).toFixed(4)));
    const L = g._line.getTotalLength(), pt = g._line.getPointAtLength(L * k);
    K.tf(g._tip, pt.x, pt.y); K.op(g._tip, showTip && k > 0.001 && k < 0.999 ? 1 : 0);
    return pt;
  };
  // plain stroke draw-on
  K.stroke = (parent, d, o = {}) => K.el("path", { d, fill: o.fill || "none", stroke: o.stroke || K.C.cream, "stroke-width": o.w || 4, "stroke-linecap": "round", "stroke-linejoin": "round", pathLength: 1, "stroke-dasharray": 1, "stroke-dashoffset": 1, opacity: o.op ?? 1 }, parent);
  K.draw = (p, k) => p.setAttribute("stroke-dashoffset", (1 - K.clamp(k)).toFixed(4));
  // ---------- type ----------
  const FONTS = { serif: "HTSerif", sans: "HTSans", hand: "HTHand" };
  K.text = (parent, str, x, y, o = {}) => {
    const g = K.g(parent, x, y);
    const e = K.el("text", { x: 0, y: 0, "font-family": FONTS[o.font || "sans"], "font-size": o.size || 44, "font-weight": o.weight || (o.font === "serif" ? 700 : o.font === "hand" ? 400 : 700),
      fill: o.fill || K.C.cream, "text-anchor": o.anchor || "middle", "letter-spacing": o.ls ?? 0 }, g);
    String(str).split("\n").forEach((l, i) => (K.el("tspan", { x: 0, dy: i ? (o.lh || 1.18) * (o.size || 44) : 0 }, e).textContent = l));
    g._t = e; return g;
  };
  K.label = (parent, str, x, y, o = {}) => K.text(parent, String(str).toUpperCase(), x, y, Object.assign({ font: "sans", size: 32, ls: 6, fill: K.C.gold }, o));
  K.rise = (g, k, dist = 26) => { K.op(g, k); K.tf(g, g._x, g._y + (1 - K.eo(k)) * dist); };
  // per-word reveal for titles: returns words; call K.words(g, t, start, step)
  K.title = (parent, str, x, y, o = {}) => {
    const g = K.g(parent, x, y), size = o.size || 96;
    const e = K.el("text", { "font-family": FONTS.serif, "font-size": size, "font-weight": 700, fill: o.fill || K.C.cream, "text-anchor": o.anchor || "middle" }, g);
    g._w = String(str).split(" ").map((w, i) => { const s = K.el("tspan", {}, e); s.textContent = (i ? " " : "") + w; return s; });
    return g;
  };
  K.words = (g, t, start, step = 0.11) => g._w.forEach((s, i) => s.setAttribute("opacity", K.eo(K.prog(t, start + i * step, 0.45)).toFixed(3)));
  K.source = (S, str) => { const g = K.text(S.ui, str, 64, 868, { size: 24, weight: 400, fill: K.C.fog, anchor: "start" }); K.op(g, 0); return g; };
  // card: ink glass with gold hairline (quotes, findings)
  K.card = (parent, x, y, w, h, o = {}) => {
    const g = K.g(parent, x, y);
    K.el("rect", { x: -w / 2 + 10, y: -h / 2 + 16, width: w, height: h, rx: 18, fill: "#000", opacity: 0.35, filter: "url(#blur6)" }, g);
    K.el("rect", { x: -w / 2, y: -h / 2, width: w, height: h, rx: 18, fill: "url(#cardG)", stroke: o.stroke || K.C.gold, "stroke-width": 2, "stroke-opacity": 0.8 }, g);
    return g;
  };
  // ---------- props ----------
  K.trophy = (parent, x, y, s = 1) => {
    const g = K.g(parent, x, y);
    g.innerHTML = `<ellipse cx="0" cy="6" rx="70" ry="12" fill="#000" opacity="0.35"/>
      <path d="M-50 -32 L50 -32 L58 4 L-58 4 Z" fill="#2A2420" stroke="${K.C.ink}" stroke-width="3"/>
      <rect x="-30" y="-24" width="60" height="12" rx="2" fill="#E8B34A" opacity="0.7"/>
      <path d="M-12 -84 C-8 -60 -16 -44 -26 -32 L26 -32 C16 -44 8 -60 12 -84 Z" fill="url(#goldG)" stroke="${K.C.ink}" stroke-width="3"/>
      <path d="M-62 -196 C-108 -196 -104 -128 -44 -116" fill="none" stroke="url(#goldG)" stroke-width="11" stroke-linecap="round"/>
      <path d="M62 -196 C108 -196 104 -128 44 -116" fill="none" stroke="url(#goldG)" stroke-width="11" stroke-linecap="round"/>
      <path d="M-70 -204 L70 -204 C68 -128 34 -88 0 -84 C-34 -88 -68 -128 -70 -204 Z" fill="url(#goldG)" stroke="${K.C.ink}" stroke-width="3"/>
      <ellipse cx="0" cy="-204" rx="70" ry="10" fill="#FFE29A" stroke="${K.C.ink}" stroke-width="3"/>
      <path d="M-44 -190 C-42 -140 -24 -108 -8 -98" fill="none" stroke="#FFF6D6" stroke-width="9" stroke-linecap="round" opacity="0.75"/>`;
    K.tf(g, x, y, s); g._s = s; return g;
  };
  K.city = (parent, y, seed = 1, color = "#203445", n = 22, x0 = -300, w = 2520) => {
    const g = K.el("g", {}, parent); let x = x0;
    for (let i = 0; i < n; i++) {
      const bw = 60 + K.rand(seed + i) * 90, bh = 120 + K.rand(seed * 2 + i) * 320;
      K.el("rect", { x, y: y - bh, width: bw, height: bh + 400, fill: color }, g);
      for (let wy = y - bh + 18; wy < y - 10; wy += 34) for (let wx = x + 12; wx < x + bw - 14; wx += 26)
        if (K.rand(wx * 0.3 + wy * 0.7 + seed) > 0.78) K.el("rect", { x: wx, y: wy, width: 10, height: 14, fill: "#FFD98A", opacity: 0.55 }, g);
      x += bw + 6; if (x > x0 + w) break;
    }
    return g;
  };
  K.plant = (parent, x, y, s = 1, seed = 1) => {
    const g = K.g(parent, x, y); let h = "";
    for (let i = 0; i < 6; i++) { const a = -90 + (i - 2.5) * 24 + (K.rand(seed + i) - 0.5) * 12, L = 80 + K.rand(seed * 3 + i) * 50, ex = Math.cos(a * Math.PI / 180) * L, ey = Math.sin(a * Math.PI / 180) * L - 56;
      h += `<path d="M0 -56 Q${ex * 0.5} ${-56 + ey * 0.15} ${ex} ${ey}" stroke="#2B4A3A" stroke-width="4" fill="none"/><ellipse cx="${ex}" cy="${ey}" rx="26" ry="11" transform="rotate(${a} ${ex} ${ey})" fill="${i % 2 ? "#4F7A5E" : "#3C634C"}"/>`; }
    g.innerHTML = h + `<path d="M-34 -60 H34 L27 0 H-27 Z" fill="#7A4B36"/>`;
    K.tf(g, x, y, s); return g;
  };

  // ---------- the hunter (character rig) ----------
  // Hip at (0,0), y up negative. Angles in degrees: 0 = limb straight down, +ve = toward facing.
  // Knees bend +ve (shin swings back); elbows bend +ve (forearm swings forward/up).
  K.Hunter = class {
    constructor(parent, o = {}) {
      const c = (this.c = Object.assign({}, K.C, o.colors || {}));
      this.o = Object.assign({ scale: 1, rim: 1 }, o);
      const ink = K.C.ink, LW = 3;
      const P = (d, fill, par, ex = {}) => K.el("path", Object.assign({ d, fill, stroke: ink, "stroke-width": LW, "stroke-linejoin": "round", "stroke-linecap": "round" }, ex), par);
      const SH = (d, par, op = 0.28) => K.el("path", { d, fill: "#000", opacity: op }, par);
      this.root = K.el("g", {}, parent);
      this.shadow = K.el("ellipse", { cx: 0, cy: 4, rx: 90, ry: 13, fill: "#000", opacity: 0.4, filter: "url(#blur6)" }, this.root);
      this.body = K.el("g", {}, this.root);
      const leg = (back) => {
        const g = K.el("g", {}, this.body), up = K.el("g", {}, g), lo = K.el("g", {}, up), ft = K.el("g", {}, lo);
        const col = back ? c.pantsDk : c.pants;
        const ug = K.el("g", { transform: "scale(1 1.15)" }, up);
        P("M-22 -10 C-27 28 -24 70 -16 106 L15 106 C19 70 24 30 22 -10 Z", col, ug);
        SH("M-22 -10 C-27 28 -24 70 -16 106 L-6 106 C-12 70 -14 30 -10 -10 Z", ug, 0.22);
        K.el("circle", { cx: 0, cy: 122, r: 15.5, fill: col }, up);
        const lg = K.el("g", { transform: "scale(1 1.16)" }, lo);
        P("M-15 -4 C-22 26 -16 62 -11 98 L10 98 C12 62 15 26 15 -4 Z", col, lg);
        SH("M-15 -4 C-22 26 -16 62 -11 98 L-3 98 C-7 62 -8 26 -5 -4 Z", lg, 0.2);
        K.el("path", { d: "M-12 88 L11 88", stroke: ink, "stroke-width": 2, opacity: 0.5 }, lg);
        P("M-13 -6 C-15 -13 -2 -15 10 -13 C28 -11 42 -3 46 6 C48 12 44 16 38 16 L-13 16 C-17 10 -16 1 -13 -6 Z", back ? "#CFC8BB" : c.shoe, ft);
        K.el("path", { d: "M-15 9 L46 9", stroke: "#B9B0A2", "stroke-width": 4 }, ft);
        K.el("path", { d: "M4 -11 L14 -3 M12 -12 L22 -4", stroke: ink, "stroke-width": 2 }, ft);
        return { g, up, lo, ft, a: 122, b: 114 };
      };
      const arm = (back) => {
        const g = K.el("g", {}, this.body), up = K.el("g", {}, g), lo = K.el("g", {}, up), hd = K.el("g", {}, lo);
        const col = back ? c.jacketDk : c.jacket, sk = back ? c.skinDk : c.skin;
        P("M-16 -12 C-20 28 -17 60 -13 86 L13 86 C16 60 20 28 16 -12 C9 -22 -9 -22 -16 -12 Z", col, up);
        SH("M-16 -12 C-20 28 -17 60 -13 86 L-4 86 C-8 60 -8 28 -6 -16 Z", up, 0.22);
        P("M-14 74 L14 74 L15 90 L-15 90 Z", back ? "#173230" : c.jacketDk, up);
        P("M-10 -2 C-12 28 -10 54 -8 76 L8 76 C10 54 12 28 10 -2 Z", sk, lo);
        P("M-11 -6 C-15 8 -11 22 -2 25 C8 27 14 19 13 6 L11 -6 Z", sk, hd);
        P("M10 0 C19 -1 21 9 14 14", sk, hd);
        K.el("path", { d: "M-6 12 C-2 16 4 16 8 12", stroke: ink, "stroke-width": 1.6, fill: "none", opacity: 0.6 }, hd);
        return { g, up, lo, hd, a: 86, b: 76 };
      };
      this.legB = leg(true); this.armB = arm(true);
      // torso (jacket over tee)
      this.torso = K.el("g", {}, this.body);
      P("M-42 8 C-46 -40 -52 -100 -60 -154 C-52 -174 -26 -182 0 -182 C26 -182 52 -174 60 -154 C54 -100 48 -40 44 8 Z", c.jacket, this.torso);
      P("M-6 -174 C4 -164 14 -164 26 -174 L24 4 L-4 4 Z", c.tee, this.torso);
      K.el("path", { d: "M-6 -174 C4 -164 14 -164 26 -174", stroke: ink, "stroke-width": 3, fill: "none" }, this.torso);
      P("M-6 -176 L-20 -132 L-6 -112 L-2 -170 Z", c.jacketDk, this.torso);
      P("M26 -176 L38 -130 L26 -110 L22 -170 Z", c.jacketDk, this.torso);
      SH("M-42 8 C-46 -40 -52 -100 -60 -154 C-54 -168 -44 -172 -36 -174 C-34 -110 -30 -50 -24 8 Z", this.torso, 0.25);
      P("M-44 -10 L46 -10 L45 10 L-43 10 Z", c.jacketDk, this.torso);
      K.el("path", { d: "M-40 -2 L44 -2", stroke: ink, "stroke-width": 1.5, opacity: 0.6 }, this.torso);
      this.rimT = K.el("path", { d: "M58 -150 C52 -100 47 -40 43 4", stroke: c.cream, "stroke-width": 4, fill: "none", opacity: 0.0, "stroke-linecap": "round" }, this.torso);
      // head (origin = neck base)
      this.head = K.el("g", {}, this.torso);
      P("M-12 8 L-11 -26 L13 -26 L14 8 Z", c.skinDk, this.head);
      this.face = K.el("g", {}, this.head);
      P("M-34 -66 C-36 -102 -14 -118 6 -118 C30 -118 44 -98 43 -72 C43 -62 48 -56 46 -50 C44 -44 40 -42 38 -34 C34 -20 22 -12 6 -12 C-14 -12 -31 -32 -34 -66 Z", c.skin, this.face);
      SH("M-34 -66 C-31 -32 -14 -12 6 -12 C-8 -16 -20 -34 -22 -62 Z", this.face, 0.22);
      K.el("path", { d: "M14 -44 C22 -40 30 -40 36 -46", stroke: c.skinDk, "stroke-width": 3, fill: "none", opacity: 0.7, "stroke-linecap": "round" }, this.face);
      P("M-20 -72 C-32 -78 -34 -58 -26 -50 C-22 -46 -18 -50 -18 -54 Z", c.skinDk, this.face);
      // wavy hair with volume
      P("M-36 -64 C-46 -98 -30 -134 4 -136 C30 -138 50 -122 50 -98 C51 -86 45 -80 41 -86 C37 -94 29 -98 22 -92 C16 -102 4 -104 -3 -96 C-11 -102 -21 -96 -22 -84 C-25 -76 -28 -70 -36 -64 Z", c.hair, this.face);
      P("M-22 -84 L-19 -60 L-14 -64 L-16 -86 Z", c.hair, this.face);
      K.el("path", { d: "M-14 -122 C0 -130 16 -128 28 -120", stroke: "#4A3A30", "stroke-width": 3, fill: "none", "stroke-linecap": "round", opacity: 0.6 }, this.face);
      this.rimH = K.el("path", { d: "M36 -126 C46 -118 51 -106 50 -96", stroke: c.cream, "stroke-width": 3, fill: "none", opacity: 0, "stroke-linecap": "round" }, this.face);
      // eyes, lids, brows, nose, mouth
      this.eyes = [[10, -72, 5.2], [31, -72, 4.4]].map(([x, y, r]) => {
        const g = K.el("g", {}, this.face);
        K.el("ellipse", { cx: x, cy: y, rx: r + 3, ry: r + 1.5, fill: "#F4EEE4" }, g);
        const iris = K.el("ellipse", { cx: x + 1.2, cy: y, rx: r, ry: r, fill: "#2A1A12" }, g);
        const glint = K.el("circle", { cx: x + 2.6, cy: y - 2, r: 1.5, fill: "#fff" }, g);
        const lid = K.el("path", { d: "", fill: c.skin, stroke: ink, "stroke-width": 2.6 }, g);
        return { g, x, y, r, iris, glint, lid };
      });
      this.browL = K.el("path", { d: "", stroke: c.hair, "stroke-width": 5, "stroke-linecap": "round", fill: "none" }, this.face);
      this.browR = K.el("path", { d: "", stroke: c.hair, "stroke-width": 4.5, "stroke-linecap": "round", fill: "none" }, this.face);
      K.el("path", { d: "M37 -72 C40 -62 45 -55 41 -51 C39 -49 36 -50 34 -52", stroke: ink, "stroke-width": 2.6, fill: "none", "stroke-linecap": "round" }, this.face);
      this.mouth = K.el("path", { d: "", stroke: ink, "stroke-width": 3, fill: "none", "stroke-linecap": "round" }, this.face);
      this.legF = leg(false); this.armF = arm(false);
      this.held = K.el("g", {}, this.armF.hd); this.heldB = K.el("g", {}, this.armB.hd);
      this.body.appendChild(this.legF.g); this.body.appendChild(this.armF.g);
      [this.legB, this.legF].forEach((l) => { K.tf(l.lo, 0, l.a); K.tf(l.ft, 0, l.b); });
      [this.armB, this.armF].forEach((a) => { K.tf(a.lo, 0, a.a); K.tf(a.hd, 0, a.b); });
    }
    pose(p) {
      const q = Object.assign({}, K.POSE.stand, p), s = (q.s ?? 1) * this.o.scale, f = q.facing ?? 1;
      K.tf(this.root, q.x, q.y, s, 0, s * f);
      if (q.alpha !== undefined) K.op(this.root, q.alpha);
      const legH = 122 + 114 + 16;
      const drop = (1 - Math.cos((Math.max(q.kneeF, q.kneeB) * Math.PI) / 180)) * 114 * 0.5;
      const hipY = (q.hipY ?? -(legH - drop)) + (q.bob || 0);
      K.tf(this.body, 0, hipY);
      K.tf(this.shadow, (q.shadowX || 0), 4, 1, 0, 1 + (q.shadowW || 0));
      const L = (l, ox, a1, a2) => { K.tf(l.g, ox, -2); K.tf(l.up, 0, 0, 1, -a1); K.tf(l.lo, 0, l.a, 1, a2); K.tf(l.ft, 0, l.b, 1, -(a1 - a2) * 0.25 + (q.toe || 0)); };
      L(this.legB, -10, q.hipB, q.kneeB); L(this.legF, 12, q.hipF, q.kneeF);
      K.tf(this.torso, 0, 0, 1, q.lean);
      const A = (a, ox, a1, a2) => { K.tf(a.g, 0, 0, 1, q.lean); K.tf(a.up, ox, -156, 1, -a1); K.tf(a.lo, 0, a.a, 1, -a2); K.tf(a.hd, 0, a.b, 1, q.wrist || 0); };
      A(this.armB, -40, q.shB, q.elB); A(this.armF, 40, q.shF, q.elF);
      K.tf(this.head, 4, -178, 1, q.head);
      // rim light on the side facing the light (rim * facing > 0 → front edge)
      const rimOn = this.o.rim * f > 0 ? 0.75 : 0;
      K.op(this.rimT, rimOn); K.op(this.rimH, rimOn);
      // face
      const bl = K.clamp(q.blink), look = q.look || 0, up = Math.max(q.brow, 0), sad = -Math.min(q.brow, 0);
      this.eyes.forEach((e) => {
        K.attr(e.iris, { cx: e.x + 1.2 + look * 2.2, cy: e.y + (q.lookY || 0) * 2 });
        K.attr(e.glint, { cx: e.x + 2.6 + look * 2.2, cy: e.y - 2 + (q.lookY || 0) * 2 });
        const ly = e.y - e.r - 2 + bl * (2 * e.r + 2) + (q.lid || 0) * e.r;
        e.lid.setAttribute("d", `M${e.x - e.r - 4} ${e.y - e.r - 8} L${e.x + e.r + 4} ${e.y - e.r - 8} L${e.x + e.r + 4} ${ly} Q${e.x} ${ly + 2} ${e.x - e.r - 4} ${ly} Z`);
      });
      const oy = -84 - up * 7 + sad * 3, iy = -86 - up * 7 - sad * 7 + (q.frown || 0) * 4;
      this.browL.setAttribute("d", `M0 ${oy + 1} Q9 ${Math.min(oy, iy) - 4} 18 ${iy}`);
      this.browR.setAttribute("d", `M25 ${iy} Q32 ${Math.min(oy, iy) - 4} 39 ${oy + 2}`);
      const m = q.mouth, op = q.open || 0;
      this.mouth.setAttribute("d", op > 0.05
        ? `M14 -34 Q25 ${-33 - m * 2} 35 -35 Q26 ${-30 + 15 * op} 14 -34 Z`
        : `M15 ${-33 + m * -1.5} Q25 ${-33 + m * 6} 34 ${-34 + m * -2}`);
      this.mouth.setAttribute("fill", op > 0.05 ? "#4A1E18" : "none");
    }
  };
  // world-space anchor of a rig part (hand, head...) in the coordinates of `layer`
  K.anchor = (el, layer, dx = 0, dy = 0) => {
    const m = layer.getCTM().inverse().multiply(el.getCTM());
    return { x: m.a * dx + m.c * dy + m.e, y: m.b * dx + m.d * dy + m.f, rot: Math.atan2(m.b, m.a) * 180 / Math.PI, s: Math.hypot(m.a, m.b) };
  };
  K.Hunter.prototype.hand = function (which = "F", layer) { return K.anchor(which === "F" ? this.armF.hd : this.armB.hd, layer || this.root.parentNode, 0, 12); };
  K.Hunter.prototype.headPt = function (layer) { return K.anchor(this.face, layer || this.root.parentNode, 6, -60); };
  K.Puppet = K.Hunter;
  K.POSE = {
    stand: { hipF: 3, kneeF: 2, hipB: -5, kneeB: 9, toe: 0, shF: 8, elF: 10, shB: -6, elB: 8, lean: 0, head: 0, brow: 0, mouth: 0.25, open: 0, blink: 0, bob: 0, look: 0 },
    cheer: { hipF: 9, kneeF: 4, hipB: -10, kneeB: 8, shF: 168, elF: 8, shB: -168, elB: -8, lean: -3, head: -10, brow: 0.9, mouth: 1, open: 0.85 },
    slump: { hipF: 3, kneeF: 6, hipB: -5, kneeB: 10, shF: 3, elF: 4, shB: -3, elB: 4, lean: 7, head: 18, brow: -0.7, mouth: -0.6, lid: 0.35 },
    think: { shF: 14, elF: 150, shB: -4, elB: 75, head: -8, brow: 0.3, mouth: -0.1, look: 1, lookY: -1 },
    point: { shF: 82, elF: 8, head: -3, brow: 0.5, mouth: 0.5 },
    shrug: { shF: 38, elF: 95, shB: -38, elB: -95, head: 6, brow: 0.8, mouth: -0.2 },
    sit: { hipY: -128, hipF: 90, kneeF: 92, hipB: 84, kneeB: 86, shF: 26, elF: 40, shB: 18, elB: 40, lean: 6 },
    sitSlump: { hipY: -128, hipF: 88, kneeF: 94, hipB: 82, kneeB: 88, shF: 34, elF: 62, shB: 30, elB: 62, lean: 22, head: 22, brow: -0.6, mouth: -0.4, lid: 0.3 },
    hold: { shF: 26, elF: 96, shB: 18, elB: 92, head: 8, brow: 0.2, mouth: 0.2, look: 0.4, lookY: 0.6 },
    wave: { shF: 150, elF: 30, head: -4, brow: 0.6, mouth: 0.8 },
  };
  K.walk = (ph, amt = 1) => {
    const a = Math.sin(ph * 6.283), c = Math.cos(ph * 6.283);
    return { hipF: 24 * a * amt, kneeF: (6 + Math.max(0, -34 * c)) * amt, hipB: -24 * a * amt, kneeB: (6 + Math.max(0, 34 * c)) * amt,
      shF: -20 * a * amt + 6, elF: 16 + 8 * Math.max(0, a), shB: 20 * a * amt - 6, elB: 16 + 8 * Math.max(0, -a),
      bob: -Math.abs(c) * 7 * amt, lean: 3 * amt, toe: 0 };
  };
  K.mix = (a, b, k) => { const o = Object.assign({}, a); for (const key in b) { if (typeof b[key] === "number") o[key] = K.lerp(a[key] ?? K.POSE.stand[key] ?? 0, b[key], k); else o[key] = b[key]; } return o; };
  // blinks at uneven seeded gaps (2.2–5.5 s), 0.13 s each
  K.blink = (t, seed = 0) => {
    let at = K.rand(seed) * 2;
    for (let i = 0; i < 400 && at <= t; i++) { if (t - at < 0.13) return Math.sin(((t - at) / 0.13) * Math.PI); at += 2.2 + K.rand(seed * 31 + i) * 3.3; }
    return 0;
  };
  // acting helpers (returns 0..1-ish curves): anticipation dips ~25 % the other way before the move,
  // settle overshoots ~6 % and rests by ~0.4 s, lag samples a driver a few frames late for follow-through
  K.anticipate = (t, t0, dur, pre = 0.2, amt = 0.25) => t < t0 - pre ? 0 : t < t0 ? -amt * Math.sin(((t - (t0 - pre)) / pre) * Math.PI / 2) : -amt * (1 - K.eo(K.prog(t, t0, dur * 0.35))) + K.eo(K.prog(t, t0, dur)) * (1 + amt * 0) ;
  K.settle = (t, t0, dur = 0.5, over = 0.06) => { const k = K.prog(t, t0, dur); return k >= 1 ? 1 : K.eo(k) + over * Math.sin(k * Math.PI) * (1 - k); };
  K.lag = (fn, t, frames = 3, i = 1) => fn(t - (frames / 30) * i) * (1 + 0.15 * i);
  K.alive = (t, seed = 0) => ({ bob: Math.sin(t * 1.7 + seed) * 2, head: Math.sin(t * 0.6 + seed) * 1.5, blink: K.blink(t, seed) });
  K.talk = (t) => ({ open: 0.15 + 0.35 * Math.abs(Math.sin(t * 9.5) * Math.sin(t * 3.1)) });

  // ---------- painted plates (p5.brush standalone, MIT — vendor/brush.js) ----------
  // Paints a static, seeded watercolour/charcoal background UNDER the SVG once at build time.
  // fn(brush, W, H) uses top-left coordinates. Use darks and mid-tones here; put light (glows) in SVG,
  // because pigment mixing turns gold-over-blue green. Include <script src="vendor/brush.js"> first.
  K.paintPlate = (S, fn, seed = 7, base = "#14212C") => {
    if (!window.brush) throw new Error("load vendor/brush.js before kit.js to use K.paintPlate");
    const W = 1920, H = 1080;
    brush.createCanvas(W, H, { parent: document.body, pixelDensity: 1 });
    const c = document.querySelector("canvas"); c.style.cssText = "position:absolute;left:0;top:0;width:1920px;height:1080px";
    document.body.insertBefore(c, document.body.firstChild);
    brush.scaleBrushes(4); brush.angleMode(brush.DEGREES); brush.seed(seed); brush.noiseSeed(seed);
    brush.clear(base); brush.push(); brush.translate(-W / 2, -H / 2);
    fn(brush, W, H);
    brush.pop(); brush.render();
    S.bg.setAttribute("fill", "none");
    return c;
  };

  // ---------- seams (vector law) ----------
  // Scenes are rendered separately, so the cut is designed per side: the last `dur` s of A accelerates
  // out (power4.in) and the first `dur` s of B arrives already moving (power4.out, starting ≥ 50 % along
  // the notional path) on the SAME axis and direction, with the same peak blur. Applied to the whole frame.
  const p4in = (x) => x * x * x * x, p4out = (x) => 1 - Math.pow(1 - x, 4);
  K.seamFx = (S, t) => {
    const se = (window.SEAMS || {})[S.name] || {}; let tx = 0, ty = 0, sc = 1, blur = 0;
    const V = (v, k, side) => {           // k: 0 at rest → 1 at the cut
      const big = v === "Z+" || v === "Z-";
      if (v === "current") tx += (side === "out" ? -1 : 1) * 520 * k;
      if (v === "up") ty += (side === "out" ? -1 : 1) * 380 * k;
      if (v === "Z+") sc *= side === "out" ? 1 + 0.35 * k : 1 - 0.22 * k;
      if (v === "Z-") sc *= side === "out" ? 1 - 0.2 * k : 1 + 0.3 * k;
      blur = Math.max(blur, (big ? 16 : 12) * k);
    };
    if (se.out && t > S.dur - se.out.dur) V(se.out.vector, p4in(K.prog(t, S.dur - se.out.dur, se.out.dur)), "out");
    if (se.in && t < se.in.dur) V(se.in.vector, 0.55 * Math.pow(1 - K.prog(t, 0, se.in.dur), 3), "in");
    const css = (tx || ty || sc !== 1) ? `translate(${tx.toFixed(1)}px, ${ty.toFixed(1)}px) scale(${sc.toFixed(4)})` : "";
    for (const el of [S.svg, document.querySelector("canvas")]) if (el) { el.style.transformOrigin = "960px 540px"; el.style.transform = css; el.style.filter = blur > 0.3 ? `blur(${blur.toFixed(1)}px)` : ""; }
  };

  // ---------- scene runner ----------
  K.scene = function (name, def) {
    const T = window.TIMING || { scenes: {}, seg: {} };
    const sc = T.scenes[name] || { start: 0, end: def.duration || 10 };
    const S = K.stage();
    S.name = name; S.start = sc.start; S.dur = +(sc.end - sc.start).toFixed(3);
    S.at = (id, f = 0) => { const g = T.seg[id]; if (!g) throw new Error("unknown segment " + id); return g[0] - sc.start + f * (g[1] - g[0]); };
    S.end = (id) => T.seg[id][1] - sc.start;
    const warm = document.createElement("div"); warm.className = "fontwarm";
    warm.innerHTML = `<span style="font-family:HTHand">a</span><span style="font-family:HTSerif;font-weight:700">a</span><span style="font-family:HTSans">a</span><span style="font-family:HTSans;font-weight:700">a</span>`;
    document.body.appendChild(warm);
    def.build(S);
    window.MOTION = { width: 1920, height: 1080, fps: 30, duration: S.dur };
    window.seek = async (t) => { const tt = Math.min(Math.max(t, 0), S.dur - 1e-3); def.draw(tt, S); K.seamFx(S, tt); };
    const q = new URLSearchParams(location.search);
    window.seek(q.has("t") ? parseFloat(q.get("t")) : 0);
    return S;
  };
})();

import { createRequire } from "module";
const req = createRequire("/home/user/hunting-titles/.claude/skills/motion/scripts/render.mjs");
let pw; for (const n of ["playwright","playwright-core"]) { try { pw = req(n); break; } catch {} }
const b = await pw.chromium.launch();
const p = await b.newPage();
p.on("console", m => console.log("console:", m.text()));
p.on("pageerror", e => console.log("err:", e.message));
const t0 = Date.now();
await p.goto("file://" + process.argv[2], { timeout: 300000 });
console.log("load ms", Date.now() - t0);
await b.close();

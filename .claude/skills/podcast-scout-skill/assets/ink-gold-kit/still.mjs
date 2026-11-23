import { createRequire } from 'node:module'; import { execFileSync } from 'node:child_process'; import path from 'node:path'; import { fileURLToPath, pathToFileURL } from 'node:url';
// Playwright as render.mjs finds it: next to this file, else the motion skill's (run its scripts/setup.sh) from here or any
// folder above (so a copy in studio-output/<slug>/film/ works too), else the global install, else playwright-core.
const req = createRequire(import.meta.url), tries = [() => req('playwright')];
for (let d = path.dirname(fileURLToPath(import.meta.url)); d !== path.dirname(d); d = path.dirname(d)) tries.push(() => createRequire(path.join(d, '.claude/skills/motion/package.json'))('playwright'));
tries.push(() => req(path.join(execFileSync('npm', ['root', '-g'], { shell: process.platform === 'win32' }).toString().trim(), 'playwright')), () => req('playwright-core'));
const chromium = (() => { for (const t of tries) { try { return t().chromium; } catch {} } throw new Error('Playwright not found: bash .claude/skills/motion/scripts/setup.sh'); })();
const [,, file, out, ...ts] = process.argv;
const b = await chromium.launch(process.env.MOTION_CHROMIUM ? { executablePath: process.env.MOTION_CHROMIUM } : {}); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
await p.goto(pathToFileURL(path.resolve(file)).href); await p.waitForTimeout(400);
for (const t of ts) { await p.evaluate(async t => { await document.fonts.ready; await window.seek(+t); }, t); await p.screenshot({ path: `${out}-${t}.png` }); }
if (errs.length) console.log('ERRORS', errs.join('\n')); await b.close();

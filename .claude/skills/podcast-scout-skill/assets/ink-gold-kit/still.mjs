import { createRequire } from 'module'; const { chromium } = createRequire('/opt/node-tools/node_modules/')('playwright');
const [,, file, out, ...ts] = process.argv;
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
await p.goto('file://' + file); await p.waitForTimeout(400);
for (const t of ts) { await p.evaluate(async t => { await document.fonts.ready; await window.seek(+t); }, t); await p.screenshot({ path: `${out}-${t}.png` }); }
if (errs.length) console.log('ERRORS', errs.join('\n')); await b.close();

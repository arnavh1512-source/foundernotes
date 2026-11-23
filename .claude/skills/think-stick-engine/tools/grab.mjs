import {createRequire} from 'module'; const require=createRequire(import.meta.url); const {chromium}=require('playwright');
const [,,file,out,...ts]=process.argv; const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1920,height:1080}});
p.on('pageerror',e=>console.log('ERR',e.message)); await p.goto('file://'+file); await p.waitForTimeout(400);
for(const t of ts){ await p.evaluate(t=>window.seek(+t),t); await p.screenshot({path:`${out}/t${(+t).toFixed(2).padStart(6,'0')}.png`}) } await b.close();

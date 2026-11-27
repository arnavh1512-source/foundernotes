import {createRequire} from 'module'; const require=createRequire(import.meta.url); const {chromium}=require('playwright');
const [,,file,out,...ts]=process.argv; const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1920,height:1080}});
p.on('pageerror',e=>console.log('ERR',e.message)); await p.goto('file://'+file); await p.waitForTimeout(400);
// size the window to the page's own canvas (vertical pages are 1080x1920); landscape pages keep 1920x1080
const M=await p.evaluate(()=>window.MOTION||null); if(M&&M.width&&M.height&&(M.width!==1920||M.height!==1080)) await p.setViewportSize({width:M.width,height:M.height});
for(const t of ts){ await p.evaluate(t=>window.seek(+t),t); await p.screenshot({path:`${out}/t${(+t).toFixed(2).padStart(6,'0')}.png`}) } await b.close();

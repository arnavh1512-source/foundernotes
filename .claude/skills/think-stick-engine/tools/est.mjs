import {createRequire} from 'module'; const require=createRequire(import.meta.url); const {chromium}=require('playwright');
const [,,file,a,b]=process.argv; const br=await chromium.launch({args:['--disable-web-security','--allow-file-access-from-files']}); const p=await br.newPage({viewport:{width:1920,height:1080}});
p.on('pageerror',e=>console.log('ERR',e.message)); await p.goto('file://'+file); await p.waitForTimeout(500);
const r=await p.evaluate(async([a,b])=>{ const c=document.getElementById('c'), sm=document.createElement('canvas'); sm.width=160; sm.height=90; const g=sm.getContext('2d',{willReadFrequently:true});
  let prev=null, n=0, f=0; for(let t=a;t<b;t+=0.1){ await window.seek(t); g.drawImage(c,0,0,160,90); const d=g.getImageData(0,0,160,90).data;
    if(prev){ let s=0,m=0; for(let i=0;i<d.length;i+=4){ s+=Math.abs(d[i]-prev[i])+Math.abs(d[i+1]-prev[i+1])+Math.abs(d[i+2]-prev[i+2]); m+=3 } n++; if(s/m/255>0.025) f++ } prev=d.slice() } return [n,f] },[+a,+b]);
console.log(JSON.stringify(r)); await br.close();

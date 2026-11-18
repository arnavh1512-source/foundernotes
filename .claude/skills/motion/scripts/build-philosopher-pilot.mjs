#!/usr/bin/env node
// Bundle owned performances and the existing gate drawing; private audio/captions stay outside git.
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {resolve,relative,isAbsolute,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
const repo=fileURLToPath(new URL('../../../../',import.meta.url));
const root=resolve(repo,'studio-output');
const output=resolve(process.argv[2]||resolve(root,'philosopher-stick-pilot/picture/index.html'));
const child=relative(root,output);
if(!child||child.startsWith('..')||isAbsolute(child))throw new Error('Output must be inside studio-output');
const read=n=>readFileSync(new URL(n,import.meta.url),'utf8');
const strip=s=>s.replace(/^import .*;$/gm,'').replace(/^export /gm,'');
const base=strip(read('../assets/story-motion.mjs'));
const gateGeometry=strip(read('../assets/stick-performance.mjs'));
const pilot=strip(read('../assets/pilot-performance.mjs'));
const gateTemplate=read('../examples/stick-gate.template.html');
let gate=gateTemplate.match(/<script>([\s\S]*?)<\/script>/)?.[1];
if(!gate||!gate.includes('function draw(t){'))throw new Error('Gate template contract changed');
gate=gate.slice(gate.indexOf('const canvas='),gate.indexOf('window.MOTION='));
gate=gate.replace("const canvas=document.getElementById('stage'), c=canvas.getContext('2d');","const canvas=gateCanvas, c=gateCanvas.getContext('2d');");
gate=gate.replace('function draw(t){','function drawGate(t,actor=true){');
gate=gate.replace(' for(const foot of p.feet)',' if(actor){for(const foot of p.feet)');
gate=gate.replace(' // No captions or dialogue',' }\n // No captions or dialogue');
const template=read('../examples/philosopher-pilot.template.html');
const marker='// @INLINE_PILOT@';
if(template.split(marker).length!==2)throw new Error('Expected one insertion marker');
const bundled=(base+'\n'+gateGeometry+'\n'+pilot+'\n'+gate).replace(/<\/script/gi,'<\\/script');
mkdirSync(dirname(output),{recursive:true});
writeFileSync(output,template.replace(marker,bundled),{flag:'wx'});
console.log(output);


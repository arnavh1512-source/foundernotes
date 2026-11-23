#!/usr/bin/env node
// Bundle this owned exercise into the existing file-based motion renderer contract.
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {resolve,relative,isAbsolute,dirname} from 'node:path';
import {fileURLToPath} from 'node:url';
const repo=fileURLToPath(new URL('../../../../',import.meta.url));
const root=resolve(repo,'studio-output');
const output=resolve(process.argv[2]||resolve(root,'stick-performance/index.html'));
const child=relative(root,output);
if(!child||child.startsWith('..')||isAbsolute(child))throw new Error('Output must be inside studio-output');
const read=(name)=>readFileSync(new URL(name,import.meta.url),'utf8');
const base=read('../assets/story-motion.mjs').replace(/^export /gm,'');
const performance=read('../assets/stick-performance.mjs').replace(/^import .*;$/gm,'').replace(/^export /gm,'');
const template=read('../examples/stick-gate.template.html');
const marker='// @INLINE_GEOMETRY@';
if(template.split(marker).length!==2)throw new Error('Expected one geometry insertion point');
const script=(base+'\n'+performance).replace(/<\/script/gi,'<\\/script');
// the inlined modules are plain script: a multi-line import or export the strips above missed would break the page
if(/^\s*(import|export)\b/m.test(script))throw new Error('Inlined module still has an import/export statement');
mkdirSync(dirname(output),{recursive:true});
writeFileSync(output,template.replace(marker,script)); // overwrites: it is a rebuild inside studio-output
console.log(output);

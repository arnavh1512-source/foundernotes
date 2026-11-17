/* Original visual staging for the owner's philosopher pitch. Silent, provisional timing. */
(function(g){
'use strict';
const K=g.FNPaintedMotion;
const clamp=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const ease=x=>{x=clamp(x);return x*x*(3-2*x)};
const lerp=(a,b,t)=>a+(b-a)*t;
const phase=(t,a,b)=>ease((t-a)/(b-a));
const n=x=>Number(x.toFixed(3));
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const rect=(x,y,w,h,c,more='')=>`<rect x="${n(x)}" y="${n(y)}" width="${n(w)}" height="${n(h)}" fill="${c}" ${more}/>`;
const path=(d,c,more='')=>`<path d="${d}" fill="${c}" ${more}/>`;
const group=(tr,body)=>`<g transform="${tr}">${body}</g>`;
const text=(x,y,s,size=32,color='#eedfc6',extra='')=>`<text x="${x}" y="${y}" font-family="Georgia,serif" font-size="${size}" fill="${color}" ${extra}>${esc(s)}</text>`;
const SHOTS=[
 {id:'hill',start:0,end:6,label:'THE ECCENTRIC PHILOSOPHER',cue:'When life feels tangled, what are you actually looking at?'},
 {id:'pacing',start:6,end:14,label:'THE VISITOR',cue:'YOUTH: You honestly believe the world is simple? Life too?'},
 {id:'slam',start:14,end:21,label:'THE CHALLENGE',cue:'YOUTH: I came to argue until I am satisfied.'},
 {id:'calm',start:21,end:29,label:'THE OTHER VIEW',cue:'A circumstance and its meaning are not the same question.'},
 {id:'memory',start:29,end:39,label:'THE CHILD’S WORLD',cue:'YOUTH: Then he grows up. The blindfold slips.'},
 {id:'storm',start:39,end:47,label:'CONTRADICTIONS',cue:'YOUTH: It is a chaotic heap of contradictions!'},
 {id:'cup',start:47,end:54,label:'THE INTERRUPTION',cue:'The cup touches the table. The visual storm stops.'},
 {id:'answer',start:54,end:62,label:'THE PHILOSOPHER',cue:'PHILOSOPHER: You are making it complicated.'},
 {id:'reaction',start:62,end:68,label:'THE QUESTION TURNS',cue:'YOUTH: I am?'},
 {id:'perspectives',start:68,end:75,label:'TWO PERSPECTIVES',cue:'Different meanings. Real obstacles still remain.'}
];
function shotAt(time){const t=clamp(Number(time)||0,0,75);const s=SHOTS.find(s=>t<s.end)||SHOTS.at(-1);return {...s,local:t-s.start};}
function cupPose(local){const k=phase(local,.3,3.2);return{x:lerp(1185,1260,k),y:lerp(610,740,k),held:local<3.2};}
function defs(){return `<defs>
<linearGradient id="wall" x2="0" y2="1"><stop stop-color="#39434a"/><stop offset="1" stop-color="#b18c67"/></linearGradient>
<linearGradient id="night" x2="0" y2="1"><stop stop-color="#182f43"/><stop offset="1" stop-color="#8d6664"/></linearGradient>
<linearGradient id="fn-coat"><stop stop-color="#748f8f"/><stop offset="1" stop-color="#354f59"/></linearGradient>
<linearGradient id="fn-vest"><stop stop-color="#c69b72"/><stop offset="1" stop-color="#79513e"/></linearGradient>
<radialGradient id="lamp"><stop stop-color="#ffe0a3" stop-opacity=".7"/><stop offset="1" stop-color="#ffe0a3" stop-opacity="0"/></radialGradient>
<filter id="paper"><feTurbulence baseFrequency=".65" numOctaves="2" seed="7"/><feColorMatrix type="saturate" values="0"/></filter>
</defs>`;}
function town(t){let buildings='';for(let i=0;i<28;i++){const x=i*76-30,h=60+K.hash(i+25)*190;buildings+=rect(x,780-h,66,h,'#263945')+rect(x+17,800-h,8,13,'#d7ab70');}return rect(0,0,1920,1080,'url(#night)')+buildings+path('M0 1010Q660 1000 1120 680Q1530 520 1920 820V1080H0Z','#203c42')+rect(1290,470,195,188,'#3b4a49')+path('M1250 480L1380 375L1520 480Z','#243c45')+rect(1360,520,57,71,'#edb46c')+path('M1140 1080Q1190 830 1387 650','none','stroke="#a08e78" stroke-width="25"');}
function room(t){let books='';for(let i=0;i<15;i++)books+=rect(1440+i*24,350+(i%3)*8,17,110-(i%3)*8,['#777f6e','#b59573','#647d83'][i%3]);return rect(0,0,1920,1080,'url(#wall)')+rect(120,90,700,505,'#263d49','stroke="#c8a47f" stroke-width="22"')+group('translate(132 102) scale(.35 .45)',town(t))+rect(456,97,24,495,'#b89b7c')+rect(125,335,690,22,'#b89b7c')+rect(1390,310,465,170,'#4c514e')+books+rect(1370,462,490,20,'#c0a280')+path('M0 805L1920 780V1080H0Z','#6d675b')+`<ellipse cx="1160" cy="390" rx="460" ry="540" fill="url(#lamp)"/>`+path('M1110 320H1215L1234 402H1091Z','#e0b77e')+rect(1155,403,10,190,'#796650')+rect(1119,593,85,12,'#ae8b60');}
function desk(shake=0){return group(`translate(0 ${n(shake)})`,path('M240 740H1730L1860 880H120Z','#ab815e','stroke="#66503e" stroke-width="6"')+path('M135 880H1855V925H135Z','#73563e')+rect(230,920,38,160,'#66503e')+rect(1700,920,38,160,'#66503e'));}
function person(kind,x,y,t,opts={}){const walk=opts.walk||0;const swing=Math.sin(t*7)*walk;const legs=path(`M-55 0L${n(-65+swing*35)} 160M55 0L${n(65-swing*35)} 160`,'none','stroke="#34464e" stroke-width="41" stroke-linecap="round"');return group(`translate(${n(x)} ${n(y)}) rotate(${n(opts.bodyTilt||0)})`,legs+K.character({kind,t,tilt:opts.tilt||0,mood:opts.mood||'neutral',left:opts.left||[-130,-90+swing*15],right:opts.right||[130,-90-swing*15],gesture:opts.gesture||'relaxed'}));}
function mug(x,y,angle=0){return group(`translate(${n(x)} ${n(y)}) rotate(${n(angle)})`,rect(-37,-53,74,50,'#efdec0','rx="7"')+`<ellipse cx="0" cy="-53" rx="37" ry="10" fill="#a88b69"/><path d="M37 -43Q85 -46 75 -20Q65 -2 37 -12" fill="none" stroke="#efdec0" stroke-width="10"/>`);}
function scribbles(t,k=1){let out='';for(let i=0;i<17;i++){const seed=K.hash(i),x=160+seed*1580,y=170+K.hash(i+34)*430,amp=35+seed*90;let d=`M${n(x)} ${n(y)}`;for(let j=1;j<7;j++)d+=`q${n(45*Math.cos(i+j+t*.3))} ${n(amp*Math.sin(j*2+i+t*.5))} 90 0`;out+=path(d,'none',`stroke="#e0b485" stroke-width="${3+i%3}" opacity="${n(.35*k)}" stroke-dasharray="${n(800*k)} 900"`);}return out;}
function caption(s){let cue=s.cue;const words=cue.split(' '),lines=[];let line='';for(const w of words){if((line+' '+w).length>70){lines.push(line);line=w;}else line+=(line?' ':'')+w;}lines.push(line);return rect(180,915,1560,140,'#152a35','opacity=".92" rx="15"')+text(220,951,s.label,22,'#d9ac71','letter-spacing="3"')+lines.map((l,i)=>text(220,994+i*38,l,31)).join('');}
function crop(body,x,y,scale){return group(`translate(960 470) scale(${scale}) translate(${-x} ${-y})`,body);}
function render(time){const s=shotAt(time),t=clamp(Number(time)||0,0,75),u=s.local;let body='';
 const young=(o={})=>person('youth',520,730,t,o),old=(o={})=>person('philosopher',1410,730,t,o);
 if(s.id==='hill'){body=town(t)+group(`translate(${n(lerp(0,-140,phase(u,0,6)))} 0) scale(${n(lerp(1,1.12,phase(u,0,6)))})`,town(t))+text(140,205,'THE ECCENTRIC',63)+text(140,290,'PHILOSOPHER',78);}
 else if(s.id==='pacing'){const p=phase(u,0,3)-phase(u,4,7);body=room(t)+person('youth',lerp(420,840,p),730,t,{walk:1-phase(u,6,8),bodyTilt:-3,tilt:-5,mood:'angry'})+old({mood:'smile'})+desk();}
 else if(s.id==='slam'){const hit=phase(u,.6,1.2),settle=phase(u,1.4,2.2),shake=u>1.2?Math.sin((u-1.2)*45)*5*Math.exp(-(u-1.2)*5):0;body=room(t)+young({bodyTilt:lerp(0,8,hit)-2*settle,mood:'angry',left:[-135,lerp(-160,5,hit)],right:[165,lerp(-140,5,hit)],tilt:lerp(-5,5,hit)})+old({tilt:2*hit})+desk(shake)+mug(1260,740+shake,-shake);}
 else if(s.id==='calm'||s.id==='answer'){const scene=room(t)+young({mood:'angry'})+old({mood:'smile',tilt:lerp(-5,2,phase(u,1,5)),left:[-120,-75],right:[110,-80]})+desk();body=crop(scene,1390,450,1.65+u*.018);}
 else if(s.id==='memory'){const k=phase(u,2,8);body=rect(0,0,1920,1080,'#d8c9a4')+path('M0 740Q700 390 1920 750V1080H0Z','#9aa27c')+`<circle cx="1530" cy="225" r="90" fill="#edd19a"/>`;for(let i=0;i<13;i++){const h=(140+K.hash(i)*260)*k;body+=rect(i*155,790-h,125,h,'#687780');}body+=group(`translate(960 760) scale(${n(lerp(.65,1.05,k))})`,person('youth',0,0,t,{left:[-170,-180+100*k],right:[170,-180+100*k],tilt:-5*k,mood:k>.5?'surprised':'smile'}))+scribbles(t,k);}
 else if(s.id==='storm'){body=room(t)+young({mood:'angry',gesture:'open',bodyTilt:4,left:[-170,-170+Math.sin(u*3)*40],right:[170,-155+Math.sin(u*3+.5)*40],tilt:-8})+old({mood:'neutral'})+desk()+scribbles(t,phase(u,0,3));}
 else if(s.id==='cup'){const c=cupPose(u),withdraw=phase(u,3.2,6.5),hx=c.x-50-120*withdraw,hy=c.y-27-100*withdraw;body=room(t)+scribbles(50.2,1)+desk()+mug(c.x,c.y,lerp(-8,0,phase(u,.3,3.2)))+path(`M1000 480Q1110 500 ${n(hx-10)} ${n(hy)}`,'none','stroke="#a88262" stroke-width="38" stroke-linecap="round"')+`<ellipse cx="${n(hx)}" cy="${n(hy)}" rx="24" ry="18" fill="#c99f82"/>`;body=crop(body,1225,680,2.05);}
 else if(s.id==='reaction'){const k=phase(u,0,5);body=room(t)+young({mood:'surprised',tilt:lerp(7,-6,k),left:[-140,-65],right:[130,-60]})+old()+desk()+scribbles(50.2,1-k);body=crop(body,520,440,1.8);}
 else{body=rect(0,0,960,1080,'#354652')+rect(960,0,960,1080,'#b7b395')+group('translate(-300 30) scale(.8)',town(t))+group('translate(650 30) scale(.8)',town(t))+rect(0,0,960,900,'#253541','opacity=".4"')+rect(960,0,960,900,'#efd4a0','opacity=".2"')+person('youth',480,760,t,{mood:'surprised',tilt:-7})+person('philosopher',1440,760,t,{mood:'smile'})+path('M960 80V865','none','stroke="#e6d4ac" stroke-width="3"');}
 const texture=rect(0,0,1920,1080,'#dac9ad','filter="url(#paper)" opacity=".025"');
 return `<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">${defs()}${body}${texture}${caption(s)}${rect(36,27,665,42,'#172c36','opacity=".9" rx="8"')}${text(55,56,'VISUAL DRAFT · dialogue not recorded',23,'#f0d8af')}</svg>`;
}
g.FNPhilosopher=Object.freeze({SHOTS,duration:75,shotAt,cupPose,render});
})(window);

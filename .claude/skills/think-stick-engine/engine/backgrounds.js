// backgrounds.js: locations that follow the script. Drawn in world coordinates by paper() (scenes that pass their own tone keep it).
// study = the philosopher's library at night; cafe; home (the mother's living room); street; greek; mind = idea space, tinted per chapter.
const BGMAP={};
['duo','study2','lookStudy','phtalk','ymtalk','philCalm','likeSelf','outOfQ','sitdown2','phonePause','coffeeAgain','knife','extreme','impulse','accuse','resolved','aha','gotcha',
 'fairness','youChose','cantAccept','onSpot','shattered','tooTough','medicine','allMyFault','glare','decide','headBurst','comeBack'].forEach(k=>BGMAP[k]='study');
['cafe','explode','blame','cafeVienna','coffeeEnd'].forEach(k=>BGMAP[k]='cafe');
['mom','phone','hangup','bookpile','bookAvalanche','mirror','mirrorY','novelist','novelistClock','drawerLock'].forEach(k=>BGMAP[k]='home');
['wallRoad','roadAhead','twoCars','carDrive','forkRoad','footsteps','stairsUp','kidCross','ysun','copyY','choiceBack'].forEach(k=>BGMAP[k]='street');
['agora','agoraWalk','greek','greekGood'].forEach(k=>BGMAP[k]='greek');
const OWN_BG=new Set(['night1','wellSeasons','glassesTint','spotNow','angerSwitch','secondnight','endask','endcard','subscribe']);
const MIND_TINTS=['#efe3d6','#e3e8f0','#e6eedf','#f0e1e1','#e8e2f0','#f1ead3','#dfecec','#efe0ea'];
const CHAPTERS=['n01','n04','d01','d05','n14','n18','d13','d16','d17','n35','d20','n41','n43'];
function chapterAt(t){ let c=0; CHAPTERS.forEach((k,i)=>{ if(window.SEG&&window.SEG[k]&&t>=window.SEG[k][0]-.01) c=i }); return c }
function bgFor(name){ if(OWN_BG.has(name)) return null; return BGMAP[name]||'mind' }
const rr=(a,b,c,d,col)=>{ x.fillStyle=col; x.fillRect(a,b,c,d) };
function book(X,Y,w,h,col,tilt=0){ x.save(); x.translate(X+w/2,Y); x.rotate(tilt); x.fillStyle=col; x.fillRect(-w/2,-h,w,h); x.fillStyle='rgba(255,255,255,.28)'; x.fillRect(-w/2+2,-h+8,w-4,3); x.fillRect(-w/2+2,-14,w-4,3); x.fillStyle='rgba(0,0,0,.12)'; x.fillRect(w/2-3,-h,3,h); x.restore() }
const BOOKC=['#8a3b2c','#2f5d4f','#c9a46a','#3d5a80','#6b4a2f','#9c6b3c','#4a3b5c','#b5543c','#d9c08f','#5e5a54','#2e4a3a','#7a2a2a'];
function bookcase(X0,X1,top,seed=1){ const fr='#5b3b23';
  rr(X0-18,top-20,X1-X0+36,G-top+20,fr); rr(X0,top,X1-X0,G-top,'#3a2616');
  const shelfH=150, n=Math.floor((G-top)/shelfH);
  for(let s=0;s<n;s++){ const y=top+(s+1)*shelfH; rr(X0-6,y-8,X1-X0+12,14,fr); let xx=X0+8, k=0;
    while(xx<X1-20){ const h0=rnd(seed*97+s*31+k*7), w=16+Math.floor(h0*18), h=86+Math.floor(rnd(seed*13+s*7+k*3)*48); const lean=(rnd(s*5+k*11+seed)>.93&&xx<X1-60)?.25:0;
      if(rnd(s*17+k*3+seed*5)>.94){ xx+=34; k++; continue }
      book(xx,y-8,w,h,BOOKC[(s*5+k*3+seed)%BOOKC.length],lean); xx+=w+(lean?18:1); k++ } }
  rr(X0-30,top-46,X1-X0+60,30,fr) }
function windowNight(X,Y,w,h){ x.save(); const g=x.createLinearGradient(0,Y,0,Y+h); g.addColorStop(0,'#1d2a4a'); g.addColorStop(1,'#3a4d78'); x.fillStyle=g; x.fillRect(X,Y,w,h);
  for(let i=0;i<14;i++){ x.fillStyle=`rgba(255,250,220,${.5+.5*rnd(i*9)})`; x.beginPath(); x.arc(X+rnd(i*3)*w,Y+rnd(i*5+1)*h*.7,1.5+rnd(i)*2,0,7); x.fill() }
  x.fillStyle='#f6e7b0'; x.beginPath(); x.arc(X+w*.72,Y+h*.28,28,0,7); x.fill(); x.fillStyle='#1d2a4a'; x.beginPath(); x.arc(X+w*.72+12,Y+h*.28-6,24,0,7); x.fill();
  x.strokeStyle='#5b3b23'; x.lineWidth=14; x.strokeRect(X,Y,w,h); x.lineWidth=8; x.beginPath(); x.moveTo(X+w/2,Y); x.lineTo(X+w/2,Y+h); x.moveTo(X,Y+h/2); x.lineTo(X+w,Y+h/2); x.stroke();
  x.fillStyle='#8a2f2a'; x.beginPath(); x.moveTo(X-40,Y-30); x.quadraticCurveTo(X+30,Y+h*.5,X-20,Y+h+40); x.lineTo(X-60,Y+h+40); x.lineTo(X-60,Y-30); x.fill();
  x.beginPath(); x.moveTo(X+w+40,Y-30); x.quadraticCurveTo(X+w-30,Y+h*.5,X+w+20,Y+h+40); x.lineTo(X+w+60,Y+h+40); x.lineTo(X+w+60,Y-30); x.fill(); x.restore() }
function lampGlow(X,Y,r,a=.5){ x.save(); const g=x.createRadialGradient(X,Y,10,X,Y,r); g.addColorStop(0,`rgba(255,214,140,${a})`); g.addColorStop(1,'rgba(255,214,140,0)'); x.fillStyle=g; x.fillRect(X-r,Y-r,2*r,2*r); x.restore() }
function woodFloor(col='#a97c50'){ rr(-600,G,3200,700,col); x.save(); x.strokeStyle='rgba(60,35,15,.18)'; x.lineWidth=3; for(let i=0;i<6;i++){ x.beginPath(); x.moveTo(-600,G+30+i*42); x.lineTo(2600,G+30+i*42); x.stroke() } x.restore() }
function frame(X,Y,w,h,inner){ x.save(); rr(X-10,Y-10,w+20,h+20,'#6b4a2f'); rr(X,Y,w,h,inner); x.restore() }
const BG={
 study:()=>{ rr(-600,-600,3200,G+600,'#d9c29a'); x.save(); x.fillStyle='rgba(120,80,40,.06)'; for(let i=-12;i<60;i++) x.fillRect(i*44,-600,20,G+600); x.restore();
   rr(-600,G-150,3200,150,'#b48a5a'); rr(-600,G-158,3200,10,'#8a6440');
   bookcase(40,640,-120,3); windowNight(1380,110,330,360); lampGlow(1890,G-470,420,.45);
   x.save(); x.strokeStyle='#3a2616'; x.lineWidth=8; x.beginPath(); x.moveTo(1890,G); x.lineTo(1890,G-420); x.stroke(); x.fillStyle='#e8c07a'; x.beginPath(); x.moveTo(1840,G-420); x.lineTo(1940,G-420); x.lineTo(1915,G-500); x.lineTo(1865,G-500); x.fill(); x.restore();
   // writing desk with the half-written manuscript and the fountain pen
   rr(1380,G-190,360,18,'#6b4a2f'); rr(1395,G-172,16,172,'#6b4a2f'); rr(1710,G-172,16,172,'#6b4a2f');
   x.save(); x.translate(1520,G-196); x.rotate(-.04); rr(-70,-6,140,8,'#fbf8ef'); x.restore(); x.save(); x.translate(1540,G-204); x.rotate(.05); rr(-60,-6,120,8,'#f4f0e4'); x.restore();
   x.save(); x.strokeStyle='#1c1c1f'; x.lineWidth=7; x.lineCap='round'; x.beginPath(); x.moveTo(1630,G-200); x.lineTo(1690,G-214); x.stroke(); x.strokeStyle='#c9a46a'; x.lineWidth=3; x.beginPath(); x.moveTo(1630,G-200); x.lineTo(1640,G-202); x.stroke(); x.restore();
   frame(880,40,200,140,'#7d8f6a'); x.save(); x.fillStyle='#c9a46a'; x.beginPath(); x.arc(960,110,26,0,7); x.fill(); x.restore();
   woodFloor('#8f6a43'); x.save(); x.fillStyle='#7a2f2a'; x.globalAlpha=.85; x.beginPath(); x.ellipse(1000,G+70,430,52,0,0,7); x.fill(); x.strokeStyle='#c9a46a'; x.lineWidth=6; x.beginPath(); x.ellipse(1000,G+70,400,42,0,0,7); x.stroke(); x.restore() },
 cafe:()=>{ rr(-600,-600,3200,G+600,'#f1e4cc'); rr(-600,G-300,3200,300,'#f7f3ea'); x.save(); x.strokeStyle='rgba(150,140,120,.35)'; x.lineWidth=2; for(let i=-10;i<70;i++){ x.beginPath(); x.moveTo(i*40,G-300); x.lineTo(i*40,G); x.stroke() } for(let j=0;j<8;j++){ x.beginPath(); x.moveTo(-600,G-300+j*40); x.lineTo(2600,G-300+j*40); x.stroke() } x.restore();
   x.save(); const g=x.createLinearGradient(0,100,0,430); g.addColorStop(0,'#bfe0f2'); g.addColorStop(1,'#e8f4fa'); x.fillStyle=g; x.fillRect(120,100,560,330); x.fillStyle='#9fc49a'; x.beginPath(); x.arc(250,380,70,0,7); x.arc(330,350,60,0,7); x.fill(); x.fillStyle='#c9cfd6'; x.fillRect(450,250,90,180); x.fillRect(560,300,70,130); x.strokeStyle='#4a3b2c'; x.lineWidth=12; x.strokeRect(120,100,560,330); x.restore();
   rr(1260,140,300,200,'#2f3a34'); x.save(); x.fillStyle='#f1eee6'; x.font='700 40px Inst'; x.textAlign='center'; x.fillText('MENU',1410,200); x.font='700 22px Inst'; ['coffee ... 3','tea ... 2','cake ... 4'].forEach((t,i)=>x.fillText(t,1410,242+i*30)); x.restore();
   [820,1180].forEach(px=>{ x.save(); x.strokeStyle='#3a2a1c'; x.lineWidth=4; x.beginPath(); x.moveTo(px,-600); x.lineTo(px,120); x.stroke(); x.fillStyle='#3a2a1c'; x.beginPath(); x.moveTo(px-50,170); x.lineTo(px+50,170); x.lineTo(px+22,120); x.lineTo(px-22,120); x.fill(); x.restore(); lampGlow(px,190,220,.35) });
   woodFloor('#b08458') },
 home:()=>{ rr(-600,-600,3200,G+600,'#dde6d6'); x.save(); x.fillStyle='rgba(90,120,90,.12)'; for(let i=-10;i<60;i++) for(let j=-10;j<20;j++){ x.beginPath(); x.arc(i*60+(j%2)*30,j*60,5,0,7); x.fill() } x.restore();
   x.save(); const g=x.createLinearGradient(0,140,0,460); g.addColorStop(0,'#cfe8f7'); g.addColorStop(1,'#f3f9fc'); x.fillStyle=g; x.fillRect(1500,140,300,320); x.strokeStyle='#f7f3ea'; x.lineWidth=14; x.strokeRect(1500,140,300,320); x.beginPath(); x.moveTo(1650,140); x.lineTo(1650,460); x.stroke(); x.fillStyle='#c98f6a'; x.fillRect(1460,110,40,400); x.fillRect(1800,110,40,400); x.restore();
   frame(150,170,160,120,'#e8b04a'); frame(360,200,110,150,'#9fc4d8');
   x.save(); x.fillStyle='#8a6f9e'; x.beginPath(); x.roundRect(-60,G-200,330,200,26); x.fill(); x.fillStyle='#7a5f8e'; x.beginPath(); x.roundRect(-60,G-260,330,90,26); x.fill(); x.restore();
   rr(-600,G,3200,700,'#c9b89a'); x.save(); x.fillStyle='#b5543c'; x.globalAlpha=.5; x.beginPath(); x.ellipse(1000,G+60,520,46,0,0,7); x.fill(); x.restore() },
 street:()=>{ x.save(); const g=x.createLinearGradient(0,-300,0,G); g.addColorStop(0,'#9fd0ee'); g.addColorStop(1,'#eaf4f8'); x.fillStyle=g; x.fillRect(-600,-600,3200,G+600);
   x.fillStyle='rgba(255,255,255,.9)'; [[300,140],[1200,90],[1750,170]].forEach(([cx,cy])=>{ x.beginPath(); x.arc(cx,cy,40,0,7); x.arc(cx+45,cy-12,48,0,7); x.arc(cx+95,cy,38,0,7); x.fill() });
   x.fillStyle='#c4cdd6'; for(let i=0;i<14;i++){ const w=120+rnd(i)*80, h=160+rnd(i*7)*260; x.fillRect(-300+i*190,G-140-h,w,h) } x.fillStyle='#d6dde3'; for(let i=0;i<14;i++){ for(let r=0;r<5;r++) for(let c=0;c<3;c++) x.fillRect(-280+i*190+c*36,G-130-(160+rnd(i*7)*260)+20+r*44,18,24) }
   x.fillStyle='#9aa3a8'; x.fillRect(-600,G-140,3200,140); x.fillStyle='#b9c0c4'; x.fillRect(-600,G-150,3200,12); x.restore(); rr(-600,G,3200,700,'#8d9196');
   x.save(); x.strokeStyle='#f1eee6'; x.lineWidth=8; x.setLineDash([60,50]); x.beginPath(); x.moveTo(-600,G+80); x.lineTo(2600,G+80); x.stroke(); x.restore() },
 greek:()=>{ x.save(); const g=x.createLinearGradient(0,-300,0,G); g.addColorStop(0,'#f3c98b'); g.addColorStop(1,'#fbeedd'); x.fillStyle=g; x.fillRect(-600,-600,3200,G+600);
   x.fillStyle='#e0b27a'; x.beginPath(); x.arc(1600,260,80,0,7); x.fill(); x.fillStyle='#d7c3a3'; x.beginPath(); x.moveTo(-600,G-120); for(let i=0;i<=16;i++) x.lineTo(-600+i*200,G-120-Math.sin(i*1.3)*60-60); x.lineTo(2600,G); x.lineTo(-600,G); x.fill(); x.restore(); rr(-600,G,3200,700,'#e4d4b4') },
 mind:()=>{ const c=chapterAt(NOW), tint=MIND_TINTS[c%MIND_TINTS.length]; rr(-800,-800,3600,G+800,tint);
   x.save(); x.globalAlpha=.08; x.fillStyle='#1c1c1f'; for(let i=0;i<7;i++){ x.beginPath(); x.arc(200+((i*331+c*97)%1500),120+((i*211+c*53)%520),40+((i*37)%90),0,7); x.fill() } x.restore(); rr(-800,G,3600,800,tint); x.save(); x.fillStyle='rgba(0,0,0,.05)'; x.fillRect(-800,G,3600,800); x.restore() }
};
function drawBG(){ const k=window.BG; if(k&&BG[k]) BG[k]() }
// the library scenes now use the full study set
S.study2=(u,ts,d)=>S.duo(u,ts,d,{mode:'wide',pact:'calm',act:'stand'});
S.lookStudy=(u,ts,d)=>{ cam(lerp(520,1520,io(ph(ts,0,d*.85))),520,1.25); paper(); ground();
  const look=Math.sin(ts*1.3); fig(1000,P({dir:look>0?1:-1,head:-.25+.1*Math.sin(ts*2),af1:.3,ab1:.2}),1.6,{...YOU,dir:look>0?1:-1,expr:'thinking'}) };

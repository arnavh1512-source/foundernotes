// scenes6.js: reference-led shot library (owner-approved pilot, Night 1 Part 2 excerpt, 2026-11-27).
// One new picture per idea (~3 s), a visual metaphor per sentence, mixed framing (wide/mid/close-up/insert),
// flat colour-band backgrounds that change per shot, one or two big words at most, and a full action in every shot
// (anticipation -> action -> reaction). Scenes are named p_*; use them as examples and helpers, not as a fixed set.
const camS=()=>cam(960,540,1/1.18);
const PKID={col:'#3d7fa8'};
const PAL=[['#efd9a7','#e3b77a','#cf8f5a','#b9774a'],['#cfe0e6','#f1e6cf','#9db58a','#7f9a6c'],['#e9e2cf','#e7c777','#d98f6a','#a9674a'],
 ['#c7d6e2','#9fb6c9','#6f8aa3','#53687e'],['#f2dcc0','#e6a98a','#c46f55','#8f4f3e'],['#e8e4d8','#cfd8c2','#a8bb93','#7f936b'],
 ['#f0e3c4','#c9d7d9','#8fb1b8','#5f8c94'],['#bfe0ef','#e6eef0','#b9c99a','#7d8c6a'],['#ddd6e8','#c4b7d6','#9a89b4','#6f6189']];
function titleTop(t,k,sz=84,col=INK){ if(k<=0) return; x.save(); x.globalAlpha=Math.min(1,k); x.fillStyle=col; x.font=`700 ${sz}px Inst`; x.textAlign='center'; x.textBaseline='middle';
  x.translate(960,120); const sc=.85+.15*back(Math.min(1,k)); x.scale(sc,sc); x.fillText(t,0,0); x.restore() }
function banner(t,X,Y,k=1){ if(k<=0) return; x.save(); x.globalAlpha=Math.min(1,k); x.translate(X,Y); x.font='700 54px Inst'; const w=x.measureText(t).width+90;
  x.fillStyle='#d9c79f'; x.beginPath(); x.moveTo(-w/2-50,-6); x.lineTo(-w/2,-6); x.lineTo(-w/2,44); x.lineTo(-w/2-50,44); x.lineTo(-w/2-28,19); x.fill(); x.beginPath(); x.moveTo(w/2+50,-6); x.lineTo(w/2,-6); x.lineTo(w/2,44); x.lineTo(w/2+50,44); x.lineTo(w/2+28,19); x.fill();
  x.fillStyle='#f6efdc'; x.strokeStyle=INK; x.lineWidth=4; x.beginPath(); x.rect(-w/2,-36,w,72); x.fill(); x.stroke(); x.fillStyle=INK; x.textAlign='center'; x.textBaseline='middle'; x.fillText(t,0,2); x.restore() }
function lbl(t,X,Y,sz=46,col=INK,k=1){ if(k<=0) return; x.save(); x.globalAlpha=Math.min(1,k); x.fillStyle=col; x.font=`700 ${sz}px Inst`; x.textAlign='center'; x.textBaseline='middle'; x.fillText(t,X,Y); x.restore() }
function pCloud(X,Y,r,col){ x.save(); x.fillStyle=col; x.beginPath(); x.arc(X-r*.9,Y,r*.7,0,7); x.arc(X,Y-r*.35,r,0,7); x.arc(X+r*.95,Y,r*.72,0,7); x.rect(X-r*.9,Y-r*.1,r*1.85,r*.8); x.fill(); x.restore() }
function closeUp(X,hy,p,o){ const s=o.s||4.2; return fig(X,p,s,{...o,y:hy+(TL+HR+5)*s,noShadow:1}) }
function car2(X,ts,s,o={}){ oldCar(X,ts,s,o); const b=Math.sin(ts*18)*3*(o.rattle??1), Y=G-40*s+b;
  x.save(); x.fillStyle='#dceaf0'; x.beginPath(); x.roundRect(X-68*s,Y-116*s,124*s,42*s,8*s); x.fill(); x.restore();
  if(o.noDriver) return; const hs=s*.62, J={hd:[X+12*s,Y-90*s]}; x.save(); x.beginPath(); x.rect(X-68*s,Y-118*s,124*s,46*s); x.clip();
  x.fillStyle=INK; x.beginPath(); x.arc(J.hd[0],J.hd[1],HR*hs,0,7); x.fill(); face(J,o.dir||1,hs,YOU,o.expr||'neutral',0,(NOW%3.6)<.13?1:0); x.restore();
  x.save(); x.fillStyle=RED; x.fillRect(J.hd[0]-14*hs,J.hd[1]+HR*hs-2,28*hs,8*hs); x.restore() }
function puff(X,Y,ts,n=3,col='#9a9387'){ x.save(); x.fillStyle=col; for(let i=0;i<n;i++){ const k=(ts*1.4+i/n)%1; x.globalAlpha=.5*(1-k); x.beginPath(); x.arc(X-k*120,Y-k*50,12+k*26,0,7); x.fill() } x.restore() }
function scribble(X,Y,r,seed,k=1){ x.save(); x.strokeStyle=INK; x.lineWidth=3; x.beginPath(); const n=Math.floor(40*k); for(let i=0;i<n;i++){ const a=rnd(seed+i*3)*7, rr2=r*(.2+rnd(seed+i*5)*.8); const px=X+Math.cos(a)*rr2, py=Y+Math.sin(a)*rr2*.7; i?x.quadraticCurveTo(X+Math.cos(a+1)*r*.6,Y+Math.sin(a+1)*r*.4,px,py):x.moveTo(px,py) } x.stroke(); x.restore() }
function bubble(X,Y,w,h,tx,ty){ x.save(); x.fillStyle='#fbf8ef'; x.strokeStyle=INK; x.lineWidth=5; x.beginPath(); x.ellipse(X,Y,w/2,h/2,0,0,7); x.fill(); x.stroke(); x.beginPath(); x.moveTo(X-20,Y+h/2-8); x.lineTo(tx,ty); x.lineTo(X+18,Y+h/2-6); x.fill(); x.stroke(); x.restore() }
function pTick(X,Y,s,k,col='#2f6f4f'){ if(k<=0) return; x.save(); x.strokeStyle=col; x.lineWidth=16*s; x.lineCap='round'; x.lineJoin='round'; const L1=40*s, L2=90*s; x.beginPath(); x.moveTo(X-40*s,Y); const a=Math.min(1,k*2); x.lineTo(X-40*s+L1*a*.7,Y+L1*a*.7); if(k>.5){ const b=(k-.5)*2; x.lineTo(X-40*s+L1*.7+L2*b*.7,Y+L1*.7-L2*b*.9) } x.stroke(); x.restore() }
function pencil(X,Y,rot){ x.save(); x.translate(X,Y); x.rotate(rot); x.fillStyle='#e7b64a'; x.fillRect(0,-12,200,24); x.fillStyle='#e9a0a0'; x.fillRect(200,-12,30,24); x.fillStyle='#f0d9b0'; x.beginPath(); x.moveTo(0,-12); x.lineTo(-36,0); x.lineTo(0,12); x.fill(); x.fillStyle=INK; x.beginPath(); x.moveTo(-24,-4); x.lineTo(-36,0); x.lineTo(-24,4); x.fill(); x.restore() }
function house(X,s,col='#b5543c'){ x.save(); x.translate(X,G); x.scale(s,s); x.fillStyle='#efe2c4'; x.strokeStyle=INK; x.lineWidth=6; x.fillRect(-90,-130,180,130); x.strokeRect(-90,-130,180,130); x.fillStyle=col; x.beginPath(); x.moveTo(-110,-128); x.lineTo(0,-210); x.lineTo(110,-128); x.closePath(); x.fill(); x.stroke(); x.fillStyle='#6b4a2f'; x.fillRect(-22,-70,44,70); x.fillStyle='#bfe0ef'; x.fillRect(40,-100,34,30); x.fillRect(-74,-100,34,30); x.restore() }
function arrowTo(X,Y,w,txt,dir,col){ x.save(); x.translate(X,Y); x.fillStyle=col; x.beginPath(); x.moveTo(-dir*w/2,-40); x.lineTo(dir*(w/2-40),-40); x.lineTo(dir*(w/2-40),-62); x.lineTo(dir*w/2+dir*20,0); x.lineTo(dir*(w/2-40),62); x.lineTo(dir*(w/2-40),40); x.lineTo(-dir*w/2,40); x.closePath(); x.fill();
  x.fillStyle='#f6f2e9'; x.font='700 40px Inst'; x.textAlign='center'; x.textBaseline='middle'; x.fillText(txt,-dir*20,2); x.restore() }
function pSun(X,Y,r,k){ x.save(); x.globalAlpha=k; x.fillStyle='#ffd45a'; x.beginPath(); x.arc(X,Y,r,0,7); x.fill(); x.strokeStyle='#ffd45a'; x.lineWidth=10; x.lineCap='round'; for(let i=0;i<12;i++){ const a=i/12*7+NOW*.3; x.beginPath(); x.moveTo(X+Math.cos(a)*r*1.25,Y+Math.sin(a)*r*1.25); x.lineTo(X+Math.cos(a)*r*1.6,Y+Math.sin(a)*r*1.6); x.stroke() } x.restore() }
const sfxShot={};

const MS=2.0; // mid-shot figure scale
function bands(i,yA=330,yB=590){ const p=PAL[i%PAL.length]; paper(p[0]);
  const band=(y0,y1,col,seed)=>{ x.fillStyle=col; x.beginPath(); x.moveTo(-60,y1); x.lineTo(-60,y0); for(let k=0;k<=24;k++){ const xx=-60+k*86; x.lineTo(xx,y0+Math.sin(k*1.7+seed)*3+rnd(k*7+seed)*4) } x.lineTo(1990,y1); x.closePath(); x.fill() };
  band(yA,1200,p[1],i*3+1); band(yB,1200,p[2],i*3+2); band(G,1200,p[3],i*3+3);
  x.save(); x.globalAlpha=.07; x.strokeStyle=INK; x.lineWidth=2; for(let k=0;k<34;k++){ const yy=yA+rnd(k*3+i)*(1080-yA), xx=rnd(k*7+i)*1920; x.beginPath(); x.moveTo(xx,yy); x.lineTo(xx+40+rnd(k)*110,yy+rnd(k+1)*3-1.5); x.stroke() } x.restore() }
function shadowAt(X,w,a=.14){ x.save(); x.globalAlpha=a; x.fillStyle=INK; x.beginPath(); x.ellipse(X,G+6,w,10,0,0,7); x.fill(); x.restore() }
function confetti(X,Y,k,n=26){ if(k<=0||k>=1) return; const C=[RED,'#e0a52b','#3d7fa8','#2f6f4f','#8a5a9a']; x.save(); for(let i=0;i<n;i++){ const a=rnd(i*5)*Math.PI*2, v=200+rnd(i*3)*420; x.fillStyle=C[i%5]; x.globalAlpha=1-k*.7; x.save(); x.translate(X+Math.cos(a)*v*k,Y+Math.sin(a)*v*k*.8+600*k*k); x.rotate(k*12+i); x.fillRect(-7,-4,14,8); x.restore() } x.restore() }
function armIK(S0,H,L1,L2,bend=1){ const dx=H[0]-S0[0], dy=H[1]-S0[1], D=Math.min(L1+L2-1,Math.hypot(dx,dy)), a=Math.atan2(dy,dx), c=Math.acos(cl((L1*L1+D*D-L2*L2)/(2*L1*D),-1,1)); return [S0[0]+Math.cos(a+bend*c)*L1,S0[1]+Math.sin(a+bend*c)*L1] }

// 10 "You can.": philosopher close-up
S.p_closePh=(u,ts,d)=>{ camS(); paper('#d8cde6'); rr(-400,640,2800,800,'#c4b7d6'); closeUp(1000,430,P({dir:-1,af1:.3,ab1:.2}),{...PHI,dir:-1,talk:1,s:4.2}) };
// 26 "Most of us pick the disappointment, because at least it is familiar": a queue at the grey door, none at the storm (wide)
S.p_queue=(u,ts,d)=>{ camS(); bands(5,300,600); doorway(220,1,210,330,{slab:'#9fb6c9'}); x.save(); x.fillStyle='#1d2a4a'; x.fillRect(270,G-330,160,330); x.restore(); lbl('ANXIETY',325,G-380,40,INK);
  doorway(1500,1,210,330,{slab:'#b7a98f'}); x.save(); x.fillStyle='#b8b8b8'; x.fillRect(1550,G-330,160,330); x.restore(); lbl('DISAPPOINTMENT',1605,G-380,40,INK);
  const cols=['#5e5a54','#7a4a24','#2f6f4f','#8a5a9a','#3d7fa8','#6b4a2f','#9c6b3c'];
  cols.forEach((c,i)=>{ const step=ts*.18, X=1460-i*95+step*95-(i===0?0:0); const in0=i===0?ph(ts,0,1.5):0; if(in0>=1) return; fig(lerp(X,1600,in0),walk(ts+i*.4,.5,.25,{dir:1}),.85,{col:c,a:1-in0*.8}) });
  const jx=lerp(400,1460-7*95+ts*.18*95,io(ph(ts,1.2,3.6))); fig(jx,ts>1.2&&ts<3.6?walk(ts,1.2,.8,{dir:1}):P({dir:1,head:.2}),.9,{...YOU,expr:'sad'}) };
// 1 sign crashes down; he jumps back and lands on his bottom (wide)
S.p_warn=(u,ts,d)=>{ camS(); bands(0); const k=back(ph(ts,.3,.75)), sw=ts>.75?.13*Math.sin((ts-.75)*6)*Math.exp(-(ts-.75)*1.2):0;
  if(ts>.75&&ts<1.05) SHAKE=Math.max(SHAKE,22*(1-(ts-.75)/.3)); if(ts>1.2&&ts<1.4) SHAKE=Math.max(SHAKE,10);
  x.save(); x.strokeStyle='#6d6a64'; x.lineWidth=6; const sy=lerp(-200,360,k); x.beginPath(); x.moveTo(700,-40); x.lineTo(700+Math.sin(sw)*60,sy-60); x.moveTo(1100,-40); x.lineTo(1100+Math.sin(sw)*60,sy-60); x.stroke(); x.restore();
  block(900+Math.sin(sw)*60,sy,620,150,'CONTROVERSIAL',sw,{fill:RED}); burst(900,sy+90,ph(ts,.75,1.1),130);
  const SITF={dir:-1,lf1:1.45,lf2:-.15,lb1:1.3,lb2:-.1,lean:-.25,af1:-.7,af2:.3,ab1:-.6,ab2:.3,head:.1};
  const pose=K(ts,[[0,{dir:-1,head:-.35}],[.7,{dir:-1,head:-.35,lean:.05,lf1:.25,lb1:-.2}],[.95,{dir:-1,lean:-.45,af1:2.6,ab1:2.5,af2:.6,ab2:.6,lf1:.6,lf2:-.9,lb1:-.3,lb2:-.6,air:70},'out'],[1.25,SITF,'inn'],[d,{...SITF,head:-.2}]]);
  const X=lerp(1380,1560,io(ph(ts,.75,1.25))); if(ts>.75&&ts<1.25) ghost(t=>lerp(1380,1560,io(ph(t,.75,1.25))),t=>K(t,[[.75,{dir:-1}],[.95,{dir:-1,lean:-.45,af1:2.6,ab1:2.5,air:70}],[1.25,SITF]]),ts,1.5,{...YOU,dir:-1,noFace:1});
  fig(X,pose,1.5,{...YOU,dir:-1,expr:ts>.75?'shocked':'thinking'}); dust(1560,ph(ts,1.25,1.8),6,.8) };
// 2 tries on pairs of glasses; the whole world takes the colour of each lens (mid)
S.p_glasses=(u,ts,d)=>{ camS(); const cols=['#d8342b','#3d7fa8','#2f6f4f','#c9a46a'], sw=[.45,1.15,1.75], idx=ts<sw[0]?-1:ts<sw[1]?0:ts<sw[2]?1:2;
  bands(1,300,560); banner('ADLER',960,130,ph(ts,0,.3)); rr(380,575,560,20,'#6b4a2f'); shadowAt(660,240,.08);
  cols.forEach((c,i)=>{ if(i<=idx&&i<3) return; const gx=460+i*140; x.save(); x.strokeStyle=c; x.lineWidth=8; x.beginPath(); x.arc(gx-22,555,20,0,7); x.moveTo(gx+42,555); x.arc(gx+22,555,20,0,7); x.stroke(); x.restore() });
  // arm: reach to the shelf just before each swap, then to the face
  let reach=0; sw.forEach(t0=>{ reach=Math.max(reach,ph(ts,t0-.35,t0-.15)-ph(ts,t0-.1,t0+.05)) });
  const p=P({dir:-1,lean:.06+.12*reach,af1:lerp(.75,1.5,reach),af2:lerp(2.45,.15,reach),head:.05*Math.sin(ts*3)});
  const J=fig(1250,p,MS,{...YOU,dir:-1,expr:idx>=2?'happy':idx>=0?'thinking':'neutral'});
  if(idx>=0){ const c=cols[idx]; x.save(); x.strokeStyle=c; x.lineWidth=7; const gx=J.hd[0]-10, gy=J.hd[1]-6; x.beginPath(); x.arc(gx-20,gy,19,0,7); x.moveTo(gx+39,gy); x.arc(gx+20,gy,19,0,7); x.stroke(); x.restore();
    x.save(); x.setTransform(1,0,0,1,0,0); x.globalAlpha=.16*cl((ts-sw[idx])/.2); x.fillStyle=c; x.fillRect(0,0,W,H); x.restore() }
  if(idx>=1){ const t0=sw[idx], k=ph(ts,t0,t0+.6); if(k>0&&k<1){ const c=cols[idx-1]; x.save(); x.translate(lerp(J.hd[0],J.hd[0]+260,k),J.hd[1]-6-Math.sin(k*Math.PI)*160+k*200); x.rotate(k*9); x.strokeStyle=c; x.lineWidth=7; x.beginPath(); x.arc(-20,0,19,0,7); x.moveTo(39,0); x.arc(20,0,19,0,7); x.stroke(); x.restore() } } };
// 3 blows out the candles, then jumps for joy in confetti (mid)
S.p_cake=(u,ts,d)=>{ camS(); paper('#f1e6d0'); rr(-400,G,2800,600,'#dccdaf'); titleTop('10',ph(ts,0,.3),120); table(700,420,170); const blow=ph(ts,.7,1.2);
  x.save(); x.fillStyle='#f6f2e9'; x.strokeStyle=INK; x.lineWidth=6; x.beginPath(); x.roundRect(760,G-260,300,90,12); x.fill(); x.stroke(); x.fillStyle='#e9a0a0'; x.fillRect(760,G-232,300,18); x.restore();
  for(let i=0;i<10;i++){ const cx=780+i*29; x.fillStyle=['#3d7fa8','#d8342b','#e0a52b'][i%3]; x.fillRect(cx-5,G-310,10,50); if(blow*10<=i){ x.save(); x.fillStyle='#ffb03a'; x.beginPath(); x.ellipse(cx+(blow>0?-6:0),G-324+Math.sin(NOW*14+i)*2,7,14,blow>0?-.5:0,0,7); x.fill(); x.restore() } else { x.save(); x.globalAlpha=.4*(1-ph(ts,1.3,d)); x.strokeStyle='#8a8072'; x.lineWidth=3; x.beginPath(); x.moveTo(cx,G-316); x.quadraticCurveTo(cx-10+Math.sin(NOW*3+i)*8,G-350,cx+4,G-390); x.stroke(); x.restore() } }
  const p=K(ts,[[0,{dir:-1,af1:.9,af2:.6}],[.55,{dir:-1,lean:-.18,af1:.9,af2:.6,head:-.15},'io'],[.75,{dir:-1,lean:.4,af1:.5,af2:.3,head:.1},'out'],[1.25,{dir:-1,lean:.3}],[1.45,{dir:-1,lean:-.05,lf1:.5,lf2:-.6,lb1:.3,lb2:-.6}],[1.7,{dir:-1,lean:0,af1:2.9,ab1:2.8,af2:.2,ab2:.2,air:60},'out'],[1.95,{dir:-1,af1:2.7,ab1:2.6,af2:.4,ab2:.4},'inn'],[d,{dir:-1,af1:2.6,ab1:2.5,af2:.5,ab2:.5,air:30*Math.abs(Math.sin((ts-1.95)*8))}]]);
  fig(1210,p,1.6,{...PKID,dir:-1,expr:ts>1.3?'happy':'neutral'}); confetti(1000,G-420,ph(ts,1.5,d));
  if(blow>0&&blow<1){ x.save(); x.strokeStyle='#9fc4d8'; x.lineWidth=4; for(let i=0;i<3;i++){ x.beginPath(); x.moveTo(1140-i*10,G-360+i*20); x.lineTo(1140-80-blow*120,G-360+i*20); x.stroke() } x.restore() } };
// 4 sleepwalking on a moving walkway: carried along without choosing (wide)
S.p_sleep=(u,ts,d)=>{ camS(); bands(3,280,560); x.save(); x.fillStyle='#f6e7b0'; x.beginPath(); x.arc(1560,180,46,0,7); x.fill(); x.fillStyle=PAL[3][0]; x.beginPath(); x.arc(1580,166,40,0,7); x.fill(); x.restore();
  x.save(); x.fillStyle='#5e5a54'; x.fillRect(200,G-30,1520,30); x.fillStyle=INK; for(let i=0;i<16;i++){ x.save(); x.translate(230+i*98,G-15); x.rotate(ts*8); x.fillRect(-12,-2,24,4); x.restore(); x.beginPath(); x.arc(230+i*98,G-15,12,0,7); x.strokeStyle='#cfc7b6'; x.lineWidth=3; x.stroke() }
  x.strokeStyle='#8a857e'; x.lineWidth=3; for(let i=0;i<20;i++){ const xx=200+((i*80+ts*260)%1520); x.beginPath(); x.moveTo(xx,G-30); x.lineTo(xx+30,G-30); x.stroke() } x.restore();
  const X=lerp(420,1380,ts/d); fig(X,walk(ts,.7,.4,{af1:1.5,af2:.05,ab1:1.45,ab2:.05,head:.12,lean:.02}),1.5,{...PKID,y:G-30-(TH+SH)*1.5+2,expr:'calm'});
  for(let i=0;i<3;i++){ const k=(ts*.6+i/3)%1; lbl('z',X+40+k*90,G-330-k*140,34+k*30,'#f6f2e9',1-k) } };
// 5 the four pushes land as real hits; on "push hard" they all shove at once (wide)
S.p_push=(u,ts,d)=>{ camS(); bands(2); const P5=[[.09,'RACE',-1,430],[.87,'CULTURE',1,430],[1.61,'FAMILY',-1,650],[2.41,'HOME',1,650]], shove=ph(ts,3.8,4.0)-ph(ts,4.5,5.0);
  let off=0, lean=0, hitNow=0; P5.forEach(([t0,w,side,y],i)=>{ const k=back(ph(ts,t0,t0+.35)); if(k<=0) return; const hitT=ts-(t0+.35);
    const tx=960+side*300-side*90*io(Math.max(0,shove)), X=lerp(960+side*1400,tx,k); arrowTo(X,y,w.length>5?360:300,w,-side,['#5e5a54','#2f6f4f','#3d7fa8','#6b4a2f'][i]);
    if(hitT>0){ const j=Math.exp(-hitT*3)*Math.sin(Math.min(hitT*9,Math.PI)); off+=-side*70*j; lean+=-side*.35*j; if(hitT<.2){ SHAKE=Math.max(SHAKE,12); hitNow=1 } } });
  if(shove>0){ SHAKE=Math.max(SHAKE,18*shove) }
  const s=1.5*(1-.18*Math.max(0,shove)); fig(960+off+Math.sin(ts*30)*8*Math.max(0,shove),P({lean:lean,af1:1.2+.5*Math.max(0,shove),ab1:1.1+.5*Math.max(0,shove),af2:1.4,ab2:1.4,lf1:.2,lb1:-.2,head:.08*Math.sin(ts*5)}),s,{...PKID,dir:off>0?-1:1,expr:shove>0||hitNow?'worried':'thinking'}) };
// 6 tries the wrong outline (doesn't fit), then steps into his own (mid)
S.p_settle=(u,ts,d)=>{ camS(); bands(4,300,600); const fill=ph(ts,2.0,2.3), fade=ph(ts,2.3,3.0);
  const OUT=[[560,{lean:-.05,af1:.2,ab1:-.2},1.25],[1360,{af1:1.0,ab1:-1.0,af2:.2,ab2:-.2},2.45],[960,{af1:.35,ab1:-.3},MS]];
  OUT.forEach(([ox,pp,sc],i)=>{ if(i!==2&&fade>=1) return; x.save(); x.globalAlpha=i===2?1-fill:.9*(1-fade); x.setLineDash([16,12]); fig(ox,P(pp),sc,{col:'#f6f2e9',lw:.5,noShadow:1,noFace:1}); x.restore() });
  let X, p; if(ts<.8){ X=lerp(160,560,io(ph(ts,0,.8))); p=walk(ts,1.6,.9,{dir:1}) } else if(ts<1.5){ X=560; const sq=Math.sin(ph(ts,.8,1.4)*Math.PI); p=P({dir:1,lean:-.1*sq,af1:.2+1.2*sq,ab1:-.2-1.0*sq,head:.2*sq}); if(ts>1.25&&ts<1.45) SHAKE=8 }
  else if(ts<2.0){ X=lerp(560,960,io(ph(ts,1.5,2.0))); p=walk(ts,1.8,.9,{dir:1}) } else { X=960; p=K(ts-2.0,[[0,{dir:1,air:18,lean:-.1}],[.3,{dir:1}],[d,{dir:1,af1:.35,ab1:-.3}]]) }
  fig(X,p,MS,{...YOU,expr:ts>2.3?'calm':ts>.8&&ts<1.5?'worried':'thinking'}); if(ts>1.1&&ts<1.5) lbl('✕',560,G-560,120,RED,1-ph(ts,1.35,1.5));
  if(fill>0&&fill<1) burst(960,G-230,fill,160,'#f6f2e9') };
// 7 a real stick arm holds the pencil, erases the tick and redraws it (insert)
S.p_tick=(u,ts,d)=>{ camS(); paper('#e8dcc2'); x.save(); x.translate(960,470); x.rotate(-.03); x.fillStyle='#fbf8ef'; x.shadowColor='rgba(0,0,0,.15)'; x.shadowBlur=20; x.fillRect(-460,-330,920,640); x.restore();
  [[700,330],[700,560]].forEach(([bx,by])=>{ x.save(); x.strokeStyle=INK; x.lineWidth=7; x.strokeRect(bx-60,by-60,120,120); x.restore() }); x.save(); x.fillStyle='#cfc7b6'; [[820,330],[820,560]].forEach(([lx,ly])=>{ x.fillRect(lx,ly-14,360,12); x.fillRect(lx,ly+12,260,12) }); x.restore();
  const er=ph(ts,.7,1.3), nw=ph(ts,1.6,2.3); x.save(); x.globalAlpha=1-er; pTick(705,320,1,1); x.restore(); pTick(705,550,1,nw);
  let px,py; if(ts<.4){ px=lerp(1500,720,io(ph(ts,0,.4))); py=lerp(900,330,io(ph(ts,0,.4))) } else if(ts<1.4){ px=720+Math.sin(ts*30)*28; py=330 } else if(ts<2.4){ px=lerp(680,780,nw); py=lerp(560,520,nw) } else { px=lerp(780,1500,io(ph(ts,2.4,2.9))); py=lerp(520,900,io(ph(ts,2.4,2.9))) }
  const rot=-.6; if(ts>.7&&ts<1.3){ x.save(); x.fillStyle='#d9c9b0'; for(let i=0;i<6;i++){ x.beginPath(); x.arc(700+rnd(i)*80+Math.sin(ts*9+i)*10,380+rnd(i+4)*40+(ts-.7)*80,5,0,7); x.fill() } x.restore() }
  pencil(px,py,rot); const Hd=[px+150*Math.cos(rot),py+150*Math.sin(rot)], S0=[1500,1180], El=armIK(S0,Hd,560,560,-1);
  x.save(); x.strokeStyle=INK; x.lineWidth=26; x.lineCap='round'; x.lineJoin='round'; x.beginPath(); x.moveTo(...S0); x.lineTo(...El); x.lineTo(...Hd); x.stroke(); x.fillStyle=INK; x.beginPath(); x.ellipse(Hd[0],Hd[1],24,20,rot,0,7); x.fill(); x.restore() };
// 9 tugs at his concrete-stuck feet so hard he falls flat on his face (mid)
S.p_stuck=(u,ts,d)=>{ camS(); bands(5); x.save(); x.strokeStyle=RED; x.lineWidth=14; x.lineCap='round'; x.beginPath(); x.moveTo(880,G-30); x.lineTo(1040,G+30); x.moveTo(1040,G-30); x.lineTo(880,G+30); x.stroke(); x.restore();
  const tug=Math.sin(ts*(7+ts*3)), hard=ph(ts,0,1.4), give=ph(ts,1.5,1.9);
  const p=P({lean:lerp(.15+.4*Math.abs(tug)*(.5+hard*.5),-.05,give),af1:lerp(1.4+.5*tug,.1,give),ab1:lerp(1.3-.5*tug,-.1,give),af2:lerp(.3,.1,give),ab2:lerp(.3,.1,give),head:lerp(.1,.45,give)+.12*Math.sin(ts*12)*give});
  fig(960,p,MS,{...YOU,y:G-(TH+SH)*MS,expr:ts>1.5?'sad':'angry'}); if(Math.abs(tug)>.97&&ts<1.5) SHAKE=Math.max(SHAKE,5+8*hard);
  x.save(); x.fillStyle='#9a9590'; x.strokeStyle=INK; x.lineWidth=5; x.beginPath(); x.roundRect(860,G-60,200,70,10); x.fill(); x.stroke(); x.fillStyle='#86817c'; for(let i=0;i<8;i++){ x.beginPath(); x.arc(880+rnd(i)*160,G-40+rnd(i+2)*40,4,0,7); x.fill() } x.restore() };
// 11 runs and hurdles through changing worlds (wide)
S.p_anyEnv=(u,ts,d)=>{ camS(); const i=Math.floor(ts/1.0)%4, wk=[7,3,0,5][i]; bands(wk);
  if(i===1){ x.save(); for(let k=0;k<20;k++){ x.fillStyle='rgba(255,250,220,.8)'; x.beginPath(); x.arc(rnd(k*7)*1920,rnd(k*3)*300,2.5,0,7); x.fill() } x.restore() }
  if(i===2) pSun(1500,170,50,1); if(i===3){ x.save(); x.fillStyle='#fff'; for(let k=0;k<40;k++){ x.beginPath(); x.arc((rnd(k)*1920+NOW*30)%1920,(rnd(k+5)*800+NOW*120)%800,4,0,7); x.fill() } x.restore() } if(i===0) pCloud(500,170,50,'#fff');
  x.save(); x.translate(1660,180); x.fillStyle='#fbf8ef'; x.strokeStyle=INK; x.lineWidth=6; x.beginPath(); x.arc(0,0,70,0,7); x.fill(); x.stroke(); x.lineCap='round'; x.lineWidth=7; x.rotate(ts*8); x.beginPath(); x.moveTo(0,0); x.lineTo(0,-55); x.stroke(); x.rotate(-ts*8+ts*.7); x.beginPath(); x.moveTo(0,0); x.lineTo(0,-35); x.stroke(); x.restore();
  const X=lerp(250,1500,ts/d); [[.55,'#8a857e'],[1.55,'#6d6a64'],[2.55,'#8a857e'],[3.4,'#5e5a54']].forEach(([t0,c])=>{ const rx=lerp(250,1500,(t0+.12)/d); x.save(); x.fillStyle=c; x.beginPath(); x.ellipse(rx,G-18,46,26,0,Math.PI,0); x.fill(); x.restore() });
  let air=0; [.55,1.55,2.55,3.4].forEach(t0=>{ const k=ph(ts,t0-.15,t0+.3); if(k>0&&k<1) air=Math.max(air,Math.sin(k*Math.PI)*90) });
  fig(X,run(ts,2.4,{dir:1,air:air}),1.4,{...YOU,expr:'calm'}) };
// 12 the door opens; he slams it shut, then kicks it shut the second time (mid)
S.p_doorShut=(u,ts,d)=>{ camS(); bands(6,300,600); const seg=ts<2.1?0:1, t=ts-seg*2.1, op=ph(t,.15,.6)-ph(t,1.45,1.6);
  doorway(1080,op,250,460); const hitT=1.6;
  let p; if(seg===0) p=K(t,[[0,{dir:1}],[.9,{dir:1,head:.1}],[1.2,{dir:1,lean:-.15,af1:2.2,af2:.6},'out'],[1.5,{dir:1,af1:1.6,af2:.05,lean:.3},'inn'],[2.1,{dir:1,af1:.4}]]);
  else p=K(t,[[0,{dir:1}],[1.0,{dir:1,lf1:-.7,lf2:-.6,lean:-.15}],[1.45,{dir:1,lf1:1.6,lf2:-.05,lb1:-.2,lean:-.3,af1:-.6,ab1:1.2},'out'],[2.2,{dir:1}]]);
  fig(seg===0?lerp(820,880,ph(t,.6,1.2)):900,p,MS,{...YOU,expr:op>.5?'worried':t>hitT?'angry':'neutral'});
  if(t>hitT&&t<hitT+.25){ SHAKE=Math.max(SHAKE,18); burst(1090,G-240,(t-hitT)/.25,110) } };
// 14 close-up: a question mark pops, he scratches his head
S.p_closeYo=(u,ts,d)=>{ camS(); paper('#e7d3b6'); rr(-400,620,2800,800,'#d5bb95'); const q=back(ph(ts,.4,.75)), q2=back(ph(ts,1.0,1.3));
  const scr=ph(ts,1.1,1.4); closeUp(820,440,P({dir:1,head:-.12+.06*Math.sin(ts*2),af1:lerp(.15,1.0,scr),af2:lerp(.1,2.8+.12*Math.sin(ts*14)*scr,scr),ab1:.1,ab2:.1,hF:scr>.5?'fist':null}),{...YOU,dir:1,noTalk:1,expr:ts<1.0?'angry':'thinking',s:4.2});
  [[1380,330,300,q,.1],[1600,220,150,q2,-.2]].forEach(([qx,qy,sz,k,r])=>{ if(k<=0) return; x.save(); x.translate(qx,qy); x.scale(k,k); x.rotate(r*Math.sin(ts*3)); x.fillStyle=RED; x.font=`700 ${sz}px Inst`; x.textAlign='center'; x.textBaseline='middle'; x.fillText('?',0,0); x.restore() }) };
// 15 the pencil sketches a car, and the sketch drives off the page
S.p_sketch=(u,ts,d)=>{ camS(); paper('#e8dcc2'); x.save(); x.fillStyle='#fbf8ef'; x.fillRect(420,160,1080,620); x.restore();
  const path=[[600,600],[600,520],[700,500],[760,400],[1060,400],[1140,500],[1300,520],[1320,600]]; let L=0; for(let i=1;i<path.length;i++) L+=Math.hypot(path[i][0]-path[i-1][0],path[i][1]-path[i-1][1]);
  const k=io(ph(ts,.1,1.5)), go=inn(ph(ts,1.9,2.7)), dx=go*1300, bob=go>0?Math.sin(ts*30)*4:0; x.save(); x.beginPath(); x.rect(420,160,1080,620); x.clip(); x.translate(dx,bob);
  x.strokeStyle=INK; x.lineWidth=8; x.lineCap='round'; x.lineJoin='round'; x.setLineDash([L*k,L+10]); x.beginPath(); path.forEach((p,i)=>i?x.lineTo(...p):x.moveTo(...p)); x.stroke(); x.setLineDash([]);
  const w=ph(ts,1.5,1.85); [[730,600],[1190,600]].forEach(([cx,cy])=>{ x.beginPath(); x.arc(cx,cy,55,0,7*w); x.stroke(); if(w>=1){ x.save(); x.translate(cx,cy); x.rotate(ts*20*go); x.beginPath(); x.moveTo(-40,0); x.lineTo(40,0); x.stroke(); x.restore() } });
  if(go>0) speed(600,560,260,go,1); x.restore();
  let acc=0, tip=path[0]; for(let i=1;i<path.length;i++){ const sl=Math.hypot(path[i][0]-path[i-1][0],path[i][1]-path[i-1][1]); if(acc+sl>=L*k){ const f=(L*k-acc)/sl; tip=[lerp(path[i-1][0],path[i][0],f),lerp(path[i-1][1],path[i][1],f)]; break } acc+=sl; tip=path[i] }
  if(ts>1.5&&ts<1.9) tip=[lerp(1320,1190,ph(ts,1.5,1.85)),600-50*Math.sin(ph(ts,1.5,1.85)*6)]; const lift=ph(ts,1.85,2.3), pt=[tip[0]+lift*300,tip[1]-lift*420];
  pencil(pt[0]+2,pt[1]-2,-.55); const Hd=[pt[0]+130*Math.cos(-.55),pt[1]+130*Math.sin(-.55)], S0=[1800,-60], El=armIK(S0,Hd,600,600,1);
  x.save(); x.strokeStyle=INK; x.lineWidth=26; x.lineCap='round'; x.lineJoin='round'; x.beginPath(); x.moveTo(...S0); x.lineTo(...El); x.lineTo(...Hd); x.stroke(); x.fillStyle=INK; x.beginPath(); x.ellipse(Hd[0],Hd[1],24,20,-.55,0,7); x.fill(); x.restore() };
// 16 driving: trees rush past, the car hops on two bumps (wide)
S.p_drive=(u,ts,d)=>{ camS(); bands(7,300,560); pCloud(400,170,46,'#fff'); pCloud(1400,120,40,'#fff');
  for(let i=0;i<6;i++){ const tx=((i*420-ts*500)%2520+2520)%2520-300; rr(tx,G-330,22,270,'#6b5a3e'); pCloud(tx+11,G-350,70,'#7f9a68') }
  x.save(); x.fillStyle='#9aa3a8'; x.fillRect(-400,G-60,2800,60); x.strokeStyle='#f1eee6'; x.lineWidth=6; x.setLineDash([50,40]); x.lineDashOffset=ts*600; x.beginPath(); x.moveTo(-400,G-30); x.lineTo(2400,G-30); x.stroke(); x.restore();
  let hop=0; [1.5,2.8].forEach(t0=>{ const k=ph(ts,t0,t0+.4); if(k>0&&k<1) hop=Math.max(hop,Math.sin(k*Math.PI)*50) });
  const X=lerp(650,1150,ts/d); x.save(); x.translate(0,-hop); car2(X,ts,1.7,{expr:hop>10?'happy':'calm'}); x.restore(); puff(X-280,G-70,ts,4); for(let t0 of [1.5,2.8]){ if(ts>t0+.38&&ts<t0+.6) SHAKE=Math.max(SHAKE,10) } };
// 17 rattles, shakes and swerves to one side, leaving skid marks (close)
S.p_rattle=(u,ts,d)=>{ camS(); bands(7,250,520); x.save(); x.fillStyle='#9aa3a8'; x.fillRect(-400,G-60,2800,60); x.restore(); const pull=Math.sin(ph(ts,.9,2.3)*Math.PI*2);
  x.save(); x.strokeStyle='rgba(30,30,30,.35)'; x.lineWidth=10; x.beginPath(); for(let i=0;i<=20;i++){ const xx=i*48; x.lineTo(xx,G-20+Math.sin(i*.5-ts*4)*14*Math.min(1,ts)) } x.stroke(); x.restore();
  SHAKE=7; x.save(); x.translate(960+pull*90,0); x.rotate(-.06*pull); x.translate(-960,0); car2(960,ts*1.7,2.4,{rattle:2.8,expr:'worried'}); x.restore();
  for(let i=0;i<3;i++){ const k=(ts*1.8+i/3)%1; x.save(); x.globalAlpha=.5*(1-k); x.fillStyle='#f1eee6'; x.beginPath(); x.arc(1240+pull*90+k*60,G-290-k*120,16+k*30,0,7); x.fill(); x.restore() }
  [0,.45,.9].forEach((t0,i)=>{ const k=ph(ts,t0+.2,t0+1.1); if(k<=0||k>=1) return; const bx=900+i*120+k*(i-1)*260, by=G-280-Math.sin(k*Math.PI)*260+k*240; x.save(); x.fillStyle='#6d6a64'; x.beginPath(); x.arc(bx,by,11,0,7); x.fill(); x.restore() }) };
// 18 relaxed driver close-up: leaning back, one hand on a proper wheel, the other behind his head, whistling
S.p_driverCU=(u,ts,d)=>{ camS(); paper('#cfe5ef'); for(let i=0;i<5;i++){ const px=((i*500-ts*900)%2500+2500)%2500-300; rr(px,300,24,500,'#7d8c6a'); pCloud(px+12,280,60,'#9db58a') }
  rr(-400,0,2800,190,'#b9a98c'); rr(-400,800,2800,400,'#a8987a'); rr(-400,190,400,630,'#b9a98c'); rr(1700,190,600,630,'#b9a98c');
  const J=closeUp(800,450,P({dir:1,lean:-.12,af1:1.05,af2:.55,ab1:2.9,ab2:2.5,head:-.05+.04*Math.sin(ts*2),hF:'fist'}),{...YOU,dir:1,noTalk:1,expr:'calm',s:3.4});
  const WX=1230, WY=700; x.save(); x.translate(WX,WY); x.rotate(.06*Math.sin(ts*1.4)); x.strokeStyle='#2a2a2e'; x.lineWidth=28; x.beginPath(); x.arc(0,0,175,0,7); x.stroke(); x.lineWidth=20; [0,2.1,4.2].forEach(a=>{ x.beginPath(); x.moveTo(0,0); x.lineTo(Math.cos(a+1.57)*165,Math.sin(a+1.57)*165); x.stroke() }); x.fillStyle='#2a2a2e'; x.beginPath(); x.arc(0,0,44,0,7); x.fill(); x.fillStyle='#d8342b'; x.beginPath(); x.arc(0,0,16,0,7); x.fill(); x.restore();
  for(let i=0;i<3;i++){ const k=(ts*.7+i/3)%1; lbl('♪',J.hd[0]+120+k*120,J.hd[1]-40-k*160,50,INK,1-k) } };
// 19 tiptoes up to the covered car, lifts the sheet, and jumps back (wide, showroom)
S.p_newCar=(u,ts,d)=>{ camS(); paper('#3b3f52'); rr(-400,G,2800,600,'#2c2f3d'); x.save(); const g=x.createRadialGradient(1060,G-120,40,1060,G-120,520); g.addColorStop(0,'rgba(255,240,200,.55)'); g.addColorStop(1,'rgba(255,240,200,0)'); x.fillStyle=g; x.fillRect(400,0,1300,1080); x.restore();
  const lift=ph(ts,2.0,2.3)-ph(ts,2.7,3.1); if(lift>0) car2(1060,0,1.7,{col:'#3d7fa8',rattle:0,noDriver:1});
  x.save(); x.fillStyle='#ece6da'; x.strokeStyle='#bfb6a6'; x.lineWidth=4; const r=Math.sin(ts*2)*6; x.beginPath(); x.moveTo(760-lift*60,G-lift*90); x.quadraticCurveTo(780+r,G-150-lift*40,880,G-170); x.quadraticCurveTo(960,G-290-r,1110,G-280); x.quadraticCurveTo(1260,G-260+r,1300,G-150); x.quadraticCurveTo(1340,G-60,1360,G); x.lineTo(760,G); x.fill(); x.stroke(); x.restore();
  if(lift>.5){ x.save(); x.strokeStyle='#fff7d0'; x.lineWidth=5; for(let i=0;i<6;i++){ const a=i/6*7; x.beginPath(); x.moveTo(820+Math.cos(a)*30,G-110+Math.sin(a)*30); x.lineTo(820+Math.cos(a)*70,G-110+Math.sin(a)*70); x.stroke() } x.restore() }
  lbl('?',1060,G-170,150,RED,ph(ts,.3,.6)*(1-lift));
  let X, p; if(ts<1.7){ X=lerp(380,660,ts/1.7); p=walk(ts,.9,.6,{dir:1,lean:.25,af1:1.2,af2:1.4,ab1:.9,ab2:1.4,air:0}) } else if(ts<2.7){ X=660; p=P({dir:1,lean:.4,af1:1.3,af2:.2,head:.15}) } else { X=lerp(660,420,out(ph(ts,2.7,3.1))); p=K(ts-2.7,[[0,{dir:1,lean:-.4,af1:2.6,ab1:2.5,air:50}],[.4,{dir:1,lean:-.1}],[d,{dir:1}]]) }
  fig(X,p,1.5,{...YOU,expr:ts>2.7?'shocked':'thinking'}) };
// 20 steps toward the fog, then pulls his foot back (wide, dark)
S.p_fog=(u,ts,d)=>{ camS(); paper('#1f2638'); rr(-400,G,2800,600,'#161b28'); x.save(); x.fillStyle='#3a4256'; x.beginPath(); x.moveTo(820,G); x.lineTo(1880,G); x.lineTo(1500,520); x.lineTo(1420,520); x.closePath(); x.fill(); x.restore();
  x.save(); for(let i=0;i<12;i++){ const fx=900+((i*230+ts*60*(1+i%3))%1300), fy=380+rnd(i)*260; x.globalAlpha=.2; x.fillStyle='#cfd6e2'; x.beginPath(); x.arc(fx,fy,120+rnd(i+3)*120,0,7); x.fill() } x.restore();
  const p=K(ts,[[0,{dir:1,head:.15}],[.6,{dir:1,head:.2,lean:.15}],[1.1,{dir:1,lean:.3,lf1:.7,lf2:-.2,af1:.6,ab1:-.3},'io'],[1.35,{dir:1,lean:-.3,lf1:-.2,af1:1.6,ab1:1.5,af2:.8,ab2:.8},'out'],[d,{dir:1,lean:-.1,af1:1.0,ab1:.9,af2:1.6,ab2:1.6}]]);
  fig(lerp(700,640,ph(ts,1.1,1.4)),p,1.25,{...YOU,col:'#e8e2d4',expr:ts>1.1?'shocked':'worried'}) };
// 21 trembling close-up, arms wrapped round himself, sweat drop
S.p_fear=(u,ts,d)=>{ camS(); paper('#262c3e'); const j=Math.sin(ts*40)*.012; closeUp(960,450,P({dir:1,rot:j,af1:.45,af2:-1.9,ab1:.35,ab2:-1.8,head:.05}),{...YOU,dir:1,noTalk:1,expr:'worried',s:4.0});
  const k=ph(ts,.2,1.4); x.save(); x.fillStyle='#9fd3ff'; x.beginPath(); const sx=1070, sy=lerp(330,430,k); x.moveTo(sx,sy-24); x.quadraticCurveTo(sx+16,sy,sx,sy+10); x.quadraticCurveTo(sx-16,sy,sx,sy-24); x.fill(); x.restore() };
// 22 grumbling and shaking a fist out of the window, the car laps round again (wide)
S.p_loop=(u,ts,d)=>{ camS(); bands(0,300,560); x.save(); x.fillStyle='#9aa3a8'; x.fillRect(-400,G-60,2800,60); x.restore(); const lap=d/2, t=ts%lap, X=lerp(-250,2170,t/lap), b=Math.abs(Math.sin(ts*7))*6;
  x.save(); x.translate(0,-b); car2(X,ts,1.5,{expr:'angry'}); const sh=[X+70,G-40*1.5-100], fh=[X+150,G-40*1.5-150+Math.sin(ts*18)*12]; x.strokeStyle=INK; x.lineWidth=14; x.lineCap='round'; x.beginPath(); x.moveTo(...sh); x.lineTo(fh[0]-20,fh[1]+30); x.lineTo(...fh); x.stroke(); x.fillStyle=INK; x.beginPath(); x.arc(fh[0],fh[1],12,0,7); x.fill(); x.restore();
  puff(X-250,G-70,ts,4); bubble(X+20,G-450,240,150,X+20,G-310); scribble(X+20,G-450,80,Math.floor(ts*6)) };
// 23 two doors burst up out of the ground with dust (wide)
S.p_twoDoors=(u,ts,d)=>{ camS(); bands(5,300,600); titleTop('2',ph(ts,1.6,1.9),120);
  const a=back(ph(ts,.4,.85)), b=back(ph(ts,.9,1.35)); x.save(); x.translate(0,(1-a)*520); doorway(330,0,240,440,{slab:'#9fb6c9'}); x.restore(); x.save(); x.translate(0,(1-b)*520); doorway(1350,0,240,440,{slab:'#b7a98f'}); x.restore();
  dust(450,ph(ts,.75,1.3),6,1); dust(1470,ph(ts,1.25,1.8),6,1); if((ts>.75&&ts<.95)||(ts>1.25&&ts<1.45)) SHAKE=Math.max(SHAKE,12);
  const jump=ts>.8&&ts<1.1?Math.sin(ph(ts,.8,1.1)*Math.PI)*40:0, look=ts<1.4?(ts<1.1?-1:1):Math.sin((ts-1.4)*2.4);
  fig(960,P({dir:look>0?1:-1,head:.1,air:jump,af1:jump?1.8:.2,ab1:jump?1.7:-.2}),1.7,{...YOU,dir:look>0?1:-1,expr:jump?'shocked':'thinking'}) };
// 24 the storm blows him back across the floor, scarf whipping (mid)
S.p_anx=(u,ts,d)=>{ camS(); bands(3,300,600); const op=out(ph(ts,0,.35)); doorway(700,op,330,480,{slab:'#9fb6c9'}); const X0=700+330*Math.cos(op*1.35);
  x.save(); x.beginPath(); x.rect(X0,G-480,700+330-X0,480); x.clip(); x.globalAlpha=op; x.fillStyle='#1d2a4a'; x.fillRect(700,G-480,330,480); pCloud(895,G-380,60,'#3a4256');
  if((ts%.8)<.1&&ts>.3){ x.strokeStyle='#ffe066'; x.lineWidth=10; x.beginPath(); x.moveTo(900,G-330); x.lineTo(860,G-230); x.lineTo(920,G-220); x.lineTo(870,G-90); x.stroke(); SHAKE=Math.max(SHAKE,8) } x.restore();
  x.save(); x.strokeStyle='#e8eef3'; x.lineWidth=5; for(let i=0;i<14;i++){ const yy=G-420+i*30, k=(ts*2.5+i*.17)%1; x.globalAlpha=.7; x.beginPath(); x.moveTo(1030+k*700,yy); x.lineTo(1130+k*700,yy); x.stroke() } x.restore();
  for(let i=0;i<4;i++){ const k=(ts*1.3+i*.25)%1; x.save(); x.translate(1030+k*900,G-300-Math.sin(k*9+i)*80); x.rotate(k*14); x.fillStyle='#fbf8ef'; x.fillRect(-20,-14,40,28); x.restore() }
  lbl('ANXIETY',865,180,64,INK,ph(ts,.15,.4)); const X=lerp(1180,1500,io(ph(ts,.3,d)));
  fig(X,P({dir:-1,lean:-.35-.06*Math.sin(ts*10),af1:2.2,af2:1.0,ab1:2.0,ab2:1.2,lf1:-.3,lb1:.35,head:-.15}),MS,{...YOU,dir:-1,wind:1.6,expr:'shocked'}) };
// 25 steps toward the grey door and slumps as the drizzle starts (mid)
S.p_dis=(u,ts,d)=>{ camS(); bands(8,300,600); const op=out(ph(ts,0,.35)); doorway(830,op,330,480,{slab:'#b7a98f'}); const X0=830+330*Math.cos(op*1.35);
  x.save(); x.beginPath(); x.rect(X0,G-480,830+330-X0,480); x.clip(); x.globalAlpha=op; x.fillStyle='#b8b8b8'; x.fillRect(830,G-480,330,480); pCloud(1010,G-390,55,'#8f8f8f'); x.strokeStyle='#6f7a86'; x.lineWidth=3;
  for(let i=0;i<14;i++){ const k=(ts*1.2+rnd(i))%1; const rx=900+rnd(i+9)*230; x.beginPath(); x.moveTo(rx,G-350+k*300); x.lineTo(rx,G-330+k*300); x.stroke() } x.fillStyle='#9aa3ad'; x.beginPath(); x.ellipse(1010,G-8,110,14,0,0,7); x.fill(); x.restore();
  lbl('DISAPPOINTMENT',995,180,64,INK,ph(ts,.15,.4)); const X=lerp(480,680,io(ph(ts,.2,1.2)));
  fig(X,ts<1.2?walk(ts,1.1,.7,{dir:1}):K(ts-1.2,[[0,{dir:1}],[.6,{dir:1,af1:.5,af2:1.1,ab1:.45,ab2:1.15,head:.2,hF:'palm',hB:'palm'},'back'],[1.2,{dir:1,lean:.12,head:.4,af1:-.05,ab1:.05}],[d,{dir:1,lean:.16,head:.45,af1:-.05,ab1:.05}]]),MS,{...YOU,expr:ts>1.2?'sad':'neutral'}) };
// 27 runs from his own rain cloud; it keeps up (mid)
S.p_cloud=(u,ts,d)=>{ camS(); bands(8,280,580); const X=lerp(500,1350,io(ph(ts,.2,d-.3))), running=ts>.2&&ts<d-.3;
  const J=fig(X,running?run(ts,2.3,{dir:1}):P({dir:1,head:.35,lean:.1}),MS,{...YOU,expr:'sad'});
  const cx=X-20+Math.sin(ts*2)*20, cy=260+Math.sin(ts*3)*10; pCloud(cx,cy,70,'#7d8590'); if((ts%1.2)<.08) { x.save(); x.strokeStyle='#ffe066'; x.lineWidth=7; x.beginPath(); x.moveTo(cx,cy+40); x.lineTo(cx-20,cy+90); x.lineTo(cx+10,cy+95); x.lineTo(cx-10,cy+140); x.stroke(); x.restore() }
  x.save(); x.strokeStyle='#5f7f9f'; x.lineWidth=3; for(let i=0;i<14;i++){ const k=(ts*1.6+rnd(i))%1, rx=cx-80+rnd(i+3)*160; x.beginPath(); x.moveTo(rx,cy+60+k*360); x.lineTo(rx-6,cy+84+k*360); x.stroke() } x.restore() };
// 28 lifts the barbell overhead easily, spins it, tosses it aside, dusts off his hands (mid)
S.p_strong=(u,ts,d)=>{ camS(); bands(1,300,600); const up=back(ph(ts,.3,.8)), toss=ph(ts,1.5,2.1);
  const p=K(ts,[[0,{dir:1,lean:.4,af1:1.0,af2:-.4,ab1:1.0,ab2:-.4,lf1:.5,lb1:-.5,lf2:-.4,lb2:-.4}],[.3,{dir:1,lean:.45,af1:1.0,af2:-.4,ab1:1.0,ab2:-.4,lf1:.55,lb1:-.55,lf2:-.5,lb2:-.5}],[.8,{dir:1,lean:0,af1:3.0,af2:.1,ab1:3.0,ab2:.1},'back'],[1.5,{dir:1,lean:-.05,af1:3.05,af2:.1,ab1:2.95,ab2:.1}],[1.75,{dir:1,lean:.15,af1:1.9,af2:.2,ab1:1.8,ab2:.2},'out'],[2.2,{dir:1,af1:.9,af2:1.5,ab1:.8,ab2:1.5}],[d,{dir:1,af1:.9,af2:1.5+.3*Math.sin(ts*16),ab1:.8,ab2:1.5-.3*Math.sin(ts*16)}]]);
  const J=fig(900,p,MS,{...YOU,expr:up>.9?'happy':'neutral'}); let bx=(J.hf[0]+J.hb[0])/2, by=lerp(G-40,(J.hf[1]+J.hb[1])/2,up), br=ts>.9&&ts<1.5?(ts-.9)*.6*Math.sin(ts*8):0;
  if(toss>0){ bx=lerp(bx,1500,out(toss)); by=lerp(by,G-40,toss)-Math.sin(toss*Math.PI)*200; br=toss*3 }
  x.save(); x.translate(bx,by); x.rotate(br); x.strokeStyle='#5e5a54'; x.lineWidth=14; x.beginPath(); x.moveTo(-200,0); x.lineTo(200,0); x.stroke(); x.fillStyle=INK; [-190,190].forEach(wx=>{ x.beginPath(); x.roundRect(wx-24,-70,48,140,10); x.fill() }); x.restore();
  if(ts>2.1&&ts<2.35) SHAKE=Math.max(SHAKE,16); dust(1500,ph(ts,2.1,2.6),6,1); pTick(1450,280,1.3,ph(ts,2.2,2.8)) };
// 29 runs, leaps the gap and lands in the light (wide, warm)
S.p_courage=(u,ts,d)=>{ camS(); paper('#f3dcae'); const land=ph(ts,2.25,3.0); x.save(); const g=x.createRadialGradient(1550,420,40,1550,420,900); g.addColorStop(0,`rgba(255,214,110,${.5+.45*land})`); g.addColorStop(1,'rgba(255,214,110,0)'); x.fillStyle=g; x.fillRect(0,0,1920,1080); x.restore(); pSun(1550,280,70+20*land,.6+.4*land);
  rr(-400,G,1150,600,'#8f6a43'); rr(1250,G,1200,600,'#9db58a'); x.save(); x.fillStyle='#5b3b23'; x.beginPath(); x.moveTo(750,G); x.lineTo(720,1080); x.lineTo(-400,1080); x.lineTo(-400,G); x.fill(); x.restore();
  titleTop('COURAGE',ph(ts,.75,1.05),96); const jx=t=>t<.6?300:t<1.4?lerp(300,720,io(ph(t,.6,1.4))):t<2.25?lerp(720,1420,ph(t,1.4,2.25)):1420;
  const jp=t=>t<.6?P({dir:1,lean:-.05,af1:.3,ab1:-.3,head:-.1}):t<1.4?run(t,2.6,{dir:1}):t<2.25?P({dir:1,lean:.3,af1:2.9,ab1:2.7,af2:.2,ab2:.2,lf1:.9,lf2:-1.2,lb1:-.6,lb2:-.4,air:Math.sin(ph(t,1.4,2.25)*Math.PI)*230+Math.max(0,(1-ph(t,1.4,1.6)))*0}):K(t-2.25,[[0,{dir:1,lean:.4,lf1:.8,lf2:-1.4,lb1:-.3,lb2:-1.3,af1:1.6,ab1:1.4}],[.3,{dir:1,af1:2.9,ab1:2.8,af2:.3,ab2:.3}],[1,{dir:1,af1:2.8,ab1:2.7,af2:.4,ab2:.4}]]);
  if(ts>1.4&&ts<2.25) ghost(jx,jp,ts,1.5,{...YOU,noFace:1},3,.05);
  fig(jx(ts),jp(ts),1.5,{...YOU,expr:ts>2.25?'happy':ts>.6?'calm':'worried'}); dust(1420,ph(ts,2.25,2.7),6,1); if(ts>2.25&&ts<2.45) SHAKE=Math.max(SHAKE,12) };

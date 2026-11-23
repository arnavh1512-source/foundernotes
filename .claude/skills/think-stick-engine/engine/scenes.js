// Pilot scenes. Cast: YOU (ink + red scarf), ADLER (grey, glasses, moustache), PHILOSOPHER (ink, white beard).
const YOU={scarf:1}, ADL={col:'#5d5a54',glasses:1,stache:1}, PHI={beard:1,col:'#5b3f8c'};
const B3=['CHILDHOOD','WORST YEAR','WHAT HURT'], BW=250, BH=88;
const breathe=t=>({head:.03*Math.sin(t*2.2),lean:.02*Math.sin(t*1.7)}); // moving hold
const hitstop=(ts,t0,n=.1)=>ts>t0&&ts<t0+n?t0:ts>=t0+n?ts-n:ts; // freeze the clock briefly at impacts
const SIT={lf1:1.5,lf2:-1.5,lb1:1.4,lb2:-1.45,lean:.06,af1:.9,af2:-.2,ab1:.8,ab2:-.1};
const HUG={lf1:2.0,lf2:-2.7,lb1:1.9,lb2:-2.6,lean:.42,head:.35,af1:1.5,af2:.5,ab1:1.4,ab2:.5};
const CROSS={lf1:1.45,lf2:-2.7,lb1:1.25,lb2:-2.75,lean:.02,af1:.7,af2:.6,ab1:.5,ab2:.6};
function train(hx,hy,X0,ts,n=3,gap=270){ let prev=[hx,hy]; for(let i=0;i<n;i++){ const bx=X0-i*gap, by=G-BH/2+Math.sin(ts*9+i)*1.5; chain(prev,[bx+BW/2*(i?1:1),by],18); block(bx,by,BW,BH,B3[i],Math.sin(ts*7+i)*.01); prev=[bx-BW/2,by] } }

// s01 ---------------------------------------------------------------
S.drag=(u,ts,d)=>{ const X=380+105*ts; cam(X-120,560,1); paper(); ground(); const p=walk(ts,.8,.65,{lean:.5,head:.22,af1:.04+.05*Math.sin(ts*5),af2:.05,ab1:-.06,ab2:.05}); const J=fig(X,p,1.6,YOU); train(J.hip[0]-6,J.hip[1],X-300,ts); for(let i=0;i<3;i++) dust(X-300-i*270-BW/2,(ts*1.3+i*.33)%1,3,.6) };
S.tug=(u,ts,d)=>{ const tt=hitstop(ts,1.05,.1); const X=900, k=ph(tt,.95,1.15); shakeAt(ts,1.05,10,.25); cam(780,560,1.25); paper(); ground();
  const p=K(tt,[[0,{lean:.45,head:.2,af1:.05,ab1:-.05}],[.55,{lean:.15,head:-.1,lf1:.35,lb1:-.3,af1:-.6,ab1:-.7,af2:.3}],[.75,{lean:.1,head:-.15,lf1:.4,lb1:-.35,af1:-.8,ab1:-.9}],[1.05,{lean:.85,head:.1,lf1:-.25,lb1:.75,lb2:-.4,af1:-1.4,ab1:-1.2,af2:.2},'back'],[1.6,{lean:.55,head:.5,af1:.0,ab1:-.05,lf1:.15,lb1:-.15}],[d,{lean:.62,head:.75,af1:-.02,ab1:-.05}]]);
  const J=fig(X,{...p,...(tt>1.6?breathe(ts):{})},1.6,YOU); train(J.hip[0]-6,J.hip[1],X-300+8*out(k)-8*ph(tt,1.2,1.5),ts); dust(X-300-BW/2,ph(tt,1.05,1.6),5) };

// s02 ---------------------------------------------------------------
S.yank=(u,ts,d)=>{ const tt=hitstop(ts,1.5,.12), snap=1.05; let X,p;
  if(tt<snap){ X=760+tt*560; p=run(tt,2.8,{}) } else if(tt<1.5){ const k=(tt-snap)/(1.5-snap); X=760+snap*560-260*out(k); p=P({lean:-.5,head:-.3,af1:2.3,af2:.3,ab1:2.0,ab2:.3,lf1:1.0,lf2:-.3,lb1:.7,lb2:-.4,air:Math.sin(k*Math.PI)*70,rot:-.5*k}) } else { X=1088; const k=ph(tt,1.5,1.9); p=K(tt,[[1.5,{rot:-1.45,lean:0,head:.1,af1:2.6,ab1:2.4,lf1:.4,lb1:.2}],[1.65,{rot:-1.38,head:.25,af1:2.2,ab1:2.0,lf1:.7,lb1:.4},'out'],[1.9,{rot:-1.45,head:.15,af1:2.5,ab1:2.3,lf1:.5,lb1:.3}],[d,{rot:-1.45,head:.2,af1:2.4,ab1:2.2,lf1:.55,lb1:.3}]]) }
  shakeAt(ts,1.5,12,.3); cam(1000,560,.95); paper(); ground(); doorway(1500,.15);
  if(tt<snap) speed(X,G-260,180,cl(tt*3),1);
  const J=fig(X,p,1.6,{...YOU,wind:tt<snap?1:0}); const taut=tt>snap-.15&&tt<1.5; chain([J.hip[0],J.hip[1]],[420,G-BH/2],taut?0:30); block(330,G-BH/2,BW*.72,BH,'PAST',0); dust(X-40,ph(tt,1.5,2.0),7); burst(J.hip[0]-30,J.hip[1],ph(tt,snap,snap+.25),70) };
S.sit=(u,ts,d)=>{ const z=lerp(1.12,1.3,io(u)); cam(950,600,z); paper(); ground(); for(let i=0;i<3;i++) block(640,G-BH/2-i*(BH+6),BW*1.2,BH*1.1,B3[i],(i-1)*.03);
  const J=fig(1030,{...P(HUG),dir:-1,head:.35+.04*Math.sin(ts*1.4),lean:.42+.02*Math.sin(ts*1.1)},1.6,YOU); chain([J.hip[0],J.hip[1]],[640+BW*.6,G-BH/2],10) };
S.adler=(u,ts,d)=>{ const tt=hitstop(ts,.95,.08); const arrive=1.7; const X=tt<arrive?-80+tt*(720/arrive):640; let p;
  if(tt<arrive) p=walk(tt,1.5,1); else p=K(tt,[[arrive,{lean:.12}],[arrive+.2,{lean:-.08},'out'],[arrive+.45,{lean:.03}],[2.2,{head:.25}],[2.35,{head:-.25}],[2.5,{head:.2}],[2.65,{head:-.15}],[2.8,{head:0}],[3.05,{af1:3.0,af2:.15,lean:-.05},'back'],[d,{af1:2.95,af2:.2,lean:-.04}]]);
  shakeAt(ts,.95,10,.25); cam(860,560,1); paper(); ground();
  for(let i=0;i<3;i++) block(1080,G-BH/2-i*(BH+6),BW,BH,B3[i],(i-1)*.03); fig(1330,{...P(HUG),dir:-1,head:.45},1.5,YOU);
  fig(X,{...p,...(tt>arrive+.5?breathe(ts):{})},1.6,ADL);
  const dy=tt<.95?lerp(-260,G-BH/2,inn(cl(tt/.95))):G-BH/2-Math.max(0,Math.sin((tt-.95)*14)*16*Math.exp(-(tt-.95)*6)); if(tt>.2) block(400,dy,230,BH,'ADLER',tt<.95?.08:0); dust(400,ph(tt,.95,1.5),6) };

// s03 ---------------------------------------------------------------
S.snap=(u,ts,d)=>{ const tt=hitstop(ts,1.1,.1); shakeAt(ts,1.1,8,.2); cam(1050,560,1.08); paper(); ground(); const ap=K(tt,[[0,{lean:.02}],[.7,{af1:2.2,af2:1.2,lean:-.04}],[1.0,{af1:2.6,af2:1.6,lean:-.08},'out'],[1.1,{af1:2.9,af2:.5,lean:.05},'back'],[d,{af1:2.85,af2:.6,lean:.03}]]);
  fig(760,{...ap,...breathe(ts)},1.6,ADL); const look=tt>1.5; const J=fig(1180,K(tt,[[0,{...HUG,dir:-1}],[1.3,{...HUG,dir:-1,head:.1,lean:.25}],[1.8,{...HUG,dir:-1,head:-.2,lean:.15},'back'],[d,{...HUG,dir:-1,head:-.15,lean:.16}]]),1.6,YOU);
  for(let i=0;i<3;i++) block(1560,G-BH/2-i*(BH+6),BW,BH,B3[i],(i-1)*.03); const k=ph(tt,1.1,2.2); chain([J.hip[0],J.hip[1]],[1560-BW/2,G-BH/2],12,tt>1.1?.5:-1,out(k)); burst(760+Math.sin(2.9)*92*1.6,G-430,ph(tt,1.1,1.35),60) };
S.knock=(u,ts,d)=>{ const t1=.7,t2=1.95,t3=3.3, tt=hitstop(hitstop(ts,t1,.08),t2,.08); shakeAt(ts,t1,8,.2); shakeAt(ts,t2,10,.22); shakeAt(ts,t3,12,.3);
  const X=tt<.9?900:tt<1.6?lerp(900,1170,io(ph(tt,.9,1.6))):tt<2.3?1170:tt<3.0?lerp(1170,1420,io(ph(tt,2.3,3.0))):1420;
  const walking=(tt>.9&&tt<1.6)||(tt>2.3&&tt<3.0);
  const pose=t=>walking?walk(t,1.6,.9,{lean:.12}):K(t,[[0,{lean:.05}],[.45,{lf1:-.7,lf2:-.6,lean:-.12,af1:.6,ab1:-.7},'out'],[.7,{lf1:1.7,lf2:0,lean:-.3,af1:-.6,ab1:1.0},'back'],[.9,{lean:.05}],[1.6,{lean:.08}],[1.8,{af1:.1,af2:2.0,ab1:.5,ab2:1.2,lean:-.15},'out'],[1.95,{af1:1.6,af2:0,lean:.3,lf1:.4,lb1:-.4},'back'],[2.3,{lean:.06}],[3.0,{lean:.06}],[3.15,{af1:.9,af2:1.4,ab1:.9,ab2:1.4,lean:-.05,lf1:.3,lb1:-.4},'out'],[3.3,{af1:1.55,af2:.05,ab1:1.5,ab2:.05,lean:.4,lf1:-.2,lb1:.7},'back'],[d,{af1:.3,ab1:.2,lean:.08,lf1:.1,lb1:-.1}]]);
  cam(X+220,560,1.05); paper(); ground();
  const k1=tt-t1, k2=tt-t2, k3=ph(tt,t3,t3+.7);
  if(k1<0) block(1080,G-BH/2,BW,BH,B3[0]); else block(1080+k1*1500,G-BH/2-(900*k1-1100*k1*k1),BW,BH,B3[0],k1*9);
  if(k2<0) block(1340,G-BH/2,BW,BH,B3[1]); else block(1340+k2*1700,G-BH/2-(500*k2-600*k2*k2),BW,BH,B3[1],k2*7);
  x.save(); x.translate(1640+k3*260,G); x.rotate(out(k3)*1.57); block(BW*.6/2*0,-BH*.8,BW*1.2,BH*1.6,B3[2],0,{crack:k3>.4}); x.restore();
  const fast=Math.abs(tt-t1)<.06||Math.abs(tt-t2)<.06; if(fast) ghost(()=>X,pose,tt,1.6,YOU,3,.03); fig(X,pose(tt),1.6,YOU); burst(1000,G-130,ph(tt,t1,t1+.25),60); burst(1290,G-300,ph(tt,t2,t2+.25),70); dust(1650+k3*260,ph(tt,t3+.6,t3+1.2),7) };
S.uneasy=(u,ts,d)=>{ cam(1000,560,1.15); paper(); ground(); const step=Math.floor(ts/.7), j=out(ph(ts%.7,0,.18)); const off=(step+j)*55;
  block(1560-off,G-BH/2,BW,BH,B3[0],.04); block(420+off*.9,G-BH/2,BW,BH,B3[1],-.03); block(1700-off*.8,G-BH*1.5-6,BW,BH,B3[2],.02);
  const bx=1000+Math.sin(ts*2.4)*60; const p=walk(ts,1.2,.5,{lean:-.12,head:.25*Math.sin(ts*5),af1:2.6,af2:1.9,ab1:2.5,ab2:1.9}); fig(bx,p,1.6,{...YOU,dir:Math.cos(ts*2.4)>0?1:-1}) };
S.path=(u,ts,d)=>{ const ex=700+out(ph(ts,.15,2.2))*1700; const X=ts<2.4?700:700+(ts-2.4)*300; cam(Math.max(900,X+250),560,1); paper(); ground(.6);
  x.save(); x.strokeStyle=RED; x.lineWidth=12; x.lineCap='round'; x.beginPath(); x.moveTo(690,G); for(let px=690;px<=ex;px+=20) x.lineTo(px,G-4+Math.sin(px*.012)*5); x.stroke(); x.restore();
  if(ts<2.5){ x.save(); x.translate(ex,G-6); x.rotate(-.75); x.fillStyle='#f2c14e'; x.strokeStyle=INK; x.lineWidth=6; x.beginPath(); x.roundRect(-18,-260,36,220,6); x.fill(); x.stroke(); x.fillStyle='#f6dcb5'; x.beginPath(); x.moveTo(-18,-40); x.lineTo(18,-40); x.lineTo(0,0); x.closePath(); x.fill(); x.stroke(); x.restore() }
  const p=ts<2.4?K(ts,[[0,{lean:.1,head:.1}],[.5,{lean:.25,head:.55},'out'],[1.8,{lean:.22,head:.5}],[2.2,{lean:.02,head:-.15},'back'],[2.4,{lean:.05}]]):walk(ts,1.5,1,{lean:.04,head:-.05}); fig(X,p,1.6,{...YOU,wind:ts>2.4?.6:0}) };

// s04 ---------------------------------------------------------------
S.book=(u,ts,d)=>{ const land=.6, tt=hitstop(ts,land,.08); shakeAt(ts,land,12,.3); cam(960,540,1); paper(); ground();
  const by=tt<land?lerp(-500,G,inn(tt/land)):G-Math.max(0,Math.sin((tt-land)*12)*14*Math.exp(-(tt-land)*5)); const op=out(ph(tt,1.2,2.2)), bw=300, bh=420;
  x.save(); x.translate(960,by); x.fillStyle='#f6f2e9'; x.strokeStyle=INK; x.lineWidth=8; x.beginPath(); x.rect(-bw,-bh,bw*2*op+0.1,bh); if(op>0){ x.fill(); x.stroke(); for(let i=0;i<6;i++){ x.beginPath(); x.moveTo(-bw+40,-bh+70+i*55); x.lineTo(-40,-bh+70+i*55); x.moveTo(40,-bh+70+i*55); x.lineTo(bw*2*op-bw-40,-bh+70+i*55); x.stroke() } }
  x.fillStyle=INK; const cw=bw*Math.cos(op*Math.PI); x.beginPath(); x.rect(cw<0?cw:0,-bh,Math.abs(cw)||1,bh); x.fill(); x.fillRect(-10,-bh,20,bh); x.restore(); dust(960,ph(tt,land,land+.6),8,1.4) };
S.nights=(u,ts,d)=>{ paper('#283041'); cam(960,540,1); const per=d/5, n=Math.min(4,Math.floor(ts/per)), k=(ts%per)/per; x.save(); x.fillStyle='#f1eee6'; for(let i=0;i<40;i++){ x.globalAlpha=.3+.5*rnd(i); x.fillRect(rnd(i+1)*W,rnd(i+2)*600,3,3) } x.restore();
  const a=Math.PI*(1-k); x.fillStyle='#f6e7b0'; x.beginPath(); x.arc(960+Math.cos(a)*700,720-Math.sin(a)*520,46,0,Math.PI*2); x.fill();
  x.strokeStyle='#f1eee6'; x.lineWidth=6; x.beginPath(); x.moveTo(-100,G); x.lineTo(2100,G); x.stroke(); x.strokeRect(820,G-200,280,200); x.beginPath(); x.moveTo(800,G-200); x.lineTo(960,G-320); x.lineTo(1120,G-200); x.stroke(); x.fillStyle=WARM; x.fillRect(900,G-150,120,80);
  x.lineWidth=10; x.lineCap='round'; for(let i=0;i<=n;i++){ if(i<4){ x.beginPath(); x.moveTo(1460+i*46,180); x.lineTo(1460+i*46,330); x.stroke() } else { x.beginPath(); x.moveTo(1440,300); x.lineTo(1640,200); x.stroke() } } };
S.calm=(u,ts,d)=>{ const bang=d-.45, tt=hitstop(ts,bang,.1); shakeAt(ts,bang,14,.35); cam(1000,560,1); paper(); ground(); x.strokeStyle=LINE; x.lineWidth=6; x.strokeRect(260,300,220,200);
  const op=tt<bang?0:out(ph(tt,bang,bang+.12)); doorway(1420,op,230,430,{off:tt>bang+.15}); if(tt>bang+.12){ const k=tt-bang-.12; block(1530-k*900,G-250+k*600*k,40,330,'',1+k*8,{fill:'#efe7d6'}) }
  const sip=ph(tt,.4,1.0)-ph(tt,1.5,1.9); const J=fig(760,{...P(CROSS),af1:lerp(.7,1.25,io(sip)),af2:lerp(.6,1.55,io(sip)),head:.03*Math.sin(ts*2)+(tt>bang+.2?.15:0)},1.6,PHI); cup(J.hf[0]+8,J.hf[1]+6,1.3); burst(1530,G-230,ph(tt,bang,bang+.3),120) };

// dialogue c1/c2 ------------------------------------------------------
S.storm=(u,ts,d)=>{ const stopT=1.25; const X=ts<stopT?1540-ts*(440/stopT):1100; const stomp=[.45,.85,1.25]; stomp.forEach(s=>shakeAt(ts,s,6,.12));
  const p=ts<stopT?walk(ts,2.3,1.1,{lean:.22,dir:-1}):K(ts,[[stopT,{lean:.25,dir:-1}],[stopT+.2,{lean:.32,af1:1.65,af2:0,ab1:-.3,dir:-1},'back'],[d,{lean:.3,af1:1.6,af2:0,ab1:-.25,dir:-1}]]);
  const jab=ts>stopT+.2?Math.max(0,Math.sin(ts*14))*.12:0; cam(1000,560,1.02); paper(); ground(); doorway(1450,1,230,430,{off:1});
  fig(600,{...P(CROSS),...breathe(ts)},1.6,PHI); cup(690,G-100,1.2); fig(X,{...p,af1:(p.af1||0)+jab,lean:p.lean+jab*.3},1.6,{...YOU,dir:-1}); stomp.forEach(s=>dust(X+20,ph(ts,s,s+.4),3,.6)) };
S.sip=(u,ts,d)=>{ cam(780,600,1.85); paper(); ground(); const sip=ph(ts,.3,1.1)-ph(ts,1.6,2.0); const fing=ph(ts,2.1,2.35);
  const J=fig(760,{...P(CROSS),af1:lerp(.7,1.25,io(sip)),af2:lerp(.6,1.55,io(sip)),ab1:lerp(.5,2.6,back(fing)),ab2:lerp(.6,.2,fing),head:.05*Math.sin(ts*1.6)+(sip>.9?-.08:0)},1.6,PHI); cup(J.hf[0]+8,J.hf[1]+6,1.3) };

// s05 ---------------------------------------------------------------
S.preach=(u,ts,d)=>{ cam(1000,560,.95); paper(); ground(); x.fillStyle='#c9a46a'; x.strokeStyle=INK; x.lineWidth=7; x.fillRect(600,G-110,220,110); x.strokeRect(600,G-110,220,110);
  const g=Math.floor(ts/1.05)%3; const arms=[{af1:2.2,ab1:2.2,af2:.2,ab2:.2},{af1:1.4,ab1:-.4,af2:.1},{af1:2.8,ab1:.2,af2:.3}][g];
  const p=mix(P({lean:.05}),P(arms),back(cl((ts%1.05)/.3))); fig(710,{...p,dir:-1},1.5,{...PHI,y:G-110-112*1.5,noShadow:1});
  [260,380,480].forEach((cx,i)=>fig(cx,{...STAND,head:.06*Math.sin(ts*3+i),lean:.06},1.25,{col:'#a9a397'}));
  const tap=Math.max(0,Math.sin(ts*12)); fig(1420,{...P({af1:1.6,af2:1.9,ab1:1.5,ab2:1.9,lean:-.08,head:-.2}),lf1:.1+tap*.25,dir:-1},1.6,{...YOU,dir:-1}) };
S.three=(u,ts,d)=>{ const L1=.45,L2=1.85,L3=3.25; [L1,L2,L3].forEach((l,i)=>shakeAt(ts,l,8+i*3,.25)); const tt=hitstop(hitstop(ts,L1,.07),L3,.1);
  const drop=(L,X,txt,i)=>{ const y=tt<L?lerp(-300,G-85,inn(cl((tt-(L-.45))/.45))):G-85; if(tt>L-.45) block(X,y,340,170,txt,tt<L?.06*(i-1):0) };
  let X,p; const kick=1.05, push=2.35, leap=2.95;
  if(tt<leap){ X=tt<push-.1?1000:1000-lerp(0,40,ph(tt,push,push+.5)); p=K(tt,[[0,{dir:-1}],[L1,{dir:-1,lean:-.15,head:-.2},'out'],[.85,{dir:-1,lf1:-.6,lean:-.1}],[kick,{dir:-1,lf1:1.5,lf2:0,lean:-.25,af1:-.5,ab1:.9},'back'],[1.2,{dir:-1,lf1:1.9,lf2:-1.7,lean:.3,af1:1.9,af2:.4,ab1:1.0,air:20}],[1.55,{dir:-1,lf1:1.7,lf2:-1.8,lean:.25,af1:1.8,ab1:1.2,air:28}],[1.9,{dir:-1,lean:.05}],[2.1,{dir:1,lean:.05},'back'],[push,{dir:1,af1:1.5,af2:.1,ab1:1.5,ab2:.1,lean:.45,lf1:-.3,lb1:.8}],[leap-.1,{dir:1,af1:1.55,ab1:1.5,lean:.55,lf1:-.4,lb1:.9}],[leap,{dir:1,lean:-.1,lf1:.5,lb1:-.3,af1:2.6,ab1:2.4}]]); if(tt>1.15&&tt<1.6) p.air=20+Math.abs(Math.sin(tt*16))*24 }
  else { const k=ph(tt,leap,leap+.55); X=lerp(1000,1490,out(k)); p=K(tt,[[leap,{dir:1,lean:.4,af1:2.8,ab1:2.6,lf1:.9,lf2:-1.2,lb1:-.6}],[leap+.55,{dir:1,lean:.5,af1:2.5,ab1:2.0,lf1:1.2,lf2:-1.6,lb1:.9,lb2:-1.4},'out'],[leap+.75,{dir:-1,lean:.1,af1:.4,ab1:.3},'back'],[d,{dir:-1,lean:-.05,head:.15,af1:1.4,af2:1.9,ab1:.3}]]); p.air=Math.sin(k*Math.PI)*120 }
  cam(1080,560,1); paper(); ground(); drop(L1,620,'THE WORLD|IS SIMPLE',0); drop(L2,1400,'PEOPLE|CAN CHANGE',1); drop(L3,1000,'ANYONE CAN|BE HAPPY',2);
  fig(X,p,1.5,{...YOU,dir:p.dir,wind:tt>leap&&tt<leap+.55?1:0}); [L1,L2,L3].forEach((l,i)=>dust([620,1400,1000][i],ph(tt,l,l+.5),6)); burst(700,G-110,ph(tt,kick,kick+.22),55) };
S.prove=(u,ts,d)=>{ cam(900,560,1.1); paper(); ground(); const go=1.85; const X=ts<go?900:900+Math.pow(ts-go,1.4)*720;
  const p=ts<go?K(ts,[[0,{af1:1.3,af2:1.6,ab1:1.3,ab2:1.6,lean:-.05}],[.25,{af1:1.4,af2:1.9,ab1:1.2,ab2:1.4}],[.5,{af1:1.25,af2:1.5,ab1:1.4,ab2:1.9}],[.75,{af1:1.4,af2:1.9,ab1:1.2,ab2:1.4}],[1.0,{af1:.3,ab1:.2,head:.3}],[1.25,{head:-.3}],[1.5,{head:.1,lean:.1}],[go,{lean:.25,lf1:-.3,lb1:.4},'out']]):walk(ts,2.0,1.15,{lean:.22});
  fig(X,p,1.6,{...YOU,wind:ts>go?1:0}); speed(X,G-260,200,ph(ts,go+.3,go+.8),1) };

// dialogue c3/c4 ------------------------------------------------------
S.rant=(u,ts,d)=>{ cam(940,520,1.45); paper(); ground(); const w=Math.sin(ts*7), c=ts%2.6, j=ph(c,1.75,1.95)-ph(c,2.1,2.35); shakeAt(c,2.35,14,.22);
  fig(940,P({af1:1.9+w*.9,af2:.4+w*.3,ab1:2.0-w*.9,ab2:.4-w*.3,lean:.12*w,head:.15*Math.sin(ts*5),air:j*90,lf1:.1+j*.6,lf2:-.05-j*.9,lb1:-.1+j*.4,lb2:-.05-j*.9}),1.6,{...YOU,wind:.3}); dust(940,ph(c,2.35,2.8),5) };
S.chair=(u,ts,d)=>{ const kick=.7, hit=1.3, tt=hitstop(ts,hit,.08); shakeAt(ts,hit,10,.25); cam(980,560,1); paper(); ground();
  fig(560,K(tt,[[0,{...CROSS}],[kick-.2,{...CROSS,lf1:1.2,lf2:-1.2}],[kick,{...CROSS,lf1:1.4,lf2:-.1,lean:-.12},'back'],[kick+.4,{...CROSS}]]),1.6,PHI);
  const cx=tt<kick?720:tt<hit?lerp(720,1185,out(ph(tt,kick,hit))):1185; chair(cx,1.6,-1); if(tt>kick&&tt<hit) speed(cx,G-60,160,1,1);
  const p=tt<hit?K(tt,[[0,{dir:-1,af1:1.8,af2:.6,ab1:1.7,ab2:.6,lean:.1}],[hit,{dir:-1,af1:1.7,ab1:1.6,lean:.08}]]):K(tt,[[hit,{dir:-1,lf1:.8,lf2:-.6,lb1:.6,lb2:-.5,lean:-.35,af1:2.6,ab1:2.4,air:30}],[hit+.25,{...SIT,dir:-1,lean:-.15,af1:2.0,ab1:1.8},'back'],[d,{...SIT,dir:-1,lean:.05,af1:1.0,ab1:.8,head:.2}]]);
  fig(1185,p,1.6,{...YOU,dir:-1}); burst(1150,G-90,ph(tt,hit,hit+.22),50) };

// s06 ---------------------------------------------------------------
const pick=(p,ks)=>{ const r={}; ks.forEach(k=>{ if(p[k]!=null) r[k]=p[k] }); return r };
function tableScene(ts,z,o={}){ cam(960,560,z); paper(); ground(); x.strokeStyle=LINE; x.lineWidth=6; x.strokeRect(820,240,280,220); table(780,360,150); cup(860,G-150,1.2); cup(1080,G-150,1.2,0); chair(600,1.6,1); chair(1320,1.6,-1);
  const a=fig(600,{...P(SIT),af1:1.2,af2:-.5,...breathe(ts),...(o.ph||{})},1.6,PHI); const b=fig(1320,{...P(SIT),dir:-1,af1:1.6,af2:1.9,ab1:1.5,ab2:1.9,head:.06*Math.sin(ts*2.5),...(o.ym||{})},1.6,{...YOU,dir:-1}); return [a,b] }
S.table=(u,ts,d)=>{ tableScene(ts,lerp(1,1.1,io(u))) };
S.bars=(u,ts,d)=>{ const hit=1.4, tt=hitstop(ts,hit,.1); shakeAt(ts,hit,9,.25); const jab=K(tt,[[0,{}],[hit-.25,{dir:-1,af1:.3,af2:1.9,lean:-.1},'out'],[hit,{dir:-1,af1:1.6,af2:0,lean:.3},'back'],[hit+.5,{dir:-1,af1:1.0,af2:.6,lean:.1}]]);
  const [a,b]=tableScene(ts,1.02,{ym:tt>hit-.3?pick(jab,['af1','af2','lean']):{}}); const k=back(ph(ts,.1,.4)), drop=ph(tt,hit,hit+.3);
  const bar=(cx,cy,v,lab,flash)=>{ if(k<=0)return; x.save(); x.translate(cx,cy); x.scale(k,k); x.fillStyle=INK; x.fillRect(-130,-22,260,44); x.fillStyle=flash?'#fff':v<.5?'#e8a33d':'#5aa469'; x.fillRect(-122,-14,244*v,28); x.fillStyle=INK; x.font='700 30px Inst'; x.textAlign='center'; x.fillText(lab,0,-36); x.restore() };
  bar(a.hd[0],a.hd[1]-130,1-.32*drop,'ADLER',tt>hit&&tt<hit+.1); bar(b.hd[0],b.hd[1]-130,1,'HIM',0) };
S.question=(u,ts,d)=>{ const land=.85, tt=hitstop(ts,land,.1); shakeAt(ts,land,14,.35); const rec=K(tt,[[0,{}],[land,{}],[land+.15,{lean:-.4,head:-.35,af1:2.4,ab1:2.2},'out'],[land+.9,{lean:.15,head:-.45}],[d,{lean:.18,head:-.5}]]);
  const [a,b]=tableScene(ts,1,{ph:pick(rec,['lean','head','af1','ab1']),ym:pick(rec,['lean','head','af1','ab1'])}); const y=tt<land?lerp(-400,G-200,inn(tt/land)):G-200-Math.max(0,Math.sin((tt-land)*13)*18*Math.exp(-(tt-land)*5)); block(960,y,300,300,'?',tt<land?.1:0); dust(960,ph(tt,land,land+.6),9,1.5) };
S.back=(u,ts,d)=>{ const pan=K(ts,[[0,{lean:0}],[.4,{lean:0}],[1.3,{lean:1}],[1.9,{lean:1}],[2.7,{lean:0}]]).lean; cam(lerp(1150,520,pan),560,1); paper(); ground();
  for(let i=0;i<3;i++) block(160+i*30,G-BH/2-i*(BH+6),BW,BH,B3[i],(i-1)*.08); chain([300,G-BH/2],[560,G-30],6,.5,1); block(1500,G-150,300,300,'?',0);
  const turn=ts>.35&&ts<2.2; const X=ts<2.4?1150:1150+(ts-2.4)*260; const p=ts<2.4?P({dir:turn?-1:1,head:turn?.1:0,lean:turn?-.05:.04,...breathe(ts)}):walk(ts,1.5,1,{lean:.06}); fig(X,p,1.6,{...YOU,dir:p.dir}) };

// scenes5.js: character-led action beats for long explanations (v2). Characters act the idea out; new pictures replace zoom pulses.
const A=(a,k)=>(a&&a[k]!==undefined)?a[k]:undefined;
function wash(col,k){ if(k<=0) return; x.save(); x.setTransform(1,0,0,1,0,0); x.globalAlpha=k; x.fillStyle=col; x.fillRect(0,0,W,H); x.restore() }
function shelf(X=200){ if(window.BG==='study') return; x.save(); x.strokeStyle=LINE; x.lineWidth=6; for(let i=0;i<4;i++) x.strokeRect(X,180+i*90,320,90); for(let i=0;i<4;i++) for(let j=0;j<6;j++){ x.fillStyle=['#c9a46a','#8a5530','#5e5a54','#3d7fa8'][(i+j)%4]; x.fillRect(X+15+j*50,195+i*90,30,75) } x.restore() }
function bigBlock(cx,cy,txt,col=INK,s=1,rot=0){ block(cx,cy,440*s,132*s,txt,rot,{fill:col}) }
// ---------- dialogue staging in the study: wide two-shot or medium on the speaker, with whole-body actions
// a.mode: wide|ph|yo ; a.act (youth): point|pace|slam|shrug|headgrab|stepback|cross ; a.pact (philosopher): stand|lean|raise|open|calm
S.duo=(u,ts,d,a={})=>{ const m=a.mode||'wide';
  if(m==='ph') cam(780,600,1.6); else if(m==='yo') cam(1200,570,1.5); else cam(990,560,1);
  paper(); ground(); shelf(160); table(880,220,150); cup(930,G-150,1.1); cup(1050,G-150,1.1,0);
  // philosopher (seated, may stand)
  const pa=a.pact||'calm'; let pp, standing=false;
  if(pa==='stand'){ const k=io(ph(ts,.2,1.0)); standing=k>.5; pp=k<.5?P({...SIT,dir:1}):K(ts,[[0,{dir:1,af1:.4,ab1:.3}],[1.0,{dir:1,af1:.5,ab1:.3}],[1.6,{dir:1,af1:1.6,af2:.4,ab1:.2,lean:.12},'back'],[d,{dir:1,af1:1.4,af2:.6,ab1:.3,lean:.08}]]) }
  else if(pa==='lean') pp=P({...SIT,dir:1,lean:lerp(.06,.32,io(ph(ts,.3,1))),af1:lerp(.9,1.5,io(ph(ts,.3,1))),af2:.3});
  else if(pa==='raise') pp=P({...SIT,dir:1,af1:lerp(.9,2.7,back(ph(ts,.3,.8))),af2:lerp(-.2,.3,ph(ts,.3,.8)),head:.08});
  else if(pa==='open') pp=P({...SIT,dir:1,af1:lerp(.9,1.3,io(ph(ts,.2,.7))),af2:-.6,ab1:lerp(.8,1.2,io(ph(ts,.2,.7))),ab2:-.6,head:-.05});
  else pp=P({...SIT,dir:1});
  const PT=pa!=='raise'; if(standing) fig(760,pp,1.6,{...PHI,dir:1,talk:PT}); else { sitAt(760,1.6,pp,{...PHI,dir:1,talk:PT}); } chair(760,1.6,1);
  // young man (standing), whole-body actions
  const ya=a.act||'stand'; let X=1240, yp;
  if(ya==='point'){ X=lerp(1300,1180,io(ph(ts,.1,.6))); yp=K(ts,[[0,{dir:-1}],[.6,{dir:-1,af1:1.65,af2:.05,lean:.18},'back'],[d,{dir:-1,af1:1.6,af2:.1,lean:.14}]]) }
  else if(ya==='pace'){ const w=ts*1.8; X=1250+170*Math.sin(w); const dirp=Math.cos(w)>0?1:-1; yp=walk(ts,1.4,1,{dir:dirp,af1:2.5,af2:2.2}) }
  else if(ya==='slam'){ const hit=Math.min(d*.45,1.0); X=lerp(1240,1150,io(ph(ts,0,hit))); yp=K(ts,[[0,{dir:-1}],[hit*.8,{dir:-1,af1:2.8,af2:.3,ab1:2.7,ab2:.3,lean:-.1},'out'],[hit,{dir:-1,af1:1.2,af2:.2,ab1:1.1,ab2:.2,lean:.55},'inn'],[d,{dir:-1,af1:1.1,af2:.3,ab1:1.0,ab2:.3,lean:.45}]]); if(ts>hit) SHAKE=Math.max(0,1-(ts-hit)/.35)*26; if(ts>hit&&ts<hit+.15) { cup(930,G-150-30,1.1) } }
  else if(ya==='shrug'){ yp=K(ts,[[0,{dir:-1}],[.5,{dir:-1,af1:1.0,af2:-1.3,ab1:1.0,ab2:-1.3,head:.18},'back'],[d,{dir:-1,af1:.9,af2:-1.2,ab1:.9,ab2:-1.2,head:.12}]]) }
  else if(ya==='headgrab'){ yp=P({dir:-1,af1:2.6,af2:2.4,ab1:2.5,ab2:2.4,lean:.05+.08*Math.sin(ts*5),head:.1*Math.sin(ts*4)}); X=1240+30*Math.sin(ts*3) }
  else if(ya==='stepback'){ X=lerp(1200,1380,out(ph(ts,.1,.6))); yp=K(ts,[[0,{dir:-1}],[.5,{dir:-1,lean:-.25,af1:2.0,af2:1.0,ab1:2.0,ab2:1.0,air:20},'out'],[d,{dir:-1,lean:-.1,af1:1.2,af2:.6,ab1:1.1,ab2:.6}]]) }
  else if(ya==='cross') yp=P({dir:-1,af1:1.05,af2:1.95,ab1:1.0,ab2:1.95,head:-.1+.05*Math.sin(ts*2),lean:-.04});
  else yp=P({dir:-1});
  if(m!=='ph') fig(X,yp,1.6,{...YOU,dir:-1,talk:['stand','cross','pace'].includes(ya)}) };
// ---------- keyword actions: the character handles the key words of the line
// a.w: words ; a.act: slam|kick|push|point|stack ; a.who: yo|ph|mom ; a.col: block colours
S.keys=(u,ts,d,a={})=>{ cam(990,540,1); paper(); ground(); const w=a.w||['IDEA'], n=w.length, act=a.act||'point', who=a.who||'yo';
  const O=who==='ph'?{...PHI,dir:1}:who==='mom'?{...MOM,dir:1}:{...YOU,dir:1}; const cols=a.col||[INK,RED,'#2f6f4f'];
  const row=act==='point'?470:G-66, slot=i=>act==='stack'?[1250,G-66-i*138]:[n===1?1250:1230+(i-(n-1)/2)*(n===3?460:480), row];
  if(act==='slam'){ let flinch=0; for(let i=0;i<n;i++){ const t0=d*(i+.4)/(n+.6), k=ph(ts,t0,t0+.35), [bx,by]=slot(i); if(k>0){ bigBlock(bx,lerp(-120,by,inn(k)),w[i],cols[i%3]); if(k>=1&&ts<t0+.6) dust(bx,ph(ts,t0+.35,t0+.8)); if(ts>t0+.35&&ts<t0+.65) SHAKE=Math.max(SHAKE,22*(1-(ts-t0-.35)/.3)); } if(ts>t0+.35&&ts<t0+.6) flinch=1 } const X=n===3?400:620; fig(X,flinch?P({dir:1,lean:-.3,af1:2.4,af2:1.2,ab1:2.3,ab2:1.2,air:30}):P({dir:1,af1:.9+.3*Math.sin(ts*3),af2:.6,head:.1}),1.6,O); return }
  if(act==='kick'){ const [bx,by]=slot(0), tk=Math.min(d*.5,1.6); const X=lerp(560,bx-240,io(ph(ts,.2,tk))); const kk=ph(ts,tk,tk+1.1);
    fig(X,ts<tk?run(ts,2.4,{dir:1}):K(ts-tk,[[0,{dir:1,lf1:-.6,lf2:-.1,lb1:.2,af1:-.8,ab1:1.2}],[.15,{dir:1,lf1:1.6,lf2:-.1,lb1:-.3,af1:1.4,ab1:-.6,lean:-.2},'out'],[.6,{dir:1,af1:.4,ab1:.2}]]),1.6,O);
    bigBlock(bx+kk*380,by-Math.sin(kk*Math.PI)*380,w[0],cols[0],1,kk*Math.PI*2); if(kk>=1&&ts<tk+1.5) dust(bx+380,ph(ts,tk+1.1,tk+1.5)); if(kk>0&&kk<.2){ burst(bx-150,by,kk*5,90); SHAKE=20*(1-kk*5) } for(let i=1;i<n;i++){ const [cx,cy]=slot(i); bigBlock(cx,cy,w[i],cols[i%3]) } return }
  if(act==='push'){ const X=lerp(380,900,io(ph(ts,.3,d*.8))); fig(X,walk(ts,1.1,.8,{dir:1,lean:.45,af1:1.5,af2:.2,ab1:1.4,ab2:.2}),1.6,O); for(let i=0;i<n;i++) bigBlock(X+290,G-66-i*138,w[i],cols[i%3]); return }
  if(act==='stack'){ let X=600; for(let i=0;i<n;i++){ const t0=d*(i+.3)/(n+.4), k=back(ph(ts,t0,t0+.45)); if(k>0){ bigBlock(lerp(2300,1250,k),lerp(-200,G-66-i*138,k),w[i],cols[i%3],1,(1-k)*.5); if(ts>t0+.4&&ts<t0+.65) SHAKE=Math.max(SHAKE,14) } }
    const beat=Math.floor(ts/(d/(n+.4))); fig(X,K(ts%(d/(n+.4)),[[0,{dir:1,af1:.4}],[.2,{dir:1,af1:2.7,af2:.2,air:40,lf1:.5,lb1:-.4},'out'],[.45,{dir:1,af1:1.6,af2:.1}]]),1.6,O); return }
  // point (default): blocks pop in as the character points to each
  let X=n===3?380:600, idx=-1; for(let i=0;i<n;i++){ const t0=d*(i+.25)/(n+.3), k=back(ph(ts,t0,t0+.4)); if(ts>=t0) idx=i; if(k>0){ const [bx,by]=slot(i); bigBlock(lerp(2300,bx,k),by,w[i],cols[i%3],1,(1-k)*.3) } }
  const ang=idx<0?.3:1.45-.22*idx; fig(X+(idx<0?0:30),P({dir:1,af1:ang,af2:.05,lean:.12+.04*Math.sin(ts*4),head:-.05}),1.6,O) };
// ---------- vignettes
S.angerSwitch=(u,ts,d)=>{ cam(980,560,1.05); const off1=d*.35, on2=d*.72; const on=ts<off1||ts>on2; paper(on?'#f6dcd4':PAPER); ground();
  const lv=ts<off1?1:ts<off1+.25?1-(ts-off1)/.25:ts<on2?0:Math.min(1,(ts-on2)/.25);
  x.save(); x.fillStyle=INK; x.fillRect(1380,G-330,140,200); x.strokeStyle=on?RED:'#8a8072'; x.lineWidth=16; x.lineCap='round'; x.beginPath(); x.moveTo(1450,G-230); x.lineTo(1450+Math.sin(lerp(-.7,.7,lv))*110,G-230-Math.cos(lerp(-.7,.7,lv))*110); x.stroke(); x.fillStyle='#fff'; x.font='700 30px Inst'; x.textAlign='center'; x.fillText(on?'ON':'OFF',1450,G-150); x.restore(); quickT(1450,G-370,'ANGER',1,46);
  const J=fig(820,on?P({dir:1,lean:.3,af1:1.6+.15*Math.sin(ts*10),af2:.1,ab1:-.4}):P({dir:1,lean:.1,head:.12,af1:.35,af2:.3,ab1:2.85,ab2:2.55}),1.6,{...MOM,dir:1,expr:on?'shouting':'happy'});
  fig(1120,P({dir:-1,head:on?.45:.05,lean:on?.25:0,af1:on?1.6:.2,af2:on?1.9:.2,ab1:on?1.5:-.2,ab2:on?1.9:.2}),1.15,{...KID,dir:-1});
  if(on) shout({hd:[J.hd[0]+40,J.hd[1]]},1,.9,1.1); else { phoneAt(J.hd[0]-HR*1.6*1.05,J.hd[1]+4,1.0,1); ring(J.hd[0]-HR*1.6*1.05,J.hd[1]+4,ts,ts<off1+.8?1:0) } };
S.goalBubble=(u,ts,d)=>{ cam(980,540,1); paper(); ground(); const calm=ph(ts,d*.8,d*.95); fig(560,P({dir:1,af1:lerp(1.2,.2,calm),af2:lerp(2.4,.1,calm),ab1:lerp(1.1,-.1,calm),ab2:lerp(2.4,.1,calm),lean:lerp(.2,.02,calm),head:lerp(-.15,.05,calm)}),1.6,YOU);
  thought(1050,330,760,360,ph(ts,.1,.5)); quickT(1050,230,'What do I want them to do?',ph(ts,.3,.7),42); const W3=['APOLOGISE','BACK DOWN','LISTEN'];
  W3.forEach((t,i)=>{ const k=back(ph(ts,d*(.25+i*.15),d*(.25+i*.15)+.4)); if(k>0){ x.save(); x.translate(820+i*235,360); x.scale(Math.max(.01,k),Math.max(.01,k)); block(0,0,215,70,t,0,{fill:[INK,RED,'#2f6f4f'][i]}); x.restore() } }) };
S.coldMachine=(u,ts,d)=>{ cam(980,540,1); paper(); ground(); wash('#9fb2c4',.32*ph(ts,.3,1.2)); const X=900; const J=fig(X,K(ts,[[0,{dir:1,af1:.4}],[.6,{dir:1,af1:1.6,af2:1.5,ab1:1.5,ab2:1.5,lean:.0},'io'],[d,{dir:1,af1:1.6,af2:1.5,ab1:1.5,ab2:1.5}]]),1.6,YOU);
  gear(J.neck[0]+4,J.neck[1]+70,34,ts*3,'#5e5a54'); gear(1300,420,90,-ts*1.2); gear(1430,300,60,ts*1.8); gear(1180,300,50,ts*2.2); quickT(1300,600,'MACHINES?',ph(ts,.4,.8),64) };
S.dominoRun=(u,ts,d)=>{ cam(980,560,1); paper(); ground(); const L=['PAST','CAUSE','EFFECT','YOU'], kd=ph(ts,.4,d*.75)*L.length;
  L.forEach((t,i)=>domino(520+i*260,Math.min(1,Math.max(0,kd-i))*1.25,t)); fig(1650,P({dir:-1,af1:lerp(.3,2.5,ph(kd,3.3,3.8)),af2:.3,lean:lerp(0,-.25,ph(kd,3.3,3.8))}),1.4,{...YOU,dir:-1}) };
S.wellSeasons=(u,ts,d)=>{ cam(980,560,1.05); const sm=ph(ts,d*.5,d*.5+.25); paper(sm<.5?'#e6edf3':'#f8ecc8'); ground(); if(sm<1) snow(ts,0,W); if(sm>0) sun(1560,220,70*sm);
  well(980,1.2); thermo(1350,G-330,'18°'); quickT(980,240,sm<.5?'WINTER: feels WARM':'SUMMER: feels COLD',1,54);
  fig(700,K(ts%(d*.5),[[0,{dir:1}],[.8,{dir:1,af1:1.5,af2:.3,lean:.35},'io'],[1.6,{dir:1,af1:1.5,af2:.3,lean:.35}],[2.0,{dir:1,af1:sm<.5?2.6:2.2,af2:sm<.5?2.6:1.2,lean:sm<.5?.0:-.25,air:sm<.5?0:25},'back']]),1.5,YOU) };
S.meaningDial=(u,ts,d)=>{ cam(980,560,1); paper(); ground(); const k=io(ph(ts,.5,d*.85)); block(700,G-280,300,90,'DIVORCE',0); quickT(700,G-160,'what happened',1,36);
  x.save(); x.translate(1300,G-300); x.strokeStyle=INK; x.lineWidth=10; x.beginPath(); x.arc(0,0,150,Math.PI,0); x.stroke(); const g=x.createLinearGradient(-150,0,150,0); g.addColorStop(0,'#3d7fa8'); g.addColorStop(1,'#d8742b'); x.strokeStyle=g; x.lineWidth=26; x.beginPath(); x.arc(0,0,120,Math.PI,0); x.stroke();
  x.strokeStyle=INK; x.lineWidth=12; x.beginPath(); x.moveTo(0,0); x.lineTo(Math.cos(Math.PI+k*Math.PI)*120,Math.sin(Math.PI+k*Math.PI)*120); x.stroke(); x.restore(); quickT(1300,G-110,'the meaning you give it',1,40);
  const J=fig(1040,P({dir:1,af1:lerp(1.2,1.7,k),af2:.5+.2*Math.sin(ts*6),lean:.15}),1.5,YOU) };
S.wallRoad=(u,ts,d)=>{ cam(980,560,1); const h=d*.5, open=ph(ts,h,h+.6); paper(); ground();
  if(open<1){ x.save(); x.globalAlpha=1-open; x.fillStyle='#5e5a54'; x.fillRect(1250,G-520,90,520); x.restore(); block(1295,G-560,360,80,'THE PAST DECIDES',0,{fill:INK}) }
  if(open>0){ x.save(); x.globalAlpha=open; x.strokeStyle=LINE; x.lineWidth=8; for(let i=0;i<8;i++){ x.beginPath(); x.moveTo(1000+i*150,G+20); x.lineTo(1080+i*150,G+20); x.stroke() } x.restore(); block(1500,G-300,320,80,'GOALS AHEAD →',0,{fill:'#2f6f4f'}) }
  let X, p; if(ts<h){ const c=ts%2.2; X=lerp(700,1170,ph(c,0,1.2)) - 160*out(ph(c,1.2,1.8)); p=c<1.2?walk(ts,1.6,1,{dir:1}):P({dir:1,lean:-.3,af1:2.2,af2:1.4,ab1:2.0,ab2:1.4,air:30*Math.sin(ph(c,1.2,1.8)*Math.PI)}); if(c>1.2&&c<1.3) SHAKE=14 } else { X=lerp(800,1700,ph(ts,h+.6,d)); p=walk(ts,1.6,1,{dir:1,lean:.08}) }
  fig(X,p,1.5,YOU) };
S.copyY=(u,ts,d)=>{ cam(980,560,1); paper(); ground(); const k=ts%3; fig(700,P({af1:2.9,af2:.2,ab1:2.7,ab2:.2,head:.2}),1.6,{col:'#e0a52b'}); sun(700,380,30);
  const fall=ph(k,1.4,1.9); fig(1250,fall<1?P({dir:-1,af1:lerp(.3,2.9,ph(k,0,.8)),ab1:lerp(-.2,2.7,ph(k,0,.8)),lean:lerp(0,.5,fall),air:0}):P({dir:-1,rot:-1.5,gy:30,af1:2.6,ab1:2.6}),1.6,{...YOU,dir:-1}); if(fall>=1&&k<2.1) dust(1250,ph(k,1.9,2.4)) };
S.agoraWalk=(u,ts,d)=>{ cam(980+ts*20,560,1); paper(); ground(); for(let i=0;i<6;i++){ x.save(); x.fillStyle='#e4dccb'; x.strokeStyle=LINE; x.lineWidth=5; x.fillRect(300+i*300,G-420,46,420); x.strokeRect(300+i*300,G-420,46,420); x.restore() }
  const X=700+ts*60; fig(X,walk(ts,1.3,.8,{dir:1,af1:1.4+.4*Math.sin(ts*4),af2:.5}),1.4,{col:'#5d5a54',beard:1}); fig(X+230,walk(ts+.3,1.3,.8,{dir:-1,ab1:1.6+.5*Math.sin(ts*5),ab2:.5}),1.4,{col:'#7a7468',dir:-1}); quickT(980+ts*20,240,'Argue it out. In public.',ph(ts,.3,.7),48) };
S.bookAvalanche=(u,ts,d)=>{ cam(980,560,1); paper(); ground(); const n=Math.floor(Math.min(16,ts*4)), fall=ph(ts,d*.6,d*.75);
  if(fall<1){ x.save(); x.translate(1180,0); x.rotate(.35*inn(fall)); x.translate(-1180,0); books(1180,n,.0); x.restore() } else { for(let i=0;i<16;i++){ x.save(); x.translate(900+i*55+Math.sin(i)*30,G-14-Math.abs(Math.sin(i*2))*20); x.rotate(Math.sin(i*1.3)); x.fillStyle=['#c9a46a','#8a5530','#5e5a54','#3d7fa8'][i%4]; x.fillRect(-45,-12,90,24); x.restore() } }
  const p=fall<1?P({dir:-1,af1:2.2,af2:.3,head:.4,lean:-.05}):P({dir:-1,rot:-1.5,gy:30,af1:2.6,ab1:2.4}); fig(1420,p,1.5,{...YOU,dir:-1}); if(fall>0&&fall<1) SHAKE=10; quickT(980,240,'piles up... thrown away',ph(ts,d*.7,d*.85),50) };
S.mirrorY=(u,ts,d)=>{ cam(980,560,1); paper(); ground(); x.save(); x.fillStyle='#e9eef2'; x.strokeStyle=INK; x.lineWidth=10; x.beginPath(); x.roundRect(1060,G-560,320,560,20); x.fill(); x.stroke(); x.restore();
  const reach=io(ph(ts,d*.45,d*.75)); fig(lerp(760,880,reach),P({dir:1,af1:lerp(.3,1.55,reach),af2:.1,lean:lerp(0,.2,reach),head:-.05}),1.6,YOU);
  x.save(); x.beginPath(); x.roundRect(1065,G-555,310,550,18); x.clip(); fig(1220,P({dir:-1,af1:2.8,ab1:2.7,head:.2}),1.6,{col:'#e0a52b',dir:-1}); sun(1220,G-470,24); if(reach>.9){ x.strokeStyle='rgba(28,28,31,.35)'; x.lineWidth=3; for(let i=0;i<4;i++){ x.beginPath(); x.arc(1080,G-280,30+i*28+ts*20%28,0,Math.PI*2); x.stroke() } } x.restore(); quickT(1220,G-600,'somebody else?',ph(ts,.3,.7),46) };
S.handPoll=(u,ts,d)=>{ cam(980,560,1); paper(); ground(); quickT(980,230,'"I like myself"?',1,58); const C=['#7a7468','#5e5a54','#8a8072','#6d6a63','#7a7468','#5e5a54'];
  for(let i=0;i<6;i++){ const X=480+i*190, half=i===3?Math.sin(ph(ts,d*.3,d*.8)*Math.PI):0; fig(X,P({af1:lerp(.2,2.9,half),af2:.1,head:.05*Math.sin(ts*2+i)}),1.25,{col:C[i]}) } };
S.stairsUp=(u,ts,d)=>{ cam(900+ts*30,560-ts*12,1); paper(); ground(); x.save(); x.strokeStyle=INK; x.lineWidth=9; x.beginPath(); x.moveTo(600,G); for(let i=0;i<9;i++){ x.lineTo(800+i*110,G-i*60); x.lineTo(800+i*110,G-(i+1)*60); } x.lineTo(1900,G-540); x.stroke(); x.restore();
  const st=ts*1.2, i=Math.floor(st), f=st-i, X=760+Math.min(st,8)*110, Y=G-Math.min(i+ io(f),8)*60; fig(X,walk(ts,1.2,1.1,{dir:1,lean:.12,air:20*Math.sin(f*Math.PI)}),1.4,{...YOU,y:Y-112*1.4}) };
S.repaint=(u,ts,d)=>{ cam(980,560,1); paper(); ground(); const k=ph(ts,.5,d*.85); x.save(); x.fillStyle='#9b968c'; x.fillRect(1000,G-520,640,520); x.fillStyle='#e8b04a'; x.fillRect(1000,G-520,640*k,520); x.restore(); block(1320,G-600,380,90,'RENEWAL',0,{fill:'#2f6f4f'});
  const X=1000+640*k-60; fig(X,P({dir:1,af1:lerp(1.2,2.6,(Math.sin(ts*6)+1)/2),af2:.2,lean:.08}),1.5,YOU); x.save(); x.strokeStyle=INK; x.lineWidth=8; x.beginPath(); x.moveTo(X+40,G-300); x.lineTo(X+70,G-300-(Math.sin(ts*6)+1)*90); x.stroke(); x.restore(); block(600,G-300,300,80,'REPLACE',0,{fill:'#8a8072'}); cross(600,G-300,90,ph(ts,.3,.8)) };
S.greekGood=(u,ts,d)=>{ cam(980,560,1); paper(); ground(); for(let i=0;i<5;i++){ x.save(); x.fillStyle='#ece5d6'; x.strokeStyle=LINE; x.lineWidth=5; x.fillRect(420+i*270,G-460,60,460); x.strokeRect(420+i*270,G-460,60,460); x.restore() } x.save(); x.fillStyle='#ece5d6'; x.beginPath(); x.moveTo(360,G-460); x.lineTo(980,G-620); x.lineTo(1600,G-460); x.fill(); x.restore();
  const f=ph(ts,d*.45,d*.6); x.save(); x.translate(980,G-260); x.scale(1,Math.abs(Math.cos(f*Math.PI))||.02); block(0,0,440,120,f<.5?'GOOD':'BENEFICIAL',0,{fill:f<.5?INK:'#2f6f4f'}); x.restore();
  fig(lerp(380,1700,ph(ts,0,d)),run(ts,2.2,{dir:1}),1.2,{col:'#5e5a54'}); x.save(); x.fillStyle='#8a5530'; const bx=lerp(380,1700,ph(ts,0,d))-40; x.beginPath(); x.arc(bx,G-150,26,0,Math.PI*2); x.fill(); x.restore() };
S.glassesTint=(u,ts,d)=>{ cam(980,560,1); const k=ph(ts,d*.38,d*.38+.15), k2=ph(ts,d*.72,d*.72+.15); paper(); ground(); wash('#3d7fa8',.22*k*(1-k2)); wash('#e8a33a',.24*k2); cloud(500,260,.9); sun(1500,230,50); for(let i=0;i<3;i++) fig(420+i*150,P({head:.1*Math.sin(ts+i)}),1.0,{col:'#8a8072'});
  const J=fig(1080,K(ts,[[0,{dir:-1}],[d*.3,{dir:-1,af1:2.6,af2:2.0,ab1:.3},'io'],[d*.45,{dir:-1,af1:.4,ab1:.2}]]),1.6,{...YOU,dir:-1}); if(ts>d*.38) shades(J,1.6,-1,1); quickT(980,180,k2>0?'a different view, a different world':'how you see the world',1,48) };
S.kidCross=(u,ts,d)=>{ cam(980,560,1); paper(); ground(); x.save(); x.strokeStyle=INK; x.lineWidth=10; x.beginPath(); x.moveTo(980,G); x.lineTo(980,G-320); x.stroke(); x.restore(); block(1120,G-300,240,60,'THIS WAY →',.05,{fill:'#2f6f4f'}); block(840,G-220,240,60,'← THAT WAY',-.05,{fill:'#8a5530'});
  const lab=['FAMILY','CULTURE','HOME']; lab.forEach((t,i)=>{ const k=back(ph(ts,.3+i*.5,.7+i*.5)); if(k>0) block(380+i*120,300+i*70,190,56,t,0,{fill:'#5e5a54'}) }); quickT(980,200,'age ~10',ph(ts,.2,.5),56);
  const go=ph(ts,d*.65,d); fig(lerp(760,1350,go),go>0?walk(ts,1.6,.8,{dir:1}):P({dir:1,head:.2*Math.sin(ts*2),af1:.4+.3*Math.sin(ts*3)}),1.0,{...YOU,dir:1}) };
S.carDrive=(u,ts,d)=>{ cam(980,560,1); paper(); ground(); const X=lerp(150,1050,io(ph(ts,.2,d*.45))); SHAKE=ts<d*.45?5:0; oldCar(X,ts,1.6,{}); for(let i=0;i<4;i++){ const c=(ts*1.5+i*.25)%1; x.save(); x.globalAlpha=(1-c)*.5; x.fillStyle='#8a8072'; x.beginPath(); x.arc(X-200-c*160,G-50-c*40,18+c*30,0,Math.PI*2); x.fill(); x.restore() } quickT(X,G-380,'FAMILIAR',1,44);
  x.save(); x.globalAlpha=.55; x.fillStyle='#d9dee3'; x.fillRect(1340,G-420,460,420); x.restore(); quickT(1570,G-200,'?',1,140); quickT(1570,G-460,'NEW: unknown',ph(ts,.4,.9),44) };
S.ifOnlyFlood=(u,ts,d)=>{ cam(980,540,1); paper(); ground(); const n=Math.floor(ph(ts,.2,d*.85)*22); for(let i=0;i<n;i++){ const bx=200+((i*397)%1500), by=160+((i*211)%520); thought(bx,by,300,110,1); quickT(bx,by+14,'IF ONLY...',1,34) }
  fig(980,P({af1:2.6,af2:2.4,ab1:2.5,ab2:2.4,lean:.15,head:.3}),1.6,YOU) };
S.novelistClock=(u,ts,d)=>{ cam(980,560,1); paper(); ground(); desk(700,420); x.save(); x.fillStyle='#fff'; x.strokeStyle=INK; x.lineWidth=4; x.fillRect(820,G-190,170,40); x.strokeRect(820,G-190,170,40); x.restore(); sitAt(1180,1.5,{dir:-1,af1:1.4+.2*Math.sin(ts*2),af2:.4,head:.15},{...YOU,dir:-1}); chair(1180,1.5,-1);
  x.save(); x.translate(1500,330); x.fillStyle='#fff'; x.strokeStyle=INK; x.lineWidth=8; x.beginPath(); x.arc(0,0,110,0,Math.PI*2); x.fill(); x.stroke(); x.lineWidth=10; x.beginPath(); x.moveTo(0,0); x.lineTo(Math.sin(ts*8)*80,-Math.cos(ts*8)*80); x.stroke(); x.lineWidth=12; x.beginPath(); x.moveTo(0,0); x.lineTo(Math.sin(ts*.7)*55,-Math.cos(ts*.7)*55); x.stroke(); x.restore();
  for(let i=0;i<3;i++){ const c=(ts*1.3+i*.33)%1; x.save(); x.globalAlpha=1-c; x.fillStyle='#f6f2e9'; x.strokeStyle=INK; x.lineWidth=3; x.translate(400+c*500,250+c*200); x.rotate(c*3); x.fillRect(-50,-60,100,120); x.strokeRect(-50,-60,100,120); x.restore() } quickT(500,200,'"one day..."',ph(ts,.3,.7),50) };
S.judged=(u,ts,d)=>{ cam(980,560,1); paper(); ground(); const k=io(ph(ts,.2,.8)); const J=fig(700,P({dir:1,af1:lerp(.3,1.7,k),af2:.2,lean:.05}),1.6,YOU); x.save(); x.fillStyle='#fff'; x.strokeStyle=INK; x.lineWidth=4; x.fillRect(J.hf[0],J.hf[1]-60,90,120); x.strokeRect(J.hf[0],J.hf[1]-60,90,120); x.restore();
  for(let i=0;i<3;i++){ const X=1150+i*210; fig(X,P({dir:-1,af1:ph(ts,1+i*.4,1.4+i*.4)*2.6,af2:.1}),1.3,{col:'#7a7468',dir:-1}); const kk=back(ph(ts,1.2+i*.4,1.6+i*.4)); if(kk>0) block(X-30,330,120,90,['2/10','3/10','NO'][i],0,{fill:RED}) } };
S.forkRoad=(u,ts,d)=>{ cam(980,560,1); paper(); ground(); x.save(); x.strokeStyle=LINE; x.lineWidth=60; x.lineCap='round'; x.beginPath(); x.moveTo(300,G+10); x.lineTo(900,G+10); x.lineTo(1500,G-260); x.moveTo(900,G+10); x.lineTo(1650,G+10); x.stroke(); x.restore();
  block(1500,G-360,260,70,'CHOICE A',0,{fill:'#8a8072'}); block(1680,G-110,260,70,'CHOICE B',0,{fill:'#2f6f4f'}); const h=d*.45; let X,Y=null,p;
  if(ts<h){ const k=ph(ts,0,h); X=k<.5?lerp(400,1150,k*2):lerp(1150,900,(k-.5)*2); Y=k<.5?G-Math.max(0,X-900)*.45:G-Math.max(0,X-900)*.45; p=walk(ts,1.6,1,{dir:k<.5?1:-1}) } else { X=lerp(900,1550,ph(ts,h,d)); p=walk(ts,1.6,1,{dir:1,lean:.1}) }
  fig(X,p,1.2,{...YOU,y:(Y??G)-112*1.2}) };
S.spotNow=(u,ts,d)=>{ cam(980,560,1); const k=ph(ts,.2,.45); paper(); ground(); wash('#14161a',.82*k); x.save(); x.globalCompositeOperation='lighter'; const g=x.createRadialGradient(980,G-200,40,980,G-200,420); g.addColorStop(0,`rgba(255,226,150,${.55*k})`); g.addColorStop(1,'rgba(255,226,150,0)'); x.fillStyle=g; x.fillRect(400,0,1200,1080); x.restore();
  fig(980,K(ts,[[0,{}],[d*.5,{}],[d*.7,{af1:1.0,af2:-.4,ab1:1.0,ab2:-.4,head:-.15,lean:-.05},'back'],[d,{af1:.9,af2:-.3,ab1:.9,ab2:-.3,head:-.1}]]),1.6,YOU); x.save(); x.globalAlpha=ph(ts,d*.4,d*.6); x.fillStyle='#f6f2e9'; x.font='700 56px Inst'; x.textAlign='center'; x.fillText('YOU decide. HERE and NOW.',980,200); x.restore() };

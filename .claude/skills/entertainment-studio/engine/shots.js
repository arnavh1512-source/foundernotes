// shots.js: real shot sizes for the stick rig. Frame a shot from the character's actual joints, so a close-up is a
// close-up. Learned the hard way (learn/dialogue-grammar-02, independent critic): our "close-ups" were full-body wides.
//   const J=jointsOf(X,pose,s,{dir});   cam(...frameShot('CU',[J]))   then draw as usual.
//   kinds: CU (head+neck), MCU (head to mid-chest), MS (head to hips), WS (whole body), TWO (both, waist up)
//   ovShoulder(side,col) after drawing: the listener's own head+shoulder in the near corner (screen space, OTS)
function jointsOf(X,p,s=1.6,o={}){ p={...STAND,...p}; const d=p.dir??o.dir??1, pt=(a,l)=>[Math.sin(a)*d*l,Math.cos(a)*l], add=(a,b)=>[a[0]+b[0],a[1]+b[1]];
  const hip=[0,0], neck=[Math.sin(p.lean)*d*TL,-Math.cos(p.lean)*TL], hd=add(neck,[Math.sin(p.lean+p.head)*d*(HR+5),-Math.cos(p.lean+p.head)*(HR+5)]), sh=[neck[0]*.9,neck[1]*.88];
  const kf=add(hip,pt(p.lf1,TH)), ff=add(kf,pt(p.lf1+p.lf2,SH)), kb=add(hip,pt(p.lb1,TH)), fb=add(kb,pt(p.lb1+p.lb2,SH));
  const low=Math.max(ff[1],fb[1],kf[1],kb[1],hd[1]+HR); const Y=o.y??(p.gy!=null?G-p.gy*s:G-low*s-(p.air||0)*s);
  const ef=add(sh,pt(p.af1,UA)), hf=add(ef,pt(p.af1+p.af2,FA)), eb=add(sh,pt(p.ab1,UA)), hb=add(eb,pt(p.ab1+p.ab2,FA));
  const w=q=>[X+q[0]*s,Y+q[1]*s]; return {hip:w(hip),neck:w(neck),hd:w(hd),sh:w(sh),ff:w(ff),fb:w(fb),hf:w(hf),hb:w(hb),R:HR*s} }
// span table: [top, bottom, share of frame height, top margin as a share of frame height]
const SHOT_SPAN={CU:[J=>J.hd[1]-J.R*1.5,J=>J.sh[1]+J.R*.6,.58,.16], MCU:[J=>Math.min(J.hd[1]-J.R*1.4,J.hf[1]-J.R,J.hb[1]-J.R),J=>lerp(J.sh[1],J.hip[1],.5),.62,.14],
  MS:[J=>Math.min(J.hd[1]-J.R*1.4,J.hf[1]-J.R,J.hb[1]-J.R),J=>J.hip[1]+J.R*.4,.64,.13], WS:[J=>Math.min(J.hd[1]-J.R*1.6,J.hf[1]-J.R,J.hb[1]-J.R),J=>Math.max(J.ff[1],J.fb[1])+J.R*.4,.6,.17], TWO:[J=>J.hd[1]-J.R*1.5,J=>J.hip[1]+J.R*.8,.6,.13]};
// returns [cx, cy, z] for cam(); bx = where the subject's centre sits across the frame (0 left .. 1 right)
function frameShot(kind,Js,bx=.5){ const sp=SHOT_SPAN[kind], top=Math.min(...Js.map(sp[0])), bot=Math.max(...Js.map(sp[1]));
  let k=sp[2]*H/(bot-top);
  // two-shots frame on the heads (outer arms may crop): in 9:16 a side-by-side pair is width-bound, so hips would shrink them to dots
  const xs=kind==='TWO'?Js.flatMap(J=>[J.hd[0]-J.R*2.6,J.hd[0]+J.R*2.6]):Js.flatMap(J=>[J.hd[0]-J.R*2,J.hd[0]+J.R*2,J.hip[0]-J.R*2.2,J.hip[0]+J.R*2.2]), wid=Math.max(...xs)-Math.min(...xs);
  if(kind==='TWO'||kind==='WS') k=Math.min(k,.94*W/wid); const tx=(Math.max(...xs)+Math.min(...xs))/2;
  const cy=top-(sp[3]-.5)*H/k, cx=tx-(bx-.5)*W/k; return [cx,cy,k/1.18] }
// share of frame height the subject's head-to-hip span covers after cam(cx,cy,z): for checks
function subjectShare(J,z){ return (J.hip[1]-(J.hd[1]-J.R))*z*1.18/H }
// over-the-shoulder foreground: the listener's head and shoulder, big, dark, soft, in the near lower corner (screen space)
function ovShoulder(side,col){ x.save(); x.setTransform(1,0,0,1,0,0); const r=Math.min(W,H)*.2, X=side<0?r*.55:W-r*.55, Y=H*.62;
  x.filter='blur(4px) brightness(.5)'; x.fillStyle=col; x.beginPath(); x.arc(X,Y,r,0,7); x.fill(); x.beginPath(); x.moveTo(X-side*r*.3,Y+r*.6); x.quadraticCurveTo(X-side*r*1.9,Y+r*1.1,X-side*r*2.3,H+40); x.lineTo(X+side*r*1.6,H+40); x.closePath(); x.fill(); x.restore() }
// Full hands for close shots (owner note 2026-11-28: "the hands are not proper"). The engine's hand is a blob barely wider
// than the arm, so at MCU/CU the arm just ends. A real hand: palm wider than the wrist, four separate fingers, a thumb.
// Opt in per episode with useFullHands(); kinds: hand/open, relaxed, fist, point, thumb, palmup, wave
function fullHand(J,e,h,kind,s,col){ if(!kind) return; const dx=J[h][0]-J[e][0], dy=J[h][1]-J[e][1], L=Math.hypot(dx,dy)||1, u=[dx/L,dy/L], side=h==='hf'?-1:1, n=[-u[1]*side,u[0]*side], [hx,hy]=J[h]; // the two hands are mirror images, so both thumbs point inward
  const P=(a,b)=>[hx+u[0]*a*s+n[0]*b*s, hy+u[1]*a*s+n[1]*b*s], rot=(v,a)=>{ a*=side; return [v[0]*Math.cos(a)-v[1]*Math.sin(a),v[0]*Math.sin(a)+v[1]*Math.cos(a)] };
  // drawn twice: first a thin gap line in the background colour (HAND_GAP), then the hand, so a hand over a same-coloured
  // body (a black hand on a black thigh, one hand over the other) still separates; the classic animation 'line gap'
  const paint=(pad,c,detail)=>{ x.save(); x.fillStyle=c; x.strokeStyle=c; x.lineCap='round'; x.lineJoin='round';
  // cartoon-hand proportions (owner: "fix the hands"): a broad round palm wider than the wrist, short thick fingers held
  // close together, and a short thick thumb set low on the side at about 40 degrees, never a peg sticking straight out
  const palm=(len=11,wid=12.5)=>{ const c=P(len*.5,0), a=Math.atan2(u[1],u[0]); x.beginPath(); x.ellipse(c[0],c[1],len*s*.6+pad,wid*s*.62+pad,a,0,7); x.fill(); const w=P(-1,0); x.beginPath(); x.ellipse(w[0],w[1],5*s+pad,6*s+pad,a,0,7); x.fill() };
  const finger=(base,dirA,len,w=4.4,curl=0)=>{ const b=P(...base); let d=rot(u,dirA); const m=[b[0]+d[0]*len*.55*s,b[1]+d[1]*len*.55*s]; d=rot(d,curl); const t=[m[0]+d[0]*len*.45*s,m[1]+d[1]*len*.45*s];
    x.lineWidth=w*s+2*pad; x.beginPath(); x.moveTo(...b); x.lineTo(...m); x.lineTo(...t); x.stroke() };
  const fingers=(spread,len,curl)=>{ for(let i=0;i<4;i++){ const off=(i-1.5)*4.3; finger([9,off],(i-1.5)*spread,len*[.9,1,.96,.8][i],3.7,curl) } };
  const thumb=(a,len=7,curl=0)=>finger([3.5,-6.6],a,len,4.4,curl);
  const fistBlock=()=>{ const c=P(5,0); x.save(); x.translate(...c); x.rotate(Math.atan2(u[1],u[0])); x.beginPath(); x.roundRect(-8*s-pad,-8.5*s-pad,16*s+2*pad,17*s+2*pad,7*s+pad); x.fill(); if(detail){ x.strokeStyle='rgba(0,0,0,.22)'; x.lineWidth=1.6*s; for(const k of [-3,1,5]){ x.beginPath(); x.moveTo(5*s,k*s); x.lineTo(8*s,k*s); x.stroke() } } x.restore() };
  if(kind==='hand'||kind==='open'){ palm(); fingers(.1,9.5,0); thumb(-.7) }
  else if(kind==='wave'){ palm(); fingers(.15,10,0); thumb(-.8) }
  else if(kind==='relaxed'){ palm(10,11); fingers(.04,8.5,.45); thumb(-.4,6.5,.35) }
  else if(kind==='palmup'){ palm(11,13); fingers(.05,8.5,-.25); thumb(-.55,6.5,-.1) }
  else if(kind==='fist'||kind==='grip'){ fistBlock(); thumb(-.5,5.2,.9) }
  else if(kind==='point'){ fistBlock(); finger([8,-2.6],-.04,11,4.2,0); thumb(-.5,5,.9) }
  else if(kind==='thumb'){ fistBlock(); const b=P(3,-6); x.lineWidth=4.8*s+2*pad; x.beginPath(); x.moveTo(...b); x.lineTo(b[0],b[1]-11*s); x.stroke() } // thumbs-up always points up
  else { palm(); fingers(.1,9.5,0); thumb(-.7) }
  x.restore() };
  paint(1.4*s,typeof HAND_GAP!=='undefined'?HAND_GAP:'rgba(255,248,235,.38)',0); paint(0,col,1) } // faint: shows over a same-coloured body, barely on the wall
function useFullHands(){ handGlyph=fullHand }

// a foreground table edge across the bottom of the frame (screen space): in 9:16 a seated two-shot otherwise leaves a dead
// floor band (critic, learn/dialogue-grammar-03). Draw after the scene, before subtitles; top = share of frame height
function ovTableEdge(top=.66,col='#7a5232',items=[]){ x.save(); x.setTransform(1,0,0,1,0,0); const Y=H*top;
  x.fillStyle='rgba(0,0,0,.18)'; x.fillRect(0,Y-10,W,14); x.fillStyle=col; x.fillRect(0,Y,W,H-Y); x.fillStyle='rgba(255,255,255,.08)'; x.fillRect(0,Y,W,10);
  x.strokeStyle='rgba(0,0,0,.12)'; x.lineWidth=3; for(let i=1;i<6;i++){ x.beginPath(); x.moveTo(0,Y+i*(H-Y)/6); x.bezierCurveTo(W*.3,Y+i*(H-Y)/6+8,W*.7,Y+i*(H-Y)/6-8,W,Y+i*(H-Y)/6); x.stroke() }
  for(const it of items) it(Y); x.restore() }

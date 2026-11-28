// shots.js: real shot sizes for the stick rig. Frame a shot from the character's actual joints, so a close-up is a
// close-up. Learned the hard way (learn/dialogue-grammar-02, independent critic): our "close-ups" were full-body wides.
//   const J=jointsOf(X,pose,s,{dir});   cam(...frameShot('CU',[J]))   then draw as usual.
//   kinds: CU (head+neck), MCU (head to mid-chest), MS (head to hips), WS (whole body), TWO (both, waist up)
//   ovShoulder(side,col) after drawing: the listener's own head+shoulder in the near corner (screen space, OTS)
function jointsOf(X,p,s=1.6,o={}){ p={...STAND,...stickRules(p)}; const d=p.dir??o.dir??1, pt=(a,l)=>[Math.sin(a)*d*l,Math.cos(a)*l], add=(a,b)=>[a[0]+b[0],a[1]+b[1]];
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
  const xs=kind==='TWO'?Js.flatMap(J=>[J.hd[0]-J.R*2.6,J.hd[0]+J.R*2.6,J.hf[0]-J.R*1.3,J.hf[0]+J.R*1.3,J.hb[0]-J.R*1.3,J.hb[0]+J.R*1.3]):Js.flatMap(J=>[J.hd[0]-J.R*2,J.hd[0]+J.R*2,J.hip[0]-J.R*2.2,J.hip[0]+J.R*2.2]), wid=Math.max(...xs)-Math.min(...xs);
  if(kind==='TWO'||kind==='WS') k=Math.min(k,.94*W/wid);
  // keep both hands inside the frame width
  if(kind==='MCU'||kind==='MS'||kind==='WS'){ const hx=Js.flatMap(J=>[J.hf[0],J.hb[0],J.hd[0]]), hw=Math.max(...hx)-Math.min(...hx)+Js[0].R*5; k=Math.min(k,.92*W/hw) }
  const tx=(Math.max(...xs)+Math.min(...xs))/2;
  const cy=top-(sp[3]-.5)*H/k, cx=tx-(bx-.5)*W/k; return [cx,cy,k/1.18] }
// share of frame height the subject's head-to-hip span covers after cam(cx,cy,z): for checks
function subjectShare(J,z){ return (J.hip[1]-(J.hd[1]-J.R))*z*1.18/H }
// over-the-shoulder foreground: the listener's head and shoulder, big, dark, soft, in the near lower corner (screen space)
function ovShoulder(side,col){ x.save(); x.setTransform(1,0,0,1,0,0); const r=Math.min(W,H)*.2, X=side<0?r*.55:W-r*.55, Y=H*.62;
  x.filter='blur(4px) brightness(.5)'; x.fillStyle=col; x.beginPath(); x.arc(X,Y,r,0,7); x.fill(); x.beginPath(); x.moveTo(X-side*r*.3,Y+r*.6); x.quadraticCurveTo(X-side*r*1.9,Y+r*1.1,X-side*r*2.3,H+40); x.lineTo(X+side*r*1.6,H+40); x.closePath(); x.fill(); x.restore() }
// Hands: plain stick arms (owner, 2026-11-28: "only stick hands no fingers"). History: blob hand -> palm-and-fingers cartoon
// hand -> finger strokes; the owner wants none of them. The arm simply ends in its round cap.
// Joints bend one way only (owner: "the hands are bending on wrong side"): an elbow folds the forearm toward the front of the
// body, so the forearm angle relative to the upper arm is never negative; a knee folds the shin backward, so its relative
// angle is never positive. stickRules() mirrors any pose that breaks this, keeping the amount of bend.
// (an arm raised above shoulder height can fold either way in our flat rig, e.g. a frontal 'hands up', so only hanging and
// forward arms are corrected)
function stickRules(p){ if(!p) return p; const q={...p}; for(const [u1,k] of [['af1','af2'],['ab1','ab2']]) if(typeof q[k]==='number'&&Math.abs(q[u1]??0)<=1.3) q[k]=Math.abs(q[k]);
  for(const k of ['lf2','lb2']) if(typeof q[k]==='number') q[k]=-Math.abs(q[k]); return q }
function fullHand(){}
function useFullHands(){ handGlyph=fullHand; if(!fig.__stick){ const f=fig; fig=(X,p,sc,o)=>f(X,stickRules(p),sc,o); fig.__stick=1 } } // plain stick hands + one-way joints

// a foreground table edge across the bottom of the frame (screen space): in 9:16 a seated two-shot otherwise leaves a dead
// floor band (critic, learn/dialogue-grammar-03). Draw after the scene, before subtitles; top = share of frame height
function ovTableEdge(top=.66,col='#7a5232',items=[]){ x.save(); x.setTransform(1,0,0,1,0,0); const Y=H*top;
  x.fillStyle='rgba(0,0,0,.22)'; x.fillRect(0,Y-14,W,16); x.fillStyle=col; x.fillRect(0,Y,W,H-Y); x.fillStyle='rgba(255,236,200,.35)'; x.fillRect(0,Y,W,12); x.fillStyle='rgba(0,0,0,.25)'; x.fillRect(0,Y+70,W,10); x.fillStyle='rgba(0,0,0,.12)'; x.fillRect(0,Y+80,W,H-Y-80);
  x.strokeStyle='rgba(0,0,0,.12)'; x.lineWidth=3; for(let i=1;i<6;i++){ x.beginPath(); x.moveTo(0,Y+i*(H-Y)/6); x.bezierCurveTo(W*.3,Y+i*(H-Y)/6+8,W*.7,Y+i*(H-Y)/6-8,W,Y+i*(H-Y)/6); x.stroke() }
  for(const it of items) it(Y); x.restore() }

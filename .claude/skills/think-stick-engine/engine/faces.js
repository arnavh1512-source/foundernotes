// faces.js: simple expressive faces for the stick cast (3/4 view toward the facing side).
// Light features on dark heads; the philosopher's mouth sits on his beard in his own colour.
const EXPR={
 neutral:{bA:0,bY:0,eye:1,mouth:.05,open:0},
 happy:{bA:-.05,bY:-1.5,eye:1,arc:1,mouth:.9,open:0},
 angry:{bA:.5,bY:1.5,eye:.72,mouth:-.55,open:0},
 shouting:{bA:.55,bY:1.8,eye:.8,mouth:-.3,open:1},
 shocked:{bA:-.25,bY:-3.2,eye:1.4,small:1,mouth:0,open:.9},
 smug:{bA:.1,bAo:-.35,bYo:-2.2,eye:.55,mouth:.55,side:1,open:0},
 sad:{bA:-.5,bY:-1,eye:.85,mouth:-.7,open:0,lookY:.5},
 thinking:{bA:0,bAo:-.15,bYo:-2.4,eye:.9,mouth:-.12,side:1,open:0,lookX:.6,lookY:-.7},
 worried:{bA:-.4,bY:-1.6,eye:1.1,mouth:-.35,open:.25},
 calm:{bA:-.05,bY:-.5,eye:.7,mouth:.35,open:0}
};
function face(J,d,s,o,ex,talk=0,blink=0){
  const E={...EXPR.neutral,...(EXPR[ex]||{})}, r=HR*s, hx=J.hd[0], hy=J.hd[1], cx=hx+d*.2*r, light='#f6f2e9';
  const eyeY=hy-.08*r, sp=.27*r, eyes=[cx-sp,cx+sp];
  x.save(); x.lineCap='round'; x.lineJoin='round';
  // eyes
  eyes.forEach((ex_,i)=>{ const far=(d>0)===(i===0); const w=.17*r*(far?.85:1), h=Math.max(.03*r,.25*r*E.eye*(1-blink*.9));
    if(E.arc&&!blink){ x.strokeStyle=light; x.lineWidth=.1*r; x.beginPath(); x.arc(ex_,eyeY+.06*r,w*1.1,Math.PI*1.1,Math.PI*1.9); x.stroke(); return }
    x.fillStyle=light; x.beginPath(); x.ellipse(ex_,eyeY,w,h,0,0,Math.PI*2); x.fill();
    if(h>.05*r){ const pr=(E.small?.055:.1)*r; x.fillStyle=INK; x.beginPath(); x.arc(ex_+d*.035*r+(E.lookX||0)*.05*r*d,eyeY+(E.lookY||0)*.07*r,pr,0,Math.PI*2); x.fill() }
    if(E.side&&i===(d>0?0:1)&&E.eye<.8){ x.fillStyle=o.col||INK; x.fillRect(ex_-w-2,eyeY-h-2,2*w+4,h*.9) } });
  // brows: inner end down when bA>0 (angry), up when bA<0 (sad/worried); "o" values for the second brow
  x.strokeStyle=light; x.lineWidth=.11*r;
  eyes.forEach((ex_,i)=>{ const other=i===(d>0?1:0), ang=(other&&E.bAo!==undefined)?E.bAo:E.bA, by=(other&&E.bYo!==undefined)?E.bYo:E.bY;
    const y0=eyeY-.42*r-by*.04*r, L=.16*r, sg=Math.sign(cx-ex_)||1; x.beginPath(); x.moveTo(ex_-sg*L,y0-ang*.08*r); x.lineTo(ex_+sg*L,y0+ang*.16*r); x.stroke() });
  // mouth
  const my=hy+(o.beard?.62:.48)*r, mx=cx+(E.side?d*.06*r:0), mw=.26*r, open=Math.min(1,(E.open||0)+talk);
  x.strokeStyle=o.beard?'#2a1f3d':light; x.lineWidth=(o.beard?.14:.1)*r;
  if(open>.08){ x.fillStyle=o.beard?'#2a1f3d':light; x.beginPath(); x.ellipse(mx,my+.02*r,mw*.7,.04*r+.11*r*open,0,0,Math.PI*2); x.fill(); if(!o.beard){ x.fillStyle='#7a2a2a'; x.beginPath(); x.ellipse(mx,my+.03*r,mw*.5,.025*r+.08*r*open,0,0,Math.PI*2); x.fill() } }
  else { const c=E.mouth*.2*r; x.beginPath(); if(E.side){ x.moveTo(mx-mw,my); x.quadraticCurveTo(mx,my+c*.4,mx+mw*d,my-c) } else { x.moveTo(mx-mw,my); x.quadraticCurveTo(mx,my+c*2,mx+mw,my) } x.stroke() }
  x.restore() }

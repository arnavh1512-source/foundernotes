// Entertainment IP overlays, drawn after the scene in screen space (studied from an owner-supplied reference, 2026-11-27;
// structure only, our own look). Driven by the shot definition in workspace.json:
//   "ui":     {"mode": "rewind"|"slow"|"play"|"ff", "text": "BASS NOTE 2"}      playback chip, top left
//   "labels": [{"t": 0.3, "end": 1.2 (optional), "noun": "JELLY", "verb": "STORES ENERGY", "at": [x, y], "to": [x, y]}]
//              screen px on the 1080x1920 (or 1920x1080) canvas; the leader line grows, then the words type on
//   "fx":     "rewind"                                                             tape-rewind bands and tracking lines
// From a second reference (a studio's "five directing moves" promo, 2026-11-27):
//   "hits":   [0.5]            THE HIT: a white impact frame at each local time, fading over the next frame or two
//   "light":  {"tint": "#ff9a3c", "alpha": 0.12, "vignette": 0.35}               LIGHT: a colour grade and vignette
//   "subs":   [[t0, t1, "line"], ...]  burned subtitles, bottom centre (dialogue)
//   "counter":{"n": 2, "of": 3, "text": "THUMP"}  a progress row (filled boxes, "2 / 3 THUMP"); "n": "?" withholds the last
//   "special":[t0, t1]  a "special moment" grade (reference-ig-03 44-47 s): the world turns cool teal and desaturated for
//              the peak, then snaps back. Scenes can add afterimages(draw, ...) for coloured trailing ghosts of black line art.
// Time itself can run ON TWOS: "twos": true on a shot or the manifest holds each drawing for two frames.
const OV={ink:'#16161a', paper:'#f6f2e9', verb:'#ffd23f', chip:'rgba(22,22,26,.84)'};
function ovIcon(mode,cx,cy,s,t){ x.fillStyle=OV.paper; x.beginPath();
  const tri=(ox,dir)=>{ x.moveTo(cx+ox,cy-s); x.lineTo(cx+ox+dir*s*1.3,cy); x.lineTo(cx+ox,cy+s); x.closePath() };
  if(mode==='rewind'){ tri(s*1.3,-1); tri(s*2.6,-1) } else if(mode==='ff'){ tri(-s*1.3,1); tri(0,1) } else tri(-s*.6,1);
  x.fill(); if(mode==='slow'){ x.globalAlpha=.5+.5*Math.sin(t*9); x.fillRect(cx+s*1.2,cy-s,s*.45,s*2); x.fillRect(cx+s*1.9,cy-s,s*.45,s*2); x.globalAlpha=1 } }
function ovUI(ui,t){ if(!ui) return; const word={rewind:'REWIND',slow:'SLOW',play:'PLAY',ff:'FAST'}[ui.mode]||'';
  // "text" may tick: [[t, "4 MIN"], [t, "11 MIN"], ...] shows the latest entry at or before t
  const tx=Array.isArray(ui.text)?(ui.text.filter(e=>e[0]<=t).pop()||[0,''])[1]:ui.text, txt=word+(tx?'  ·  '+tx:''); x.font='800 44px Inst'; const tw=x.measureText(txt).width, X0=56, Y0=W<H?130:60;
  x.fillStyle=OV.chip; x.beginPath(); x.roundRect(X0,Y0,tw+130,84,18); x.fill();
  ovIcon(ui.mode,X0+44,Y0+42,17,t); x.fillStyle=OV.paper; x.textBaseline='middle'; x.fillText(txt,X0+100,Y0+44) }
function ovLabel(L,t){ const k=t-L.t; if(k<0||(L.end!==undefined&&t>=L.end)) return; const grow=Math.min(1,k/.15), [ax,ay]=L.at, [bx,by]=L.to||L.at;
  x.font='800 56px Inst'; const w=Math.max(x.measureText(L.noun).width,x.measureText(L.verb||'').width)+36, hgt=L.verb?140:76;
  // the leader leaves the chip edge nearest its target, straight toward it, so it never cuts across a face beside the chip
  const sx=Math.max(ax+10,Math.min(ax+w-30,bx)), sy=by<ay?ay-70:ay-70+hgt;
  x.strokeStyle=OV.ink; x.lineWidth=5; x.lineCap='round'; x.beginPath(); x.moveTo(sx,sy); x.lineTo(sx+(bx-sx)*grow,sy+(by-sy)*grow); x.stroke();
  x.fillStyle=OV.ink; x.beginPath(); x.arc(bx,by,9*grow,0,7); x.fill();
  const n=Math.max(0,Math.floor((k-.12)*32)), noun=L.noun.slice(0,n), verb=(L.verb||'').slice(0,Math.max(0,n-L.noun.length));
  if(!noun) return; x.fillStyle=OV.chip; x.beginPath(); x.roundRect(ax-20,ay-70,w+6,hgt,16); x.fill();
  x.textBaseline='middle'; x.fillStyle=OV.paper; x.fillText(noun,ax,ay-32); if(verb){ x.fillStyle=OV.verb; x.fillText(verb,ax,ay+32) } }
function ovRewindFX(t){ const c=x.canvas; x.save(); x.globalAlpha=1;
  for(let i=0;i<7;i++){ const y=((i*331+t*2400)%H), h=24+(i*37)%60, dx=((i%2)?1:-1)*(14+(i*13)%30); x.drawImage(c,0,y,W,h,dx,y,W,h) }
  x.globalAlpha=.55; x.fillStyle='#ffffff'; for(let i=0;i<3;i++){ const y=((i*613+t*3100)%H); x.fillRect(0,y,W,3+i) }
  x.globalAlpha=.12; x.fillStyle='#2a3a6a'; x.fillRect(0,0,W,H); x.restore() }
function ovLight(L){ if(!L) return; x.save(); if(L.tint){ x.globalAlpha=L.alpha??.12; x.globalCompositeOperation='multiply'; x.fillStyle=L.tint; x.fillRect(0,0,W,H) }
  x.restore(); if(L.vignette){ const g=x.createRadialGradient(W/2,H*.45,Math.min(W,H)*.35,W/2,H*.45,Math.max(W,H)*.75); g.addColorStop(0,'rgba(0,0,0,0)'); g.addColorStop(1,`rgba(10,8,20,${L.vignette})`); x.fillStyle=g; x.fillRect(0,0,W,H) } }
function ovHits(hits,t){ for(const h of hits||[]){ const k=t-h; if(k>=0&&k<.1){ x.fillStyle=`rgba(255,255,255,${k<1/30?.85:.85*(1-(k-1/30)/(.1-1/30))})`; x.fillRect(0,0,W,H) } } }
function ovCounter(c){ if(!c) return; const of=c.of||3, n=c.n==='?'?of-1:c.n, bs=46, gap=16, rowW=of*bs+(of-1)*gap, X0=(W-rowW)/2, Y0=H*.075;
  for(let i=0;i<of;i++){ x.lineWidth=5; x.strokeStyle=OV.ink; x.fillStyle=i<n?OV.verb:'rgba(246,242,233,.85)'; x.beginPath(); x.roundRect(X0+i*(bs+gap),Y0,bs,bs,8); x.fill(); x.stroke() }
  x.font='800 50px Inst'; x.textAlign='center'; x.textBaseline='top'; x.fillStyle=OV.ink; x.fillText(`${c.n==='?'?n:c.n} / ${of}  ${c.n==='?'?'?':(c.text||'')}`,W/2,Y0+bs+18); x.textAlign='left' }
// coloured afterimages of black line art (pink / cyan / violet ghosts behind a fast move): draw(dt) draws the subject at
// time offset dt; a CSS filter turns black ink into a tinted, translucent ghost
function afterimages(draw,n=3,step=.04,hues=[290,170,240]){ for(let i=n;i>=1;i--){ x.save(); x.filter=`invert(1) sepia(1) saturate(7) hue-rotate(${hues[(i-1)%hues.length]}deg) opacity(${.22+.12*(n-i)})`; draw(-i*step); x.restore() } }
function ovSpecial(sp,t){ if(!sp) return; const [a,b]=sp; if(t<a||t>=b) return; x.save(); x.globalCompositeOperation='saturation'; x.globalAlpha=.65; x.fillStyle='#808080'; x.fillRect(0,0,W,H);
  x.globalCompositeOperation='multiply'; x.globalAlpha=.35; x.fillStyle='#7fb7b0'; x.fillRect(0,0,W,H); x.restore() }
function ovSubs(subs,t){ const L=(subs||[]).find(e=>t>=e[0]&&t<e[1]); if(!L) return; const fs=W<H?58:48, maxw=W*.84; x.font=`800 ${fs}px Inst`; x.textAlign='center'; x.textBaseline='middle';
  const words=String(L[2]).split(' '), lines=[]; let cur=''; for(const w of words){ const tr=cur?cur+' '+w:w; if(x.measureText(tr).width>maxw&&cur){ lines.push(cur); cur=w } else cur=tr } if(cur) lines.push(cur);
  const y0=(W<H?H-430:H-150)-(lines.length-1)*fs*1.15; lines.forEach((ln,i)=>{ const y=y0+i*fs*1.15; x.lineJoin='round'; x.lineWidth=12; x.strokeStyle='#111'; x.strokeText(ln,W/2,y); x.fillStyle='#ffe45c'; x.fillText(ln,W/2,y) }); x.textAlign='left' }
function ovDraw(shot,t){ x.setTransform(1,0,0,1,0,0); x.globalAlpha=1;
  ovLight(shot.light); ovSpecial(shot.special,t); if(shot.fx==='rewind') ovRewindFX(t); ovHits(shot.hits,t); ovCounter(shot.counter); ovUI(shot.ui,t); for(const L of shot.labels||[]) ovLabel(L,t); ovSubs(shot.subs,t) }

/* FounderNotes Painted Character Motion — original dependency-free SVG implementation.
 * Deterministic frames: identical time + shot + settings => identical SVG.
 * Reference concepts: puppet poses, parallax and shot-to-voice timing. No third-party source is copied.
 */
(function (global) {
  'use strict';
  const WIDTH = 1920, HEIGHT = 1080;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const mix = (a, b, k) => a + (b - a) * k;
  const ease = (k) => { k = clamp(k, 0, 1); return k * k * (3 - 2 * k); };
  const tween = (t, a, b, v0, v1) => mix(v0, v1, ease((t - a) / Math.max(0.0001, b - a)));
  const esc = (s) => String(s).replace(/[&<>"']/g, (ch) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const num = (n) => Number(Number(n).toFixed(3));
  const circle = (x,y,r,fill,extra='') => `<circle cx="${num(x)}" cy="${num(y)}" r="${num(r)}" fill="${fill}" ${extra}/>`;
  const ellipse = (x,y,rx,ry,fill,extra='') => `<ellipse cx="${num(x)}" cy="${num(y)}" rx="${num(rx)}" ry="${num(ry)}" fill="${fill}" ${extra}/>`;
  const rect = (x,y,w,h,fill,extra='') => `<rect x="${num(x)}" y="${num(y)}" width="${num(w)}" height="${num(h)}" fill="${fill}" ${extra}/>`;
  const path = (d,fill,extra='') => `<path d="${d}" fill="${fill}" ${extra}/>`;
  const group = (transform, contents, extra='') => `<g transform="${transform}" ${extra}>${contents}</g>`;
  const hash = (n) => { const v = Math.sin((n + 17.47) * 127.1) * 43758.5453; return v - Math.floor(v); };
  const colors = {ink:'#20242d',cream:'#f4dfbc',paper:'#e5cb9b',blue:'#1b3041',gold:'#f2ae5e',brown:'#78513a'};

  function defs() {
    return `<defs>
      <linearGradient id="fn-night" x2="0" y2="1"><stop stop-color="#172c40"/><stop offset="1" stop-color="#543b46"/></linearGradient>
      <linearGradient id="fn-study" x2="0" y2="1"><stop stop-color="#243341"/><stop offset="1" stop-color="#5b403a"/></linearGradient>
      <radialGradient id="fn-light"><stop stop-color="#ffdfa0" stop-opacity="0.8"/><stop offset="0.45" stop-color="#e9a84c" stop-opacity="0.18"/><stop offset="1" stop-color="#c67835" stop-opacity="0"/></radialGradient>
      <linearGradient id="fn-coat" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#708a8e"/><stop offset="1" stop-color="#31444b"/></linearGradient>
      <linearGradient id="fn-vest"><stop stop-color="#b98156"/><stop offset="1" stop-color="#684733"/></linearGradient>
      <linearGradient id="fn-desk"><stop stop-color="#996444"/><stop offset="1" stop-color="#553d30"/></linearGradient>
      <filter id="fn-soft"><feGaussianBlur stdDeviation="4"/></filter>
      <filter id="fn-grain"><feTurbulence baseFrequency="0.42" numOctaves="3" seed="8" result="n"/><feColorMatrix in="n" type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope="0.13"/></feComponentTransfer></filter>
      </defs>`;
  }

  // Original layer coordinate system: depth 0 distant, 1 subject, >1 foreground.
  // Focus drift uses a small motion relative to the screen center to simulate a physical camera.
  function layer(content, depth, cam, options={}) {
    if (!Number.isFinite(depth) || depth < 0 || depth > 3) throw Error('layer depth out of range');
    const panX = (cam.x || 0) * depth;
    const panY = (cam.y || 0) * depth;
    const zoom = 1 + ((cam.zoom === undefined ? 1 : cam.zoom) - 1) * depth;
    const angle = (cam.roll || 0) * depth;
    const transform = `translate(${num(960-panX)} ${num(540-panY)}) rotate(${num(angle)}) scale(${num(zoom)}) translate(-960 -540)`;
    const alpha = options.opacity === undefined ? 1 : clamp(options.opacity,0,1);
    return group(transform, content, `opacity="${num(alpha)}"`);
  }

  // Bend a flexible two-piece sleeve from shoulder to wrist. A held object must be
  // drawn in the wrist group, never at an independently animated global position.
  function arm(shoulder, wrist, tone, cuff, sign, bend=48) {
    const [sx,sy] = shoulder, [wx,wy] = wrist;
    const dx=wx-sx, dy=wy-sy, len=Math.max(1,Math.hypot(dx,dy));
    const nx=-dy/len, ny=dx/len;
    const elbow=[mix(sx,wx,0.51)+nx*bend*sign,mix(sy,wy,0.51)+ny*bend*sign];
    return `<path d="M ${num(sx)} ${num(sy)} L ${num(elbow[0])} ${num(elbow[1])} L ${num(wx)} ${num(wy)}" fill="none" stroke="#222e34" stroke-width="56" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M ${num(sx)} ${num(sy)} L ${num(elbow[0])} ${num(elbow[1])} L ${num(wx)} ${num(wy)}" fill="none" stroke="${tone}" stroke-width="43" stroke-linecap="round" stroke-linejoin="round"/>
      ${circle(elbow[0],elbow[1],24,tone)} ${circle(wx,wy,24,cuff)}`;
  }
  function hand(x, y, tone, gesture='relaxed', rotation=0) {
    let fingers='';
    if (gesture==='point') fingers=`<path d="M 0 -8 Q 16 -21 37 -27" stroke="${tone}" stroke-width="12" fill="none" stroke-linecap="round"/>`;
    if (gesture==='open') fingers=[-12,2,16].map((a)=>`<path d="M ${a} -2 L ${a+5} -28" stroke="${tone}" stroke-width="8" stroke-linecap="round"/>`).join('');
    return group(`translate(${num(x)} ${num(y)}) rotate(${rotation})`,ellipse(0,0,22,26,tone)+fingers);
  }
  function propAttached(x, y, type, rotation=0) {
    let obj='';
    if(type==='pencil') obj=rect(-4,-70,9,90,'#d4b077')+path('M-4 20 L5 20 L1 39 Z','#2b2423');
    if(type==='cup') obj=ellipse(0,0,39,16,'#f5e1bf')+rect(-37,0,74,53,'#f5e1bf')+`<path d="M 38 6 Q 76 3 71 29 Q 65 55 37 35" stroke="#f5e1bf" stroke-width="10" fill="none"/>`;
    if(type==='scroll') obj=rect(-40,-8,80,26,'#dfc69b',`rx="7"`)+circle(-40,5,12,'#b58a5c');
    return obj ? group(`translate(${num(x)} ${num(y)}) rotate(${num(rotation)})`,obj) : '';
  }

  // Controlled gestures are character-relative and keyed entirely by scene time.
  // Character coordinates: (0,0) base; body extends upward ~400px.
  function character(opts={}) {
    const kind=opts.kind==='philosopher'?'philosopher':'youth';
    const t=Number(opts.t)||0, speech=clamp(Number(opts.speech)||0,0,1);
    const age=kind==='philosopher';
    const coat=age?'url(#fn-vest)':'url(#fn-coat)',skin=age?'#c99f82':'#d7a98c';
    const hair=age?'#e9dcc7':'#262d32';
    const mood=opts.mood||'neutral';
    const blink=Math.sin(t*(age?2.1:2.8)+(age?0.5:1.9))>0.996?0.05:1;
    const eyebrows=mood==='angry'?-12:mood==='surprised'?13:0;
    const breath=3*Math.sin(t*(age?1.7:2.3));
    const nod=(opts.nod||0) * Math.sin(t*2.8);
    const tilt=(opts.tilt||0)+nod;
    const left=opts.left||[-122,-85],right=opts.right||[140,-85];
    const gest=opts.gesture||'relaxed';
    const torso=path(`M-100 -235 Q-140 -205 -139 -146 L-118 30 Q0 ${num(66+breath)} 120 30 L138 -160 Q132 -214 96 -235 Q0 -263 -100 -235 Z`,coat,'stroke="#26323b" stroke-width="7"');
    const lapels=path('M-80 -222 L-8 -145 L-34 24 L-78 -157Z',age?'#c19a70':'#96aaa9','opacity="0.8"')+path('M75 -224 L10 -145 L33 24 L85 -162Z',age?'#b78b62':'#54737a','opacity="0.75"');
    const [lx,ly]=left,[rx,ry]=right;
    const back=arm([-100,-204],left,age?'#8f6046':'#4c656b',skin,-1)+arm([100,-204],right,age?'#8f6046':'#4c656b',skin,1);
    const finger=hand(lx,ly,skin,gest)+hand(rx,ry,skin,opts.rightGesture||'relaxed');
    const held=opts.prop ? propAttached(rx,ry,opts.prop,opts.propAngle||0) : '';
    const head=group(`translate(0 ${num(-305+breath/2)}) rotate(${num(tilt)})`,
      ellipse(0,4,76,88,skin,'stroke="#6b4b43" stroke-width="4"')+
      (age?path('M-78 -8 Q-80 -110 -15 -112 Q40 -120 78 -40 Q48 -79 16 -75 Q-39 -84 -78 -8Z',hair):path('M-77 -30 Q-108 -120 -28 -132 Q21 -147 58 -102 Q86 -105 81 -35 L65 -61 Q40 -52 14 -84 Q-10 -48 -53 -63Z',hair))+
      (age?path('M-63 50 Q-74 116 0 132 Q76 118 66 45 Q30 88 0 79 Q-32 94 -63 50 Z','#e0d1ba','opacity="0.8"'):'')+
      `<path d="M-58 ${num(-26+eyebrows)} Q-32 ${num(-36+eyebrows)} -11 -26" stroke="${hair}" fill="none" stroke-width="8" stroke-linecap="round"/>
       <path d="M13 ${num(-26+eyebrows)} Q34 ${num(-38+eyebrows)} 58 -28" stroke="${hair}" fill="none" stroke-width="8" stroke-linecap="round"/>`+
      ellipse(-32,-4,11,6*blink,'#292e31')+ellipse(33,-4,11,6*blink,'#292e31')+
      path('M-3 8 Q-12 26 4 33','#00000000','stroke="#9d6e59" stroke-width="4"')+
      (speech>0.05 ? ellipse(0,61,13,4+speech*18,'#683e40') : path('M-17 59 Q0 '+(mood==='smile'?75:63)+' 18 59','#00000000','stroke="#7a4441" stroke-width="4"')));
    const out=back+torso+lapels+held+finger+head;
    return group(`translate(${num(opts.x||0)} ${num(opts.y||0)}) scale(${num(opts.scale||1)})`,out);
  }

  function stars(t=0) {let r='';for(let i=0;i<74;i++){let x=hash(i)*1920,y=hash(i+291)*630; r+=circle(x,y,1+hash(i+82)*1.5,'#ffe7c9',`opacity="${num(0.28+hash(i+48)*0.42+Math.sin(t/3+i)*0.06)}"`);}return r;}
  function skyline() {let r='';for(let i=0;i<31;i++){let x=i*67-20,h=100+hash(i+40)*200; r+=rect(x,880-h,62,h,i%4===0?'#243644':'#1d303e');for(let j=0;j<4;j++)if(hash(i*19+j)>0.45)r+=rect(x+12+j*11,890-h+hash(j+i+8)*40,6,9,'#d1a775',`opacity="${num(.4+hash(i+j)*.5)}"`);}return r;}
  function lamp(t){return `<g>${ellipse(1430,430,220,240,'url(#fn-light)',`opacity="${num(.85+.06*Math.sin(t*5))}"`)}${path('M1370 390 L1490 390 L1462 475 L1398 475Z','#e6aa63','stroke="#6e4734" stroke-width="8"')}${rect(1422,473,16,135,'#816048')}${ellipse(1430,612,60,14,'#9c7250')}</g>`;}
  function studyBack(t){return rect(0,0,WIDTH,HEIGHT,'url(#fn-study)')+rect(250,75,710,640,'#263442','stroke="#c39466" stroke-width="28"')+rect(280,108,652,583,'url(#fn-night)')+stars(t)+skyline()+rect(584,94,29,608,'#a67d59')+rect(271,386,677,25,'#a67d59')+path('M0 790 L1920 740 L1920 1080 L0 1080 Z','#413b3b')+rect(95,692,1550,28,'#84614f')+rect(115,715,32,132,'#a7805a')+lamp(t);}
  function table(t){return path('M175 724 L1730 724 L1853 996 L22 996Z','url(#fn-desk)','stroke="#362a2a" stroke-width="10"')+path('M210 748 L1690 748 L1788 953 L110 953Z','#7c523d','opacity="0.6"')+ellipse(1237,772,90,20,'#d9b58a')+rect(1210,777,60,48,'#e2c5a3')+`<path d="M1270 787 Q1310 782 1312 811 Q1313 830 1268 820" fill="none" stroke="#e2c5a3" stroke-width="12"/>`+`<path d="M1244 759 Q1228 ${num(745-6*Math.sin(t*2))} 1249 723" stroke="#ecd8bd" opacity="0.6" fill="none" stroke-width="5"/>`;}
  function paperMap(t, frac=0) {
    const k=ease(frac);
    return group(`translate(${num(900+20*k)} ${num(839-10*k)}) rotate(${num(-5+7*k)})`,
      rect(-294,-116,598,275,'#dbbf92',`rx="14" stroke="#977656" stroke-width="8"`)+
      path('M-256 -71 Q-159 -99 -88 -42 Q13 -64 109 -28 Q183 -39 248 35','none','stroke="#927b60" stroke-width="13" stroke-linecap="round" stroke-dasharray="17 10"')+
      path('M-243 98 L-80 -13 L72 65 L245 -72','none','stroke="#ab7356" stroke-width="8"')+
      rect(164,-42,79,75,'#6b655a')+rect(180,-38,42,69,'#9f6d50')+
      circle(-170,34,20,'#5c706b')+circle(40,23,17,'#5c706b')+
      path(`M-174 35 Q${num(-70+120*k)} ${num(-10-16*k)} ${num(30+180*k)} ${num(15-30*k)}`,'none',`stroke="#ecd199" stroke-width="11" stroke-dasharray="${num(460*k)} 460" stroke-linecap="round"`));
  }
  function gateBack(t){return rect(0,0,1920,1080,'#718b8a')+rect(0,500,1920,580,'#967d60')+path('M0 710 L650 465 L1280 480 L1920 800 L1920 1080 L0 1080Z','#ad956f')+rect(85,185,450,570,'#8e6e5a')+rect(1385,190,450,565,'#8e6e5a')+path('M550 795 L550 344 Q960 110 1368 344 L1368 800Z','#46545b')+[...Array(18)].map((_,i)=>rect(605+i*41,328,16,475,'#a7a39a')).join('')+rect(575,795,760,40,'#4b4a49')+circle(1216,586,34,'#d3a367')+circle(1216,586,12,'#6b584b')+path('M1 1040 L1918 1040','#000','stroke="#5e554a" stroke-width="18"');}
  function stairsBack(t){let steps='';for(let j=0;j<12;j++){const y=1000-j*38,w=1200-j*55;steps+=path(`M${num(960-w/2)} ${num(y)} L${num(960+w/2)} ${num(y)} L${num(960+(w-15)/2)} ${num(y-30)} L${num(960-(w-15)/2)} ${num(y-30)}Z`,j%2?'#bca280':'#ccb18a','stroke="#8f7c67" stroke-width="3"');}return rect(0,0,1920,1080,'#809a93')+path('M0 0 L580 0 L650 1080 L0 1080Z','#a47c66')+path('M1920 0 L1330 0 L1280 1080 L1920 1080Z','#be9a79')+steps+rect(485,210,145,290,'#433a3a')+rect(1425,182,140,296,'#4a4d50')+ellipse(960,190,300,180,'#d9bc8c',`opacity="${num(.75+.05*Math.sin(t/3))}"`);}
  // Caption text wraps by words into at most two lines of CAPTION_CHARS (~1150px of 34px Georgia inside the
  // 1350px box); the box grows upward for the second line and an overlong second line ends in an ellipsis.
  const CAPTION_CHARS=64;
  function wrapCaption(text,max=CAPTION_CHARS){
    const lines=[''];
    for(const w of String(text).split(/\s+/).filter(Boolean)){const i=lines.length-1;if(lines[i]&&(lines[i]+' '+w).length>max&&i===0)lines.push(w);else lines[i]=lines[i]?lines[i]+' '+w:w;}
    return lines.map((l)=>l.length>max?l.slice(0,max-1).trimEnd()+'…':l);
  }
  function caption(label,text){const lines=wrapCaption(text),up=(lines.length-1)*40;return group('translate(0 0)',rect(285,947-up,1350,108+up,'#121c29','opacity="0.85" rx="14"')+`<text x="960" y="${984-up}" font-family="Georgia,serif" font-size="27" fill="#e2bc87" text-anchor="middle">${esc(label)}</text><text x="960" y="${1027-up}" font-family="Georgia,serif" font-size="34" fill="#fcf0dd" text-anchor="middle">${lines.map((l,i)=>`<tspan x="960" dy="${i?40:0}">${esc(l)}</tspan>`).join('')}</text>`);}

  const DEFAULT_BEATS = [
    {id:'gate',duration:4.2,speaker:'YOUTH',text:'Every road ends at a locked gate.'},
    {id:'study',duration:4.2,speaker:'PHILOSOPHER',text:'Who drew the map you are holding?'},
    {id:'map',duration:4.2,speaker:'YOUTH',text:'The map says there are no other routes.'},
    {id:'stairs',duration:4.2,speaker:'PHILOSOPHER',text:'What about the stairs behind the bakery?'},
    {id:'close',duration:4.2,speaker:'PHILOSOPHER',text:'An accurate map can still leave something out.'}
  ];
  function resolveBeat(beats, t){let start=0;for(let i=0;i<beats.length;i++){let end=start+beats[i].duration;if(t<end||i===beats.length-1)return {beat:beats[i],index:i,local:clamp(t-start,0,beats[i].duration),start}; start=end;}throw Error('empty beats')}
  function draw(beat, s, duration, absTime, showCaptions=true) {
    const progress=clamp(s/Math.max(duration,0.01),0,1);
    const zoom=1+0.07*ease(progress),camera={x:18*progress,y:8*progress,zoom};
    let bg='',near='',subjects='';
    switch(beat.id){
      case 'gate': bg=gateBack(absTime);near=group('translate(1200 705)',character({kind:'youth',x:0,y:0,scale:1.14,t:absTime,mood:'angry',left:[-150,-5],right:[112,-30],gesture:'point'}));break;
      case 'study': bg=studyBack(absTime);subjects=character({kind:'youth',x:430,y:755,scale:1.05,t:absTime,mood:'surprised',left:[-135,-30],right:[170,-75]})+character({kind:'philosopher',x:1480,y:750,scale:1.0,t:absTime,mood:'smile',left:[-116,-80],right:[110,-85]});near=table(absTime)+paperMap(absTime,0.2);break;
      case 'map': bg=studyBack(absTime);subjects=character({kind:'youth',x:440,y:800,scale:1.03,t:absTime,left:[-85,-30],right:[165,20],gesture:'point',prop:'pencil',propAngle:20});near=table(absTime)+paperMap(absTime,progress);break;
      case 'stairs': bg=stairsBack(absTime);subjects=character({kind:'youth',x:540,y:980,scale:1.2,t:absTime,mood:'surprised',left:[-150,-25],right:[175,-80]});near=ellipse(1620,1020,350,40,'#716659','opacity="0.28"');break;
      case 'close':bg=studyBack(absTime);subjects=character({kind:'youth',x:470,y:776,scale:1,t:absTime,mood:'smile',left:[-115,-30],right:[165,-20],prop:'pencil'})+character({kind:'philosopher',x:1460,y:776,scale:1,t:absTime,mood:'smile',left:[-118,-65],right:[110,-80]});near=table(absTime)+paperMap(absTime,1);break;
      default:throw Error('Unknown shot: '+beat.id);
    }
    const body=layer(bg,0.25,camera)+layer(subjects,1,camera)+layer(near,1.2,camera)+rect(0,0,1920,1080,'#f9e8c8','opacity="0.055" filter="url(#fn-grain)"');
    const subtitle=showCaptions?caption(beat.speaker,beat.text):'';
    return defs()+body+subtitle;
  }
  function validate(beats){if(!Array.isArray(beats)||!beats.length)throw Error('beats must be a nonempty array');let d=0;for(const b of beats){if(!['gate','study','map','stairs','close'].includes(b.id))throw Error('unsupported beat '+b.id);if(!Number.isFinite(b.duration)||b.duration<=0)throw Error('invalid duration');d+=b.duration;}return d;}
  function mount(svg, program={}){
    if(!svg||svg.tagName.toLowerCase()!=='svg')throw Error('Expected an SVG root');
    const beats=program.beats||DEFAULT_BEATS;const duration=validate(beats);
    svg.setAttribute('viewBox','0 0 1920 1080');svg.setAttribute('xmlns','http://www.w3.org/2000/svg');
    return {duration, seek:(t)=>{const time=clamp(Number(t)||0,0,duration-0.00001);const {beat,local}=resolveBeat(beats,time);svg.innerHTML=draw(beat,local,beat.duration,time,program.captions!==false);return {shot:beat.id,time,local};}};
  }
  global.FNPaintedMotion=Object.freeze({WIDTH,HEIGHT,clamp,ease,tween,hash,layer,character,propAttached,draw,validate,mount,DEFAULT_BEATS});
})(window);

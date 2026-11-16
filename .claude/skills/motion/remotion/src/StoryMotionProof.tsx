import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {gripTransform, layerMatrix, mix, progress, solveArm, svgMatrix} from '../../assets/story-motion.mjs';

// Original technical fixture, with manual action times; not a narrated episode.
const Book: React.FC = () => <g><rect x={-20} y={-120} width={125} height={140} rx={7} fill="#536f65" stroke="#263f37" strokeWidth={4}/><path d="M-5 -114V14M22 -82H78M22 -64H62" stroke="#d3d9bd" strokeWidth={4}/></g>;
const Hand: React.FC = () => <g fill="url(#skin)" stroke="#764d39" strokeWidth={3} strokeLinejoin="round"><path d="M-12 15L-18 -6Q-16 -20 -9 -12L-4 0L-7 -28Q-5 -36 0 -29L6 -5L3 -34Q6 -40 10 -32L16 -6L14 -28Q18 -34 22 -23L27 0L28 -14Q33 -19 36 -8L39 14Q26 31 3 29Z"/></g>;
export const StoryMotionProof: React.FC = () => {
  const frame = useCurrentFrame(); const {fps, width, height} = useVideoConfig(); const t = frame / fps;
  const reach = progress(t, .1, 1.3), lift = progress(t, 1.6, 1.2), back = progress(t, 4.1, 1.2), release = progress(t, 5.3, .6);
  const bookX = mix(970, 955, lift * (1 - back)), bookY = mix(680, 540, lift * (1 - back));
  const angle = -12 * lift * (1 - back); const held = t >= 1.4 && t < 5.3;
  const target = held ? [bookX, bookY] : [mix(840, 970, reach * (1 - release)), mix(760, 680, reach * (1 - release))];
  const lean = 12 * reach * (1 - release), arm = solveArm([780 + lean, 520], target, 145, 140, -1);
  const camera = {x: mix(-22, 22, t / 6), y: -5, zoom: mix(1, 1.055, t / 6), roll: 0};
  const layer = (depth: number) => svgMatrix(layerMatrix(camera, depth, width, height));
  const armPath = `M${arm.shoulder.join(' ')}L${arm.elbow.join(' ')}L${arm.wrist.join(' ')}`;
  const glance = 5 * lift * (1 - back);
  return <AbsoluteFill style={{backgroundColor: '#e9dfce'}}><svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
    <defs><linearGradient id="wall" x2="0" y2="1"><stop stopColor="#f6edda"/><stop offset="1" stopColor="#b9b8a2"/></linearGradient><linearGradient id="skin"><stop stopColor="#e5b38b"/><stop offset="1" stopColor="#ae7355"/></linearGradient><linearGradient id="shirt"><stop stopColor="#63887d"/><stop offset="1" stopColor="#304e48"/></linearGradient><radialGradient id="light"><stop stopColor="#fff3c4" stopOpacity=".6"/><stop offset="1" stopColor="#fff3c4" stopOpacity="0"/></radialGradient></defs>
    <g transform={layer(.12)}><rect x={-200} y={-200} width={2320} height={1500} fill="url(#wall)"/><rect x={1200} y={180} width={400} height={430} rx={8} fill="#b5c7c2" stroke="#e7dfc9" strokeWidth={24}/><path d="M1400 190V600M1210 390H1590" stroke="#e7dfc9" strokeWidth={14}/><ellipse cx={1250} cy={400} rx={650} ry={550} fill="url(#light)"/></g>
    <g transform={layer(.5)}><rect x={-200} y={810} width={2320} height={500} fill="#b49e7d"/><path d="M0 810H1920M300 810L100 1080M1350 810L1620 1080" stroke="#918c73" strokeWidth={5}/><rect x={600} y={505} width={210} height={335} rx={30} fill="#b59c73"/></g>
    <g transform={layer(1)}>
      <ellipse cx={710} cy={900} rx={190} ry={30} fill="#394d40" opacity=".15"/>
      <path d="M650 730L620 890M750 730L800 890" stroke="#3a4944" strokeWidth={48} strokeLinecap="round"/>
      <path d={`M610 505Q690 470 ${790 + lean} 505L790 755Q700 790 610 750Z`} fill="url(#shirt)" stroke="#29483e" strokeWidth={5}/>
      <path d="M625 525L580 630L600 750" stroke="#764d39" strokeWidth={35} fill="none" strokeLinecap="round"/>
      <path d="M625 525L580 630L600 750" stroke="url(#skin)" strokeWidth={29} fill="none" strokeLinecap="round"/>
      <g transform={`translate(${690 + lean} 388) rotate(${-3 + glance})`}><path d="M-24 88V122H25V88" fill="url(#skin)"/><ellipse rx={69} ry={91} fill="url(#skin)" stroke="#764d39" strokeWidth={4}/><path d="M-67 -12Q-86 -101 2 -106Q70 -101 69 -18L41 -62Q-2 -41 -37 -65Z" fill="#343b32"/>{[-26,26].map(x=><g key={x}><ellipse cx={x} cy={-3} rx={12} ry={9} fill="#fff7e9"/><circle cx={x+3+glance*.5} cy={-3} r={5} fill="#303d33"/><path d={`M${x-14} -27L${x+12} -30`} stroke="#414638" strokeWidth={5}/></g>)}<path d="M4 0L13 27L3 29M-15 52Q3 62 24 47" fill="none" stroke="#86563e" strokeWidth={4}/></g>
      <path d={armPath} fill="none" stroke="#764d39" strokeWidth={36} strokeLinecap="round" strokeLinejoin="round"/><path d={armPath} fill="none" stroke="url(#skin)" strokeWidth={29} strokeLinecap="round" strokeLinejoin="round"/>
      {!held && <g transform={`translate(970 680)`}><Book/></g>}
      <g transform={gripTransform(arm, angle)}>{held && <Book/>}<Hand/></g>
    </g>
    <g transform={layer(1.25)}><path d="M890 700H1620L1710 765H860Z" fill="#b08758" stroke="#6e644e" strokeWidth={5}/><path d="M905 767L900 1000M1630 767L1680 1000" stroke="#75634b" strokeWidth={25}/><ellipse cx={1605} cy={550} rx={70} ry={110} fill="#617863"/><rect x={1550} y={625} width={100} height={90} rx={12} fill="#9f7453"/></g>
    <text x={110} y={1000} fontFamily="sans-serif" fontSize={30} fill="#3f5149">Technical motion test · manual cues · no narration</text>
  </svg></AbsoluteFill>;
};

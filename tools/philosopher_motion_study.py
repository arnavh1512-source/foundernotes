"""Original silent blocking study. Pillow + FFmpeg; no external assets or TTS.

This is a craft test, not the narrated pilot or an automatic creative review.
Run: python tools/philosopher_motion_study.py --out PATH --cut 1
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import random
import shutil
import subprocess
import struct
import wave
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DURATION = 960, 540, 24, 24
INK = '#263537'
PAPER = '#ead9b7'
GOLD = '#d6a55e'
KIT_FONTS = Path(__file__).resolve().parents[1] / '.claude/skills/podcast-scout-skill/assets/ink-gold-kit/fonts'


def load_font(size, *candidates):
    # Windows system fonts first (the study was drawn with them), then the repo's bundled fonts, so it runs anywhere.
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT = load_font(22, 'C:/Windows/Fonts/georgia.ttf', str(KIT_FONTS / 'Lora-Bold.ttf'))
SMALL = load_font(12, 'C:/Windows/Fonts/arial.ttf', str(KIT_FONTS / 'InstrumentSans-Regular.ttf'))

def ease(t, a, b):
    k = max(0, min(1, (t-a)/(b-a)))
    return k*k*(3-2*k)

def lerp(a, b, k):
    return a+(b-a)*k

def arm_joint(shoulder,hand,upper=70,lower=75,bend=1):
    """Solve a reachable two-link arm without changing either bone length."""
    dx,dy=hand[0]-shoulder[0],hand[1]-shoulder[1]
    distance=math.hypot(dx,dy)
    if not abs(upper-lower)<distance<upper+lower:
        raise ValueError('Hand target is outside the arm reach')
    a=(upper*upper-lower*lower+distance*distance)/(2*distance)
    h=math.sqrt(max(0,upper*upper-a*a))
    ux,uy=dx/distance,dy/distance
    return shoulder[0]+ux*a+bend*uy*h,shoulder[1]+uy*a-bend*ux*h

def line(d, pts, fill, width=3):
    width=max(1,round(width))
    d.line(pts, fill=fill, width=width, joint='curve')
    r = width/2
    for x,y in (pts[0],pts[-1]):
        d.ellipse((x-r,y-r,x+r,y+r), fill=fill)

def background(kind):
    im = Image.new('RGB',(W,H))
    d = ImageDraw.Draw(im)
    top,bottom = ((31,51,63),(128,109,94)) if kind != 'dawn' else ((71,100,111),(225,184,126))
    for y in range(H):
        k=y/H
        d.line((0,y,W,y),fill=tuple(int(lerp(a,b,k)) for a,b in zip(top,bottom)))
    rng=random.Random(31)
    if kind in ('gate','dawn','stairs'):
        for depth in range(3):
            base=350+depth*42
            color=['#475d61','#3c5054','#2c4146'][depth]
            pts=[(0,H),(0,base)]
            pts += [(x,base-rng.randrange(8,58)) for x in range(0,W+60,60)]
            pts += [(W,H)]
            d.polygon(pts,fill=color)
        for x in range(20,960,44):
            y=370+rng.randrange(10,90)
            d.rectangle((x,y,x+25,y+45),fill='#31484a')
            if rng.random()>.35:
                d.rectangle((x+9,y+13,x+13,y+19),fill='#d2b16e')
    if kind=='gate':
        d.polygon([(0,420),(580,420),(810,540),(0,540)],fill='#9c8c72')
        d.rectangle((555,55,820,465),fill='#5c6260')
        d.rounded_rectangle((582,98,790,473),radius=100,fill='#283b3d')
        d.rectangle((582,212,790,473),fill='#283b3d')
        for x in range(597,790,22):
            d.line((x,180,x,473),fill='#6c6f61',width=7)
        d.rectangle((582,280,790,291),fill='#6c6f61')
        d.rectangle((582,379,790,390),fill='#6c6f61')
        d.rectangle((672,290,702,320),fill='#b79b65')
        d.rectangle((682,298,691,314),fill='#4d534c')
    elif kind=='study':
        d.rectangle((0,0,W,415),fill='#334449')
        d.rectangle((86,70,324,318),fill='#a58b64')
        d.rectangle((96,80,314,308),fill='#749095')
        d.ellipse((139,122,190,173),fill='#debe83')
        line(d,[(205,80),(205,308)],'#a58b64',8)
        line(d,[(96,214),(314,214)],'#a58b64',8)
        for y in (112,184,256):
            d.rectangle((700,y,903,y+8),fill='#93785c')
            for x in range(714,890,24):
                ht=rng.randrange(25,48)
                d.rectangle((x,y-ht,x+15,y),fill=rng.choice(['#897b65','#647c79','#b49a72']))
        d.rectangle((0,415,W,H),fill='#6c6253')
        for x in range(-200,1200,110):
            d.line((480+(x-480)*.45,415,x,540),fill='#807360',width=2)
    elif kind=='stairs':
        for i in range(9):
            x,y=100+i*77,488-i*30
            d.polygon([(x,y),(x+100,y),(x+100,540),(x,540)],fill='#68726b')
            d.rectangle((x,y,x+100,y+9),fill='#b2ac8f')
    return im

BACKGROUNDS={k:background(k) for k in ['gate','study','stairs','dawn']}

def character(d,x,y,s=1,old=False,tilt=0,reach=None,gaze=1,walk=0,lean=0,feet=None,eyes_down=False,expression='neutral',blink=False,left_reach=None,front_arm=False):
    """Feet origin; hand targets and limbs share a character-local transform."""
    skin='#d5ac84' if not old else '#d4b393'
    coat='#719493' if not old else '#ad815c'
    dark='#344c51' if not old else '#745b48'
    def p(a,b): return (x+s*(a+lean*(-b/150)),y+s*b)
    stride=math.sin(walk)*20
    lf,rf=feet or ((-17-stride,0),(17+stride,0))
    line(d,[p(-12,-77),p((lf[0]-12)/2,-37+lf[1]*.4),p(*lf)],'#253b40',13*s)
    line(d,[p(12,-77),p((rf[0]+12)/2,-37+rf[1]*.4),p(*rf)],'#30494e',13*s)
    line(d,[p(lf[0]-3,lf[1]-1),p(lf[0]+12,lf[1]-1)],'#172d34',7*s)
    line(d,[p(rf[0]-3,rf[1]-1),p(rf[0]+12,rf[1]-1)],'#172d34',7*s)
    d.polygon([p(-25,-146),p(21,-146),p(30,-73),p(-29,-73)],fill=coat)
    d.polygon([p(-25,-146),p(-7,-133),p(-4,-74),p(-29,-73)],fill=dark)
    line(d,[p(-2,-137),p(0,-80)],'#bdd0bd' if not old else '#d3b58b',2*s)
    hx,hy=p(tilt,-170)
    d.ellipse((hx-24*s,hy-29*s,hx+24*s,hy+25*s),fill=skin)
    if old:
        d.pieslice((hx-25*s,hy-31*s,hx+25*s,hy+27*s),180,345,fill='#d7d4bd')
        d.polygon([(hx-21*s,hy+5*s),(hx+23*s,hy+4*s),(hx+6*s,hy+47*s),(hx-14*s,hy+29*s)],fill='#ded8bf')
        line(d,[(hx-15*s,hy-5*s),(hx+17*s,hy-5*s)],'#676e62',2*s)
    else:
        d.pieslice((hx-27*s,hy-34*s,hx+25*s,hy+18*s),165,355,fill='#263a3e')
        d.polygon([(hx-25*s,hy-17*s),(hx-12*s,hy-40*s),(hx+23*s,hy-22*s),(hx+10*s,hy-8*s)],fill='#263a3e')
    ex=hx+gaze*8*s
    ey=hy+(5 if eyes_down else -3)*s
    if blink:
        line(d,[(ex-3*s,ey),(ex+3*s,ey)],'#25363b',1*s)
    else:
        d.ellipse((ex-2*s,ey-2*s,ex+2*s,ey+2*s),fill='#25363b')
    brow=4 if expression=='strained' else 0
    line(d,[(ex-5*s,ey-8*s-brow),(ex+4*s,ey-7*s+brow)],'#4a4940',2*s)
    if not old:
        mouth=2 if expression=='strained' else -1
        line(d,[(hx+3*s,hy+14*s),(hx+11*s,hy+(14+mouth)*s)],'#805d4c',2*s)
    left=left_reach or (-34,-91+math.sin(walk)*8)
    right=reach or (34,-91-math.sin(walk)*8)
    for side,hand in [(-1,left),(1,right)]:
        if front_arm and side==1:
            continue
        shoulder=(side*20,-137)
        elbow=((shoulder[0]+hand[0])*.5+side*12,(shoulder[1]+hand[1])*.5+16)
        line(d,[p(*shoulder),p(*elbow),p(*hand)],coat,12*s)
        cx,cy=p(*hand)
        d.ellipse((cx-6*s,cy-6*s,cx+6*s,cy+6*s),fill=skin)
    return p(*right)

def map_sheet(d,box,progress=0,continuous=False):
    x,y,w,h=box
    d.polygon([(x,y+5),(x+w-7,y),(x+w,y+h),(x+5,y+h-3)],fill=PAPER)
    for k in range(1,5):
        line(d,[(x+k*w/5,y+10),(x+k*w/5-8,y+h-8)],'#c5b48f',1)
    road=[(x+w*.17,y+h*.76),(x+w*.35,y+h*.45),(x+w*.65,y+h*.48),(x+w*.83,y+h*.20)]
    line(d,road,'#a57e54',4)
    for px,py in road:
        d.ellipse((px-4,py-4,px+4,py+4),fill='#8c704e')
    route=[(x+w*.35,y+h*.45),(x+w*.46,y+h*.20),(x+w*.64,y+h*.15)]
    if progress>0:
        if not continuous:
            line(d,route[:2],'#477876',5)
            if progress>.6: line(d,route[1:],'#477876',5)
        else:
            q=min(1,progress/.6)
            end=(lerp(route[0][0],route[1][0],q),lerp(route[0][1],route[1][1],q))
            line(d,[route[0],end],'#477876',5)
            if progress>.6:
                q=(progress-.6)/.4
                end=(lerp(route[1][0],route[2][0],q),lerp(route[1][1],route[2][1],q))
                line(d,[route[1],end],'#477876',5)

def caption(im,text,sub):
    d=ImageDraw.Draw(im)
    d.rectangle((0,468,W,H),fill='#172e35')
    d.text((W/2,483),text,font=FONT,anchor='mt',fill='#eee0c0')
    d.text((W/2,516),sub,font=SMALL,anchor='mt',fill='#acbdb7')
    d.text((27,24),'FOUNDER / NOTES',font=SMALL,fill='#e0caa4')

def frame(t,cut):
    shot=min(4,int(t/4.8)); u=t-shot*4.8
    im=BACKGROUNDS[['gate','study','study','stairs','dawn'][shot]].copy()
    d=ImageDraw.Draw(im)
    if shot==0:
        x=lerp(380,510,ease(u,0,1.4))
        walking=u<1.4
        stop=ease(u,1.3,2)
        d.ellipse((x-40,441,x+50,458),fill='#776f5e')
        if cut>=3:
            release=ease(u,3.15,4.15)
            lean=stop*(4+2*math.sin(u*9)*(1-release))-8*release
            hand_x=lerp(33,(597-x)/1.18-lean*138/150,stop)
            character(d,x,449,1.18,reach=(lerp(hand_x,29,release),lerp(lerp(-92,-138,stop),-95,release)),gaze=1,walk=u*8 if walking else 0,lean=lean,tilt=-5*release,eyes_down=release>.5,expression='strained' if stop>.5 else 'neutral',blink=2.45<u<2.58)
        else:
            character(d,x,449,1.18,reach=(lerp(33,63,stop),lerp(-92,-138,stop)),gaze=1,walk=u*8 if walking else 0,lean=4*stop,expression='strained' if cut>=2 and stop>.5 else 'neutral')
        d.text((670,80),'CLOSED',font=SMALL,fill='#ded0ad')
        caption(im,'The familiar way is closed.','01 / THE OBSTACLE')
    elif shot==1:
        k=ease(u,1.2,2.8)
        reaction=ease(u,2.5,3.7) if cut>=3 else 0
        character(d,355,455,1.12,tilt=lerp(9,-5,reaction) if cut>=3 else lerp(9,0,k),gaze=1,reach=(58,-99),lean=8+6*reaction,eyes_down=cut>=2,blink=cut>=3 and 2.3<u<2.45)
        character(d,660,455,1.16,old=True,gaze=-1,reach=(-45,-108),eyes_down=cut>=2,blink=cut>=3 and .6<u<.75,front_arm=cut>=3)
        d.polygon([(230,350),(730,350),(790,417),(190,417)],fill='#9b7755')
        d.polygon([(190,417),(790,417),(790,434),(190,434)],fill='#684e3d')
        d.rectangle((238,434,250,468),fill='#4e4036')
        d.rectangle((730,434,742,468),fill='#4e4036')
        map_sheet(d,(390,357,190,48),k,continuous=cut>=2)
        # Foreground hand must remain visible over the tabletop.
        if cut>=2:
            q=ease(u,.7,2.2)
            hx,hy=lerp(613,563,q),lerp(343,369,q)
            joint=arm_joint((683,296),(hx,hy)) if cut>=3 else (625,331)
            line(d,[(683,296),joint,(hx,hy)],'#ad815c',14)
            d.ellipse((hx-6,hy-6,hx+6,hy+6),fill='#d4b393')
        caption(im,'He looks again. This time, at the gaps.','02 / THE QUESTION')
    elif shot==2:
        d.rectangle((0,0,W,H),fill='#816d54')
        map_sheet(d,(180,55,600,370),ease(u,.6,3.8),continuous=cut>=2)
        k=ease(u,.6,3.8)
        if cut==1:
            px,py=lerp(390,564,k),lerp(222,111,k)
        else:
            # Follow the exact two-segment ink path; hand and line share geometry.
            q=min(1,k/.6)
            px,py=lerp(390,456,q),lerp(221.5,129,q)
            if k>.6:
                q=(k-.6)/.4; px,py=lerp(456,564,q),lerp(129,110.5,q)
        d.polygon([(px-49,540),(px+48,540),(px+20,py+38),(px-9,py+12)],fill='#ad815c')
        d.rounded_rectangle((px-8,py,px+12,py+62),radius=9,fill='#d4b393')
        caption(im,'A small path was missing from the map.','03 / THE DISCOVERY')
    elif shot==3:
        if cut==1:
            k=ease(u,.2,4.6)
            x=lerp(220,650,k); y=488-(x-100)*30/77
            character(d,x,y,1.1,gaze=1,walk=u*7,lean=8)
        else:
            q=1+min(5.8,max(0,u-.2)/.72)
            n=int(q); f=q-n; k=ease(f,0,1)
            planted=(145+n*77,488-n*30)
            swing=(145+(n-1+2*k)*77,488-(n-1+2*k)*30-math.sin(math.pi*f)*28)
            x=(planted[0]+swing[0])/2
            y=488-(n-.5+k)*30
            lf,rf=(planted,swing) if n%2 else (swing,planted)
            feet=tuple(((px-x)/1.1-8*(-(py-y)/1.1/150),(py-y)/1.1) for px,py in (lf,rf))
            character(d,x,y,1.1,gaze=1,lean=8,feet=feet)
        caption(im,'He tests the path with his own feet.','04 / THE ACTION')
    else:
        d.ellipse((650,56,748,154),fill='#e9c88a')
        d.polygon([(0,456),(440,328),(960,452),(960,540),(0,540)],fill='#314b4b')
        k=ease(u,0,1.4)
        if cut>=3:
            settle=ease(u,1.4,2.3)
            lift=ease(u,2.4,3.6)
            character(d,lerp(370,440,k),395,.78,gaze=1,walk=u*6 if u<1.4 else 0,lean=lerp(6,-3,settle)+math.sin(u*2)*.8*settle,tilt=4*lift,reach=(lerp(34,54,lift),lerp(-91,-124,lift)),blink=1.6<u<1.75)
        else:
            character(d,lerp(370,440,k),395,.78,gaze=1,walk=u*6 if u<1.4 else 0)
        caption(im,'The map was old. The world was not.','05 / THE CHANGE  ·  SILENT MOTION STUDY')
    # Reproducible paper grain is part of the original drawing, not external media.
    im=Image.blend(im,TEXTURE,.045)
    return im

rng=random.Random(17)
TEXTURE=Image.new('RGB',(W,H)); TEXTURE.putdata([(v,v,v) for v in (rng.randrange(256) for _ in range(W*H))])

def stick_background():
    im=Image.new('RGB',(W,H),'#eee8da')
    d=ImageDraw.Draw(im)
    for x,h in [(70,110),(135,145),(225,94),(785,130),(865,165)]:
        d.rectangle((x,425-h,x+52,425),fill='#d9d9cb')
        for y in range(425-h+15,414,24):
            d.rectangle((x+12,y,x+20,y+10),fill='#c3cabb')
    d.rectangle((0,425,W,H),fill='#d8cbb4')
    d.line((0,425,W,425),fill='#b9aa91',width=3)
    for n in range(5):
        x,y=55+n*34,425-n*17
        d.rectangle((x,y,x+48,445),fill='#a7b5a7')
        d.line((x,y,x+48,y),fill='#6f8c7f',width=3)
    d.rounded_rectangle((580,92,826,427),radius=110,fill='#b6b6a5')
    d.rectangle((580,215,826,427),fill='#b6b6a5')
    d.rounded_rectangle((600,115,806,427),radius=94,fill='#40565a')
    d.rectangle((600,220,806,427),fill='#40565a')
    for x in range(612,803,24):
        line(d,[(x,205),(x,423)],'#82928c',6)
    line(d,[(600,310),(806,310)],'#b8b29a',8)
    d.rounded_rectangle((684,302,715,331),radius=5,fill='#d3aa64')
    d.text((703,158),'CLOSED',font=SMALL,anchor='mm',fill='#eee8da')
    d.text((44,35),'FOUNDER NOTES / ORIGINAL MOTION STUDY',font=SMALL,fill='#6d7d72')
    return im

STICK_BG=stick_background()

def stick_arm(shoulder,target,weight,side):
    upper,lower=44,46
    a0=math.radians(65 if side==1 else 115)
    b0=math.radians(80 if side==1 else 100)
    a,b=a0,b0
    if weight>0:
        joint=arm_joint(shoulder,target,upper,lower,bend=-1)
        a1=math.atan2(joint[1]-shoulder[1],joint[0]-shoulder[0])
        b1=math.atan2(target[1]-joint[1],target[0]-joint[0])
        a=a0+((a1-a0+math.pi)%(2*math.pi)-math.pi)*weight
        b=b0+((b1-b0+math.pi)%(2*math.pi)-math.pi)*weight
    elbow=(shoulder[0]+upper*math.cos(a),shoulder[1]+upper*math.sin(a))
    hand=(elbow[0]+lower*math.cos(b),elbow[1]+lower*math.sin(b))
    return elbow,hand

def stick_actor(d,x,lean=0,gaze=1,old=False,grip=None,phase=0,point=0,walk=0,contact_weight=1):
    ink='#345d59' if old else '#734f32'
    ground=425
    pelvis=(x,ground-66)
    chest=(x+lean,ground-120)
    head=(chest[0]+gaze*3,ground-158+abs(lean)*.12)
    d.ellipse((x-38,420,x+40,433),fill='#bdb8a5')
    stride=math.sin(walk)*14
    for side in (-1,1):
        foot=(x+side*20+side*stride,ground-max(0,side*math.sin(walk))*12)
        knee=(x+side*14+side*stride*.4,ground-31)
        line(d,[pelvis,knee,foot],ink,8)
        line(d,[foot,(foot[0]+10,foot[1])],ink,6)
    line(d,[pelvis,(x+lean*.6,ground-91),chest],ink,9)
    neck=(chest[0],chest[1]-17)
    line(d,[chest,neck],ink,7)
    hx,hy=head
    d.ellipse((hx-20,hy-22,hx+20,hy+20),fill='#f8f1e3',outline=ink,width=4)
    # Original small facial cues; body language carries the performance.
    ex=hx+gaze*8
    d.ellipse((ex-1.6,hy-4,ex+1.6,hy-.8),fill=ink)
    line(d,[(ex-4,hy+8),(ex+3,hy+8+phase*2)],ink,2)
    if old:
        line(d,[(hx-13,hy-7),(hx+12,hy-7)],ink,2)
        d.polygon([(hx-11,hy+15),(hx+12,hy+15),(hx+2,hy+33)],fill='#b7bbaa')
    for side in (-1,1):
        shoulder=(chest[0]+side*8,chest[1]+3)
        if grip is not None:
            target=(grip[0],grip[1]+(15 if side==-1 else 0))
            elbow,hand=stick_arm(shoulder,target,contact_weight,side)
        elif old and side==-1 and point:
            hand=(shoulder[0]-65*point,shoulder[1]-14*point+34*(1-point))
            elbow=((shoulder[0]+hand[0])/2,shoulder[1]+17)
        else:
            hand=(shoulder[0]+side*(22+phase*13),shoulder[1]+52-phase*17)
            elbow=(shoulder[0]+side*18,shoulder[1]+28)
        line(d,[shoulder,elbow,hand],ink,7)
        d.ellipse((hand[0]-4,hand[1]-4,hand[0]+4,hand[1]+4),fill='#f8f1e3',outline=ink,width=2)

def grip_weight(t):
    return ease(t,2.2,3.25)*(1-ease(t,7.2,8.0))

def stick_frame(t):
    im=STICK_BG.copy(); d=ImageDraw.Draw(im)
    approach=ease(t,0,1.8)
    x=lerp(400,545,approach)
    effort=ease(t,4.1,4.8)*(1-ease(t,6.7,7.3))
    recoil=ease(t,8.0,8.6)
    x-=recoil*28
    lean=lerp(7,-12,effort)-6*recoil
    contact=3.25<=t<7.2
    grip=(612,310)
    gaze=-1 if t>8.6 else 1
    if 1.8<=t<3.1:
        # A preparatory hand lift precedes contact, rather than teleporting the entire action.
        phase=ease(t,1.8,3.1)
    else:
        phase=effort if contact else recoil*.6
    stick_actor(d,x,lean,gaze,grip=grip,phase=phase,walk=t*9 if t<1.8 else 0,contact_weight=grip_weight(t))
    arrival=ease(t,7.1,8.6)
    if arrival>0:
        stick_actor(d,lerp(-50,363,arrival),lean=2,gaze=-1,old=True,point=ease(t,8.8,10.4),walk=t*7 if arrival<1 else 0)
    if t<4.1: title='A familiar route. A real obstacle.'
    elif t<8.6: title='More effort does not open every gate.'
    else: title='First notice what else is there.'
    d.text((480,475),title,font=FONT,anchor='mm',fill='#344c4c')
    d.text((480,511),'STICK PERFORMANCE TEST / ORIGINAL FOLEY / NO NARRATION',font=SMALL,anchor='mm',fill='#77847a')
    return Image.blend(im,TEXTURE,.025)

def write_foley(path,duration):
    """Small original contact cues; not synthesized speech or a final mastered mix."""
    rate=24000; rnd=random.Random(44)
    events=[(.25,'step'),(.68,'step'),(1.1,'step'),(1.53,'step'),(3.25,'metal'),(4.6,'metal'),(5.55,'metal'),(7.4,'step'),(7.8,'step'),(8.2,'step')]
    samples=[]
    for i in range(int(duration*rate)):
        t=i/rate; sample=0
        for at,kind in events:
            q=t-at
            if not 0<=q<.55: continue
            if kind=='step': sample+=.12*math.exp(-q*34)*(math.sin(2*math.pi*95*q)+rnd.uniform(-.4,.4))
            else: sample+=.065*math.exp(-q*10)*(math.sin(2*math.pi*690*q)+.4*math.sin(2*math.pi*1137*q))
        samples.append(struct.pack('<h',int(max(-.8,min(.8,sample))*32767)))
    with wave.open(str(path),'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(b''.join(samples))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,required=True); ap.add_argument('--cut',type=int,choices=[1,2,3],required=True)
    ap.add_argument('--style',choices=['blocking','stick'],default='blocking')
    args=ap.parse_args()
    if args.out.exists(): raise SystemExit('Use a fresh output path; prior cuts are retained')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    ffmpeg=shutil.which('ffmpeg')
    if not ffmpeg: raise SystemExit('FFmpeg is required')
    duration=12 if args.style=='stick' else DURATION
    draw=stick_frame if args.style=='stick' else lambda t:frame(t,args.cut)
    cmd=[ffmpeg,'-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-vf','scale=1280:720:flags=lanczos:out_color_matrix=bt709:out_range=tv','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv','-movflags','+faststart',str(args.out)]
    if args.style=='stick':
        audio=args.out.with_suffix('.wav');write_foley(audio,duration)
        cmd[cmd.index('-an'):cmd.index('-an')+1]=['-i',str(audio),'-c:a','aac','-b:a','128k','-shortest']
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(FPS*duration):
            p.stdin.write(draw(i/FPS).tobytes())
            if i%120==0: print(f'{i}/{FPS*duration}',flush=True)
        p.stdin.close()
        if p.wait(timeout=90): raise RuntimeError('FFmpeg encode failed')
    except BaseException:
        p.kill();p.wait();raise
    times=[.8,2.8,5.8,7.7,10.3,12.7,15.8,18.3,20.5,23]
    if args.style=='stick':times=[.2,1.5,2.5,3.3,4.5,5.7,7.2,8.1,9.5,11.5]
    sheet=Image.new('RGB',(W*2,H*5),'#172e35')
    for i,t in enumerate(times): sheet.paste(draw(t),(i%2*W,i//2*H))
    sheet.save(args.out.with_suffix('.jpg'))
    args.out.with_suffix('.json').write_text(json.dumps({'duration_s':duration,'fps':FPS,'cut':args.cut,'style':args.style,'audio':args.style=='stick','status':'unreviewed-motion-study','sha256':hashlib.sha256(args.out.read_bytes()).hexdigest(),'sample_times_s':times},indent=2),encoding='utf-8')
    print(args.out,flush=True)

if __name__=='__main__': main()

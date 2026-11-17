"""Original ink-and-paper acting revision. Reuses the approved recorded pilot.

No external artwork, models, extra voice generation, or time stretching.
The optional chamber treatment keeps identical audio for visual comparison.
"""
import argparse, json, math, random, subprocess, wave
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'studio-output/philosopher-ink'
W,H,FPS,DURATION=1920,1080,30,64.5
INK='#393b36'; PAPER='#f0e9db'; TEAL='#668c83'; RUST='#bb7860'
VOICE=ROOT.parent/'reference-media/approved-dialogue.wav'
SEGMENTS=[
 (2,5.503,'youth','You honestly believe the world is simple? Life too?'),
 (6.203,11.766,'host','Astonishingly simple. Yours, mine, every problem either of us has.'),
 (12.566,22.345,'youth',"Then I'll tell you why I climbed this hill. First, I'm going to argue with you until I'm satisfied. Then, if I can manage it, I'm going to make you take it all back."),
 (23.045,29.249,'host',"Annoy me? I've been hoping a young person would turn up and teach me something. Please, begin."),
 (30.049,37.409,'youth',"The romance dies and realism moves in. Then come the knotted relationships, the duties at work and at home."),
 (38.059,40.789,'youth',"It's a chaotic heap of contradictions!"),
 (42.589,46.434,'host',"It isn't complicated. You are making it complicated."),
 (47.534,48.140,'youth','I am?'),
 (48.840,56.013,'host',"We live in a subjective one, built from the meaning we give things. The world you see isn't the one I see."),
 (56.913,63.482,'host',"A different perspective won't make every obstacle disappear. But it may change the question you ask next.")]
# Boundaries are tied to actual recorded sentences and prop impacts, not an equal shot grid.
SHOTS=[(0,2,'arrival'),(2,6.203,'challenge'),(6.203,9,'host'),(9,12.566,'two'),
 (12.566,16.566,'slam'),(16.566,20,'youth'),(20,23.045,'hostlisten'),
 (23.045,26.5,'host'),(26.5,30.049,'two'),(30.049,33.1,'field'),
 (33.1,35.5,'work'),(35.5,38.059,'load'),(38.059,40.789,'knot'),
 (40.789,42.589,'cup'),(42.589,45,'host'),(45,47.534,'youthlisten'),
 (47.534,48.840,'reaction'),(48.840,52.3,'lens'),(52.3,56.913,'perspective'),
 (56.913,60.25,'barrier'),(60.25,64.5,'question')]

def ease(x):
    x=max(0,min(1,x));return x*x*(3-2*x)
def ramp(t,a,b):return ease((t-a)/(b-a))
def mix(a,b,k):return a+(b-a)*k
@lru_cache(None)
def font(size,bold=False):
    candidates=['C:/Windows/Fonts/'+('segoeuib.ttf' if bold else 'segoeui.ttf'),'/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf']
    for candidate in candidates:
        if Path(candidate).is_file():return ImageFont.truetype(candidate,size)
    raise RuntimeError('Install Segoe UI or DejaVu Sans for the captions.')
def line(d,points,fill=INK,width=4):
    d.line(points,fill=fill,width=max(1,int(width)),joint='curve')
    r=width/2
    for x,y in (points[0],points[-1]):d.ellipse((x-r,y-r,x+r,y+r),fill=fill)
def curve(d,points,fill=INK,width=4):
    a,b,c,e=points
    pts=[]
    for j in range(33):
        q=j/32;p=1-q
        pts.append((p**3*a[0]+3*p*p*q*b[0]+3*p*q*q*c[0]+q**3*e[0],p**3*a[1]+3*p*p*q*b[1]+3*p*q*q*c[1]+q**3*e[1]))
    line(d,pts,fill,width)
def smooth_shape(d,points,fill,stroke=INK,width=3):
    # Closed Catmull-Rom contour gives drawn faces and clothing a soft silhouette.
    contour=[]
    for i in range(len(points)):
        a,b,c,e=[points[j%len(points)] for j in (i-1,i,i+1,i+2)]
        for k in range(10):
            q=k/10
            contour.append(tuple(.5*((2*b[v])+(-a[v]+c[v])*q+(2*a[v]-5*b[v]+4*c[v]-e[v])*q*q+(-a[v]+3*b[v]-3*c[v]+e[v])*q*q*q) for v in (0,1)))
    d.polygon(contour,fill=fill);line(d,contour+[contour[0]],stroke,width)
def word(d,xy,text,size=36,fill=INK,anchor='mm',bold=False):d.text(xy,text,font=font(size,bold),fill=fill,anchor=anchor)

@lru_cache(None)
def background(kind):
    im=Image.new('RGB',(W,H),'#71877a' if kind=='study' else PAPER);d=ImageDraw.Draw(im)
    rng=random.Random(53)
    # Translucent pigment blooms are fixed in world space; they never flicker.
    wash=Image.new('RGBA',(W,H));w=ImageDraw.Draw(wash)
    palette=[(121,145,126,12),(177,147,103,10),(255,252,232,22)]
    for i in range(155):
        x=rng.randrange(-250,W);y=rng.randrange(-250,H);r=rng.randrange(80,330)
        w.ellipse((x-r,y-r,x+r,y+r),fill=palette[i%3])
    im=Image.alpha_composite(im.convert('RGBA'),wash.filter(ImageFilter.GaussianBlur(40))).convert('RGB');d=ImageDraw.Draw(im)
    if kind=='study':
        d.polygon([(0,726),(1920,695),(1920,1080),(0,1080)],fill='#b1a086')
        line(d,[(0,726),(1920,695)],'#7e816b',3)
        for x in range(-300,2400,250):line(d,[(960+(x-960)*.7,710),(x,1080)],'#a08f78',2)
        d.rounded_rectangle((1350,90,1770,590),radius=180,fill='#a5bcb3',outline='#8a9789',width=7)
        d.ellipse((1580,140,1650,210),fill='#e4c992')
        for x in range(1355,1765,60):
            hh=40+rng.randrange(90);d.rectangle((x,586-hh,x+48,586),fill='#829a91')
        line(d,[(1560,100),(1560,590)],'#9c9580',8);line(d,[(1350,350),(1770,350)],'#9c9580',7)
        d.rectangle((140,180,530,580),fill='#aca58f',outline='#746f5e',width=4)
        for yy in (295,430,560):
            for j in range(11):
                x=156+j*32;ht=rng.randrange(55,105)
                d.rectangle((x,yy-ht,x+23,yy),fill=['#798e83','#be9e78','#9b7564'][j%3],outline='#6f7669',width=2)
            line(d,[(140,yy+2),(530,yy+2)],'#706d5a',7)
        # A lit, ordinary study, rather than a dark presentation template.
        d.polygon([(1110,280),(1210,280),(1250,390),(1075,390)],fill='#ddc18d',outline='#8c8166')
        line(d,[(1160,390),(1160,605)],'#8a806a',8);d.ellipse((1110,590,1210,610),fill='#a49273')
    elif kind=='field':
        d.ellipse((-400,450,1600,1500),fill='#c0c7a0');d.ellipse((700,500,2500,1500),fill='#a4b49b')
        d.ellipse((1400,130,1510,240),fill='#dfc58e')
        for i in range(80):
            x=rng.randrange(W);y=rng.randrange(610,820)
            line(d,[(x,y),(x+5,y-15)],'#899d80',2)
    for i in range(13000):
        x=rng.randrange(W);y=rng.randrange(H);d.point((x,y),fill='#ded7c8' if i%2 else '#f9f3e5')
    return im

def hand(d,p,angle=0,s=1,open=True):
    def q(x,y):return(p[0]+s*(x*math.cos(angle)-y*math.sin(angle)),p[1]+s*(x*math.sin(angle)+y*math.cos(angle)))
    # Connected palm and separate fingers replace floating circular fists.
    points=[q(-8,3),q(-11,-6),q(-6,-15),q(0,-18),q(10,-12),q(12,2),q(7,9),q(-3,10)]
    d.polygon(points,fill='#f3e8d4');line(d,points+[points[0]],INK,2*s)
    if open:
        for j in range(3):line(d,[q(-4+j*5,-5),q(-6+j*6,-19-2*(j==1))],INK,2*s)
    line(d,[q(-7,0),q(-17,-5),q(-17,-10)],INK,2*s)

def actor(d,x,y,t,who='youth',s=1,mood='neutral',pose='rest',energy=0,mouth=0,lean=0,look=1,headtilt=0):
    old=who=='host';shirt=RUST if old else TEAL
    breath=1.2*math.sin(t*2.1);a=math.radians(lean)
    def p(xx,yy):return (x+s*(xx*math.cos(a)-yy*math.sin(a)),y+s*(xx*math.sin(a)+yy*math.cos(a)+breath))
    def ln(pts,c=INK,w=4):line(d,[p(*v) for v in pts],c,w*s)
    # One continuous silhouette: shoes, knees, hip, spine and attentive shoulders.
    for sign in (-1,1):
        bend=energy*sign*12 if pose=='walk' else 0
        leg=[(sign*27,-94),(sign*37+bend,10),(sign*42-bend,115)]
        ln(leg,INK,19);ln(leg,'#747c70' if old else '#6c7a73',12)
        ln([(sign*42-bend,115),(sign*42-bend+25,119)],INK,10)
    torso=[(-49,-250),(-28,-263),(28,-263),(50,-250),(39,-95),(-35,-95)]
    smooth_shape(d,[p(*v) for v in torso],shirt,width=4*s)
    ln([(-32,-211),(-27,-153),(-33,-126)],'#a66f5b' if old else '#78978c',2)
    ln([(0,-260),(0,-105)],'#9c6957' if old else '#4e7068',3)
    for yy in (-205,-166,-128):
        px,py=p(9,yy);d.ellipse((px-2*s,py-2*s,px+2*s,py+2*s),fill=INK)
    ln([(-20,-276),(-20,-259),(0,-240),(20,-259),(20,-276)],'#eee3d1',13)
    ln([(-20,-259),(0,-240),(20,-259)],INK,3)
    l=(-77,-108);r=(79,-110)
    if pose=='question':l=(-90-60*energy,-190-65*energy);r=(90+60*energy,-180-55*energy)
    if pose=='point':r=(120+25*energy,-260-10*energy)
    if pose=='head':l=(-65,-345);r=(105,-156)
    if pose=='offer':l=(-85-80*energy,-160-110*energy);r=(85,-117)
    if pose=='slam':l=(-100,-200+140*energy);r=(115,-200+140*energy)
    if pose=='knot':l=(-105,-210-35*energy);r=(105,-210-35*energy)
    if pose=='chest':r=(12,-231);l=(-80,-120)
    if pose=='walk':l=(-75,-110+30*energy);r=(75,-110-30*energy)
    for sign,target in [(-1,l),(1,r)]:
        sh=(sign*47,-244);el=(sign*(74+abs(target[0])*.15),mix(-181,target[1],.25))
        ln([sh,el,target],INK,18);ln([sh,el,target],shirt,12)
        hand(d,p(*target),angle=sign*.4+a,s=s,open=pose!='slam')
    # Head has its own acting pivot, separate from the spine.
    ha=math.radians(headtilt);hx,hy=p(0,-337)
    def hp(xx,yy):return(hx+s*(xx*math.cos(ha)-yy*math.sin(ha)),hy+s*(xx*math.sin(ha)+yy*math.cos(ha)))
    def hline(pts,c=INK,w=3):line(d,[hp(*v) for v in pts],c,w*s)
    # Outline is slightly asymmetrical, an original drawn shape instead of a perfect emoji circle.
    face=[(-56,-25),(-48,-61),(-20,-78),(15,-78),(48,-60),(60,-23),(54,23),(31,54),(-7,61),(-42,40),(-58,9)]
    smooth_shape(d,[hp(*v) for v in face],'#f4eddd',width=3.5*s)
    if old:
        hair=[(-58,-14),(-66,-39),(-49,-63),(-29,-82),(4,-88),(36,-78),(58,-55),(62,-18),(46,-43),(19,-52),(-14,-55),(-42,-42)]
        d.polygon([hp(*v) for v in hair],fill='#d0cec0');hline(hair,INK,3)
        beard=[(-49,15),(-35,31),(-14,30),(2,37),(22,29),(46,15),(39,50),(10,81),(-13,75),(-40,50)]
        smooth_shape(d,[hp(*v) for v in beard],'#dfddce',width=2*s)
        for j in (-22,-7,12,28):hline([(j,46),(j-3,61)],'#aaa99d',1.5)
    else:
        hair=[(-58,-7),(-69,-43),(-48,-71),(-58,-80),(-23,-79),(-12,-95),(8,-84),(36,-82),(59,-57),(63,-14),(48,-40),(27,-43),(9,-55),(-14,-34),(-43,-34)]
        d.polygon([hp(*v) for v in hair],fill='#494d45');hline(hair,INK,2)
    blink=(t+(1.7 if old else .2))%4.3<.11
    for sign in (-1,1):
        ex=sign*23;ey=-7
        if blink:hline([(ex-10,ey),(ex+10,ey)],INK,3)
        else:
            xx,yy=hp(ex,ey);d.ellipse((xx-10*s,yy-12*s,xx+10*s,yy+11*s),fill='#fffaf0',outline=INK,width=max(1,round(2*s)))
            xx,yy=hp(ex+look*4,ey+(4 if mood=='worried' else 0));d.ellipse((xx-3*s,yy-6*s,xx+3*s,yy+6*s),fill=INK)
        if old:
            xx,yy=hp(ex,ey);d.ellipse((xx-17*s,yy-18*s,xx+17*s,yy+17*s),outline=INK,width=max(1,round(2*s)))
        b=-31-(10 if mood=='shock' else 0)
        slope=sign*9 if mood=='angry' else (-sign*9 if mood=='worried' else sign*1)
        hline([(ex-12,b-slope),(ex+12,b+slope)],INK,3)
    if old:hline([(-6,-9),(6,-9)],INK,2)
    hline([(4,-1),(10,14),(1,17)],'#a49a85',2)
    if mouth>.08:
        xx,yy=hp(0,34);d.ellipse((xx-11*s,yy-2*s,xx+11*s,yy+(4+15*mouth)*s),fill='#6e4e43',outline=INK,width=max(1,round(s)))
        if mouth>.5:hline([(-7,35),(7,35)],'#f6ead5',2)
    elif mood=='shock':
        xx,yy=hp(0,37);d.ellipse((xx-6*s,yy-5*s,xx+6*s,yy+7*s),outline=INK,width=max(1,round(2*s)))
    else:hline([(-11,37),(0,33 if mood in ('angry','worried') else 40),(11,37)],INK,2.5)

def desk(d):
    d.polygon([(330,647),(1570,647),(1670,735),(245,735)],fill='#b89d79',outline=INK)
    line(d,[(245,735),(1670,735)],'#726c57',9)
    for x in (330,1550):line(d,[(x,735),(x-12,870)],'#726c57',15)
    d.polygon([(970,664),(1110,664),(1140,712),(986,712)],fill='#f5ebd5',outline='#918c76')
    for yy in (678,691):line(d,[(999,yy),(1090,yy)],'#b8b09b',2)
def cup(d,x,y,t,scale=1):
    d.ellipse((x-55*scale,y-10*scale,x+55*scale,y+10*scale),fill='#c2b398',outline='#8e8b76',width=2)
    d.rounded_rectangle((x-30*scale,y-64*scale,x+30*scale,y-5*scale),radius=8*scale,fill='#eee6cd',outline=INK,width=max(1,int(3*scale)))
    d.ellipse((x+19*scale,y-51*scale,x+57*scale,y-16*scale),outline=INK,width=max(1,int(4*scale)))
    d.ellipse((x-29*scale,y-70*scale,x+29*scale,y-53*scale),fill='#9c8667',outline=INK,width=2)
    for j in range(2):curve(d,[(x+j*18*scale,y-80*scale),(x-14*scale,y-100*scale),(x+13*scale,y-120*scale),(x-4*scale,y-135*scale)],'#bdb6a2',2)

def prop_card(d,x,y,kind,s=1):
    if kind=='work':
        d.rounded_rectangle((x-90*s,y-65*s,x+90*s,y+65*s),radius=10*s,fill='#baa487',outline=INK,width=3)
        d.arc((x-28*s,y-90*s,x+28*s,y-40*s),180,360,fill=INK,width=5)
        line(d,[(x-90*s,y-9*s),(x+90*s,y-9*s)],INK,3)
    elif kind=='home':
        d.polygon([(x-90*s,y-10*s),(x,y-100*s),(x+90*s,y-10*s)],fill='#bb8a73',outline=INK)
        d.rectangle((x-65*s,y-10*s,x+65*s,y+80*s),fill='#d8c8a8',outline=INK,width=3)
        d.rectangle((x-13*s,y+18*s,x+20*s,y+80*s),fill='#83998a',outline=INK,width=2)
    else:
        for dx in (-35,35):
            d.ellipse((x+dx-20*s,y-50*s,x+dx+20*s,y-10*s),fill='#eee5d0',outline=INK,width=3)
            curve(d,[(x+dx-30*s,y+40*s),(x+dx-28*s,y-8*s),(x+dx+28*s,y-8*s),(x+dx+30*s,y+40*s)],INK,4)

def knot(d,cx,cy,t,size=170,release=0):
    pts=[]
    for j in range(140):
        a=j/139*math.pi*8
        pts.append((cx+(1-release)*(math.sin(a*1.73+t*.3)*size*(.45+.25*math.sin(a*.3)))+release*(j/139-.5)*size*3,
                    cy+(1-release)*math.cos(a*1.13)*size*(.28+.16*math.cos(a*.41))))
    line(d,pts,'#ae735e',5)

def voice_data():
    with wave.open(str(VOICE),'rb') as f:
        import array
        assert f.getsampwidth()==2 and f.getnchannels()==1
        if abs(f.getnframes()/f.getframerate()-DURATION)>.1:
            raise ValueError('This edit requires the approved 64.5-second pilot master.')
        data=array.array('h',f.readframes(f.getnframes()));sr=f.getframerate()
    rms=[]
    for n in range(math.ceil(DURATION*FPS)):
        a=data[int(n/FPS*sr):int((n+1)/FPS*sr)]
        rms.append(min(1,math.sqrt(sum(v*v for v in a)/max(1,len(a)))/4200))
    return rms
RMS=[]
def speaking(t,who):return next((RMS[min(len(RMS)-1,int(t*FPS))] for a,b,w,_ in SEGMENTS if a<=t<b and w==who),0) if RMS else 0

def frame(t,treatment='story',captions=True):
    start,end,scene=next((row for row in SHOTS if row[0]<=t<row[1]),SHOTS[-1]);u=t-start
    if treatment=='chamber' and 30.049<=t<40.789:scene='youth'
    bg='field' if scene in ('arrival','field') else 'study' if scene not in ('work','load','knot','lens','perspective','barrier','question') else 'paper'
    im=background(bg).copy();d=ImageDraw.Draw(im)
    ym=speaking(t,'youth');hm=speaking(t,'host');beat=math.sin(t*2.8)*.5+.5
    if scene=='arrival':
        # Youth actively climbs toward the lit study; no title-card preamble.
        d.polygon([(1300,470),(1540,470),(1540,700),(1300,700)],fill='#b1a087',outline=INK)
        d.polygon([(1270,470),(1420,360),(1570,470)],fill='#8c8872',outline=INK)
        d.rectangle((1390,530,1450,700),fill='#d9b77a',outline=INK,width=4)
        x=690+150*ramp(u,0,2);actor(d,x,680,t,s=.7,pose='walk',energy=math.sin(t*9),lean=8,look=1)
    elif scene in ('two','slam'):
        k=ramp(u,.15,.65)*(1-ramp(u,1.6,2.8))
        actor(d,610,708,t,s=1.1,mood='angry',pose='slam' if scene=='slam' else 'question',energy=k if scene=='slam' else beat*.3,mouth=ym,look=1,headtilt=4)
        actor(d,1345,706,t,'host',s=1.08,pose='offer' if hm else 'rest',energy=beat*.5,mouth=hm,look=-1,headtilt=-3)
        desk(d);cup(d,1310,685,t)
        if scene=='slam' and .63<u<1.05:
            k=1-(u-.63)/.42
            for x in (500,730):line(d,[(x,625),(x-18,609)],'#a7735a',max(1,4*k))
    elif scene in ('challenge','youth','youthlisten','reaction'):
        mood='shock' if scene=='reaction' else 'worried' if scene=='youthlisten' else 'angry'
        action='chest' if scene=='reaction' else 'question' if scene!='youthlisten' else 'rest'
        # A listening reaction changes eyes, spine and hands; it is not just another zoom.
        hit=ramp(u,.08,.38);settle=ramp(u,.65,1.15)
        lean=(-8*hit+5*settle if scene in ('reaction','youthlisten') else 10*hit-7*settle)
        actor(d,860,1000,t,s=2.0,mood=mood,pose=action,energy=hit*(1-ramp(u,1.7,2.2)),mouth=ym,lean=lean,look=1,headtilt=mix(3,-6,ramp(u,.2,.65)))
    elif scene in ('host','hostlisten'):
        offer=ramp(u,.12,.48)*(1-ramp(u,1.7,2.2))
        lean=(-7*ramp(u,.12,.45)+5*ramp(u,.7,1.2)) if scene=='host' else 6*ramp(u,.15,.5)-4*ramp(u,.8,1.3)
        actor(d,1060,1000,t,'host',s=2,pose='offer' if scene=='host' else 'rest',energy=offer,mouth=hm,lean=lean,look=-1,headtilt=-5+4*ramp(u,.4,.8))
    elif scene=='field':
        k=ramp(u,.3,2.5)
        actor(d,880,650,t,s=1.06,pose='question',energy=1-k,mood='worried' if k>.5 else 'neutral',mouth=ym,headtilt=-6*k)
        # Warm recollection drains into the concrete obligations shown next.
        for j in range(7):line(d,[(170+j*230,730),(210+j*230,730)],'#97a18d',3)
    elif scene in ('work','load'):
        actor(d,960,650,t,s=1.18,pose='head' if scene=='load' else 'question',energy=beat,mood='worried',mouth=ym,lean=5)
        props=[(380,330,'work'),(1530,330,'home'),(440,650,'people')]
        for j,(x,y,kind) in enumerate(props):
            amount=ramp(u,j*.2,j*.2+.7)
            if scene=='work' and j>0:continue
            prop_card(d,x,y,kind,s=.85)
            curve(d,[(x+70,y+35),(x+230,y+100),(750,530),(880,495)],'#b87b65',4*amount+.1)
        if scene=='load':knot(d,960,530,t,90)
    elif scene=='knot':
        actor(d,690,910,t,s=1.8,pose='knot',energy=ramp(u,.1,.8),mood='angry',mouth=ym,headtilt=-6)
        knot(d,1370,400,t,260)
        curve(d,[(900,480),(1020,300),(1130,550),(1200,430)],'#ae735e',5)
    elif scene=='cup':
        # The wrist follows the handle until release. The cup ends exactly on the table.
        k=ramp(u,0,.822);cy=mix(425,650,k);cx=mix(1020,1130,k);withdraw=ramp(u,.88,1.65)
        d.polygon([(0,650),(1920,650),(1920,1080),(0,1080)],fill='#c0aa87')
        line(d,[(0,650),(1920,650)],'#8c8068',5)
        wrist=(cx+78+100*withdraw,cy-35-130*withdraw)
        sleeve=[(1900,250),(1620,385),(1420,520),(wrist[0]+65,wrist[1]-35)]
        curve(d,sleeve,INK,56);curve(d,sleeve,RUST,48)
        line(d,[(wrist[0]+65,wrist[1]-35),wrist],INK,28)
        line(d,[(wrist[0]+65,wrist[1]-35),wrist],'#f3e8d4',21)
        cup(d,cx,cy,t,2)
        hand(d,(cx+78+100*withdraw,cy-35-130*withdraw),angle=.7,s=2,open=withdraw>.2)
        if .822<u<1.2:
            for dx in (-125,125):line(d,[(cx+dx,cy-5),(cx+dx*1.2,cy-26)],'#8e917a',4)
    elif scene in ('lens','perspective'):
        # The SAME doorstep stays in both views. Interpretation changes, geometry does not.
        for offset in (0,960):
            d.rectangle((offset+270,210,offset+670,720),fill='#c3b394',outline=INK,width=4)
            d.rectangle((offset+303,240,offset+637,720),fill='#92a79a',outline=INK,width=4)
            for j in range(2):d.polygon([(offset+245-j*35,720+j*36),(offset+700+j*35,720+j*36),(offset+720+j*35,755+j*36),(offset+225-j*35,755+j*36)],fill='#d3c3a5',outline=INK)
            d.ellipse((offset+575,466,offset+593,484),fill='#b0875d',outline=INK)
        line(d,[(960,130),(960,805)],'#c0b39c',3)
        if scene=='lens':
            k=ramp(u,.2,2.3)
            # A moving lens selects a reading of one fixed thing, rather than deleting obstacles.
            overlay=Image.new('RGBA',(W,H));od=ImageDraw.Draw(overlay)
            od.ellipse((210+70*k,180,730+70*k,700),fill=(96,120,139,50),outline='#6e817c',width=7)
            od.ellipse((1170-70*k,180,1690-70*k,700),fill=(213,167,86,35),outline='#9f947b',width=7)
            im=Image.alpha_composite(im.convert('RGBA'),overlay).convert('RGB');d=ImageDraw.Draw(im)
        else:
            actor(d,170,688,t,s=.78,pose='head',mood='worried',look=1)
            actor(d,1130,688,t,'host',s=.78,pose='point',energy=ramp(u,.2,1.3),look=1,mouth=hm)
    elif scene in ('barrier','question'):
        # A real closed gate remains. Only the person's next action changes.
        d.rectangle((1020,210,1560,735),fill='#ccd1bb',outline='#828c78',width=5)
        for xx in range(1060,1550,65):line(d,[(xx,220),(xx,725)],'#838c78',8)
        line(d,[(1020,400),(1560,400)],'#838c78',10)
        line(d,[(1020,660),(1560,660)],'#838c78',10)
        d.rounded_rectangle((1180,410,1250,462),radius=7,fill='#b8a17c',outline=INK,width=4)
        actor(d,800,655,t,s=1.12,pose='head' if scene=='barrier' else 'point',energy=ramp(u,.25,1.7),mood='worried' if scene=='barrier' else 'neutral',headtilt=-4,look=1)
        if scene=='question':
            # Circle the latch, the newly considered question, not a magical open gate.
            if u>.7:d.arc((1140,365,1290,510),-70,-70+int(350*ramp(u,.7,1.6)),fill='#a66e53',width=5)
    if captions:caption(d,t)
    return im

def caption(d,t):
    for a,b,who,text in SEGMENTS:
        if a<=t<b:
            words=text.split();groups=[];g=[]
            for w in words:
                if len(' '.join(g+[w]))>47 and g:groups.append(g);g=[]
                g.append(w)
            if g:groups.append(g)
            weights=[sum(len(w)+1 for w in v) for v in groups];target=(t-a)/(b-a)*sum(weights);idx=0
            for j,w in enumerate(weights):
                if target<w:idx=j;break
                target-=w
            label=' '.join(groups[idx]);f=font(43,True);width=d.textlength(label,font=f)
            d.rounded_rectangle(((W-width)/2-26,824,(W+width)/2+26,900),radius=12,fill='#f8f1e1',outline='#c5bca7',width=2)
            word(d,(960,859),label,43,bold=True)
            break

def self_check():
    assert SHOTS[0][0]==0 and SHOTS[-1][1]==DURATION
    assert all(a[1]==b[0] for a,b in zip(SHOTS,SHOTS[1:]))
    assert all(a<b and len(text)>0 for a,b,_,text in SEGMENTS)
    assert frame(39).tobytes()==frame(39).tobytes(), 'render must scrub deterministically'
    assert frame(39).tobytes()!=frame(39.5).tobytes(), 'acting cannot be a frozen pose'
    assert frame(39,'story').tobytes()!=frame(39,'chamber').tobytes()
    print('Timing, deterministic scrub, motion and treatment checks passed.',flush=True)

def render(name,start=0,end=DURATION,treatment='story'):
    OUT.mkdir(parents=True,exist_ok=True);picture=OUT/(name+'-picture.mp4')
    cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-threads','4','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',str(picture)]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as p:
        try:
            count=round((end-start)*FPS)
            for i in range(count):
                p.stdin.write(frame(start+i/FPS,treatment).tobytes())
                if i%300==0:print(f'{name}: {i}/{count}',flush=True)
            p.stdin.close()
            if p.wait():raise RuntimeError('Picture encode failed')
        except BaseException:p.kill();raise
    output=OUT/(name+'.mp4')
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(picture),'-ss',str(start),'-i',str(VOICE),'-t',str(count/FPS),'-map','0:v:0','-map','1:a:0','-c:v','copy','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-c:a','aac','-b:a','192k','-movflags','+faststart',str(output)],check=True)
    return output

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--render',action='store_true');ap.add_argument('--comparison',action='store_true');ap.add_argument('--audio',type=Path);ap.add_argument('--out',type=Path);a=ap.parse_args()
    if a.audio:VOICE=a.audio.resolve()
    if a.out:OUT=a.out.resolve()
    if not VOICE.is_file():ap.error('Provide the approved pilot master with --audio (48 kHz, mono, 16-bit PCM WAV).')
    OUT.mkdir(parents=True,exist_ok=True);RMS=voice_data();self_check()
    sample=[3,7.5,14,18,25,31.5,34.5,36.5,39.5,41.8,44,47.9,50,54,58,62]
    sheet=Image.new('RGB',(1600,900),PAPER)
    for j,t in enumerate(sample):
        im=frame(t);sheet.paste(im.resize((400,225),Image.Resampling.LANCZOS),((j%4)*400,(j//4)*225))
    sheet.save(OUT/'storyboard.jpg',quality=94)
    frame(39.5).save(OUT/'acting-preview.png')
    (OUT/'shot-plan.json').write_text(json.dumps(SHOTS,indent=2),encoding='utf-8')
    if a.render:print(render('Philosopher-Ink-Acting-Pilot'),flush=True)
    if a.comparison:print(render('Philosopher-Chamber-Treatment',30.049,56.915,'chamber'),flush=True)


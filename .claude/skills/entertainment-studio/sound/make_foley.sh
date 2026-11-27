#!/bin/bash
# Half Landing temporary foley, synthesised with ffmpeg (original, no licence needed). Copy into an episode's sound/ and run;
# ep_build.py uses an episode's sound/ before the shared CC0 bank.
# PHONE RULE: most viewers hear Reels on a phone speaker, which reproduces little below ~150 Hz. Every sound keeps real energy
# above 150 Hz (harmonics, a knock, a click); ep_review.py flags any cue sound that is mostly below it.
set -e; cd "$(dirname "$0")"; S="-ar 48000 -ac 1"
g(){ ffmpeg -v error -y -f lavfi -i "aevalsrc='$2':s=48000:d=$3" -af "$4" $S "$1.wav"; }
# the sound check's kick through the wall: a body with harmonics, a mid knock (the wall) and a click
g boom "(0.5*sin(2*PI*(55+60*exp(-25*t))*t)+0.45*sin(2*PI*(110+90*exp(-25*t))*t)+0.3*sin(2*PI*170*t))*exp(-7*t)+0.35*(random(0)*2-1)*exp(-45*t)" 0.5 "lowpass=f=1800,equalizer=f=400:t=q:w=1:g=6"
# a band's bass note: a fast pluck with strong harmonics, gently muffled
g bass "(0.45*sin(2*PI*55*t)+0.5*sin(2*PI*110*t)+0.42*sin(2*PI*165*t)+0.3*sin(2*PI*220*t)+0.18*sin(2*PI*330*t))*(1-exp(-400*t))*exp(-5.5*t)+0.25*(random(7)*2-1)*exp(-90*t)" 0.55 "lowpass=f=1400"
# the pot rattling: short metallic pings
g rattle "0.30*sin(2*PI*2400*t)*exp(-35*t)+0.26*gt(t,0.06)*sin(2*PI*3150*t)*exp(-45*(t-0.06))+0.22*gt(t,0.13)*sin(2*PI*2750*t)*exp(-50*(t-0.13))+0.16*gt(t,0.21)*sin(2*PI*3500*t)*exp(-60*(t-0.21))+0.05*(random(1)*2-1)*exp(-25*t)" 0.42 "highpass=f=900"
# sticky caramel stretching
g squelch "0.55*sin(2*PI*(210+420*t)*t+3*sin(2*PI*17*t))*exp(-3.5*t)*(1-exp(-35*t))" 0.5 "bandpass=f=650:width_type=h:w=700"
# a wet splat: a mid-range burst over a small thud
g splat "0.6*(random(2)*2-1)*exp(-24*t)+0.3*sin(2*PI*180*t)*exp(-22*t)" 0.28 "bandpass=f=1200:width_type=h:w=2400"
# fabric and caramel under tension
g creak "0.30*(sin(2*PI*(150+95*t)*t)+0.5*sin(4*PI*(150+95*t)*t)+0.33*sin(6*PI*(150+95*t)*t))*(1-exp(-12*t))*exp(-1.6*t)*(1+0.3*sin(2*PI*23*t))" 0.55 "bandpass=f=850:width_type=h:w=900"
# an elastic snap back
g snap "0.75*sin(2*PI*(950-760*t)*t)*exp(-24*t)+0.2*(random(3)*2-1)*exp(-90*t)" 0.24 "highpass=f=120"
# a jelly boing, a soft plop
g boing "0.6*sin(2*PI*(260+90*sin(2*PI*9*t)*exp(-4*t))*t)*exp(-4.5*t)" 0.6 "lowpass=f=1600"
g plop "0.5*sin(2*PI*(180-120*t)*t)*exp(-18*t)+0.25*(random(4)*2-1)*exp(-40*t)" 0.25 "lowpass=f=1500"
# a toaster beep, a crunch, a toaster spring
g beep "0.5*sin(2*PI*2200*t)*gt(mod(t,0.24),0)*lt(mod(t,0.24),0.09)" 0.5 "highpass=f=600"
g crunch "0.6*(random(5)*2-1)*(exp(-22*t)+0.6*gt(t,0.07)*exp(-25*(t-0.07))+0.4*gt(t,0.15)*exp(-30*(t-0.15)))" 0.3 "bandpass=f=2500:width_type=h:w=3000"
g spring "0.6*sin(2*PI*(420+260*sin(2*PI*22*t))*t)*exp(-9*t)+0.3*(random(6)*2-1)*exp(-70*t)" 0.35 "highpass=f=200"
# a phone vibrating on a hard counter: pulsed 170 Hz with harmonics (phone-audible), plus the rattle of the surface
g buzz "(0.5*sin(2*PI*170*t)+0.35*sin(2*PI*340*t)+0.2*sin(2*PI*510*t)+0.08*(random(8)*2-1))*gt(mod(t,0.3),0)*lt(mod(t,0.3),0.19)" 0.6 "lowpass=f=2400"
# peak-normalise every sound to -3 dB so the cue gains in workspace.json are the only level control
for f in boom bass rattle squelch splat creak snap boing plop beep crunch spring buzz; do
  mx=$(ffmpeg -nostats -i "$f.wav" -af volumedetect -f null - 2>&1 | sed -n 's/.*max_volume: \([-0-9.]*\) dB/\1/p')
  ffmpeg -v error -y -i "$f.wav" -af "volume=$(python3 -c "print(-3-($mx))")dB" $S "$f.tmp.wav" && mv "$f.tmp.wav" "$f.wav"
done

#!/usr/bin/env python3
"""Synthesize original sound effects for the stick exercise from its SOUND_EVENTS.

Everything is generated here from noise and sine partials (no samples, no
third-party audio), so the result is fully owned. Deterministic: fixed seed.

Usage: python3 stick-sfx.py events.json out.wav [--duration 14.5]
"""
import argparse, json, wave
import numpy as np

SR = 48000


def env(n, attack, decay):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(attack, 1e-4)) * np.exp(-t / decay)


def noise(rng, n, lowpass=None):
    x = rng.standard_normal(n)
    if lowpass:  # one-pole low-pass, 0..1 (smaller = darker)
        y = np.empty(n); acc = 0.0
        for i in range(n):
            acc += lowpass * (x[i] - acc); y[i] = acc
        x = y / (np.abs(y).max() + 1e-9)
    return x


def tone(freqs, n, decays):
    t = np.arange(n) / SR
    return sum(np.sin(2 * np.pi * f * t) * np.exp(-t / d) for f, d in zip(freqs, decays))


def make(kind, rng, dur=None):
    if kind == 'step':
        n = int(.14 * SR); return .8 * noise(rng, n, .05) * env(n, .006, .035) + .6 * tone([90], n, [.05]) * env(n, .004, .06)
    if kind == 'clank':  # inharmonic metal partials
        n = int(.6 * SR); return .6 * tone([523, 1311, 2087, 2950], n, [.25, .18, .1, .06]) * env(n, .001, .5) + .3 * noise(rng, n, .5) * env(n, .001, .01)
    if kind == 'rattle':
        n = int((dur or 2) * SR); out = np.zeros(n); i = 0
        while i < n:
            m = int(.07 * SR); hit = .35 * tone([780 + rng.uniform(-60, 60), 1900], m, [.03, .02]) * env(m, .001, .03)
            out[i:i + m] += hit[:n - i]; i += int(rng.uniform(.045, .09) * SR)
        return out * np.sin(np.pi * np.arange(n) / n) ** .5
    if kind == 'twang':  # snapping grip on the springing gate
        n = int(.9 * SR); t = np.arange(n) / SR; f = 210 * (1 + .25 * np.exp(-t / .05))
        return .8 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / .35) * (1 + .3 * np.sin(2 * np.pi * 9 * t)) + .4 * tone([1311], n, [.08])
    if kind == 'whoosh':
        n = int((dur or .4) * SR); x = noise(rng, n, .25); s = np.sin(np.pi * np.arange(n) / n) ** 2
        return .7 * x * s
    if kind == 'thud':
        n = int(.45 * SR); t = np.arange(n) / SR; f = 70 * (1 + 1.2 * np.exp(-t / .03))
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .002, .07) + .5 * noise(rng, n, .05) * env(n, .001, .04)
    if kind == 'slam':
        n = int(.3 * SR); return .9 * tone([110, 180], n, [.08, .05]) * env(n, .001, .1) + .6 * noise(rng, n, .15) * env(n, .001, .04)
    if kind == 'pluck':  # noticing beat
        n = int(.5 * SR); return .5 * tone([880, 1320], n, [.18, .1]) * env(n, .002, .3)
    if kind == 'chime':  # relief
        n = int(1.6 * SR); return .45 * tone([659, 988, 1319], n, [.9, .6, .4]) * env(n, .01, 1.2)
    raise ValueError(f'unknown sound type {kind!r}')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('events'); ap.add_argument('out'); ap.add_argument('--duration', type=float, default=14.5)
    a = ap.parse_args()
    events = json.load(open(a.events))
    rng = np.random.default_rng(20261119)
    mix = np.zeros(int(a.duration * SR) + SR)
    for e in events:
        clip = make(e['type'], rng, e.get('dur')) * float(e.get('gain', 1))
        i = int(round(float(e['t']) * SR)); mix[i:i + len(clip)] += clip[:len(mix) - i]
    mix = mix[:int(a.duration * SR)]
    mix *= .89 / (np.abs(mix).max() + 1e-9)  # peak headroom; loudness is normalised in the mux step
    with wave.open(a.out, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype('<i2').tobytes())
    print(f'{a.out}: {len(events)} events, {a.duration}s')


if __name__ == '__main__':
    main()

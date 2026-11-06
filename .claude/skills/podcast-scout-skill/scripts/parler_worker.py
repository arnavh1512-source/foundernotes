#!/usr/bin/env python3
"""Parler-TTS batch worker for narrate.py --engine parler (runs in the Parler venv: PARLER_PYTHON).

    $PARLER_PYTHON parler_worker.py jobs.json

jobs.json: {"model": "parler-tts/parler-tts-mini-v1", "description": "A male speaker ...",
            "jobs": [{"id": "s01", "text": "...", "out": "/abs/s01.raw.wav", "seed": 42}, ...]}

Parler-TTS (huggingface/parler-tts, Apache-2.0) is driven by a written voice DESCRIPTION, not a reference recording,
so no real person's voice is cloned. Each sentence is generated separately (Parler is steadiest on short inputs)
with the same description and seed, then joined with natural pauses. The model loads once per batch.
"""
import json, os, re, sys, time
import numpy as np, soundfile as sf, torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer, logging as hf_logging

hf_logging.set_verbosity_error()


MAX_WORDS = 14   # Parler skips clauses on long inputs (ASR caught whole phrases missing): keep chunks short


def sentences(text):
    """Sentences, then long ones split at colons/semicolons, then at the comma nearest the middle, until every chunk
    is <= MAX_WORDS words. Chunks inside a sentence get a short breath, between sentences a full pause."""
    out = []
    for snt in [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]:
        parts = [snt]
        changed = True
        while changed:
            changed = False
            nxt = []
            for p in parts:
                w = p.split()
                if len(w) <= MAX_WORDS:
                    nxt.append(p); continue
                cut = None
                m = [mm.end() for mm in re.finditer(r"[:;]\s", p)] or [mm.end() for mm in re.finditer(r",\s", p)]
                if m:
                    mid = len(p) / 2
                    cut = min(m, key=lambda c: abs(c - mid))
                if cut is None or cut <= 0 or cut >= len(p):
                    nxt.append(p); continue
                nxt += [p[:cut].strip(), p[cut:].strip()]; changed = True
            parts = nxt
        out += parts
    return out


def pause_after(s, nxt):
    if not re.search(r"[.!?]$", s.strip()):          # a clause break inside a sentence: a short breath
        return 0.16 if s.strip().endswith(",") else 0.24
    p = 0.38
    if s.rstrip().endswith("?"):
        p += 0.18
    if s.rstrip().endswith("..."):
        p += 0.15
    if nxt and len(nxt.split()) <= 4:
        p += 0.1
    return p


# ---------- one voice for the whole channel ----------
# Parler picks a voice from a DESCRIPTION, so every generated chunk can come out as a slightly different man
# (measured on the phone film: chunk median pitch 110-175 Hz, ~8 semitones apart). Fix, keeping Parler's human
# intonation: (1) a saved ANCHOR take (the channel voice, made once, reused for every film); (2) each chunk is
# generated as N candidates and the one whose WavLM speaker embedding is closest to the anchor wins (pitch distance
# breaks ties); (3) the winner's median pitch is moved to the anchor's (contour kept, shift capped at 4 semitones)
# and its loudness matched. Env: PARLER_ANCHOR (wav path), PARLER_CANDIDATES (default 3; 1 = off).
ANCHOR_TEXT = "Here's what the evidence actually says. Let's look at it together."
TARGET_F0 = 132.0          # a settled mid male voice; the anchor is chosen near this


class Voice:
    def __init__(self, sr):
        import librosa
        from transformers import AutoFeatureExtractor, WavLMForXVector
        self.lr, self.sr = librosa, sr
        self.fe = AutoFeatureExtractor.from_pretrained("microsoft/wavlm-base-plus-sv")
        self.m = WavLMForXVector.from_pretrained("microsoft/wavlm-base-plus-sv").eval()
        self.ref, self.f0, self.tone = None, TARGET_F0, None

    def emb(self, y):
        y16 = self.lr.resample(y, orig_sr=self.sr, target_sr=16000)
        with torch.no_grad():
            e = self.m(**self.fe(y16, sampling_rate=16000, return_tensors="pt")).embeddings[0]
        return torch.nn.functional.normalize(e, dim=-1).numpy()

    def med_f0(self, y):
        f0, _, _ = self.lr.pyin(y, fmin=60, fmax=320, sr=self.sr, frame_length=2048)
        v = f0[np.isfinite(f0)]
        return float(np.median(v)) if v.size > 5 else None

    # ---- tone colour: long-term average spectrum (LTAS) of the voiced frames, smoothed to ~1/3 octave
    def ltas(self, y):
        S = np.abs(self.lr.stft(y, n_fft=1024, hop_length=256)) ** 2
        e = S.sum(0); keep = e > e.max() * 1e-3
        p = 10 * np.log10(S[:, keep].mean(1) + 1e-10) if keep.any() else 10 * np.log10(S.mean(1) + 1e-10)
        f = np.fft.rfftfreq(1024, 1 / self.sr); out = np.empty_like(p)
        for i, fi in enumerate(f):                   # 1/3-octave smoothing
            lo, hi = fi / 1.122, fi * 1.122 + 30
            out[i] = p[(f >= lo) & (f <= hi)].mean()
        return out - out[(f > 300) & (f < 3000)].mean()   # shape only, level removed

    def tone_dist(self, y):
        if self.tone is None: return 0.0
        f = np.fft.rfftfreq(1024, 1 / self.sr); band = (f > 120) & (f < 8000)
        return float(np.sqrt(np.mean((self.ltas(y)[band] - self.tone[band]) ** 2)))

    def pieces(self, y):
        iv = self.lr.effects.split(y, top_db=35, frame_length=1024, hop_length=256)
        return [y[a:b] for a, b in iv if (b - a) / self.sr > 0.35]

    def score(self, y):
        """Closest to the channel voice, AND steady inside: every spoken piece near the voice's pitch and level."""
        f = self.med_f0(y)
        st = abs(12 * np.log2(f / self.f0)) if f else 6.0
        sim = float(self.emb(y) @ self.ref) if self.ref is not None else 0.0
        worst_st, lv = 0.0, []
        for pc in self.pieces(y):
            fp = self.med_f0(pc)
            if fp: worst_st = max(worst_st, abs(12 * np.log2(fp / (f or self.f0))))
            lv.append(20 * np.log10(np.sqrt(np.mean(pc ** 2)) + 1e-9))
        spread = (max(lv) - min(lv)) if len(lv) > 1 else 0.0
        self.last_worst = max(worst_st, spread / 2)       # semitones, or half the level spread in dB
        return sim - 0.03 * st - 0.012 * self.tone_dist(y) - 0.02 * worst_st - 0.006 * spread, f

    def ride(self, y):
        """Slow volume rider: evens loudness inside a sentence (+/-6 dB, ~0.4 s smoothing), keeps the expression."""
        hop = 256; fr = self.lr.util.frame(np.pad(y, (0, 1024)), frame_length=1024, hop_length=hop)
        r = np.sqrt((fr ** 2).mean(0)) + 1e-9; voiced = r > r.max() * 0.08
        if voiced.sum() < 4: return y
        tgt = np.median(r[voiced]); g = np.ones_like(r)
        g[voiced] = np.clip(tgt / r[voiced], 10 ** (-6 / 20), 10 ** (6 / 20))
        k = max(1, int(0.4 * self.sr / hop)); g = np.convolve(g, np.ones(k) / k, mode="same")
        gs = np.interp(np.arange(len(y)), np.arange(len(g)) * hop, g)
        return (y * gs).astype("float32")

    def settle(self, y, f):
        """Same voice every sentence: move the median pitch to the anchor's (rise and fall kept), EQ the tone colour
        to the voice's saved spectrum (smooth, capped at +/-8 dB) and level the VOICED parts, not the silences."""
        if f:
            n = float(np.clip(12 * np.log2(self.f0 / f), -4, 4))
            if abs(n) > 0.25:
                y = self.lr.effects.pitch_shift(y, sr=self.sr, n_steps=n).astype("float32")
        if self.tone is not None:
            g = np.clip(self.tone - self.ltas(y), -8, 8)
            g = np.convolve(g, np.ones(9) / 9, mode="same")
            D = self.lr.stft(y, n_fft=1024, hop_length=256)
            y = self.lr.istft(D * (10 ** (g / 20))[:, None], hop_length=256, length=len(y)).astype("float32")
        y = self.ride(y)
        fr = self.lr.util.frame(np.pad(y, (0, 1024)), frame_length=1024, hop_length=256)
        r = np.sqrt((fr ** 2).mean(0)); v = r[r > r.max() * 0.1]
        level = float(np.sqrt(np.mean(v ** 2))) if v.size else (float(np.sqrt(np.mean(y ** 2))) or 1.0)
        return (y * (0.11 / (level or 1.0))).astype("float32")


def trim(y, sr):
    nz = np.flatnonzero(np.abs(y) > 0.01)             # trim the model's leading/trailing silence
    return y[max(nz[0] - int(0.03 * sr), 0): nz[-1] + int(0.08 * sr)] if nz.size else y


def main():
    cfg = json.load(open(sys.argv[1]))
    torch.set_num_threads(max(1, torch.get_num_threads()))
    model = ParlerTTSForConditionalGeneration.from_pretrained(cfg["model"])
    tok = AutoTokenizer.from_pretrained(cfg["model"])
    sr = model.config.sampling_rate
    d = tok(cfg["description"], return_tensors="pt")
    ncand = max(1, int(os.environ.get("PARLER_CANDIDATES", "4")))

    def gen(text, seed):
        torch.manual_seed(seed)
        p = tok(text, return_tensors="pt")
        with torch.no_grad():
            a = model.generate(input_ids=d.input_ids, attention_mask=d.attention_mask,
                               prompt_input_ids=p.input_ids, prompt_attention_mask=p.attention_mask)
        return trim(a.cpu().numpy().squeeze().astype("float32"), sr)

    V = Voice(sr) if ncand > 1 or os.environ.get("PARLER_ANCHOR") else None
    if V is not None:
        anchor = os.environ.get("PARLER_ANCHOR")
        if anchor and os.path.exists(anchor):
            ya, asr_ = sf.read(anchor, dtype="float32")
            if asr_ != sr: ya = V.lr.resample(ya, orig_sr=asr_, target_sr=sr)
        else:                                            # make the channel voice once: 8 takes, closest to TARGET_F0
            takes = [gen(ANCHOR_TEXT, 7000 + k) for k in range(8)]
            f0s = [V.med_f0(y) or 999 for y in takes]
            ya = takes[int(np.argmin([abs(12 * np.log2(f / TARGET_F0)) for f in f0s]))]
            if anchor:
                os.makedirs(os.path.dirname(anchor) or ".", exist_ok=True); sf.write(anchor, ya, sr)
            print(f"parler: made the channel anchor voice ({', '.join(f'{f:.0f}' for f in f0s)} Hz takes)", file=sys.stderr)
        V.ref, V.f0 = V.emb(ya), V.med_f0(ya) or TARGET_F0
        tone_f = (os.path.splitext(anchor)[0] + ".tone.npy") if anchor else None
        if tone_f and os.path.exists(tone_f):
            V.tone = np.load(tone_f)
        else:                                        # learn the voice's tone colour once from clean takes, keep it
            refs = [gen(t_, 8100 + k) for k, t_ in enumerate([ANCHOR_TEXT, "So let's look at what they found.",
                    "That's a different question, and this video doesn't cover it.", "And this time, nothing."])]
            refs = [y_ for y_ in refs if (V.med_f0(y_) or 999) and abs(12 * np.log2((V.med_f0(y_) or 999) / V.f0)) < 3] or refs
            V.tone = np.median([V.ltas(y_) for y_ in refs], axis=0)
            if tone_f: np.save(tone_f, V.tone)
            print(f"parler: learned the voice's tone colour from {len(refs)} takes", file=sys.stderr)
        print(f"parler: anchor voice {V.f0:.0f} Hz, {ncand} candidates per chunk", file=sys.stderr, flush=True)

    t0 = time.time()
    for job in cfg["jobs"]:
        parts = sentences(job["text"]); out = []
        for i, snt in enumerate(parts):
            base = int(job.get("seed", 42)) + 1000 * i
            if V is None:
                y = gen(snt, base)
            else:
                best = None
                for k in range(ncand * 2):           # second round only when the first round's best is still odd
                    if k == ncand and best[3] <= 3.5: break
                    y_ = gen(snt, base + 97 * k + (5003 if k >= ncand else 0))
                    sc, f = V.score(y_)
                    if best is None or sc > best[0]: best = (sc, y_, f, V.last_worst)
                y = V.settle(best[1], best[2])
            out.append(y)
            if i < len(parts) - 1:
                out.append(np.zeros(int(pause_after(snt, parts[i + 1]) * sr), "float32"))
        y = np.concatenate(out) if out else np.zeros(1, "float32")
        y *= min(1.0, 0.89 / (float(np.max(np.abs(y))) or 1.0))
        sf.write(job["out"], y, sr)
        print(f"parler: {job['id']} {len(y)/sr:.1f}s ({time.time()-t0:.0f}s elapsed)", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()

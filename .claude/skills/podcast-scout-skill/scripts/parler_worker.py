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
        self.ref, self.f0 = None, TARGET_F0

    def emb(self, y):
        y16 = self.lr.resample(y, orig_sr=self.sr, target_sr=16000)
        with torch.no_grad():
            e = self.m(**self.fe(y16, sampling_rate=16000, return_tensors="pt")).embeddings[0]
        return torch.nn.functional.normalize(e, dim=-1).numpy()

    def med_f0(self, y):
        f0, _, _ = self.lr.pyin(y, fmin=60, fmax=320, sr=self.sr, frame_length=2048)
        v = f0[np.isfinite(f0)]
        return float(np.median(v)) if v.size > 5 else None

    def score(self, y):
        f = self.med_f0(y)
        st = abs(12 * np.log2(f / self.f0)) if f else 6.0
        sim = float(self.emb(y) @ self.ref) if self.ref is not None else 0.0
        return sim - 0.02 * st, f

    def settle(self, y, f):
        """Move the chunk's median pitch to the anchor's (keeps the rise and fall) and match loudness."""
        if f:
            n = float(np.clip(12 * np.log2(self.f0 / f), -4, 4))
            if abs(n) > 0.25:
                y = self.lr.effects.pitch_shift(y, sr=self.sr, n_steps=n).astype("float32")
        rms = float(np.sqrt(np.mean(y ** 2))) or 1.0
        return (y * (0.085 / rms)).astype("float32")


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
    ncand = max(1, int(os.environ.get("PARLER_CANDIDATES", "3")))

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
                for k in range(ncand):
                    y_ = gen(snt, base + 97 * k)
                    sc, f = V.score(y_)
                    if best is None or sc > best[0]: best = (sc, y_, f)
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

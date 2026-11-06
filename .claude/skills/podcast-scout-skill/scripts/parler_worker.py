#!/usr/bin/env python3
"""Parler-TTS batch worker for narrate.py --engine parler (runs in the Parler venv: PARLER_PYTHON).

    $PARLER_PYTHON parler_worker.py jobs.json

jobs.json: {"model": "parler-tts/parler-tts-mini-v1", "description": "A male speaker ...",
            "jobs": [{"id": "s01", "text": "...", "out": "/abs/s01.raw.wav", "seed": 42}, ...]}

Parler-TTS (huggingface/parler-tts, Apache-2.0) is driven by a written voice DESCRIPTION, not a reference recording,
so no real person's voice is cloned. Each sentence is generated separately (Parler is steadiest on short inputs)
with the same description and seed, then joined with natural pauses. The model loads once per batch.
"""
import json, re, sys, time
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


def main():
    cfg = json.load(open(sys.argv[1]))
    torch.set_num_threads(max(1, torch.get_num_threads()))
    model = ParlerTTSForConditionalGeneration.from_pretrained(cfg["model"])
    tok = AutoTokenizer.from_pretrained(cfg["model"])
    sr = model.config.sampling_rate
    d = tok(cfg["description"], return_tensors="pt")
    t0 = time.time()
    for job in cfg["jobs"]:
        parts = sentences(job["text"]); out = []
        for i, snt in enumerate(parts):
            torch.manual_seed(int(job.get("seed", 42)) + 1000 * i)
            p = tok(snt, return_tensors="pt")
            with torch.no_grad():
                a = model.generate(input_ids=d.input_ids, attention_mask=d.attention_mask,
                                   prompt_input_ids=p.input_ids, prompt_attention_mask=p.attention_mask)
            y = a.cpu().numpy().squeeze().astype("float32")
            nz = np.flatnonzero(np.abs(y) > 0.01)             # trim the model's leading/trailing silence
            if nz.size:
                y = y[max(nz[0] - int(0.03 * sr), 0): nz[-1] + int(0.08 * sr)]
            out.append(y)
            if i < len(parts) - 1:
                out.append(np.zeros(int(pause_after(snt, parts[i + 1]) * sr), "float32"))
        y = np.concatenate(out) if out else np.zeros(1, "float32")
        y *= min(1.0, 0.89 / (float(np.max(np.abs(y))) or 1.0))
        sf.write(job["out"], y, sr)
        print(f"parler: {job['id']} {len(y)/sr:.1f}s ({time.time()-t0:.0f}s elapsed)", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build an Entertainment IP episode workspace: render each shot into a cache, assemble one take per variant.

A shot's render key hashes the engine rig, scenes/_common.js, its own scene file, its definition and the
asset version files it uses. Unchanged shots are reused, so variants share identical renders and a revised
shot re-renders alone.

    python3 ep_build.py <workspace> --precheck  frames from every shot first (nothing renders until checked)
    python3 ep_build.py <workspace>             render missing shots, assemble takes, run QC
    python3 ep_build.py <workspace> --export    copy the selected take to export/
"""
import argparse, hashlib, json, re, shutil, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
ENGINE = REPO / ".claude/skills/think-stick-engine/engine"
RENDER = REPO / ".claude/skills/motion/scripts/render.mjs"
SCRIPTS = REPO / ".claude/skills/podcast-scout-skill/scripts"
FONTS = REPO / ".claude/skills/podcast-scout-skill/assets/ink-gold-kit/fonts"
OVERLAY = Path(__file__).resolve().parents[1] / "engine/overlay.js"   # playback chip, labels, rewind effect
OVERLAY_KEYS = ("time", "ui", "labels", "fx", "hits", "light", "counter", "twos", "special")
SFX = REPO / ".claude/skills/think-stick-engine/assets/sfx"
FPS = 30
PAGE_VERSION = "1"  # bump when shot_page() changes, so cached clips re-render


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load(ws):
    return json.loads((Path(ws) / "workspace.json").read_text())


def save(ws, m):
    (Path(ws) / "workspace.json").write_text(json.dumps(m, indent=1) + "\n")


def vertical(m):
    return m.get("format") == "vertical"


def asset_file(ws, m, aid, v):
    for a in m["assets"]:
        if a["id"] == aid:
            for ver in a["versions"]:
                if ver["v"] == v:
                    return Path(ws) / ver["file"]
    raise KeyError(f"{aid} v{v}")


def resolve(m, variant):
    """Shot list for one variant: the base shots with that variant's overrides applied."""
    ov = next(v for v in m["variants"] if v["id"] == variant).get("overrides", {})
    base = {"twos": True} if m.get("twos") else {}   # "twos": true on the manifest runs every shot on twos
    return [{**base, **s, **ov.get(s["id"], {})} for s in m["shots"]]


def render_key(ws, m, shot):
    h = hashlib.sha256(PAGE_VERSION.encode())
    for p in (ENGINE / "stick.html", ENGINE / "faces.js", Path(ws) / "scenes/_common.js", Path(ws) / f"scenes/{shot['scene']}.js"):
        h.update(p.read_bytes())
    h.update(json.dumps({k: shot.get(k) for k in ("id", "scene", "dur", "args", "uses")}, sort_keys=True).encode())
    extra = {k: shot[k] for k in OVERLAY_KEYS if k in shot}
    if extra:  # only shots that use time remaps or overlays depend on overlay.js, so older episodes keep their cached clips
        h.update(OVERLAY.read_bytes()); h.update(json.dumps(extra, sort_keys=True).encode())
    if vertical(m) or not m.get("overlay_tag", True):
        h.update(json.dumps({"format": m.get("format"), "overlay_tag": m.get("overlay_tag", True)}, sort_keys=True).encode())
    for u in shot.get("uses", []):
        h.update(asset_file(ws, m, u["asset"], u["v"]).read_bytes())
    return h.hexdigest()[:12]


def shot_page(ws, m, shot, key):
    """Engine rig with the timeline replaced by one shot (local time), its scene and its asset versions."""
    film = Path(ws) / "film"
    (film / "fonts").mkdir(parents=True, exist_ok=True)
    for f in FONTS.glob("InstrumentSans-*.ttf"):
        shutil.copy(f, film / "fonts" / f.name)
    shutil.copy(ENGINE / "faces.js", film / "faces.js")
    shutil.copy(OVERLAY, film / "overlay.js")
    assets = {u["asset"]: json.loads(asset_file(ws, m, u["asset"], u["v"]).read_text()) for u in shot.get("uses", [])}
    tag = (f"{m['series'].upper()} · {m['episode']} · {shot['id']} · ANIMATIC" + (" · TEMP AUDIO" if any(c.get("temporary") for c in m["audio_cues"]) else "")) if m.get("overlay_tag", True) else ""
    (film / f"shot_{key}.js").write_text(f"window.SHOT={json.dumps({**shot, 'tag': tag})};window.ASSETS={json.dumps(assets)};")
    html = (ENGINE / "stick.html").read_text()
    head = '<script src="timing.js"></script><script src="turns.js"></script><script src="shots.js"></script>'
    t01 = "const T0=+(Q.get('from')||0), T1=+(Q.get('to')||window.DUR);"
    assert head in html and t01 in html and "const SEGS=window.SEG" in html, "engine stick.html changed: update shot_page()"
    logo = "LOGO.src='logo.png';"
    assert logo in html, "engine stick.html changed: update shot_page()"
    # Entertainment IP carries its own series brand: never load the Think! logo
    if vertical(m):  # Reels/Shorts: same rig, a 1080x1920 canvas
        dims, canvas = "const W=1920,H=1080", 'width="1920" height="1080"'
        assert dims in html and canvas in html, "engine stick.html changed: update shot_page()"
        html = html.replace(dims, "const W=1080,H=1920").replace(canvas, 'width="1080" height="1920"')
    html = html.replace(head, f'<script src="shot_{key}.js"></script>').replace(t01, "const T0=0, T1=window.SHOT.dur;").replace(logo, "")
    html = re.sub(r'<script src="scenes\.js"></script>.*?<script src="env\.js"></script>',
                  f'<script src="faces.js"></script><script src="overlay.js"></script><script src="../scenes/_common.js"></script><script src="../scenes/{shot["scene"]}.js"></script>', html, flags=re.S)
    i = html.index("const SEGS=window.SEG")
    html = html[:i] + """window.seek=async(tt)=>{ const SH=window.SHOT, d=SH.dur, tm=SH.time;
  // ON TWOS: hold each drawing for two frames (the overlays still move on ones)
  const t=Math.min(d-1e-3,SH.twos?Math.floor(+tt*15+1e-6)/15:+tt), tOv=Math.min(d-1e-3,+tt);
  // time remap: "time": {"from": a, "to": b, "scene_dur": D} plays the scene from a to b over the shot (b < a rewinds, a stretch is slow motion)
  // or "keys": [[shot_t, scene_t], ...] for a speed ramp (e.g. a near-freeze on the key moment of a slow replay)
  const ramp=k=>{ let i=1; while(i<k.length-1&&t>k[i][0]) i++; const [a,b]=[k[i-1],k[i]]; return a[1]+(b[1]-a[1])*Math.max(0,Math.min(1,(t-a[0])/((b[0]-a[0])||1))) };
  const sd=tm&&tm.scene_dur||d, ts=tm?Math.max(0,Math.min(sd-1e-3,tm.keys?ramp(tm.keys):tm.from+(tm.to-tm.from)*t/d)):t; NOW=ts; CAMZ=1; CAMX=0;
  const draw=()=>{ x.setTransform(1,0,0,1,0,0); x.globalAlpha=1; x.fillStyle=PAPER; x.fillRect(0,0,W,H); S[SH.scene](ts/sd,ts,sd,SH.args||{}) };
  SHAKE=0; draw(); if(SHAKE>0){ const sk=SHAKE; SHAKE=sk; draw() }
  x.setTransform(1,0,0,1,0,0); x.globalAlpha=1; x.drawImage(grain(),0,0,W,H); ovDraw(SH,tOv);
  if(!window.SHOT.tag) return; x.font='700 24px Inst'; const tw=x.measureText(window.SHOT.tag).width; x.fillStyle='rgba(20,20,24,.62)'; x.fillRect(28,26,tw+28,40); x.fillStyle='#f6f2e9'; x.textBaseline='middle'; x.fillText(window.SHOT.tag,42,47) };
document.fonts.ready.then(()=>seek(0));
</script></body></html>
"""
    page = film / f"shot_{key}.html"
    page.write_text(html)
    return page


def render_shot(ws, m, shot):
    key = render_key(ws, m, shot)
    clip = Path(ws) / f"takes/clips/{shot['id']}-{key}.mp4"
    if clip.exists():
        return key, clip, False
    clip.parent.mkdir(parents=True, exist_ok=True)
    page = shot_page(ws, m, shot, key)
    subprocess.run(["node", str(RENDER), str(page), "--out", str(clip)], cwd=REPO, check=True, stdout=subprocess.DEVNULL)
    return key, clip, True


def duration(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode())


def cue_file(ws, cue):
    """A cue's sound: the episode's own sound/ folder first (its foley), then the shared CC0 bank."""
    files = sorted((Path(ws) / "sound").glob(f"{cue['kind']}*.wav")) or sorted(SFX.glob(f"{cue['kind']}*.wav"))
    if not files:
        raise SystemExit(f"cue {cue.get('id')}: no sound named {cue['kind']}* in sound/ or the shared bank")
    return files[cue.get("pick", 0) % len(files)]


def cue_filter(i, cue, ms):
    """One cue's chain: optional cut to cue['dur'] (with a 30 ms fade, so a sound can stop on an action), delay, gain."""
    cut = f"atrim=0:{cue['dur']},afade=t=out:st={max(0, cue['dur'] - 0.03):.3f}:d=0.03," if cue.get("dur") else ""
    return f"[{i}]{cut}adelay={ms}|{ms},volume={cue.get('gain', 1.0)}[a{i}]"


def build_audio(ws, m, shots, clips, out):
    """Cues at shot start + local time; a quiet room tone keeps holds from being dead air."""
    starts, t = {}, 0.0
    for s, c in zip(shots, clips):
        starts[s["id"]] = t
        t += duration(c)
    total, ins, flt = t, [], []
    for i, c in enumerate(m["audio_cues"]):
        f = cue_file(ws, c)
        ins += ["-i", str(f)]
        ms = int(round((starts[c["shot"]] + c["t"]) * 1000))
        flt.append(cue_filter(i, c, ms))
    n = len(m["audio_cues"])
    flt.append(f"anoisesrc=d={total:.3f}:c=brown:a=0.03:seed=7,lowpass=f=700,highpass=f=60[rt]")
    flt.append("".join(f"[a{i}]" for i in range(n)) + f"[rt]amix=inputs={n + 1}:normalize=0,atrim=0:{total:.3f},"
               "acompressor=threshold=0.1:ratio=4:attack=3:release=150:makeup=2,alimiter=limit=0.7[o]")  # tame transients so assembly can reach -14 LUFS
    raw = out.with_name(out.stem + "-raw.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(flt), "-map", "[o]", "-ar", "48000", "-ac", "2", str(raw)], check=True)
    normalize(raw, out)
    return starts, total


def normalize(src, dst, lufs=-14.0, tp=-1.5):
    """Measured two-pass loudnorm. assemble.py's single pass undershoots on short clips with sparse cues."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-af", f"loudnorm=I={lufs}:TP={tp}:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, check=True)
    j = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    af = (f"loudnorm=I={lufs}:TP={tp}:LRA=11:linear=true:measured_I={j['input_i']}:measured_TP={j['input_tp']}"
          f":measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", af, "-ar", "48000", str(dst)], check=True)
    # sparse, sharp foley: linear gain is capped by the true-peak limit and lands short (A12, A13 measured -16.2 LUFS).
    # When it lands more than 1 LU short, raise it through a limiter and normalise once more.
    got = integrated(dst)
    if got is not None and got < lufs - 1.0:
        lifted = Path(str(dst) + ".lift.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(dst), "-af", f"volume={lufs - got + 1.0:.2f}dB,alimiter=limit=0.8:level=false",
                        "-ar", "48000", str(lifted)], check=True)
        normalize_once(lifted, dst, lufs, tp); lifted.unlink(missing_ok=True)


def integrated(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[0-9.]+) LUFS", r.stderr)
    return float(m[-1]) if m else None


def normalize_once(src, dst, lufs, tp):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-af", f"loudnorm=I={lufs}:TP={tp}:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True, check=True)
    j = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    af = (f"loudnorm=I={lufs}:TP={tp}:LRA=11:linear=true:measured_I={j['input_i']}:measured_TP={j['input_tp']}"
          f":measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af", af, "-ar", "48000", str(dst)], check=True)


def build(ws):
    ws = Path(ws).resolve()
    m = load(ws)
    m["takes"], log = [], []
    py = sys.executable
    for var in m["variants"]:
        shots = resolve(m, var["id"])
        rows = []
        for s in shots:
            key, clip, fresh = render_shot(ws, m, s)
            log.append(f"{var['id']:>12} {s['id']}: {'RENDERED' if fresh else 'reused  '} {clip.name}")
            rows.append({"id": s["id"], "dur": s["dur"], "render_key": key, "clip": str(clip.relative_to(ws)), "clip_sha256": sha(clip),
                         "uses": [{**u, "sha256": sha(asset_file(ws, m, u["asset"], u["v"]))} for u in s.get("uses", [])]})
        clips = [ws / r["clip"] for r in rows]
        audio = ws / f"takes/{var['id']}-audio.wav"
        starts, total = build_audio(ws, m, shots, clips, audio)
        take = ws / f"takes/{var['id']}.mp4"
        subprocess.run([py, str(SCRIPTS / "assemble.py"), "--scenes", *map(str, clips), "--narration", str(audio), "--out", str(take),
                        "--format", "vertical" if vertical(m) else "landscape"],
                       check=True, stdout=subprocess.DEVNULL)
        # assemble.py runs its own single-pass loudnorm, which pulls sparse foley back down (A13: -14.0 -> -16.2 LUFS);
        # put our measured two-pass audio back into the take (picture copied untouched)
        fixed = take.with_suffix(".mux.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(take), "-i", str(audio), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{total:.3f}", str(fixed)], check=True)
        fixed.replace(take)
        qc = ws / f"takes/{var['id']}-qc.json"
        subprocess.run([py, str(SCRIPTS / "qc_video.py"), str(take), "--min-duration", "5", "--format", "vertical" if vertical(m) else "horizontal", "--json", str(qc), "--sheet", str(ws / f"takes/{var['id']}-sheet.jpg")],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for r in rows:
            r["start"] = round(starts[r["id"]], 3)
        m["takes"].append({"id": f"T-{var['id']}", "variant": var["id"], "file": str(take.relative_to(ws)), "sha256": sha(take),
                           "duration": round(duration(take), 3), "qc": json.loads(qc.read_text())["status"] if qc.exists() else "NOT RUN", "shots": rows})
    save(ws, m)
    print("\n".join(log))
    for t in m["takes"]:
        print(f"{t['id']}: {t['duration']}s  QC {t['qc']}  {t['file']}")


def precheck(ws, step=0.25):
    """Frames from every shot of every variant, without rendering video: review/precheck/<variant>.jpg."""
    ws = Path(ws).resolve()
    m = load(ws)
    grab = REPO / ".claude/skills/think-stick-engine/tools/grab.mjs"
    for var in m["variants"]:
        frames = []
        # clear the last run first: after a page error, old frames left on disk look like a fresh precheck
        shutil.rmtree(ws / f"review/precheck/{var['id']}", ignore_errors=True)
        (ws / f"review/precheck/{var['id']}.jpg").unlink(missing_ok=True)
        for s in resolve(m, var["id"]):
            key = render_key(ws, m, s)
            out = ws / f"review/precheck/{var['id']}/{s['id']}"
            out.mkdir(parents=True, exist_ok=True)
            ts = [round(min(s["dur"] - 1 / FPS, i * step), 3) for i in range(int(s["dur"] / step) + 1)]
            r = subprocess.run(["node", str(grab), str(shot_page(ws, m, s, key).resolve()), str(out.resolve()), *map(str, ts)], capture_output=True, text=True)
            if r.returncode or "ERR" in r.stdout:
                sys.exit(f"{s['id']}: page error\n{r.stdout}{r.stderr}")
            frames += [(s["id"], t, out / f"t{t:06.2f}.png") for t in ts]
        sheet = ws / f"review/precheck/{var['id']}.jpg"
        tile = ",".join(f"{sid} {t:.2f}" for sid, t, _ in frames)
        lst = ws / f"review/precheck/{var['id']}.txt"
        lst.write_text("".join(f"file '{p.resolve()}'\nduration 1\n" for _, _, p in frames))
        cols = 6
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-vf", f"scale=400:-2,tile={cols}x{-(-len(frames) // cols)}", "-frames:v", "1", str(sheet)], check=True)
        print(f"{var['id']}: {len(frames)} frames -> {sheet}  ({tile})")


def export(ws):
    ws = Path(ws).resolve()
    m = load(ws)
    sel = m.get("selected") or sys.exit("no selected take: review the takes and record selected.take and selected.reason first")
    take = next(t for t in m["takes"] if t["id"] == sel["take"])
    label = "_TEMP-AUDIO" if any(c.get("temporary") for c in m["audio_cues"]) else ""
    out = ws / "export" / f"{m['series_slug']}-{m['episode'].lower()}-animatic{label}.mp4"
    out.parent.mkdir(exist_ok=True)
    shutil.copy(ws / take["file"], out)
    m["export"] = {"file": str(out.relative_to(ws)), "from_take": take["id"], "sha256": sha(out)}
    save(ws, m)
    print("exported", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("workspace")
    ap.add_argument("--export", action="store_true", help="copy the selected take to export/")
    ap.add_argument("--precheck", action="store_true", help="frames from every shot before rendering (owner rule)")
    a = ap.parse_args()
    precheck(a.workspace) if a.precheck else export(a.workspace) if a.export else build(a.workspace)

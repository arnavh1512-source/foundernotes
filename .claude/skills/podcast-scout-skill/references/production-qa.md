# Production QA (Gate Q)

Owned by studio-reality-checker. Default verdict NEEDS WORK until evidence says otherwise.
You cannot watch or hear the video: judge from measurements, stills and the contact sheet, and
say so in the report.

## Automated

```bash
python3 scripts/qc_video.py final/video.mp4 --timings narration/timings.json \
  --captions narration/captions.srt --sheet final/sheet.jpg --json final/qc.json
python3 scripts/package_lint.py package/package.json --duration <seconds>
```

FAIL lines block delivery. Every WARN is either fixed or justified in `ledger.md`.

## Look (open the images)

- [ ] Contact sheet: every scene distinct, nothing empty, no slide-like stretches.
- [ ] Stills at each scene midpoint and each transition midpoint: no muddy double exposure,
      no text clipped by frame edge, no overlaps, no fallback fonts, no missing images.
- [ ] Frame 0 shows the subject (no fade from black); first useful insight before 0:30.
- [ ] Labels readable at phone size; contrast OK; captions zone clear.
- [ ] Charts: zero baseline, units, source line, exact ledger numbers.

## Truth

- [ ] Claim table: every spoken/on-screen claim → ledger source (read, dated). None missing.
- [ ] Qualifiers in the brief survived into narration, titles and thumbnail.
- [ ] Imagined scenes/analogies are framed as such in narration.
- [ ] No podcast footage, guest voice, logos, real likenesses or copyrighted characters.

## Sound

- [ ] `timings.json` engine/voice is the male default (or owner's explicit choice).
- [ ] −14 LUFS ±1.5, true peak ≤ −1 dBTP; no dead air > 2 s mid-video.
- [ ] Music/SFX licences recorded; music ducked under voice.
- [ ] If Whisper was available: transcript diff shows no dropped words. Otherwise: "not checked".

## Captions

- [ ] Caption text matches speech (or is a faithful shortening); names spelled right.
- [ ] ≤ 42 chars/line, ≤ 20 chars/s, 0.7–7 s, no overlaps, ends before video end.

## Report

```
VERDICT: READY | NEEDS WORK | NOT READY        RATING: B-/B/B+/A- (honest)
ATTEMPT: n of 3
EVIDENCE: qc.json summary, sheet.jpg, stills/…, claim table
REQUIRED FIXES: [scene/file] problem → fix → owner role
NOT CHECKED: what could not be verified here (e.g. listening test)
```

# Contact correction after internal draft rendering

This revision follows the frame-supported Alan Becker comparison documented in BENCHMARK_CORRECTION_2026-11-17.md. The lesson being tested is grounded whole-body performance with stable support and purposeful steps. No new continuous benchmark playback or sound review was completed.

## Evidence

Source at 12eb1da5f309b60636903c1ce32fd68836fbe5ee moves the recovery foot from [650,830] at 4.15 seconds to [630,830] at 4.8 seconds, while keeping its height at the ground plane. It also moves the first stair support from [420,800] at 9.4 seconds to [350,770] at 10.5 seconds without a lift arc. The earlier tests checked only the initial force-phase support. These are geometry findings, not claims from watching the encoded video.

## Correction and checks

Recovery contacts now stay planted through 7.0 seconds. The repositioning foot lifts during 7.0–8.3 seconds. Stair steps alternate one fixed support and one lifted foot; the final contacts are [420,800] and [350,770]. Local Node tests pass all three tests, including 316 sampled poses, limb lengths/reach, prop grips, recovery contacts and stair support intervals. JavaScript sampling reports no clamped limbs.

## Review hold

The prior GitHub Actions run 44099388529 successfully rendered its draft and extracted frames, but that is the prior geometry. This revision needs a new render and review. Local execution has recovered; the normal HTML renderer still lacks Playwright, whose registry could not resolve. Artifact transfer also failed on DNS. Browser artifact download timed out; local file navigation was explicitly blocked by browser policy. No workaround was used to bypass that policy. Headless Chrome did not produce the requested frame. No revised frames or full motion were inspected. The PR remains draft, with no artistic approval and no owner-facing preview. Do not claim indefinite background improvement or a completed narrated pilot.

# Optional animation backend assessment

Reviewed upstream READMEs on 2026-11-17. No upstream source, characters, sample audio or demo assets are vendored.

| Project | Best use here | Connection currently implemented |
| --- | --- | --- |
| [Synfig](https://github.com/synfig/synfig) | Vector/bitmap tweened character scenes | Checked picture import |
| [Friction](https://github.com/friction2d/friction) | Vector/raster motion graphics | Checked picture import |
| [Theatre.js](https://github.com/theatre-js/theatre) | Visual timing authoring for JS/SVG/Three.js | Capability routing only; authoring-data bridge is future work |
| [OpenToonz](https://github.com/opentoonz/opentoonz) | Hand-drawn facial acting, gestures, frame-by-frame scenes | Checked picture import |
| [FreeMoCap](https://github.com/freemocap/freemocap) | Performer movement reference and capture | Import after external retargeting/rendering; no live capture adapter |
| [Effekseer](https://github.com/effekseer/Effekseer) | Restrained particle accents | Checked picture import after external effect rendering |
| [OpenVDB](https://github.com/AcademySoftwareFoundation/openvdb) | Sparse volumetric effects through a compatible renderer | Checked picture import after external 3D rendering; not a standalone scene generator |
| [Natron](https://github.com/NatronGitHub/Natron) | Masks, tracking, compositing and color finishing | Checked picture import |
| [Remotion](https://github.com/remotion-dev/remotion) | Deterministic scripted SVG/React production | Direct local CLI producer and original technical fixture |

Use scripts/animation_backends.py --list or --recommend character to inspect the capability catalog. These tools are optional: adding names to a catalog does not install binaries or prove integration quality. No automatic capture, retargeting, OpenToonz project generation, Theatre timeline serialization, native project renderer or AI character generation is implemented.

For the target psychology videos, first test one original character/world with the same narration in two treatments. Prefer clear poses, anticipation, readable cause/effect, held-object continuity, reaction shots, purposeful cuts and clean audio. Use effects when they explain the idea.

OpenToonz is a good authoring option for expressive hand-drawn scenes. Export and assemble a picture edit matching the measured narration, provide source project/asset rights in picture_provenance, then pass through produce and independent critique. Do not assume that installing it generates finished artwork from scripts.

Upstream license notes: Synfig GPLv3; Friction GPL-3.0-only; Theatre core Apache-2.0 and Studio AGPLv3; FreeMoCap AGPLv3; OpenVDB current README Apache-2.0 (relicensed); Effekseer root MIT with separate tool/runtime licenses; Natron GPLv2; OpenToonz modified BSD outside separately licensed third-party/brush directories. Review the exact pinned release and bundled assets before redistributing code or binaries. No code license determines rights to unrelated art/audio.

Theatre README says newer development temporarily moved to a private repository; FreeMoCap development README notes private git dependencies. Effekseer warns against master for production. Pin tested releases instead of tracking development branches.

## Motion kit study
Studied [mahabharat-motion-kit](https://github.com/SahilScripts/mahabharat-motion-kit) at 1f7349369be58bc1d7dfb5b7c97a537d7f370909. Useful general techniques: word-anchored action, depth-layer camera movement, two-bone reach with a prop nested under the actual hand transform, and strip/close-up review. Independently implemented in motion/assets/story-motion.mjs and motion/remotion. No license file was present in the inspected tree; no source or artwork was copied. Its Hindi, vertical and no-caption choices do not override FounderNotes channel rules.

Remotion has its own license terms; do not describe it as MIT. Check [current licensing](https://www.remotion.dev/license) for your organization before production use.

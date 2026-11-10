# Explanation-first visual direction — FounderNotes

**Owner direction (2026-11-11).** Choose animation style **after** the script and viewer-first plan establish what the video must explain. A recognizable, coherent visual world matters more than a large catalog, flashy transitions, or constantly changing styles. Treat references as examples of broad storytelling principles, **not** assets or shot lists to reproduce.

## The ordering that cannot be reversed

1. **Viewer's problem and learning promise first.** Complete and pass `viewer-first-plan.json` pre-script gate. The first 15–30 seconds introduce the recognizable problem and deliver an insight; fictional characters must not precede that context.
2. **Lock the claim and explanatory beat.** For each chapter/shot, write `viewer_question`, `explained_change`, `claim_id` (if factual), and `visual_job` before querying any style catalog. A scene must *show a situation, action, mechanism, comparison, evidence, consequence, or intentional reflection*.
3. **Match the visual job to the medium.** Search the actual animation library only now. Select one principal **visual grammar** for the episode and up to two complementary explanations/diagram treatments; do not swap aesthetics just to increase variety. Verify engine availability, licenses, cost and deterministic timing.
4. **Prove with the SAME narration.** Compare **two or three** meaningfully different treatments of one **identical short voiced excerpt** (recommended 20–40 seconds from the approved 60–90 second pilot). Keep **exact script, recorded WAV, duration, captions, factual claims and scene objective identical**. Change visual design, acting, framing and staging—not the explanatory content. Render actual comparable excerpts where the tools are available; three stills are useful preflight, **not** a substitute for temporal comparison. Record every real render and limitation; no synthetic scores masquerading as outsider feedback.
5. **Pick on explanatory clarity first.** Inspect shots at actual narration speed, mobile readability and with audio on. Record the option chosen, the rejected alternatives, timing, concrete weaknesses and owner/editorial approval in `production/visual-treatment-comparison.md` using the template. Use the chosen direction to make a **reviewed 60–90 second pilot**, then pass the existing full-production gate. A draft comparison alone never proves the full pilot was watched.

## Scene need → animation approach

| What a scene must communicate | Default starting treatment | Visible proof that it communicates |
| --- | --- | --- |
| Viewers recognize themselves | Original simple characters in a familiar bedroom, classroom, workplace or conversation | Recognizable situation and specific contextual prop |
| Emotion or social tension | Readable posture, face, hesitation and reaction shots | Character **changes** expression or position in response to a cause |
| Invisible mechanism | Tactile metaphor: a growing load, branching choices, a repeating loop | Mechanism's cause → operation → consequence is visible and not misleading |
| Research or evidence | Clean, sourced diagram, original illustrated experiment or honest data visual | Numbers, comparison and caveat align with the research ledger |
| Important distinction | Side-by-side scenarios or a before-and-after transformation | The relevant variable is clear and the contrast is not deceptive |
| Important insight landing | Deliberate visual hold on **one powerful image** | Viewers have enough time to interpret it, rather than arbitrary dead air |

## Preferred direction for upcoming **psychology explainers**

Use **original illustrated characters** with **simple silhouettes, expressive poses, restrained colors, tactile/textured backgrounds and occasional clean explanatory diagrams** as the preferred candidate **when it serves the specific explanation**. This is *not* a mandate to make engineering, documentary, data-heavy or unrelated episodes look like psychology cartoons.

- **Acting, not standing and gesturing:** characters slump, hesitate, lean back, turn away, interrupt, reach or visibly react to another person's behavior. Design a reaction chain with a cause and payoff.
- **Environment variety within one art style:** bedrooms, classrooms, workspaces, kitchens, hallways and conversation scenes *only when the narrative naturally requires them*. Avoid recurring generic doorways, posters or interchangeable faceless rooms.
- **Meaningful action:** e.g., someone hides a phone or fails to notice an offered object. Each pose or movement must communicate a distinct idea. Don't animate for animation's sake.
- **Camera grammar:** alternate appropriate face/reaction close-ups, hands/props, medium two-shots, context-setting wides and diagrams. Vary framing **because** emphasis changes; no three unmotivated pushes in a row.
- **Visual simplicity:** protect the focal action, negative space, readable diagram labels and bottom `180px` subtitle safe area. Avoid headline piles, decorative motion clutter or a slideshow of repeated characters.
- **Intentional holds:** let an image land when the script needs it, with purposeful subtle acting/texture or a readable tableau. Differentiate deliberate stillness from missing renders, frozen output and dropped narration; document the intent for QC.

## Storyboard evidence required per important shot

Record `shot_id | voice start-end | chapter payoff | visual_job | concrete setting | recurring character/prop | initial pose → meaningful action → reaction/outcome | camera/framing | mechanism/claim_id | style/engine | continuity in/out | readable labels + captions safe zone`.

Maintain a character/world sheet (silhouette, clothing, face/pose range, reusable background surfaces, palette, lighting and scale) so changing **situations** does not make the episode look like unrelated videos. Use original, cleared artwork rather than copying footage, characters, compositions, a competitor's signature designs or copyrighted graphic elements.

## Same-narration comparison: decision rubric

For each treatment record measured `actual_excerpt_seconds`, voice WAV path, start/end, source/render path and screenshot set. Judge:

1. **Clarity of mechanism** (highest priority): can a viewer describe what changed and why?
2. **Recognition / acting**: clear familiar context, facial/postural cues and purposeful reaction.
3. **Information hierarchy**: one focal action, readable labels and subtitles on a phone.
4. **Narrative continuity**: character/object identities, scene world and transitions are consistent.
5. **Timing and sound**: actions land against the **same recorded audio**; holds/pace feel intentional.
6. **Rights and practical renderability**: original assets, licensed dependencies, installed engine, deterministic export and budget.

Use recorded observations with timecodes rather than inventing automated "clarity" scores. Prefer the more understandable treatment even if it is technically simpler. The existing `viewer-first`, `lint_scenes.py`, `qc_video.py`, fact lock and independent review gates still apply. If no full clips were rendered, label the comparison **unverified** and do not approve full production.

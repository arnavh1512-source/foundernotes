# Viewer Value & Hook Analysis — required for every supplied source video

**Purpose:** answer *why would someone care, what exactly might they find interesting, why watch to the end, what will they learn, and how can they use this knowledge?* The output is a researched **editorial hypothesis**, not a guarantee of CTR, virality, retention, views or audience reactions.

## Trigger and permissions

- **Source mode (default):** whenever the owner supplies a video, video URL, recorded episode, clip or video-derived transcript to *make FounderNotes content from*, run this analysis **before the final angle and script**. Do not require a special command. A standalone topic with no video can also use this framework without falsely inventing source-video observations.
- **Competitor mode (strictly opt-in):** only on an explicit request such as "analyze my competitor's video" or "compare these competitor channels/videos". A source video supplied for creative inspiration **is not automatic permission** to perform competitor benchmarking. A routine public YouTube topic-coverage lookup for originality is not a competitor teardown: do not analyze others' scripts, thumbnails, edit pacing or channel statistics without owner opt-in.
- **Analysis only:** if the owner asks just to study a video/competitor, write the report and stop. If they ask to create content from a source video, use the approved findings for an **original, independently fact-checked** treatment; do not lift scripts, visuals, voices, titles, thumbnails, music or the original video's footage.
- Competitor analysis is on-demand per request, not a sticky toggle for all future productions. No monitoring, paid analytics, channel scraping or unauthorized browsing.

## Intake: what was actually examined?

1. Record each input's identity, whether it is an owner's upload or a video URL, and the **access path**: real video+audio review, transcript-only, frame-only, partial coverage, or unavailable.
2. Attempt the documented Agent-Reach gateway first for public YouTube transcripts. Respect login/rate-limit restrictions. Use user-provided video/transcripts, chapter data and authorized readers as available. Do not imply that a transcript is the same as watching the editing or hearing the voice.
3. Save real source moments: timecodes *only if observed in actual caption timestamps or directly inspected video*, otherwise truthful paragraph/line IDs. Record exactly which parts were available. Titles/description snippets alone are insufficient to infer the source's content or pacing; report **BLOCKED** if no substantive content can be accessed.
4. Independently fact-check every substantive claim and any proposed personal application; find limitations and counterexamples. A video creator's statement is evidence of *what they said*, not evidence it is true.
5. Public comments, reviews, view counts, likes, upload dates, subscribers and analytics must be marked **observed** only if actually retrieved, linked and dated. Avoid invented viewers, inferred CTR, engagement percentages, average view duration, RPM, click-through improvement, audience demographics or causes of virality.

## Required analysis lenses

A. **What people might find interesting** (separate, mandatory): list specific moments with a *concrete detail* (surprise, paradox, emotional stake, personal recognition, visual transformation, unresolved decision, stakes, myth correction), a reason the *target audience* might find it interesting, a genuine source locator and the uncertainty. Avoid "people love X" without supporting observations.

B. **Hook mechanics:** identify the **curiosity gap**, opening contrast/problem, expectation violation, concrete visual, answer being withheld, honest stakes, and time-to-first-proof. Suggest **at least three original hooks** that can actually be satisfied by the evidence and visual plan. Each hook has the promise, the proof needed, and a fallback when the evidence is weak. The opening 3 seconds and first 15 seconds need specific storyboard actions, not empty hype.

C. **Why it matters now and why finish:** relevance to the viewer, real-world consequences, cost of misunderstanding, practical decision improved, and the exact payoff to deliver. "Why now" can explicitly be "evergreen/no timely claim"; never manufacture urgency.

D. **Learning and useful knowledge:** target before→after mental model, 2–5 concrete learning outcomes, prerequisite concepts, misconceptions corrected, which facts are established vs contested, and what *cannot* yet be concluded. Each promised lesson is connected to source evidence and an independently checked explanation.

E. **Daily-life application:** for each usable lesson include **who**, **when** in their life/work/study, an achievable **action**, what they should observe/learn from applying it, boundaries or safety limits, and one practical example (could be school, productivity, decision making, business or ordinary life). Do not fake applicability for purely historical/technical material: sometimes the takeaway is a better way to reason, not a behavioral instruction.

F. **Attention, confusion and payoff map:** identify likely boring/confusing segments and explain how to restructure them; specify fresh information every narrative beat; one concrete proof/demo early; finish by resolving the promise; build 1–3 retention-friendly rehooks only where they reveal real new substance. Mark all retention predictions as editorial guesses without measured viewer analytics.

G. **Viewer objections and originality:** identify what skeptics would question, what could be oversold, the counterexample, and the unique explanation/experiment/visual the original FounderNotes version adds.

## Extra mode: competitor analysis (explicit request only)

Use the same lenses **plus** observed hook/title/thumbnail promise, first 30–60 s structure, beat pacing, reveal/payoff pattern, explanation density, visual/sound choices *only when the actual material was inspected*. Contrast competitors' **observable approaches**, strengths and missed explanations with an original differentiation idea. When data allow, include real publication dates, video age, view counts and channel baselines to contextualize public performance; if not, mark these **unavailable**. Do not infer retention, CTR, demographics, audience psychology or causal reasons for view counts. Never present a single competitor video as a representative sample of a niche.

For comparisons, choose explicit peer criteria (topic, age, format, available baseline); clearly flag unmatched comparisons. Do **not** auto-fetch or silently inspect competitor videos without an explicit owner request.

## Handoff and deliverables

- The source-mode report is `studio-output/<slug>/research/viewer-value.json` and a readable `viewer-value.md`. For explicit competitor analysis, use `competitor-viewer-value.json` and `competitor-viewer-value.md`. Keep files separate to ensure competitor mode cannot silently pollute source analysis.
- The included original agent `.claude/agents/studio-viewer-analyst.md` requests **Opus medium** under task-based model routing. Researcher obtains real source evidence, analyst builds the interpretation and hook options, scriptwriter chooses a truthful promise, reality checker audits accuracy, and packager tests the promise vs the actual final film. The eight existing core production specialists remain intact.
- Use the `assets/viewer-value.example.json` as a format example **only**; it is fictional and must not be cited as video research.
- The standard-library `scripts/viewer_value.py` verifies the JSON and writes Markdown; it **does not autonomously watch videos, measure viewer reactions, write an AI opinion or replace source verification**.

Example:
```bash
python3 .claude/skills/podcast-scout-skill/scripts/viewer_value.py \
  studio-output/pilot/research/viewer-value.json \
  --out studio-output/pilot/research/viewer-value.md
```

Competitor mode requires a request-specific second confirmation at the CLI:
```bash
python3 .claude/skills/podcast-scout-skill/scripts/viewer_value.py \
  studio-output/pilot/research/competitor-viewer-value.json \
  --competitor-requested \
  --out studio-output/pilot/research/competitor-viewer-value.md
```

The validation contract requires (i) substantive accessed source, (ii) source-grounded **viewer_interest** moments, (iii) explicit evidence/caveats, (iv) true learning-to-application connections, (v) distinct original hooks, and (vi) no competitor fields without explicit mode and flag. Validation passing only proves the report's **structure**, not that its reasoning, media review or claims are accurate. The researcher/reality checker must examine evidence and sign off separately.

## Gate before script, gate before publishing

- **Gate V (viewer value):** can a target viewer quickly understand a *specific* interesting question, personal stake, truthful promise, testable learning payoff and concrete use or intellectual benefit? Are all source locators real and access limitations disclosed? Has the analyst considered boring or confusing moments and falsifiable viewer objections?
- **Gate F (fact lock):** verify every claim and application. The scriptwriter must map chosen hooks and promised lessons into actual script beats and a last-minute payoff check. Reject empty clickbait or a promise that the film never fulfils.
- **Gate P (package):** title, thumbnail, intro and description must promise the **same supported lesson** the final video delivers. No "this will go viral" guarantees.

No paid data access, credential collection, copying other videos or automatic YouTube publishing.

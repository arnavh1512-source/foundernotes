# Mandatory Viewer-First Production Rule — FounderNotes

**Status: NON-NEGOTIABLE for every NEW video, including source-video adaptations and original topics.** This is a production gate, not merely advice. No script draft, animation assignment, narrator generation, long-form render, or publishing package is approved by bypassing it. The only exception is a request to **analyze material only** rather than produce a video; that request ends with the analysis.

## One sentence comes before the script

**Complete this sentence with a specific, recognizable situation and a truthful benefit:**

> “This video is for someone struggling with ___; they’ll understand ___ and leave knowing how to ___.”

- Say **who** that person is, the problem they recognize in daily life, why it matters now (or why it is evergreen), exactly **what changes in their understanding**, and what they will **know how to do or reason about**.
- For a topic with no direct behavioral prescription, “how to” may mean how to spot a false assumption, compare alternatives, understand a mechanism, or make a more informed decision. Do not invent self-help actions.
- If the sentence cannot be completed **without vague words** such as “be inspired”, “unlock secrets”, “change your life” or “gain insights”, the topic is not ready. Research/rescope before writing; don't invent urgency or audience demand.

## Preparation order (MANDATORY, do not reverse)

| Order | Establish | Gate acceptance |
| --- | --- | --- |
| **1. Viewer need** | Target viewer, frustrating problem, reason to care now | A **recognizable daily-life situation** is explicit |
| **2. Learning promise** | Exactly what they will understand or do differently | An **honest, useful, specific** completed viewer-promise sentence |
| **3. Evidence and angle** | Independently checked claims, limitations, fresh angle and *what people might find interesting* | Real evidence locators, **two specific curiosity/interest details**, a fresh explanation, no recycled advice |
| **4. Opening** | Recognition and curiosity in the first 15–30 seconds | Concrete opening action and **an insight delivered by 30 seconds**—not a tease alone |
| **5. Learning progression** | How every chapter develops the understanding | Each chapter has a **unique question, new insight and distinct payoff**; no rephrased filler |
| **6. Visual storytelling** | What appears as each point is explained | **Every scene earns its place** through a visible action or explanatory change; one coherent style and continuity |
| **7. Narration and sound** | Natural spoken flow, emphasis and transition comfort | Listener-friendly words, deliberately paced emphasis, caveats alongside claims, no unpleasant robotic or rushed delivery |
| **8. Pilot** | Real 60–90-second test of the entire choice set | **Watch and review the rendered pilot** before producing the full video; outsiders must understand, want the answer **and already learn something** |

The rule applies regardless of animation engine, imported video, narrator casting, model tier or style catalog. It must not be softened for time pressure or length quotas.

### Specific vetoes

- **Audience first:** Never introduce fictional characters before the viewer understands the problem. Character dramatizations must explain the viewer's situation, not hijack the hook.
- **Value early:** Opening must **deliver one source-backed insight** as well as an honest curiosity gap.
- **Chapter payoff:** Repeating an earlier claim, generic motivational statements, or a longer paraphrase is **not a new chapter**.
- **Meaningful scenes:** Transitions show a new situation, mechanism, comparison or consequence—not random effects. Keep a coherent visual language.
- **Research honesty:** Present a claim's material qualification **next to the claim**, not buried at the end. Distinguish actual viewer observations from hypotheses.
- **Runtime earned:** The channel's existing **8:00+ full-length requirement still applies**, but **never add filler, invented examples or artificial pauses** to hit it. If the topic cannot support eight substantive minutes, **stop and deepen evidence or rescope the concept; do not approve a padded script**.
- **Originality:** For videos used as references, make an original explanatory treatment. **Competitor teardowns remain opt-in only**; supplying a source video does not authorize competitive analysis.

## Operational files and CLI gates

Fill a copy of `assets/viewer-first-plan.template.json` at:

`studio-output/<slug>/research/viewer-first-plan.json`

This template contains deliberate placeholders and **must FAIL** until all eight stages are prepared.

Before writing the script, run from the repo root:

```bash
python3 .claude/skills/podcast-scout-skill/scripts/viewer_first_gate.py \
  studio-output/<slug>/research/viewer-first-plan.json --stage pre-script
```

A **FAIL = no script draft or TTS**. Save the reasons and fix the preparation. The scriptwriter and producer must verify the evidence, not merely obey a green JSON schema.

After a real **60–90 second pilot** has been rendered, listened to, inspected and reviewed, fill `pilot.actual_review` with observed evidence, an actual measured duration, a reviewer, and independent judgments. Before moving to a long-form video:

```bash
python3 .claude/skills/podcast-scout-skill/scripts/viewer_first_gate.py \
  studio-output/<slug>/research/viewer-first-plan.json --stage full-production
```

A **FAIL = do not scale to full production**. Report the blocker, fix the pilot, and rerun.

**First pilot review question (mandatory):**

> “Would someone who knows nothing about our channel understand the problem, want the answer, and already have learned something?”

The three parts are individually required; no overall “looks fine” substitutes. A PASS from a structural test **does not prove** an outsider watched, that the claims are true, or that the hook works. Store honest inspection notes or review evidence and require human editorial judgment.

## Roles and handoffs

- **Researcher (Opus):** retrieve and verify evidence and actual source moments.
- **Viewer analyst (Opus):** discover what people might find interesting, the viewer problem, stakes, learning/application and truthful hooks. On source videos, perform the existing required `viewer-value-analysis.md` workflow. Competitor analysis **only when requested**.
- **Coordinator (Opus):** owns the viewer-first plan and runs the **pre-script** gate before delegating a script; owns the **full-production** gate after the pilot.
- **Scriptwriter (Opus):** refuses to script on failed/missing gate; uses promised learning and unique chapter payoffs, puts an insight in the first 30 seconds, avoids artificial runtime expansion. Complete an actual script and verify it realizes the plan; never just rely on its fields.
- **Visual director (Opus):** aligns every scene with a chapter's payoff and a meaningful visual change; shows the viewer problem before optional fictional characters.
- **Sound/editor (Sonnet):** produce a comfortable, natural, evidence-backed pilot with real synced audio and checked visuals; measure its duration and playback, not an estimate.
- **Reality checker (Opus):** independently challenges the promise, early insight, chapter redundancy, evidence, actual audio and pilot. Reject weak material even when the JSON validator passes.
- **Packager (Sonnet):** title/thumbnail/description promise exactly the delivered lesson, not a misleading curiosity gap.

The eight production-agent roles stay unchanged; the additional viewer analyst is a **pre-production specialist**, not an excuse to skip their gates. All roles use **Opus/Sonnet/Haiku only**. No automatic publishing.

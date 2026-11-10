# FounderNotes — task-based Claude model routing

Adapted from the **9 November 2026** Claude model-selection playbook by Addy Osmani supplied by the project owner. This is a **policy for Claude Code**, not a benchmark of this particular studio. Use **only Opus, Sonnet and Haiku**. No fourth model is available or permitted for this project.

## Default routing

| Assignment | Requested Claude Code alias | Effort | Reason |
| --- | --- | --- | --- |
| Main session / production coordinator | `opus` | `medium` | Story angle, scope, evidence gates, review budgets and consequential decisions |
| `studio-researcher` | `opus` | `medium` | Primary-source interpretation, conflicting evidence and ambiguity |
| `studio-scriptwriter` | `opus` | `medium` | Story architecture, argument quality, original narration and editorial trade-offs |
| `studio-visual-director` | `opus` | `medium` | Choosing a coherent visual language, shot logic and continuity |
| `studio-animator` | `sonnet` | `medium` | Implementing approved shot specifications in known engines |
| `studio-sound-engineer` | `sonnet` | `medium` | Voicebox casting and reproducible narration, alignment, SFX and mixing steps |
| `studio-editor` | `sonnet` | `medium` | Assembly and iterative repairs against objective audio/video QC |
| `studio-reality-checker` | `opus` | `medium` | Independent fact lock, rights review, high-stakes acceptance decisions |
| `studio-packager` | `sonnet` | `medium` | Working from locked facts to titles, metadata, thumbnail brief, chapters and distribution copy |
| `studio-source-indexer` (optional helper) | `haiku` | `medium` | Read-only extraction of candidate references and timestamps; never a fact-lock verdict |
| `studio-qc-log-reader` (optional helper) | `haiku` | `medium` | Read-only log extraction and test failure reporting; never a film QC verdict |

The original **eight production roles** are unchanged as roles. Two small helpers are opt-in and work under a core agent. Do **not** automatically spawn them when a task is small or has a sequential dependency.

## Escalation without changing model families

1. Give every task an explicit acceptance criterion and a way to **verify the result**: primary-source checks, real preview frames, timestamps, ASR, executable tests, or film/audio QC. Models do not substitute for evidence.
2. Start a scoped production job on **Sonnet medium**; if its real tests or artifacts fail, refine the specification and retry. For persistent complex implementation failures, try **Sonnet high**, then move a concise summary to **Opus medium**, and if needed **Opus high**. Use a higher effort setting for harder technical decisions before assuming that all failures require another model.
3. Start research judgment, script architecture, creative direction and independent fact/rights review on **Opus medium**, raising to **Opus high** for unusually complex, consequential, or contradictory material.
4. Use **Haiku only for reversible, easy-to-check indexing, routing and log-reading**. Its output is not evidence and cannot approve, publish, sign off, or alter the editorial truth.
5. The main coordinator selects the actual session model in the Claude Code UI/CLI. Agent frontmatter selects an **alias**, not a guaranteed version. If `opus`, `sonnet`, or `haiku` is unavailable, **report the limitation and obtain an approved fallback** instead of silently changing an agent's capabilities.
6. Track actual runtime `model`, effort, date, task duration, errors, test outputs and manual quality assessment in the handoff. The labels “Opus 5.5”, “Sonnet 5.5” and “Haiku 5.5” describe the **preferred** generation where available. They are not proof of the model that ran; check Claude Code `/model` and `/effort status` when possible.
7. Handoffs between models should be short and include: **task, constraints, paths, observed evidence, what failed, and the next decision**. Do not send 50 pages of raw logs or invent context continuity; preserve an audit trail of verified work.

## Creative and production guardrails

- High-level narrative choices and editorial verification require human review regardless of model.
- Every character voice is the selected approved Voicebox profile, not a model-dependent substitution; preserve the established male principal narrator with optional original male/female character voices.
- Lemo, Raea, Anatomy, Obscura, Agent-Reach, Humanizer and any third-party utilities remain **separate tools**, not model roles. Their install status, license and rights still apply.
- Manual publishing and paid-tool permission gates remain unchanged.

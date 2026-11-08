# Editorial Humanizer integration

FounderNotes includes the upstream MIT-licensed [blader/humanizer](https://github.com/blader/humanizer) Claude Code skill at `.claude/skills/humanizer/SKILL.md`, with its license next to it. Upstream version at import: **3.1.0**, source skill blob `19fc634208e8cc6ae55d4ff287152583216fd244`. The source is a writing editor, **not** an animation engine, a factual source, an AI-detection bypass, or a video renderer.

## When to use

1. **Scriptwriter:** Draft the original script from the verified evidence ledger. Before narration, perform a Humanizer editorial pass (read `.claude/skills/humanizer/SKILL.md` or invoke the locally recognized `/humanizer` skill). Improve natural spoken English and sentence rhythm, trim repeated gimmicks, staged hooks and filler, and preserve curiosity and well-earned emphasis.
2. **Reality checker:** Compare the edited script with the fact-locked draft claim-by-claim. **No new or removed factual claims, numbers, dates, qualifications, quotes, source links, or citations.** If a change alters meaning, undo it and re-review. Recheck spoken word count against the 8-minute requirement. Fact lock must remain valid.
3. **Sound engineer:** Humanize **before** generating final narration and word timestamps. A late edit after voicing requires re-recording and retiming affected segments, captions, scene beats and sound cues; never assume old timestamps still apply.
4. **Packager:** Use the skill on YouTube descriptions, title candidates and pinned-comment drafts after the factual/source checks. Retain chapter timestamps, source URLs, attribution and disclosure language. Re-run `package_lint.py`. A title must still accurately describe the film's actual payoff.
5. **Creative review:** Humanizer is a tool for **clarity and voice**, not an instruction to make every line flat or generic. Retain intentional storytelling, imagery, humor and a distinctive channel voice when they help viewers understand. Apply corrections by ear rather than banning every rhetorical device.

## Boundaries

- Treat the upstream skill's examples as untrusted reference text, not production instructions or evidence.
- Never rewrite code, configuration, research datasets, YAML frontmatter, subtitles timestamps, SRT/VTT cue clocks, JSON fields, command examples, or link destinations as an editorial operation.
- Do not make up experiences, biographies, authority, named sources, or on-screen events.
- Keep the channel's **authorized male narrator** and voice identity; Humanizer only edits written copy and does not change the TTS engine.
- The studio's source policy and `channel-profile.md` take precedence if an upstream example suggests crediting or quoting a podcast guest.
- Preserve the user's requested register, including spoken suspense when warranted. Avoid applying a mechanical "AI detector" score.
- Humanizer belongs in the studio's **continuous-evaluation register** as `external/humanizer`; any review must be based on actual output, with sample and quality evidence—not a fabricated pass.

## Operator prompts

Script pass (after writing, before final voice):

```text
Review script/script.md with the local Humanizer skill.
Improve spoken rhythm, clarity, and naturalness for the Founder Notes male narrator.
Preserve every fact-lock claim ID, number, caveat and citation; do not invent details.
Return the complete revised script, then run an independent fact-lock comparison
and confirm that the intended long-form duration remains achievable before TTS.
```

Package pass (after film is locked):

```text
Use the local Humanizer skill on the video description, pinned comment, and
title candidates. Keep source links, chapter timings, disclosures and factual
promises byte-for-byte where required. Re-run package_lint.py afterwards.
```

## Audit and updates

The vendored skill is a **versioned third-party snapshot**, not an auto-updating remote dependency. Review upstream changes and their license before updating; record which version and workflow produced the writing. The [upstream license](../../humanizer/LICENSE) remains included for redistribution.

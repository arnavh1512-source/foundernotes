# Agent-Reach: preferred optional research adapter

Upstream: https://github.com/Panniantong/Agent-Reach (MIT). Agent-Reach is a **platform and transcript retrieval adapter**, not an animation engine or a direct replacement for Obscura's browser API. It is **not bundled or automatically installed** by FounderNotes.

## Safe workflow
1. Check whether `agent-reach` exists in the actual execution environment. If absent, use the host's web/search/transcript tools and record the fallback; do not invent retrieved content.
2. If available, inspect `agent-reach channels` and the current channel's documented capabilities before use. Supported platforms and login requirements can change.
3. Prefer public, official sources for factual verification, with independent corroboration and source dates. For YouTube use legitimately accessible metadata/transcripts; never infer speech content from titles.
4. For authenticated platforms obtain **explicit account-owner authorization**. Do not copy browser sessions, login state, API keys, or private platform content without consent. Do not attempt to bypass authentication, paywalls or platform restrictions.
5. Capture source URL, title, publication date, retrieval method, transcript timestamp range and access limitations in the research ledger. Only mark a claim verified if actually read.
6. Agent-Reach may require network access, local tools, or optional keys; do not promise that every channel works. If a connector fails, record its error and continue with compliant alternatives.

## Migration note
The legacy Obscura binary installer, browser wrapper and their tests currently remain in the tree for compatibility and provenance. They are **not the primary research path**. Do not run them automatically or delete working code without a tested replacement. The production stack and crew docs point here instead.

## Validation gate
Before describing Agent-Reach as integrated, run a local doctor/channel availability check, read one public page and one permitted transcript with correct provenance, test failures and timeouts, and document the actual tool/version. No live end-to-end tests are claimed in this document.

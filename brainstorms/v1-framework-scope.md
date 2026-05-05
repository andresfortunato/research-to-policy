# super-claudio-research v1 — Brainstorming Summary

## Problem

Bootstrap a Claude Code framework for applied economics / policy research at Harvard's Growth Lab. Pilot with the Córdoba (close-out Aug 2026) and Cambodia (close-out Sept 2026) engagements, sharing publicly with the broader Lab and the open-source community. Existing academic-economics frameworks (MixtapeTools, Sant'Anna brothers, Blattman, paulgp) are structurally absent for applied development research: messy admin/trade data, diagnostic mode (no estimand), policy-memo register, multi-author multi-country teams, deliverable bundles. The framework must adapt scc's planning/handoff discipline to policy research, add verification guardrails that scale with stakes (not always-fire), accept Python and R as first-class, and seed long-lived institutional memory across engagements.

## Decisions Made

- **Audience scope (T1):** all three (pilot teams, broader Lab, open-source) — but built and iterated publicly with the two pilot engagements as the proving ground.
- **Default register (T2):** markdown-first. R/Python skills load on demand. LaTeX/Beamer support deferred to a later add-on package borrowed from Pedro/Hugo.
- **Languages (T2 / "3"):** language-agnostic at the core, with Python and R as the two first-class targets for v1. Stata can come later.
- **Hard gates vs nudges (T3):** mostly nudges + user-invoked checks. Only the manifest entry (every analytical run logs to a manifest) is non-negotiable. Verification by skill or selective subagent, not by always-fire hook.
- **Verification stack (T3 + T6):** combine four primitives —
  1. Conditional Stop hooks (silent-by-default, current `insights-logging` pattern) for discipline nudges
  2. Manifest + reproducibility logging (silent hook, ~100 tokens/run)
  3. **`/verify` skill** (user-invoked, per-artifact, lightweight) — built with `skill-creator`
  4. **`/deliverable-review` skill** (forked parallel subagents, ~10k tokens, deliverables only) — built with `skill-creator`, the Pedro `seven-pass-review` pattern adapted for policy outputs
- **Handoff time scales (T4):** all three named explicitly — within-session, researcher↔researcher mid-engagement, project→follow-up years later. The wiki layer addresses the longest scale; existing scc-style handoff.md addresses the shortest.
- **Bundle vs single artifact (T5):** policy work produces multiple artifacts (memo + deck + dataset + briefing). v1 ships *components* that compose, no orchestration layer yet — coordination and hierarchy figured out later from real use.
- **Wiki layer:** yes, 100%. Adopt the Karpathy three-layer pattern (`raw/` immutable + `wiki/` LLM-owned + `CLAUDE.md` schema), with `wiki/index.md` and `wiki/log.md` as non-negotiable navigation surfaces.
- **Summary discipline:** page-type budgets (source ≤300 words, concept ≤800, entity ≤600), relevance-by-frontmatter, periodic compression via lint pass.
- **Cleanup agent:** keep, adapted for research. Identify orphan scripts, intermediate CSVs, unused charts. Produces a proposal; researcher signs off; runs at phase close-out, not continuously.
- **Deliverable profiles:** start small (a few profiles, not comprehensive). Add as engagements surface needs. No upfront orchestration.
- **Existing repo philosophy preserved:** silent-by-default hooks, conditional-not-always-fire, composable conventions, project-shared `.claude/`, short CLAUDE.md with pointers.

## Patterns Adopted from Studied Repos

- **From scc (super-claudio-code):** install.js + CLI scaffolding model, session-start hook, pre-compact hook, brainstorming/planning/implementation/learning-capture skills (research-adapted), archivist agent (research-adapted).
- **From Pedro Sant'Anna (`claude-code-my-workflow`):** `pre-compact.py` + `post-compact-restore.py` hooks; path-scoped rules with YAML frontmatter; `quality_reports/{plans,specs,decisions,session_logs}/` directory; the seven-pass-review parallel-fork pattern.
- **From Hugo Sant'Anna (`clo-author`):** worker-critic pairing with strict separation (critics may not write); decision records (Decision/Alternatives/Why-rejected/What-would-invalidate); phase-based severity gradient.
- **From Hugo (`obsidian-vault-manager`):** WIP-limited multi-project dashboard concept (deferred but noted) for researchers juggling multiple country engagements.
- **From Cunningham (`MixtapeTools`):** per-entry parallel subagent fan-out (the bibcheck pattern, generalized to per-claim memo verification); cross-language replication mindset.
- **From Blattman (`claudeblattman`):** non-coder accommodation (markdown-first); SESSION_LOG append-only discipline; `council` parallel-critique pattern.
- **From Karpathy gist:** the entire three-layer wiki / three-operations / two-special-files architecture.
- **From Imbad's `academic-research-skills`:** mode-registry / cross-skill advisor concept (deferred but noted) — solves "which entry point do I use?" once skill count grows.
- **From shanraisshan:** "skills are folders not files," "descriptions are triggers not summaries," CLAUDE.md kept short, `.claude/rules/` glob-scoped lazy-load.

## Patterns Explicitly Rejected for v1

- Journal-targeting + ≥95 submission gate (Hugo) — irrelevant; replaced by deliverable profiles.
- Single-artifact pipeline (Pedro/Hugo) — replaced by composable components, no orchestrator.
- TDD vocabulary (scc) — reframed as "specification-driven analysis."
- Always-fire verification hooks — only conditional or user-invoked.
- Three-strikes-escalate-to-User (Hugo) — escalate to team channel/researcher review.
- Bilingual triggers, badge systems (Imbad, shanraisshan).
- LaTeX/Beamer infrastructure (deferred).
- Mandatory N-stage pipelines.
- Coordination/orchestration layer between deliverables (deferred until pattern emerges).

## Research Findings (key sources)

- **Proposal (Fortunato 2026)** — pilot context: Córdoba/Cambodia engagements, Anthropic Team plan, public-goods commitment, three responsible-use principles (researcher accountability, reproducibility, third pillar implied).
- **Zhang et al. 2026 (AAAI)** — AI-generated code dependency drift kills reproducibility. Justifies the manifest layer as non-negotiable.
- **Karpathy gist (2024)** — the LLM Wiki pattern. Three layers, three operations, two special files. Verbatim spec retrieved.
- **Sant'Anna ecosystem** — ~15 research groups have forked Pedro's template as of March 2026; the `seven-pass-review` parallel-fork is the highest-leverage import.
- **Existing super-claudio-research** — already has `.claude/conventions/insights-logging.md` + Stop hook + design philosophy. v1 builds on this, doesn't replace it.

## Open Questions for Planning

- **Install model:** scc-style CLI (`scc-research init`) vs. existing copy-from-template install.sh. Pick one and commit.
- **Wiki location:** `wiki/` at project root vs. nested. Whose markdown editor support matters?
- **Manifest format:** plain CSV vs. JSON-Lines vs. SQLite. Trade simplicity vs queryability.
- **Where do plans live:** `plan/plan-<name>/` (scc style) vs. `quality_reports/plans/` (Pedro style) vs. simpler. Pick one.
- **Skill naming for the two new ones:** `/verify` and `/deliverable-review` — confirmed names? Or different?
- **Initial deliverable profiles:** which 2-3 to ship in v1 (likely: country-diagnostic-memo, ministerial-briefing, internal-research-memo)?
- **Initial conventions to add beyond `insights-logging`:** the README roadmap lists 6 (`handoff-format`, `evidence-ledger`, `chart-registry`, `reproducibility-check`, `citation-discipline`, `plan-structure`) — which subset is v1?

## Constraints Identified

- **Pilot timeline:** v1 must be useful to Córdoba team by mid-May 2026 workshop. Cambodia engagement runs through end-Sept 2026.
- **Audience heterogeneity:** within Growth Lab, fluency spans deep-coder to non-coder. Markdown-first default protects the floor; skills/components serve the ceiling.
- **Public-goods commitment:** open-source from day one. Forces clean separation of project-specific config (gitignored) from framework (committed).
- **Existing philosophy:** "silent by default, conditional not always-fire, composable not monolithic, project-shared not user-personal." This is the design constitution; new additions must conform.
- **Budget for verification cost:** routine work tolerates ~100 tokens of overhead; deliverable review tolerates ~10k. Anything in between is suspect.
- **Reproducibility imperative:** Zhang et al. cited explicitly in proposal — manifest + dependency capture is non-negotiable, not a v2 nice-to-have.

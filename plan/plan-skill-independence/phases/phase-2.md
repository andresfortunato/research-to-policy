# Phase 2 — Vendor + adapt `implementation` skill

Read `plan.md` for the goal, constraints, decisions, file manifest, and repo context. This file scopes Phase 2.

## Intent

Copy `~/github/super-claudio-code/skills/implementation/{SKILL.md, references/escalation-reference.md}` into `.claude/skills/implementation/`, adapt language and cross-references to research. Same surgical-not-architectural adaptation philosophy as Phase 1. The escalation-reference is the heavier lift — software-shaped escalation triggers need research-domain rewrites, but the structure (severity tiers, escalate-vs-handle test, examples format) stays.

## Files

- ✚ `.claude/skills/implementation/SKILL.md`
- ✚ `.claude/skills/implementation/references/escalation-reference.md`

## Adaptations — SKILL.md

### Mechanical swaps

- Path swaps:
  - `.scc/learnings/` → `learnings/` (r2p puts learnings at project root, per `learning-capture.md`).
  - `.scc/status/plan-[name].md` → drop the line entirely. r2p's per-plan `handoff.md` is the source of truth for session state; no sidecar status file.
- Drop `tdd` skill cross-reference; replace with `/verify` (per-artifact sanity check) cross-reference.
- Drop "framework's context-monitor hook" reference. Replace with a one-line mention of r2p's `precompact-handoff.sh` as the compaction-nudge analog.
- "Active plans" and "Latest handoff" bash blocks at the top of the skill: keep verbatim. Both already use `plan/plan-*/` glob and `handoff.md` filename — domain-neutral.
- Plan Completion subagents: scc lists two — `archivist` and `cleanup`. Drop `cleanup`; only the archivist remains. Update the boilerplate to match r2p's Phase-5 protocol:
  - Tripwire 1 of `check-insights.sh` is BLOCKING.
  - The hook writes a `.archival-triggered` sentinel for loop-protection.
  - The archivist synthesizes `archive/plan-<slug>.md` (60–150 lines), appends to `archive/index.md`, optionally edits `CLAUDE.md`, deletes the plan directory.
  - Cross-reference `docs/plan-archival-mechanism.md` and `.claude/agents/archivist.md`.

### Domain-shaped rewrites

- "Code is ground truth" → "**The artifact is ground truth.** The plan captures the analysis intent; what landed in `output/` (charts, tables, .meta.json) and `insights/` (evidence-based findings) is reality. When they diverge, the artifact wins for what was actually measured; the plan wins for intent and constraints. The plan tells you *which* artifacts and *why* — the artifact tells you *what the data actually showed*."
- "Verify with evidence" — verification defaults rewrite: "does it build? do existing tests still pass?" → "does the script run end-to-end with the same seed? does the chart re-render byte-identical (or sign-and-magnitude-identical, depending on stochastic content)? do diagnostic counts in `methods/<slug>/rule.md` still match the rule? do downstream insights still cite the artifact correctly?"
- Default verification language: "passing build / passing test / visual confirmation" → "script runs end-to-end / sign-of-coefficients hold / source citation present / numbers reconcile."
- "Parallelization" section: instructions for teammate output write to `plan/plan-[name]/output/[task-name]/` → `plan/plan-[name]/scratch/[task-name]/`. The rationale (output is temporary; cleaned up at archival) stays. Add a sentence: "`scratch/` not `output/` — research projects use `output/` for analytical artifacts (charts, tables); a parallel-team output directory inside the plan must not collide with that."
- "Record what didn't work" — "this library silently swallows errors" example reframed as research-shaped: "PONDII didn't exist in 2014 EPH waves" or "the survey vintage break in 2018Q3 invalidates pre-2018Q3 wage comparisons without a deflator-chain adjustment".

### Cross-references to add

- "Verify with evidence" → cross-link `/verify` skill (per-artifact, ≤2k tokens) and `/deliverable-review` (last-mile, ≤12k tokens, seven-lens).
- "Record what didn't work" — "where it goes" bullets: `learnings/<slug>.md` for project-wide gotchas (cross-link `learning-capture.md`); `plan/plan-[name]/handoff.md` for tactical session-state; `plan/plan-[name]/log.md` for direction-changes within the plan.
- "Plan Completion" — cross-link `docs/plan-archival-mechanism.md` and `.claude/agents/archivist.md`.

## Adaptations — references/escalation-reference.md

This is the heavy lift. Read scc's full file once. The structure (severity tiers, the escalate-vs-handle test, example format) stays; the escalation triggers themselves get researched-domain rewrites. Suggested replacements:

| scc trigger (software) | r2p trigger (research) |
|---|---|
| Architectural decision needed (new abstraction, new dependency layer) | Methodology call surfaces mid-flight (deflator unexpectedly relevant; identification strategy invalidated by data shape) |
| Integration seam contradiction (new code can't connect to existing X) | Data-source seam contradiction (a regressor's vintage coverage doesn't match the analysis window; a survey break invalidates a pre-period control) |
| Tests/build broken (existing test suite fails) | Reconciliation broken (diagnostic counts in `methods/<slug>/rule.md` diverge from rule; chart re-renders with different sign or magnitude than prior insight cited) |
| Unfamiliar dependency (a library Claude doesn't know) | Unfamiliar `methods/<slug>/rule.md` or `decisions/<date>_<slug>.md` that the plan didn't account for |
| Sample restriction unexpectedly removes >X% of observations | (research-only; no scc analog) |
| Data quality issue: missingness pattern, outliers, top-coding | (research-only; no scc analog) |

Keep the escalate-vs-handle test verbatim ("would the user want to make this decision themselves, or would they say 'just handle it'?"). Keep severity guidance and example format.

The two research-only triggers (sample-restriction surprise, data-quality surprise) are additions — scc doesn't have analogs because they're research-domain failure modes. Worth adding because they're high-frequency in applied research.

## Verification

- `wc -l SKILL.md` ≈ 165 ± 20.
- Frontmatter `description:` mentions research workflow and `.completed`-driven archival explicitly.
- `grep -E "\.scc/|tdd skill|context-monitor hook|cleanup subagent|cleanup agent"` → 0 matches in SKILL.md.
- Plan Completion section explicitly names the archivist as the **only** post-`.completed` agent (no cleanup subagent reference).
- Symlink: fresh scratch project + `r2p init` → `~/.claude/skills/implementation/` → `<r2p-repo>/.claude/skills/implementation/`.
- Active-plans / latest-handoff bash blocks at the top still execute unmodified (smoke-test in scratch).
- `escalation-reference.md` examples are research-domain (no JSX, no test runners, no architectural-pattern jargon). At least 5 research-shaped triggers; sample-restriction and data-quality additions present.
- Path-swap audit: `grep "\.scc/"` against the new SKILL.md and references file → 0 matches.
- Teammate output dir: `grep -n "output/\[task-name\]\|scratch/\[task-name\]"` → matches go to `scratch/`, not `output/`.

## Dependencies

Upstream: Phase 1 (planning skill exists; cross-references to it are valid; adaptation choices established).
Downstream: Phase 3 (agent-teams cross-refs implementation; README updates depend on both skills shipped).

# Skill Independence — Brainstorming Summary

## Problem

r2p's v1.1 README (just shipped in plan-cordoba-lessons Phase 6) prominently features `/planning` and `/implementation` in the workflow narrative, the worked-example quickstart, and the skills table. But those two skills aren't bundled with r2p — they ship with super-claudio-code. A researcher who runs `npm install -g research-to-policy` + `r2p init` today gets brainstorming, learning-capture, verify, deliverable-review, etc., but the workflow breaks the moment they invoke `/planning`.

The cordoba-lessons plan.md decided to "rely on scc's planning skill — installed globally" and treat any research-adapted version as a v1.2 question. We're now reversing that decision: distribution requires standalone install. Vendor the missing skills + adapt them to applied research.

## Decisions Made

- **Vendor `planning`, `implementation`, and `agent-teams` from scc.** The first two are core-workflow; agent-teams is cross-referenced by implementation for parallelization (research has natural parallels — comparing identification strategies, running robustness checks). Drop dependence on scc entirely.
- **Don't vendor `tdd`.** Research has no TDD analog. Replace TDD cross-references with `/verify` (per-artifact sanity check, r2p's existing skill).
- **Don't vendor a `cleanup` subagent.** Phase 5 settled the boundary: archivist (per-plan, automated) + `/research-cleanup` (project-wide, user-invoked). The cleanup-subagent reference in scc's implementation skill's Plan Completion gets dropped, not ported.
- **Skill names unchanged: `planning`, `implementation`, `agent-teams`.** r2p's brainstorming skill (already shipped in Phase 3 of cordoba-lessons) triggers "the planning skill" by name — `brainstorm-format.md` explicitly says "agnostic about whose". Renaming would force chasing references in already-shipped r2p skills. Last-installer-wins for users with both scc and r2p installed; document the precedence in README.
- **Project-identity check reads `CLAUDE.md`, not `.scc/status/project.md`.** r2p's `CLAUDE.md` is already the convention-pointer + project-orientation file (seeded by `r2p init`). No new hidden directory.
- **Drop `.scc/status/plan-[name].md`.** r2p's per-plan `handoff.md` is the source of truth for session state. No new hidden status directory.
- **Drop the framework's `context-monitor` hook cross-reference.** scc-specific. r2p has `precompact-handoff.sh` for compaction nudges; that's the analog and it's already wired.
- **Add `r2p plan init <slug>` CLI subcommand.** Parity with `scc plan init`. Small lift (one new lib file + one cli.js wire-up); the planning skill instructs users to run it.
- **Teammate output dir: `plan/plan-<slug>/scratch/`, not `output/`.** scc's implementation skill instructs parallel agents to write to `plan/plan-[name]/output/[task-name]/`. Research projects use `output/` for analytical artifacts (charts, tables, .meta.json) — name collision. Rename the parallel-agent dir to `scratch/`.
- **Verification language is domain-shaped throughout.** "Build passes / tests pass / visual confirmation" → "script runs end-to-end / sign-of-coefficients hold / chart re-renders / source citation present / numbers reconcile to prior insight." `plan-structure-mechanism.md` already names this principle; the vendored skills must match.
- **Examples are research-shaped throughout.** WebsiteLayout / App.tsx / i18n provider → methods/cpi-deflator/rule.md, output/06_chart.png, decisions/2026-05-08_identification-strategy.md.

## Research Findings

- **scc planning skill** (`~/github/super-claudio-code/skills/planning/SKILL.md`, 154 lines): mostly domain-neutral. SE-specific: TDD cross-ref, `WebsiteLayout`/`App.tsx`/`i18n` examples, `scc plan init` command, `.scc/status/project.md` identity check, behavioral test lists language.
- **scc implementation skill** (`~/github/super-claudio-code/skills/implementation/SKILL.md`, 169 lines): mostly domain-neutral. SE-specific: TDD cross-ref, "code is ground truth" framing, build/test verification defaults, cleanup-agent in Plan Completion, `.scc/learnings/` and `.scc/status/` paths, framework's-context-monitor-hook reference, `output/[task-name]/` for parallel teammates.
- **scc agent-teams**: not yet read; will adapt during Phase 3.
- **References files**: `planning/references/multi-session.md` (light adaptation expected — generic session-scoping concerns) and `implementation/references/escalation-reference.md` (heavy adaptation expected — software-shaped escalation triggers need full rewrite).

## Open Questions

- None blocking — the design is settled. Implementation will surface adaptation calls per-skill (per-paragraph, often), but those are tactical decisions that don't need brainstorming pre-resolution.

## Constraints Identified

- **Don't break the workflow narrative just shipped.** README Phase 6 names `/planning` and `/implementation`; the vendored versions must keep those names so the worked-example quickstart stays valid.
- **Don't redesign scc's skills.** Their bones (intent over implementation, decisions as records, verify with evidence, escalation triggers, phase-level execution) are domain-neutral and load-bearing. We adapt language and cross-references; we do not re-architect.
- **Don't break scc-resident users.** A user with both r2p and scc installed will have whichever installed last winning the symlink. Document in README so the precedence is explicit.
- **Maintain the brainstorm → planning handoff contract.** `brainstorm-format.md` says "the brainstorming skill triggers the planning skill by name". The vendored planning skill must preserve the contract: read `brainstorms/<topic>.md`, incorporate Decisions Made into plan.md, don't re-debate.
- **No new hooks.** This plan is skills + one CLI command. If any vendored skill references scc-side hooks, drop the reference rather than porting.
- **Cordoba-lessons archival deferred until skill-independence ships.** The `.completed` marker is removed at this plan's start and re-touched after Phase 3 commits; cordoba-lessons archives last so the archivist has the full v1.1+ surface to describe.

## Decision records to file

None. These are framework-development calls, not domain methodology calls. The brainstorm + plan are the citable form; no `decisions/<date>_<slug>.md` graduation needed.

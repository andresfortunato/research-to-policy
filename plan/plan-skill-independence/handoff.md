# Handoff: plan-skill-independence

**Status:** ACTIVE — plan setup complete; Phase 1 next (fresh session).
**Date:** 2026-05-08
**Last commit on plan branch:** to be set when this commit lands.

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Vendor + adapt `planning` | ⏭ next | Single SKILL.md + multi-session.md; surgical adaptation. |
| 2 | Vendor + adapt `implementation` | pending | Heavier — escalation-reference.md needs research-domain trigger rewrite. |
| 3 | Vendor + adapt `agent-teams` + ship `scr plan init` + README pass | pending | Last phase; re-touches cordoba-lessons `.completed` at the end. |

## Where we are

Plan setup committed: `brainstorms/skill-independence.md`, `plan/plan-skill-independence/{plan.md, phases/phase-{1,2,3}.md, handoff.md}`. cordoba-lessons `.completed` marker was removed at this plan's start so the archivist doesn't fire on an unrelated plan mid-flight; Phase 3 re-touches it as its final action.

## What's next

**Phase 1 — Vendor + adapt `planning` skill.** Read `phases/phase-1.md`. Source: `~/github/super-claudio-code/skills/planning/{SKILL.md, references/multi-session.md}`. Surgical adaptation — preserve scc's bones, swap language and cross-references. `installGlobals()` already walks `.claude/skills/`, so dropping the new skill into the directory is enough for symlinking.

## Implementation hints

- Read the scc skill in full before adapting (≤155 lines; cheap).
- Do mechanical swaps first (path + cross-ref), then domain rewrites (verification language, examples), then verify. Same shape as Phase 5 of cordoba-lessons.
- Verification: `wc -l`, frontmatter, scc-residue grep, fresh-scratch symlink check.
- Phase 1's adaptations anchor Phases 2–3 — language choices (e.g., how the verification rewrite reads) cascade. Pick once, propagate.

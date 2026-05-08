# Handoff: plan-cordoba-lessons

**Status:** ACTIVE — plan written, awaiting review and Phase 1 kickoff.
**Date:** 2026-05-08
**Last commit on plan branch:** `a917b7d` — "Refresh handoff + fill hash trail (cc232fc)" (pre-plan; this plan not yet committed)

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Six small wins (script-header tweaks, web-scraping bundle, addendum pattern) | ⏭ next | Mechanical, isolated; ships first. |
| 2 | Theme-parallel opt-in (insights-logging + check-insights.sh + INDEX schema) | ⏭ queued | Schema change; ships before Phases 3–5 so they land theme-aware. |
| 3 | Brainstorming skill (port from scc, research-adapted) | ⏭ queued | Closes the methodology-essay-isn't-a-plan gap. |
| 4 | Learning-capture skill + retrieve-learnings.sh + precompact-handoff.sh | ⏭ queued | Three-bucket model: insights/decisions/learnings. |
| 5 | Plan archival (Stop hook extension + archivist agent + archive/) | ⏭ queued | Existing four .completed markers archived manually first. Archivist scope kept narrow — defers project-wide cleanup to `/research-cleanup`. |
| 6 | README rewrite for researcher audience | ⏭ queued | Quickstart → workflow → scaffolding → tools → what's in here → updates → design philosophy (last). Ships after all components exist. |

## Where we are

The cordoba audit (this conversation) surfaced framework gaps. They're
captured in this plan's "Decisions Made" — none re-debatable. Plan
written and saved at `plan/plan-cordoba-lessons/plan.md`. No code
landed yet. Awaiting user review of the plan before Phase 1 kicks off.

The plan is sized to v1.1 (6 phases, ~30 file changes plus a README
rewrite, all framework-internal, no pilot-project dependency). It
deliberately defers (a) chart-registry / citation-discipline /
evidence-ledger (already in TODO.md, want pilot feedback first)
and (b) any retrofit-onto-existing-projects workflow (separate
plan, post-v1.1).

## What's next

1. **User review** of `plan.md`. Surface any "this scope is wrong"
   pushback before scaffolding hooks. The single most contestable
   decision is Phase 5's reuse of `check-insights.sh` for the
   archival tripwire — alternative is a second Stop hook
   (`check-archival.sh`). Either works; one-hook-two-checks chosen
   here for hook-count discipline.
2. **Manual archival** of the four pre-existing `.completed` markers
   (plan-install-redesign, plan-project-conventions, plan-refdocs-conventions,
   plan-v1-framework) — done before Phase 5 ships, so the new Stop
   hook doesn't fire on legacy markers. Can be done as part of
   Phase 5 scope or as pre-Phase-5 housekeeping.
3. **Phase 1 kickoff** — script-header.md edits + web-scraping skill
   bundle + addendum pattern. Mirror `plan/plan-refdocs-conventions/`
   rhythm; verification log lands in this handoff after Phase 1
   commits.

## Surprises

- scr's CLI has only `init` (no `plan init` like scc) — plan dir
  scaffolded by hand. Worth noting: scc's planning skill assumes
  `scc plan init` exists. The brainstorming-skill port (Phase 3)
  must be agnostic about this — skill says "trigger the planning
  skill" without naming whose CLI scaffolds.
- The web-scraping skill is referenced by `source-registry.md`
  but not shipped — Phase 1 closes a real existing gap, not just
  a cordoba-flagged one.
- scc's three new hooks are JS; the framework constitution mandates
  bash. Three bash ports are the hidden cost of Phases 4 and 5.
  Sized in budget.

## What didn't work

- Initial framing had the theme-parallel question as a real fork
  ("opt-in vs theme-required"). User clarified: only opt-in is
  sensible; the question is purely about implementation cost.
  Plan reflects the simplified shape.
- Initial framing tried to bundle "improve framework" with
  "retrofit existing projects." User split them — this plan is
  the first; retrofit is a separate plan post-v1.1.

## Verification log

(Empty — no phases executed. Lands here as Phase 1 commits.)

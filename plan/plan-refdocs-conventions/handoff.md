# Handoff: refdocs-conventions

**Status:** ACTIVE — plan written, no execution yet
**Date:** 2026-05-06
**Last commit on plan branch:** `1587f4a` — "Fill in handoff hash trail (f26ff27)"

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Conventions + design rationale | ⏭ next | Two convention files, two mechanism docs, one edit to `audience-and-philosophy.md` |
| 2 | Templates + CLAUDE.md pointer blocks | ⏸ blocked on P1 | Examples must quote required-section lists from P1's conventions |
| 3 | Installer + framework-level docs | ⏸ blocked on P2 | `install.sh` mirrors what P2 puts in `templates/` |

## Where we are

Plan was authored from a comparison of `~/cambodia-growth/` (working
research project) against `super-claudio-research` (this framework).
The Cambodia repo's `data_sources/` (flat folder of API reference docs
with INDEX.md, status-and-anchor pattern) and
`methods/electronics_entry/cohort_rule.md` (operational methodology
with v1→v2 evolution and diagnostic counts) are the templates being
ported. Nothing has been built yet — this session only produced
`plan/plan-refdocs-conventions/{plan.md, handoff.md}` and the
unchanged scaffolded `log.md`. No source files in `.claude/`, `docs/`,
or `templates/` have been touched.

## What's next

1. **Phase 1** — Start with `.claude/conventions/data-sources.md` since
   methods reuses its "boundary with neighbors" framing. Reference
   `~/cambodia-growth/data_sources/INDEX.md` and `imf_sdmx_api.md` for
   the structure to mirror; reference
   `.claude/conventions/source-registry.md` for the in-framework prose
   style to match.
2. Then `.claude/conventions/methods.md`, modeled on
   `~/cambodia-growth/methods/electronics_entry/cohort_rule.md` (the
   seven required sections come straight from that file's headings).
3. Edit `docs/audience-and-philosophy.md` to add the cross-cutting
   "verified-as-of + headline anchor" principle once, then write
   `docs/data-sources-mechanism.md` and `docs/methods-mechanism.md`
   referencing it.

Reading order to start cold: this file → `plan.md` →
`.claude/conventions/source-registry.md` (closest in-framework analog
for prose style) → `~/cambodia-growth/data_sources/imf_sdmx_api.md`
(target structure to port).

## Surprises

- The framework's `templates/CLAUDE.md.template` already names
  `methods/` in the directory tree but ships zero scaffolding for it —
  a gap the plan closes. Worth noting in the README blurb that this
  is a backfill, not a net-new folder.
- `wiki/concepts/`, `decisions/`, and `methods/` all plausibly host
  methodology content; the boundary needs to be drawn explicitly in
  each new convention or future researchers will re-litigate. The
  plan's Decisions Made captures the carve-up; both convention files
  must restate it concisely.

## What didn't work

Nothing yet — no execution.

## Verification log

- `scc plan init refdocs-conventions` — scaffolded
  `plan/plan-refdocs-conventions/{plan.md, handoff.md, log.md,
  phases/, context/}` and `.scc/status/plan-refdocs-conventions.md`.
  Verified by `ls plan/plan-refdocs-conventions/`.
- Manual read of `~/cambodia-growth/CLAUDE.md`,
  `~/cambodia-growth/data_sources/INDEX.md`,
  `~/cambodia-growth/data_sources/imf_sdmx_api.md`,
  `~/cambodia-growth/methods/electronics_entry/cohort_rule.md` —
  confirms the patterns the plan is porting are in the shape the
  plan describes.

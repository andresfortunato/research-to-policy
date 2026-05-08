# Phase 2 — Theme-parallel opt-in

Read `plan.md` for the goal, constraints, decisions, file manifest,
and repo context that govern all phases. This file scopes Phase 2.

## Intent

Permit `insights/<theme>/NN_*.md` and `output/<theme>/NN_*` alongside
the flat layout. Update the convention prose, the `check-insights.sh`
glob, and the INDEX schema to accept both. No declaration file, no
enforcement — just permission. Ships second because it's the schema
change; landing it before Phases 3–5 means new conventions/skills/hooks
can reference the opt-in pattern in their docs without retrofit.

## Files

- `.claude/conventions/insights-logging.md` — add a "Theme-parallel
  layout (opt-in)" section: when a project has multiple parallel
  inquiries, organize as `insights/<theme>/NN_*.md`; numbering can
  be per-theme or global; INDEX gets an optional `theme` column.
  Flat layout stays default.
- `.claude/hooks/check-insights.sh` — extend tripwire glob to
  accept both `insights/[0-9]+_*.md` and `insights/*/[0-9]+_*.md`;
  extend artifact glob to accept `output/<theme>/0[0-9]*_*` paths.
- `templates/insights/INDEX.md` — add optional `theme` column to
  the example table; keep the no-theme example row first.
- `docs/theme-parallel-mechanism.md` (new) — rationale: why opt-in
  not required, why subfolder not declaration, what "theme" means
  operationally (a line of inquiry that has its own audience and
  its own deliverable target), why hooks accept both rather than
  forcing migration. cordoba's four-theme structure as the
  motivating diagnostic.
- `templates/CLAUDE.md.template` — pointer block for insights
  updated to mention the opt-in pattern; codebase-tree shows
  `insights/` with optional `<theme>/` annotation.
- `README.md` — one paragraph in "Conventions installed" about
  the opt-in pattern. (Tactical edit; full rewrite is Phase 6.)

## Verification

- `check-insights.sh` test: in a scratch dir with
  `output/spatial-equilibrium/01_chart.png` staged and no
  `insights/*.md` change, hook fires with the nudge naming the
  artifact.
- `check-insights.sh` test: same scratch dir but with
  `insights/spatial-equilibrium/01_*.md` staged — hook stays
  silent. Both flat and subfolder insights satisfy the tripwire.
- `insights-logging.md` opens with the existing rule (flat is
  default); the new section is clearly labeled "opt-in" and
  references the rationale doc.
- The INDEX schema accepts a theme column without breaking
  existing un-themed indexes (column is optional, sort by `NN`
  still works).

## Dependencies

Upstream: Phase 1 (no hard dep, but Phase 1 lands first by
sequencing).
Downstream: Phases 3, 4, 5 reference the opt-in pattern in their
docs. Schema change must be in place before they ship.

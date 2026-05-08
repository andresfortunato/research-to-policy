# Insights Logging — Protocol

**Trigger**: After any data-analysis session, phase, or implementation step
that produces evidence (charts, panels, comparisons, regressions, decompositions).

## Where insights live

- Per-doc file: `insights/NN_<short_slug>.md` (e.g. `insights/02_phase3b_bilateral_fdi.md`).
- Numbering is **sequential across the whole project**, regardless of plan/phase.
  Use `ls insights/ | sort` to find the next free `NN`.
- Index: `insights/INDEX.md` — one row per insight in a markdown table:
  `| NN | [Title](NN_slug.md) | YYYY-MM-DD | source |` (add a `theme`
  column if the project uses theme subfolders — see below).

## Theme-parallel layout (opt-in)

When a project carries multiple parallel lines of inquiry — each with
its own audience and its own deliverable target — flat numbering can
collide ("which theme is `07_` about?"). The opt-in alternative is
a one-level subfolder per theme:

```
insights/
├── INDEX.md
├── 01_overall_macro_priors.md          # cross-cutting; lives at top level
├── spatial-equilibrium/
│   ├── 01_amenity_gradient_buenos_aires.md
│   └── 02_within_metro_dispersion.md
└── labor-markets/
    └── 01_eph_panel_attrition.md
```

Rules:

- **Flat is the default.** Single-theme projects, or projects in early
  exploration, stay flat. Don't introduce subfolders preemptively.
- **Themes are free-form.** No `themes.md` declaration, no upfront
  enumeration. Use lowercase-snake-case (suggested, not enforced).
  Add a theme by creating its folder; retire one by emptying it.
- **Numbering can be per-theme or global.** Per-theme (`01_`, `02_`
  inside each subfolder) is usually less friction; pick one shape
  per project and stay consistent.
- **Cross-cutting insights stay flat.** When a finding spans themes,
  put it at `insights/NN_*.md` — don't force it into one theme's
  folder.
- **Hooks accept both shapes.** `check-insights.sh` globs flat and
  subfolder paths; you can adopt or migrate gradually without
  retrofitting.

Rationale and tradeoffs: `docs/theme-parallel-mechanism.md`.

## Required structure

```markdown
# <Title — concrete claim, not "Analysis of X">
**Date**: YYYY-MM-DD
**Source**: <plan/phase, notebook, or script that produced these>
**Data**: <datasets used — e.g. WB BX.KLT.DINV.WD.GD.ZS, output/06b_panel.csv>

## Insights
1. **<one-sentence claim>** — <specific number/comparison that proves it>. <Implication.>
2. ...

## Charts referenced
- `output/06c_fdi_at_entry.png` — supports insight 1, 2
- ...

## What this insight does NOT establish
- ... (scope honesty)
```

## What counts as a good insight

- A **specific number** or comparison the reader can cite
  (`Cambodia FDI/GDP = 9.6% in 2024 — above every sustainer's at-entry value except CZE 2001 (8.3%)`).
- Something **non-obvious**: surprising, contradicts a prior, or sharpens framing.
- **Evidence-bearing**: the chart/CSV/cell that supports it must be referenced.

## What doesn't count

- "We built a chart of X." (process, not insight)
- Generic stylized facts already in CLAUDE.md or prior insight docs.
- Anything without a number, percentile, or named comparison.

## How many

3–8 insights per doc. Fewer than 3 means the analysis wasn't deep enough;
more than 8 means padding. Be ruthlessly relevant.

## Discipline

- **One commit** updates `insights/NN_*.md` AND `insights/INDEX.md` together —
  the index is what makes the corpus searchable.
- **Never overwrite** a previous insight doc — append a new numbered one if a
  finding gets revised, and reference the prior doc in the new one.
- Insights persist across plans; they're a project-level asset, not a
  plan-level artifact.
- The insights doc is **distinct from the handoff** — handoff is tactical
  ("what's done, what's next"); insight is substantive ("what we learned
  from the data").

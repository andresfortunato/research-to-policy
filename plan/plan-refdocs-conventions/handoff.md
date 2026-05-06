# Handoff: refdocs-conventions

**Status:** ACTIVE — Phase 2 complete; Phase 3 next
**Date:** 2026-05-06
**Last commit on plan branch:** *(this commit, fill in)* — "Phase 2: templates + CLAUDE.md pointer blocks"

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Conventions + design rationale | ✅ done | 65b37e9. Two convention files, two mechanism docs, Principle 9 added to audience-and-philosophy.md. |
| 2 | Templates + CLAUDE.md pointer blocks | ✅ done | This commit. Five seed files + edits to CLAUDE.md.template + audience-and-philosophy.md. |
| 3 | Installer + framework-level docs | ⏭ next | Two `mirror_dir` calls in `install.sh`; two README "Conventions installed" entries. Verify against fresh dir + `~/cambodia-growth/`. |

## Where we are

Phase 2 shipped five new template files plus edits to two
existing files. The new templates are:

- `templates/data_sources/README.md` (14 lines) — one-liner +
  pointer to convention + mention of EXAMPLE doc
- `templates/data_sources/INDEX.md` (70 lines) — empty quick-nav
  table seed + adding-a-source recipe (quotes the convention's
  bullets), with a "(none yet)" helper-functions table
- `templates/data_sources/EXAMPLE_world_bank_api.md` (172 lines)
  — generic worked example with the six required sections
  (Status, Headline anchor, Endpoints, Query shape, Parsing,
  Pitfalls). Anchor is `NY.GDP.PCAP.CD / VNM / 2022 ≈ 4,164`,
  captioned as illustrative. The `> This is a template / worked
  example.` blockquote at the top makes the placeholder status
  unambiguous.
- `templates/methods/README.md` (16 lines) — one-liner +
  pointer to convention + boundary mention
- `templates/methods/EXAMPLE_method/rule.md` (123 lines) —
  generic worked example carrying all seven required sections
  (Source / Rule / Why this version / Exclusions / Edge cases /
  Known limitations / Diagnostic counts) plus an optional
  "Structural-economy filter" section. Modeled on cambodia's
  cohort_rule.md, genericized to a "complex-tradable entrant"
  rule with `vN`-style versioning and placeholder diagnostic
  counts.

The CLAUDE.md.template edit added two pointer blocks (Methods
after Decision Records — cross-link relationship; Data Sources
after Source Registry — both about external knowledge), each
5 lines body, matching the existing style. The codebase-structure
tree gained `data_sources/` and an updated gloss for `methods/`.

## What's next

**Phase 3 — installer + framework README.**

1. Edit `install.sh` to add `mirror_dir` calls for
   `templates/data_sources/` and `templates/methods/`. Mirror the
   pattern of the existing `mirror_dir` calls in section
   "3. Project-level scaffolding" (lines ~72–78). Note that the
   existing scaffolding section uses `mkdir -p insights wiki raw
   deliverables sources` — Phase 3 should bump this to also
   create `data_sources methods`. The `mirror_dir` for
   `templates/data_sources/` mirrors INDEX, README, and the
   EXAMPLE_*.md doc.
2. Edit framework `README.md` to add `data-sources` and `methods`
   to the "Conventions installed" list with one-paragraph blurbs.
   Match the style of the existing seven entries.
3. **Verification per plan:**
   - `bash install.sh /tmp/test-research-project` against fresh
     empty dir; result includes `data_sources/{INDEX,README,
     EXAMPLE_world_bank_api}.md` and `methods/{README.md,
     EXAMPLE_method/rule.md}`.
   - Re-run install in same dir; every line of output for
     newly-installed files starts with `~` (skip — idempotent).
   - Re-run install against `~/cambodia-growth/`. Existing
     `data_sources/INDEX.md` and `methods/electronics_entry/`
     are NOT overwritten — `copy_if_absent` handles this. Verify
     by `git diff` in the cambodia-growth repo (no changes to
     existing tracked files; new EXAMPLE_*.md files appear).

Reading order to start cold for Phase 3: this file → `plan.md`
("Phase 3 — Installer + framework-level docs" section) →
`install.sh` (sections "1. Conventions, hooks, skills" and
"3. Project-level scaffolding") → framework `README.md` (the
"Conventions installed" list, search heading).

## Surprises

- **CLAUDE.md.template already had a `## Data Sources` stub
  heading** (a project-overview placeholder, with prose that
  itself was stale — it pointed at "methods/" for "full data
  ledgers", but data ledgers go in `data_sources/` now). Adding
  the new pointer block also called "Data Sources" would have
  created a duplicate-heading collision. Resolved by deleting
  the stub heading + body (the new pointer block subsumes its
  purpose: data_sources/INDEX.md is the canonical at-a-glance
  list, and the pointer block points there). Also removed the
  matching "Data Sources" line from the recommended-top-sections
  comment at the top of the template. Net: no `## Data Sources`
  stub before convention pointer blocks; one `## Data Sources`
  pointer block after Source Registry.
- **`EXAMPLE_method/rule.md` has eight section headings, not
  seven.** The seven required sections are all present in the
  required order. The extra section, "Structural-economy
  filter" (between Exclusions and Edge cases), mirrors the
  cambodia model where exclusions split naturally into "explicit
  list of re-export hubs" (the canonical Exclusions section) and
  "data-driven population threshold" (the structural filter).
  The convention says "extra sections are fine; missing required
  sections are a smell" — keeping this preserves the realism of
  the worked example. Acceptable.
- **`EXAMPLE_world_bank_api.md` is 172 lines** — a third of the
  cambodia `imf_sdmx_api.md` (467 lines). Cambodia accumulated a
  real engagement's worth of dataflow cheatsheets and codelist
  tables. The seed file is deliberately focused on the six
  required sections plus minimum supporting content. Acceptable
  — the goal is to show shape, not provide exhaustive content.
- **`audience-and-philosophy.md` pointer-block count bumped to
  ten** (from eight, as Phase 1's surprise predicted). The line
  now reads: "Insights Logging, Wiki, Script Headers, Analytical
  Commit Format, Handoff Format, Plan Structure, Decision
  Records, Methods, Source Registry, Data Sources." Order
  matches the order they appear in the template.

## What didn't work

Nothing this session — Phase 2 went as planned, with the one
collision (Data Sources stub vs pointer block) resolved cleanly.

## Verification log

- `wc -l` on the five new files: 70, 14, 172, 16, 123. INDEX is
  in the typical-seed range; EXAMPLE_world_bank_api is upper-end
  but acceptable for a seed showing all six required sections;
  EXAMPLE_method/rule.md fits in the typical-rule range.
- `grep -E '^## ' templates/methods/EXAMPLE_method/rule.md` →
  Source / Rule / Why this version / Exclusions / Edge cases /
  Structural-economy filter / Known limitations / Diagnostic
  counts. All seven required sections present, in order; one
  extra section between Exclusions and Edge cases (allowed).
- `grep -nE '^(\*\*Status\*\*|## Headline anchor|## [0-9]+\.)' templates/data_sources/EXAMPLE_world_bank_api.md`
  → all six required sections present in order (Status,
  Headline anchor, Endpoints, Query shape, Parsing, Pitfalls).
- `awk` body-line count of new pointer blocks: Methods = 5 lines,
  Data Sources = 5 lines (counted manually from file content).
  Both ≤6, both reference `.claude/conventions/<name>.md (read on
  demand)`, both follow name-when-applies-where-protocol shape
  of the existing eight blocks.
- `grep -c '^## Data Sources$' templates/CLAUDE.md.template` →
  1 (no duplicate heading after the stub-removal fix).
- `git diff --stat HEAD` before commit: 2 modified files
  (CLAUDE.md.template, audience-and-philosophy.md) + 5 new
  files in `templates/data_sources/` and `templates/methods/`.

## Hash trail

- Init plan: `b9c7ca7`
- Cleanup `.Rhistory`: `8aa3d46`
- Phase 1 work: `65b37e9`
- Handoff refresh after Phase 1: `c6d9d9e`
- Hash-trail fill-in for Phase 1: `fcfbc1d`
- Phase 2 work + handoff refresh: *(this commit, fill in)*

# Handoff: refdocs-conventions

**Status:** ACTIVE — Phase 1 complete; Phase 2 next
**Date:** 2026-05-06
**Last commit on plan branch:** `65b37e9` — "Phase 1: data-sources + methods conventions and design rationale"

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Conventions + design rationale | ✅ done | 65b37e9. Two convention files, two mechanism docs, Principle 9 added to audience-and-philosophy.md. |
| 2 | Templates + CLAUDE.md pointer blocks | ⏭ next | Build seed files that mirror the required-section lists from Phase 1's conventions. Two pointer blocks in CLAUDE.md.template (≤6 lines each); refresh codebase-structure tree. |
| 3 | Installer + framework-level docs | ⏸ blocked on P2 | Two `mirror_dir` calls in `install.sh`; two README "Conventions installed" entries. |

## Where we are

Phase 1 shipped four prose files plus an edit to
`docs/audience-and-philosophy.md`. The two conventions
(`data-sources.md`, `methods.md`) are 187 and 181 lines — at the
upper edge of the existing 62–183-line convention range, but
within the band the plan specified. Each opens with a
**Boundary with neighbors** section that disambiguates from
`raw/sources/`, `wiki/concepts/`, `decisions/`, and
`data/README.md`. Both reference (don't duplicate) the new
**Verifiable freshness anchors** principle in
`audience-and-philosophy.md`.

The audience-and-philosophy edit added Principle 9, bumped the
header to "nine design principles", added a row to the binding
table, and fixed a pre-existing stale line in Principle 5 (it
listed seven pointer blocks including "Manifest Logging" — but
manifest logging was replaced by `script-header` +
`analytical-commit-format` in `bcae991`, leaving eight blocks).
That fix was not in the plan's scope strictly speaking, but the
file was open, the line was wrong, and it would have been worse
to leave it. Flagged below in Surprises.

No skill, helper module, install change, or template seed
shipped — those are Phase 2/3.

## What's next

1. **Phase 2 — templates.** Five files to write, one to edit:
   - `templates/data_sources/INDEX.md` — empty quick-nav table
     ("If you want X, read Y") + the "how to add a source"
     recipe. The recipe quotes the convention's adding-a-source
     bullets.
   - `templates/data_sources/README.md` — one-liner pointing at
     `.claude/conventions/data-sources.md`.
   - `templates/data_sources/EXAMPLE_world_bank_api.md` —
     generic worked example carrying all required sections
     (Status, Headline anchor(s), Endpoints, Query shape,
     Parsing, Pitfalls). The headline anchor must be a
     plausible WB indicator triple, captioned as illustrative.
     Modeled on `~/cambodia-growth/data_sources/imf_sdmx_api.md`.
   - `templates/methods/README.md` — one-liner pointing at
     `.claude/conventions/methods.md`.
   - `templates/methods/EXAMPLE_method/rule.md` — generic worked
     example with all seven required sections (Source / Rule /
     Why this version / Exclusions / Edge cases / Known
     limitations / Diagnostic counts). Modeled on
     `~/cambodia-growth/methods/electronics_entry/cohort_rule.md`,
     genericized (no Cambodia / electronics specifics — pick a
     plausible cross-country tradable-classification rule).
   - `templates/CLAUDE.md.template` — add two pointer blocks
     (Data Sources, Methods) ≤6 lines each, matching the style
     of the existing eight blocks. Refresh the codebase-structure
     tree to surface `data_sources/` alongside `methods/` (the
     tree currently lists `methods/` alone and is missing
     `data_sources/`).

2. **Phase 3 — installer + framework README.** After Phase 2:
   - Edit `install.sh` to add `mirror_dir` calls for
     `templates/data_sources/` and `templates/methods/`. Mirror
     the pattern of the existing `mirror_dir` calls in section
     "3. Project-level scaffolding".
   - Edit framework `README.md` to add `data-sources` and
     `methods` to the "Conventions installed" list with
     one-paragraph blurbs.
   - Verification per plan: fresh-install + idempotent re-run +
     re-install against `~/cambodia-growth/` (existing files
     should not be overwritten).

Reading order to start cold: this file → Phase 1's commit
`65b37e9` (the four files + edit) →
`.claude/conventions/data-sources.md` and
`.claude/conventions/methods.md` (the required-sections lists
that Phase 2's templates must match) →
`~/cambodia-growth/data_sources/imf_sdmx_api.md` and
`~/cambodia-growth/methods/electronics_entry/cohort_rule.md`
(the patterns to genericize for the EXAMPLE_* files) →
`templates/CLAUDE.md.template` (the existing pointer-block
style to match).

## Surprises

- **Pre-existing staleness in `audience-and-philosophy.md`.**
  Principle 5 said "The seven pointer blocks shipped in v1:
  Insights Logging, Wiki, **Manifest Logging**, Handoff Format,
  Plan Structure, Decision Records, Source Registry." But
  `bcae991` replaced Manifest Logging with Script Headers +
  Analytical Commit Format — leaving eight pointer blocks. The
  v1 plan's handoff explicitly noted this count change but
  didn't update this file. I fixed it in passing (eight blocks,
  current names). After Phase 2 ships data-sources and methods
  blocks, this line bumps to ten — Phase 2 should update it
  again.
- **Convention line counts at the upper edge of the band.**
  data-sources is 187, methods is 181; the plan said
  "~120-180 lines, outliers either way are a smell." Both have
  three-folder boundary disambiguations (data-sources vs
  `raw/sources/` vs `wiki/concepts/` vs `data/README.md`;
  methods vs `decisions/` vs `wiki/concepts/`) which add a
  whole section over a typical convention. Trimmable, but
  trimming would lose the disambiguation that the plan
  explicitly required. Acceptable.
- **No `phases/` or `context/` content was needed.** The plan
  scaffolded those dirs but Phase 1's work didn't require any
  per-phase notes or context files — `plan.md` was enough.
  Both dirs remain empty (git won't track them) and may stay
  empty for Phases 2/3.

## What didn't work

Nothing this session — Phase 1 went as planned.

## Verification log

- `wc -l .claude/conventions/data-sources.md
   .claude/conventions/methods.md
   docs/data-sources-mechanism.md
   docs/methods-mechanism.md
   docs/audience-and-philosophy.md` →
  187, 181, 229, 284, 133. Conventions in band; mechanism docs
  are longer (allowed — `docs/source-registry-mechanism.md` is
  273); audience-and-philosophy gained 13 lines from Principle
  9 + binding-table row.
- `grep -n 'Boundary with neighbors\|Verifiable freshness\|audience-and-philosophy'
   .claude/conventions/data-sources.md .claude/conventions/methods.md` →
  data-sources has Boundary at line 16, references
  `docs/audience-and-philosophy.md` at lines 67, 82, 83 (cross-cut
  cite, not duplication). methods has Boundary at line 16,
  references at line 115. ✓
- Plan files committed in `b9c7ca7` (init plan), `8aa3d46`
  (cleanup empty `.Rhistory` that scaffolding had created),
  `65b37e9` (Phase 1 work). Three commits, plus this
  handoff-refresh commit to follow.

## Hash trail

- Init plan: `b9c7ca7`
- Cleanup `.Rhistory`: `8aa3d46`
- Phase 1 work: `65b37e9`
- Handoff refresh: `c6d9d9e`
- This hash-trail fill-in: (this commit)

# Handoff: refdocs-conventions

**Status:** ✅ COMPLETE — all 3 phases shipped. Ready for archival.
**Date:** 2026-05-06
**Last commit on plan branch:** `baefabc` — "Phase 3: install.sh + README for data_sources/methods"

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Conventions + design rationale | ✅ done | 65b37e9. Two convention files, two mechanism docs, Principle 9 added to audience-and-philosophy.md. |
| 2 | Templates + CLAUDE.md pointer blocks | ✅ done | 0f18ff0. Five seed files + edits to CLAUDE.md.template + audience-and-philosophy.md. |
| 3 | Installer + framework-level docs | ✅ done | baefabc. install.sh mkdir + two mirror_dir calls; README.md two convention entries + tree refresh. |

## Where we are

Phase 3 was a small, mechanical phase: two file edits.

**`install.sh`** — bumped the project-level scaffolding line from
`mkdir -p insights wiki raw deliverables sources` to also include
`data_sources methods`, and added two `mirror_dir` calls right
after the existing five. Pattern matches the existing calls
exactly (no new helpers, no new conditionals).

**`README.md`** — three additions:

- Conventions tree (top of "What's in here"): added
  `methods.md` and `data-sources.md` to the conventions listing
  with one-line glosses.
- `docs/` tree: added `data-sources-mechanism.md` and
  `methods-mechanism.md` (the Phase 1 outputs).
- `templates/` tree: added `data_sources/` and `methods/`
  entries with one-line glosses listing the seed files.
- "Conventions installed" prose section: added two new
  subsections — `methods` (after `decision-records`) and
  `data-sources` (after `source-registry + /scan-sources`),
  each one paragraph matching the existing style. Each blurb
  names the required sections, the boundary with neighbors, and
  the pointer to the convention + mechanism doc + template.

Verification passed all three checks per plan.

## What's next

**Plan complete.** Per implementation skill:

1. User confirms plan completion.
2. `touch plan/plan-refdocs-conventions/.completed` triggers the
   Stop hook, which spawns the archivist + cleanup subagents.
3. Archivist synthesizes `archive/plan-refdocs-conventions.md`,
   updates `archive/index.md`, cleans up
   `plan/plan-refdocs-conventions/`, updates `.scc/status/`.
4. Cleanup scans the file manifest for dead code (none expected
   for this plan — every new file is intentional).

Future framework work post-archive (per plan.md "Open Items
Deferred"):

- **Project-utility-module convention** (`<project>_utils.py` +
  cross-link from data_sources docs to helper functions). Defer
  to v1.2 — needs a Python+R bilingual story.
- **`/methods-lint` / `/data-sources-lint` skills.** Possible if
  discipline slips in pilot use; not v1.
- **Auto-extraction of headline anchors into a smoke-test
  runner.** Tempting (run all anchors weekly, alert on drift)
  but adds always-on infra; the convention is the v1
  deliverable.
- **Lifting "headline anchor" into a wiki convention.** Synthesis
  pages might benefit from an anchor field too; defer until
  synthesis pages see enough usage.

## Surprises

- **cambodia-growth install side-effect.** The Phase 3
  verification step ran `bash install.sh ~/cambodia-growth`. That
  cambodia repo had been on an older framework version (only
  `.claude/conventions/insights-logging.md` was tracked); this
  install run brought every framework file the cambodia-growth
  repo had been missing — eight new convention files, all hooks,
  all skills, all template scaffolding (`raw/`, `wiki/`,
  `deliverables/`, `sources/`). Test-specific additions from
  *this* phase (`data_sources/EXAMPLE_*`, `data_sources/README`,
  `methods/EXAMPLE_method/`, `methods/README`) were cleaned up
  after verification. The broader framework upgrade was left in
  place as untracked files for the user to review and decide on.
  This is normal `install.sh` behavior — it mirrors everything.
- **Existing cambodia assets fully preserved.** The plan's load-
  bearing claim was that `data_sources/INDEX.md` (cambodia's
  hand-curated index) and `methods/electronics_entry/` (the v2
  cohort rule + supporting PDFs) survive a re-install. Verified:
  `data_sources/INDEX.md (exists, skipping)` in install output,
  no entries for `electronics_entry/` or
  `structural_transformation_analysis/` (those weren't iterated
  because the source `templates/methods/` only contains
  `EXAMPLE_method/` and `README.md`). `git diff` on cambodia-
  growth's tracked files showed exactly the same three modified
  files that were modified before the install ran (`.gitignore`,
  `CLAUDE.md`, `slides/Kickoff with CAPRED.pptx`) — no overwrite.

## What didn't work

Nothing this session — Phase 3 went as planned, and was the
shortest of the three (two file edits, three verification runs).

## Verification log

- **Fresh install** — `rm -rf /tmp/test-research-project && mkdir
  /tmp/test-research-project && bash install.sh /tmp/test-research-project`.
  Output included `+ data_sources/EXAMPLE_world_bank_api.md`,
  `+ data_sources/INDEX.md`, `+ data_sources/README.md`,
  `+ methods/EXAMPLE_method`, `+ methods/README.md`. Post-run
  `ls` confirmed all five files in expected locations including
  `methods/EXAMPLE_method/rule.md`.
- **Idempotency** — re-ran install in the same `/tmp` dir; every
  data_sources/methods line started with `~` (skip): six lines
  total (5 files + 1 conventions/methods.md), all skipped.
- **Cambodia-growth** — `bash install.sh ~/cambodia-growth`.
  Output: `~ data_sources/INDEX.md (exists, skipping)` (existing
  INDEX preserved); `+` for the four new EXAMPLE/README files.
  `methods/electronics_entry/` and
  `methods/structural_transformation_analysis/` not listed (not
  iterated). `git diff --stat` showed no new tracked-file
  modifications beyond the pre-existing three.
- **`git status --short`** before commit on framework repo:
  `M README.md`, `M install.sh`, plus an unrelated
  `?? plan/plan-v1-framework/.completed` (gitignored, ignore).
- **`git diff --stat`** before commit: 2 files, 23 insertions, 3
  deletions. Within expected envelope for this phase.

## Hash trail

- Init plan: `b9c7ca7`
- Cleanup `.Rhistory`: `8aa3d46`
- Phase 1 work: `65b37e9`
- Handoff refresh after Phase 1: `c6d9d9e`
- Hash-trail fill-in for Phase 1: `fcfbc1d`
- Phase 2 work + handoff refresh: `0f18ff0`
- Hash-trail fill-in for Phase 2: `6c2813f`
- Phase 3 work: `baefabc`
- Handoff refresh + hash-trail fill-in for Phase 3: (this commit)

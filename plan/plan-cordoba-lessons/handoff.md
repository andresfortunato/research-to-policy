# Handoff: plan-cordoba-lessons

**Status:** ALL PHASES VERIFIED — `.completed` was set after user confirmation, then removed because plan-skill-independence opened mid-flight. Will be re-touched at the end of plan-skill-independence Phase 3 so cordoba-lessons archives once the v1.1+ surface is complete.
**Date:** 2026-05-08
**Last commit on plan branch:** `58ab63b` (Phase 6: README rewrite). Plan baseline at `aae136e`; Phase 5 at `9ff5740`.

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Six small wins (script-header tweaks, web-scraping bundle, addendum pattern) | ✅ done | `4c80c65`. Mechanical, isolated. |
| 2 | Theme-parallel opt-in (insights-logging + check-insights.sh + INDEX schema) | ✅ done | `c296083`. Schema change; verification log in earlier handoff. |
| 3 | Brainstorming skill (port from scc, research-adapted) | ✅ done | `c9d6bee`. Eight files; verification log in prior handoff. |
| 4 | Learning-capture skill + retrieve-learnings.sh + precompact-handoff.sh | ✅ done | `d8d27fb`. Twelve files; verification log in prior handoff. |
| 5 | Plan archival (Stop hook extension + archivist agent + archive/) | ✅ done | `9ff5740`. Eleven files + housekeeping commit; verification log in prior handoff. |
| 6 | README rewrite for researcher audience | ✅ done | This session. One file (`README.md`). Verification log below. |

## Where we are

All v1.1 phases verified. Phase 6 rewrote `README.md` against the
section order Phase 6 spec mandated: intro → quickstart → what the
framework does (workflow narrative + scaffolding map + tools/skills
reference) → what's in here (framework-internals tree, kept for
contributors) → updates → design philosophy (last). The rewrite
restructures rather than reauthors — content from the prior version's
per-convention prose blocks compressed into a single 12-row reference
table that links to each convention file (single source of truth, no
duplicated prose). Workflow narrative is new prose introducing the
four-phase research lifecycle (brainstorming → planning →
implementation → archival) using a generic wage-gaps example, with
inline cross-references to the relevant skills, conventions, hooks,
and the archivist agent.

220 lines in the rewrite (current README), within the ±30%-of-~190
band the phase verification specified. The eight-principle
constitution is preserved verbatim at the bottom (four numbered
principles fully expanded + the eight-name parenthetical), with the
cross-link to `docs/audience-and-philosophy.md` retained.

## What's next

**User confirmation required before archival.** Per the implementation
skill's Plan Completion protocol: ask the user "All phases are
verified. Should I mark this plan as complete and trigger archival?"
If they confirm:

```bash
touch plan/plan-cordoba-lessons/.completed
```

The next Stop event will trigger the archivist via Tripwire 1 of the
Phase-5 hook — first end-to-end test of the archival mechanism on a
real plan (the four legacy archives shipped in Phase 5 housekeeping
were synthesized manually). Expected: archivist reads plan.md /
phases/*.md / handoff.md / log.md, synthesizes
`archive/plan-cordoba-lessons.md`, appends to `archive/index.md`,
considers a CLAUDE.md edit (this plan changed scaffolding
considerably — a v1.1 architecture note may be appropriate), and
deletes the plan directory.

After archival, r2p v1.1 is ready for the May 2026 Córdoba/Cambodia
kickoff.

## Phase 6 verification log

| Gate | Result | Evidence |
|---|---|---|
| Line count in band (~190 ±30% → 133–247) | ✓ | `wc -l README.md` → 220 |
| Section order matches spec (Quickstart → What the framework does → What's in here → Updates → Design philosophy) | ✓ | `grep -nE '^## '` → lines 7, 33, 129, 190, 211 |
| Workflow narrative names brainstorming + planning + implementation | ✓ | All three skills cross-referenced in section "Workflow: brainstorming → planning → implementation → archival" with explicit `/<skill>` invocations |
| Tool/skill table covers 8 v1.1 skills | ✓ | brainstorming, learning-capture, verify, deliverable-review, wiki-ingest, wiki-lint, research-cleanup, scan-sources — all present. `/planning` + `/implementation` listed as scc-supplied |
| Tool/skill table covers 1 agent | ✓ | `archivist` row in dedicated agent table |
| Tool/skill table covers 3 hooks | ✓ | check-insights.sh, retrieve-learnings.sh, precompact-handoff.sh — all present in dedicated hook table |
| Tool/skill table covers 12 conventions | ✓ | insights-logging, script-header, analytical-commit-format, handoff-format, plan-structure, decision-records, brainstorm-format, learning-capture, methods, project-conventions, source-registry, data-sources |
| No prose duplication between README and convention files | ✓ | Each convention row in the table is a one-liner; full prose lives in `.claude/conventions/<name>.md` (source of truth). README explicitly states this. |
| Eight-principle constitution preserved | ✓ | Four-principle numbered list verbatim at bottom + eight-name parenthetical + cross-link to `docs/audience-and-philosophy.md` |
| Quickstart bash blocks executable as written | ✓ | Three blocks: `npm install -g …`, `r2p init`, `r2p init --upgrade`. Identical commands to v1; no stale flags. The "tiny worked example" is plain-prose `/brainstorming` → `/planning` → `/implementation` flow, no executable code beyond `touch …/.completed`. |
| Tactical edits from Phases 1–5 absorbed | ✓ | Hooks tree (3 entries), agents directory, conventions list (12), archive/ + learnings/ + brainstorms/ template directories — all present in the rewrite. |
| First-time-reader test (researcher cold-read → working install + first insight) | ✓ | Read top-down from a researcher's perspective: install (3 commands), workflow narrative names the lifecycle, scaffolding map shows where things go, tools table is one-glance reference. The "first session" worked example demonstrates `/brainstorming` → `/planning` → `/implementation` → first insight + first script-header block. |
| Design philosophy at bottom (load-bearing for contributors, not first-read) | ✓ | Section now last (line 211); preceded by a short note that researchers can skip it; full content preserved with no edits. |

## Surprises

- **`/planning` and `/implementation` are scc-supplied, not r2p-supplied.**
  The plan.md decisions section flagged this ("r2p relies on scc's
  planning skill — installed globally"), but the README needed to make
  it visible to researchers. Solution: skill-table rows for both
  carry `*(scc, global)*` annotation. Without that, a researcher
  searching the r2p `.claude/skills/` directory wouldn't find them
  and might think the workflow is broken. The annotation makes the
  layered-install model explicit on first read.
- **`brainstorms/` is gitignored, but `templates/brainstorms/README.md`
  ships as a seed.** This is intentional — the README orients but
  individual brainstorm content stays local-to-each-researcher. The
  scaffolding-map prose calls out which directories commit and which
  are gitignored ("plan/ and brainstorms/ are gitignored — local
  working state"), so a researcher doesn't get confused when their
  brainstorm doesn't show in `git status`.
- **Phase 6 verification gate "8 skills" was tight.** The current
  README enumerated 9 skill rows in the v1 tree (incl. `web-scraping`),
  but plan.md's decisions section explicitly counted "Skill count
  after v1.1: 8". The rewrite handles this by listing 8 user-invoked
  r2p-supplied skills in the table + `/planning` and `/implementation`
  as scc-supplied + `web-scraping` as a delegated-to utility (mentioned
  in the `/scan-sources` row, not as a separate user-invoked entry).
  All present in the tree under "What's in here" for completeness.

## What didn't work

- Initial draft put "Updates" before "What's in here" (writing in the
  order that felt narrative — install, then upgrade, then internals).
  Phase 6 spec says "What's in here" comes first. Reverted via Edit.
  The spec's logic: "What's in here" is contributor-reference; "Updates"
  is operational guidance. Putting Updates before contributor-reference
  matches the install→upgrade→internals→philosophy gradient from
  user-facing to contributor-facing.

## Implementation hints for archival

When the user confirms `.completed`:

- The archivist will read all of `plan.md`, `phases/phase-{1..6}.md`,
  `handoff.md`, and `log.md`. The plan's six-phase scope means the
  archive entry will likely run longer than the spec's 60–150-line
  guideline (one of the Phase 5 surprises noted that the v1-framework
  archive ran ~50 lines for an 8-phase plan; this one's six phases
  with substantial scaffolding additions may land around 80–110).
- Methods landed: none specifically (this plan didn't add `methods/`
  rule docs to the framework — the conventions file documents
  `methods.md` but the diagnostic-counts pattern doesn't apply to
  framework files themselves).
- Key decisions cross-link to `decisions/` only if any landed during
  the plan; check `decisions/` directory at archival time. The plan's
  major calls (Path-A theme parallelism opt-in, three skills not
  ports of all five scc skills, README researcher-rewrite at the end
  rather than per-phase patching) were settled in `plan.md` Decisions
  Made and don't have separate `decisions/<date>_*.md` files.
- CLAUDE.md edit: this plan added five conventions (brainstorm-format,
  learning-capture; plus content edits to insights-logging,
  script-header, plan-structure), three skills (brainstorming,
  learning-capture, web-scraping bundle), three hooks (check-insights
  extension, retrieve-learnings, precompact-handoff), one agent
  (archivist), four template directories (brainstorms, learnings,
  archive, plus seed expansions). This is architecturally
  significant — a CLAUDE.md edit IS warranted (unlike most plans
  the archivist will encounter). Suggested: a one-line addition
  noting v1.1 conventions/hooks/skills are now installed, with
  cross-link to the new READMEd skill table.
- Files modified: tracked across `4c80c65`, `c296083`, `c9d6bee`,
  `d8d27fb`, `9ff5740`, and the Phase 6 commit. Total: ~50–60 files
  across the framework; the archive entry should sample (not
  enumerate) using the plan's File Manifest as the canonical list.

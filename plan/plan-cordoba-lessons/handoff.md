# Handoff: plan-cordoba-lessons

**Status:** ACTIVE — Phase 2 complete; Phase 3 next.
**Date:** 2026-05-08
**Last commit on plan branch:** `c296083` — "Phase 2: theme-parallel opt-in (insights/<theme>/, output/<theme>/)" (plan baseline at `aae136e`).

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Six small wins (script-header tweaks, web-scraping bundle, addendum pattern) | ✅ done | `4c80c65`. Mechanical, isolated. |
| 2 | Theme-parallel opt-in (insights-logging + check-insights.sh + INDEX schema) | ✅ done | `c296083`. Schema change; verification log below. |
| 3 | Brainstorming skill (port from scc, research-adapted) | ⏭ next | Closes the methodology-essay-isn't-a-plan gap. |
| 4 | Learning-capture skill + retrieve-learnings.sh + precompact-handoff.sh | ⏭ queued | Three-bucket model: insights/decisions/learnings. |
| 5 | Plan archival (Stop hook extension + archivist agent + archive/) | ⏭ queued | Existing four .completed markers archived manually first. Archivist scope kept narrow — defers project-wide cleanup to `/research-cleanup`. |
| 6 | README rewrite for researcher audience | ⏭ queued | Quickstart → workflow → scaffolding → tools → what's in here → updates → design philosophy (last). Ships after all components exist. |

## Where we are

Phase 2 landed in one commit. The opt-in theme-parallel layout is now
in place across the convention, the hook, the INDEX template, the
CLAUDE.md.template tree + pointer block, the README, and a new
`docs/theme-parallel-mechanism.md` rationale doc. Hooks accept both
flat (`insights/NN_*.md`, `output/NN_*`) and theme-parallel
(`insights/<theme>/NN_*.md`, `output/<theme>/NN_*`) shapes.

Phase 3 is the brainstorming-skill port from scc. Reference material
lives at `~/github/super-claudio-code/skills/brainstorming/SKILL.md`
— read once, then write the scr version with research-domain examples
(deflator choice, identification strategy, reference-category
selection, survey-vintage breakage) and a planning-skill-agnostic
handoff.

## What's next

1. **Phase 3 kickoff** — `phases/phase-3.md`. Touches:
   `.claude/skills/brainstorming/SKILL.md` (new),
   `.claude/conventions/brainstorm-format.md` (new),
   `templates/brainstorms/README.md` (new),
   `docs/brainstorm-mechanism.md` (new),
   `templates/CLAUDE.md.template` (pointer block + tree gloss),
   `src/lib/install-project.js` (seed `templates/brainstorms/` on
   init; symlink skill globally — but check first whether
   `installGlobals()` already auto-symlinks every subdir of
   `<framework>/.claude/skills/`; that was the surprise from Phase 1
   — it does, so no JS edit may be needed for the symlink),
   `README.md` (one entry under Conventions installed + one under
   Skills).
2. **Pre-Phase 5 housekeeping (deferrable until Phase 5):** archive
   the four pre-existing `.completed` markers manually
   (plan-install-redesign, plan-project-conventions,
   plan-refdocs-conventions, plan-v1-framework) so the new Stop
   hook doesn't fire on legacy markers when Phase 5 lands.

## Phase 2 verification log

| Gate | Result | Evidence |
|---|---|---|
| `insights-logging.md` adds clearly-labeled "Theme-parallel layout (opt-in)" section | ✓ | New section after "Where insights live"; flat-is-default rule preserved at top. Cross-links to `docs/theme-parallel-mechanism.md`. |
| `check-insights.sh` artifact glob accepts `output/<theme>/0[0-9]_*` | ✓ | Regex extended to `output/([^/]+/)?0[0-9][a-z]?_.*\.(png\|csv\|meta\.json)`. |
| `check-insights.sh` insights glob accepts `insights/<theme>/NN_*.md` | ✓ | Regex extended to `insights/([^/]+/)?[0-9]+_.*\.md`. |
| Theme artifact + no insights doc → hook fires naming the artifact | ✓ | Scratch-dir test: `output/spatial-equilibrium/01_chart.png` produced JSON `additionalContext` listing the file. |
| Theme insights doc staged → hook silent | ✓ | Scratch-dir test: `insights/spatial-equilibrium/01_*.md` exits 0 with no stdout. |
| Flat artifact + no insights doc → hook still fires (regression) | ✓ | Scratch-dir test: `output/01_chart.png` produced the JSON nudge. |
| Flat insights doc staged → hook still silent (regression) | ✓ | Scratch-dir test: `insights/01_finding.md` exits 0 with no stdout. |
| `INDEX.md` template carries optional `Theme` column with omit/keep guidance | ✓ | Header preamble explains: omit for flat, keep for theme-parallel; example cross-references `insights-logging.md`. |
| `docs/theme-parallel-mechanism.md` mirrors the rhythm of `insights-mechanism.md` | ✓ | Sections: Problem → What the framework does → Why opt-in → Why subfolder not declaration → "Theme" defined → Cross-cutting insights → Tradeoffs → What this does NOT do → Provenance. |
| `CLAUDE.md.template` codebase-tree annotates `insights/`/`output/` with opt-in pattern; pointer block updated | ✓ | Tree adds inline comments for both directories; Insights Logging block names the opt-in pattern in one sentence. |
| `README.md` insights-logging paragraph documents opt-in pattern | ✓ | One paragraph added; full rewrite deferred to Phase 6. Cross-links to all three docs (convention, mechanism, theme-parallel-mechanism). |
| No project-specific cordoba content shipped in committed framework files | ✓ | Theme names in examples are generic (`spatial-equilibrium`, `labor-markets`). Provenance section in mechanism doc references "the cordoba audit" abstractly (no filenames, no scripts). |

## Surprises

- **No surprises in Phase 2.** The scope was tight (six files,
  one of them new), the regex change was a single optional
  capture group `([^/]+/)?` in two places, and verification was a
  scratch-dir bash sequence. The decision to keep the existing
  hook nudge text flat-biased ("ls insights/ | sort") rather than
  bloating it for theme-aware projects is intentional — the
  convention file carries the full guidance; the hook stays terse.

## What didn't work

- Nothing meaningful in Phase 2.

## Implementation hints for Phase 3

- Read `~/github/super-claudio-code/skills/brainstorming/SKILL.md`
  once, then write the scr version. The adaptation work is
  domain-shifting (web-app examples → applied-research examples)
  + planning-skill-agnostic handoff text + output path
  (`brainstorms/<topic>.md`).
- The directory `brainstorms/` is already in
  `templates/CLAUDE.md.template`'s codebase tree (line ~42:
  "decision-rationale write-ups feeding plans (gitignored)"),
  so no tree change is needed there — only the pointer block.
  Check whether the brainstorms/ subdirectory needs to be
  seeded by `install-project.js` (TBD; depends on whether
  v1 install already creates it).
- For symlinking the new skill: `installGlobals()` already
  iterates every subdir of `<framework>/.claude/skills/` and
  symlinks each into `~/.claude/skills/` (this was the Phase 1
  surprise). Adding `.claude/skills/brainstorming/` is sufficient
  — no JS edits, just like web-scraping in Phase 1.
- Theme-parallel awareness: the brainstorming skill should mention
  `brainstorms/<topic>.md` as the default and note (one line) that
  theme-parallel projects may use `brainstorms/<theme>/<topic>.md`
  if they wish. Don't over-engineer this; one sentence in the
  SKILL.md suffices.
- Decisions-vs-brainstorms boundary: `decisions/` records carry
  peer-reviewable methodology calls; `brainstorms/` carry
  decisions-pre-planning that may or may not graduate to
  `decisions/`. Document this boundary in `brainstorm-mechanism.md`.

# Framework v1.1 — Córdoba Lessons

Completed: 2026-05-08

## What was built

A six-phase framework upgrade (v1.1) motivated by auditing `~/cordoba`, an
applied-research project that ran without r2p conventions and accumulated the
failure modes the framework was designed to prevent. The plan shipped six
convention hardening fixes, an opt-in theme-parallel layout for `insights/`
and `output/`, three skills/hooks ported from `super-claudio-code`
(brainstorming, learning-capture, plan archival via archivist agent + Stop hook
tripwire), a pre-compact handoff nudge, and a full README rewrite for the
researcher audience. All six phases verified and committed; the framework is
ready for the May 2026 Córdoba/Cambodia kickoff.

## Key decisions

1. **Theme-parallel layout: opt-in subfolder (Path A), not a declared `themes.md`.**
   `insights/<theme>/NN_*.md` is permitted alongside the flat `insights/NN_*.md`
   default. Hooks and the INDEX schema accept both shapes. Alternatives considered
   were a required `themes.md` declaration file and a per-theme `insights_<theme>/`
   top-level directory. Path A was chosen because it preserves the flat default,
   avoids upfront enumeration, and keeps the schema change minimal. Explicitly
   deferred: revisiting `themes.md` only if pilot use shows free-form theme strings
   produce drift.

2. **Hook implementation language: bash (constitution-mandated).**
   The three scc source hooks (`stop.js`, `pre-compact.js`, `user-prompt-submit.js`)
   are JavaScript. The framework constitution mandates pure bash + standard Unix tools
   for hooks (no runtime dependencies above `jq`). All three were re-implemented in
   bash. This enforces the "one project, one env" principle and prevents JS leakage
   outside `src/`.

3. **Three skills ported, not all five from scc.**
   `brainstorming`, `learning-capture`, and the bundled `web-scraping` were ported.
   `cleanup.js` (code-shaped; `/research-cleanup` already covers the research
   equivalent) and the planning skill (r2p relies on scc's globally-installed version;
   a research-domain rewrite is a v1.2 call) were explicitly not ported.

4. **Archivist and `/research-cleanup` are complementary, not redundant.**
   The archivist is automated (Stop hook fires on `.completed`), scoped to the plan
   being archived. `/research-cleanup` is user-invoked and project-wide. The boundary
   is unit (plan vs project) and trigger (hook vs user). Each skill documents the
   other's scope; no duplicated cleanup logic. This plan required both the archivist
   agent file and a "Boundary with archivist agent" paragraph added to the
   `/research-cleanup` SKILL.md.

5. **README rewritten at the end, not per-phase.**
   Phase 6 (README rewrite) was sequenced last so it could describe the full v1.1
   surface in one pass. Per-phase patching was rejected because the README would have
   required revision with each subsequent phase landing. Rewrite landed at 220 lines
   with section order: quickstart → workflow narrative → scaffolding map → tools/skills
   reference table → what's in here → updates → design philosophy.

6. **`/planning` and `/implementation` annotated as scc-supplied in the README.**
   These skills are installed globally from scc, not bundled in r2p. Without explicit
   annotation, researchers searching `.claude/skills/` would not find them and might
   assume the workflow is broken. The skill table rows carry `*(scc, global)*`
   annotations to make the layered-install model visible on first read.

## Methods landed

None. This plan added framework conventions, skills, hooks, and an agent — no
`methods/<slug>/rule.md` files were created or modified (those belong to individual
research projects, not to the framework repo itself).

## Files added or modified

Grouped by directory; all new unless marked. (✚ new, ✎ modified)

**.claude/agents/**
- ✚ `archivist.md` — research-adapted port of the scc archivist agent

**.claude/conventions/**
- ✎ `script-header.md` — `Supersedes:` field, project-relative paths rule, shared-utilities note, one-env note
- ✎ `insights-logging.md` — opt-in `<theme>/` subfolder layout documented
- ✎ `plan-structure.md` — `.completed` marker → archival flow documented
- ✚ `learning-capture.md` — gotcha/insight types, `index.yaml` format, retrieval contract
- ✚ `brainstorm-format.md` — `brainstorms/<topic>.md` shape, planning-skill handoff

**.claude/hooks/**
- ✎ `check-insights.sh` — extended: glob `insights/<theme>/*.md`; detect `.completed` for archival tripwire
- ✚ `retrieve-learnings.sh` — bash port of scc `user-prompt-submit.js`
- ✚ `precompact-handoff.sh` — bash port of scc `pre-compact.js`

**.claude/skills/**
- ✚ `brainstorming/SKILL.md` — research-adapted port of scc brainstorming
- ✚ `learning-capture/SKILL.md` — research-adapted port of scc learning-capture
- ✎ `research-cleanup/SKILL.md` — "Boundary with archivist agent" paragraph added
- ✚ `web-scraping/` — bundled skill (sourced from `~/.claude/skills/web-scraping/`)

**.claude/**
- ✎ `settings.template.json` — wired `UserPromptSubmit` + `PreCompact` hooks

**docs/**
- ✚ `theme-parallel-mechanism.md`
- ✚ `learning-capture-mechanism.md`
- ✚ `brainstorm-mechanism.md`
- ✚ `plan-archival-mechanism.md`
- ✎ `audience-and-philosophy.md` — "one project, one env" + opt-in theme parallelism added if appropriate

**templates/**
- ✎ `CLAUDE.md.template` — pointer blocks for brainstorming, learning-capture, archival; codebase-tree updated
- ✚ `brainstorms/README.md`
- ✚ `learnings/README.md`, `learnings/index.yaml`
- ✚ `archive/README.md`, `archive/index.md`
- ✎ `deliverables/internal-research-memo/PROFILE.md` — dated addendum pattern endorsed
- ✎ `deliverables/internal-research-memo/template.md` — Update-section example added

**src/lib/**
- ✎ `install-project.js` — seeds `brainstorms/`, `learnings/`, `archive/` on `r2p init`

**Root**
- ✎ `README.md` — full researcher-audience rewrite (Phase 6)
- ✎ `TODO.md` — cordoba-lessons items marked shipped; v1.1 candidates updated

## Learnings

**`brainstorms/` is gitignored but its seed README ships.** The seed orients the
directory without committing brainstorm content, which stays local to each researcher.
The scaffolding-map prose in README.md explicitly flags which directories commit and
which are gitignored to prevent confusion when `git status` is clean after a
brainstorming session.

**Phase 6 "8 skills" count was tighter than it appeared.** The v1 README tree listed
9 skill rows (including `web-scraping`), but the plan's decisions section counted
"Skill count after v1.1: 8". Resolution: 8 user-invoked r2p-supplied skills in the
reference table, with `/planning` and `/implementation` listed separately as
scc-supplied, and `web-scraping` surfaced as a delegated-to utility (mentioned in the
`/scan-sources` row) rather than a standalone entry. All present in the tree under
"What's in here" for completeness.

**Section-order discipline in the README rewrite mattered.** An initial draft put
"Updates" before "What's in here" (felt narrative: install → upgrade → internals).
The Phase 6 spec mandated the reverse. The spec's logic — "What's in here" is
contributor reference; "Updates" is operational guidance — puts contributor reference
before the upgrade story, matching the user-to-contributor gradient that runs through
the document.

**`/planning` and `/implementation` visibility gap.** These scc-global skills are
central to the workflow but absent from `.claude/skills/`. Without explicit annotation
in the README skill table, a researcher's first cold read would suggest a broken
workflow. The `*(scc, global)*` annotation is the fix; it also makes the
layered-install model (r2p + scc together) explicit for the first time in user-facing
docs.

## Metrics

- Phases: 6 completed
- Sessions: 2 (plan + phases 1–5 in session 1; Phase 6 in session 2)
- Final commit: `58ab63b` (Phase 6: README rewrite)

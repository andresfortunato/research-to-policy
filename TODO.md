# TODO — research-to-policy

Project-development backlog for the framework itself. Researchers *using* the framework do not need this file — it tracks what could land in v1.1+ and beyond. v1 is the current scoped release, designed for the May 2026 Córdoba/Cambodia kickoff workshop and the two pilots' close-out periods (end-Aug and end-Sept 2026); see `plan/plan-v1-framework/plan.md` for the build history.

## Shipped

- **v1.1** — cordoba-lessons (six small wins, theme-parallel opt-in, `brainstorming` skill, `learning-capture` skill + retrieve-learnings hook, plan archival via `archivist` agent + Stop hook tripwire, README rewrite for researcher audience). See `archive/plan-cordoba-lessons.md`.
- **v1.2** — skill-independence (vendored `planning`, `implementation`, `agent-teams` skills from super-claudio-code; added `r2p plan init <slug>` CLI subcommand; rationale at `docs/skill-independence-mechanism.md`). See `archive/plan-skill-independence.md` after archival.

## v1.3 and beyond

- **Plugin migration (dual CLI + plugin distribution)** — convert r2p from "npm CLI + global symlinks" to "npm CLI + Claude Code plugin" (the scc / Everything-Claude-Code pattern). Skills would get auto-rendered `(research-to-policy)` labels and namespaced commands (`/research-to-policy:planning`) — replaces the current hardcoded `(r2p) ` prefix in description fields. CLI shrinks to project-only scaffolding; plugin owns skills/hooks/agents. Layout: add `.claude-plugin/{plugin.json, marketplace.json}`, move `.claude/skills/` → `skills/`, `.claude/hooks/` → `hooks/` (+ `hooks/hooks.json` for auto-wiring), `.claude/agents/` → `agents/`, `.claude/conventions/` → `conventions/`. Delete `src/lib/install-globals.js` (plugin handles symlinks via `${CLAUDE_PLUGIN_ROOT}`). Drop hook entries from project `settings.json` (plugin auto-wires). `r2p init` writes `extraKnownMarketplaces` + `enabledPlugins` block to project's `.claude/settings.json` instead of symlinking. Once landed: revert the hardcoded `(r2p) ` description prefix on all 12 skills. Reference: `~/github/super-claudio-code/.claude-plugin/` and its README "Installation" section for the dual-channel pattern. Confirmed-real env var: `${CLAUDE_PLUGIN_ROOT}` (used by Superpowers in its `hooks/hooks.json`).
- **TDD-equivalent for research pipelines** — heavier whole-pipeline regression on every change (per-artifact `/verify` covers single-artifact sanity but not full-pipeline drift). Possible skill name: `pipeline-check`.
- **`evidence-ledger`** — a project-level table of formal claims, the chart/CSV that supports each, and whether the claim has been challenged.
- **`chart-registry`** — `save_fig(findings={...})` pattern so every chart ships with metadata Claude can read without re-opening the PNG.
- **`citation-discipline`** — every quantitative claim must reference a source (paper, dataset, internal doc).
- **LaTeX/Beamer add-on** — borrowed from Pedro/Hugo Sant'Anna's templates; useful when the deliverable register shifts toward academic outputs.
- **WIP-limited multi-project dashboard** (Hugo's vault-manager pattern) — for researchers juggling multiple country engagements.
- **Stata first-class support** — alongside R and Python.
- **Mode-registry / cross-skill advisor** (Imbad pattern) — once skill count exceeds ~8 and "which entry point?" becomes the bottleneck.
- **Globalize conventions** (without conflicting with Claude's defaults) — let researchers share one set of conventions across multiple project repos. Open question: how does this interact with project-shared `.claude/conventions/` (README principle 4 — "project-shared, not user-personal")? Collaborators cloning a project repo without `r2p` installed would see `@`-references in `CLAUDE.md` to paths that don't exist for them.

## Build pattern for new entries

Each addition follows the same pattern: one convention file in `.claude/conventions/`, optionally one hook script in `.claude/hooks/`, one section in `docs/`, optionally a skill in `.claude/skills/`. See `docs/extending.md`.

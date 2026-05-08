# Phase 3 — Vendor + adapt `agent-teams`, ship `scr plan init`, README pass

Read `plan.md` for the goal, constraints, decisions, file manifest, and repo context. This file scopes Phase 3.

## Intent

Last phase of skill-independence. Vendor the third scc skill (agent-teams), add the `scr plan init <slug>` CLI subcommand the planning skill recommends, drop the `(scc, global)` annotations from the README's skills table, and write the rationale doc. After this phase ships, scr is genuinely standalone — `npm install -g super-claudio-research` + `scr init` produces the full workflow surface.

## Files

- ✚ `.claude/skills/agent-teams/SKILL.md` (+ any references it carries)
- ✚ `src/lib/plan-init.js`
- ✎ `src/cli.js` — wire `scr plan init <slug>` subcommand
- ✎ `README.md` — drop `*(scc, global)*` annotations from `/planning` and `/implementation` skill rows; add precedence note for users with scc co-installed; Quickstart no longer references scc
- ✚ `docs/skill-independence-mechanism.md` — rationale (why vendor + adapt vs require scc co-install)
- ✎ `TODO.md` — mark shipped
- After commit: `touch plan/plan-cordoba-lessons/.completed` to re-arm cordoba archival

## Adaptations — agent-teams

Read `~/github/super-claudio-code/skills/agent-teams/` first; apply the same three-tier framework (mechanical / domain-shaped / cross-cutting) used in Phases 1–2.

Default research adaptations expected:
- Teammate output dir: `output/<task-name>/` → `scratch/<task-name>/` (matches Phase 2's swap; one consistent rule project-wide).
- Examples: software-team work units (build / test / lint / migrate) → research-team work units (compare 2 identification strategies in parallel; run 3 robustness checks; ingest 5 raw sources).
- Cross-references: drop scc-specific (`tdd`, cleanup-agent, context-monitor); add scr equivalents (`/verify`, archivist, `precompact-handoff.sh`).
- Path swaps: `.scc/...` → project root.

Phase-2 surprise risk: agent-teams may reference scc-side hooks or skills not yet anticipated. Surface as escalations if encountered; don't port silently.

## `scr plan init <slug>` CLI

`src/lib/plan-init.js` scaffolds:

```
plan/plan-<slug>/
├── plan.md              ← from templates/plan/plan.md (new template seed)
├── handoff.md           ← from templates/handoff.md (existing)
├── log.md               ← empty seed
├── phases/              ← empty dir
└── context/             ← empty dir
```

Idempotent: re-run skips existing files (same `copyIfAbsent` pattern as `install-project.js`). Slug validation: lowercase-snake-case, no leading `plan-` (the prefix is added).

`src/cli.js` adds a `plan` command with `init` subcommand using commander's nested-command pattern (already a dep).

If `templates/plan/plan.md` doesn't exist, this phase adds it as a minimal seed (Goal / Constraints / Decisions Made / File Manifest / Phases — empty headers researcher fills in).

## README updates

- Skills table rows for `/planning` and `/implementation`: drop the `*(scc, global)*` annotation entirely.
- Quickstart worked-example block: no change (it already names `/planning` and `/implementation` without explaining where they come from — now true).
- New short subsection in **Updates** or **Design philosophy**: "If you also have super-claudio-code installed, scr's symlinks (created by `scr init`) win over scc's for the three vendored skills (planning, implementation, agent-teams). Symlink whichever you want last."
- Skill count check: phase-6's verification gate said "8 skills" for v1.1. Post-Phase-3, scr ships 11 user-invoked skills (8 + planning + implementation + agent-teams). Update any explicit count language in README to reflect 11.

## docs/skill-independence-mechanism.md

Short rationale doc (~40 lines): why we vendored vs. required scc co-install (distribution / single-install UX), what we adapted (verification language, examples, paths, cross-refs) vs preserved (skills' bones), how the precedence works for users with both frameworks installed. Cross-links Phase 6 README rewrite as the trigger and `brainstorms/skill-independence.md` as the design conversation.

## Verification

- `agent-teams` SKILL.md: same gates as Phases 1–2 (line count in band, frontmatter updated, scc-residue grep clean, symlink works).
- `scr plan init plan-test-foo` on a scratch project creates the scaffold; second run reports `~ <file> (exists, skipping)` for each file (idempotent).
- `scr init` on a fresh scratch project: `~/.claude/skills/{planning,implementation,agent-teams}/` all symlink into the scr repo. `installGlobals` reports `(3 skills linked)` for the new ones.
- README skill table: `grep "scc, global"` → 0 matches.
- README Quickstart bash blocks still execute (no stale flags introduced).
- `scr` CLI: `scr --help` shows the new `plan init` subcommand. `scr plan init --help` shows usage.
- Skill count language in README updated (8 → 11 user-invoked skills, or skill count removed if ambiguous).
- Re-touch cordoba-lessons `.completed` marker as the **last** action of the phase commit. The next Stop event fires the archivist on cordoba-lessons (first end-to-end archival on a real plan, as originally intended).

## Dependencies

Upstream: Phases 1 and 2 (skills must exist before README cites them; agent-teams cross-refs implementation).
Downstream: cordoba-lessons archival fires on next Stop after Phase 3 commits.

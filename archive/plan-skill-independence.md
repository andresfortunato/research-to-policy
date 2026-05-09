# Framework v1.2 — Skill Independence

Completed: 2026-05-08

## What was built

A three-phase vendoring effort that made r2p fully standalone by porting `planning`,
`implementation`, and `agent-teams` from super-claudio-code and adapting them to
applied-research language. The plan also shipped `r2p plan init <slug>`, a CLI
subcommand that scaffolds a new plan directory with all required files. After this
plan, `npm install -g research-to-policy` + `r2p init` produces the full workflow
surface — brainstorming → planning → implementation → archival, plus parallel-team
orchestration — with no scc co-install required.

## Key decisions

1. **Vendor `planning`, `implementation`, `agent-teams`; skip `tdd` and `cleanup`.**
   Only the three skills central to the workflow narrative the README already promised
   were vendored. `tdd` has no research analog (replaced by `/verify` cross-refs);
   `cleanup` is covered by the existing archivist + `/research-cleanup` boundary.
   Alternatives included vendoring more scc skills for parity and requiring scc
   co-install indefinitely. Chose the narrow vendor scope because it closes the
   distribution gap without over-scoping.

2. **Skill names unchanged (`planning`, `implementation`, `agent-teams`).**
   The brainstorming skill already triggers "the planning skill" by name in
   `brainstorm-format.md`. Renaming would have required chasing references already
   shipped in cordoba-lessons. Alternatives: rename to research-specific slugs,
   namespace as `r2p-planning`. Rejected to avoid breaking the brainstorm-handoff
   contract.

3. **Project-identity swap: `cat .scc/status/project.md` → `cat CLAUDE.md`.**
   scc uses `.scc/status/project.md` as the session-entry context anchor; r2p uses
   `CLAUDE.md`. All three vendored skills have the reference updated. No new hidden
   directories were added (r2p constraint).

4. **`r2p plan init <slug>` uses commander's nested-command pattern.**
   `r2p plan init` rather than a flat `r2p plan-init`. The nested shape (`r2p plan
   --help` reveals subcommands) leaves `r2p plan list` and `r2p plan archive` as
   natural extension points. Flat command was the simpler alternative but would have
   produced flag explosion as more plan-management commands land.

5. **`templates/plan/plan.md` seed added (none existed).**
   Phase 3 spec flagged its absence as a risk; confirmed at phase start that
   `templates/plan/` was missing entirely. The 25-line seed mirrors
   `plan-skill-independence/plan.md`'s structure and is scaffolded by `r2p plan init`.

6. **Distribution-independence criterion: fresh `npm install` only.**
   Mid-Phase-2, the success criterion was sharpened: the goal is that a fresh
   `npm install -g research-to-policy` + `r2p init` symlinks only r2p's skills,
   never reaching for scc. A user's own global scc symlinks are personal-environment
   state, not a distribution problem. README last-installer-wins note covers the
   coexistence case; `docs/skill-independence-mechanism.md` has the full rationale.

## Methods landed

None. This plan added framework skills, a CLI subcommand, a plan template seed, and
a mechanism doc — no `methods/<slug>/rule.md` files were created or modified.

## Files added or modified

Grouped by directory. (✚ new, ✎ modified)

**.claude/skills/**
- ✚ `planning/SKILL.md` — research-adapted port (163 lines)
- ✚ `planning/references/multi-session.md` — port + light adaptation (95 lines)
- ✚ `implementation/SKILL.md` — research-adapted port (175 lines)
- ✚ `implementation/references/escalation-reference.md` — research-domain trigger rewrite (90 lines)
- ✚ `agent-teams/SKILL.md` — research-adapted port (161 lines)
- ✚ `agent-teams/references/` — ported reference files

**src/**
- ✎ `cli.js` — wired `r2p plan init <slug>` subcommand via commander nested-command pattern
- ✚ `lib/plan-init.js` — scaffolds `plan/plan-<slug>/{plan.md, handoff.md, log.md, phases/, context/}`

**templates/**
- ✚ `plan/plan.md` — 25-line plan seed (Goal / Constraints / Decisions Made / File Manifest / Repo Context / Phases / Phase Order)

**docs/**
- ✚ `skill-independence-mechanism.md` — rationale for vendor+adapt vs scc co-install requirement (59 lines)

**Root**
- ✎ `README.md` — dropped `*(scc, global)*` annotations from skills table; added `/agent-teams` row; added `r2p plan init` block in Updates; added last-installer-wins precedence note
- ✎ `TODO.md` — v1.1 + v1.2 marked shipped

## Learnings

**Distribution-independence is a crisper criterion than "no scc dependency."** The
original framing ("vendored skills don't depend on scc") was correct but underspecified.
The sharper version — a fresh `npm install` + `r2p init` must symlink only r2p's files —
is testable by reading `src/lib/install-globals.js` and confirming it iterates only
`.claude/agents/*.md` and `.claude/skills/*/`. A user's personal scc globals are not r2p's
problem; documenting the coexistence behavior (last-installer-wins) is sufficient.

**`agent-teams` needed less adaptation than expected.** Orchestration, file ownership,
output collection, and quality gates are more framework-shaped than language-shaped.
The research adaptations narrowed to: swapping `plan/plan-<slug>/scratch/<task-name>/`
for scc's output dir, reframing examples (parallel deflators, robustness checks, per-country
panels), and dropping the `.scc/status/` consolidation step. The bones are unchanged.

**README pre-existing edits require a clean-working-tree check before Phase 3 staging.**
An unrelated unstaged change (the `/verify` row's "When" column wording) was present in
README.md at Phase 3 session start. It was reverted before staging to keep the commit
clean. The lesson: treat `git diff HEAD -- README.md` as a pre-staging gate whenever
README is in the phase's file manifest.

## Metrics

- Phases: 3 completed
- Sessions: 1 (all three phases in a single session on 2026-05-08)
- Final commit: `1a99830` (Phase 3: agent-teams + CLI + README + mechanism doc)

# Handoff: plan-cordoba-lessons

**Status:** ACTIVE — Phase 3 complete; Phase 4 next.
**Date:** 2026-05-08
**Last commit on plan branch:** `c9d6bee` — "Phase 3: brainstorming skill (research-adapted port from scc)" (plan baseline at `aae136e`).

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Six small wins (script-header tweaks, web-scraping bundle, addendum pattern) | ✅ done | `4c80c65`. Mechanical, isolated. |
| 2 | Theme-parallel opt-in (insights-logging + check-insights.sh + INDEX schema) | ✅ done | `c296083`. Schema change; verification log in earlier handoff. |
| 3 | Brainstorming skill (port from scc, research-adapted) | ✅ done | `c9d6bee`. Eight files; verification log below. |
| 4 | Learning-capture skill + retrieve-learnings.sh + precompact-handoff.sh | ⏭ next | Three-bucket model: insights/decisions/learnings. |
| 5 | Plan archival (Stop hook extension + archivist agent + archive/) | ⏭ queued | Existing four .completed markers archived manually first. Archivist scope kept narrow — defers project-wide cleanup to `/research-cleanup`. |
| 6 | README rewrite for researcher audience | ⏭ queued | Quickstart → workflow → scaffolding → tools → what's in here → updates → design philosophy (last). Ships after all components exist. |

## Where we are

Phase 3 landed in one commit. The brainstorming skill now ships in
scr — research-adapted port from scc, with domain examples shifted
to deflator choice / identification strategy / reference categories /
survey-vintage breakage. Output at `brainstorms/<topic>.md`; planning-
skill handoff is agnostic ("the planning skill"). The convention file
documents the file shape and boundary with `decisions/`, `plan/`,
`insights/`, and `/verify`. The mechanism doc explains why brainstorms
are gitignored (working state, not citable form) and why they're
distinct from `/verify` (timing) and `decisions/` (artifact-vs-conversation).

`scr init` now creates `brainstorms/` as scaffolding and seeds the
README. The global symlink at `~/.claude/skills/brainstorming` was
rewritten from scc's version to scr's during scratch-dir verification —
any researcher running `scr init` gets the research-adapted skill from
that point on.

Phase 4 is the learning-capture skill plus two new bash hooks
(`retrieve-learnings.sh` for UserPromptSubmit; `precompact-handoff.sh`
for PreCompact). Reference material lives at
`~/github/super-claudio-code/skills/learning-capture/SKILL.md` and the
two upstream JS hooks (`stop.js`/`pre-compact.js`/`user-prompt-submit.js`).
Bash-port the JS hooks (no JS leakage outside `src/` per the v1
constitution); research-adapt the skill domain examples (gotcha
example: "PONDII didn't exist in 2014 EPH waves" rather than
web-app gotchas).

## What's next

1. **Phase 4 kickoff** — `phases/phase-4.md`. Touches:
   - `.claude/skills/learning-capture/SKILL.md` (new)
   - `.claude/conventions/learning-capture.md` (new)
   - `.claude/hooks/retrieve-learnings.sh` (new — bash port of scc `user-prompt-submit.js`)
   - `.claude/hooks/precompact-handoff.sh` (new — bash port of scc `pre-compact.js`)
   - `.claude/settings.template.json` (wire UserPromptSubmit + PreCompact)
   - `templates/learnings/{README.md, index.yaml}` (new — empty `learnings: []` seed)
   - `docs/learning-capture-mechanism.md` (new — three-bucket rationale)
   - `templates/CLAUDE.md.template` (pointer block + tree gloss)
   - `src/lib/install-project.js` (seed `templates/learnings/`)
   - `README.md` (Conventions + Skills + Hooks tactical edits)
2. **Pre-Phase 5 housekeeping (deferrable until Phase 5):** archive
   the four pre-existing `.completed` markers manually
   (plan-install-redesign, plan-project-conventions,
   plan-refdocs-conventions, plan-v1-framework) so the new Stop
   hook doesn't fire on legacy markers when Phase 5 lands.

## Phase 3 verification log

| Gate | Result | Evidence |
|---|---|---|
| Skill triggers on research-domain phrasing | ✓ | Description names "how should we measure", "what's the right deflator", "let's think about identification", "explore options for", "brainstorm", "should we use X or Y". |
| Output path `brainstorms/<topic>.md` consistent across SKILL / convention / mechanism | ✓ | All three docs reference the same path. Theme-parallel option (`brainstorms/<theme>/<topic>.md`) documented in SKILL + convention + CLAUDE.md.template tree gloss. |
| Planning-skill handoff is agnostic | ✓ | SKILL.md says "trigger the planning skill" by name; convention emphasizes "agnostic about whose"; mechanism doc names this as an explicit design choice (scr does not ship its own planning skill in v1.1). |
| `scr init --upgrade` lands the new skill globally | ✓ | `installGlobals()` is called by both `init` and `init --upgrade` in `src/commands/init.js`. Scratch-dir test: symlink `~/.claude/skills/brainstorming` was rewritten from scc's version to scr's. |
| `brainstorms/` directory created in target projects | ✓ | Added to SCAFFOLDING_DIRS in install-project.js; mirrorDir copies the README seed. Scratch-dir test confirmed `brainstorms/README.md` was created. |
| Gitignore covers `brainstorms/` so README seed stays local-only | ✓ | Existing `brainstorms/` line in GITIGNORE_BLOCK; verified in scratch test (gitignore reads `plan/ \n brainstorms/ \n .scc/`). |
| CLAUDE.md.template carries pointer block + tree gloss | ✓ | Pointer block "Brainstorming" added before "Plan Structure"; tree gloss expanded with opt-in theme-parallel note. |
| README.md tactical edits land conventions / skills / docs / templates entries plus the description block | ✓ | `brainstorming/` listed under `.claude/skills/`; `brainstorm-format.md` under `.claude/conventions/`; `brainstorm-mechanism.md` under `docs/`; `brainstorms/README.md` under `templates/`; new entry "brainstorm-format + /brainstorming" inserted between plan-structure and decision-records. |
| Boundary documented vs `decisions/`, `plan/`, `insights/`, `/verify` | ✓ | Convention "Distinct from neighboring conventions" section names all four; mechanism doc has "Why brainstorms are distinct from /verify" and "Why brainstorms are distinct from decisions/" sections. |
| No project-specific cordoba content shipped in committed framework files | ✓ | Domain examples are generic (PWT rgdpe/rgdpo, EPH 2014 break, deflator choice, reference categories). The mechanism doc references "an applied-research project that ran without scr conventions" abstractly — no filenames, no scripts. |

## Surprises

- **Global symlink swap happened automatically and silently.** The
  pre-Phase-3 state was `~/.claude/skills/brainstorming` →
  `~/github/super-claudio-code/skills/brainstorming/` (scc's version).
  After `scr init` ran in the scratch dir, `installSkills()` detected
  the existing symlink, called `unlink`, and created a new symlink to
  scr's version. This is the intended behavior — scr's skills win for
  any name collision — but worth flagging: any researcher who had been
  relying on scc's brainstorming skill globally now gets scr's
  research-adapted version on the same machine. The two are similar
  enough in shape that this should not surprise users; the description
  changes are domain-shaped.
- **No JS edit needed for the symlink itself, as predicted in the Phase 1
  surprise note.** `installSkills()` iterates every subdir of
  `<framework>/.claude/skills/` — adding `brainstorming/` was sufficient.
  The install-project.js edit was only for seeding `templates/brainstorms/`
  in the target project (since `brainstorms/` was not previously in
  `SCAFFOLDING_DIRS`).

## What didn't work

- Nothing meaningful in Phase 3.

## Implementation hints for Phase 4

- Read `~/github/super-claudio-code/skills/learning-capture/SKILL.md`
  once, then write the scr version. The adaptation work is
  domain-shifting (web-app gotchas → applied-research gotchas:
  variable broke in 2014, dataset has known underreporting, deflator
  series version diverges in oil-exporters) + retrieval contract
  (trigger-keyword matching is the routing mechanism, not theme).
- The two upstream JS hooks (`pre-compact.js`, `user-prompt-submit.js`)
  must be **bash-ported**, not vendored — v1 constitution forbids JS
  leakage outside `src/`. Reference shape is `check-insights.sh`
  (silent-by-default, JSON `additionalContext` only on a tripwire,
  no jq dependency for simple cases). Read both upstream JS files
  for the trigger logic, then write the bash equivalents from scratch.
- `templates/learnings/index.yaml` should ship as `learnings: []` —
  an empty seed. The retrieval hook reads this file and matches on
  trigger keywords; the format needs to support quick keyword scans
  (consider whether a flat list-of-objects with `triggers: [...]`
  fields is enough, or whether a separate keyword index is needed —
  scc's version is the reference).
- Wire both hooks in `.claude/settings.template.json` — UserPromptSubmit
  for `retrieve-learnings.sh`, PreCompact for `precompact-handoff.sh`.
  The settings template is what gets copied into `.claude/settings.json`
  on `scr init`.
- `learnings/` is project-wide, not theme-aware (decision in plan.md).
  Don't introduce theme subfolders; trigger-keyword matching does the
  routing.
- The three-bucket model (insights / decisions / learnings) is the
  rationale to document in `docs/learning-capture-mechanism.md` —
  insights are *findings from data*, decisions are *methodology calls*,
  learnings are *gotchas and tacit knowledge that don't fit the other
  two*. The mechanism doc should make the boundary obvious.

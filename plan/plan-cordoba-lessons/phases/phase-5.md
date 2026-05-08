# Phase 5 — Plan archival (Stop hook extension + archivist agent)

Read `plan.md` for the goal, constraints, decisions, file manifest,
and repo context that govern all phases. This file scopes Phase 5.

## Intent

Port scc's plan-archival mechanic: a `.completed` marker in a
`plan/plan-<name>/` directory triggers the `archivist` agent on
next Stop, which synthesizes a permanent archive entry to
`archive/plan-<name>.md`, updates `archive/index.md`, and deletes
the plan directory. cordoba had no archival concept; scr's
existing `plan/plan-*/.completed` markers (already used by the
four shipped plans) are the half-finished version of this.

**Boundary discipline.** Archivist (this phase, automated, per-plan)
and `/research-cleanup` (existing v1, user-invoked, project-wide)
are complementary, not redundant. Both sides must explicitly
defer to the other. Verification includes a consistency check.

## Files

- `.claude/agents/archivist.md` (new) — adapted port of scc
  `agents/archivist.md`. Research adaptations: archive entry
  surfaces "Decisions made" (cross-linking to `decisions/`) and
  "Methods landed" (cross-linking to `methods/<>/rule.md`) in
  addition to scc's "Files modified". Updates `CLAUDE.md` if a
  new convention/skill/hook landed (the mechanism docs already
  track this implicitly; the archivist makes it explicit).
  **Boundary with `/research-cleanup`.** The archivist scope is
  *narrow and per-plan*: synthesize the archive entry, write to
  `archive/`, delete `plan/plan-<name>/`, update CLAUDE.md if
  architecture changed. It does NOT do project-wide cleanup
  (orphan scripts, stale intermediates, unreferenced charts) —
  that's `/research-cleanup`'s job. Archivist agent prose
  explicitly says: "If you notice repo-wide cruft, recommend
  the user run `/research-cleanup` after this archive completes;
  do not attempt repo-wide cleanup yourself."
- `.claude/skills/research-cleanup/SKILL.md` (extend) —
  add a "Boundary with archivist agent" paragraph: per-plan
  archival is the archivist's job; this skill audits everything
  *outside* an active plan's scope (orphans, intermediates,
  unreferenced charts older than the most-recent `data/raw/`
  change). Cross-link the agent. Discipline: no overlap, no
  redundant cleanup logic.
- `.claude/hooks/check-insights.sh` (extend, not duplicate) —
  after the existing insights-tripwire logic, scan
  `plan/plan-*/.completed` for any plan whose `.archival-triggered`
  sentinel is missing. If found, emit a Stop-blocking
  `additionalContext` instructing Claude to launch the
  archivist agent. Sentinel-write protects against re-block
  loops. Silent if no `.completed` markers or all already
  triggered.
- `.claude/conventions/plan-structure.md` (extend) — add a
  "Completion and archival" section documenting: marker file
  name, sentinel file name, what the archivist does, when to
  create the marker (when handoff says ✅ COMPLETE), where the
  archive lives. Cross-link to the agent.
- `templates/archive/README.md` (new) — orientation: archive
  is permanent project-level memory; one entry per completed
  plan; index.md is the rollup.
- `templates/archive/index.md` (new) — empty seed (header +
  "(no archived plans yet)" placeholder).
- `docs/plan-archival-mechanism.md` (new) — rationale: why
  archive vs leave-the-directory (signal-to-noise as plan
  count grows); why `.completed` marker is the right trigger
  (researcher-controlled, not auto-detected from handoff);
  why the archivist is an agent not a skill (multi-step file
  ops + cleanup is agent-shaped).
- `templates/CLAUDE.md.template` — codebase-tree gloss for
  `archive/`.
- `src/lib/install-project.js` — seed `templates/archive/` on
  init; symlink the archivist agent globally.
- `README.md` — "Hooks" sub-entry for the extended Stop hook
  behavior; "Agents installed" block (new section if none
  exists yet). (Tactical edit; full rewrite is Phase 6.)

## Verification

- In a scratch project with `plan/plan-test/` containing
  `.completed`, running a Stop event: hook emits the agent-launch
  `additionalContext`; sentinel `.archival-triggered` lands.
  On the next Stop, hook does NOT re-block (sentinel honored).
- Same scratch project: archivist agent (invoked via the hook
  nudge) writes `archive/plan-test.md` with the documented
  structure, appends to `archive/index.md`, and deletes
  `plan/plan-test/`. Both markers gone with the directory.
- In a scratch project with NO `.completed` markers, Stop hook
  behaves exactly as v1 (insights tripwire only). No regression.
- Existing four `.completed` markers in this repo
  (`plan/plan-{install-redesign,project-conventions,refdocs-conventions,v1-framework}/.completed`)
  are still readable by the new code, but the live framework
  repo's plans don't auto-archive on the next Stop —
  sentinel files are pre-created (or the plans are archived
  manually) before this phase ships, so the new Stop hook
  finds them already-triggered.
- **Consistency check between archivist and `/research-cleanup`.**
  Run both in sequence in a scratch project: archivist on a
  `.completed` plan, then `/research-cleanup`. The two outputs
  should be non-overlapping — archivist touched only the plan
  directory and `archive/`; `/research-cleanup` proposes only
  project-wide items (nothing inside the now-deleted plan
  directory, nothing already archived). If overlap exists, the
  boundary paragraph in either file is wrong; fix.

## Dependencies

Upstream: Phase 4 (precompact-handoff hook hint at
learning-capture; archivist agent surfaces "Learnings captured"
in archive entries) AND the four pre-existing `.completed`
markers being archived manually first (so the new Stop hook
doesn't fire on legacy markers).
Downstream: Phase 6 (README rewrite covers archival as
end-of-plan lifecycle moment).

## Reference patterns

Upstream agent: `~/github/super-claudio-code/agents/archivist.md`.
Upstream stop hook: `~/github/super-claudio-code/hooks/stop.js` —
read for the sentinel-file pattern, then bash-port into the
existing `check-insights.sh` rather than adding a second hook.

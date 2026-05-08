# Handoff: plan-cordoba-lessons

**Status:** ACTIVE — Phase 5 complete; Phase 6 next.
**Date:** 2026-05-08
**Last commit on plan branch:** `<TBD>` — "Phase 5: plan archival (archivist agent + Stop hook extension + archive/)" (plan baseline at `aae136e`).

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Six small wins (script-header tweaks, web-scraping bundle, addendum pattern) | ✅ done | `4c80c65`. Mechanical, isolated. |
| 2 | Theme-parallel opt-in (insights-logging + check-insights.sh + INDEX schema) | ✅ done | `c296083`. Schema change; verification log in earlier handoff. |
| 3 | Brainstorming skill (port from scc, research-adapted) | ✅ done | `c9d6bee`. Eight files; verification log in prior handoff. |
| 4 | Learning-capture skill + retrieve-learnings.sh + precompact-handoff.sh | ✅ done | `d8d27fb`. Twelve files; verification log in prior handoff. |
| 5 | Plan archival (Stop hook extension + archivist agent + archive/) | ✅ done | `<TBD>`. Eleven files + housekeeping commit that archived the four legacy plans first; verification log below. |
| 6 | README rewrite for researcher audience | ⏭ next | Quickstart → workflow → scaffolding → tools → what's in here → updates → design philosophy (last). Ships now that all components exist. |

## Where we are

Phase 5 landed in two commits: a housekeeping commit that archived the
four pre-existing `.completed` plans manually (so the new Stop hook
wouldn't fire on legacy markers post-ship), and the Phase 5 implementation
itself. The framework now has its plan-archival lifecycle wired:
researcher creates `plan/plan-<slug>/.completed`, the Stop hook's new
Tripwire 1 emits `decision: block` instructing Claude to launch the
archivist subagent, the archivist synthesizes
`archive/plan-<slug>.md`, appends to `archive/index.md`, optionally
edits CLAUDE.md, and deletes the plan directory.

`check-insights.sh` is now a two-tripwire Stop hook. Tripwire 1 (plan
archival, BLOCKING) runs before Tripwire 2 (insights, NON-BLOCKING)
because archival is the higher-signal event — the insights nudge can
wait for the next Stop after archival completes. Sentinel pattern
(`.archival-triggered`) bash-ports scc's stop.js loop-protection.

`.claude/agents/archivist.md` is the research-adapted port: scc's
"Files modified" section is augmented with **Methods landed**
(cross-links to `methods/<slug>/rule.md`) and **Key decisions**
explicitly cross-linking to `decisions/YYYY-MM-DD_<slug>.md`. The
boundary paragraph deferring repo-wide cleanup to `/research-cleanup`
is load-bearing — it pairs symmetrically with the boundary paragraph
just added to `research-cleanup/SKILL.md`.

The four legacy plans archived during housekeeping
(`archive/plan-install-redesign.md`, `plan-project-conventions.md`,
`plan-refdocs-conventions.md`, `plan-v1-framework.md`) populate the
archive on first contact rather than shipping with `(no archived plans
yet)`. Each entry follows the archivist's documented structure (60–110
lines: What was built / Key decisions / Methods landed / Files added
or modified / Learnings / Metrics).

`install-globals.js` already iterated `.claude/agents/` from Phase 3 of
the install-redesign plan — the new archivist.md gets symlinked
automatically; no installer-globals change needed. `install-project.js`
got `archive` added to `SCAFFOLDING_DIRS` and one new `mirrorDir` call
for `templates/archive/`. `upgrade.js` got `templates/archive/index.md`
added to its `EXCLUDE` set so the archivist's append-only edits to
`index.md` survive `scr init --upgrade`.

## What's next

**Phase 6 — README rewrite for researcher audience.** All v1.1
components now exist; the rewrite can describe the full surface in one
pass without churn. Per `phases/phase-6.md`:

- Section order: intro summary → quickstart → what the framework does
  (workflow narrative, scaffolding, tools/skills) → what's in here
  (component reference) → updates → design philosophy.
- Audience: applied researchers at the May 2026 Córdoba/Cambodia
  kickoff, not framework developers. Quickstart is the entry point;
  design philosophy is at the bottom (load-bearing for contributors,
  not what a researcher needs first).
- Tactical edits already landed in Phases 1–5 (Hooks/Agents tree
  entries, Conventions installed entries) become inputs for the
  rewrite — they're correct in content but live in the old structure.
  Phase 6 reorganizes; it doesn't re-author.
- After Phase 6 ships: the cordoba-lessons plan is itself ready for
  archival via the new `.completed` mechanism. That will be the first
  end-to-end test of the archivist agent on a real plan.

Phase 6 is a single-pass rewrite — likely one or two sessions
depending on how much pruning the design-philosophy section needs.

## Phase 5 verification log

| Gate | Result | Evidence |
|---|---|---|
| Hook: `.completed` present, no sentinel → `decision: block` + sentinel written | ✓ | Scratch `plan/plan-test-foo/.completed`, hook exits 2, stdout is valid `{"decision":"block","reason":"..."}` JSON, `.archival-triggered` lands with ISO-8601 timestamp. |
| Hook: re-Stop after sentinel exists → silent | ✓ | Same scratch with sentinel + `.completed` both present, hook exits 0 with empty stdout. Loop-protection works. |
| Hook: no plan dir → silent (no regression) | ✓ | Empty scratch with `git init`, hook exits 0 silent. |
| Hook: `.completed` AND analysis evidence → archival fires first (insights tripwire deferred) | ✓ | Scratch with `plan/plan-foo/.completed` AND `output/06_chart.png` untracked → archival block JSON emits, exit 2; insights tripwire NOT reached. |
| Hook: NO `.completed` but uncommitted analysis evidence → insights tripwire fires (no regression) | ✓ | Scratch with only `output/06_chart.png` untracked → exit 0, hookSpecificOutput.additionalContext nudge for insights doc. |
| Hook: clean repo (no plan, no analysis evidence) → silent | ✓ | Bare scratch with `git init`, hook exits 0 silent. |
| `scr init`: seeds `archive/` with README.md + index.md | ✓ | Fresh `scr init` output shows `+ archive/README.md` and `+ archive/index.md`. |
| `scr init`: symlinks archivist agent globally | ✓ | `~/.claude/agents/archivist.md` → repo's `.claude/agents/archivist.md` after fresh init. `installGlobals` reports `✓ ~/.claude/agents/ (1 agents linked)`. |
| `scr init --upgrade`: divergent `archive/index.md` preserved (EXCLUDEd) | ✓ | Pre-edited scratch index.md keeps user-appended row; no `.framework-new` sidecar emitted. Control: divergent `insights-logging.md` correctly DOES emit a sidecar. |
| `scr init --upgrade`: divergent pre-Phase-5 `check-insights.sh` → sidecar lands with new Tripwire 1 | ✓ | Simulated old v1 install: original stub untouched, `check-insights.sh.framework-new` written with the new two-tripwire content. |
| Boundary mutual-deference: archivist defers to /research-cleanup | ✓ | Frontmatter description + dedicated section in `agents/archivist.md`; recommends user run `/research-cleanup` after plan-touched-many-source-files cases. |
| Boundary mutual-deference: /research-cleanup defers to archivist | ✓ | New "Boundary with the archivist agent" section in `skills/research-cleanup/SKILL.md`; declares it does NOT touch `plan/` or `archive/`. |
| Pre-housekeeping: four legacy `.completed` markers no longer present | ✓ | `ls plan/` returns only `plan-cordoba-lessons`; the four legacy plan directories deleted; archive entries written for each. |
| `archive/index.md` populated with four entries on first contact | ✓ | `archive/index.md` lists Install Redesign / Project Conventions / Refdocs Conventions / v1 framework with dates and full-archive links. |
| No project-specific cordoba content shipped | ✓ | All Phase 5 framework files (agent, hook, conventions, mechanism doc, README, templates) use generic placeholders (`<slug>`, `<name>`); the four archive entries describe scr-internal plans (install-redesign etc.), not cordoba research. |

## Surprises

- **`install-globals.js` already iterated `.claude/agents/` from
  install-redesign Phase 3.** Phase 5 was scoped to "wire archivist
  symlink in `installGlobals()`" but the work was already done — the
  loop walks every `.md` file in the framework's `.claude/agents/`
  and creates a symlink. Dropping `archivist.md` into the directory
  is plug-and-play. The original task to extend `installGlobals` got
  removed from the task list as misconceived. Same observation extends
  to upgrade.js: agents are symlinks, not project-mirrored, so they
  should NOT be walked by upgrade's per-project file copier — that
  path correctly remains untouched.
- **`upgrade.js` needed one EXCLUDE addition, not a directory walk.**
  The agent didn't need adding to upgrade.js at all (agents go through
  `installGlobals`, not `upgradeProject`), but the new
  `templates/archive/index.md` did need adding to the EXCLUDE set —
  otherwise an `scr init --upgrade` would emit a `.framework-new`
  sidecar against an archive index that the archivist appends to
  across sessions. Found by reasoning about what would happen on a
  long-lived project's second upgrade; verified in scratch.
- **The four legacy archives are larger than the archivist's spec
  suggests.** The spec says 60–150 lines; the v1-framework archive
  came in at ~50 lines (above), the install-redesign at ~70, the
  refdocs/project at ~50 each. v1-framework has more content because
  it's an 8-phase plan with two post-ship simplifications. The spec
  "60–150" is a guideline, not a hard ceiling — the load-bearing
  property is "useful reference, not copy of the plan", and a v1
  archive that omits the manifest-replacement decision would fail
  that test.
- **Sentinel ISO-8601 format is `date -u +"%Y-%m-%dT%H:%M:%SZ"`.**
  scc's stop.js uses `new Date().toISOString()` which emits
  millisecond precision (`2026-05-08T17:34:12.123Z`). The bash port
  drops to second precision because `date` doesn't have a portable
  millisecond format across BSD and GNU. Functionally identical: the
  sentinel is a presence flag, not a timestamp the hook reads back.

## What didn't work

- Initially considered putting the archival tripwire AFTER the
  insights tripwire on the assumption that insights were the more
  common case. Rejected: archival fires once per plan, blocks Stop,
  and is action-required; insights fires repeatedly with non-blocking
  nudges. Putting archival first means a Stop event with both
  conditions emits the higher-priority block immediately, and the
  insights nudge naturally rolls forward to the next Stop after the
  archivist completes. This matches scc's stop.js layering.
- Initially considered making the archivist update `CLAUDE.md`
  unconditionally (mirror scc's behavior). Pulled back: most v1
  plans don't change architecture (they ship seeds, edit prose,
  refactor internals); a CLAUDE.md edit "to be safe" produces churn.
  Spec now says "skip this step entirely if the plan was scoped to
  internal protocol edits, doc rationale, or seeds without an
  architectural surface."
- Initially considered emitting a non-blocking nudge for archival
  (matching the existing insights tripwire shape). Rejected: the
  archivist invocation is a multi-step file mutation; if Claude
  ignores the nudge, the `.completed` marker stays and the next Stop
  re-emits — but a non-blocking nudge can be missed. Blocking with
  sentinel-protection is the right shape: forces the action while
  protecting against re-block loops.

## Implementation hints for Phase 6

- `phases/phase-6.md` describes the rewrite scope in detail. Read it
  once at session start; the rest of `plan.md` is already well-trod.
- Read the **current** README in full before drafting. Many section-
  level edits landed across Phases 1–5 (Conventions installed,
  Hooks tree, Agents tree, Quickstart parenthetical). The rewrite
  reorganizes; it doesn't reauthor — preserve content where the
  intent is correct, just relocate.
- Anchor the rewrite to the section order from `plan.md` Decisions:
  intro → quickstart → workflow narrative → scaffolding map →
  tools/skills reference → what's in here → updates → design
  philosophy. Workflow narrative is new prose (brainstorming →
  planning → implementation → archival, with handoffs) — not in the
  current README.
- The "Tools/skills" section can be a reference table (not the
  current per-skill prose blocks) — researchers want a one-glance
  catalogue, not paragraphs.
- Design philosophy moves to bottom but stays — contributors and
  future-Claude need it. Don't delete; reorder.
- After Phase 6 ships: refresh handoff one last time, mark plan
  complete, `touch plan/plan-cordoba-lessons/.completed`. The
  archivist will run on the next Stop — first real-world test of
  the Phase 5 mechanism.

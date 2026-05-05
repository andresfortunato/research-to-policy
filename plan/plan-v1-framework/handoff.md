# Handoff: plan-v1-framework

**Status:** ACTIVE — Phase 1 complete
**Date:** 2026-05-05
**Last commit on plan branch:** (will be set by the Phase 1 commit immediately after this handoff)

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Foundation: directory layout, settings, install.sh | ✅ done | empty `.gitkeep` placeholders for `.claude/skills/`, `.claude/agents/`, `templates/{wiki,raw,deliverables}/`; install.sh now mirrors them, seeds `manifest.jsonl`, gitignores `plan/ brainstorms/ .scc/` in targets |
| 2 | Wiki layer (Karpathy three-layer) | next | depends on Phase 1 only — parallelizable with Phase 3 |
| 3 | Manifest + reproducibility hook | next | depends on Phase 1 only — parallelizable with Phase 2 |
| 4 | `/verify` + `/deliverable-review` skills | blocked | needs 2 + 3 |
| 5 | Handoff / plan-structure / decision-records conventions | next | depends on Phase 1 only |
| 6 | Research-cleanup skill + deliverable profiles | blocked | needs 5 |
| 7 | Source registry + `/scan-sources` skill | blocked | needs 2 + 3 |
| 8 | Documentation, README, workshop materials | blocked | needs all |

## Where we are

Phase 1 lays the structural bones. New top-level scaffolding directories exist (with `.gitkeep` markers in the framework repo, stripped during install). `install.sh` now handles the new layout idempotently:

- Mirrors `.claude/{conventions,hooks,skills,agents}/` from framework into target
- Mirrors `templates/{wiki,raw,deliverables}/` into target's `wiki/`, `raw/`, `deliverables/`
- Seeds an empty `manifest.jsonl` at target root
- `.gitignore` block now shares `.claude/{conventions,hooks,skills,agents}/` + `settings.json`, and ignores `plan/`, `brainstorms/`, `.scc/`
- `.gitkeep` placeholders are filtered out at install time so they don't propagate

`templates/CLAUDE.md.template` has the new directory tree but no convention-pointer blocks yet (those land per-phase in 2/3/5/7). `settings.template.json` is unchanged structurally — Phase 3 adds PostToolUse, Phase 5 adds PreCompact entries. README's Roadmap is rewritten into "v1 — being built now" / "v1.1 and beyond" sections that match the plan's 8 phases.

## What's next

Two phases unblocked and parallelizable: Phase 2 (wiki layer) and Phase 3 (manifest hook). Either can run next; if a parallel agent team is desired they can run together since their file footprints don't overlap. Phase 5 (handoff/plan/decision conventions) is also unblocked from Phase 1 alone and parallelizes cleanly with 2 and 3 — three-way parallel is feasible.

Sequential reading order to start Phase 2 or 3:
1. `plan/plan-v1-framework/plan.md` — phase summary lives there
2. This handoff — for what's already in place
3. The relevant source files (mostly new files, so just `templates/wiki/` for Phase 2 or `.claude/hooks/` for Phase 3)

## Surprises

- **`.gitkeep` propagation is a real concern.** The first install pass would have copied `.gitkeep` files into target projects, leaving stray placeholders. `copy_if_absent` now filters them. Worth remembering when later phases add more empty scaffolding.
- **`.gitignore` upgrade path is acknowledged but not automated.** Existing installs keep their old block; the install message tells them to review manually. If we ever add many more directories to share, we may want a real upgrade routine — for now the cost-to-benefit isn't there.

## What didn't work

(none yet — Phase 1 went smoothly)

## Verification log

- `bash install.sh /tmp/test-research-project` (fresh) — produces target with new dirs (empty), seeded files (insights/INDEX.md, manifest.jsonl, CLAUDE.md, settings.json), .gitignore with framework block.
- `bash install.sh /tmp/test-research-project` (re-run) — every file reports "exists, skipping"; no duplicates.
- `python3 -c "import json; json.load(...)"` on settings.template.json and target settings.json — both valid.
- `.gitkeep` files NOT present in target — filter works.
- `check-insights.sh` — fires correctly when an analysis artifact is staged without an insights doc; emits the same JSON nudge as before.
- `.gitignore` append behavior — pre-existing rules are preserved, framework block appended below them with a separating blank line; fresh-creation case has no leading blank line.

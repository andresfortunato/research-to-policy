# Handoff: plan-skill-independence

**Status:** Phase 1 complete + verified. Phase 2 next (fresh session).
**Date:** 2026-05-08
**Last commit on plan branch:** `f449044` (Phase 1).

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Vendor + adapt `planning` | ✅ done | SKILL.md (163 lines) + references/multi-session.md (95 lines). All verification gates pass. |
| 2 | Vendor + adapt `implementation` | ⏭ next | Heavier — `references/escalation-reference.md` needs research-domain trigger rewrite. |
| 3 | Vendor + adapt `agent-teams` + ship `scr plan init` + README pass | pending | Last phase; re-touches cordoba-lessons `.completed` at the end. |

## Where we are

Phase 1 vendored `planning` skill + adapted to research domain. Two files landed:
- `.claude/skills/planning/SKILL.md` — 163 lines (target ~150 ± 20).
- `.claude/skills/planning/references/multi-session.md` — 95 lines.

Adaptations applied per `phases/phase-1.md`:
- Project-identity bash block reads `CLAUDE.md` (not `.scc/status/project.md`); warning text adjusted.
- Plan Setup recommends `scr plan init <slug>` (Phase 3) with manual-`mkdir` fallback for now.
- Dropped `tdd` skill cross-reference; replaced with `/verify` + `methods.md` diagnostic-counts pattern + `decisions/` records.
- Frontmatter `description:` tightened to research-domain triggers (research-design plans, methodology calls, multi-phase analyses).
- Verification language: "build passes / tests pass / visual confirmation" → "script runs end-to-end / sign-of-coefficients / chart re-renders with same seed / source citation present / row-count reconciliation."
- Tasks-as-Checkpoints example replaced with EPH working-age-filter example.
- Pointer-Principle example: `App.tsx + WebsiteLayout` → `scripts/03_regress.R + decisions/2026-05-08_identification.md`.
- Cross-references added: `decision-records.md`, `plan-structure.md`, `methods.md`, `brainstorm-format.md` (five-section schema named explicitly).
- `multi-session.md` example reframed as a 4-phase EPH harmonization analysis; dropped `context-monitor` hook reference; renamed `.scc/learnings/` → `learnings/`; renamed UserPromptSubmit hook reference to `retrieve-learnings.sh`.

## Phase 1 verification log

| Gate | Result | Evidence |
|---|---|---|
| `wc -l SKILL.md` ≈ 150 ± 20 | ✓ | 163 lines (within 130–170 band) |
| Frontmatter mentions research/methodology/analysis | ✓ | "research-design plans, methodology calls, or multi-phase analyses" |
| scc-residue grep (`.scc/`, `WebsiteLayout`, `App.tsx`, `tdd skill`, `scc plan init`, `i18n provider`) → 0 matches | ✓ | grep exit 1 (no matches) on both files |
| Software-residue smoke check (`react`, `jsx`, `frontend`, `backend`, `API endpoint`, `component`) → 0 matches | ✓ | grep exit 1 |
| Brainstorm-handoff contract preserved (5-section schema named) | ✓ | "Problem", "Decisions Made", "Research Findings", "Open Questions", "Constraints Identified" all present in "Consuming brainstorming output" |
| Project-identity reads `CLAUDE.md`, not `.scc/status/project.md` | ✓ | line 7 of SKILL.md |
| Symlink mechanism wired (no installer change needed) | ✓ | `src/lib/install-globals.js:43-52` walks `.claude/skills/` and symlinks each subdir; new `planning/` directory will be picked up at next `scr init` |

## What's next

**Phase 2 — Vendor + adapt `implementation` skill.** Read `phases/phase-2.md`. Source: `~/github/super-claudio-code/skills/implementation/{SKILL.md, references/escalation-reference.md}`. The references file is the heaviest lift in this plan — escalation triggers need full research-domain rewrite (the structure stays; the trigger list re-shaped from "API contract change", "auth flow", etc. → research-domain triggers like "deflator chain change", "identification spec swap", "vintage-break discovery").

## Implementation hints for Phase 2

- Reuse the language choices anchored in Phase 1: verification phrasing, example shape, cross-reference targets. Don't re-derive.
- The implementation SKILL.md cross-refs the planning skill — confirm the phrasing matches what shipped in Phase 1 (e.g., references to "Plan Completion", "Consuming brainstorming output", "/verify", `methods.md`, `decision-records.md`).
- `escalation-reference.md` is the judgment-heavy file. The structure (severity tiers, trigger list with examples) stays; the triggers themselves need full domain rewrite. Research-domain triggers: contradicted methodology assumption, vintage-break discovery, sign-flip vs brainstorm prediction, source-citation gap, sample-size collapse, deflator divergence, fixed-effects spec change, etc.
- The Plan Completion section of implementation drops the `cleanup` subagent line — only the `archivist` agent runs post-`.completed` (per plan.md decision).
- `.scc/status/plan-[name].md` references → drop entirely; `handoff.md` is scr's source of truth. `.scc/learnings/` → `learnings/`.
- Verification gates same shape as Phase 1: line count band, frontmatter, scc-residue grep, software-residue smoke check, cross-ref correctness.

## Surprises

- The user's `~/.claude/skills/planning` currently symlinks to scc's planning skill (last installer was scc). The system reminder during this session showed *both* `planning` skill descriptions in the available-skills list — the new scr-shipped description registered alongside the global symlink. The plan's "last installer wins" precedence note is the right approach; documenting it in Phase 3's README pass remains the deferred work.
- `.claude/skills/planning/references/multi-session.md` came in at 95 lines — slightly tighter than the 96-line scc original, despite domain rewrites and an extended handoff example. The compaction came from dropping the context-monitor hook reference (3 lines) and consolidating the prose around the EPH example.

## What didn't work

- No dead ends this phase — the surgical-adaptation pattern from cordoba-lessons Phase 5 (mechanical swaps first, then domain rewrites, then verify) carried over cleanly. Reading the scc skill in full once at the start (per the plan's implementation hint) was enough; no re-reading needed during the rewrite.

# Handoff: plan-skill-independence

**Status:** Phase 2 complete + verified. Phase 3 next (fresh session).
**Date:** 2026-05-08
**Last commit on plan branch:** `45b12da` (Phase 2). Phase 1 at `f449044`.

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Vendor + adapt `planning` | ✅ done | SKILL.md (163 lines) + references/multi-session.md (95 lines). All gates pass. |
| 2 | Vendor + adapt `implementation` | ✅ done | SKILL.md (175 lines) + references/escalation-reference.md (90 lines). All gates pass. |
| 3 | Vendor + adapt `agent-teams` + ship `scr plan init` + README pass | ⏭ next | Last phase; re-touches cordoba-lessons `.completed` at the end. |

## Where we are

Phase 2 vendored `implementation` skill + adapted to research domain. Two files landed:
- `.claude/skills/implementation/SKILL.md` — 175 lines (target 165 ± 20).
- `.claude/skills/implementation/references/escalation-reference.md` — 90 lines (no spec; scc was 69, +21 lines covers the two new research-only triggers).

Adaptations applied per `phases/phase-2.md`:
- Frontmatter `description:` mentions research workflow + `.completed`-driven archival explicitly.
- "Code is ground truth" → "The artifact is ground truth"; ground-truth pointers updated to `output/` (charts/tables/.meta.json) and `insights/`.
- "Verify with evidence" rewritten with research defaults (script runs end-to-end with same seed; diagnostic counts match `methods/<slug>/rule.md`; downstream insights cite the artifact correctly). Cross-refs added to `/verify` (≤2k tokens, per-artifact) and `/deliverable-review` (≤12k tokens, multi-lens).
- TDD cross-reference dropped.
- `context-monitor` hook reference replaced with one-line `precompact-handoff.sh` mention; PreCompact hook line in Session End updated to name `precompact-handoff.sh`.
- "Record what didn't work" → `learnings/<slug>.md` (not `.scc/learnings/`); cross-link `learning-capture.md`. Examples reframed as research-shaped (sample-size collapse, PONDII vintage absence, 2018Q3 break).
- Parallelization teammate output dir: `output/[task-name]/` → `scratch/[task-name]/` with rationale sentence (avoid colliding with project's analytical `output/`).
- Session End: `.scc/status/plan-[name].md` line dropped entirely. `handoff.md` is source of truth.
- Plan Completion: cleanup subagent dropped. Section expanded to scr's Phase-5 protocol — Tripwire 1 of `check-insights.sh` is BLOCKING; `.archival-triggered` sentinel for loop-protection; archivist synthesizes `archive/plan-[name].md` (60–150 lines), appends to `archive/index.md`, optionally edits `CLAUDE.md`, deletes plan dir. Cross-references `docs/plan-archival-mechanism.md` and `.claude/agents/archivist.md`.
- escalation-reference.md: kept all six scc trigger headers (Contradicted Assumption, Debugging Spiral, Invalidated Future Phase, Unresolvable Ambiguity, Missing External Dependency, Scope Expansion) with research-rewritten examples; added two research-only triggers (Sample Restriction Surprise, Data Quality Issue).

## Phase 2 verification log

| Gate | Result | Evidence |
|---|---|---|
| `wc -l SKILL.md` ≈ 165 ± 20 | ✓ | 175 lines (within 145–185 band) |
| Frontmatter `description:` mentions research + `.completed`-driven archival | ✓ | "research plan", "Drives the full session lifecycle through to `.completed`-driven archival via the archivist agent" |
| scc-residue grep (`.scc/`, `tdd skill`, `context-monitor hook`, `cleanup subagent`, `cleanup agent`) → 0 matches | ✓ | grep exit 1 on both files |
| Software-residue smoke (`react`, `jsx`, `frontend`, `backend`, `API endpoint`, `component`, `UserContext`, `AuthContext`) → 0 matches | ✓ | grep exit 1 on both files |
| Plan Completion names archivist as ONLY post-`.completed` agent | ✓ | line 166 of SKILL.md: "archivist is the **only** post-`.completed` agent" |
| Active-plans / latest-handoff bash blocks execute unmodified | ✓ | smoke test prints `plan-cordoba-lessons` and `plan-skill-independence` + their handoff heads |
| Teammate output dir uses `scratch/` not `output/` | ✓ | line 108 of SKILL.md: `plan/plan-[name]/scratch/[task-name]/` with rationale |
| `/verify` and `/deliverable-review` cross-refs present | ✓ | line 37 of SKILL.md |
| `precompact-handoff.sh` mention present | ✓ | lines 51 and 142 of SKILL.md |
| `learnings/<slug>.md` (not `.scc/learnings/`) referenced | ✓ | lines 64 and 148 of SKILL.md |
| At least 5 research-shaped triggers in escalation-reference.md | ✓ | 8 triggers (### 1–### 8); all examples research-domain (deflator/EPH/wage/methodology/fixed-effects/panel/coefficient/methods/ — 13 matches) |
| Sample-restriction + data-quality additions present | ✓ | ### 7 Sample Restriction Surprise; ### 8 Data Quality Issue |
| Symlink mechanism wired | ✓ | `installGlobals()` walks `.claude/skills/`; new `implementation/` dir picked up at next `scr init` (same mechanism Phase 1 used; no installer change) |
| Cross-references to `planning` skill match Phase 1 phrasing | ✓ | "that's the planning skill" (line 24); "Plan Completion" section name preserved |
| Referenced support files exist | ✓ | `.claude/agents/archivist.md`, `.claude/hooks/check-insights.sh`, `.claude/hooks/precompact-handoff.sh`, `docs/plan-archival-mechanism.md` all present |

## What's next

**Phase 3 — Vendor + adapt `agent-teams` skill + ship `scr plan init <slug>` + README pass + `docs/skill-independence-mechanism.md` + TODO bump.** Read `phases/phase-3.md`. Heaviest phase by file count but each individual change is light:

- `.claude/skills/agent-teams/SKILL.md` (+ any references files scc ships) — research-adapted port. Cross-refs the implementation skill (now shipped); the parallelization-detection language in this skill should match the Parallelization section's phrasing in `.claude/skills/implementation/SKILL.md` (lines 99–112).
- `src/cli.js` — wire the `scr plan init <slug>` subcommand.
- `src/lib/plan-init.js` — scaffold `plan/plan-<slug>/{plan.md, handoff.md, log.md, phases/, context/}`.
- `docs/skill-independence-mechanism.md` — mechanism doc explaining the vendor-and-adapt choice + last-installer-wins precedence note.
- `README.md` — drop `(scc, global)` annotations from the skills table for `/planning` and `/implementation`; add precedence note for users with scc installed; update Quickstart so it no longer suggests scc dependency.
- `TODO.md` — mark skill-independence shipped; bump v1.2 candidates.
- **Final action**: re-touch `plan/plan-cordoba-lessons/.completed` so cordoba-lessons archives **after** skill-independence (per plan.md Repo Context).

## Implementation hints for Phase 3

- Reuse Phase 1 + Phase 2 anchored language: verification phrasing ("script runs end-to-end / sign-of-coefficients / source citation / row-count reconciliation"), example shape (deflator chains, identification specs, methods/<slug>/rule.md, decisions/<date>_<slug>.md, output/), cross-reference targets (`/verify`, `/deliverable-review`, `learning-capture.md`, `decision-records.md`, `plan-structure.md`, `methods.md`, `brainstorm-format.md`, `precompact-handoff.sh`, `check-insights.sh`, archivist agent).
- `agent-teams` SKILL.md likely cross-refs implementation. Check that the phrases used match Phase 2's Parallelization section: `scratch/[task-name]/` (not `output/`), "lead consolidates results into handoff.md", "propagation problem" framing.
- `src/lib/install-globals.js` already iterates `.claude/skills/`, so the new `agent-teams/` directory will be picked up automatically. No installer change needed for the skill itself.
- `scr plan init <slug>` is a small CLI subcommand. Phase-1 SKILL.md already references it ("`scr plan init <slug>` (added in scr v1.2)"); that line resolves once the subcommand ships in Phase 3. Test by running `scr plan init test-slug` in a scratch directory and confirming the directory tree matches the plan setup recommended by `.claude/skills/planning/SKILL.md` (lines 119–123 reference the scaffolding contract).
- README pass: the current README's skills table (post-Phase-6 cordoba-lessons rewrite) annotates `/planning` and `/implementation` as `*(scc, global)*`. Drop those annotations. Add a one-line precedence note: "If you also have scc installed, last-installer-wins symlinks — `scr init` after `scc init` makes scr's skills authoritative; vice versa makes scc's authoritative."
- `docs/skill-independence-mechanism.md` should be short (40–80 lines): why vendor + adapt vs require scc co-install (distribution gap; researcher onboarding shouldn't require two npm installs), what was vendored (planning, implementation, agent-teams), what wasn't (tdd, cleanup), how the symlink precedence resolves, when scr should re-pull from scc upstream (only if scc evolves the load-bearing structure — verification protocol, escalation framing, lifecycle protocol).
- Re-touching cordoba-lessons `.completed` is the **last** action of Phase 3 — `touch plan/plan-cordoba-lessons/.completed`. Don't do it earlier; the next Stop event will fire archivist for cordoba-lessons, which is fine after skill-independence's commits are in place.

## Surprises

- The user's `~/.claude/skills/implementation` symlink (pointing to scc's skill) and the new scr-shipped one register **both** descriptions in the available-skills list, mirroring the Phase 1 observation for `planning`. The two-entry pattern is now confirmed across both vendored skills; Phase 3's README precedence note is the right place to document it.
- escalation-reference.md ended up at 90 lines vs scc's 69 — the +21 lines is exactly the two new research-only triggers (~10 lines each). The six-trigger structure stayed; the research rewrites of the existing six were near-zero net (1–2 sentences in/out per example). The compactness held.
- All four cross-referenced support files (`archivist.md`, `check-insights.sh`, `precompact-handoff.sh`, `plan-archival-mechanism.md`) shipped in cordoba-lessons Phase 5; Phase 2 only has to reference them, not author them. The Plan Completion section is significantly more detailed than scc's because scr's lifecycle protocol (Tripwire 1 BLOCKING + `.archival-triggered` sentinel + 60–150 line archive entry contract) is more specific than scc's two-subagent-line gesture.

## What didn't work

- No dead ends this phase. The Phase 1 anchored language (verification phrasing, example shape, cross-reference targets) carried directly into Phase 2 — no re-derivation. The escalation-reference rewrite was the heaviest single piece of writing, but the structure-preserves-examples-rewrite split kept it surgical.
- Initial draft of escalation-reference.md examples ran longer than scc's. Tightened by holding to scc's 1–2 sentence example budget per trigger; research-domain specificity stayed but verbose qualifiers got cut.

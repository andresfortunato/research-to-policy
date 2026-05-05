# Handoff: plan-v1-framework

**Status:** ✅ COMPLETE — all 8 phases shipped. Ready for archival.
**Date:** 2026-05-05
**Last commit on plan branch:** to be filled in after this session's commit

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Foundation: directory layout, settings, install.sh | ✅ done | b9dc29b |
| 2 | Wiki layer (Karpathy three-layer) | ✅ done | df4e53a |
| 3 | Manifest + reproducibility hook | ✅ done | df4e53a |
| 4 | `/verify` + `/deliverable-review` skills | ✅ done | 1042f9f |
| 5 | Handoff / plan-structure / decision-records conventions | ✅ done | df4e53a |
| 6 | Research-cleanup skill + deliverable profiles | ✅ done | 1042f9f |
| 7 | Source registry + `/scan-sources` skill | ✅ done | 1042f9f |
| 8 | Documentation, README, workshop materials | ✅ done | this session |

## Where we are

This session ran Phase 8 — solo, sequential, the final docs-and-polish phase. Three things landed:

1. **Framework-repo `.gitignore`** — one line (`.DS_Store`). Resolves the long-standing untracked-file noise.
2. **`docs/audience-and-philosophy.md`** — the design constitution. Two-audience framing (researchers evaluating + contributors extending). Eight design principles (silent-by-default, conditional-not-always-fire, composable, project-shared, short CLAUDE.md, markdown-first, stakes-graded verification, open-source-from-day-one) each with a one-paragraph statement and a concrete example. Ends with a "principles ↔ proposed addition" check table — the gate any new convention/hook/skill must pass. Also lists what the framework deliberately is *not* (no orchestration, no PM dashboard, no agent-of-agents, no always-on quality gates, no LLM-managed source-of-truth code).
3. **`README.md` rewrite** — restructured "Conventions installed" to cover all v1 components: source-registry + `/scan-sources`, `/verify`, `/deliverable-review`, `/research-cleanup`, deliverable profiles. Updated "What's in here" tree to show six skills + agents/manifest-checker.md + nine docs + the three deliverable profiles inline. Trimmed the v1-build-progress table entirely — Roadmap now contains only v1.1+ deferrals. Added a one-line pointer to `docs/audience-and-philosophy.md` from the top-of-file design-philosophy section.

Workshop materials skipped per plan: "outline-only; full slides built later in PowerPoint by the user."

## What's next

**Nothing for this plan.** v1 is shipped. After commit + push:
1. User confirms plan completion.
2. `touch plan/plan-v1-framework/.completed` triggers the archivist + cleanup subagents (per the implementation skill's plan-completion protocol).
3. Archivist synthesizes `archive/plan-v1-framework.md` from this handoff + log.md + the brainstorm; cleanup scans the file manifest for dead code.

Future framework work (post-archive):
- Pilot use surfaces what to revisit. Likely candidates: deliverable-profile length targets, `/scan-sources` rate-limit defaults, lens-weighting tables.
- v1.1 conventions (`evidence-ledger`, `chart-registry`, `citation-discipline`) when a real engagement surfaces the need.
- LaTeX/Beamer add-on borrowed from Pedro/Hugo Sant'Anna when register shifts academic.

## Surprises

- **The README "v1 — build progress" table outlived its usefulness once everything shipped.** Originally a project-tracking aid for researchers watching the build land. Once shipped, the table just adds noise — every row says ✅ shipped. Deleted it; the new Roadmap section is one short paragraph saying "v1 is shipped, see plan/plan-v1-framework/plan.md for build history" plus the v1.1+ deferral list.
- **The "Design philosophy" section at the top of README and `docs/audience-and-philosophy.md` overlap deliberately.** README has the four-principle short version (most users won't read further); the doc has the full eight. Added a one-line pointer from README to the doc. The four-vs-eight gap is intentional — silent-by-default and conditional-not-always-fire are the same idea split into two principles in the doc, and markdown-first / stakes-graded / open-source-from-day-one weren't in the original README list.
- **The constitution doc doubles as a contributor gate.** Its closing table ("if a proposed addition fails one of these and the failure is intentional, the constitution gets revised first — explicitly, in this document — before the addition lands") is the explicit policy that keeps the framework small over time. Without that statement, the design principles are just descriptive; with it, they're prescriptive.
- **No workshop/ directory.** The plan said "optional, outline-only, full slides built later in PowerPoint by the user." Decided not to ship even an outline — the workshop is engagement-specific (Córdoba/Cambodia kickoff) and the plan's open-source-from-day-one constraint argues against committing engagement-specific materials. The user will build PowerPoint slides directly. Reflagged this in the philosophy doc under "open-source from day one."

## What didn't work

Nothing this session — Phase 8 is small enough that no approach got abandoned. The plan was concrete, the file footprint was tight, and the install verification cleared first try.

## Verification log

- `bash install.sh /tmp/scc-v1-phase8-test` (fresh) — every previously-shipped file landed; new docs entry (`audience-and-philosophy.md`) present in `docs/`. No new install.sh changes were needed (Phase 8 only edits committed-already files + adds a doc + adds a framework-repo .gitignore that doesn't propagate to targets).
- `grep -E '^## (Insights Logging|Wiki|Manifest Logging|Handoff Format|Plan Structure|Decision Records|Source Registry)$' /tmp/scc-v1-phase8-test/CLAUDE.md` — all SEVEN pointer blocks still present (no regression from Phase 7).
- `ls docs/ | grep -E '\.md$'` — nine docs files: audience-and-philosophy, extending, handoff-mechanism, insights-mechanism, manifest-mechanism, plan-structure-mechanism, source-registry-mechanism, verification-architecture, wiki-architecture.
- `cat .gitignore` (framework repo, not target) — single line `.DS_Store`.
- `git status --short` — clean except the three Phase 8 changes (modified README.md, untracked .gitignore + docs/audience-and-philosophy.md). `.DS_Store` no longer untracked (caught by the new framework .gitignore).
- README is internally consistent: tree section, conventions section, and roadmap section all reference the same six skills, six conventions, and three deliverable profiles.

## Hash trail
- Phase 1: b9dc29b
- Phase 2/3/5 work: df4e53a
- Phase 2/3/5 handoff: 43526ec
- README polish (interim): 1a92005
- Prior handoff refresh: b731b59
- Phase 4/6/7 work: 1042f9f
- Phase 4/6/7 handoff refresh: a518d2b
- Handoff hash trail fill-in: c912903
- **Phase 8 work: <to be filled in after commit>**

## Known minor items (not blocking — list closed by Phase 8)

- ~~`.DS_Store` untracked in framework repo~~ → resolved by framework `.gitignore`.
- ~~README needs `jq` prerequisite + entries for /verify, /deliverable-review, /research-cleanup, profiles, /scan-sources, source-registry~~ → all done.
- ~~Roadmap should be empty for v1; only v1.1+ deferrals~~ → done.

Open across-version notes for follow-up:
- Seven-lens names from `/deliverable-review` are referenced in the deliverable profile lens-weighting tables. If lens names ever change, the profiles need to update too.
- Phase 7 scratch-edit files at `plan/plan-v1-framework/output/phase-7/` are committed as audit trail. The archivist subagent should clean these up at archive time.

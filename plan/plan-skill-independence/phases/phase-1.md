# Phase 1 — Vendor + adapt `planning` skill

Read `plan.md` for the goal, constraints, decisions, file manifest, and repo context. This file scopes Phase 1.

## Intent

Copy `~/github/super-claudio-code/skills/planning/{SKILL.md, references/multi-session.md}` into `.claude/skills/planning/`, adapt language and cross-references to the research domain. The bones of the skill (intent over implementation, constraints over instructions, decisions as records, tasks as checkpoints, context budget, multi-session design) are domain-neutral and stay verbatim. The adaptations are surgical: swap SE examples for research examples, swap SE verification language for domain-shaped verification, swap scc-specific paths/commands/cross-references for r2p equivalents.

## Files

- ✚ `.claude/skills/planning/SKILL.md`
- ✚ `.claude/skills/planning/references/multi-session.md`

## Adaptations

### Mechanical swaps (no judgment)

- Project-identity bash block at the top: `cat .scc/status/project.md` → `cat CLAUDE.md` (researcher's project-orientation file, seeded by `r2p init`). Adjust the warning text accordingly: instead of "create `.scc/status/project.md`", say "ensure `CLAUDE.md` exists at project root — `r2p init` seeds it from the framework template."
- Plan Setup section: replace `Run \`scc plan init [name]\`` with `Run \`r2p plan init <slug>\` (added in Phase 3 of plan-skill-independence) — or scaffold the directory manually with \`mkdir -p plan/plan-<slug>/{phases,context}\`.`
- Drop `tdd` skill cross-reference; replace with `/verify` cross-reference and a pointer to `methods.md`'s "diagnostic counts" pattern + `decisions/` records.
- Frontmatter `description:` field: tighten the trigger language to research-domain ("research-design plans, methodology calls, multi-phase analyses").

### Domain-shaped rewrites (judgment)

- "Verification criteria" examples throughout: "build passes / tests pass / visual confirmation" → "script runs end-to-end / sign-of-coefficients hold / chart re-renders with same seed / source citation present / numbers reconcile to the prior insight."
- "What Goes in a Plan / Must Have" — keep the structure; rephrase "Behavioral test lists" entry: "Verification gates per phase — domain-shaped (sign-of-coefficients, magnitude sanity, source citation present, breakpoint alignment), not unit tests. See `plan-structure-mechanism.md`."
- "Tasks as Checkpoints" examples: replace the `WebsiteLayout / App.tsx / i18n` example pair with a research example. Suggested:
  - **Bad:** "Open scripts/01_clean.R; add filter for adults; save to data/processed/."
  - **Good:** "Apply working-age filter (15–64) to the EPH harmonized panel; save to `data/processed/eph_working_age.csv`. Verify: row count matches `methods/working-age-filter/rule.md` diagnostic counts; no NA in the age column; commit message has Run/Out lines."
- "The Pointer Principle" example: "Modify App.tsx to add WebsiteLayout wrapper" → "Modify `scripts/03_regress.R` to swap the city fixed-effects spec for the matched-pairs spec defined in `decisions/2026-05-08_identification.md`."
- "Context Files" examples: software-shaped → research-shaped (a context file might describe how `data_sources/world_bank_api.md` interacts with the project's deflator chain, or how `methods/age-cohort-definition/rule.md` evolves vN-to-vN+1).
- "Recommended Plan Structure" code block: keep the structure verbatim; add a sentence after noting that research plans naturally cross-link `decisions/`, `methods/<slug>/rule.md`, and `data_sources/`.

### Cross-references to add

The vendored skill should explicitly cross-reference r2p's existing conventions when the research adaptation is load-bearing:

- "Decisions Made" section → cross-link `decision-records.md` (when a brainstorm decision graduates to a peer-reviewable methodology call, file at `decisions/YYYY-MM-DD_<slug>.md`).
- "Verification" — cross-link `plan-structure-mechanism.md` ("verification is domain-shaped, not code-shaped").
- "Consuming brainstorming output" — cross-link `brainstorm-format.md`'s five-section schema explicitly. The handoff contract is that contract.

### references/multi-session.md

Light adaptation: skim for code-shaped language. Specific fixes likely needed:
- Session-scoping examples reframed for research (a 4-phase identification analysis spanning 3 sessions, not a frontend migration).
- Handoff prose stays mostly verbatim (handoff-format.md and r2p's existing handoff convention align with scc's protocol already).

## Verification

- `wc -l .claude/skills/planning/SKILL.md` ≈ 150 ± 20 (preserves scc's structure; adaptations don't add bulk).
- Frontmatter `description:` mentions research/methodology/analysis explicitly.
- `grep -E "\.scc/|WebsiteLayout|App\.tsx|tdd skill|scc plan init|i18n provider"` against the new SKILL.md → 0 matches.
- Symlink: a fresh scratch project + `r2p init` results in `~/.claude/skills/planning/` → `<r2p-repo>/.claude/skills/planning/`. (No installer change needed; `installGlobals()` already walks `.claude/skills/`.)
- Brainstorm-handoff contract preserved: SKILL.md still has a "Consuming brainstorming output" section that names the five-section schema (Problem / Decisions / Research / Open Questions / Constraints).
- Project-identity bash block reads `CLAUDE.md`, not `.scc/status/project.md`.
- Examples throughout are research-shaped (no JSX, no npm install, no test runners). Smoke-test: `grep -iE "react|jsx|frontend|backend|API endpoint|component"` → 0 matches. (If a generic word like "API" survives in a non-software context, that's fine; the grep is a smoke-check, not a hard gate.)

## Dependencies

Upstream: none. Ships first; adaptation choices made here anchor Phases 2 and 3.
Downstream: Phase 2 (implementation skill cross-refs the planning skill); Phase 3 (agent-teams cross-refs both, CLI command is recommended by planning, README updates the skills table).

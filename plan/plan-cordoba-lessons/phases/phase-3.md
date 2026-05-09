# Phase 3 — Brainstorming skill

Read `plan.md` for the goal, constraints, decisions, file manifest,
and repo context that govern all phases. This file scopes Phase 3.

## Intent

Port scc's `brainstorming` skill into r2p. The skill produces
`brainstorms/<topic>.md` with a Decisions / Research / Open-questions
structure and triggers "the planning skill" (whichever is installed).
cordoba's `Spatial Equilibrium Plan in Cordoba.txt` — a methodology
essay that felt like a plan but never became one — is the
cautionary tale.

## Files

- `.claude/skills/brainstorming/SKILL.md` (new) — adapted port of
  `~/github/super-claudio-code/skills/brainstorming/SKILL.md`.
  Domain examples shifted from web-app design (CRDT vs OT,
  WebSocket vs polling) to applied research (deflator choice,
  identification strategy, reference-category selection,
  survey-vintage breakage). Output path: `brainstorms/<topic>.md`
  (existing `brainstorms/` directory in CLAUDE.md.template tree).
  Trigger: "the planning skill" — agnostic about whose. Output
  structure same as scc (Problem / Decisions Made / Research /
  Open Questions / Constraints).
- `.claude/conventions/brainstorm-format.md` (new) — short
  convention documenting the brainstorm doc shape and the
  handoff-to-planning expectation. Cross-link to the skill.
- `templates/brainstorms/README.md` (new) — one-line orientation:
  "Decisions-pre-planning. Output of `/brainstorming` skill."
- `docs/brainstorm-mechanism.md` (new) — rationale: why
  brainstorms are distinct from `/verify` (verify is per-artifact
  sanity-check; brainstorm is decisions-before-execution); why
  `brainstorms/` is gitignored in target projects (decisions are
  captured in `decisions/` records, not in brainstorms);
  cordoba's methodology essay as the cautionary tale.
- `templates/CLAUDE.md.template` — pointer block: name +
  when-to-apply + "see `.claude/conventions/brainstorm-format.md`";
  ≤6 lines. Codebase-tree gloss for `brainstorms/`.
- `src/lib/install-project.js` — seed `templates/brainstorms/` on
  init; symlink the new skill globally.
- `README.md` — "Conventions installed" entry; "Skills installed"
  entry. (Tactical edit; full rewrite is Phase 6.)

## Verification

- Skill triggers on the same triggers as scc's (synonyms in
  research domain — "how should we measure...", "what's the right
  deflator...", "let's think about identification").
- Skill output file lands at `brainstorms/<topic>.md` and matches
  the documented structure.
- Skill terminates cleanly when the user says "go to planning" —
  handoff is "the planning skill" agnostic, no scc-specific
  machinery.
- `r2p init --upgrade` on a v1 project lands the new skill
  globally; existing brainstorm files (if any) untouched.

## Dependencies

Upstream: Phase 1 (web-scraping skill exists; brainstorming may
reference it as one of several skills available — soft dep);
Phase 2 (mentions theme-aware brainstorm filenames as opt-in).
Downstream: Phase 6 (README rewrite covers brainstorming as the
first stage of the workflow).

## Reference patterns

Upstream skill: `~/github/super-claudio-code/skills/brainstorming/SKILL.md`.
Read once, then write the r2p version against the existing
`.claude/conventions/`-shape (intent doc at `docs/<name>-mechanism.md`,
protocol at `.claude/conventions/<name>.md`, seeds at `templates/<dir>/`).

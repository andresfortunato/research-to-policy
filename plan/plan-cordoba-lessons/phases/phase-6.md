# Phase 6 — README rewrite (researcher audience)

Read `plan.md` for the goal, constraints, decisions, file manifest,
and repo context that govern all phases. This file scopes Phase 6.

## Intent

Rewrite `README.md` for the audience that matters at the May 2026
kickoff: applied researchers, not framework contributors. The
current README reads as a constitution-and-component-catalogue
(design principles up front, every convention/skill explained in
turn). A researcher installing scr for the first time should land
on quickstart, see the workflow narrative (brainstorming → planning
→ implementation, with handoffs), see the scaffolding, and see the
tool reference — *before* the design philosophy. Ships last because
every preceding phase changes what the README has to describe;
rewriting against a moving target wastes effort.

## Files

- `README.md` — full rewrite with the section order below.
  Existing intro paragraph kept (the framing is good); the
  rest is restructured.

## Section order (top → bottom)

1. **Intro summary** — kept from current README; sets up "Claude
   Code is for software engineers; research has different
   rhythms; here's the harness that adapts it."
2. **Quickstart** — install via npm (existing flow), `scr init`
   in a research project, run a tiny worked example
   (`/brainstorming` → `/planning` → first analysis script
   with header → first insight doc). One-screen, copy-pasteable.
3. **What the framework does.** Three subsections in this order:
   - **Workflow: brainstorming → planning → implementation
     (with handoffs).** Narrative walk-through using a generic
     research example (e.g., "you're testing a hypothesis about
     wage gaps across cities"). Cross-references the
     brainstorming, planning, and implementation skills;
     the handoff convention; the decision-records convention;
     the insights-logging convention. Plain prose, no
     constitution language.
   - **Scaffolding and project structure.** Annotated tree
     showing what `scr init` lays down. Maps each folder to
     its purpose in plain English (`insights/` = "evidence-based
     findings"; `decisions/` = "methodology calls you'd defend
     in peer review"; `methods/` = "operational rules with
     diagnostic counts"; `learnings/` = "tacit gotchas worth
     remembering"; etc.). Theme-parallel opt-in mentioned here
     as a one-paragraph note.
   - **Tools and skills.** Reference table: skill/agent/hook
     name, what it does in one line, when to invoke it. Group
     by lifecycle moment (before-execution, during-execution,
     end-of-session, end-of-plan). The current "Conventions
     installed" section becomes a sibling table.
4. **What's in here.** The existing repository tree (current
   README's lines 18–70) — moved here, kept as reference for
   contributors. Section now reads as "if you want to look at
   the framework's own internals."
5. **Updates.** A short section pointing at git tags / release
   notes / TODO.md. Where to find changes between versions;
   how to upgrade an existing project (`scr init --upgrade`
   flow, sidecars, manual merge).
6. **Design philosophy.** Moved to the bottom. The
   eight-principle constitution (silent-by-default,
   conditional-not-always-fire, etc.) — load-bearing for
   anyone proposing new conventions/hooks/skills, but not
   what a researcher needs to read first. Cross-link
   `docs/audience-and-philosophy.md` for full text.

## Verification

- First-time-reader test: a researcher unfamiliar with scr
  can read top-down and reach a working install + first
  insight doc within ~10 minutes. Tested by reading the
  rewrite cold.
- Quickstart code blocks all execute as written (no stale
  flags, no missing steps).
- Workflow narrative names all three core skills
  (brainstorming, planning, implementation) and shows how
  they hand off to each other. The handoff convention is
  referenced inline, not in a separate section.
- Tool/skill reference table covers all v1.1 components
  (8 skills, 1 agent, 3 hooks, 12 conventions) — no
  component is undocumented.
- Design philosophy section preserves the full
  eight-principle constitution (no content lost, only
  moved).
- Convention pointer blocks in `templates/CLAUDE.md.template`
  (per-project) and the README "Conventions installed" table
  do NOT duplicate prose — the README links to the
  convention file, the CLAUDE.md template links to the
  convention file, the convention file is the single source
  of truth.
- `wc -l README.md` band: rewrite should be in roughly the
  same total length as v1 (current ~190 lines) ± 30%.
  Significantly longer means we duplicated convention prose;
  significantly shorter means we lost component coverage.

## Dependencies

Upstream: Phases 1–5. README rewrite must describe the v1.1
surface — components added across Phases 1–5 must all exist
before the rewrite lands, otherwise the rewrite has to be
patched as each phase ships. Single rewrite at the end avoids
churn. Tactical README edits in earlier phases (one-line
additions noting new skill/hook) are temporary scaffolding
that this rewrite supersedes.

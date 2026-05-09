# Log: plan-cordoba-lessons

## 2026-05-08 — plan written

- Diagnostic source: `~/cordoba` audit run during this conversation.
  ~22 R/Python scripts, ~4900 LOC, four parallel lines of inquiry,
  no r2p conventions installed. Surfaced 7+ framework gaps and 3
  scc components worth porting.
- Brainstorm consumed in-conversation (no separate
  `brainstorms/<topic>.md` written — discussion was tight enough
  that the plan's "Decisions Made" carries the load).
- Resolved 5 open questions during planning:
  - Theme-parallel: Path A (opt-in subfolder) — confirmed by user.
  - Hook implementation language: bash (constitution-mandated;
    no JS leakage outside `src/`).
  - Phasing: one plan with 5 phases, not split into separate
    plans — confirmed by user that the cordoba narrative is
    cohesive enough.
  - Theme as free-form vs declared: free-form. No `themes.md`
    declaration; lowercase-snake-case suggested only.
  - Learning-capture theme-awareness: project-wide, not theme-aware
    (gotchas are universal lessons; trigger-keyword retrieval
    routes them).
- Plan slug: `cordoba-lessons` — chosen over `framework-v1-1` for
  diagnostic specificity.
- Scope split confirmed: this plan = improve framework based on
  cordoba lessons. A second plan (post-v1.1) = retrofit/triage
  workflow for onboarding r2p into existing disorganized projects.
- 5 phases initially, strict sequential order: small wins →
  theme-parallel → brainstorming → learning-capture+hooks → plan
  archival. Theme-parallel intentionally landed before the new
  conventions/skills/hooks so they're theme-aware-by-default
  rather than retrofitted.

## 2026-05-08 — plan revised (user review pass 1)

- **Phase 6 added: README rewrite for researcher audience.** Current
  README reads as a constitution-and-component catalogue (design
  principles up front). Audience that matters at the May 2026
  kickoff is applied researchers, not framework contributors. New
  section order: intro summary → quickstart → what the framework
  does (workflow narrative, scaffolding, tools/skills) → what's
  in here → updates → design philosophy (last). Ships after
  Phases 1–5 land all components, so the rewrite describes a
  stable surface.
- **Archivist / `/research-cleanup` boundary made explicit.** The
  archivist agent (Phase 5, hook-triggered, per-plan) and the
  `/research-cleanup` skill (existing v1, user-invoked, project-wide)
  are complementary, not redundant. Phase 5 now requires:
  (a) archivist prose explicitly defers project-wide cleanup to
  `/research-cleanup`; (b) `/research-cleanup` SKILL.md gets a
  "Boundary with archivist agent" paragraph; (c) verification
  includes a consistency check (run both in scratch project,
  confirm non-overlapping output). One automation, one ad-hoc
  skill — no duplicated cleanup logic.
- TODO.md items NOT pulled forward: chart-registry,
  citation-discipline, evidence-ledger, LaTeX/Beamer, Stata
  first-class, mode-registry. Skill count after v1.1 will be 8
  — at the threshold where mode-registry becomes worth
  considering for v1.2.

## 2026-05-08 — Phase 1 kickoff: web-scraping source corrected

- Plan said "fetch from canonical Anthropic source"; user clarified
  the working `~/.claude/skills/web-scraping/` on this machine *is*
  ours, not vendored from upstream. plan.md and phases/phase-1.md
  updated to source the bundle from `~/.claude/skills/web-scraping/`.
  No scope change; just provenance correction.

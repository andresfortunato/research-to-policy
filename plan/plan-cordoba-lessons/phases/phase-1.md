# Phase 1 — Six small wins

Read `plan.md` for the goal, constraints, decisions, file manifest,
and repo context that govern all phases. This file scopes Phase 1.

## Intent

Six low-friction hardenings that the cordoba audit surfaced. All
are markdown additions or skill-symlink wiring; no new directories,
no new hooks, no schema changes. Ships first because mechanical
and isolated — highest confidence, no architectural ripple.

## Files

- `.claude/conventions/script-header.md` — add four sections:
  `Supersedes:` optional field with cross-link example to
  `decisions/YYYY-MM-DD_<slug>.md`; rule "use repo-relative paths
  (`here::here()` / `pathlib`), never `setwd("/home/...")`";
  one-paragraph "shared utilities go in `R/` or `scripts/_lib/`,
  imported not duplicated"; one-paragraph "one project, one env —
  sub-tools with own `.venv`/`pyproject.toml` is an anti-pattern".
- `.claude/skills/web-scraping/` (new) — bundle our own web-scraping
  skill into the framework. Source: copy from `~/.claude/skills/web-scraping/`
  (the working version on this machine — `SKILL.md` + `references/`).
  Symlinked into `~/.claude/skills/` by `scr init` like other global
  skills. Do NOT vendor the binary blob from `~/cordoba/docs/web-scraping.skill`.
- `templates/deliverables/internal-research-memo/PROFILE.md` —
  add a paragraph endorsing dated `## Update: <date>` addendum
  sections over rewrites. Note in success-criteria: "Long-running
  inquiries should accrete dated addenda; rewrites discard the
  inquiry's history."
- `templates/deliverables/internal-research-memo/template.md` —
  add a commented `<!-- ## Update: YYYY-MM-DD ... -->` example
  at the bottom.
- `src/lib/install-project.js` — extend skills-symlink list to
  include `web-scraping`. Idempotent.
- `README.md` — one line in the "Skills installed" block (or
  equivalent) noting `web-scraping` ships with v1.1. (This is
  a tactical edit; full README rewrite is Phase 6.)

## Verification

- Re-run `scr init` against a fresh empty dir. Result:
  `~/.claude/skills/web-scraping/` exists (symlinked).
- `script-header.md` example block contains the new
  `Supersedes:` field as optional, with format
  `Supersedes: scripts/<old>.R (decision: decisions/<slug>.md)`.
- `script-header.md` "Format examples" updated for both R and
  Python with `here::here()` / `pathlib.Path(__file__).parent`
  usage. No `setwd("/home/...")` anywhere.
- `internal-research-memo/PROFILE.md` "Success criteria" block
  names the addendum pattern explicitly.
- `scr init --upgrade` against a v1 project: existing
  `script-header.md` lands as `script-header.md.framework-new`
  sidecar (divergent), not overwritten. Researcher merges
  manually.
- No new hooks fire. Hook count unchanged.

## Dependencies

None upstream. Outputs feed Phases 3 (web-scraping skill is
referenced from brainstorming) and 6 (README rewrite covers
all v1.1 additions).

## Reference patterns

Mirror the rhythm of `plan/plan-refdocs-conventions/` and
`plan/plan-project-conventions/`. Read either's handoff for the
shipped-pattern verification log.

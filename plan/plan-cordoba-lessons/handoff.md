# Handoff: plan-cordoba-lessons

**Status:** ACTIVE — Phase 1 complete; Phase 2 next.
**Date:** 2026-05-08
**Last commit on plan branch:** `4c80c65` — "Phase 1: six small wins (script-header tweaks, web-scraping bundle, addendum pattern)" (plan baseline at `aae136e`).

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Six small wins (script-header tweaks, web-scraping bundle, addendum pattern) | ✅ done | Mechanical, isolated; shipped first. Verification log below. |
| 2 | Theme-parallel opt-in (insights-logging + check-insights.sh + INDEX schema) | ⏭ next | Schema change; ships before Phases 3–5 so they land theme-aware. |
| 3 | Brainstorming skill (port from scc, research-adapted) | ⏭ queued | Closes the methodology-essay-isn't-a-plan gap. |
| 4 | Learning-capture skill + retrieve-learnings.sh + precompact-handoff.sh | ⏭ queued | Three-bucket model: insights/decisions/learnings. |
| 5 | Plan archival (Stop hook extension + archivist agent + archive/) | ⏭ queued | Existing four .completed markers archived manually first. Archivist scope kept narrow — defers project-wide cleanup to `/research-cleanup`. |
| 6 | README rewrite for researcher audience | ⏭ queued | Quickstart → workflow → scaffolding → tools → what's in here → updates → design philosophy (last). Ships after all components exist. |

## Where we are

Phase 1 landed in one commit (six small wins, all framework-internal,
no architectural ripple). Plan baseline committed at `aae136e` ahead
of Phase 1; Phase 1's commit hash filled in below once it lands.

Phase 2 is the schema change — opt-in `insights/<theme>/` subfolder
support in `insights-logging.md` + `check-insights.sh` glob update +
`insights/INDEX.md` template — and it should land before Phases 3–5
so the new conventions/skills/hooks reference theme-awareness as
already-shipped rather than retrofitted.

## What's next

1. **Phase 2 kickoff** — `phases/phase-2.md`. Touches:
   `.claude/conventions/insights-logging.md` (document opt-in
   `<theme>/` subfolder), `.claude/hooks/check-insights.sh` (extend
   glob to also pick up `insights/<theme>/*.md`), and the
   `insights/INDEX.md` template if its schema needs a theme column.
   Plus a new rationale doc at `docs/theme-parallel-mechanism.md`.
2. **Pre-Phase 5 housekeeping (deferrable until Phase 5):** archive
   the four pre-existing `.completed` markers manually
   (plan-install-redesign, plan-project-conventions,
   plan-refdocs-conventions, plan-v1-framework) so the new Stop
   hook doesn't fire on legacy markers when Phase 5 lands.

## Phase 1 verification log

| Gate | Result | Evidence |
|---|---|---|
| script-header.md adds optional `Supersedes:` field with example | ✓ | New "Optional fields" section + format `Supersedes: scripts/<old>.R (decision: decisions/<slug>.md)`. |
| Format examples updated for R (`here::here()`) + Python (`pathlib.Path(__file__).parent.parent`) | ✓ | Both examples rewritten; no `setwd("/...")` anywhere. |
| New "Repo-relative paths" rule | ✓ | New section explicitly forbids absolute user paths. |
| New "Shared utilities" section (`R/`, `scripts/_lib/`) | ✓ | Idiomatic locations + import-not-duplicate rule. |
| New "One project, one env" section | ✓ | Anti-pattern named (sub-tools with own `.venv`/`pyproject.toml`). |
| `web-scraping` skill bundled at `.claude/skills/web-scraping/` | ✓ | SKILL.md + 3 references (`ai-extraction.md`, `anti-detection.md`, `data-pipeline.md`) sourced from `~/.claude/skills/web-scraping/`. |
| `internal-research-memo/PROFILE.md` endorses addendum pattern | ✓ | Success criterion #6 added: "Long-running memos accrete dated addenda; they are not rewritten." |
| `internal-research-memo/template.md` has commented `## Update:` example | ✓ | Three-part addendum block (What's new / What this changes / What still stands) at file bottom. |
| `README.md` one-line tactical update | ✓ | `web-scraping/` entry added to `.claude/skills/` tree in "What's in here". Full rewrite is Phase 6. |
| `scr init` in fresh dir: installs everything | ✓ | All conventions + memo template land correctly. |
| `scr init --upgrade` against divergent `script-header.md`: sidecar pattern | ✓ | `.framework-new` sidecar written; original untouched. |
| Hook count unchanged | ✓ | Still only `check-insights.sh`. |

## Surprises

- **The plan said `install-project.js` needed a "skills-symlink list"
  extension. It doesn't.** `install-globals.js` (added in
  plan-install-redesign Phase 3) iterates every subdirectory of
  `<framework>/.claude/skills/` and symlinks each into
  `~/.claude/skills/`. Adding the `web-scraping/` directory is
  sufficient — no JS edits. Phase 1's plan paragraph is one
  outdated bullet because it was written against the pre-Phase-3
  install model.

- **On THIS user's machine, `~/.claude/skills/web-scraping/` is a
  real directory, not a symlink.** The framework copy is new (this
  Phase); the user's home-dir copy preexisted (May 5). After the
  framework bundle lands, the two are byte-identical. On a *fresh*
  machine, `scr init`'s `installGlobals()` step will create the
  symlink correctly. On *this* machine, the real dir blocks the
  symlink — `install-globals.js` catches the EEXIST and silently
  skips ("don't overwrite user's files"). One-shot fix if the user
  wants framework updates to flow through:

  ```bash
  rm -rf ~/.claude/skills/web-scraping
  ln -s /Users/anf191/github/super-claudio-research/.claude/skills/web-scraping ~/.claude/skills/web-scraping
  ```

  Optional. The skill works either way today — but the symlink is
  the supported path going forward.

## What didn't work

- Nothing meaningful in Phase 1. One scope clarification (plan said
  "fetch from canonical Anthropic source"; reality is the working
  `~/.claude/skills/web-scraping/` *is* ours). Logged in `log.md`,
  plan + phase-1.md updated before the plan-baseline commit.

## Implementation hints for Phase 2

- Read `.claude/conventions/insights-logging.md` and
  `.claude/hooks/check-insights.sh` first; both are short.
- The `<theme>/` subfolder pattern is **opt-in and free-form** — no
  `themes.md` declaration, no enumeration, no enforcement. The hook
  just globs `insights/*.md` AND `insights/*/*.md`. Convention text
  documents the subfolder option as available, not required.
- New file at `docs/theme-parallel-mechanism.md` carries the
  rationale (why opt-in, why no declaration). Mirror the rhythm
  of `docs/insights-mechanism.md` for style.
- `templates/insights/INDEX.md` may need a `Theme` column or a
  free-text "scope" hint — confirm with the existing seed before
  changing the schema.

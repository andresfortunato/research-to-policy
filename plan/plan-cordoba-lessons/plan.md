# Plan: cordoba-lessons (framework v1.1)

Improve the research-to-policy framework based on lessons drawn from
auditing `~/cordoba` — a real applied-research project that ran without
research-to-policy conventions and accumulated the failure modes
the framework was designed to prevent. Six phases, all framework-internal:
six small markdown wins, opt-in theme-parallel layout for `insights/` and
`output/`, three skills/hooks ported from `super-claudio-code` (brainstorming,
learning-capture, plan archival), a pre-compact handoff nudge, and a
final researcher-audience README rewrite.

## Goal

Ship v1.1 of the framework before the May 2026 Córdoba/Cambodia kickoff,
covering: (a) six low-friction conventions hardening that the cordoba
audit surfaced, (b) opt-in theme-parallel layout for projects with
multiple lines of inquiry running in parallel, (c) three
research-adapted ports from super-claudio-code that close gaps the
audit identified — brainstorm-before-plan, tacit-learning capture
with retrieval, and plan archival on `.completed`, and (d) a
researcher-audience README rewrite once all components are in place.
Out of scope: any retrofit/triage workflow for onboarding r2p into
existing disorganized projects (deferred to a separate plan after
v1.1 ships).

## Constraints

- **Preserve the framework constitution**
  (`docs/audience-and-philosophy.md`): silent-by-default,
  conditional-not-always-fire, composable, project-shared, short
  CLAUDE.md, markdown-first, stakes-graded verification, open-source
  from day one. Anything new must conform.
- **Hooks stay pure bash + standard Unix tools.** scc's three new hooks
  (`stop.js`, `pre-compact.js`, `user-prompt-submit.js`) are JS. They
  must be re-implemented in bash to match `check-insights.sh` and the
  v1-framework constitution. No new runtime dependencies (`jq` is the
  ceiling).
- **No project-specific Córdoba content in committed framework files.**
  The cordoba audit motivated this plan, but no examples / scripts /
  filenames from `~/cordoba` ship in `templates/` or
  `.claude/conventions/`. Generic placeholders only.
- **Theme-awareness is opt-in, not declarative.** No `themes.md`
  declaration file, no upfront enumeration. Subfolder use is permitted;
  flat layout stays default. Hooks accept both shapes.
- **Don't break existing installs.** `r2p init --upgrade` users on a
  v1 project must land v1.1 cleanly: existing `insights/INDEX.md`,
  hooks, and `CLAUDE.md` must survive the upgrade with sidecars on
  divergence (see `src/lib/upgrade.js` pattern).
- **Don't port `cleanup.js` agent.** Code-shaped; we already have
  `/research-cleanup` for the research-shaped equivalent.
- **Archivist and `/research-cleanup` are complementary, not
  redundant.** The archivist (Phase 5) is *automated* — the Stop
  hook fires it on `.completed`, scoped narrowly to the plan being
  archived. `/research-cleanup` (existing v1) is *user-invoked* —
  ad-hoc, broad-scope, repo-wide audit. They must produce
  consistent results: archivist defers project-wide cleanup
  (orphans, intermediates, unreferenced charts) to
  `/research-cleanup`, and `/research-cleanup` documents that
  per-plan archival is the archivist's job. No duplicated cleanup
  logic; the boundary is the unit (plan vs project) and the trigger
  (hook vs user).
- **Don't port scc's planning skill.** r2p relies on scc's planning
  skill (installed globally). Brainstorming skill triggers "the
  planning skill" — agnostic about whose. A research-adapted planning
  skill is a future consideration outside this plan.
- **Token-cost budgets carry over.** Routine hook output ≤200 tokens;
  skill invocations follow scc convention (brainstorming is open
  conversation, learning-capture writes one file).
- **Verification is domain-shaped, not code-shaped.** Each phase's
  verification gate names the markdown shape, the silent/triggered
  hook behaviors, and the install-flow effect. Not unit tests.

## Decisions Made

Settled in the brainstorm preceding this plan; not to be re-debated.

- **Theme-parallel: opt-in subfolder (Path A), not declared up-front.**
  `insights/<theme>/01_*.md` permitted alongside `insights/01_*.md`.
  Hooks/skills/INDEX schema accept both. Free-form theme strings
  (lowercase-snake-case suggested, not enforced).
- **Sub-tools-with-own-envs is an anti-pattern.** One project, one env.
  cordoba's `scrapers/zonaprop/.venv` + `scrapers/mercadolibre/.venv`
  is the cautionary tale, not a borrow.
- **No `_fixed`/`_v2`/`_extended` filenames.** Iteration is captured
  via a new `Supersedes:` script-header line + decision-record
  cross-link. Belongs in `script-header.md` (not a new convention).
- **Project-relative paths required.** `here::here()` in R, `pathlib`
  in Python. Absolute user paths (`setwd("/home/...")`) are an
  anti-pattern. Belongs in `script-header.md`.
- **Shared utilities convention.** Project helpers go in `R/`
  (R idiom) or `scripts/_lib/` (Python idiom), imported not
  duplicated. One short addition; no separate convention file —
  add as a section in `script-header.md` to keep convention-count
  low.
- **Bundle the web-scraping skill.** `source-registry.md` already
  references "the existing web-scraping skill"; v1 ships nothing
  there. cordoba carries it as a binary in `docs/`. We ship it
  globally via the same skills-symlink mechanism `r2p init` already
  uses. **Source: copy from `~/.claude/skills/web-scraping/` — this
  is our own skill (not vendored from an Anthropic-canonical source);
  do NOT vendor cordoba's binary blob.**
- **Addendum pattern endorsed in `internal-research-memo`.** Dated
  `## Update: <date>` sections rather than rewrites. cordoba's
  `spatial_equilibrium_report.md` section 9 is the existence proof.
- **Learning-capture is project-wide, not theme-aware.** Gotchas
  ("PONDII didn't exist in 2014 EPH waves") are universal lessons,
  not theme-scoped. Trigger-keyword matching does the routing.
- **Three new skills, two new hooks, one new agent in this plan.**
  Skills: `brainstorming`, `learning-capture`, plus the bundled
  `web-scraping`. Hooks: `retrieve-learnings.sh` (UserPromptSubmit),
  `precompact-handoff.sh` (PreCompact). Agent: `archivist`.
  `check-insights.sh` is *extended* to detect `.completed`, not
  duplicated. Skill count after v1.1: 8 — at the threshold where
  scc's mode-registry becomes worth considering for v1.2 (TODO.md
  already tracks this).
- **README is rewritten for applied researchers, not framework
  developers.** Current README reads as a constitution-and-component
  catalogue. The audience that matters at the May 2026 kickoff is
  applied researchers — they need quickstart, a workflow narrative
  (brainstorming → planning → implementation, with handoffs), the
  scaffolding map, and the tools/skills as a reference table.
  Design philosophy moves to the bottom — load-bearing for
  contributors, but not what a researcher needs first. Section
  order: intro summary → quickstart → what the framework does
  (workflow narrative, scaffolding, tools/skills) → what's in
  here (component reference) → updates → design philosophy.
  Phase 6 ships this rewrite once Phases 1–5 have landed all
  components (no rewriting against a moving target).
- **Hook implementation language: bash.** Mandated by constitution.
  Three JS hooks from scc → three bash hooks here. No JS leakage
  outside `src/` (the `r2p` CLI itself).

## File Manifest

```
research-to-policy/
├── .claude/
│   ├── agents/
│   │   └── archivist.md                                ✚ research-adapted port of scc archivist
│   ├── conventions/
│   │   ├── script-header.md                            ✎ add Supersedes: field, paths rule, shared-utilities note, one-env note
│   │   ├── insights-logging.md                         ✎ document opt-in <theme>/ subfolder layout
│   │   ├── plan-structure.md                           ✎ document .completed marker → archival flow
│   │   ├── learning-capture.md                         ✚ new convention (gotcha/insight types, index.yaml format, retrieval contract)
│   │   └── brainstorm-format.md                        ✚ new convention (brainstorms/<topic>.md shape, planning-skill handoff)
│   ├── hooks/
│   │   ├── check-insights.sh                           ✎ extend: also glob insights/<theme>/*.md; detect .completed for archival nudge
│   │   ├── retrieve-learnings.sh                       ✚ new bash hook (port of scc user-prompt-submit.js)
│   │   └── precompact-handoff.sh                       ✚ new bash hook (port of scc pre-compact.js)
│   ├── skills/
│   │   ├── brainstorming/SKILL.md                      ✚ research-adapted port of scc brainstorming
│   │   ├── learning-capture/SKILL.md                   ✚ research-adapted port of scc learning-capture
│   │   ├── research-cleanup/SKILL.md                   ✎ add "Boundary with archivist agent" paragraph
│   │   └── web-scraping/                               ✚ bundled (canonical Anthropic skill — sourced once, symlinked globally)
│   └── settings.template.json                          ✎ wire UserPromptSubmit + PreCompact hooks
├── docs/
│   ├── theme-parallel-mechanism.md                     ✚ rationale (opt-in vs required, why no declaration)
│   ├── learning-capture-mechanism.md                   ✚ rationale (3-bucket model: insights vs decisions vs learnings)
│   ├── brainstorm-mechanism.md                         ✚ rationale (brainstorm→plan handoff, why distinct from /verify)
│   ├── plan-archival-mechanism.md                      ✚ rationale (.completed marker, why archive vs delete)
│   └── audience-and-philosophy.md                      ✎ add "one project, one env" + "opt-in theme parallelism" to constitution if appropriate
├── templates/
│   ├── CLAUDE.md.template                              ✎ pointer blocks for brainstorming, learning-capture, archival; codebase-tree updates
│   ├── brainstorms/README.md                           ✚ seed (one-line orientation)
│   ├── learnings/                                      ✚ seed dir
│   │   ├── README.md                                   ✚ orientation (gotcha vs insight, retrieval mechanic)
│   │   └── index.yaml                                  ✚ empty seed (`learnings: []`)
│   ├── archive/                                        ✚ seed dir
│   │   ├── README.md                                   ✚ orientation
│   │   └── index.md                                    ✚ empty seed (header + placeholder list)
│   └── deliverables/internal-research-memo/
│       ├── PROFILE.md                                  ✎ endorse dated `## Update: <date>` addendum pattern; cordoba pattern as the example
│       └── template.md                                 ✎ add commented Update-section example
├── src/lib/
│   └── install-project.js                              ✎ seed templates/{brainstorms,learnings,archive}/ on init; idempotent
├── README.md                                           ✎✎ Phase 6 full rewrite (researcher audience; quickstart → workflow → scaffolding → tools → what's in here → updates → design philosophy)
└── TODO.md                                             ✎ mark cordoba-lessons items shipped; bump remaining v1.1 candidates
```

No deletions. No directory moves.

## Repo Context

This plan is the third "convention pack" since v1 shipped — after
`plan-refdocs-conventions` (added `data_sources/` + `methods/`,
archived 2026-05-06) and `plan-project-conventions` (added
`project_conventions/`, archived shortly after). Both followed the
same shape: `.claude/conventions/<name>.md` for protocol +
`docs/<name>-mechanism.md` for rationale + `templates/<dir>/` seeds
+ pointer block in `CLAUDE.md.template` + entry in `install-project.js`
+ entry in `README.md`. Phase 1 of this plan follows that pattern
mechanically; Phases 3–5 add a parallel pattern for skills/hooks/agents
that scc has already road-tested. Phase 2 is the only architectural
change (opt-in theme-parallel layout).

`super-claudio-code` (`~/github/super-claudio-code/`) is the upstream
for the brainstorming/learning-capture/archivist ports. Read the
`SKILL.md` files there before adapting; the research adaptation is
small (different domain examples, planning-skill agnostic, project-wide
rather than `.scc/`-rooted directories).

The cordoba audit (this conversation) is the diagnostic source. No
artifacts from `~/cordoba` ship in this plan — the audit motivated
the gaps; the gaps motivated the conventions.

## Phases

Six phases. Phase 1 ships first because it's mechanical and isolated
(highest confidence, no architectural ripple). Phase 2 ships next
because it's the schema change — landing it before Phases 3–5 means
their new conventions/skills/hooks land theme-aware-by-default rather
than retrofitted. Phases 3–5 are parallelizable but small; sequencing
is by complexity (3 simplest → 5 most involved). Phase 6 (README
rewrite) ships last so it can describe the full v1.1 surface in
one pass.

Each phase has its own file at `phases/phase-N.md` with intent,
file list, and verification gates. Read only the phase you're
implementing — the rest stays out of context.

| Phase | Title | Scope | File |
|---|---|---|---|
| 1 | Six small wins | `script-header.md` extensions; bundle web-scraping skill; addendum pattern in `internal-research-memo` | `phases/phase-1.md` |
| 2 | Theme-parallel opt-in | `insights-logging.md` + `check-insights.sh` glob + INDEX schema accept `<theme>/` subfolders | `phases/phase-2.md` |
| 3 | Brainstorming skill | Port from scc, research-adapted; output to `brainstorms/<topic>.md`; planning-skill agnostic | `phases/phase-3.md` |
| 4 | Learning-capture + 2 hooks | Port skill from scc; bash-port `UserPromptSubmit` + `PreCompact` hooks; new `learnings/` directory | `phases/phase-4.md` |
| 5 | Plan archival | Extend Stop hook for `.completed` detection; new `archivist` agent; `archive/` directory; boundary with `/research-cleanup` | `phases/phase-5.md` |
| 6 | README rewrite | Researcher-audience restructure: quickstart → workflow → scaffolding → tools → what's in here → updates → design philosophy | `phases/phase-6.md` |

## Phase Order + Dependencies

- **Phase 1** has no upstream dependencies; ships first. All other
  phases can technically start once Phase 1 lands, because Phase 1's
  shared-utilities / paths edits to `script-header.md` don't conflict
  with anything in Phases 2–6.
- **Phase 2** ships second. It's the schema change — landing it before
  Phases 3–5 means new conventions/skills/hooks can reference the
  opt-in pattern in their docs without retrofit.
- **Phase 3** depends on Phase 1 (uses `web-scraping` skill if a
  brainstorm surfaces a scraping question; not a hard dep) and
  Phase 2 (mentions theme-aware brainstorm filenames as opt-in).
- **Phase 4** depends on Phase 2 (learning-capture conventions
  document boundary with theme-aware insights). Phase 4 is internally
  parallel: skill, retrieve-learnings hook, precompact-handoff hook
  are independent files; can ship in one or three commits.
- **Phase 5** depends on Phase 4 (precompact-handoff hook hint at
  learning-capture; archivist agent surfaces "Learnings captured"
  in archive entries) and on the four pre-existing `.completed`
  markers being archived manually first (so the new Stop hook
  doesn't fire on legacy markers).
- **Phase 6** depends on all preceding phases. README rewrite must
  describe the v1.1 surface — components added across Phases 1–5
  must all exist before the rewrite lands, otherwise the rewrite
  has to be patched as each phase ships. Single rewrite at the
  end avoids churn.

Strict order: 1 → 2 → 3 → 4 → 5 → 6. Phases 3 and 4 could run in
parallel in different branches if multi-session, but the file
conflicts in `templates/CLAUDE.md.template`, `src/lib/install-project.js`,
and `README.md` make sequential simpler.

## Open Items Deferred (to post-v1.1)

- **chart-registry**, **citation-discipline**, **evidence-ledger** —
  already in `TODO.md`, not pulled forward. Best designed against
  pilot feedback rather than retrofit-from-cordoba.
- **Research-adapted planning skill.** scc's planning skill works
  fine via global symlink; a research-domain rewrite is a v1.2 call
  if pilot use surfaces friction.
- **Triage workflow for retrofitting r2p onto existing disorganized
  projects.** This is the second cordoba-derived plan; covered in
  TODO.md as a follow-up.
- **Mode-registry / cross-skill advisor.** Skill count after v1.1:
  8. At threshold; defer to v1.2.
- **`themes.md` declaration file.** Explicitly rejected in this
  plan; revisitable only if pilot use shows free-form theme strings
  produce drift.

## Implementation hint for next session

Phase 1 mirrors the rhythm of `plan/plan-refdocs-conventions/` and
`plan/plan-project-conventions/` — read either's handoff for the
shipped-pattern verification log. Phases 3–5 mirror nothing in this
repo; the pattern lives in `~/github/super-claudio-code/` and the
adaptation work is "research-ify the domain examples + bash-port
the JS hooks + agnostic-ize the planning-skill handoff". Read each
upstream `SKILL.md` or `agents/*.md` once, then write the r2p
version against the existing `.claude/conventions/`-shape (intent
docs at `docs/<name>-mechanism.md`, protocol at
`.claude/conventions/<name>.md`, seeds at `templates/<dir>/`).

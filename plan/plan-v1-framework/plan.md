# Plan: super-claudio-research v1 framework

## Goal

Ship a v1 framework that is useful to the Córdoba (close-out Aug 2026) and Cambodia (close-out Sept 2026) pilot teams by the mid-May 2026 kickoff workshop, while remaining clean enough to open-source from day one. The build adapts scc's planning + handoff + verification discipline to applied development research, adopts Karpathy's three-layer wiki for cross-engagement memory, adds stakes-graded verification (silent manifest, user-invoked `/verify`, deliverables-only forked review), and ships a small set of conventions + skills + profiles that researchers can install with one command.

Decisions and rationale: see `brainstorms/v1-framework-scope.md`.

## Constraints

- **Preserve the existing repo's design constitution:** silent-by-default hooks, conditional-not-always-fire, composable-not-monolithic, project-shared-not-user-personal, short CLAUDE.md with pointers. Anything new must conform.
- **Do not replace the existing `insights-logging` convention.** It works. Build alongside.
- **Markdown-first.** Do not assume any particular language toolchain in core skills/conventions. Python and R are the two first-class language targets, but core hooks and conventions stay language-neutral.
- **No LaTeX/Beamer infrastructure in v1.** Stub a roadmap entry pointing at Pedro/Hugo for later borrowing.
- **No orchestrator / coordination layer between deliverables.** Ship components, not workflows. Coordination patterns will emerge from real use.
- **Hooks must remain pure bash + standard Unix tools** for the conditional-Stop-hook style. Manifest hook may shell out to `jq` if needed; document the dependency.
- **No always-fire verification.** Manifest entry on every analytical Bash run is the only non-negotiable hook. Everything else (verify, review, lint) is user-invoked or selectively triggered.
- **Open-source from day one.** No project-specific Córdoba/Cambodia content in committed framework files. Pilot-specific config goes in the *target project*, not in this repo.
- **Don't break `install.sh`.** Existing users of the repo (if any) must still get a working install. Extend, don't rewrite.
- **Verification cost budget:** routine manifest hook ≤200 tokens; `/verify` invocation ≤2k tokens; `/deliverable-review` ≤12k tokens. Anything in between is suspect and probably the wrong primitive.
- **Don't proliferate skills.** Ship the minimum viable set (the two verification skills + adapted research planning skills). Imbad's mode-registry pattern becomes necessary somewhere around 8+ skills — we should stay below that for v1.

## Decisions Made (consumed from brainstorm)

These are settled. Do not re-debate during execution.

- **Three audience scopes** served simultaneously, with the two pilot engagements as the proving ground.
- **Markdown-first**, with R + Python as the two first-class language targets. Stata and LaTeX deferred.
- **Verification stack:** conditional Stop hooks (existing pattern) + silent manifest hook (new) + `/verify` user-invoked skill + `/deliverable-review` forked parallel review. Both new skills built via the `skill-creator` skill.
- **Wiki layer adopted** in full: Karpathy three layers (`raw/` immutable, `wiki/` LLM-owned, schema in CLAUDE.md), three operations (ingest, query, lint), two special files (`wiki/index.md`, `wiki/log.md`).
- **Page-type budgets** for wiki pages: source ≤300 words, concept ≤800, entity ≤600, synthesis no cap but `last_condensed` frontmatter required.
- **Cleanup agent kept** but adapted for research repos (orphan scripts, intermediate CSVs, unused charts). Produces a proposal, never auto-deletes.
- **Bundle of components, no orchestration** for v1. Multi-deliverable coordination figured out from real use, not designed up front.
- **Existing `insights-logging` convention preserved unchanged.**

### Decisions resolved during planning

These were open in the brainstorm. Resolved here; can be revisited only with explicit scope-change.

- **Install model:** extend existing `install.sh` to copy the new conventions/hooks/skills/templates and seed `wiki/` + `raw/` + `manifest.jsonl`. A scc-style CLI (`scc-research init …`) is deferred to v2; one shell script is enough for the pilot and easier to audit.
- **Plan directory location:** `plan/plan-<name>/` at project root (scc style). Matches the planning skill's expectations and makes scc patterns transferable. Reject `quality_reports/plans/` (Pedro style).
- **Manifest format:** **JSON Lines** (`manifest.jsonl`) at project root. One JSON object per line: `timestamp`, `script`, `language`, `inputs`, `outputs`, `output_sha256`, `seed`, `env_hash`, `git_sha`, `phase` (optional). JSONL is greppable, appendable from a hook in pure bash + `jq`, parseable in Python and R, and survives merge conflicts.
- **Wiki location:** `wiki/` at project root (sibling of `raw/`, `data/`, `output/`). Easy to find, plays well with Obsidian and other markdown editors.
- **Skill names confirmed:** `/verify` (per-artifact, user-invoked) and `/deliverable-review` (forked parallel review). Located at `.claude/skills/verify/SKILL.md` and `.claude/skills/deliverable-review/SKILL.md`.
- **Skills vs. conventions split:** `.claude/conventions/` holds protocols Claude reads on demand (existing pattern: insights-logging, handoff-format, etc.); `.claude/skills/` holds invokable Anthropic-format skills with `SKILL.md` + frontmatter (the verification skills, the wiki skills). Both ship in v1.
- **Initial conventions to ship beyond `insights-logging`** (4 of the 6 roadmap items): `handoff-format`, `manifest-logging` (new, formerly `reproducibility-check`), `plan-structure`, `decision-records`. Defer `evidence-ledger`, `chart-registry`, `citation-discipline` to v1.1 — useful but not blocking.
- **Initial deliverable profiles** (3): `country-diagnostic-memo`, `ministerial-briefing`, `internal-research-memo`. Each is a markdown template + a one-page profile (length target, register, audience, success criteria, recommended review lenses for `/deliverable-review`).
- **Hook script language:** bash for conditional Stop hooks (existing pattern continues); allow one `pre-compact` hook in bash too, importing Pedro's pattern but rewritten without Python dependency.
- **Source registry + targeted continuous scraping:** ship a project-level YAML registry (`sources/registry.yaml`) listing news/policy/company/infra sources of interest per engagement, plus a `/scan-sources` skill that reads the registry, identifies due-for-rescrape items, delegates fetching to the existing `web-scraping` skill, dedupes by content hash, lands new content in `raw/sources/<slug>/YYYY-MM-DD_<title-slug>.md` with frontmatter, and logs every run to `manifest.jsonl`. Reject "scrape everything on a cron schedule" (too noisy, expensive, fragile); reject "free-form bookmarks" (no structure for ingest). Registry is the single source of truth.

## File Manifest

Directory layout after this plan ships (✚ = new, ✎ = modified, · = untouched):

```
super-claudio-research/
├── .claude/
│   ├── conventions/
│   │   ├── insights-logging.md            ·
│   │   ├── handoff-format.md              ✚ session-end handoff protocol
│   │   ├── manifest-logging.md            ✚ JSONL manifest spec + reproducibility
│   │   ├── plan-structure.md              ✚ research-adapted scc plan layout
│   │   ├── decision-records.md            ✚ Decision/Alternatives/Why/Invalidate template
│   │   └── source-registry.md             ✚ project-level watchlist + scrape protocol
│   ├── skills/                            ✚ new top-level dir
│   │   ├── verify/
│   │   │   └── SKILL.md                   ✚ user-invoked per-artifact checks
│   │   ├── deliverable-review/
│   │   │   └── SKILL.md                   ✚ forked parallel review (deliverables only)
│   │   ├── wiki-ingest/
│   │   │   └── SKILL.md                   ✚ raw/ → wiki/ ingest workflow
│   │   ├── wiki-lint/
│   │   │   └── SKILL.md                   ✚ orphans, contradictions, stale, budget
│   │   ├── scan-sources/
│   │   │   └── SKILL.md                   ✚ registry-driven targeted scraping
│   │   └── research-cleanup/
│   │       └── SKILL.md                   ✚ orphan scripts/charts/intermediates
│   ├── agents/                            ✚ new top-level dir
│   │   └── manifest-checker.md            ✚ subagent invoked by /verify if needed
│   ├── hooks/
│   │   ├── check-insights.sh              ·
│   │   ├── log-manifest.sh                ✚ silent PostToolUse, appends manifest.jsonl
│   │   ├── pre-compact.sh                 ✚ writes handoff snapshot before compaction
│   │   └── post-compact-restore.sh        ✚ surfaces snapshot on resume
│   └── settings.template.json             ✎ wire new hooks; add Skill discovery path
├── docs/
│   ├── extending.md                       ·
│   ├── insights-mechanism.md              ·
│   ├── handoff-mechanism.md               ✚
│   ├── manifest-mechanism.md              ✚
│   ├── plan-structure-mechanism.md        ✚
│   ├── wiki-architecture.md               ✚ Karpathy three-layer, page budgets, lint
│   ├── verification-architecture.md       ✚ /verify vs /deliverable-review vs hooks
│   ├── source-registry-mechanism.md       ✚ design rationale, dedup, freq logic
│   └── audience-and-philosophy.md         ✚ markdown-first, language-agnostic, scope
├── templates/
│   ├── CLAUDE.md.template                 ✎ add wiki + manifest + handoff pointers
│   ├── insights/INDEX.md                  ·
│   ├── wiki/                              ✚ seeds for the wiki layer
│   │   ├── SCHEMA.md                      ✚ how the wiki is organized
│   │   ├── index.md                       ✚ empty seed catalog
│   │   ├── log.md                         ✚ empty append-only log
│   │   └── README.md                      ✚ what goes here vs raw/
│   ├── raw/README.md                      ✚ immutable-sources convention
│   ├── sources/                           ✚ source-registry seeds
│   │   ├── registry.yaml                  ✚ commented example registry
│   │   └── README.md                      ✚ how to register a source
│   ├── manifest.jsonl                     ✚ empty seed file
│   ├── decision-record.md                 ✚ template for /decision capture
│   ├── handoff.md                         ✚ session-end handoff template
│   └── deliverables/                      ✚ initial 3 profiles
│       ├── country-diagnostic-memo/
│       │   ├── PROFILE.md                 ✚ length, audience, register, review lenses
│       │   └── template.md                ✚ skeleton structure
│       ├── ministerial-briefing/
│       │   ├── PROFILE.md                 ✚
│       │   └── template.md                ✚
│       └── internal-research-memo/
│           ├── PROFILE.md                 ✚
│           └── template.md                ✚
├── install.sh                             ✎ copy new files, seed wiki/raw/manifest
├── README.md                              ✎ update Conventions Installed; trim Roadmap
└── (plan/, brainstorms/, .scc/ all gitignored in target projects; committed in framework repo)
```

## Repo Context

The framework is itself a Claude Code project. The repo is two things at once:
1. **A framework distribution** — the files in `.claude/`, `templates/`, `docs/`, and `install.sh` are what gets installed into target research projects.
2. **A working environment** — `plan/`, `brainstorms/`, and `.scc/` are this repo's own scaffolding while we build the framework. They are gitignored at the *target-project* level by `install.sh`'s `.gitignore` block, but committed *here* so the build process is auditable and reproducible.

This dual identity matters during implementation: when adding a new convention file, we are *authoring* it in `.claude/conventions/`, not *applying* it to this repo. We are also writing the matching `docs/<name>-mechanism.md` for human readers. The CLAUDE.md template in `templates/` is the *target's* CLAUDE.md, not this repo's.

The existing `insights-logging` convention is the canonical example of the three-artifact pattern (`.claude/conventions/<name>.md` + optional `.claude/hooks/check-<name>.sh` + `docs/<name>-mechanism.md`). New conventions follow it. See `docs/extending.md` for the authoring rules — read it once before writing any convention file.

`.claude/skills/` is a new top-level directory introduced by this plan. Skills follow Anthropic's standard format (`SKILL.md` with YAML frontmatter: `name`, `description`, `allowed-tools`, etc.). Skills are *invokable* (slash commands or auto-triggered); conventions are *referenced* (Claude reads them when the situation matches the CLAUDE.md pointer). The two systems are complementary, not competitive.

## Phases

### Phase 1 — Foundation: directory layout, settings, install.sh

**Intent.** Lay down the structural bones — new top-level directories (`.claude/skills/`, `.claude/agents/`, `templates/wiki/`, `templates/raw/`, `templates/deliverables/`), update `settings.template.json` to wire new hooks and discover skills, update `install.sh` to seed wiki/raw/manifest in target projects, update `templates/CLAUDE.md.template` to point at the new conventions. No conventions or skills yet — just the empty rooms they'll furnish.

**Modifies/Adds.** `.claude/skills/` (new dir), `.claude/agents/` (new dir), `templates/wiki/` + `templates/raw/` + `templates/deliverables/` (new), `templates/CLAUDE.md.template`, `settings.template.json`, `install.sh`, `README.md` (Roadmap section).

**Verification.** `bash install.sh /tmp/test-research-project` produces a target with the new dirs seeded and an updated `.gitignore`. Existing `insights-logging` convention still installs. Settings file is valid JSON.

### Phase 2 — Wiki layer (Karpathy three-layer)

**Intent.** Make the wiki layer real. Author the wiki schema doc (`templates/wiki/SCHEMA.md`) that lives in target projects, the design doc (`docs/wiki-architecture.md`) that lives here, and two skills: `/wiki-ingest` (raw → wiki, touching index.md and log.md) and `/wiki-lint` (orphans, contradictions, stale, page-budget violations). Seed `templates/wiki/index.md` and `templates/wiki/log.md` empty.

**Modifies/Adds.** `.claude/skills/wiki-ingest/SKILL.md`, `.claude/skills/wiki-lint/SKILL.md`, `templates/wiki/{SCHEMA.md,README.md,index.md,log.md}`, `templates/raw/README.md`, `docs/wiki-architecture.md`, `templates/CLAUDE.md.template` (add wiki pointer block).

**Verification.** Skill files have valid frontmatter (`name`, `description`, `allowed-tools`). SCHEMA.md is concrete enough that Claude can ingest a sample PDF dropped in `raw/` without needing further direction. Lint skill flags an orphan page in a hand-built test wiki. Page-type budgets are stated and enforced as a `/wiki-lint` rule.

### Phase 3 — Manifest + reproducibility hook

**Intent.** Author `manifest-logging` convention + silent `log-manifest.sh` hook. Hook fires on PostToolUse for `Bash(Rscript|python|stata) *` matching, appends one JSON line per analytical run with timestamp, script path, output paths and SHAs, seed if extractable, env hash (R: `R.version.string` + loaded packages; Python: `python --version` + `pip freeze` digest; Stata: version), git sha. Document the format and the audit ritual.

**Modifies/Adds.** `.claude/conventions/manifest-logging.md`, `.claude/hooks/log-manifest.sh`, `docs/manifest-mechanism.md`, `templates/manifest.jsonl` (empty seed), `templates/CLAUDE.md.template` (add manifest pointer), `settings.template.json` (wire hook).

**Verification.** Run an R one-liner via Bash in a test project — a row appears in `manifest.jsonl` with the expected schema. Run a Python script — same. Run a non-analytical bash command (`ls`, `git status`) — *no* row appears. Hook costs ≤200 tokens (verify by reading the hook output size).

### Phase 4 — `/verify` and `/deliverable-review` skills (use skill-creator)

**Intent.** Build the two verification skills via the `skill-creator` skill (this is what the user explicitly requested). `/verify` is per-artifact, user-invoked, ≤2k tokens — checks one regression result, one chart, one paragraph against domain rules (sign of coefficients, magnitudes, missingness, source citation). `/deliverable-review` is forked parallel — adapts Pedro's seven-pass pattern, but with policy-research lenses: data validity, identification/reasoning, robustness, framing, audience-fit, political-economy realism, peer-Lab plausibility. Spawned via Task in parallel; synthesizer reconciles. Run only on advanced deliverable drafts.

**Modifies/Adds.** `.claude/skills/verify/SKILL.md`, `.claude/skills/deliverable-review/SKILL.md`, `.claude/agents/manifest-checker.md`, `docs/verification-architecture.md`. The `skill-creator` skill drives the authoring.

**Verification.** `/verify outputs/regression_latest.json` produces a structured report with at least three checks executed; cost ≤2k tokens. `/deliverable-review` on a sample memo spawns ≥5 parallel subagents (one per lens) with separate contexts; synthesizer collapses into a single report; total cost ≤12k tokens. Both skills have invocation examples in their SKILL.md.

### Phase 5 — Handoff, plan-structure, decision-records conventions

**Intent.** Author the three conventions that adapt scc's project discipline to research. `handoff-format` is the multi-time-scale handoff (within-session, researcher↔researcher, project→follow-up-years-later). `plan-structure` is the research-adapted version of scc's `plan/plan-<name>/` layout — replace "code-shaped" verification with "domain-shaped" (sign-of-coefficients, magnitude sanity, breakpoint alignment) and reference `decision-records` for methodology calls. `decision-records` is the policy-research analog of pre-registration: Decision / Alternatives / Why-rejected / Key-assumptions / What-would-invalidate.

**Modifies/Adds.** `.claude/conventions/handoff-format.md`, `.claude/conventions/plan-structure.md`, `.claude/conventions/decision-records.md`, `templates/handoff.md`, `templates/decision-record.md`, `docs/handoff-mechanism.md`, `docs/plan-structure-mechanism.md`, `templates/CLAUDE.md.template` (add three pointer blocks), optionally `.claude/hooks/pre-compact.sh` + `post-compact-restore.sh` (Pedro-pattern, rewritten in bash).

**Verification.** Conventions follow the existing three-artifact pattern. `templates/handoff.md` is concrete enough that a researcher reading it knows what to fill in. `pre-compact.sh` writes a state file referencing the active plan; `post-compact-restore.sh` reads and surfaces it; both are silent in the no-active-plan case.

### Phase 6 — Research-cleanup skill + initial deliverable profiles

**Intent.** Build `/research-cleanup` skill (orphan scripts > 30 days, intermediate CSVs older than `data/raw/` mtime, charts not appearing in any insight or deliverable, scratch-marked notebook cells). It produces `cleanup-proposal.md`; researcher signs off; never auto-deletes. Then ship the three initial deliverable profiles (`country-diagnostic-memo`, `ministerial-briefing`, `internal-research-memo`), each with a `PROFILE.md` (length target, register, audience, success criteria, recommended `/deliverable-review` lenses) and a `template.md` (skeleton structure).

**Modifies/Adds.** `.claude/skills/research-cleanup/SKILL.md`, `templates/deliverables/{country-diagnostic-memo,ministerial-briefing,internal-research-memo}/{PROFILE.md,template.md}`.

**Verification.** Cleanup skill, run on a hand-built messy test project, produces a proposal correctly identifying at least one orphan script and one stale chart. Each deliverable profile has a length target and a recommended set of `/deliverable-review` lenses appropriate to its audience (a ministerial briefing weights political-economy-realism more than peer-Lab-plausibility; the country-diagnostic-memo is the inverse).

### Phase 7 — Source registry + `/scan-sources` skill

**Intent.** Make targeted continuous scraping a first-class, lightweight capability. Author the `source-registry` convention and a `/scan-sources` skill. The registry (`sources/registry.yaml` in the target project) lists URLs of interest with metadata: slug, url, category (`investment` | `company` | `innovation` | `infrastructure` | `policy` | `news` | `other`), freq (`daily` | `weekly` | `monthly` | `adhoc`), last_scraped (auto-updated), scrape_method (`httpx` | `playwright` | `scrapegraph` | `crawl4ai`), content_selector (optional CSS or XPath), notes. The skill: reads the registry, filters to entries due for re-scrape (now > last_scraped + freq, or `--force`), delegates fetching to the existing `web-scraping` skill, computes content hash per fetched item, dedupes against a sidecar `sources/seen.jsonl` log, lands new content in `raw/sources/<slug>/YYYY-MM-DD_<title-slug>.md` with frontmatter (`url`, `source_slug`, `category`, `scraped_at`, `content_sha256`, `title`), updates `last_scraped` in registry, appends one line per run to `manifest.jsonl`. Researcher invokes `/scan-sources` (all due), `/scan-sources --slug=<slug>` (one source), or `/scan-sources --category=investment` (filtered). Scraped content does *not* auto-ingest into `wiki/` — that requires explicit `/wiki-ingest` so the researcher controls what becomes load-bearing knowledge.

**Modifies/Adds.** `.claude/conventions/source-registry.md`, `.claude/skills/scan-sources/SKILL.md`, `templates/sources/registry.yaml` (with commented examples for an "investment news," "company filings," "infrastructure tracker," "policy news" entry), `templates/sources/README.md`, `docs/source-registry-mechanism.md`, `templates/CLAUDE.md.template` (add source-registry pointer block), `install.sh` (seed `sources/` + empty `sources/seen.jsonl`), `templates/raw/README.md` (note the `raw/sources/<slug>/` subtree convention).

**Verification.** Build a test registry with 3 entries (one daily, one weekly, one adhoc); run `/scan-sources` — only the daily and weekly fire on first run; second run within an hour fires nothing (silent). Same URL fetched twice produces only one `raw/sources/<slug>/...md` file (dedup works). Each scrape produces a manifest row with `script: scan-sources`, the source URL, and the output path. `--force` bypasses the freq check. `/scan-sources --category=investment` filters correctly. Skill respects polite-scraping defaults inherited from the `web-scraping` skill (rate limits, robots.txt, identifiable User-Agent).

### Phase 8 — Documentation, README, workshop materials prep

**Intent.** Polish docs, update README to reflect installed conventions and the wiki/manifest/skills additions, draft kickoff-workshop materials (slides outline, demo notebook plan, the public-goods commitment one-pager). Move shipped items from "Roadmap" to "Conventions installed." Write `docs/audience-and-philosophy.md` capturing the design constitution for outside contributors.

**Modifies/Adds.** `README.md`, `docs/audience-and-philosophy.md`, possibly `workshop/` (outline-only, full slides built later in PowerPoint by the user).

**Verification.** Fresh-eyes test: a researcher who has never seen the repo can read README.md + docs/audience-and-philosophy.md and (a) understand what's in the box, (b) install it on a new project, (c) name three things they would do differently than scc and why.

## Phase Order + Dependencies

- Phase 1 (foundation) blocks all others — must happen first.
- Phase 2 (wiki) depends on Phase 1 only. Can run in parallel with Phase 3.
- Phase 3 (manifest) depends on Phase 1 only. Can run in parallel with Phase 2.
- Phase 4 (verification skills) depends on Phase 3 (manifest is what `/verify` reads against) and Phase 2 (review skill references wiki for context).
- Phase 5 (handoff/plan/decision conventions) depends on Phase 1 only. Can run in parallel with Phases 2-4 if a second session is available; otherwise sequence after Phase 4.
- Phase 6 (cleanup + profiles) depends on Phase 5 (profiles reference decision-records and `/deliverable-review`).
- Phase 7 (source registry + `/scan-sources`) depends on Phase 2 (lands content in `raw/sources/<slug>/` for later `/wiki-ingest`) and Phase 3 (logs runs to manifest). Can run in parallel with Phases 4-6.
- Phase 8 (docs) depends on all prior phases.

## Multi-Session Notes

Multi-session candidate: the manifest is now ~30 files added/modified across 8 phases, multiple integration seams (hooks, settings, install.sh, CLAUDE.md template, four new convention systems). Per-phase plan files are not needed yet — the phase summaries above are scoped tightly enough — but if any one phase's execution exceeds 50% context, split it into its own `phases/phase-N.md` at that point. Most likely candidates for splitting: Phase 4 (skill-creator authoring two skills + a subagent), Phase 5 (three conventions + two hooks), and Phase 7 (registry + skill + dedup logic + integration with `web-scraping`).

A `handoff.md` will be written at the end of each session; a `log.md` records direction changes. The `.scc/status/plan-v1-framework.md` file is updated when the active phase advances.

## Open Items Deferred

- scc-style CLI (`scc-research init`) → v2.
- LaTeX/Beamer add-on package borrowed from Pedro/Hugo → v1.1+.
- WIP-limited multi-project dashboard (Hugo's vault-manager pattern) → v1.1+.
- Mode-registry / cross-skill advisor (Imbad pattern) → only when skill count exceeds ~8.
- Additional conventions from existing roadmap (`evidence-ledger`, `chart-registry`, `citation-discipline`) → v1.1.
- Stata first-class support → v1.1.
- Additional deliverable profiles (donor concept note, external blog post, conference paper) → as engagements surface need.
- Brand assets integration (`gl_brand_assets/` is sitting in the repo untouched) → handle in Phase 7 if time, else v1.1.

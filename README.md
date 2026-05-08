# super-claudio-research

A Claude Code harness for **research projects** — applied economics, data analysis, and policy research.

The default Claude Code experience is built for software engineering. Research projects have different rhythms: long multi-session plans, evidence accumulation across phases, the need to remember what was *learned* (not just what was *built*), and a constant temptation to over-produce charts without distilling findings. This framework adds the lightweight conventions and hooks that make Claude Code work for that flow.

## Design philosophy

1. **Externalize conventions, hook the discipline.** Long-form rules live in `.claude/conventions/*.md` (read on demand) — not in CLAUDE.md (loaded every session). A small Stop hook checks state and *nudges* Claude when the discipline is being skipped. CLAUDE.md stays short.
2. **Conditional hooks, not always-fire prompts.** Every hook script must be **silent by default** and only emit `additionalContext` when the actual condition holds. Always-fire hooks pressure Claude to comply mechanically (writing trivial insights to "satisfy the rule"), which destroys the signal.
3. **Composable, not monolithic.** Each convention is one file in `conventions/` and (optionally) one script in `hooks/`. Adopt only what your project needs.
4. **Project-shared, not user-personal.** Everything in `.claude/conventions/`, `.claude/hooks/`, and `.claude/settings.json` is committed to the research repo so collaborators (human or AI) get the same scaffolding. User-personal config stays in `.claude/settings.local.json` (gitignored).

The full eight-principle constitution (silent-by-default, conditional-not-always-fire, composable, project-shared, short CLAUDE.md, markdown-first, stakes-graded verification, open-source-from-day-one) is in `docs/audience-and-philosophy.md`. Read that before proposing a new convention or hook.

## What's in here

```
.claude/
├── conventions/
│   ├── insights-logging.md          ← evidence-based findings doc protocol
│   ├── script-header.md             ← every analytical script's header block (Inputs/Outputs/Seed/Env)
│   ├── analytical-commit-format.md  ← Run:/Out: lines in commit messages for analytical changes
│   ├── handoff-format.md            ← multi-time-scale session-end handoff protocol
│   ├── plan-structure.md            ← plan/plan-<slug>/ layout for multi-session work
│   ├── decision-records.md          ← Decision/Alternatives/Why/Invalidate template
│   ├── methods.md                   ← project-internal rule docs (Source/Rule/Exclusions/Diagnostic counts)
│   ├── project-conventions.md       ← project-bespoke style/process rules (visualization, writing, etc.)
│   ├── source-registry.md           ← project-level watchlist + scrape protocol
│   └── data-sources.md              ← API/dataset reference docs (Status/Anchor/Workflow/Pitfalls)
├── hooks/
│   └── check-insights.sh            ← Stop hook (silent unless analysis lacks insights doc)
├── skills/                          ← symlinked into ~/.claude/skills/ (global) by `scr init`, not per-project
│   ├── verify/                      ← per-artifact sanity check (≤2k tokens)
│   ├── deliverable-review/          ← forked parallel seven-lens review (≤12k tokens)
│   ├── wiki-ingest/                 ← raw/ → wiki/ distillation
│   ├── wiki-lint/                   ← orphans, contradictions, stale, page-budget violations
│   ├── research-cleanup/            ← orphans + intermediates + unused charts proposal
│   ├── scan-sources/                ← registry-driven targeted scraping
│   └── web-scraping/                ← Playwright/httpx/BeautifulSoup + AI-extraction toolkit (delegated to by /scan-sources)
└── settings.template.json           ← copied to .claude/settings.json (project-shared)

docs/
├── insights-mechanism.md            ← design rationale + tradeoffs
├── handoff-mechanism.md             ← multi-time-scale handoff design rationale
├── plan-structure-mechanism.md      ← scc adaptation for research, layout rationale
├── wiki-architecture.md             ← Karpathy three-layer, page budgets, ingest/query/lint
├── verification-architecture.md     ← /verify + /deliverable-review design rationale
├── source-registry-mechanism.md     ← registry format, dedup, freq logic, fail-modes
├── data-sources-mechanism.md        ← flat folder, INDEX, anchor-as-smoke-test rationale
├── methods-mechanism.md             ← sub-folder, vN evolution, diagnostic-counts rationale
├── project-conventions-mechanism.md ← why a separate folder, no enforced sections, no anchors
├── audience-and-philosophy.md       ← design constitution for users + contributors
└── extending.md                     ← how to add new conventions/hooks

templates/
├── CLAUDE.md.template               ← short CLAUDE.md scaffold with all v1 pointer blocks
├── insights/INDEX.md                ← empty INDEX seed
├── wiki/                            ← SCHEMA.md + README.md + index.md + log.md (Karpathy seeds)
├── raw/README.md                    ← immutable-sources convention (incl. raw/sources/<slug>/)
├── sources/                         ← registry.yaml + README.md + seen.jsonl (registry seeds)
├── data_sources/                    ← INDEX.md + README.md + EXAMPLE_world_bank_api.md (data-sources seeds)
├── methods/                         ← README.md + EXAMPLE_method/rule.md (methods seeds)
├── project_conventions/             ← INDEX.md + README.md + EXAMPLE_visualization.md (project-conventions seeds)
├── handoff.md                       ← session-end handoff template
├── decision-record.md               ← decision-record fillable template
└── deliverables/                    ← three v1 profiles, each with PROFILE.md + template.md
    ├── country-diagnostic-memo/     ← 4–7k words, technical-peer audience
    ├── ministerial-briefing/        ← ≤1.2k words / 2pp hard cap, executive audience
    └── internal-research-memo/      ← 5–12k words, working-through-a-question
```

Hooks are pure bash + standard Unix tools. The `scr` CLI requires Node ≥18 (one runtime dep: `commander`); everything `scr init` installs into a target project is plain markdown, JSON, YAML, or shell.

## Quickstart — install into an existing research project

```bash
npm install -g github:andresfortunato/super-claudio-research
cd /path/to/your/research-project
scr init
```

`scr init` is idempotent — safe to re-run. It copies `.claude/{conventions,hooks}/`, the project-relative `.claude/settings.json`, the `templates/` seeds (insights, wiki, raw, sources, data_sources, methods, project_conventions, deliverables), `CLAUDE.md`, and a framework block in `.gitignore` into the target project — collaborators (human or AI) cloning the project repo inherit them. Skills and agents go *global*: they're symlinked into `~/.claude/{skills,agents}/` once and shared across every project on the machine, so a skill upgrade lands everywhere automatically. Existing files (`CLAUDE.md`, `.claude/settings.json`, user-edited convention files) are never overwritten.

### Pulling framework updates into an existing project

```bash
cd /path/to/your/research-project
scr init --upgrade
```

For each framework convention or template seed, `--upgrade` either copies it in (if absent), silently skips it (if byte-identical), or writes a `<file>.framework-new` sidecar (if divergent — your version stays put). Review sidecars with your preferred diff tool and merge manually. `CLAUDE.md`, `insights/INDEX.md`, `wiki/index.md`, `wiki/log.md`, `sources/registry.yaml`, and other user-curated seeds are left alone.

### Project → project convention sync

To copy a working set of conventions from one of your project repos into another (without going through the framework):

```bash
cp -R /path/to/source-project/.claude/conventions/. /path/to/dest-project/.claude/conventions/
```

`cp -R` overwrites — review with `git diff` in the destination repo before committing.

## Conventions installed

### `insights-logging`

After substantive data analysis, write `insights/NN_<slug>.md` (3–8 evidence-based findings with concrete numbers) and append a row to `insights/INDEX.md`. The Stop hook fires only when uncommitted analysis artifacts exist (`output/0[0-9][a-z]?_*.{png,csv,meta.json}`, `methods/*.md`) and no new `insights/*.md` is staged.

Projects carrying multiple parallel lines of inquiry — each with its own audience and deliverable target — may opt into a one-level subfolder layout: `insights/<theme>/NN_*.md` and `output/<theme>/NN_*`. Flat is the default; the hook accepts both shapes; no `themes.md` declaration is required.

See `.claude/conventions/insights-logging.md`, `docs/insights-mechanism.md`, and `docs/theme-parallel-mechanism.md`.

### `script-header` + `analytical-commit-format`

Reproducibility audit without an automatic log. Every analytical script (R / Python / Stata) starts with a fixed-shape header — Script / Inputs / Outputs / Seed / Env. Every commit that produces or modifies analytical artifacts under `output/`, `insights/`, or `deliverables/<name>/charts/` includes `Run:` and `Out:` lines in the message. Together: `git log -- output/06c.png` resolves to a commit, the commit message names the script, the script's header documents inputs/seed/env. No JSONL log, no `jq` dependency, no PostToolUse hook — git carries the trail.

See `.claude/conventions/script-header.md` and `.claude/conventions/analytical-commit-format.md`.

### `handoff-format`

End of any working session that touched a `plan/plan-<name>/`: rewrite that plan's `handoff.md` in place. Multi-time-scale: within-session, researcher↔researcher (branch handoff), project→follow-up-years-later.

See `.claude/conventions/handoff-format.md` and `docs/handoff-mechanism.md`. Template: `templates/handoff.md`.

### `plan-structure`

Multi-session work lives at `plan/plan-<slug>/{plan.md, handoff.md, log.md}` (scc-style, at project root). Verification is **domain-shaped** — sign-of-coefficients, magnitude sanity, breakpoint alignment, source-citation present — not code-shaped. Methodology calls cross-link to `decisions/`.

See `.claude/conventions/plan-structure.md` and `docs/plan-structure-mechanism.md`.

### `decision-records`

The policy-research analog of pre-registration. Methodology calls you'd defend in peer review (deflator choice, identification strategy, sample restriction) get filed once at `decisions/YYYY-MM-DD_<slug>.md` with five sections: Decision / Alternatives / Why-rejected / Key-assumptions / What-would-invalidate. Lighter than ADRs but heavier than nothing.

See `.claude/conventions/decision-records.md`. Template: `templates/decision-record.md`.

### `methods`

Operational project-internal rules — how an entrant cohort is defined, which exclusions apply, what threshold gates inclusion — live in `methods/<method-slug>/rule.md` with seven required sections: Source / Rule / Why-this-version / Exclusions / Edge cases / Known limitations / Diagnostic counts. One sub-folder per method (rules accrete codebooks, PDFs, helper queries); rule files evolve `v1 → v2 → v3` with the prior version preserved in-doc. Boundary: `decisions/` is peer-reviewable methodology calls; `wiki/concepts/` is distilled domain claims with citations; `methods/` is project-internal rules with diagnostic counts. Contestable methods cross-link to a `decisions/` record.

See `.claude/conventions/methods.md` and `docs/methods-mechanism.md`. Template: `templates/methods/EXAMPLE_method/rule.md`.

### `project-conventions`

Project-bespoke style and process rules — visualization color choices, writing voice, slide design, naming idioms — live in a flat `project_conventions/<domain>.md` folder with `INDEX.md` for quick-nav. One file per domain, lowercase snake_case; every file opens with "Use this document whenever ..." so Claude knows when to load it on demand. Unlike `data_sources/` and `methods/`, no required internal sections — style rules don't fit a single template; the convention enforces only naming and triggering language. Boundary: `.claude/conventions/` is framework-shared protocols; `data_sources/` is external-system reference docs with anchors; `methods/` is operational compute rules with diagnostic counts; `project_conventions/` is project decisions about how *this engagement* does its work. Principle 9 (freshness anchors) deliberately does not bind — these are decisions, not aging claims.

See `.claude/conventions/project-conventions.md` and `docs/project-conventions-mechanism.md`. Templates: `templates/project_conventions/{INDEX,README,EXAMPLE_visualization}.md`.

### Wiki layer (Karpathy three-layer)

Two skills (`/wiki-ingest`, `/wiki-lint`) plus the schema doc that lives in target projects (`templates/wiki/SCHEMA.md`). `raw/` is immutable; `wiki/` is LLM-owned distilled knowledge. Page types — source (≤300 words), concept (≤800), entity (≤600), synthesis (uncapped + `last_condensed` frontmatter required). `/wiki-ingest <raw/path>` distills; `/wiki-lint` flags orphans, contradictions, stale pages, and budget violations. Researchers may correct factual errors; ingest is always explicit.

See `docs/wiki-architecture.md`. Schema travels with target projects in `wiki/SCHEMA.md`.

### `source-registry` + `/scan-sources`

Project-level YAML watchlist (`sources/registry.yaml`) of news / company / policy / infra / investment URLs to track continuously, plus the `/scan-sources` skill that re-scrapes entries due for re-fetch. Fields per entry: `slug`, `url`, `category`, `freq` (`daily` / `weekly` / `monthly` / `adhoc`), `last_scraped`, `scrape_method`, `content_selector`, `notes`. Dedup is content-hash via `sources/seen.jsonl`. Fresh content lands in `raw/sources/<slug>/YYYY-MM-DD_<title-slug>.md` and requires explicit `/wiki-ingest` to become wiki-promoted (so the researcher controls what becomes load-bearing). Fetching delegates to the existing `web-scraping` skill (rate limits, robots.txt, identifiable User-Agent inherited). `/scan-sources` is always explicit — never auto-fires on a clock. Flags: `--slug=<slug>` (single source), `--category=<cat>` (filtered), `--force` (bypass freq window).

See `.claude/conventions/source-registry.md` and `docs/source-registry-mechanism.md`. Registry seed: `templates/sources/registry.yaml`.

### `data-sources`

API/dataset reference docs — "how to access World Bank's wbgapi", "how IMF SDMX dataflows are structured" — live in a flat `data_sources/<source>_<thing>.md` folder with six required sections: Status (verified-as-of date) / Headline anchor (a concrete value future-Claude can re-fetch as a smoke test) / Endpoints / Query shape / Parsing / Pitfalls. `data_sources/INDEX.md` is the quick-nav table. Boundary: `raw/sources/` holds *fetched content* governed by the source-registry; `data_sources/` holds *how-to-access* docs written by hand. The headline-anchor + freshness pattern is the load-bearing discipline — re-fetching the anchor proves the doc is still accurate.

See `.claude/conventions/data-sources.md` and `docs/data-sources-mechanism.md`. Templates: `templates/data_sources/{INDEX,README,EXAMPLE_world_bank_api}.md`.

### `/verify` — per-artifact sanity check

User-invoked, ≤2k tokens. Pick one artifact — a regression result, a chart, or a paragraph — and run 3–5 domain-shaped checks: sign-of-coefficients, magnitude plausibility, missingness handling, source citation present, provenance (does `git log` resolve the artifact to a script with a valid header?). Three artifact-type check menus; the skill picks per invocation, biased toward cheap checks. Run before publishing or handing off — not as a routine background pass.

See `.claude/skills/verify/SKILL.md` and `docs/verification-architecture.md`.

### `/deliverable-review` — forked parallel seven-lens review

User-invoked, ≤12k tokens total. Spawns one subagent per lens (data validity, identification/reasoning, robustness, framing, audience-fit, political-economy realism, peer-Lab plausibility), each in a separate context (~1.5k tokens each); a synthesizer reconciles their structured reports into a single audit. Run only on advanced deliverable drafts (last-mile, not exploratory). Lens weighting per deliverable type comes from `templates/deliverables/<profile>/PROFILE.md`.

See `.claude/skills/deliverable-review/SKILL.md` and `docs/verification-architecture.md`.

### `/research-cleanup` — orphan + intermediate audit

User-invoked. Audits the project for accumulated cruft: orphan scripts older than 30 days, intermediate CSVs older than `data/raw/`'s most-recent-change watermark, charts not referenced by any insight or deliverable, notebook cells marked as scratch. Produces a markdown proposal at `cleanup-proposal.md`; the researcher reviews and acts manually. **Never deletes, moves, or modifies anything itself.** Run before milestones (close-out, hand-off, open-sourcing).

See `.claude/skills/research-cleanup/SKILL.md`.

### Deliverable profiles

Three profiles ship in v1 — each is a `PROFILE.md` (length target, register, audience, success criteria, recommended `/deliverable-review` lens weights) plus a `template.md` (skeleton). Use the profile that matches the audience; copy the template into `deliverables/<your-deliverable>/` to start.

- **`country-diagnostic-memo`** — 4–7k words / 10–18 pages of body + ≤500-word executive summary; technical-peer audience; flagship analytic deliverable. Heavy weight on data validity + identification + robustness lenses.
- **`ministerial-briefing`** — 500–1.2k words / 2-page hard cap; executive audience ("read in the back of a car between meetings"). Heavy weight on framing + audience-fit + political-economy realism.
- **`internal-research-memo`** — 5–12k words; working through a question, not landing a polished conclusion. Permissive length; even-weighted lenses.

See `templates/deliverables/<profile>/PROFILE.md` for each.

Project-development backlog (v1.1+ items, open design questions) lives in `TODO.md` at the framework root.

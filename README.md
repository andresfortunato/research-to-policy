# super-claudio-research

A Claude Code harness for **research projects** — applied economics, data analysis, and policy research.

The default Claude Code experience is built for software engineering. Research projects have different rhythms: long multi-session plans, evidence accumulation across phases, the need to remember what was *learned* (not just what was *built*), and a constant temptation to over-produce charts without distilling findings. This framework adds the lightweight conventions and hooks that make Claude Code work for that flow.

## Design philosophy

1. **Externalize conventions, hook the discipline.** Long-form rules live in `.claude/conventions/*.md` (read on demand) — not in CLAUDE.md (loaded every session). A small Stop hook checks state and *nudges* Claude when the discipline is being skipped. CLAUDE.md stays short.
2. **Conditional hooks, not always-fire prompts.** Every hook script must be **silent by default** and only emit `additionalContext` when the actual condition holds. Always-fire hooks pressure Claude to comply mechanically (writing trivial insights to "satisfy the rule"), which destroys the signal.
3. **Composable, not monolithic.** Each convention is one file in `conventions/` and (optionally) one script in `hooks/`. Adopt only what your project needs.
4. **Project-shared, not user-personal.** Everything in `.claude/conventions/`, `.claude/hooks/`, and `.claude/settings.json` is committed to the research repo so collaborators (human or AI) get the same scaffolding. User-personal config stays in `.claude/settings.local.json` (gitignored).

## What's in here

```
.claude/
├── conventions/
│   ├── insights-logging.md          ← evidence-based findings doc protocol
│   ├── manifest-logging.md          ← JSONL audit log of every analytical Bash run
│   ├── handoff-format.md            ← multi-time-scale session-end handoff protocol
│   ├── plan-structure.md            ← plan/plan-<slug>/ layout for multi-session work
│   └── decision-records.md          ← Decision/Alternatives/Why/Invalidate template
├── hooks/
│   ├── check-insights.sh            ← Stop hook (silent unless analysis lacks insights doc)
│   ├── log-manifest.sh              ← PostToolUse/Bash, silent JSONL append per analytical run
│   ├── pre-compact.sh               ← PreCompact, snapshots active plan handoff before compaction
│   └── post-compact-restore.sh     ← SessionStart matcher=compact, surfaces snapshot on resume
├── skills/
│   ├── wiki-ingest/                 ← raw/ → wiki/ distillation
│   └── wiki-lint/                   ← orphans, contradictions, stale, page-budget violations
├── agents/                          ← subagents (populated by Phase 4)
└── settings.template.json           ← copy to your project's .claude/settings.json

docs/
├── insights-mechanism.md            ← design rationale + tradeoffs
├── manifest-mechanism.md            ← why JSONL, field-by-field, tradeoffs, extension points
├── handoff-mechanism.md             ← multi-time-scale handoff design rationale
├── plan-structure-mechanism.md      ← scc adaptation for research, layout rationale
├── wiki-architecture.md             ← Karpathy three-layer, page budgets, ingest/query/lint
└── extending.md                     ← how to add new conventions/hooks

templates/
├── CLAUDE.md.template               ← short CLAUDE.md scaffold with all v1 pointer blocks
├── insights/INDEX.md                ← empty INDEX seed
├── wiki/                            ← SCHEMA.md + README.md + index.md + log.md (Karpathy seeds)
├── raw/README.md                    ← immutable-sources convention
├── handoff.md                       ← session-end handoff template
├── decision-record.md               ← decision-record fillable template
├── manifest.jsonl                   ← empty seed (target-project audit log)
└── deliverables/                    ← memo / briefing / report profiles (populated by Phase 6)
```

**Hard dependency:** `jq` is required by `log-manifest.sh` (the manifest hook). Install via `brew install jq` or your package manager. Hook fails silent if `jq` is missing — no log row written, no error either.

## Quickstart — install into an existing research project

```bash
git clone https://github.com/<you>/super-claudio-research $HOME/GitHub/super-claudio-research
cd /path/to/your/research-project
bash $HOME/GitHub/super-claudio-research/install.sh .
```

`install.sh` is idempotent — safe to re-run as the framework grows. It mirrors `.claude/{conventions,hooks,skills,agents}/` and the `templates/` seeds (insights, wiki, raw, deliverables) into your project, seeds an empty `manifest.jsonl`, copies `settings.template.json` to `.claude/settings.json` (only if absent — your customizations are preserved), and appends a framework block to `.gitignore` that shares the framework scaffolding while hiding local working state (`plan/`, `brainstorms/`, `.scc/`).

## Conventions installed

### `insights-logging`

After substantive data analysis, write `insights/NN_<slug>.md` (3–8 evidence-based findings with concrete numbers) and append a row to `insights/INDEX.md`. The Stop hook fires only when uncommitted analysis artifacts exist (`output/0[0-9][a-z]?_*.{png,csv,meta.json}`, `methods/*.md`) and no new `insights/*.md` is staged.

See `.claude/conventions/insights-logging.md` and `docs/insights-mechanism.md`.

### `manifest-logging`

Every analytical Bash run (`Rscript`, `python`, `python -m`, `stata`) is silently logged as one JSON line in `manifest.jsonl` at the project root. Schema: `timestamp / script / language / inputs / outputs / output_sha256 / seed / env_hash / git_sha / phase`. The PostToolUse hook is silent on non-analytical commands (`ls`, `git`, `cat`, …) and never writes to stdout. Audit ritual uses `jq` queries to reproduce a specific output.

See `.claude/conventions/manifest-logging.md` and `docs/manifest-mechanism.md`.

### `handoff-format`

End of any working session that touched a `plan/plan-<name>/`: rewrite that plan's `handoff.md` in place. Multi-time-scale: within-session (compact-resume), researcher↔researcher (branch handoff), project→follow-up-years-later. The `pre-compact.sh` hook snapshots the active handoff before context loss; `post-compact-restore.sh` (SessionStart matcher `compact`) surfaces it on resume.

See `.claude/conventions/handoff-format.md` and `docs/handoff-mechanism.md`. Template: `templates/handoff.md`.

### `plan-structure`

Multi-session work lives at `plan/plan-<slug>/{plan.md, handoff.md, log.md}` (scc-style, at project root). Verification is **domain-shaped** — sign-of-coefficients, magnitude sanity, breakpoint alignment, source-citation present — not code-shaped. Methodology calls cross-link to `decisions/`.

See `.claude/conventions/plan-structure.md` and `docs/plan-structure-mechanism.md`.

### `decision-records`

The policy-research analog of pre-registration. Methodology calls you'd defend in peer review (deflator choice, identification strategy, sample restriction) get filed once at `decisions/YYYY-MM-DD_<slug>.md` with five sections: Decision / Alternatives / Why-rejected / Key-assumptions / What-would-invalidate. Lighter than ADRs but heavier than nothing.

See `.claude/conventions/decision-records.md`. Template: `templates/decision-record.md`.

### Wiki layer (Karpathy three-layer)

Two skills (`/wiki-ingest`, `/wiki-lint`) plus the schema doc that lives in target projects (`templates/wiki/SCHEMA.md`). `raw/` is immutable; `wiki/` is LLM-owned distilled knowledge. Page types — source (≤300 words), concept (≤800), entity (≤600), synthesis (uncapped + `last_condensed` frontmatter required). `/wiki-ingest <raw/path>` distills; `/wiki-lint` flags orphans, contradictions, stale pages, and budget violations. Researchers may correct factual errors; ingest is always explicit.

See `docs/wiki-architecture.md`. Schema travels with target projects in `wiki/SCHEMA.md`.

## Roadmap

The framework is built incrementally. The current scoped release is **v1**, designed for the May 2026 Córdoba/Cambodia kickoff workshop and the two pilots' close-out periods (end-Aug and end-Sept 2026). See `plan/plan-v1-framework/plan.md` for the full sequenced build.

### v1 — build progress

| Phase | Title | Status |
|---|---|---|
| 1 | Foundation: directory layout, settings, install.sh | ✅ shipped |
| 2 | Wiki layer (Karpathy three-layer) — `/wiki-ingest`, `/wiki-lint`, schema, page-type budgets | ✅ shipped |
| 3 | Manifest + reproducibility hook — silent PostToolUse JSONL log | ✅ shipped |
| 4 | `/verify` + `/deliverable-review` skills | next |
| 5 | Handoff / plan-structure / decision-records conventions + PreCompact/SessionStart hooks | ✅ shipped |
| 6 | `/research-cleanup` skill + initial deliverable profiles | next |
| 7 | Source registry + `/scan-sources` skill | next |
| 8 | Documentation polish + workshop materials | blocked |

### v1 — still to come (Phases 4, 6, 7)

- **`/verify`** skill — per-artifact, user-invoked, ≤2k tokens. Sign / magnitude / missingness / source-citation checks against domain rules. Reads `manifest.jsonl` to scope what was produced.
- **`/deliverable-review`** skill — forked parallel review (≤12k tokens) with policy-research lenses (data validity, identification, robustness, framing, audience-fit, political-economy realism, peer-Lab plausibility).
- **`/research-cleanup`** skill — orphan scripts, intermediate CSVs, unused charts. Produces a proposal; researcher signs off; never auto-deletes.
- **Initial deliverable profiles** — `country-diagnostic-memo`, `ministerial-briefing`, `internal-research-memo`. Each has a length target, register, audience, success criteria, and recommended `/deliverable-review` lenses.
- **`source-registry`** convention + **`/scan-sources`** skill — project-level YAML watchlist for targeted continuous scraping (delegates fetching to the existing `web-scraping` skill, dedupes by content hash, lands content in `raw/sources/<slug>/` for explicit `/wiki-ingest` later).

### v1.1 and beyond

- **`evidence-ledger`** — a project-level table of formal claims, the chart/CSV that supports each, and whether the claim has been challenged.
- **`chart-registry`** — `save_fig(findings={...})` pattern so every chart ships with metadata Claude can read without re-opening the PNG.
- **`citation-discipline`** — every quantitative claim must reference a source (paper, dataset, internal doc).
- **LaTeX/Beamer add-on** — borrowed from Pedro/Hugo Sant'Anna's templates; useful when the deliverable register shifts toward academic outputs.
- **WIP-limited multi-project dashboard** (Hugo's vault-manager pattern) — for researchers juggling multiple country engagements.
- **Stata first-class support** — alongside R and Python.
- **Mode-registry / cross-skill advisor** (Imbad pattern) — once skill count exceeds ~8 and "which entry point?" becomes the bottleneck.

Each addition follows the same pattern: one convention file in `.claude/conventions/`, optionally one hook script in `.claude/hooks/`, one section in `docs/`, optionally a skill in `.claude/skills/`. See `docs/extending.md`.

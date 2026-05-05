# super-claudio-research

A Claude Code harness for **research projects** — applied empirical, data-analytical, and policy work.

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
│   └── insights-logging.md          ← evidence-based findings doc protocol
├── hooks/
│   └── check-insights.sh            ← Stop-hook nudge (silent unless tripped)
├── skills/                          ← invokable Anthropic-format skills (populated by v1)
├── agents/                          ← subagents for forked review fan-out (populated by v1)
└── settings.template.json           ← copy to your project's .claude/settings.json

docs/
├── insights-mechanism.md            ← design rationale + tradeoffs
└── extending.md                     ← how to add new conventions/hooks

templates/
├── CLAUDE.md.template               ← short CLAUDE.md scaffold (pointer-style)
├── insights/INDEX.md                ← empty INDEX seed
├── wiki/                            ← Karpathy three-layer wiki seeds (populated by v1)
├── raw/                             ← immutable-sources convention (populated by v1)
└── deliverables/                    ← memo / briefing / report profiles (populated by v1)
```

## Quickstart — install into an existing research project

From the root of your research project:

```bash
SUPER_CLAUDIO=$HOME/GitHub/super-claudio-research

# 1. Copy conventions, hooks, settings template
mkdir -p .claude/conventions .claude/hooks
cp $SUPER_CLAUDIO/.claude/conventions/*.md .claude/conventions/
cp $SUPER_CLAUDIO/.claude/hooks/*.sh .claude/hooks/
chmod +x .claude/hooks/*.sh

# 2. Set up settings.json (only if you don't have one yet)
[ ! -f .claude/settings.json ] && cp $SUPER_CLAUDIO/.claude/settings.template.json .claude/settings.json

# 3. Seed the insights/ tree
mkdir -p insights
[ ! -f insights/INDEX.md ] && cp $SUPER_CLAUDIO/templates/insights/INDEX.md insights/INDEX.md

# 4. .gitignore — share conventions+hooks+settings, keep local state private
cat <<'GITIGNORE' >> .gitignore
# Claude Code internal state
.claude/*
!.claude/conventions/
!.claude/conventions/**
!.claude/hooks/
!.claude/hooks/**
!.claude/settings.json
GITIGNORE

# 5. Add the pointer to your CLAUDE.md (or create one from the template)
[ ! -f CLAUDE.md ] && cp $SUPER_CLAUDIO/templates/CLAUDE.md.template CLAUDE.md
```

Or use `./install.sh <target-project-path>` from this repo.

## Conventions installed

### `insights-logging`

After substantive data analysis, write `insights/NN_<slug>.md` (3–8 evidence-based findings with concrete numbers) and append a row to `insights/INDEX.md`. The Stop hook fires only when uncommitted analysis artifacts exist (`output/0[0-9][a-z]?_*.{png,csv,meta.json}`, `methods/*.md`) and no new `insights/*.md` is staged.

See `.claude/conventions/insights-logging.md` for the protocol and `docs/insights-mechanism.md` for the design rationale.

## Roadmap

The framework is built incrementally. The current scoped release is **v1**, designed for the May 2026 Córdoba/Cambodia kickoff workshop and the two pilots' close-out periods (end-Aug and end-Sept 2026). See `plan/plan-v1-framework/plan.md` for the full sequenced build.

### v1 — being built now

- **`handoff-format`** — multi-time-scale handoff (within-session, researcher↔researcher, project→follow-up-years-later).
- **`manifest-logging`** — JSONL audit log of every analytical run (script, inputs, outputs+SHAs, env hash, git sha). Silent PostToolUse hook. Subsumes the older `reproducibility-check` idea.
- **`plan-structure`** — research-adapted version of scc's `plan/plan-<name>/` layout, with domain-shaped verification (sign-of-coefficients, magnitude sanity) replacing code-shaped tests.
- **`decision-records`** — policy-research analog of pre-registration: Decision / Alternatives / Why-rejected / Key-assumptions / What-would-invalidate.
- **`source-registry`** — project-level YAML watchlist + `/scan-sources` skill for targeted continuous scraping (delegates fetching to the existing `web-scraping` skill, dedupes by content hash, lands content in `raw/sources/<slug>/`).
- **Wiki layer** (Karpathy three-layer) — `raw/` immutable + `wiki/` LLM-owned + schema in CLAUDE.md, with `/wiki-ingest` and `/wiki-lint` skills enforcing page-type budgets.
- **`/verify`** skill — per-artifact, user-invoked, ≤2k tokens. Sign / magnitude / missingness / source-citation checks against domain rules.
- **`/deliverable-review`** skill — forked parallel review (≤12k tokens) with policy-research lenses (data validity, identification, robustness, framing, audience-fit, political-economy realism, peer-Lab plausibility).
- **`/research-cleanup`** skill — orphan scripts, intermediate CSVs, unused charts. Produces a proposal; researcher signs off; never auto-deletes.
- **Initial deliverable profiles** — `country-diagnostic-memo`, `ministerial-briefing`, `internal-research-memo`. Each has a length target, register, audience, success criteria, and recommended `/deliverable-review` lenses.

### v1.1 and beyond

- **`evidence-ledger`** — a project-level table of formal claims, the chart/CSV that supports each, and whether the claim has been challenged.
- **`chart-registry`** — `save_fig(findings={...})` pattern so every chart ships with metadata Claude can read without re-opening the PNG.
- **`citation-discipline`** — every quantitative claim must reference a source (paper, dataset, internal doc).
- **LaTeX/Beamer add-on** — borrowed from Pedro/Hugo Sant'Anna's templates; useful when the deliverable register shifts toward academic outputs.
- **WIP-limited multi-project dashboard** (Hugo's vault-manager pattern) — for researchers juggling multiple country engagements.
- **Stata first-class support** — alongside R and Python.
- **Mode-registry / cross-skill advisor** (Imbad pattern) — once skill count exceeds ~8 and "which entry point?" becomes the bottleneck.

Each addition follows the same pattern: one convention file in `.claude/conventions/`, optionally one hook script in `.claude/hooks/`, one section in `docs/`, optionally a skill in `.claude/skills/`. See `docs/extending.md`.

## Why "super-claudio"

This is a meta-harness — Claude Code on top of Claude Code. The discipline added here is what makes Claude Code reliable for research where the value is in *what was learned*, not just *what was shipped*.

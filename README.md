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
└── settings.template.json           ← copy to your project's .claude/settings.json

docs/
├── insights-mechanism.md            ← design rationale + tradeoffs
└── extending.md                     ← how to add new conventions/hooks

templates/
├── CLAUDE.md.template               ← short CLAUDE.md scaffold (pointer-style)
└── insights/INDEX.md                ← empty INDEX seed
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

The framework is intentionally minimal. Future conventions to add (in order of likely value for research workflows):

- **`handoff-format`** — standardized session-end handoff for multi-phase plans
  (status table, what didn't work, surprises, what's next).
- **`evidence-ledger`** — a project-level table of formal claims, the chart/CSV
  that supports each, and whether the claim has been challenged.
- **`chart-registry`** — `save_fig(findings={...})` pattern so every chart ships
  with metadata Claude can read without re-opening the PNG.
- **`reproducibility-check`** — a Stop hook that flags new analysis without a
  re-runnable script in `scripts/`.
- **`citation-discipline`** — every quantitative claim must reference a
  source (paper, dataset, internal doc).
- **`plan-structure`** — multi-phase plan format aligned to the SCC plugin's
  `plan/plan-<name>/` directory layout.

Each addition follows the same pattern: one convention file in `.claude/conventions/`, optionally one hook script in `.claude/hooks/`, one section in `docs/`. See `docs/extending.md`.

## Why "super-claudio"

This is a meta-harness — Claude Code on top of Claude Code. The discipline added here is what makes Claude Code reliable for research where the value is in *what was learned*, not just *what was shipped*.

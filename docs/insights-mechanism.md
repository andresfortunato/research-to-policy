# Insights mechanism — design rationale

## The problem this solves

Research sessions produce a lot of artifacts — charts, panel CSVs, methods notes, derived tables. By default, Claude Code (and most AI coding agents) **report what they did** in their reply text and move on. The artifacts pile up; what was *learned* from them gets buried in the conversation, then lost when the session ends.

The traditional fix — "tell Claude to summarize at the end of every session" — has two failure modes:
1. **In CLAUDE.md**: a long protocol loads every turn (40+ lines), even on sessions that don't need it. Context bloat.
2. **As an always-fire reminder**: Claude is pressured to write something at every stop, so it writes trivial summaries to "comply" with the rule. Signal collapses.

The insights mechanism is engineered to avoid both.

## Three pieces

### 1. The convention file (`.claude/conventions/insights-logging.md`)

Defines what counts as an insight, the file structure, the numbering protocol, and the discipline (one commit, never overwrite). Lives outside CLAUDE.md and is read **only when Claude is actually writing an insights doc**. Cost: zero context tokens on sessions that don't trigger it.

### 2. The CLAUDE.md pointer (~4 lines)

Just enough to make Claude aware the convention exists and where to look:
```
## Insights Logging
After any substantive data analysis: write insights/NN_<slug>.md and update
insights/INDEX.md. Full protocol: .claude/conventions/insights-logging.md
(read on demand). A Stop hook nudges if artifacts were produced without an
insights doc.
```

### 3. The Stop hook (`.claude/hooks/check-insights.sh`)

The discipline-enforcer. Runs at every turn-end. **Silent by default.** Emits `additionalContext` only when both conditions hold:

```
Tripwire 1: Uncommitted analysis artifacts present
   git status -u | grep -E 'output/0[0-9][a-z]?_*.(png|csv|meta\.json)|methods/.*\.md'

AND

Tripwire 2: No new insights/*.md in git status
   git status -u | grep -E 'insights/[0-9]+_.*\.md'  ← must be empty
```

When both fire, the hook returns JSON with a one-shot reminder pointing at the convention file. When either fails, the hook exits 0 silently.

## Why these specific tripwires

- **Notebook-prefixed artifacts** (`output/0[0-9][a-z]?_*`) is the right granularity for "real analysis" because the project naming convention attaches a notebook number to every chart-registry artifact. PNGs without a number prefix (presentations, ad-hoc explorations) don't trigger.
- **`methods/*.md`** catches the case where a methodology note is written without a corresponding insights doc.
- **Uncommitted state** (`git status` not git log) means the hook fires on the working session, not on past commits. Once analysis + insights are committed together, the hook stays silent for unrelated future sessions.

## What this does NOT do

- **Doesn't enforce quality.** The hook can detect that an insights doc is missing; it can't detect that the insights are weak. Quality is still on the human + AI to maintain.
- **Doesn't auto-write the doc.** The hook nudges; Claude writes. This is intentional — auto-generated insights are exactly the trivial summaries we're trying to avoid.
- **Doesn't fire on research/exploration sessions.** If Claude reads files, runs ad-hoc queries, and produces nothing in `output/0*` or `methods/`, the hook stays silent.

## Tradeoffs accepted

- **Pattern coupling to naming convention.** The framework assumes notebook-prefixed `output/0[0-9][a-z]?_*` filenames. Projects with different conventions need to edit the regex in `check-insights.sh`. This is the cost of detection precision.
- **Mid-analysis nudges.** The hook fires after every turn that satisfies the conditions, not only at "end of session." A multi-turn analysis session will see the nudge multiple times until insights are written. Trade: some extra prompts in exchange for a real "did you do this?" check at every checkpoint.
- **No fallback when git is unavailable.** The hook silently exits in non-git directories. For non-git research projects, the hook is inert.

## Extension points

- **Tighten the trigger**: edit the analysis-hit regex in `check-insights.sh` to match your project's artifact naming.
- **Add tripwires**: e.g. fire on new files in `regressions/` or `tables/` for projects that organize artifacts differently.
- **Loosen the snooze**: append `[ -f .insights-skip ] && exit 0` near the top so users can `touch .insights-skip` to silence the hook for a session.
- **Hard block** (not recommended for most cases): change the JSON output to include `"decision": "block"` to force continuation. Use sparingly — adds friction.

## Provenance

This mechanism originated in a Cambodia growth-diagnostics project where multi-phase analysis kept producing charts faster than findings were being distilled. After 7 phases, the team realized the most useful artifact across plans was a *project-level insights index* — and the only way to keep it populated was to make "writing the insight" a turn-stop concern, not a session-end concern.

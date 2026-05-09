---
name: r2p-adopt
description: Audit an existing, pre-framework research project and propose how to map it onto the research-to-policy structure — file classification (raw/output/scripts/decisions), CLAUDE.md and .claude/ reconciliation, methodology archaeology (extracting decisions from READMEs and script docstrings), and orphan detection. Use when the user says "adopt this framework", "onboard existing project", "/r2p-adopt", "migrate this messy project to r2p", "how do I apply r2p to this old project", or otherwise asks to bring an already-existing project under the framework. Produces a markdown proposal at `ADOPTION_PROPOSAL.md`; the researcher reviews and executes the moves manually. NEVER moves, deletes, or rewrites anything.
allowed-tools: Read, Write, Bash, Glob, Grep
disable-model-invocation: true
---

<!--
This skill is dormant by default. It only fires when the user explicitly types
`/r2p-adopt`. Adoption is a one-shot transition; routing on natural-language
prompts ("clean this up", "this is messy") would mis-fire on already-adopted
projects. The seed `.claude/settings.json` also sets
`skillOverrides: {"r2p-adopt": "user-invocable-only"}` so the description
doesn't load into Claude's context across sessions — defense in depth.
-->


# r2p-adopt

One-time audit for bringing an existing, pre-framework research project under
research-to-policy. Walks the tree, classifies files against framework slots,
reconciles any prior `CLAUDE.md` or `.claude/` content, surfaces methodology
calls hidden in READMEs and script docstrings as candidate decision records,
and flags orphan analysis. Output is a single markdown file at the project
root (`ADOPTION_PROPOSAL.md`); the researcher executes the moves by hand. The
skill never moves, deletes, edits, or commits.

## When to invoke

- Right after `r2p init` on an existing, disorganized project — random scripts
  at the root, charts mixed with data, methodology buried in READMEs.
- The user says "adopt this", "onboard this project", "/r2p-adopt", "how do
  I apply r2p to this old repo", "migrate this messy project".
- Once per project. Adoption is a transition, not a recurring task.

## When NOT to invoke

- **Greenfield projects.** `r2p init` lays everything down clean; nothing to
  audit.
- **Projects already r2p-native.** For ongoing maintenance use
  `/research-cleanup` instead.
- **Mid-plan or mid-analysis.** The proposal is long and the moves shouldn't
  compete with active work. Wait for a quiet moment.
- **As a recurring task.** This is a one-shot. Re-running it after the
  researcher has executed the moves produces a much shorter proposal but
  doesn't add value over `/research-cleanup`.

## Preconditions

- `r2p init` has been run. Look for `.claude/conventions/` and the
  scaffolding directories (`insights/`, `decisions/`, `archive/`, etc.). If
  missing, write a one-line proposal that says "Run `r2p init` first" and
  stop.
- Run from project root.
- Note in the preflight section if the working tree is dirty — the researcher
  should commit or stash before executing the proposed moves so the migration
  is bisectable.

## Workflow

1. **Verify the framework is installed.** Check for `.claude/conventions/`
   and the standard scaffolding dirs. If absent → write a one-section
   proposal recommending `r2p init` and stop.
2. **Walk the tree.** Glob the project for scripts, data, charts, markdown,
   and existing AI config. Skip directories listed in `audit-checklist.md`
   (`.git/`, `node_modules/`, `__pycache__/`, framework-installed dirs that
   are already in their right place, etc.).
3. **Run the four audits below.** Each populates one section of the proposal.
4. **Write `ADOPTION_PROPOSAL.md`** at project root. Overwrite if it exists —
   a previous proposal is presumed acted on or discarded.
5. **Report to the user** in one paragraph: counts per audit, where the
   proposal lives, the reminder that nothing has been moved.

Detailed classification heuristics, trigger-phrase lists, and skip-rules live
in `audit-checklist.md` next to this file. Read it before running the audits;
it's the source of truth for "is this filename pattern a raw input or a
derivative?" and similar judgment calls.

## Audits

### 1. File classification

For each non-framework file, propose a target slot under the framework.
Apply heuristics in priority order (filename pattern, then path signal,
then content peek for ambiguous cases). See `audit-checklist.md` for the
full pattern → slot table.

Findings split into four buckets:

- **Likely raw data** — moves to `raw/<source>/`. Filename has `raw_*`,
  `_orig`, or sits in a directory called `raw/` already.
- **Likely processed/intermediate** — moves to `data/processed/`. `_v2.csv`,
  `_clean`, `panel_*`, sits in `data/` but not `data/raw/`.
- **Likely chart/output** — moves to `output/`. `.png`/`.pdf`/`.svg` outside
  `output/`. Suggest a numeric prefix (`output/NN_<slug>`) for sortability if
  the project has more than ~5 charts.
- **Unclear provenance — researcher decides.** Top-level `.csv` or
  `.parquet` with no obvious raw/processed marker, files whose name doesn't
  match any pattern. List these explicitly under a "researcher decides"
  subheader rather than guessing wrong.

For markdown files outside framework dirs (`README.md`, `NOTES.md`, etc.):
peek at content. If it reads as **methodology** → flag for audit 3
(archaeology). If it reads as **findings** (specific numbers, charts
referenced, "we find") → propose extracting into `insights/NN_<slug>.md`.
If neither → leave in place and note its presence.

For scripts in `scripts/`, `src/`, `code/`, or `analysis/`: don't propose
renaming the directory — the framework doesn't mandate one. Just note its
existence and recommend the script-header convention
(`.claude/conventions/script-header.md`) gets adopted on next edit.

For notebooks (`.ipynb`): note their location only. Don't propose moves; do
recommend a separate `/research-cleanup` pass to flag scratch cells.

Each finding records: source path, proposed target path (or "<unclear —
researcher decides>"), one-sentence rationale, what was searched.

### 2. CLAUDE.md / .claude/ reconciliation

If the project predates r2p, it likely has prior AI config — `CLAUDE.md`,
`.claude/`, `.cursorrules`, `.windsurfrules`, `AGENTS.md`,
`.github/copilot-instructions.md`. The framework's `r2p init` is conservative
(never overwrites), so prior content sits alongside the new conventions.
This audit surfaces overlap and conflicts.

- **Existing `CLAUDE.md`.** Read it. For each section/rule, classify:
  - **Conflicts** with a framework convention — surface so the researcher
    decides which to keep.
  - **Duplicates** a framework rule now living in `.claude/conventions/` —
    propose deleting from `CLAUDE.md` so the convention file is the single
    source of truth.
  - **Project-specific** (research scope, dataset names, glossary, audience
    notes) — keep. This is exactly what `CLAUDE.md` is for.
  - **Operational project rule** (e.g. "always run pytest before commit") —
    propose moving to `project_conventions/<domain>.md`.
- **Pre-existing `.claude/` content.** List each file the framework didn't
  install. For each, ask the researcher: keep, delete, or merge with the
  matching framework artifact.
- **Other tools' AI config.** `.cursorrules`, `.windsurfrules`, `AGENTS.md`:
  propose extracting any project-bearing rules into `project_conventions/`
  so they're tool-agnostic, then leaving the original files in place
  (they're cheap and other tooling may still read them).

### 3. Methodology archaeology

The point: methodology calls deserve `decisions/` records. In a pre-framework
project they're scattered across READMEs, NOTES.md files, script docstrings,
and inline comments. This audit surfaces candidates.

For each candidate:

- Find the source location with grep. Trigger phrases live in
  `audit-checklist.md` ("we chose", "rejected because", "deflator",
  "specification", "exclusion", etc.).
- Record the file path and approximate line number.
- Quote the candidate sentence/paragraph.
- Propose a `decisions/YYYY-MM-DD_<slug>.md` filename. Date is best-guess
  from `git log -1 --format=%ad <file>`; today's date if no git history.
- Note: **researcher writes the full 5-section decision record** using the
  candidate paragraph as raw material. The skill surfaces; the researcher
  deliberates.

Don't auto-generate decision records. Methodology calls deserve the
researcher's deliberation — the value of `decisions/` comes from the
researcher having actually thought through "what would invalidate this".

### 4. Orphan analysis

This overlaps with `/research-cleanup`. Adoption is a natural moment to
confront accumulated cruft, so we run it once here. After adoption, defer
to `/research-cleanup`. Cross-link in the proposal so the researcher knows.

- **Charts without insights.** For every image under `output/`, `figures/`,
  `charts/`, or any directory with >5 image files: grep its basename across
  all `.md` files in the project. Zero hits → orphan candidate. Propose
  either writing a retroactive `insights/NN_<slug>.md` (if the chart is
  load-bearing — filename suggests it answers a question) or noting it for
  later cleanup.
- **Scripts without inbound references.** For every script outside framework
  dirs: grep its filename across the rest of the repo. Zero hits → potential
  orphan. Cross-check `git log --grep="Run: <script>"` for recent commits
  using the analytical-commit-format convention. Note in the proposal.
  Adoption isn't the time to delete, but the researcher should know.

## Proposal format

Write `ADOPTION_PROPOSAL.md` at project root. Schema:

```markdown
# Adoption proposal — YYYY-MM-DD

Generated by `/r2p-adopt`. **Nothing here has been moved, deleted, or
rewritten.** This proposal walks you through bringing this project under
research-to-policy. Each section lists what was found, what's proposed,
and the manual step to take. Work top-to-bottom; commit after each
section so the migration is bisectable.

## Preflight
- Framework installed: yes (`.claude/conventions/` present)
- Git status: clean / **<n> uncommitted changes — commit or stash before
  proceeding**
- Existing AI config detected: CLAUDE.md, .cursorrules

## Suggested execution order

1. Commit any pending work (preflight).
2. **Section 2** (CLAUDE.md / .claude/ reconciliation) — small, low-risk
   diff first.
3. **Section 3** (decisions/ archaeology) — high-value; doing this early
   surfaces what the project has already settled.
4. **Section 1** (file moves) — biggest diff; do it in chunks (raw/
   first, then output/, then intermediates).
5. **Section 4** (orphan analysis) — defer to a separate session, or to
   `/research-cleanup` once you're r2p-native.

After each section, commit with a message like:
- `adopt: extract methodology calls to decisions/`
- `adopt: move raw inputs to raw/`
- `adopt: prune CLAUDE.md duplicates now covered by conventions/`

## 1. File classification

### Likely raw data → `raw/<source>/`
- `data/wb_indicators_2024.csv` (847 KB) → propose
  `raw/world-bank/wb_indicators_2024.csv`. **Rationale**: filename pattern;
  treated as source of truth in scripts (no upstream generator).

### Likely processed/intermediate → `data/processed/`
- `panel_v2.csv` at root (12 MB) → propose `data/processed/panel_v2.csv`.
  **Rationale**: `_v2` suffix; modified 2026-04-15; output of
  `scripts/build_panel.py`.

### Likely chart/output → `output/`
- `fdi_chart.png` at root → propose `output/01_fdi_chart.png` (numeric
  prefix for sortability).

### Unclear provenance — researcher decides
- `combined_data.csv` (3.2 MB) at root. Could be raw download or derived.
  **Action**: open and inspect, then move to `raw/` or `data/processed/`.

### Scripts directory
- `scripts/` exists (14 .py files). Framework doesn't rename. **Action**:
  adopt `.claude/conventions/script-header.md` on next edit of each script.

(If a bucket is empty: `(none)` under that header.)

## 2. CLAUDE.md / .claude/ reconciliation

### Existing CLAUDE.md
- Lines 12–30 ("Code style") duplicate
  `.claude/conventions/script-header.md`. **Propose**: delete from
  CLAUDE.md.
- Lines 31–60 ("Project context: Cambodia case study") project-specific.
  **Keep** — this is what CLAUDE.md is for.
- Lines 61–65 ("Always run pytest before commit") operational project rule.
  **Propose**: move to `project_conventions/testing.md`.

### Pre-existing .claude/
- `.claude/hooks/format-on-save.sh` — pre-existing, no overlap with
  framework hooks. **Keep**.

### Other AI config
- `.cursorrules` — extract project-bearing rules to `project_conventions/`,
  leave file in place for Cursor users.

(If none: `(none)` under each header.)

## 3. Methodology archaeology

For each candidate, **write a `decisions/YYYY-MM-DD_<slug>.md` record**
using the source paragraph as raw material. Then either delete the
originating sentence or leave a one-line pointer.

- `README.md:42–46` — "We use the World Bank deflator series rather than
  IMF WEO because WEO has gaps for Cambodia 2018–2019." → propose
  `decisions/2026-05-08_use-wb-deflator-not-weo.md`.
- `scripts/build_panel.py:1–15` (docstring) — sample exclusion: "drop
  countries with <5 years coverage". → propose
  `decisions/2026-05-08_min-five-years-coverage.md`.
- `notes.md:18` — "We exclude oil exporters from the headline sample;
  sensitivity in appendix." → propose
  `decisions/2026-05-08_exclude-oil-exporters.md`.

## 4. Orphan analysis

(Cross-link: `/research-cleanup` is the ongoing-maintenance equivalent.
This is a one-time sweep at adoption.)

### Charts without insights
- `output/explore_07.png`, `output/old_fdi_v3.png` — neither referenced in
  any markdown. **Decide**: keep + write retroactive insight, or move to
  `_archive/`.

### Scripts without inbound references
- `scripts/munge_v1.py` — superseded by v3 per filename pattern; no
  inbound references; no recent `Run:` commits. **Likely safe to archive.**

## Audits skipped (preconditions not met)

(List any audits the skill couldn't run — e.g. "chart audit skipped: no
output/, figures/, or charts/ directories present.")
```

If every audit returned zero findings, still write the file with `(none)`
under each section. The researcher needs to confirm the audit ran.

## Rules

- **Never moves a file.** Not even into a staging dir.
- **Never edits CLAUDE.md or any pre-existing file.** Suggest edits, never
  apply them.
- **Never writes a decision record.** Only surfaces candidates.
- **Never commits.** The proposal is uncommitted markdown.
- **Hedge on classification.** "Researcher decides" beats a wrong slot.
  False positives in classification cost 30 seconds; false negatives lose
  work.
- **Cite line numbers.** Every methodology-archaeology finding has a
  `file:line` reference — the researcher must verify the quote by hand.
- **Skip the directories listed in `audit-checklist.md`.** Tooling state
  (`.git/`, `node_modules/`, `__pycache__/`, etc.) and framework working
  dirs (`plan/`, `archive/` — these belong to active framework usage, not
  pre-framework legacy).
- **Don't recurse twice.** Glob once per filetype at the start of the
  workflow; cache and reuse across audits.

## Invocation example

```
User: /r2p-adopt
```

Skill walks the project, runs four audits, writes `ADOPTION_PROPOSAL.md`,
and reports:

> Wrote `ADOPTION_PROPOSAL.md`. Found 47 candidate file moves (12 raw, 8
> intermediate, 18 chart, 9 unclear-provenance), 3 sections in CLAUDE.md to
> reconcile against framework conventions, 7 methodology calls hidden in
> READMEs and script docstrings (propose 7 new decisions/ records), and 14
> orphan charts. Nothing has been moved. Review the proposal section by
> section; commit after each.

## What this skill does NOT do

- No moves, no deletes, no edits. Proposal-only.
- Doesn't run `r2p init` for you — recommends it and stops if scaffolding
  is missing.
- Doesn't write `decisions/` records — surfaces candidates only.
- Doesn't lint code, fix bugs, or refactor.
- Doesn't compete with `/research-cleanup` — that's for ongoing
  maintenance once the project is r2p-native.

## Boundary with /research-cleanup

`/r2p-adopt` runs **once**, when bringing an existing project under the
framework. Its scope: *mapping unfamiliar structure onto framework slots*
and *extracting buried methodology*. Orphan detection appears here only
because adoption is a natural moment to confront accumulated cruft.

`/research-cleanup` runs **periodically**, once the project is r2p-native.
Its scope: *catching newly-accumulated cruft against framework reference
points* (raw watermark, insights cross-references, recent `Run:` commits in
the analytical-commit-format).

After adoption, do not re-run `/r2p-adopt`. Use `/research-cleanup` for
ongoing audits.

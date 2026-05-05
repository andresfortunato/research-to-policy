---
name: verify
description: Per-artifact verification of one regression result, one chart, or one paragraph against domain rules — sign-of-coefficients, magnitudes, missingness, source citation, manifest reproducibility. Use when the user says "/verify <path>", "verify this regression", "check this chart against the manifest", "sanity-check this paragraph", or otherwise asks to inspect a single artifact for plausibility before publishing it. User-invoked only; never auto-fires. Budget ≤2k tokens.
allowed-tools: Read, Bash, Glob, Grep, Task
---

# verify

Run a tight, three-to-five-check sanity audit on a single research artifact.
This skill exists because researchers move fast, and the costliest mistakes
(a sign flip in a regression, a chart with the wrong y-axis units, a
paragraph claiming a number that no longer matches the underlying CSV)
slip through the cracks between analysis and deliverable. `/verify` is the
small-stakes companion to `/deliverable-review`: cheap enough to run
casually, narrow enough to actually finish.

## When to invoke

The user types one of:

- `/verify <path>` — point at one file (`output/06c_fdi_at_entry.png`,
  `output/regression_latest.json`, `deliverables/draft.md`, a single CSV row).
- "Verify this regression result against the manifest."
- "Sanity-check this paragraph — does the number match what's in `output/`?"
- "Does this chart's underlying data match the latest run?"

## When NOT to invoke

- The user is asking for a *full* deliverable review — that's `/deliverable-review`.
- No specific artifact is named — verify is per-artifact, not per-project.
- The artifact is still mid-edit / clearly in draft state and the user
  hasn't yet asked for a check. Verify is user-invoked only; never
  auto-fire on file writes.
- The check would require re-running the analysis end-to-end. That's
  a reproduction job, not verification — point the user at the audit
  ritual in `.claude/conventions/manifest-logging.md`.

## Preconditions

- `manifest.jsonl` exists at the project root (Phase 3 hook populates it).
  If absent, warn the user that reproducibility checks will be skipped,
  then proceed with domain-only checks.
- The target artifact path is readable. If absent, stop and tell the user.

## The check menu

Pick three to five checks appropriate to the artifact type. Do not run
every check — the budget is ≤2k tokens. Choose by artifact:

### A. Regression result (`*.json`, `*.rds`, regression-table markdown)

1. **Sign sanity.** For each coefficient, compare the sign against the
   user's stated prior or the deliverable's claim. Flag any that disagree.
   If priors aren't stated, ask the user once before flagging.
2. **Magnitude plausibility.** Are coefficients within an order of
   magnitude of comparable estimates? (e.g. an FDI elasticity of 14.2
   should raise an eyebrow; one of 0.42 typically should not.)
3. **Sample-size and missingness.** Read N, count of missing observations,
   and the share of dropped rows. Flag if N is unusually small for the
   panel structure, or if missingness > 25%.
4. **Standard-error sanity.** Are SEs clustered when the data structure
   demands it (panel, repeated-cross-section, hierarchical)? Look at the
   script that produced the result via `jq` on `manifest.jsonl`.
5. **Manifest reproducibility.** Find the `manifest.jsonl` row whose
   `outputs` includes this artifact. Confirm `output_sha256` matches
   `sha256sum <artifact>`. Mismatch means the artifact has been edited
   since it was produced — flag loudly.

### B. Chart (`*.png`, `*.pdf`, `*.svg`)

1. **Axis-and-label sanity.** Read the chart's source script (look up via
   manifest) and confirm units, axis ranges, and legend match what the
   chart's surrounding caption claims.
2. **Underlying data freshness.** Find the manifest row that produced
   this chart. Find the row that produced the *input CSV*. If the input
   CSV has a more recent run than the chart, the chart may be stale.
3. **Series count and ordering.** Cross-check the number of series and
   their ordering against the source script — extra/dropped series
   silently happen when joins are revised.
4. **Source citation.** Does the deliverable referencing this chart
   actually cite a source line? Grep for the chart filename in
   `deliverables/`, `insights/`, and confirm a citation is nearby.
5. **Manifest reproducibility.** Same as A.5.

### C. Paragraph (a span inside a markdown deliverable)

1. **Number-to-evidence trace.** For every numeric claim in the paragraph,
   find the supporting `output/`, `insights/`, or table cell. Flag any
   number that has no traceable source.
2. **Sign and magnitude consistency.** Do the numbers in the paragraph
   agree with the regression / chart they implicitly cite? If the
   regression says `+0.42` and the paragraph says "negative effect",
   that's the bug verify exists to catch.
3. **Source citation discipline.** Every external claim (e.g. "the World
   Bank reports...") must cite a source page in `wiki/sources/` or a
   file in `raw/`. Flag uncited claims.
4. **Tense and scope honesty.** A paragraph claiming "we find that X
   causes Y" when the underlying analysis is correlational is the
   most expensive class of error. Read the script's identification
   strategy via the manifest's `script` field; flag mismatches.
5. **Insight cross-check.** If the paragraph references a finding,
   confirm the corresponding `insights/NN_*.md` exists and the numbers
   match.

## Workflow

1. **Identify the artifact type** from the path / extension. Pick the
   relevant menu (A, B, or C). If ambiguous (e.g. a `.json` that's
   not a regression), ask the user once.
2. **Pick 3–5 checks** from the menu. Bias toward the cheapest checks
   first (sign, magnitude, manifest hash); only run script-reading
   checks if budget allows.
3. **For manifest-dependent checks**, delegate to the `manifest-checker`
   subagent via the Task tool. It reads `manifest.jsonl`, finds the row
   matching the artifact, and reports back the relevant fields. This
   keeps the manifest-parsing logic out of `/verify`'s context.
4. **Run the checks.** Each check produces a `pass` / `flag` / `skip`
   verdict with one sentence of evidence.
5. **Emit the report** (format below). Stop. The user decides what to act on.

## Report format

Always emit a single markdown report to stdout. Always include the
"Checks run" section with all selected checks (even passes), so the
report is useful as a record:

```markdown
# /verify <artifact-path> — YYYY-MM-DD

**Artifact type**: regression | chart | paragraph
**Manifest row found**: yes (run YYYY-MM-DD HH:MM:SS) | no

## Checks run
- [PASS] Sign sanity — all 4 coefficients match stated priors.
- [FLAG] Magnitude plausibility — coefficient on `log_fdi_gdp` is 14.2; typical range is 0.1–2.0.
- [PASS] Manifest reproducibility — output_sha256 matches.
- [SKIP] Standard-error clustering — script source not readable.

## Flags requiring researcher attention
1. Magnitude on `log_fdi_gdp` (14.2) is two orders of magnitude above
   comparable FDI elasticities. Re-check units; common cause is a
   log-vs-level mix-up on the regressor.

## Notes
- Skipped clustering check because <reason>.
- 3 of 5 menu checks executed (per ≤2k token budget).
```

If a section has zero entries, write `(none)` under it. Always emit
all three sections.

## Rules

- **Read-only.** Never edit the artifact. Never modify `manifest.jsonl`.
- **No re-running.** If a check would require re-executing the analysis,
  skip it and note that re-running is a separate step (point the user
  at the audit ritual in `.claude/conventions/manifest-logging.md`).
- **Three to five checks. Stop there.** A long verify report dilutes
  signal; a short one with a real flag is the goal.
- **Prefer flags over passes.** False positives are cheap (researcher
  glances and dismisses); silent misses are expensive.
- **Skip with explanation, not silently.** If a check can't run, say
  why in the Notes section.

## Invocation example

```
User: /verify outputs/regression_latest.json
```

Skill will:
1. Identify artifact as regression result (.json under outputs/).
2. Pick five checks from menu A: sign sanity, magnitude plausibility,
   N + missingness, SE clustering, manifest reproducibility.
3. Spawn `manifest-checker` subagent via Task to find the manifest row
   for `outputs/regression_latest.json`.
4. Confirm `output_sha256` matches `sha256sum outputs/regression_latest.json`.
5. Read the regression JSON; check coefficient signs against the
   adjacent `insights/NN_*.md` claim, check magnitudes, read N.
6. Print the markdown report. Total cost ≈1.2k tokens.

```
User: /verify deliverables/cordoba-diagnostic-draft.md
```

Skill will:
1. Identify artifact as a paragraph-bearing markdown file. Ask the user
   once: "Verify the whole file or a specific paragraph?" Default to
   the most recent edit if no answer.
2. Pick four checks from menu C: number-to-evidence trace, sign-magnitude
   consistency, source citation, insight cross-check.
3. Grep numeric claims; for each, find the supporting `output/`, `insights/`,
   or `wiki/` page.
4. Print the report.

## Cross-references

- `.claude/conventions/manifest-logging.md` — schema verify reads against.
- `.claude/conventions/insights-logging.md` — paragraph checks may
  cross-reference insight docs.
- `.claude/agents/manifest-checker.md` — subagent for manifest queries.
- `docs/verification-architecture.md` — how /verify fits with the manifest
  hook, the insights Stop hook, and `/deliverable-review`.

## What this skill does NOT do

- Does not run a full deliverable review. That's `/deliverable-review`,
  ≤12k tokens, parallel-lens.
- Does not auto-fire on file writes. User-invoked only.
- Does not re-execute scripts to reproduce outputs. That's a separate
  audit ritual.
- Does not edit artifacts. Read-only by design.
- Does not enforce a fixed checklist. The check menu is a menu — pick
  by artifact and budget.

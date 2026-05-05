# Verification architecture — design rationale

## The problem this solves

Research deliverables fail in different ways at different stakes, and a
single verification mechanism can't catch all of them without becoming
either too noisy (false-positive fatigue) or too lax (silent misses on
high-stakes work). The framework's answer is **stakes-graded
verification**: four layers, each cheap-by-budget at its own scale,
each fired by a different trigger, each with a non-overlapping job.

The four layers, ordered by cost:

| Layer                    | Trigger          | Cost budget | Cadence                              |
|--------------------------|------------------|-------------|--------------------------------------|
| Insights-logging Stop hook | Automatic, end-of-turn | ~100 tok/turn | Every turn that touches `output/0*` |
| Manifest-logging hook    | Automatic, PostToolUse | ≤200 tok/run | Every analytical Bash run            |
| `/verify`                | User-invoked     | ≤2k tokens  | Per-artifact, before publishing      |
| `/deliverable-review`    | User-invoked     | ≤12k tokens | Per advanced draft, before sending   |

The first two are **automatic** and **silent-by-default** (they only
emit output when something is wrong or when something needs to be
recorded). The latter two are **user-invoked** — verification at this
cost is a deliberate act, not an ambient one.

## Why four layers, not one

A single always-fire verification hook would face an impossible tradeoff:
broad enough to catch real defects (and produce noise on every turn),
or narrow enough to be quiet (and miss most real defects). The four
layers each take a different cut at the verification problem:

- **Insights Stop hook** catches *missing distillation*. You ran the
  analysis but didn't write down what you learned.
- **Manifest hook** catches *missing reproducibility metadata*. You
  ran the analysis but didn't record the inputs, env, or git sha.
- **`/verify`** catches *artifact-level defects*. The regression's
  signs flipped, the chart's axis is wrong, the paragraph cites a
  number that doesn't exist.
- **`/deliverable-review`** catches *deliverable-level defects*. The
  draft overclaims, the framing dismisses an alternative, the
  recommendations ignore implementation capacity, the audience is
  wrong.

Each is necessary; none subsumes another. Trying to fold any pair
together compromises both.

## Layer 1: Insights-logging Stop hook (Phase 1)

**Existing — covered in `docs/insights-mechanism.md`.**

A bash Stop hook (`check-insights.sh`) that runs at every turn-end
and silently exits unless: (a) uncommitted analysis artifacts are
present in `output/0*` or `methods/`, AND (b) no new
`insights/NN_*.md` is staged. When both fire, it emits a one-shot
`additionalContext` reminder.

Cost: ~100 tokens per turn (and zero on most turns).

Job: surface the *did you write down what you learned?* prompt at
exactly the moment the discipline applies. Doesn't enforce quality;
nudges existence.

## Layer 2: Manifest-logging hook (Phase 3)

**Covered in `docs/manifest-mechanism.md` and
`.claude/conventions/manifest-logging.md`.**

A bash PostToolUse hook (`log-manifest.sh`) that fires on every
analytical Bash command (`Rscript`, `R`, `python`, `python3`, `stata*`)
and appends one JSON line to `manifest.jsonl` with: timestamp, script
path, language, inputs/outputs, output sha256, seed (if extractable),
env hash, git sha, phase.

Cost: ≤200 tokens per analytical run, silent on success.

Job: record *what ran, with what env, producing what hash*. Does not
verify anything by itself — it builds the ledger that `/verify` reads
against. Without this layer, `/verify`'s reproducibility checks have
nothing to check against.

## Layer 3: `/verify` (Phase 4)

**This phase. See `.claude/skills/verify/SKILL.md`.**

A user-invoked skill that runs three to five domain checks against a
single named artifact (regression result, chart, paragraph). Reads
against `manifest.jsonl` for reproducibility context via the
`manifest-checker` subagent.

Cost: ≤2k tokens per invocation.

The check menus (regression / chart / paragraph) are deliberately
narrow — sign of coefficients, magnitude plausibility, missingness,
source citation, manifest-hash match. The skill picks 3–5 checks per
invocation, biased toward cheap checks, and emits a structured
markdown report.

Why user-invoked, not automatic:
1. The check menu requires judgment about which lens applies (no
   automatic hook can know whether a regression coefficient's sign
   is wrong without the user's prior).
2. Always-fire verification on every artifact would either spam
   the chat (always running) or stay silent in cases that mattered
   (running selectively without context).
3. Running cheaply is the design property — making it user-invoked
   means the cost is paid only when a researcher actually wants the
   check.

The `manifest-checker` subagent is split out so manifest-parsing logic
stays out of the parent context. The parent passes an artifact path,
the subagent returns a compact JSON block with the matching row,
hash check, and script path. The parent decides what to flag.

## Layer 4: `/deliverable-review` (Phase 4)

**This phase. See `.claude/skills/deliverable-review/SKILL.md`.**

A forked parallel review for advanced deliverable drafts. Spawns one
subagent per lens (data validity, identification/reasoning, robustness,
framing, audience-fit, political-economy realism, peer-Lab
plausibility) via the Task tool, in parallel, in the same turn. Each
lens runs in its own context and reports back a fixed-format
findings-and-questions block. The parent skill then synthesizes into
a single consolidated report.

Cost: ≤12k tokens total (≤1.5k per lens × 7 lenses + ≤1.5k synthesizer).

Why forked-parallel, not sequential:

Sequential seven-pass review (one context, seven readings) suffers from
contamination: pass three reads pass two's flags and biases toward
confirming them; pass seven sees so much accumulated context it
struggles to focus. Forked-parallel review trades the cost of seven
fresh contexts for genuine independence — when two lenses agree on a
finding, that agreement carries information; when they disagree,
the disagreement is itself the signal.

Why user-invoked:
1. 12k tokens is too expensive to spend on every save.
2. Many drafts are mid-composition; running parallel review on a
   half-written draft is wasted budget.
3. The deliverable's profile (length target, audience, recommended
   lenses) is the right cue — and the user sets the profile by
   choosing which deliverable template to start from.

Why advanced-drafts-only:
- Forked review is structural and substantive. It catches "this draft
  overclaims" / "this draft has the wrong frame" — issues that only
  exist once a draft has structure to evaluate. On an outline, every
  lens would correctly say "not enough here to evaluate."
- The skill refuses to run on drafts that look incomplete (no
  executive summary, sections marked TBD, numbers marked `[CHECK]`)
  and points the user at `/verify` for partial checks.

## How the four layers compose

Picture a researcher's day:

1. **Mid-analysis** — `Rscript scripts/06c.R` runs. The manifest hook
   silently appends one row to `manifest.jsonl`. No chat output.
2. **End-of-turn** — Claude's reply ends. The insights Stop hook fires;
   sees `output/06c_fdi_at_entry.png` is uncommitted but no
   `insights/0*.md` is staged. Emits a one-shot reminder. Claude writes
   `insights/03_fdi_entry_threshold.md`. Both files committed together.
3. **Before publishing the chart externally** — the researcher types
   `/verify output/06c_fdi_at_entry.png`. The skill picks four
   chart-menu checks (axis sanity, manifest hash, source citation,
   data freshness), spawns `manifest-checker` to confirm the chart
   matches its manifest row, returns a report in ≤2k tokens. One flag:
   the chart's underlying CSV was regenerated yesterday but the chart
   hasn't been re-rendered. Researcher re-runs the chart script.
4. **Before sending the deliverable** — the researcher types
   `/deliverable-review deliverables/cordoba-diagnostic.md`. The
   skill reads the country-diagnostic-memo profile, spawns 7 lenses
   in parallel, synthesizes. Total cost ≈10.8k tokens. Three cross-lens
   agreements, five single-lens findings, one researcher-decision
   point. Researcher addresses the agreements, considers the
   single-lens flags, makes a call on the decision point, then
   sends the deliverable.

Each layer fires when its trigger condition is met. None fires
redundantly. The total cost across a day of analysis is dominated by
the (rare) deliverable-review invocations, with the always-on hooks
contributing tens to low hundreds of tokens each.

## Why these specific budgets

The cost budgets aren't arbitrary; they're sized to the cognitive job:

- **200 tokens** for the manifest hook is "log a structured record
  with no commentary" — anything more means the hook is doing
  judgment work that belongs elsewhere.
- **2k tokens** for `/verify` is "three-to-five focused checks plus a
  structured report" — anything more means the skill is sliding
  toward review territory and should be using `/deliverable-review`.
- **12k tokens** for `/deliverable-review` is "seven independent
  readings plus a synthesizer" — anything less compromises the
  independence (lenses get squeezed and contaminated); anything more
  means the synthesizer is over-elaborating.

If a future skill wants a budget between `/verify` and
`/deliverable-review` (say, 5k tokens), that's a yellow flag — there
probably isn't a real concern at that intermediate scale. Either it's
artifact-level (use `/verify`) or it's deliverable-level (use
`/deliverable-review`).

## What this architecture does NOT do

- **No automatic deliverable review.** Forked-parallel on every save
  would cost ~12k tokens × dozens of saves per day = obvious
  budget collapse. Always user-invoked.
- **No correctness proof.** Verification surfaces flags; researchers
  resolve them. False negatives are possible at every layer.
- **No replacement for human review.** The peer-Lab-plausibility lens
  approximates a senior peer; it doesn't replace one. The political-
  economy-realism lens approximates a senior policy advisor; it
  doesn't replace one. These are first-pass filters.
- **No version control.** Verification reads the current file; it
  doesn't track verification history across versions. If you want
  that, commit the verify report alongside the artifact.
- **No quality enforcement at write time.** Hooks don't block on
  quality; skills don't refuse to run on weak analysis. The framework
  surfaces; the researcher decides.

## Tradeoffs accepted

- **User-invoked is opt-in.** A researcher who never types `/verify`
  gets only the two automatic layers. Trade: predictable cost vs
  opt-in coverage. Accepted because mandatory verification at high
  cost (always-fire `/deliverable-review`) is far worse.
- **The check menus in `/verify` are not exhaustive.** They catch
  the most common failure modes (sign, magnitude, missingness,
  citation, hash). A subtle defect outside the menu won't be caught
  by `/verify` and will need `/deliverable-review` or human review.
- **The seven lenses are policy-research-flavored.** A different
  research domain (e.g., clinical trials) would weight different
  lenses. The framework ships with the policy-research seven; the
  lens set is editable per project.
- **Forked-parallel costs 7×.** Worth it for the independence
  property; not worth it on a mid-composition draft (hence the
  advanced-drafts-only rule).
- **The `manifest-checker` subagent is one extra hop.** Adds latency
  but keeps `/verify`'s parent context inside its 2k budget. Worth
  it for the discipline.

## Extension points

- **New artifact types in `/verify`.** Add a new check menu (D, E, F)
  to `verify/SKILL.md` for, e.g., synthetic-control results, structural
  estimation outputs, or qualitative interview transcripts.
- **New lenses in `/deliverable-review`.** Add an eighth lens (e.g.
  "ethics review" or "data-protection review") for engagements that
  need it. Update the per-deliverable profiles to include or exclude
  the new lens.
- **Project-specific check thresholds.** A project working with very
  short panels might tolerate higher missingness; a project working
  with very small effect sizes might tolerate weaker SEs. Edit the
  thresholds inline in the SKILL.md, or factor them into a separate
  project-config file referenced from the skill.
- **Subagent for `/deliverable-review` data-validity lens.** That
  lens already does manifest checks; it could call `manifest-checker`
  for each numeric claim. Not in v1 — kept the lens self-contained
  for simplicity. The seam is there.

## Provenance

The four-layer structure adapts patterns from three sources:
- **Conditional Stop hook** — the existing `insights-logging` pattern,
  preserved unchanged.
- **PostToolUse manifest hook** — Phase 3's adaptation of
  reproducibility-ledger patterns from data-engineering practice.
- **Forked parallel review** — Pedro Cossio's seven-pass deliverable
  review, refitted to policy-research lenses (substituting
  political-economy-realism and peer-Lab-plausibility for code-shaped
  passes that don't apply to memos).

Adopted in this framework because policy-research deliverables fail
in failure-mode-shaped ways that no single layer can catch, and
budget-graded verification is the way to keep coverage broad without
making cost ruinous.

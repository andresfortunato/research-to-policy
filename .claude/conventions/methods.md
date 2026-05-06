# Methods — Protocol

**Trigger**: Whenever the project commits to an operational rule —
how an entrant cohort is defined, which exclusions apply to a
sample, what threshold gates inclusion in a regression — and the
rule is project-internal (not a published methodology that
already has a citation). Methods docs capture *what we decided to
compute and why*, paired with diagnostic counts that prove the
rule is in force.

This convention defines a folder of methodology specs, one
sub-folder per method, modeled on the v1→v2-evolution pattern
proven out in pilot use. Each method's `rule.md` is the source of
truth for the operational rule its scripts implement.

## Boundary with neighbors

Three folders plausibly host methodology content. Researchers
must draw the boundary explicitly to avoid re-litigating it:

- **`decisions/YYYY-MM-DD_<slug>.md`** is for *peer-reviewable
  methodology calls* — a deflator choice, an identification
  strategy, a sample-restriction rationale you'd defend in
  review. One page each, dated, never edited after the fact.
  See `.claude/conventions/decision-records.md`.
- **`wiki/concepts/<slug>.md`** is for *distilled domain claims
  with citations* — "the Balassa RCA index has a known bias
  toward small economies (Yu et al. 2009)". Public knowledge,
  cited.
- **`methods/<method>/rule.md`** is for *operational
  project-internal rules with diagnostic counts* — "we class a
  country as an electronics entrant in year y if [exact
  conditions], producing 49 narrow entrants under v2." Lives
  with the code that implements it; updated as the rule
  evolves (v1 → v2 → v3).

The cleanest test: would another researcher writing the *same*
diagnostic from scratch arrive at the same rule by reading domain
literature? If yes, it belongs in `wiki/concepts/`. If no — if
it's a project-internal call codified in scripts — it belongs in
`methods/`. If the call is contestable enough that you'd file it
once and defend it under review, it *also* gets a `decisions/`
record cross-linked from the `methods/` doc.

## Where methods docs live

- `methods/` at the project root.
- One **sub-folder per method**: `methods/<method-slug>/`,
  where `<method-slug>` names the method in concrete terms
  (`electronics_entry/`, `manufacturing_employment/`,
  `tradable_classification/`). The slug doubles as the
  directory handle — short, snake_case, decision-bearing.
- Each method's folder contains `rule.md` (required; the
  protocol below) plus any adjuncts: PDFs of the underlying
  codebook, a notebook tying the rule to its diagnostic
  outputs, a CSV of edge-case exclusions kept for transparency.
- **No top-level `methods/INDEX.md`.** The directory listing is
  the index — each method's folder name is its handle. If a
  project grows past ~10 methods, that's a signal to refocus
  the engagement, not to add an INDEX.
- The methods folder is **committed**. The rules are
  researcher-shared.

## Required structure of `rule.md`

Every `methods/<method>/rule.md` carries these seven sections in
order:

```markdown
# <Method name> (vN)

## Source
<Which dataset, which table, which preprocessing already applied.
Concrete enough that someone else can reload it: schema, year
range, key columns. If a column is pre-computed (e.g.
`export_rca` from Atlas), say so.>

## Rule
<The operational rule, in numbered steps. Plain English plus the
exact thresholds, windows, and codes. A reader should be able to
re-implement the rule from this section alone.>

## Why this version
<Context from prior versions: what v1 missed, what v2 fixed, why
the change is load-bearing. Cite specific cases that drove the
change (a country that the old rule incorrectly admitted /
excluded, with the diagnostic count that surfaced it). If this
is v1, the section explains why this rule was chosen over
plausible alternatives.>

## Exclusions
<Lists of codes, countries, sectors, or periods explicitly
dropped. Each exclusion paired with rationale (re-export hub,
micro-jurisdiction, schema break). Transparency CSVs preserved
under `output/` are referenced here.>

## Edge cases
<The cases where the rule's plain-English statement is ambiguous
and a deliberate call was made: NULL values, censored
trajectories, single-observation series. Document the call and
the reasoning.>

## Known limitations
<What the rule does not handle. Pre-period coverage gaps,
right-censoring, schema breaks, deflator simplifications.
Phrased as "accept as known" — not bugs to fix, but caveats for
chart captions and deliverable text.>

## Diagnostic counts
<The numbers that prove the rule is in force. From the script
that implements it (named in the section, e.g.
`build_06_electronics_cohort.py`): N entrants, breakdown by
class, exclusions applied, and any cross-tabs that catch a
regression in the rule. These ARE the headline anchors for
this doc — see `docs/audience-and-philosophy.md` on verifiable
freshness.>
```

All seven sections are required. Missing any of them is a smell —
the rule is not yet operationally codified.

## Versioning

Methods evolve. The convention is in-place editing with a `vN`
in the heading and a `Why this version` section that preserves
the genealogy:

- v1 → v2: edit `rule.md` in place, bump the heading to `(v2)`,
  rewrite `Why this version` to describe what changed and why.
  Git history preserves v1.
- For load-bearing methodology changes (the kind that change
  headline counts by >10%), pair the v2 edit with a
  `decisions/YYYY-MM-DD_<method>-v2.md` decision record. The
  rule.md cross-links to the decision; the decision cross-links
  to the rule. This is the audit trail.
- Diagnostic counts move with the rule. When v2 ships, re-run
  the implementing script and update the counts. A stale count
  ("v2 is the rule but the diagnostic block reports v1
  numbers") is a verification failure and a smell for `/verify`.

## Discipline rules

- **The rule.md is the spec; the script is the implementation.**
  When they disagree, fix one to match the other deliberately.
  Don't let a script's behavior be the de facto rule with the
  doc as a stale shadow.
- **Diagnostic counts are headline anchors.** A rule.md whose
  diagnostic block cannot be regenerated from
  `git log -- methods/<method>/` plus the named script is
  broken. The `analytical-commit-format` convention's `Run:`
  line is how the script and the rule.md stay tied.
- **Cross-link decisions both ways.** If a decision record
  governs the method, the rule.md's `Why this version` cites
  the decision; the decision's body names the method.
- **One sub-folder per method, even small ones.** A two-line
  exclusion rule still gets `methods/<rule>/rule.md` plus its
  exclusion CSV. Resist the urge to consolidate "small"
  methods into a single file — a year later, the consolidation
  is harder to navigate than the directory listing.
- **Don't mirror the wiki.** A method's rule.md is operational,
  not encyclopedic. If you find yourself writing background on
  the broader concept (history of the RCA index, debate over
  product-space vs complexity), that text belongs in
  `wiki/concepts/`. Keep rule.md tight.

## What this convention does NOT cover

- **Statistical methods literature** — citations and definitions
  belong in `wiki/concepts/`, not here.
- **Code documentation** — script docstrings, function comments,
  and the `script-header` convention cover the implementation.
  rule.md describes the *rule*, not the code that implements
  it.
- **One-off filters that don't recur** — a notebook-local subset
  for a single chart doesn't earn a methods folder. The
  threshold for promotion: "we'll re-apply this rule, and
  someone else needs to reproduce it."
- **The decision rationale you'd defend in peer review** —
  that's a `decisions/` record. Methods captures *what to do*
  with operational counts; decisions captures *why* with the
  alternatives-rejected analysis.

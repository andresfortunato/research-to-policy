# Methods — Protocol (v2, absorbs decision-records and learning-capture)

**Trigger**: the project commits to a methodology call, an operational rule, or
discovers a trap in applying one. All three land in the same file.

## What changed in v2 and why

v1 split methodology across three directories **by genre**:

| v1 folder | Genre |
|---|---|
| `decisions/YYYY-MM-DD_<slug>.md` | peer-reviewable choice: *why this and not that* |
| `methods/<slug>/rule.md` | operational rule: *what we compute* |
| `learnings/<slug>.md` | tacit trap: *what will bite you* |

Research does not arrive by genre. It arrives by **topic**, and one topic
routinely needs all three:

> *The FUA is the city unit* → a **rule** (apportion BEA counties into FUA
> polygons by tract-centroid population share), a **justification** (vs CBSA,
> rejected because Argentina has no CBSA analogue), and a **trap** (an FUA is
> not an EPH aglomerado — never pool Gran Córdoba with Río Cuarto).

On the pilot that was three files in three directories held together by
hand-written cross-links, and the boundary failed in practice: 43 files
accumulated in `decisions/` against a spec that called >30 over-recording,
while `methods/` starved at 4; two of the largest "decisions" were plainly
operational rules. Only **7 of 71** learnings used the documented format.

**A boundary that fails 90% of the time is not being violated — it is not
real.** v2 keeps one directory, split by topic.

## Where methods live

- `research/methods/<topic-slug>.md` — one flat file per methodological object.
  Kebab-case, decision-bearing: `city-unit.md`, `price-normalization.md`,
  `iibb-burden.md`.
- `research/methods/_craft.md` — **one** file for cross-cutting numerical and
  reasoning traps with no topic home (`rolling(center=True)` NaNs at the
  endpoint, `np.isclose` breaking a log mean on small shares, two ×2 margins
  summing to ×3 not ×4). Deliberately a single capped file so it cannot grow
  into a second 70-file directory.
- `research/methods/INDEX.md` — one row per topic: slug, one-line rule,
  status, triggers.
- Adjuncts (a codebook PDF, an exclusions CSV) go in
  `research/methods/_adjuncts/<topic>/`.

## Required shape

```markdown
---
slug: city-unit
status: active               # active | superseded-by:<slug> | invalidated
triggers: "fua efua aglomerado metro cbsa apportion tract"
decided: 2026-07-22
revised: 2026-07-29
evidence: [124, 131, 133]    # docs that rest on this rule
---

# <Rule name> (v2)

## Rule
<Numbered, operational, re-implementable from this section alone. Exact
thresholds, windows, codes.>

## Why this and not the alternatives
<Alternatives considered, and the specific empirical reason each was rejected.
Cite a number: "PWT rgdpo inflates oil-exporter productivity ~40% in our
sample" beats "rgdpo is misleading". ← the old decision record.>

## Traps
<Numbered. Each one: the symptom that reveals it, then the fix. These are what
a colleague would warn you about. ← the old learnings.>

## Diagnostic counts
<The numbers that prove the rule is in force, and the script that emits them.
A topic file with no diagnostic counts probably isn't a method — it's either a
claim (→ claims.md) or a trap (→ _craft.md).>

## Scope and limits
<What the rule does not handle. Accept-as-known caveats for chart captions.>

## Changelog
- v2 2026-07-29 — <what changed, why, what number it moved>
- v1 2026-07-22 — initial
```

`## Rule` and `## Changelog` are always required. `## Why this and not the
alternatives` is required for anything a reviewer would question. `## Traps`
and `## Diagnostic counts` are required once they exist — an empty section is
better than a missing one, because it shows the question was asked.

## The tradeoff v2 accepts, stated openly

v1 decision records were **append-only, never edited**, so peer-review
genealogy survived. A living topic file gets edited. The genealogy moves to
`git log -- research/methods/<topic>.md` plus the mandatory `## Changelog`.

This is acceptable because (a) this is applied policy research with a git
history, not a pre-registered trial, and (b) the never-edit rule was already
fiction on the pilot — 12 of 43 records had no `Status` field at all and others
carried statuses (`accepted`, `adopted`) that were not in v1's vocabulary.
Codify what survives contact.

**Where it is not acceptable**: if a number goes into an external publication
and a referee may ask what it was before, snapshot the topic file into the
deliverable's folder at submission time. Don't reintroduce a frozen-record
directory for the general case.

## Retrieval — pull, never push

`triggers:` is a whitespace-separated keyword string: **the words someone would
search for to find this doc**, including acronyms, synonyms and dataset codes the
filename does not carry. It is a *pull* index, read by a session that is looking
for something. **Nothing pushes it into context.**

Grep it before assuming a topic is undocumented, and fall back to a body grep,
which is wider but never misses:

```bash
grep -il '^triggers:.*<keyword>' research/methods/*.md research/sources/*.md
grep -ril '<keyword>' research/methods research/sources
```

**Be generous with keywords.** Under grep an extra keyword costs nothing until
someone searches it, and then it returns one extra filename they discard for
free. A *missing* keyword is the only real failure: it makes the doc hard to
find. Ten or fifteen is fine.

**This reverses the v2 rule, and the reversal is the point.** v2 capped keywords
at 4–8 and banned generic words because a `UserPromptSubmit` hook matched them
against every prompt, so each extra keyword was a false-positive risk paid by a
later session. That hook is gone — v3.1 deleted it on the rule that a hook may
enforce but may not inject.
(Measured in `docs/v3-assessment-cordoba.md`, in the framework repo.)
The reason for the cap went with it. The v2 cap was also never
checked and drifted 63% past itself — mean 12.5 keywords against guidance of
4–8. Under pull that drift stops being a defect, which retires the problem
instead of requiring a check to manage it.

**Why the trigger line still earns its keep once no hook reads it** — measured,
not assumed. Six realistic lookups against 194 method and source docs on the
pilot: filenames alone found 4 of 6; `triggers:` found 5 of 6 with tight result
sets of 2–6 candidates; filename plus triggers found 6 of 6. The two the
filenames missed are the whole argument — `monotributo` is documented in a
`setr_*` file, and `deflator ipc` lives in `price-normalization.md`. That is what
a trigger line carries that a filename cannot: **the mapping between how you
would ask and how the file is named.** A body grep also finds 6 of 6 but returns
up to 22 candidates over a 2.4 MB corpus.

A `triggers:` line is not automation. It is static metadata in the file it
describes: it cannot error, cannot inject, cannot break a run, and stale at worst
means one grep misses and you search again. `lint-research.sh` invariant 7 still
WARNs on a doc that has *no* trigger line — that doc is genuinely hard to find.
Nothing checks how many keywords it has, deliberately.

The v1 two-file-write requirement is gone and stays gone: the trigger lives in
the same file as the content, so a method can no longer be invisible because
someone forgot an index row.

## Sizing

**One file per methodological object. 20–35 files is normal for a multi-theme
6-month engagement.** v1's ">10 methods means refocus the engagement" was off
by 3×: the pilot's 43 decisions plus 63 project learnings consolidate to 28
topic files. If a project passes ~40, check whether topics are being split at
evidence granularity.

## Distinct from neighbours

- **`research/evidence/`** — what the data showed. Methods is how we looked.
- **`research/claims.md`** — the curated narrative claims. A method is never a
  claim.
- **`research/sources/<source>.md`** — how to *access* a source and its
  source-specific gotchas (an expiring token, a silent HTTP 200). A trap
  belongs with the source if it would bite anyone touching that source, and
  with the method if it only bites this analysis.
- **`.claude/conventions/project/`** — style and process (palettes, slide
  furniture, deck periodization). Not methodology.
- **r2p's `docs/field-notes/`** — lessons about *the framework itself*
  (evidence-id collisions across worktrees, parallel fan-out hygiene). Those do
  not belong in a project repo, where no future project can see them.

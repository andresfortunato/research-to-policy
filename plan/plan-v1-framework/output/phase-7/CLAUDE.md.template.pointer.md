# Phase 7 — CLAUDE.md.template pointer block

## Where to splice

Add this section **after the existing `## Decision Records` section** and
**before the closing HTML comment** (`<!-- Add one similar pointer block ...`).

The closing comment currently references `source-registry in Phase 7` as
an upcoming addition; once this block is spliced in, that reference can
be removed (it's now realized) and the comment trimmed to a generic
"add one similar pointer block per additional convention you adopt."

## The block to splice in

```markdown
## Source Registry

Tracked-source watchlist in `sources/registry.yaml` plus dedup ledger
`sources/seen.jsonl`. Use `/scan-sources` to refresh entries due for
re-scrape; `/scan-sources --slug=<slug>` for one source;
`/scan-sources --category=<cat>` to filter; `--force` to bypass the
freq window. Scraped content lands in `raw/sources/<slug>/...md` and
requires explicit `/wiki-ingest` for wiki promotion. Full protocol:
`.claude/conventions/source-registry.md` (read on demand).
```

## Suggested closing-comment rewrite

The current comment reads:

```html
<!--
Add one similar pointer block per additional convention you adopt. The
super-claudio-research framework will install more over time
(source-registry in Phase 7). Each ships with its own pointer template;
copy the relevant block in here and trim to project specifics.
-->
```

Suggested rewrite (drops the now-realized Phase 7 reference):

```html
<!--
Add one similar pointer block per additional convention you adopt. The
super-claudio-research framework will install more over time. Each
convention ships with its own pointer template in
plan/plan-v1-framework/output/phase-N/ during development; copy the
relevant block here and trim to project specifics.
-->
```

## Style notes

- Block is ~7 lines, matching the visual weight of the existing six
  pointer blocks (Insights Logging, Wiki, Manifest Logging, Handoff
  Format, Plan Structure, Decision Records).
- Heading uses **Source Registry** (capitalized title-case) to match
  the others.
- Mentions the three invocation modes inline (one-liner each) so the
  user doesn't have to open the convention file for the common case.
- Closes with the protocol pointer in the standard "Full protocol:
  `.claude/conventions/<name>.md` (read on demand)" form.

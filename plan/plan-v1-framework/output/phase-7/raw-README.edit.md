# Phase 7 — templates/raw/README.md edit

## Summary

Replace the current "Subtree convention" section (lines 36–42), which
forecasts the `raw/sources/<slug>/` subtree as a Phase 7 deliverable,
with a realized version that documents how `/scan-sources` populates
the subtree and how loose `raw/` files relate to it.

## Current text (to replace)

```markdown
## Subtree convention

Loose files at `raw/` root are fine for one-off papers and ad-hoc
acquisitions. Continuous-scrape sources will be organized under
`raw/sources/<slug>/YYYY-MM-DD_<title-slug>.md` once the source-registry
machinery ships (Phase 7 of framework v1). Until then, just use the date
prefix at the root.
```

## Replacement text

```markdown
## Subtree convention

Two layouts coexist under `raw/`:

- **Loose files at the root** — `raw/YYYY-MM-DD_<slug>.<ext>`. Use for
  one-off acquisitions: a paper a colleague forwarded, a dataset
  codebook, an ad-hoc scrape from the `web-scraping` skill, a
  meeting transcript. No registry entry, no recurring fetch.

- **Continuous-scrape subtrees** — `raw/sources/<slug>/YYYY-MM-DD_<title-slug>.md`.
  Use for sources tracked in `sources/registry.yaml` and fetched by
  `/scan-sources`. The skill creates the per-slug directory on first
  fetch; one file per fetched item; YAML frontmatter carries `url`,
  `source_slug`, `category`, `scraped_at`, `content_sha256`, `title`.

The `raw/sources/<slug>/` layout is reserved for `/scan-sources`
output. Don't drop loose files into a slug directory; if a one-off
acquisition relates to a tracked source, put it at the `raw/` root and
note the relationship in the wiki page.

See `.claude/conventions/source-registry.md` for the registry protocol
and `templates/sources/README.md` for how to register a new source.
```

## Where to splice

The replacement is a drop-in for the existing "## Subtree convention"
section. The section's heading stays the same; only the body changes.
Surrounding sections ("## What does NOT count", "## Ingest into the
wiki") are unaffected.

## Why this rewording

- **Removes the "forecast" language.** Phase 7 is now realized; the
  README should reflect current truth, not roadmap.
- **Makes the loose-vs-subtree distinction load-bearing.** Researchers
  will be tempted to drop manual scrapes into `raw/sources/<slug>/`
  for organization; this section says don't — that subtree is
  reserved for `/scan-sources` output, and the dedup ledger only
  knows about files it wrote.
- **Adds the frontmatter-fields list inline.** A reader looking at
  `raw/sources/foo/2026-05-05_bar.md` should see what frontmatter to
  expect without opening the convention file.
- **Cross-references the new convention and template.** Closes the
  loop between the three files (`raw/README.md`,
  `source-registry.md`, `templates/sources/README.md`) the way the
  Wiki section already cross-references `wiki/SCHEMA.md`.

## Verification

After the lead applies this edit:

```bash
grep -A 5 "## Subtree convention" templates/raw/README.md | head -20
#   expected: shows the new "Two layouts coexist" intro, not the old "Phase 7" forecast
```

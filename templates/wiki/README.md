# wiki/

Distilled, queryable project knowledge. Built from `raw/`, owned by Claude.

## Mental model

```
raw/   → immutable source material (papers, scrapes, dataset notes)
wiki/  → distilled pages with claims, citations, cross-links (this dir)
```

A claim in `wiki/` always cites a source page. A source page always cites a
file in `raw/`. The chain back to evidence is unbroken.

## What goes here vs `raw/`

| Goes in `raw/`                          | Goes in `wiki/`                           |
|-----------------------------------------|-------------------------------------------|
| The PDF of a paper                      | A source page summarizing the paper       |
| A scrape of a news article (full HTML→md) | A concept page citing the article         |
| A dataset codebook                      | An entity page about the dataset          |
| A transcript                            | An entity (person) and concept pages it touches |

If you're tempted to write something in `raw/`, you're using it wrong.
If you're tempted to read the full text of a paper from `wiki/`, you're using it wrong.

## Ownership

- **Claude owns `wiki/`.** The `/wiki-ingest` skill is the sanctioned writer.
- **Researchers may correct factual errors.** If a wiki page misstates what a source says, fix the page directly — it's just markdown.
- **Researchers should not restructure.** Renaming pages, splitting concepts, or changing the schema breaks links and confuses the lint. Talk to Claude first (`/wiki-ingest` can refactor on instruction).

## Files

- `SCHEMA.md` — authoritative format spec. Read this first.
- `index.md` — the catalog. Updated by `/wiki-ingest` on every run.
- `log.md` — append-only ingest log.
- `sources/`, `concepts/`, `entities/`, `synthesis/` — page directories (created on first ingest).

## Operations

- `/wiki-ingest <raw/path>` — distill one raw file into wiki pages.
- `/wiki-lint` — audit for orphans, contradictions, stale synthesis, budget violations.

Querying is just reading: open the page, follow the links, drop into chat.

# sources/

The project's curated watchlist of URLs to re-scrape periodically.

## Files

- `registry.yaml` — the watchlist. Human-edited; one entry per URL.
- `seen.jsonl` — append-only dedup log of fetched content hashes.
  Maintained by `/scan-sources`; never edit by hand.

## Mental model

```
sources/registry.yaml    →  what to track (curated list)
/scan-sources             →  fetch what's due, dedup, write
raw/sources/<slug>/...md  →  one file per fetched item (immutable)
sources/seen.jsonl        →  audit log of every successful fetch
```

`/scan-sources` lands content in `raw/sources/`. Promotion to load-bearing
knowledge in `wiki/` requires explicit `/wiki-ingest <raw/sources/<slug>/<file>.md>`.

## How to register a new source

1. Decide the slug. Short, kebab-case, unique within the registry.
   Used as the directory name under `raw/sources/`. Examples:
   `cambodia-mef-news`, `vn-port-throughput`, `kh-exchange-filings`.
2. Pick the category from the closed list:
   `investment | company | innovation | infrastructure | policy | news | other`.
3. Pick the freq from the closed list:
   `daily | weekly | monthly | adhoc`.
   Use `adhoc` for sources you never want auto-scraped — they fire
   only under `--slug` or `--force`.
4. Pick the scrape method by escalation:
   - Try `httpx` first (cheap, fast, works for most static HTML).
   - Move to `playwright` if the page is JS-rendered or behind a login.
   - Move to `crawl4ai` for content-heavy prose pages where you want
     clean markdown.
   - Move to `scrapegraph` (LLM-driven) only when structure is
     irregular and selectors won't hold. Pricey — use sparingly.
5. (Optional) Add a `content_selector` — a CSS selector or XPath that
   narrows the page to its meaningful body. Skipping this means the
   skill will scrape the full page including nav and footer, which
   inflates the content hash and hurts dedup quality.
6. Write a `notes` field. One or two lines: why this source is worth
   tracking, what to watch for, what's known to break.
7. Set `last_scraped: null`. The skill will populate it on first run.

Append the entry to the `sources:` list in `registry.yaml`. Commit
with a message that explains the addition (the rationale belongs in git
log too, not just in `notes`).

## How to retire a source

Don't delete the entry — set `freq: adhoc` and add a `notes` line
explaining when/why you stopped tracking it. This preserves the audit
trail. Old `raw/sources/<slug>/` files stay (raw/ is immutable). If
the source becomes interesting again, flip the freq back.

## How to force a re-fetch

```
/scan-sources --slug=<slug> --force
```

Use this when:
- A registry entry's last fetch failed or returned bad content.
- A breaking event happened and you need fresh content before the freq
  window opens.
- You changed the `content_selector` and want to re-extract from the
  same URL.

`--force` bypasses the freq check but **not** the dedup check. If the
re-fetched content has the same sha256 as the prior fetch, no new file
is written.

## How to query past scrapes

`sources/seen.jsonl` is the dedup ledger of successful fresh content. With
`jq` installed:

```bash
# All distinct content sha256s captured for one source
jq 'select(.slug == "investment-news-cambodia")' sources/seen.jsonl

# All fresh content captured in the last 30 days
jq --arg cutoff "$(date -u -v-30d +%Y-%m-%dT%H:%M:%SZ)" \
   'select(.scraped_at > $cutoff)' sources/seen.jsonl

# Distinct URLs ever seen for a slug (useful when the index URL changes)
jq -r 'select(.slug == "policy-news-example") | .url' sources/seen.jsonl | sort -u
```

For run history (including failures and duplicates), use git instead:

```bash
# When did we last update last_scraped for this entry?
git log -p -- sources/registry.yaml | grep -B1 'investment-news-cambodia'

# Every fresh-content commit
git log -- raw/sources/

# Per-run failures: scan the per-run reports in your shell history,
# or grep recent commits for "scan-sources" mentions.
```

## What this directory is NOT

- **Not a bookmarks file.** Free-form URL lists go in your notes app.
  This file is structured input to a skill.
- **Not a crawl seed list.** One URL per entry. Multi-page indexes
  need multiple entries.
- **Not the wiki.** Scraped content lands in `raw/sources/`. The wiki
  is downstream and curated — `/wiki-ingest` does the promotion.

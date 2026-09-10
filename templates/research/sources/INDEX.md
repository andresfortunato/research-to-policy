# Data sources — index

Documentation for every external data source this project uses.
**Bulk data lives in `data/`; helper functions live in the project's
utility module; this folder holds the *references* — how to access
each source, what's in it, what to watch out for.**

---

## Quick navigation

| If you want… | Read |
|---|---|
| (example — replace) World Bank indicators via the API | `EXAMPLE_world_bank_api.md` |

Sort rows by likely access frequency, not alphabetically. Three to
ten rows is the right size; if it grows past ten, the engagement is
probably touching too many sources. This table is a **curated
shortcut** — the full listing below is the canonical one, and it is
the only place every doc must appear.

---

## Files in this folder

**The canonical listing: one row per source doc, no exceptions.**
Group files by source family (all IMF docs together, then World
Bank, then OECD, etc.). Drop the `EXAMPLE_*.md` row once a real
source is documented.

**Every cell in this file is capped at 120 characters.** The index
answers *which file*, not *what does it say* — if a cell needs more
room, that content belongs in the doc's `## What it gives you`. The
evidence index has held the same cap across 285 rows with zero
violations; this one had no cap and the pilot's grew to 26,000
tokens. `lint-research.sh` invariant 20 WARNs on both halves: an
overlong cell, and a source doc with no row here.

**Never add a section named after an operation** — "folded in from
the old index", "docs that had no row yet". A migration is an event;
an index is a map. Merge those rows into the family group they
belong to and delete the section, or you get the pilot's six
overlapping listings of the same 130 sources.

| File | Purpose |
|---|---|
| `EXAMPLE_world_bank_api.md` | Worked example — delete once real sources land. |

---

## Conventions for adding new sources

When adding a new data source, follow the recipe in
`.claude/conventions/sources.md` (full protocol). The short
form:

1. **Create `research/sources/<source>_<thing>.md`** with frontmatter
   (`source`, `status`, `triggers`, `wrapper`, `env`) and the five
   required sections: `## What it gives you` / `## Access` /
   `## Headline anchor` / `## Gotchas` / `## Coverage limits`. Naming
   is lowercase snake_case; the first token names the source, the rest
   narrows the scope (`imf_sdmx_api.md`, `world_bank_wbgapi.md`).
   `triggers:` is what a future session greps to find this doc — a
   doc without one is hard to find. Be generous: an extra keyword
   costs nothing until someone searches it.
2. **Run the headline-anchor query at least once** and paste the
   returned value into the doc; set `status: verified <today>` in the
   frontmatter.
   A date stamp without a re-fetchable anchor rots silently — see
   "Verifiable freshness anchors" in `docs/audience-and-philosophy.md`,
   in the framework repo (`r2p init` does not install `docs/`).
3. **Add a row to the Quick navigation table** above so future-you
   finds it.
4. **Cross-link from `CLAUDE.md`** only if the source is core
   enough that an agent would waste time without knowing it
   exists. Most sources don't need the cross-link — the INDEX
   carries them all.

Avoid sub-folders within `research/sources/`. Flat is easier to scan,
and the INDEX's grouping does the organizing work.

---

## Helper functions

Required when the project has a utility module (`<project>_utils.py`
or analogous R file). List each wrapper here so the bridge from "API
mechanics" to "wrapper we already wrote" is one table; a researcher
who hits a strange function name in a notebook jumps here, finds
the row, and lands on the reference doc.

Full protocol (env-var pattern, wrapper signatures, docstring
back-links): `.claude/conventions/sources.md`.

| Helper | Source |
|---|---|
| *(none yet — add `wrapper_name(args)` → `research/sources/<file>.md` as wrappers land)* | — |

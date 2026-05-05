# Phase 7 — implementation notes

## Files written (direct, no lead-merge needed)

- `.claude/conventions/source-registry.md` — the protocol. Schema (six
  required fields, two enum sets), dedup logic, freq logic,
  why-not-cron, why-not-bookmarks, discipline rules, hand-off boundary
  to `/wiki-ingest`. ~190 lines.
- `.claude/skills/scan-sources/SKILL.md` — the invokable skill. YAML
  frontmatter with `name`, `description`, `allowed-tools` (Read,
  Write, Edit, Bash, Glob, Grep, Skill — Skill needed to delegate to
  `web-scraping`). Workflow in 8 steps, three invocation modes
  documented, polite-scraping inheritance from `web-scraping` called
  out, manifest-row schema conformance to Phase 3 specified.
- `templates/sources/registry.yaml` — seed registry with `sources: []`
  plus four commented examples covering the four method × freq ×
  category archetypes (investment-news daily/httpx,
  company-filings weekly/playwright,
  infrastructure-tracker monthly/scrapegraph,
  policy-news weekly/crawl4ai). Parses as YAML cleanly.
- `templates/sources/README.md` — how-to-register guide with
  step-by-step (slug → category → freq → method → selector → notes →
  `last_scraped: null`), how-to-retire, how-to-force, how-to-query
  (`jq` recipes mirroring Phase 3's audit ritual). Distinguishes
  `seen.jsonl` (per-success) from `manifest.jsonl` (per-run, including
  failures).
- `docs/source-registry-mechanism.md` — design doc. Why YAML over
  SQLite/CSV/markdown; why JSONL for the dedup log; why hash
  post-extraction body not raw HTML; the four registry-piece
  cross-references; freq logic rationale (4-bucket enum vs
  free-form intervals); dedup asymmetry (failures + duplicates get
  manifest rows but not seen.jsonl rows); tradeoffs, extension
  points, provenance.

## Scratch outputs (for lead to splice into shared files)

- `CLAUDE.md.template.pointer.md` — the "## Source Registry" block to
  splice into `templates/CLAUDE.md.template`, plus a suggested
  rewrite of the trailing closing comment that currently references
  Phase 7 as future work.
- `install.sh.edit.md` — three-part edit: (a) add `sources` to
  section-3 mkdir + mirror_dir, (b) add section 4b for empty-seed
  `sources/seen.jsonl` mirroring section 4's `manifest.jsonl`
  pattern, (c) gitignore confirmation (no change needed — the
  selective `.claude/*` rule doesn't touch siblings; sources/ and
  raw/sources/ are committed by default; cosmetic comment-only
  belt-and-suspenders option provided).
- `raw-README.edit.md` — drop-in replacement for the current
  "## Subtree convention" section that documents the realized
  loose-file-vs-subtree distinction, lists the per-file frontmatter
  fields inline, and cross-references the new convention/template.

## Verification ran (and passed)

1. **YAML parse, registry.yaml**:
   `python3 -c "import yaml; yaml.safe_load(open('templates/sources/registry.yaml').read())"`
   → returns `{'sources': []}` (the four examples are commented out;
   the live YAML is just the empty list). No error.
2. **YAML parse, SKILL.md frontmatter**: extracted between the two
   `---` fences and `yaml.safe_load`-ed. Returns dict with three keys
   (`name: "scan-sources"`, `description: "Read sources/registry.yaml..."`,
   `allowed-tools: "Read, Write, Edit, Bash, Glob, Grep, Skill"`).
3. **Install propagation**: fresh `bash install.sh /tmp/scc-phase7-test`
   lands `.claude/conventions/source-registry.md`,
   `.claude/skills/scan-sources/SKILL.md`,
   `docs/source-registry-mechanism.md` (well, docs is framework-repo
   only, not propagated — confirmed). `sources/` directory NOT
   seeded — expected, since `install.sh` edit is deferred to
   lead-side merge.
4. **No untouched-file modification**: `git status` confirms no edit
   to `templates/CLAUDE.md.template`, `install.sh`, or
   `templates/raw/README.md`. All three sit untouched in working tree.
5. **No /tmp test scratch in framework repo**: `find /Users/anf191/github/super-claudio-research -name '*.test*' -newer /tmp/scc-phase7-test 2>/dev/null` → empty.

## Judgment calls (worth surfacing in handoff Surprises)

- **`adhoc` freq exists but never auto-fires.** The plan listed
  `adhoc` in the freq enum but didn't specify what it does. Decided:
  `adhoc` entries are skipped under the default invocation; only
  fetched under `--slug=<slug>` or `--force`. Reasoning: the freq
  field is binding, so `adhoc` needs a meaning, and "never auto"
  matches the typical use case (paywalled, expensive, or
  intentionally hand-curated sources). Documented in convention,
  README, and skill.
- **`last_scraped` updates even on failure.** The plan didn't
  specify; chose to bump the timestamp on 4xx/5xx/timeout so a flaky
  source doesn't get hammered every invocation. The failure is
  recorded in `manifest.jsonl` (with `outputs: null` and a `notes`
  field) so it's auditable. The trade is: the registry alone won't
  show you which sources are broken; you must check the manifest.
  The skill's report surfaces failures, mitigating this in practice.
- **Dedup asymmetry: failures + duplicates → manifest row, but only
  successes → seen.jsonl row.** The plan was silent on what gets
  appended where. Decided: `manifest.jsonl` records every fetch
  attempt (audit log of what we did); `seen.jsonl` records only
  successful fresh content (dedup ledger of what's been seen).
  Documented in both the convention and the design doc.
- **Skill writes the manifest row directly, not via the Phase 3
  hook.** The hook fires on `Bash` tool invocations; the skill's
  HTTP fetches are not those. So the skill is responsible for
  conforming to the Phase 3 row schema by convention. Added a
  `notes` extension field to the row for duplicate/failure markers
  — Phase 3's design doc explicitly says "downstream consumers
  tolerate unknown fields by default."
- **Install.sh gitignore confirmed correct as-is.** The selective
  `.claude/*` rule applies only inside `.claude/`; `sources/` and
  `raw/sources/` are top-level siblings and fall through to
  "committed by default." No positive `!` rule needed. The edit
  scratch file documents this so the lead doesn't second-guess.

## Nothing to escalate

No scope ambiguity. No constraint violation. No file outside the
direct-write list was touched. All shared-file edits emitted as
scratch in `plan/plan-v1-framework/output/phase-7/` for lead-side
consolidation. Polite-scraping defaults inherited from `web-scraping`
skill (rate limits, robots.txt, User-Agent) — the skill explicitly
defers without re-spec'ing them.

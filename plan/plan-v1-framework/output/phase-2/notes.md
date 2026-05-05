# Phase 2 — integration notes for the lead

## Files written

**Skills (framework-side):**
- `.claude/skills/wiki-ingest/SKILL.md`
- `.claude/skills/wiki-lint/SKILL.md`

**Templates (target-project seeds):**
- `templates/wiki/SCHEMA.md`
- `templates/wiki/README.md`
- `templates/wiki/index.md`
- `templates/wiki/log.md`
- `templates/raw/README.md`

**Docs:**
- `docs/wiki-architecture.md`

**Scratch (this directory):**
- `claude-md-pointer.md` — paste-ready 6-line block for `templates/CLAUDE.md.template`. Style matches existing "## Insights Logging" block.
- `notes.md` — this file.

## Verification ran

1. **Frontmatter parses (PyYAML).** Both SKILL.md files load as dicts via `yaml.safe_load`; `name`, `description`, `allowed-tools` all present and correctly typed. Description lengths 349 and 354 chars — well within Anthropic's recommended ~250–500 range for triggering accuracy.
2. **Fresh install lands files correctly.** `bash install.sh /tmp/test-research-project-phase2` (clean dir) seeded `wiki/{SCHEMA,README,index,log}.md`, `raw/README.md`, `.claude/skills/wiki-{ingest,lint}/SKILL.md`. No `.gitkeep` files propagated. Cleaned up after.
3. **SCHEMA.md cold-ingest test (mental walk-through).** A Claude reading SCHEMA.md cold and handed `raw/2026-04-12_studwell_how-asia-works.md`: knows the page types, naming, frontmatter, body skeletons, and has a worked example using exactly that filename. Should not need clarifying questions.
4. **wiki-lint covers the four required rules:** orphans, contradictions, stale (>90 days `last_condensed`), budget violations (source ≤300, concept ≤800, entity ≤600, synthesis requires `last_condensed`). All four are stated explicitly and each gets a section in the report format.

## Surprises

- **Phases 3 and 5 are landing in parallel.** During my install test I saw `handoff-format.md`, `manifest-logging.md`, and `log-manifest.sh` already present in `.claude/conventions/` and `.claude/hooks/` — Phase 3 and Phase 5 agents have committed alongside me. No file collisions with Phase 2's footprint (skills/wiki/raw/docs are non-overlapping). The lead will need to merge three phases' worth of CLAUDE.md pointer blocks; mine is in `claude-md-pointer.md`.
- **PyYAML not installed by default.** I used `pip3 install --quiet pyyaml` to validate frontmatter strictly. If the lead reruns verification on a fresh machine, either install pyyaml or use the regex fallback I tried first.
- **`templates/CLAUDE.md.template` already references `wiki/` in the directory tree.** Phase 1 added that. So my pointer block is purely additive — the tree section doesn't need changes.

## Decisions I made (worth flagging)

- **Synthesis page creation threshold = ≥3 sources.** Stated in SCHEMA.md and wiki-ingest. The plan said "synthesis page (uncapped + last_condensed required)" but didn't specify when one should exist. ≥3 felt right (avoids premature synthesis, matches "rare" in the page-type table); the lead can revise if too strict.
- **Lint stale threshold = 90 days.** Plan said "stale (synthesis page where `last_condensed` > 90 days ago)" — taken at face value, encoded in wiki-lint SKILL.md.
- **Word counts via `wc -w`.** Cheap and approximate. The skill instructs Claude to count body words (post-frontmatter); markdown punctuation adds a few percent of noise but won't trigger false positives on a 250-word page.
- **No subdirectories enforced under `wiki/`.** Schema *suggests* `wiki/sources/`, `wiki/concepts/`, `wiki/entities/`, `wiki/synthesis/` (and the index/lint examples assume them) but they're created on first ingest, not pre-seeded. Avoids empty directories the user has to look at on day one.

## What didn't work (resolved)

- First frontmatter validation pass failed because PyYAML isn't installed system-wide on macOS Python. Resolved with `pip3 install`.
- Initially considered putting the SCHEMA inline in CLAUDE.md (per Karpathy original). Reverted: the plan and brainstorm specifically locate the schema in `wiki/SCHEMA.md`, and that's where ingest reads it.

## Escalation-worthy surprises

None. Constraints held; no architectural questions surfaced; no invalidated assumptions from earlier phases.

# Log: plan-v1-framework

## 2026-05-05 — plan written
- Brainstorm consumed from `brainstorms/v1-framework-scope.md`
- Resolved 5 open questions during planning (install model, plan dir location, manifest format, wiki location, skill names)
- 7 phases scoped; Phase 1 blocks all; Phases 2/3/5 can parallelize after Phase 1

## 2026-05-05 — added Phase 7 (source registry + /scan-sources)
- New phase: project-level `sources/registry.yaml` + `/scan-sources` skill that delegates fetching to the existing `web-scraping` skill, dedupes via content-hash, lands new items in `raw/sources/<slug>/`, logs to manifest.
- Renumbered docs phase from 7 → 8.
- Phase 7 depends on Phase 2 (raw/wiki layer) + Phase 3 (manifest); parallels with 4/5/6.
- Decision recorded: registry over free-form bookmarks; targeted re-scrape over cron-everything.

## 2026-05-05 — Phase 1 executed
- Five new dirs created with `.gitkeep` markers; install.sh now filters them at copy time so target projects don't inherit stray placeholders.
- `.gitignore` block in install.sh extended to share `.claude/{skills,agents}/` and ignore `plan/ brainstorms/ .scc/` in target projects (plan note: "gitignored in target projects, committed in framework repo").
- `settings.template.json` left structurally unchanged in Phase 1 — Phase 3 will add PostToolUse for `log-manifest.sh`, Phase 5 will add PreCompact for `pre-compact.sh`. Comment field updated to flag this.
- README Roadmap rewritten into v1 / v1.1+ sections matching the 8-phase plan; "What's in here" tree updated.
- CLAUDE.md.template's Codebase Structure tree updated; convention-pointer blocks deferred to per-phase additions.

## 2026-05-05 — Phases 2, 3, 5 executed (three-way parallel)
- Three subagents ran in parallel; each emitted scratch CLAUDE.md.template and settings.json edits to `plan/plan-v1-framework/output/phase-N/`; lead spliced.
- Six pointer blocks now in CLAUDE.md.template (Insights, Wiki, Manifest, Handoff, Plan Structure, Decision Records).
- settings.template.json wired four hook events (Stop, PostToolUse, PreCompact, SessionStart matcher `compact`).

## 2026-05-05 — Phases 4, 6, 7 executed (second three-way parallel)
- Same three-way parallel protocol — landed cleanly with zero merge conflicts. Second confirmation that the file-footprint partition + scratch-emission approach works.
- Phase 4 (`/verify`, `/deliverable-review`, `manifest-checker` agent, `verification-architecture.md`) — pure-additive, no shared-file edits.
- Phase 6 (`/research-cleanup`, three deliverable profiles) — pure-additive, no shared-file edits.
- Phase 7 (source-registry convention, `/scan-sources` skill, `templates/sources/`, design doc) — emitted three scratch edits for `templates/CLAUDE.md.template` (Source Registry pointer block, seven now), `install.sh` (seed `sources/` + empty `sources/seen.jsonl`), and `templates/raw/README.md` (rewrite "Subtree convention" from forecast to realized). Lead applied all three.
- Judgment calls recorded in handoff Surprises: check-menu pattern in `/verify`; per-lens budget in `/deliverable-review`; deliverable length targets; cleanup proposal overwritten not appended; `adhoc` freq never auto-fires; `last_scraped` updates on failure; dedup asymmetry between manifest.jsonl and seen.jsonl.
- Only Phase 8 (docs/README/workshop) remains.

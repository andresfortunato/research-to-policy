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

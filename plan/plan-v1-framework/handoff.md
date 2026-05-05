# Handoff: plan-v1-framework

**Status:** ACTIVE — Phases 1, 2, 3, 5 complete
**Date:** 2026-05-05
**Last commit on plan branch:** `df4e53a` — "Phases 2/3/5: wiki layer, manifest hook, project-discipline conventions"

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Foundation: directory layout, settings, install.sh | ✅ done | b9dc29b |
| 2 | Wiki layer (Karpathy three-layer) | ✅ done | df4e53a — wiki-ingest + wiki-lint skills, SCHEMA.md, page-type budgets enforced |
| 3 | Manifest + reproducibility hook | ✅ done | df4e53a — silent PostToolUse hook (jq dependency), JSONL row schema |
| 4 | `/verify` + `/deliverable-review` skills | next | unblocked (deps 2+3 done) — parallelizable with 6 and 7 |
| 5 | Handoff / plan-structure / decision-records conventions | ✅ done | df4e53a — three conventions + PreCompact and SessionStart hooks |
| 6 | Research-cleanup skill + deliverable profiles | next | unblocked (dep 5 done) — parallelizable with 4 and 7 |
| 7 | Source registry + `/scan-sources` skill | next | unblocked (deps 2+3 done) — parallelizable with 4 and 6 |
| 8 | Documentation, README, workshop materials | blocked | needs all |

## Where we are

This session ran Phases 2, 3, and 5 in parallel via three subagents, then merged the integration files. Each agent wrote to non-overlapping file footprints (skills, conventions, hooks, docs, templates) and emitted CLAUDE.md pointer blocks + settings hook entries to `plan/plan-v1-framework/output/phase-N/` for the lead to splice. That worked cleanly.

After consolidation:

- **`templates/CLAUDE.md.template`** has six pointer blocks (Insights Logging from Phase 1, plus Wiki / Manifest Logging / Handoff Format / Plan Structure / Decision Records added this session). The closing comment that listed deferred conventions was trimmed accordingly.
- **`.claude/settings.template.json`** wires four hook events: Stop (Phase 1, insights), PostToolUse / Bash (Phase 3, manifest), PreCompact (Phase 5, snapshot), SessionStart matcher `compact` (Phase 5, restore). The leading `_comment` was rewritten to summarize all four.
- **Six new conventions / two new skills / four new design docs / three new template files / four new hook scripts** all installed correctly via the unchanged `install.sh` (Phase 1's mirror_dir + chmod logic propagates new files automatically).

Verification was thorough: fresh install lands every file with no `.gitkeep` leakage; `settings.json` parses as JSON with all four hook events; SKILL.md frontmatters parse as YAML; log-manifest.sh appends a valid JSON row on `Rscript scripts/t.R` and is silent on `ls`; pre-compact.sh is silent without an active plan; check-insights.sh (Phase 1) still fires correctly.

## What's next

Three phases now unblocked and parallelizable: **Phase 4** (`/verify` + `/deliverable-review` skills, built via skill-creator), **Phase 6** (research-cleanup skill + three deliverable profiles), **Phase 7** (source registry + `/scan-sources` skill). File footprints are largely disjoint:

- Phase 4: `.claude/skills/{verify,deliverable-review}/`, `.claude/agents/manifest-checker.md`, `docs/verification-architecture.md`
- Phase 6: `.claude/skills/research-cleanup/`, `templates/deliverables/{country-diagnostic-memo,ministerial-briefing,internal-research-memo}/`
- Phase 7: `.claude/conventions/source-registry.md`, `.claude/skills/scan-sources/`, `templates/sources/`, `docs/source-registry-mechanism.md`, plus a `templates/CLAUDE.md.template` pointer block and an `install.sh` edit (seed `sources/` and `sources/seen.jsonl`)

Integration touchpoints to coordinate when running parallel:
- Phase 7 modifies `install.sh` (seed sources/) and `templates/CLAUDE.md.template` (add source-registry pointer). Phases 4 and 6 don't touch these.
- Phase 7 also extends `templates/raw/README.md` to document the `raw/sources/<slug>/` subtree convention. Already noted in the README that this is forecast for Phase 7.

Sequential reading order to start any of 4/6/7:
1. `plan/plan-v1-framework/plan.md` — phase summary
2. This handoff — what's already in place
3. The relevant existing artifacts (e.g. for Phase 4: `.claude/conventions/manifest-logging.md` so `/verify` knows what schema it's reading; for Phase 7: `.claude/skills/wiki-ingest/SKILL.md` since `/scan-sources` lands content for later ingest)

Three-way parallel is feasible again, same protocol as this session: agents emit CLAUDE.md pointer / install.sh edit / settings.json edit suggestions to `plan/plan-v1-framework/output/phase-N/`; lead consolidates.

## Surprises

- **Three-way parallel agent work landed cleanly with zero merge conflicts.** Each agent saw the others' files appearing on disk during their own install-test runs (since they all install into `/tmp/`-based fresh dirs but test against the live framework repo). No agent treated this as a contradiction or surprise; the file-footprint partition held. Worth remembering for Phases 4/6/7: the same pattern is reusable.
- **Phase 3 hook has a hard `jq` dependency.** Documented in convention + design doc. Hook fails silent if `jq` is missing rather than erroring. Fine for now; Phase 8 README polish should mention `jq` in install prerequisites.
- **Phase 5 shipped both `pre-compact.sh` and `post-compact-restore.sh`.** The plan flagged the latter as deferrable, but Claude Code's docs (verified via WebFetch) document `SessionStart` matcher `compact` as the post-compact resume event. So both shipped. The `_comment` in settings.template.json now references both.
- **Phase 5 `post-compact-restore.sh` has a 24-hour staleness check** on the snapshot it surfaces — judgment call by the agent, not in the plan. Avoids injecting last-week's plan state as "current" if you compact and resume days later.
- **Phase 2 agent picked some thresholds that weren't in the plan**: synthesis page creation requires ≥3 sources (encoded in SCHEMA.md and wiki-ingest); `wiki-lint` stale threshold is 90 days from `last_condensed`. Both reasonable; revisit only if they prove wrong in pilot use.
- **A user-driven README.md edit was in progress** when this session started — uncommitted modification + an "init" commit at f4c4a08 the user made earlier today. Left untouched; the user is mid-edit and that's not framework-build work.
- **A scripts/test.R file** was left at the framework repo root by Phase 3's smoke test (the agent created it under the current working dir instead of /tmp). Cleaned up before commit. Worth reminding any future agent to confine smoke-test scratch to /tmp.

## What didn't work

- Initial integration plan considered having parallel agents directly edit `templates/CLAUDE.md.template` and `.claude/settings.template.json`. Discarded in favor of scratch-file emission + lead-side merge. Cleaner; avoided three-way diff conflicts entirely.

## Verification log

- `bash install.sh /tmp/scc-research-integration-test` (fresh) — every Phase 2/3/5 file landed; no `.gitkeep` leakage.
- `python3 -c "import json; json.load(open('.claude/settings.json'))"` — valid; hook events `['PostToolUse', 'PreCompact', 'SessionStart', 'Stop']` all present.
- `head -10 .claude/skills/wiki-{ingest,lint}/SKILL.md | yaml.safe_load` — both frontmatters parse; `name` field correct.
- `grep -E '^## (Insights Logging|Wiki|Manifest Logging|Handoff Format|Plan Structure|Decision Records)$' CLAUDE.md` — all six pointer blocks present in installed target.
- `echo '{"tool_input":{"command":"Rscript scripts/t.R"}}' | bash .claude/hooks/log-manifest.sh` — appends one JSONL row to `manifest.jsonl` with `language:"R"`, `seed:42` (extracted from script), real `env_hash`, real `git_sha`.
- `echo '{"tool_input":{"command":"ls -la"}}' | bash .claude/hooks/log-manifest.sh` — zero rows appended; zero stdout.
- `bash .claude/hooks/pre-compact.sh` with no active plan — silent; no `.scc/snapshots/` created.
- `bash .claude/hooks/check-insights.sh` (Phase 1) — still fires correctly when analysis evidence is staged without insights doc.
- `git log --oneline -3` — `df4e53a` (this session), `f4c4a08` (user's "init" — see Surprises), `f8a99cb` (Phase 1 commit-hash record).

## Hash trail
- Phase 1: b9dc29b
- Phase 2/3/5: df4e53a (this commit)

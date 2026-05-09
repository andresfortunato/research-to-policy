# research-to-policy v1 framework

Completed: 2026-05-05

## What was built

The v1 framework. Eight phases shipped, then two simplification passes (`490f66f` removed pre/post-compact hooks; `bcae991` replaced `manifest.jsonl` + manifest-checker subagent with two zero-cost conventions: `script-header` and `analytical-commit-format`). Final state: seven conventions, six skills, one Stop hook (`check-insights.sh`), zero hard external dependencies, no shipped subagents. Designed for the May 2026 Córdoba/Cambodia kickoff.

## Key decisions

1. **Constitution.** Eight principles in `docs/audience-and-philosophy.md`: silent-by-default, conditional-not-always-fire, composable, project-shared, short CLAUDE.md, markdown-first, stakes-graded verification, open-source-from-day-one. Anything new must conform.
2. **Three audience scopes** served simultaneously (single researcher, two-person team, multi-stakeholder engagement) with the Córdoba and Cambodia pilots as the proving ground.
3. **Verification is stakes-graded.** Routine = silent Stop hook (≤200 tokens); per-artifact = `/verify` user-invoked (≤2k); deliverable last-mile = `/deliverable-review` forked parallel review (≤12k). No always-fire deliverable check.
4. **Wiki layer adopted in full** (Karpathy three-layer): `raw/` immutable, `wiki/` LLM-owned, schema in `wiki/SCHEMA.md`. Three operations (ingest/query/lint), page-type budgets enforced.
5. **`manifest.jsonl` rejected post-ship.** ~80% of audit value already in git; 20% delta (auto-discipline, env_hash without lockfile) didn't pay for the JSONL substrate, `jq` dep, PostToolUse hook, manifest-checker subagent. Replaced with `script-header` (every analytical script's fixed-shape header) + `analytical-commit-format` (`Run:`/`Out:` lines). Together: `git log -- output/<file>` is the audit trail.
6. **Pre/post-compact hooks rejected post-ship.** Snapshot-before-compaction + restore-on-resume worked but didn't pay over cold-resume reading `plan/plan-<name>/handoff.md` directly.
7. **Three deliverable profiles ship in v1**: `country-diagnostic-memo` (4–7k words, technical-peer), `ministerial-briefing` (≤1.2k words / 2pp hard cap, executive), `internal-research-memo` (5–12k words, working-through-a-question). Each: `PROFILE.md` (length target, register, audience, success criteria, lens weights) + `template.md` (skeleton).
8. **Source registry over free-form bookmarks.** `sources/registry.yaml` watchlist + `/scan-sources` skill that delegates fetching to web-scraping skill, dedups by content hash via `sources/seen.jsonl`. Always explicit; never auto-fires on a clock.

## Methods landed

None — v1 shipped seed templates and protocol docs; `methods/` shipped as a convention with an `EXAMPLE_method/rule.md` seed but no project-internal methods landed in this plan.

## Files added or modified

- ✚ `.claude/conventions/` — `insights-logging` (preserved), `script-header`, `analytical-commit-format`, `handoff-format`, `plan-structure`, `decision-records`, `source-registry`.
- ✚ `.claude/hooks/check-insights.sh` (final state: only hook shipped).
- ✚ `.claude/skills/` — `verify`, `deliverable-review`, `wiki-ingest`, `wiki-lint`, `research-cleanup`, `scan-sources`.
- ✚ `templates/` — CLAUDE.md.template (eight pointer blocks), wiki/ (SCHEMA + README + index + log seeds), raw/README.md, sources/registry.yaml + README + seen.jsonl, decision-record.md, handoff.md, deliverables/ (three profiles).
- ✚ `docs/` — eight mechanism docs (insights, handoff, plan-structure, wiki-architecture, verification-architecture, source-registry, audience-and-philosophy, extending).
- ✚ `install.sh` (initial), `README.md` (initial), `.gitignore`.
- ✘ `manifest.jsonl` substrate, `log-manifest.sh` hook, `manifest-checker` agent (removed in `bcae991`).
- ✘ `pre-compact.sh`, `post-compact-restore.sh` hooks (removed in `490f66f`).

## Learnings

- **Pressure-test "what does this add over git?" before shipping infrastructure that mirrors git's properties.** The manifest decision was instructive: 250 lines of bash hook + 200 lines of subagent + a `jq` dependency for value that turned out to be replicable with two zero-cost conventions. The simplification pass cut hard-dependency count to zero and shipped subagent count to zero.
- **Cold-resume from `handoff.md` works.** The compact hooks were designed to handle context loss, but in practice reading the handoff file directly is enough. Hook discipline needs to add real value over the just-read-the-file fallback.
- **Three-way-parallel agent execution worked.** Phases 2/3/5 ran in parallel via three subagents emitting scratch edits to `plan/plan-v1-framework/output/phase-N/`; lead spliced. Phases 4/6/7 ran the same way with zero merge conflicts. The file-footprint partition + scratch-emission protocol is the load-bearing primitive.
- **Script-header convention is opinionated about the field set.** Five fields (Script / Inputs / Outputs / Seed / Env), in that order, every time. Looser ("write whatever") was rejected because grep-discipline only works on a fixed shape and `/verify` parses by anchoring on those exact field names.
- **Verification architecture is three layers, not four.** Provenance substrate (script-header + commit format) sits underneath as conventions, not a verification layer. The hierarchy (insights Stop hook → /verify → /deliverable-review) is cleaner — three user-facing tiers, each with a clear cost ceiling and a clear trigger.

## Metrics
- Phases: 8 + 2 post-ship simplifications
- Sessions: ~6 (estimated from log entries 2026-05-05)
- Final commit: `bcae991`

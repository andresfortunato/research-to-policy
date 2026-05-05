# Handoff: plan-v1-framework

**Status:** ACTIVE — Phases 1, 2, 3, 4, 5, 6, 7 complete; only Phase 8 (docs/README polish + workshop materials) remains
**Date:** 2026-05-05
**Last commit on plan branch:** _to be set after this session's commit_

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Foundation: directory layout, settings, install.sh | ✅ done | b9dc29b |
| 2 | Wiki layer (Karpathy three-layer) | ✅ done | df4e53a |
| 3 | Manifest + reproducibility hook | ✅ done | df4e53a |
| 4 | `/verify` + `/deliverable-review` skills | ✅ done | this session — verify, deliverable-review skills + manifest-checker agent + verification-architecture design doc |
| 5 | Handoff / plan-structure / decision-records conventions | ✅ done | df4e53a |
| 6 | Research-cleanup skill + deliverable profiles | ✅ done | this session — research-cleanup skill + three profiles (country-diagnostic-memo, ministerial-briefing, internal-research-memo) |
| 7 | Source registry + `/scan-sources` skill | ✅ done | this session — source-registry convention, scan-sources skill, sources/ template, design doc; install.sh + CLAUDE.md.template + raw/README.md spliced from scratch edits |
| 8 | Documentation, README, workshop materials | next | unblocked — last phase |

## Where we are

This session ran Phases 4, 6, and 7 in parallel via three subagents — same protocol as the prior session for Phases 2/3/5. Each agent wrote to non-overlapping file footprints. Phases 4 and 6 touched zero shared files (skills auto-discovered from `.claude/skills/`). Phase 7 emitted three scratch-file edits to `plan/plan-v1-framework/output/phase-7/` for the lead to splice into `templates/CLAUDE.md.template`, `install.sh`, and `templates/raw/README.md`. Splice was clean.

After consolidation:

- **`templates/CLAUDE.md.template`** now has seven pointer blocks (added Source Registry after Decision Records). The trailing closing comment was rewritten to drop the now-realized "Phase 7" reference and become a generic guidance note.
- **`install.sh`** now seeds `sources/` (mirror of `templates/sources/`) and creates an empty `sources/seen.jsonl` (the dedup ledger). Section 3 mkdir line and mirror_dir block updated; new section 4b mirrors section 4's `manifest.jsonl` empty-seed pattern. No `.gitignore` rule changes were needed — the selective `.claude/*` rule is sibling-scoped, so `sources/` and `raw/sources/` are committed by default.
- **`templates/raw/README.md`** "## Subtree convention" section rewritten from forecast-language ("Phase 7 will ship…") to realized two-layout doc (loose-files-at-root vs. `raw/sources/<slug>/` reserved for `/scan-sources`). Frontmatter fields listed inline; cross-references to source-registry convention and templates/sources/README.md added.
- **Two new skills (verify, deliverable-review), one new agent (manifest-checker), one new convention (source-registry), three more new skills (research-cleanup, scan-sources), three deliverable profiles, two new design docs (verification-architecture, source-registry-mechanism), four template files (sources/registry.yaml, sources/README.md, six deliverable PROFILE.md/template.md pairs)** all installed correctly via the unchanged `mirror_dir` logic.

Verification was thorough (see Verification log).

## What's next

**Phase 8 only** — docs polish, README update, workshop materials prep. Scope from plan.md:

- Update `README.md` to move shipped items from "Roadmap" to "Conventions installed." Add entries for `/verify`, `/deliverable-review`, `/research-cleanup`, deliverable profiles, `/scan-sources`, source-registry. The Roadmap should now be effectively empty for v1 (everything shipped); flag v1.1+ items.
- Write `docs/audience-and-philosophy.md` capturing the design constitution (silent-by-default hooks, conditional-not-always-fire, composable-not-monolithic, project-shared-not-user-personal, short CLAUDE.md with pointers, markdown-first, language-neutral core, open-source-from-day-one).
- Optionally: `workshop/` (outline-only; full slides built later in PowerPoint by the user).
- Add `jq` to the install prerequisites note in README (Phase 3 hook depends on it; flagged in prior handoff).
- One-line framework-repo `.gitignore` to handle `.DS_Store` (still untracked; not blocking).

Phase 8 is solo — single agent, sequential. Read order:
1. `plan/plan-v1-framework/plan.md` — phase summary
2. This handoff — what's been built
3. Current `README.md` — see how the Roadmap-to-Conventions move should land

## Surprises

- **Three-way parallel landed cleanly again — second confirmation of the pattern.** Phase 4/6/7 agents each saw the others' files appearing on disk during their own install-test runs and treated it as expected (the system prompt warned them). Zero merge conflicts on integration. The scratch-edit protocol (Phase 7 emits suggestions to `plan/plan-v1-framework/output/phase-7/`, lead splices) avoided the only realistic conflict point.
- **Phase 4 `/verify` uses a check-menu pattern, not a fixed checklist.** Three artifact types (regression / chart / paragraph) each have a 5-check menu; the skill picks 3–5 per invocation, biased toward cheap checks. The plan said "at least three checks executed"; the menu adds explicit per-artifact-type discipline so different artifacts don't share the same checks.
- **Phase 4 `/deliverable-review` budgeted explicitly (1.5k × 7 lenses + 1.5k synthesizer = 12k).** The plan capped total at 12k; the agent budgeted per-lens so a runaway lens fails loud (drops itself, notes in report) instead of silently blowing the cap. Lens reports use a fixed-format `## Lens: <name>` block so the synthesizer can parse mechanically.
- **Phase 4 `manifest-checker` returns JSON-shaped markdown** rather than free prose, so `/verify`'s parent context can rely on a stable structure. Small discipline call; plan didn't specify return format.
- **Phase 6 length targets were judgment calls.** Country-diagnostic 4k–7k words / 10–18pp; ministerial-briefing 500–1.2k words / 2pp hard cap (the "back of the car between meetings" use case); internal-research 5k–12k words (deliberately permissive — the purpose is working through a question, not landing a polished conclusion). Worth revisiting if these prove wrong in pilot use.
- **Phase 6 cleanup proposal is overwritten on each invocation, not appended.** Previous proposal is presumed acted-on or discarded. `data/raw/` mtime is computed as a single watermark rather than per-file dependency tracing — simpler and adequate for the proposal use case.
- **Phase 7 `adhoc` freq never auto-fires.** Plan listed `adhoc` in the freq enum but didn't specify behavior. Decided: only fetched under `--slug=<slug>` or `--force`. Matches the typical use case (paywalled, expensive, hand-curated sources). Documented in convention, README, and skill.
- **Phase 7 `last_scraped` updates even on fetch failure.** Prevents hammering broken URLs every invocation. Failure is recorded in `manifest.jsonl` (with `outputs: null` and a `notes` field) so it's auditable — but the registry alone won't show broken sources; researchers must check the manifest or the skill's per-run report.
- **Phase 7 dedup is asymmetric:** `manifest.jsonl` records every fetch attempt (success / duplicate / failure); `sources/seen.jsonl` records only successful fresh content. Plan was silent on the split; the agent picked this and documented it in both convention and design doc.
- **Phase 7 skill writes the manifest row directly, not via the Phase 3 hook.** The hook fires on `Bash` tool invocations; the skill's HTTP fetches are not those. So the skill conforms to the Phase 3 row schema by convention. A `notes` extension field carries duplicate/failure markers — Phase 3's design doc explicitly tolerates unknown fields.
- **Gitignore for `sources/` was a no-op.** Phase 7's agent verified that the existing `.claude/*` selective-include rule doesn't reach siblings: `sources/` and `raw/sources/` fall through to "committed by default," same as `wiki/`, `insights/`, etc. No positive `!` rule needed. Worth knowing; means future top-level scaffolding directories (e.g. `decisions/` if one ships) inherit the same default.

## What didn't work

Nothing this session — the second three-way parallel run confirmed the protocol. No retries, no abandoned approaches.

(Prior session: discarded direct-edit-of-shared-files in favor of scratch-emission + lead-side merge. That decision held up again here.)

## Verification log

- `bash install.sh /tmp/scc-v1-final-test` (fresh) — every Phase 4/6/7 file landed; `sources/{registry.yaml,README.md,seen.jsonl}` created; six deliverable files under `deliverables/{country-diagnostic-memo,ministerial-briefing,internal-research-memo}/`; `.claude/skills/{verify,deliverable-review,research-cleanup,scan-sources}/SKILL.md` and `.claude/agents/manifest-checker.md` all present. No `.gitkeep` leakage.
- `bash install.sh /tmp/scc-v1-final-test` (re-run) — idempotent; reports `~ … (exists, skipping)` for everything; no overwrites.
- `python3 -c "import yaml; ..."` on all four new SKILL.md frontmatters — all parse, all have `name` / `description` / `allowed-tools` keys.
- `python3 -c "import yaml; yaml.safe_load(open('templates/sources/registry.yaml').read())"` — returns `{'sources': []}` (the four examples are commented out as intended).
- `python3 -c "import json; json.load(open('.claude/settings.json'))"` (in installed target) — valid; hook events `['PostToolUse', 'PreCompact', 'SessionStart', 'Stop']` all four still wired (no settings change this session).
- `grep -E '^## (Insights Logging|Wiki|Manifest Logging|Handoff Format|Plan Structure|Decision Records|Source Registry)$' /tmp/scc-v1-final-test/CLAUDE.md` — all SEVEN pointer blocks present.
- `grep -A 3 "## Subtree convention" /tmp/scc-v1-final-test/raw/README.md` — shows the new "Two layouts coexist under `raw/`" intro, not the old Phase 7 forecast.
- `bash .claude/hooks/check-insights.sh` (Phase 1, with staged chart in a fresh `git init` repo) — fires correctly with the expected JSON nudge.
- `echo '{"tool_input":{"command":"Rscript scripts/foo.R"}}' | bash .claude/hooks/log-manifest.sh` (Phase 3) — appends one row to manifest.jsonl.
- `echo '{"tool_input":{"command":"ls -la"}}' | bash .claude/hooks/log-manifest.sh` (Phase 3) — silent; zero rows.

## Hash trail
- Phase 1: b9dc29b
- Phase 2/3/5 work: df4e53a
- Phase 2/3/5 handoff: 43526ec
- README polish: 1a92005
- Prior handoff refresh: b731b59
- Phase 4/6/7 work + this handoff: _to be filled in after commit_

## Known minor items (not blocking next session)
- `.DS_Store` is still untracked in the framework repo; Phase 8 should add a one-line framework-repo `.gitignore` (or use `git update-index --skip-worktree`).
- Phase 8 README polish should:
  - Add `jq` to install prerequisites (Phase 3 dependency, flagged previously).
  - Add Conventions/skills entries for `/verify`, `/deliverable-review`, `/research-cleanup`, deliverable profiles, `/scan-sources`, `source-registry`.
  - Move the entire Roadmap into "Conventions installed" (everything's shipped now); leave only v1.1+ deferrals in the Roadmap.
- The seven-lens names from `/deliverable-review` (data validity, identification/reasoning, robustness, framing, audience-fit, political-economy realism, peer-Lab plausibility) are referenced in the deliverable profile lens-weighting tables. If lens names ever change, the profiles need to update too.
- The Phase 7 scratch-edit files at `plan/plan-v1-framework/output/phase-7/` are committed to the plan branch as audit trail. They can be cleaned up at plan-archive time but don't need to be removed now.

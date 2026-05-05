# Handoff: plan-v1-framework

**Status:** ✅ COMPLETE — all 8 phases shipped, then post-ship simplification (manifest + compact-hook removal). Ready for archival.
**Date:** 2026-05-05
**Last commit on plan branch:** `bcae991` — "Replace manifest.jsonl with script-header + analytical-commit-format conventions"

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Foundation: directory layout, settings, install.sh | ✅ done | b9dc29b |
| 2 | Wiki layer (Karpathy three-layer) | ✅ done | df4e53a |
| 3 | ~~Manifest + reproducibility hook~~ → script-header + analytical-commit-format conventions | ✅ done, then replaced | df4e53a → bcae991 |
| 4 | `/verify` + `/deliverable-review` skills | ✅ done | 1042f9f (verify rewired in bcae991) |
| 5 | Handoff / plan-structure / decision-records conventions | ✅ done | df4e53a |
| 6 | Research-cleanup skill + deliverable profiles | ✅ done | 1042f9f |
| 7 | Source registry + `/scan-sources` skill | ✅ done | 1042f9f (manifest-write removed in bcae991) |
| 8 | Documentation, README, workshop materials | ✅ done | d6eaf4b |
| post | Pre/post-compact hooks removed | ✅ done | 490f66f |
| post | manifest.jsonl replaced with conventions | ✅ done | bcae991 |

## Where we are

The plan finished Phase 8 (`d6eaf4b`), then took two simplification passes during the same session window:

1. **`490f66f` — pre/post-compact hooks removed.** User decision: the conditional snapshot-before-compaction + restore-on-resume discipline didn't pay for the install footprint. Cold-resume from a freshly-rewritten `handoff.md` works without hook involvement.
2. **`bcae991` — manifest.jsonl replaced.** User challenged the manifest's value vs. git: "what does manifest add?" Conceded: ~80% of the manifest's audit value is already in git (timestamps, SHAs, file contents, history). The 20% delta (auto-discipline, env_hash without a lockfile, seedless-run surfacing) didn't pay for the JSONL substrate, the `jq` dependency, the PostToolUse hook, the manifest-checker subagent. Replaced with two zero-cost conventions: `script-header` (every analytical script's fixed-shape header — Script / Inputs / Outputs / Seed / Env) and `analytical-commit-format` (commits that produce analytical artifacts include `Run:` and `Out:` lines). Together they turn `git log -- output/<file>` into the audit trail.

After both simplifications:

- **Hooks:** one. `check-insights.sh` only. Was four (insights + manifest + pre-compact + post-compact-restore).
- **Hook events wired:** one. `Stop` only. Was four.
- **Hard external dependencies:** zero. Was one (`jq`).
- **Subagents shipped:** zero. Was one (`manifest-checker`).
- **`.claude/agents/` directory:** absent (no shipped subagents). Was present.
- **Conventions:** seven. insights / script-header / analytical-commit-format / handoff-format / plan-structure / decision-records / source-registry.
- **CLAUDE.md.template pointer blocks:** eight (added Script Headers + Analytical Commit Format; dropped Manifest Logging).
- **Skills:** unchanged at six. /verify rewired internally to use git+header instead of manifest+subagent.

## What's next

**Nothing for this plan.** v1 is shipped and simplified. After this handoff is committed:
1. User confirms plan completion.
2. `touch plan/plan-v1-framework/.completed` triggers the archivist + cleanup subagents.
3. Archivist synthesizes `archive/plan-v1-framework.md`; cleanup scans the file manifest for dead code.

Future framework work (post-archive):
- Pilot use surfaces what to revisit. Likely candidates: deliverable-profile length targets, `/scan-sources` rate-limit defaults, lens-weighting tables.
- v1.1 conventions (`evidence-ledger`, `chart-registry`, `citation-discipline`) when a real engagement surfaces the need.
- LaTeX/Beamer add-on borrowed from Pedro/Hugo Sant'Anna when register shifts academic.
- **Optional `check-script-headers.sh` Stop hook** — backstops the script-header discipline by nudging if a freshly-staged `scripts/*.{R,py,do}` lacks the header. Documented as a v1.1 seam in `docs/verification-architecture.md`. Add only if pilot use shows the discipline is forgotten frequently.

## Surprises (across the full session arc, not just Phase 8)

- **The manifest's value proposition didn't survive direct comparison with git.** When asked "what does manifest add to git?" the honest answer was: ~80% of the value is already in git (timestamps, SHAs, file contents). The 20% delta (auto-discipline, env_hash without a lockfile) was real but didn't justify the install footprint. The decision to drop it was the right one — the framework is now simpler, has zero hard dependencies, and the audit trail still works (via the two replacement conventions).
- **The compact hooks were a similar story.** PreCompact + SessionStart-on-compact handed off the active plan's handoff snapshot across context loss. In practice, cold-resume reading `plan/plan-<name>/handoff.md` directly works fine — the hook discipline didn't add enough value over the just-read-the-file fallback.
- **Script-header convention is opinionated about the field set.** Five fields (Script / Inputs / Outputs / Seed / Env), in that order, every time. Considered: looser ("just write whatever you want about the script"). Decided against because grep-discipline (`grep -E '^# (Script|Inputs|Outputs|Seed|Env):'`) only works with a fixed shape, and `/verify` parses the header by anchoring on those exact fields.
- **/scan-sources lost a feature it didn't need.** Was writing a manifest row per fetched entry. After removal, the audit trail is git history of `sources/registry.yaml` (last_scraped bumps) plus the per-file frontmatter on `raw/sources/*.md` files. Same information, no separate log.
- **Eight pointer blocks in CLAUDE.md.template.** Was seven after Phase 7. Replacing the Manifest Logging block with two new blocks (Script Headers + Analytical Commit Format) bumped to eight. Still well within the "short CLAUDE.md" principle — each block is ~5 lines, total CLAUDE.md is ~120 lines.
- **The verification architecture is now 3 layers, not 4.** Provenance substrate (script-header + commit format) sits underneath as conventions, not a verification layer. The hierarchy (insights Stop hook → /verify → /deliverable-review) is cleaner — three user-facing tiers, each with a clear cost ceiling and a clear trigger.

## What didn't work

- **Initial Phase 4–7 install of manifest-checker subagent + manifest.jsonl integration.** Worked technically but added 250 lines of bash hook + 200 lines of subagent + a `jq` dependency for value that turned out to be replicable with git + two conventions. Removed in `bcae991`. Lesson: pressure-test "what does this add over git?" before shipping infrastructure that mirrors git's properties.
- **Initial Phase 5 install of pre/post-compact hooks.** Snapshotted the active plan's handoff before compaction; restored on resume. Worked but didn't add enough over just reading `plan/plan-<name>/handoff.md` cold. Removed in `490f66f`.

(Prior session: discarded direct-edit-of-shared-files in favor of scratch-emission + lead-side merge during the three-way parallel runs. That decision held up.)

## Verification log (post-bcae991)

- `bash install.sh /tmp/scc-v1-postmanifest` (fresh) — landed only `check-insights.sh` in `.claude/hooks/`; conventions dir has seven entries (added script-header + analytical-commit-format, removed manifest-logging); no `.claude/agents/` directory; no `manifest.jsonl` in target. Settings.json hook events: `['Stop']`.
- `bash install.sh /tmp/scc-v1-postmanifest` (re-run) — idempotent.
- `grep -E '^## (Insights Logging|Wiki|Script Headers|Analytical Commit Format|Handoff Format|Plan Structure|Decision Records|Source Registry)$' /tmp/scc-v1-postmanifest/CLAUDE.md` — all eight pointer blocks present.
- `grep -rln 'manifest-logging\|manifest-checker\|log-manifest\|manifest\.jsonl'` across shipped framework — only intentional historical references remain (in script-header.md, audience-and-philosophy.md, verification-architecture.md, all explaining the replacement).
- Framework `.gitignore` still contains the single `.DS_Store` line.

## Hash trail
- Phase 1: b9dc29b
- Phase 2/3/5 work: df4e53a
- Phase 2/3/5 handoff: 43526ec
- README polish (interim): 1a92005
- Prior handoff refresh: b731b59
- Phase 4/6/7 work: 1042f9f
- Phase 4/6/7 handoff refresh: a518d2b
- Handoff hash trail fill-in: c912903
- Phase 8 work: d6eaf4b
- Phase 8 hash fill-in: 61362a9
- Pre/post-compact hooks removed: 490f66f
- **manifest.jsonl replaced by conventions: bcae991**
- This handoff refresh: f26ff27

## Known minor items
- The seven-lens names from `/deliverable-review` are referenced in the deliverable profile lens-weighting tables. If lens names ever change, the profiles need to update too.
- Phase 7 scratch-edit files at `plan/plan-v1-framework/output/phase-7/` are committed as audit trail. Phases 2/3/5 also have scratch dirs. The archivist subagent should clean these up at archive time.
- Pilot use will surface whether the script-header discipline holds without a backstop hook. If headers go missing, ship the optional `check-script-headers.sh` Stop hook (seam documented in `docs/verification-architecture.md`).

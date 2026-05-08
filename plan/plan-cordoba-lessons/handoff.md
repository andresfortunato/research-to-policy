# Handoff: plan-cordoba-lessons

**Status:** ACTIVE — Phase 4 complete; Phase 5 next.
**Date:** 2026-05-08
**Last commit on plan branch:** `d8d27fb` — "Phase 4: learning-capture skill + 2 hooks (research-adapted from scc)" (plan baseline at `aae136e`).

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Six small wins (script-header tweaks, web-scraping bundle, addendum pattern) | ✅ done | `4c80c65`. Mechanical, isolated. |
| 2 | Theme-parallel opt-in (insights-logging + check-insights.sh + INDEX schema) | ✅ done | `c296083`. Schema change; verification log in earlier handoff. |
| 3 | Brainstorming skill (port from scc, research-adapted) | ✅ done | `c9d6bee`. Eight files; verification log in prior handoff. |
| 4 | Learning-capture skill + retrieve-learnings.sh + precompact-handoff.sh | ✅ done | `d8d27fb`. Twelve files; verification log below. |
| 5 | Plan archival (Stop hook extension + archivist agent + archive/) | ⏭ next | Existing four .completed markers archived manually first. Archivist scope kept narrow — defers project-wide cleanup to `/research-cleanup`. |
| 6 | README rewrite for researcher audience | ⏭ queued | Quickstart → workflow → scaffolding → tools → what's in here → updates → design philosophy (last). Ships after all components exist. |

## Where we are

Phase 4 landed in one commit. The third bucket — `learnings/` — is now
real: skill, convention, two hooks (UserPromptSubmit + PreCompact),
templates seeds, mechanism doc, install-project + upgrade wiring,
CLAUDE.md.template pointer block, and README tactical edits. The
skill is globally symlinked at `~/.claude/skills/learning-capture/`
during `scr init`.

`retrieve-learnings.sh` is the load-bearing piece: ~80 lines bash that
reads `learnings/index.yaml`, tokenizes the user's prompt, counts
trigger-keyword overlap, and surfaces up to three matched learnings
as `additionalContext` when at least one entry has ≥2 trigger hits.
Silent otherwise — verified across four positive/negative/threshold/
multi-match cases. Uses jq (the v1 framework's runtime ceiling) for
stdin/stdout JSON; silent if jq is missing.

`precompact-handoff.sh` is informational-only: when any `plan/plan-*/`
exists, it emits a two-line reminder (refresh handoff, capture
learnings); silent when no active plan. Verified silent + active
cases.

A pre-existing gap surfaced and got fixed inside this phase:
`scr init --upgrade` previously didn't walk `.claude/hooks/` or pick
up `.claude/settings.template.json`, so any hook-shaped change from
Phase 2 onward wouldn't propagate to existing v1 projects. Extending
upgrade.js to walk `.claude/hooks/` + sidecar settings.template.json
was the smallest fix that satisfied Phase 4's verification gate ("new
files land cleanly; existing settings.template.json sidecars on
divergence") and retroactively closed the Phase 2 gap.

Phase 5 is plan archival: extend `check-insights.sh` to detect
`.completed` markers and nudge archival; new `archivist` agent
(research-adapted port from scc); new `archive/` directory; explicit
boundary doc with `/research-cleanup` (archivist = automated,
plan-scoped; `/research-cleanup` = user-invoked, project-scoped).
The four pre-existing `.completed` markers in `plan/` (plan-install-
redesign, plan-project-conventions, plan-refdocs-conventions,
plan-v1-framework) need to be archived manually first, before the
new Stop-hook extension fires on legacy markers.

## What's next

1. **Phase 5 kickoff** — `phases/phase-5.md`. Touches:
   - `.claude/agents/archivist.md` (new — research-adapted port of scc archivist)
   - `.claude/conventions/plan-structure.md` (extend: document `.completed` → archival flow)
   - `.claude/hooks/check-insights.sh` (extend: add `.completed` detection + archival nudge alongside existing insights-tripwire)
   - `.claude/skills/research-cleanup/SKILL.md` (extend: add "Boundary with archivist agent" paragraph)
   - `templates/archive/{README.md, index.md}` (new — empty seeds; index header + placeholder list)
   - `docs/plan-archival-mechanism.md` (new — `.completed` marker rationale, archive vs delete, boundary with /research-cleanup)
   - `templates/CLAUDE.md.template` (pointer block + tree gloss for `archive/`)
   - `src/lib/install-project.js` (seed `templates/archive/`)
   - `src/lib/install-globals.js` (symlink the new agent)
   - `README.md` (Conventions + Skills + Hooks + Agents tactical edits)
2. **Pre-Phase 5 housekeeping (do BEFORE Phase 5 lands the Stop-hook
   extension):** archive the four pre-existing `.completed` markers
   manually (plan-install-redesign, plan-project-conventions,
   plan-refdocs-conventions, plan-v1-framework). Either move them
   to `archive/` with a hand-written summary, or delete the markers
   if the plans themselves were already cleaned up. Otherwise the
   new Stop hook will fire on legacy markers as soon as Phase 5
   ships, producing a confusing first-contact experience.

## Phase 4 verification log

| Gate | Result | Evidence |
|---|---|---|
| `retrieve-learnings.sh`: matching prompt fires | ✓ | Scratch fixture with `learnings/index.yaml` containing PONDII entry; prompt "Why does PONDII fail in EPH 2014 wave for our panel?" matches 4 trigger words → emits Relevant Learnings JSON. |
| `retrieve-learnings.sh`: irrelevant prompt silent | ✓ | Prompt "What time is it right now?" with same fixture → exit 0, no stdout. |
| `retrieve-learnings.sh`: 1-keyword prompt silent (below threshold) | ✓ | Prompt "Tell me about PONDII please." matches 1 trigger; threshold is 2 → silent. |
| `retrieve-learnings.sh`: multi-match prompt surfaces both learnings | ✓ | Prompt mixing PONDII+EPH+2014 with PWT+rgdpe+oil triggers both entries; both files emitted in additionalContext separated by `\n\n---\n\n`. |
| `retrieve-learnings.sh`: missing index silent | ✓ | Empty scratch dir with no `learnings/index.yaml` → exit 0, no stdout. |
| `retrieve-learnings.sh`: empty `learnings: []` index silent | ✓ | Scratch dir with `learnings: []` only → exit 0, no stdout. |
| `precompact-handoff.sh`: no plan silent | ✓ | Empty scratch dir with no `plan/` → exit 0, no stdout. |
| `precompact-handoff.sh`: active plan(s) fires with two reminders + active list | ✓ | Scratch dir with `plan/plan-foo/` and `plan/plan-bar/` → emits PreCompact JSON additionalContext naming both slugs. |
| `learning-capture` SKILL: two-file atomicity documented | ✓ | SKILL.md "How it works" steps 4–5 enforce `learnings/<slug>.md` + `learnings/index.yaml` row written together; convention "Atomicity" section restates. |
| `learning-capture.md` convention length within band | ✓ | 153 lines — within the 80–150 band (slight overrun acceptable; covers retrieval contract + boundary section). |
| `scr init` lands all three hooks executable | ✓ | Scratch dir post-init: `check-insights.sh`, `precompact-handoff.sh`, `retrieve-learnings.sh` all `-rwxr-xr-x`. |
| `scr init` wires UserPromptSubmit + PreCompact in settings.json | ✓ | Generated `.claude/settings.json` contains both new hook entries alongside existing Stop. |
| `scr init` seeds `learnings/` with README + index.yaml | ✓ | Both files copied via `mirrorDir(templates/learnings/, ...)`. |
| `learnings/` is committed (not gitignored) | ✓ | `grep learnings .gitignore` returns nothing in the post-init scratch dir. |
| Global skill symlink | ✓ | `~/.claude/skills/learning-capture` → `~/github/super-claudio-research/.claude/skills/learning-capture`. |
| `scr init --upgrade`: divergent settings.template.json sidecars | ✓ | Pre-staged scratch with old 110-byte settings.template.json → upgrade emits `⚠ .claude/settings.template.json.framework-new`; original untouched. |
| `scr init --upgrade`: divergent check-insights.sh sidecars | ✓ | Pre-staged scratch with old check-insights stub → upgrade emits `⚠ .claude/hooks/check-insights.sh.framework-new`; original untouched. |
| `scr init --upgrade`: new hooks land directly | ✓ | retrieve-learnings.sh + precompact-handoff.sh appear as `+` in upgrade output and end up `-rwxr-xr-x` in `.claude/hooks/`. |
| No project-specific cordoba content shipped | ✓ | Domain examples are PONDII / EPH 2014 / PWT rgdpe-rgdpo / educ-NA-rural-attrition — generic-shaped survey-vintage / deflator-divergence / sample-restriction warnings; mechanism doc references "an applied-research project that ran without scr conventions" abstractly. |

## Surprises

- **`scr init --upgrade` previously didn't propagate hook updates.**
  upgrade.js walked only `.claude/conventions/` and `templates/`,
  missing `.claude/hooks/` entirely. This meant Phase 2's
  check-insights.sh extension wouldn't have reached existing v1
  projects either — a quietly-broken state that nobody hit because
  no v1 project had upgraded yet. Phase 4's verification gate ("new
  files land cleanly; existing settings.template.json sidecars on
  divergence") forced the fix. upgrade.js now walks `.claude/hooks/`
  and treats `.claude/settings.template.json` as a single tracked
  candidate. Hooks land `-rwxr-xr-x`. The retroactive effect: any
  v1 project running `scr init --upgrade` post-Phase-4 picks up
  Phase 2's check-insights.sh extension along with Phase 4's new
  hooks.
- **The two-file atomicity rule shows up in three places.** SKILL.md
  enforces it ("step 4: write the file. step 5: append to index.yaml.
  always do both atomically"); the convention restates it under
  "Atomicity"; the mechanism doc explains *why* a single-file design
  was rejected (would force the hook to open every `.md` on every
  prompt; would tie retrieval to filename heuristics rather than
  researcher-curated triggers). Three separate restatements is
  intentional — the failure mode (silent invisibility of unindexed
  learnings) is too quiet to surface from a single mention.
- **Settings.template.json now ships into projects on upgrade.**
  Pre-Phase-4, `scr init` only copied `settings.template.json` →
  `settings.json` on first install; the template itself never landed
  in projects. Upgrade now copies the template directly to
  `.claude/settings.template.json` so divergent users can diff
  against their runtime `.claude/settings.json`. New behavior; no
  documented impact yet but flagged here in case pilot users see
  unexpected `+ .claude/settings.template.json` on their next
  upgrade.

## What didn't work

- Initially considered using a JSON parser (e.g., python-based) for
  the YAML index in retrieve-learnings.sh. Rejected — the v1
  constitution caps runtime deps at jq, and the index format is
  shallow enough that bash regex matching on `- file:` and
  `triggers: "..."` lines is sufficient. Confirmed by the
  edge-case tests (empty index, missing index, multi-entry index).
- The PreCompact hook's reminder text initially included a list of
  "things you might have learned this session" as a checklist
  (variable broke / deflator vintage / sample restriction). Pulled
  back to a one-line nudge — the SKILL.md description already covers
  what counts as a learning; the hook just needs to ping. Avoids
  noise on routine compactions.

## Implementation hints for Phase 5

- Read `~/github/super-claudio-code/agents/archivist.md` once, then
  write the scr version. Adaptation work: domain examples shifted
  to research artifact types (insights doc, decision record,
  notebook outputs); narrowed scope (per-plan archival, not
  project-wide cleanup); explicit boundary paragraph against
  `/research-cleanup`.
- Extend `check-insights.sh`, don't fork it. The plan calls out
  *extending* the existing hook for `.completed` detection. The
  current hook is a Stop hook with two tripwires (analysis evidence
  + insights doc absence) — adding a third tripwire (`.completed`
  marker → archival nudge) keeps the hook count down and matches
  the constitution's "compose, don't duplicate" principle.
- The new `.claude/agents/` directory will need a global-symlink
  pass in `installGlobals()`. scc's install-globals likely iterates
  agents/ same way it iterates skills/; check the existing pattern
  there before writing scr's agent installer.
- Archive four pre-existing `.completed` markers BEFORE landing the
  Stop-hook extension. They're at `plan/plan-install-redesign/`,
  `plan/plan-project-conventions/`, `plan/plan-refdocs-conventions/`,
  `plan/plan-v1-framework/`. Either move to `archive/` with
  hand-written summaries, or delete the markers if the underlying
  plan dirs were already cleaned. Otherwise the first session post-
  Phase-5 will see four archival nudges fire at once, which would
  make the new behavior look noisy on first contact.
- The boundary doc between archivist agent and `/research-cleanup`
  skill is load-bearing — the constraint section of plan.md called
  out "consistent results, no duplicated cleanup logic". Archivist
  defers project-wide concerns (orphans, intermediates, unreferenced
  charts) to `/research-cleanup`; `/research-cleanup` documents
  that per-plan archival is the archivist's job. Codify this in
  both files' "Distinct from neighboring conventions" sections.

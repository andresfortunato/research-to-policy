# Handoff: <plan-name or project>

**Status:** <ACTIVE — Phase N complete | PAUSED — reason | CLOSED — YYYY-MM-DD>
**Date:** YYYY-MM-DD
**Last commit on plan branch:** `<sha>` — "<commit subject>"

## Phase status

<!-- Drop this whole table if there is no formal plan. -->

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | <title> | ✅ done | <one-line summary of what landed> |
| 2 | <title> | 🔄 in progress | <where mid-flight stopped> |
| 3 | <title> | ⏭ next | <unblocking dependency, if any> |
| 4 | <title> | ⛔ blocked | <what's blocking> |

## Where we are

<2-6 sentences. What concretely landed this session. The current state of the
repo, the plan, and any open branches. A new reader should be able to
`git checkout` and orient in one minute.>

## What's next

<1-3 next moves in order. If parallelizable, say so. Reading order to start:
which files in this plan matter, which to skip. Be specific.>

1. <next move>
2. <next move>

## Surprises

<Things this session uncovered that future-you / a teammate / a 2028-you would
not want to rediscover. Tools that misbehave, constraints that were
load-bearing, assumptions that turned out to be wrong. Empty if genuinely
nothing surprising. Don't pad.>

## What didn't work

<Dead-ends, abandoned approaches. The point is to save the next reader from
re-running the experiment. Empty is fine.>

## Verification log

<One bullet per check actually executed this session. Format:
`- <command or check> — <expected outcome>`. No entry without the command
having been run. This is the evidence backing every ✅ in the table above.>

- <`bash …` or manual check> — <expected outcome and actual outcome>

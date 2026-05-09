# Skill Independence — Why scr Vendors Three scc Skills

## The trigger

After cordoba-lessons Phase 6 rewrote the README for a researcher
audience, a distribution gap surfaced: the workflow narrative names
`/brainstorming` → `/planning` → `/implementation` → archival, but
two of those four skills shipped only with super-claudio-code (scc).
A researcher running `npm install -g super-claudio-research` got a
project that referenced skills they didn't have. The Quickstart
required two installs — scr + scc — to actually work.

## What we did

Vendored three scc skills into scr's `.claude/skills/`:

- `planning/SKILL.md` (+ `references/multi-session.md`)
- `implementation/SKILL.md` (+ `references/escalation-reference.md`)
- `agent-teams/SKILL.md`

Adapted to research-domain language. Verification phrasing swaps
"build / tests / visual confirmation" for "script runs end-to-end /
sign-of-coefficients hold / source citation present / row-count
reconciliation". Examples shift from JSX/auth-flow shapes to
deflator-chain / identification-strategy / methods-rule shapes.
Cross-references replace `tdd` with `/verify`, drop the
`context-monitor` hook for `precompact-handoff.sh`, drop the
`cleanup` subagent (only the archivist runs post-`.completed`).

The skills' bones — intent over implementation, decisions as records,
verify with evidence, escalation triggers, phase-level execution,
handoffs as bridges, `.completed` → archivist lifecycle — are
domain-neutral and unchanged. The adaptation is surgical, not
architectural.

## What we didn't vendor

`tdd` and `cleanup`. Research has no test-driven-development analog;
`/verify` covers per-artifact sanity. Cleanup is the existing
user-invoked `/research-cleanup` plus the archivist's per-plan
sweep — no separate cleanup agent.

## Precedence for users with both frameworks installed

Both scr and scc install their skills as symlinks under
`~/.claude/skills/`. Last-installer-wins: `scr init` after `scc init`
makes scr's skills authoritative; vice versa makes scc's authoritative.
Re-run whichever framework you want active. The two frameworks don't
detect each other; we don't implement defer-and-merge logic — the
symlink filesystem already resolves it.

## When to re-pull from scc upstream

Only when scc evolves a load-bearing structure — the verification
protocol, the escalation framing, the lifecycle protocol. Mechanical
churn (one example renamed, one cross-ref tightened) doesn't warrant
a re-vendor pass. The design conversation behind this decision lives
at `brainstorms/skill-independence.md`; the planning record is at
`plan/plan-skill-independence/plan.md`.

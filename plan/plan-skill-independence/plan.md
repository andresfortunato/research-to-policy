# Plan: skill-independence

Make r2p fully standalone by vendoring `planning`, `implementation`, and `agent-teams` from super-claudio-code, adapting them to applied research. After this plan ships, `npm install -g research-to-policy` + `r2p init` produces a working research project with the full workflow narrative the v1.1 README describes — no scc dependency.

## Goal

Close the distribution gap surfaced after the cordoba-lessons Phase 6 README rewrite: a researcher installing only r2p today gets brainstorming, learning-capture, verify, deliverable-review, etc., but the workflow breaks at `/planning` because that skill ships with scc, not r2p. Vendor the three load-bearing scc skills, adapt them to research-domain language and cross-references, ship `r2p plan init <slug>` for scaffolding parity, and update the README to drop the `(scc, global)` annotations.

## Constraints

- **Preserve scc's design intent.** The skills' bones (intent over implementation, decisions as records, verify with evidence, escalation triggers, phase-level execution, handoffs as bridges, `.completed` → archivist lifecycle) are domain-neutral and load-bearing. Adapt language and cross-references; do **not** re-architect.
- **Skill names unchanged.** `planning`, `implementation`, `agent-teams`. r2p's brainstorming skill triggers "the planning skill" by name — renaming would force chasing references already shipped.
- **Hooks stay pure bash.** This plan is skills + one CLI command. If a vendored skill references scc-side hooks (`context-monitor`), drop the reference rather than porting.
- **No new hidden directories.** scc uses `.scc/status/` and `.scc/learnings/`; r2p stays at project root with `learnings/` (existing) and `handoff.md` (existing).
- **Don't vendor `tdd` or a `cleanup` subagent.** Research has no TDD analog — replace TDD cross-refs with `/verify`. Cleanup is the existing user-invoked `/research-cleanup`; the archivist is the only post-`.completed` agent.
- **Don't break the workflow narrative just shipped.** Phase 6 of cordoba-lessons names `/planning` and `/implementation` in the worked-example quickstart and skills table; vendored versions keep the names.
- **Don't break scc-resident users.** Last-installer-wins for symlinks; document in README so precedence is explicit.
- **Maintain the brainstorm-handoff contract.** `brainstorm-format.md` says the brainstorming skill triggers the planning skill by name; the vendored planning skill must preserve the five-section consume-brainstorm step.
- **Cordoba-lessons archival deferred.** The `.completed` marker was removed at this plan's start; re-touched after Phase 3 commits so cordoba-lessons archives last.

## Decisions Made

Settled in `brainstorms/skill-independence.md`; not to be re-debated.

- Vendor `planning`, `implementation`, `agent-teams`.
- Don't vendor `tdd`; replace cross-refs with `/verify`.
- Don't vendor `cleanup`; the existing archivist + `/research-cleanup` cover the boundary.
- Skill names unchanged.
- Project-identity bash block: `cat .scc/status/project.md` → `cat CLAUDE.md`.
- Add `r2p plan init <slug>` CLI subcommand for parity.
- Teammate output dir: `plan/plan-<slug>/scratch/<task-name>/` (avoid colliding with analytical `output/`).
- Verification language is domain-shaped (sign-of-coefficients, magnitude sanity, source citation, breakpoint alignment).
- Examples are research-shaped (deflator-choice, identification-strategy, methods/<slug>/rule.md, output/06_chart.png, decisions/<date>_<slug>.md).
- Plan Completion drops the cleanup-subagent line; archivist is the only post-`.completed` agent.
- Drop the framework's `context-monitor` hook cross-reference; r2p's `precompact-handoff.sh` is the compaction-nudge analog.
- `.scc/learnings/` → `learnings/`; `.scc/status/plan-[name].md` → drop (handoff.md is source of truth).

## File Manifest

```
research-to-policy/
├── .claude/skills/
│   ├── planning/
│   │   ├── SKILL.md                                ✚ research-adapted port (~155 lines)
│   │   └── references/multi-session.md             ✚ port + light adaptation
│   ├── implementation/
│   │   ├── SKILL.md                                ✚ research-adapted port (~170 lines)
│   │   └── references/escalation-reference.md      ✚ research-adapted port (heavy: triggers rewrite)
│   └── agent-teams/
│       ├── SKILL.md                                ✚ research-adapted port
│       └── references/                             ✚ port any references
├── src/
│   ├── cli.js                                      ✎ wire `r2p plan init <slug>` subcommand
│   └── lib/
│       └── plan-init.js                            ✚ scaffold plan/plan-<slug>/{plan.md, handoff.md, log.md, phases/, context/}
├── docs/
│   └── skill-independence-mechanism.md             ✚ rationale: why vendor + adapt vs require scc co-install
├── README.md                                       ✎ drop (scc, global) annotations from skills table; add precedence note for users with scc installed; Quickstart no longer mentions scc dependency
└── TODO.md                                         ✎ mark skill-independence shipped; bump v1.2 candidates
```

No deletions. No directory moves.

## Repo Context

This is the first cordoba-lessons follow-up after v1.1 ships. cordoba-lessons closed at Phase 6 (README rewrite for researcher audience) with `.completed` set; that marker was removed at the start of this plan and is re-set at the end of Phase 3 so cordoba-lessons archives **after** skill-independence — the archivist will then synthesize a v1.1+ surface in cordoba-lessons' archive entry that includes the now-vendored skills.

Phase 5 of cordoba-lessons established the agent-installation pattern: `installGlobals()` in `src/lib/install-globals.js` already iterates `.claude/agents/*.md` and `.claude/skills/*/`, creating symlinks into `~/.claude/{agents,skills}/`. New skills landing in `.claude/skills/` are automatically symlinked at the next `r2p init` — no installer change needed for the skills themselves. The CLI subcommand (`r2p plan init`) is the only `src/` change.

scc is the upstream for all three vendored skills. Read each scc SKILL.md once at phase start; adaptation is surgical (swap language, drop scc-specific references, preserve structure) — not a redesign.

## Phases

Three phases, sequential. The skills are independent files but Phase 3's README rewrite + CLI wiring depend on Phases 1 and 2 having shipped the skills first.

| Phase | Title | Scope | File |
|---|---|---|---|
| 1 | Vendor + adapt `planning` | SKILL.md + references/multi-session.md | `phases/phase-1.md` |
| 2 | Vendor + adapt `implementation` | SKILL.md + references/escalation-reference.md | `phases/phase-2.md` |
| 3 | Vendor + adapt `agent-teams` + ship `r2p plan init` | SKILL.md + CLI wiring + README + mechanism doc + TODO | `phases/phase-3.md` |

## Phase Order + Dependencies

- **Phase 1** has no upstream dependency. Ships first because planning is the most-cross-referenced skill and adaptation choices made here (language, cross-refs, examples) anchor Phases 2 and 3.
- **Phase 2** depends on Phase 1. Implementation cross-refs the planning skill and reuses adaptation choices (verification language, example shape, cross-ref targets).
- **Phase 3** depends on Phases 1 and 2. agent-teams cross-refs implementation; CLI subcommand is recommended by planning; README updates cite the now-shipped skills; mechanism doc references all three.

Strict order: 1 → 2 → 3. Each phase verifies independently before the next starts.

## Open Items Deferred (to post-skill-independence)

- **Research-domain `tdd`-equivalent skill.** r2p's `/verify` covers per-artifact sanity. A heavier "test-suite-equivalent" workflow (whole-pipeline regression on every change) might warrant a future skill, but it's not load-bearing for v1.2.
- **scc parity at the `/babysit-prs`-equivalent level.** scc has multiple agents and skills r2p doesn't bundle; only `planning`, `implementation`, `agent-teams` are vendored here because they're load-bearing for the workflow narrative the README already promises.
- **Bidirectional skill compatibility.** A user with scc installed who runs `r2p init` will get r2p's symlinks winning. We document the precedence; we do not implement detect-and-defer logic.

## Implementation hint for next session

Read each scc skill in full once at the phase start (each is 150–170 lines; reading is cheap). Adaptations are surgical — language, examples, cross-references, path swaps — not architectural redesigns. The references/ files are the heavier lift, especially `escalation-reference.md` in Phase 2 (the escalation triggers need full research-domain rewrite; the structure of the reference stays).

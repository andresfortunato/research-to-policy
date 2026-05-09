# Phase 4 — Learning-capture + retrieval hook + precompact-handoff hook

Read `plan.md` for the goal, constraints, decisions, file manifest,
and repo context that govern all phases. This file scopes Phase 4.

## Intent

Port scc's `learning-capture` skill, the `UserPromptSubmit` retrieval
hook, and the `PreCompact` handoff hook. Establishes a third bucket
distinct from `insights/` (formal findings) and `decisions/`
(peer-reviewable methodology): tacit gotchas worth remembering across
sessions (PONDII-not-in-2014, asking-vs-transaction-price gap,
housing-share-assumption-uncertainty are the cordoba-shaped examples).

## Files

- `.claude/skills/learning-capture/SKILL.md` (new) — adapted port.
  Two types: gotcha (severity low/medium/high) and insight.
  Frontmatter same as scc. Index file: `learnings/index.yaml` with
  `triggers: "..."` keyword string per entry. Domain examples
  shifted to research (variable-vintage breakage, deflator-base
  drift, sample-restriction-side-effects).
- `.claude/conventions/learning-capture.md` (new) — convention
  doc covering: when to capture (gotchas surfaced during work),
  file format, index format, retrieval mechanic. Boundary with
  `insights/` (formal findings, evidence-based claims) and
  `decisions/` (peer-reviewable methodology choices).
- `.claude/hooks/retrieve-learnings.sh` (new) — bash port of scc
  `user-prompt-submit.js`. Greps `learnings/index.yaml` for
  trigger keywords matching the user prompt; emits matched
  learning content as `additionalContext`. Min 2 trigger matches
  to fire (avoid noise). Cap at 3 learnings injected. Silent if
  `learnings/index.yaml` missing or no match. ~50 lines bash.
- `.claude/hooks/precompact-handoff.sh` (new) — bash port of scc
  `pre-compact.js`. Informational-only; emits two reminders:
  update the active plan's `handoff.md`; consider capturing any
  surprises as learnings. Silent if no `plan/plan-*/` exists.
- `.claude/settings.template.json` — wire `UserPromptSubmit`
  matcher (calls retrieve-learnings.sh) and `PreCompact` matcher
  (calls precompact-handoff.sh).
- `templates/learnings/README.md` (new) — orientation: gotcha
  vs insight, how retrieval works, when to capture.
- `templates/learnings/index.yaml` (new) — empty seed
  (`learnings: []` plus a commented format example).
- `docs/learning-capture-mechanism.md` (new) — rationale: the
  three-bucket model (insights / decisions / learnings); why
  project-wide not theme-aware; why trigger-keyword retrieval
  over LLM matching (sub-millisecond, deterministic, transparent);
  cordoba-shaped examples (PONDII, formality definition,
  asking-vs-transaction).
- `templates/CLAUDE.md.template` — pointer block for
  learning-capture; codebase-tree gloss for `learnings/`.
- `src/lib/install-project.js` — seed `templates/learnings/` on
  init; symlink the new skill; symlink the two new hooks.
- `README.md` — "Conventions installed" entry; "Skills installed"
  entry; "Hooks" sub-entry naming the two new hooks. (Tactical
  edit; full rewrite is Phase 6.)

## Verification

- `retrieve-learnings.sh` test: with `learnings/index.yaml`
  containing one entry with triggers "PONDII EPH 2014 vintage"
  and a user prompt "Why does PONDII fail in EPH 2014 wave?",
  the hook emits the learning content (≥2 trigger words match).
- `retrieve-learnings.sh` test: same setup, prompt "What time is
  it?" — hook stays silent (zero trigger matches, well under
  the threshold).
- `precompact-handoff.sh` test: in a project with
  `plan/plan-active/` directory, fires the two-line reminder.
  In a project with no `plan/`, stays silent.
- `learning-capture` SKILL: writing a new learning produces both
  the `.md` file and the `index.yaml` entry atomically (the
  SKILL prose enforces this; the convention restates it).
- Conventions list at `wc -l` band: ~80–150 lines for
  `learning-capture.md`.
- `r2p init --upgrade`: existing `settings.template.json` lands
  as a `.framework-new` sidecar if user has diverged it (likely);
  new files land cleanly.

## Dependencies

Upstream: Phase 2 (learning-capture conventions document boundary
with theme-aware insights).
Internal parallelism: skill + retrieve-learnings hook +
precompact-handoff hook are independent files; can ship in one
commit or three.
Downstream: Phase 5 (precompact-handoff hook hint at
learning-capture; archivist agent surfaces "Learnings captured"
in archive entries); Phase 6 (README rewrite covers learnings).

## Reference patterns

Upstream skill: `~/github/super-claudio-code/skills/learning-capture/SKILL.md`.
Upstream hooks: `~/github/super-claudio-code/hooks/user-prompt-submit.js`,
`~/github/super-claudio-code/hooks/pre-compact.js`. Read each once;
bash-port the hooks (no JS leakage outside `src/`).

# CLAUDE.md pointer blocks for Phase 5 conventions

Three blocks to splice into `templates/CLAUDE.md.template`, immediately
after the existing `## Insights Logging` block (around line 68) and
before the `<!-- Add one similar pointer block ... -->` comment.

Format mirrors the existing Insights Logging block: title, one
when-to-apply sentence, "Full protocol" pointer, optional hook nudge note.
≤8 lines each.

---

## Handoff Format

End of any working session that touched a `plan/plan-<name>/`: rewrite
that plan's `handoff.md` in place. Multi-time-scale (within-session,
researcher↔researcher, year-later). Full protocol:
`.claude/conventions/handoff-format.md` (read on demand). A PreCompact
hook snapshots the active handoff before context loss; a SessionStart
hook restores it on resume.

---

## Plan Structure

Multi-session work lives at `plan/plan-<slug>/{plan.md, handoff.md, log.md}`.
Verification is domain-shaped (sign-of-coefficients, magnitude sanity,
breakpoint alignment), not code-shaped. Full protocol:
`.claude/conventions/plan-structure.md` (read on demand). Cross-link
methodology calls to `decisions/`.

---

## Decision Records

Methodology calls you'd defend in peer review (deflator choice,
identification strategy, sample restriction): file once at
`decisions/YYYY-MM-DD_<slug>.md`. Format: Decision / Alternatives /
Why-rejected / Key-assumptions / What-would-invalidate. Full protocol:
`.claude/conventions/decision-records.md` (read on demand).

# Implementation Log — install-redesign

<!-- Append-only. Record direction changes, scope shifts, decision pivots — not minor edits. -->

## 2026-05-07 — Plan opened

Brainstorm at `brainstorms/install-redesign.md` consumed. Plan written. Phase 1 ready to start.

Key resolved-during-planning calls (see plan.md "Decisions resolved during planning"): sidecar-based `--upgrade`, append-if-missing hook merging, `scr init --upgrade` over a separate `scr upgrade` command, `TODO.md` at framework root, manual migration via warning rather than an `scr migrate` command.

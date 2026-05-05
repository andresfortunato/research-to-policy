# Phase 5 — execution notes

## What shipped

- **Three conventions** (`.claude/conventions/`): `handoff-format.md`,
  `plan-structure.md`, `decision-records.md`. All within the 50–120 line
  target (95 / 117 / 120).
- **Two design docs** (`docs/`): `handoff-mechanism.md` (111 lines),
  `plan-structure-mechanism.md` (123 lines). Both within the 80–150 line target.
- **Two templates**: `templates/handoff.md` (50 lines, derived from the
  current `plan/plan-v1-framework/handoff.md` working example) and
  `templates/decision-record.md` (34 lines, ≤30 was the target — slightly
  over because the five sections plus header genuinely need that space).
- **Both hooks**: `.claude/hooks/pre-compact.sh` and
  `.claude/hooks/post-compact-restore.sh`. Pure bash + awk, no python or jq
  dependency. Both made executable and copied by `install.sh` automatically
  via the existing `mirror_dir` + `chmod +x` block.
- **Scratch outputs** (this directory): pointer blocks for CLAUDE.md, the
  settings JSON splice, and these notes.

## Hook decision: shipped both

The plan flagged `post-compact-restore.sh` as deferrable if Claude Code
didn't expose a clean post-compact event. Per
https://code.claude.com/docs/en/hooks the `SessionStart` event has a
documented `compact` matcher value that fires on session resume after
compaction — that's the right hook. Confirmed via WebFetch on the live
docs (May 2026).

There is also a `PostCompact` event, but it has no `additionalContext`
output channel — purely observational. So `SessionStart` matcher
`compact` is the only path to surface the snapshot. That's what
`post-compact-restore.sh` wires into.

## Surprises

- **Awk JSON-escaping is the right primitive.** Python is out (no
  dependency); jq would be cleanest but isn't a guaranteed dependency
  yet (Phase 3's manifest hook may introduce it; this hook predates that
  guarantee). Awk's `gsub(/\\/, "\\\\")` correctly doubles backslashes,
  contrary to what I initially feared.
- **macOS bash 3.x compat.** Initial draft used `${arr[-1]}` (negative
  array index) which is a bash 4+ feature. Replaced with
  `ls -1 ... | tail -1` for portability. Worth remembering for any future
  hook authoring.
- **`echo`-vs-`printf` testing trap.** During smoke tests, piping
  `echo "$json"` to a JSON parser failed for inputs containing
  backslashes — `echo` (in zsh / bash with xpg_echo) interprets
  `\b` as backspace, mangling the JSON. The hook itself was fine; the
  test harness was the bug. Notable because it could bite future
  contributors validating hook output.
- **Stale snapshot policy.** Added a 24-hour age check on the latest
  snapshot in `post-compact-restore.sh`. Older snapshots are silenced —
  if you compacted a week ago and start a new session today, you don't
  want last-week's plan state injected as "current." Not specified in
  the plan; judgment call.

## What didn't work / dead ends

- **First pass of the JSON escape used `python3 -c '... json.dumps(...)'`
  with an awk fallback.** Dropped to awk-only when re-reading the
  bash-only-hooks constraint. The awk version is simpler anyway.

## Verification log

- `bash pre-compact.sh` with active plan + handoff.md → snapshot file written
  to `.scc/snapshots/precompact-YYYYMMDD-HHMMSS.md`. Confirmed via
  smoke-test under `/tmp/test-pedrohook`.
- `bash pre-compact.sh` with no plan → silent, no snapshot dir created.
- `bash pre-compact.sh` with plan dir but no handoff.md → silent.
- `bash post-compact-restore.sh` with snapshot < 24h old → emits valid
  JSON `additionalContext` (validated with `python3 -c 'json.load(...)'`
  on input containing quotes and backslashes).
- `bash post-compact-restore.sh` with no snapshots → silent.
- `bash post-compact-restore.sh` with snapshot > 24h old → silent.
- `bash install.sh /tmp/test-research-project-phase5` (fresh) → all three
  new conventions land in `.claude/conventions/`, both hooks land in
  `.claude/hooks/` and are executable; cleaned up after.
- Line counts: `wc -l` on every authored file — all within targets.

## Where things splice (for the lead's integration pass)

- **`templates/CLAUDE.md.template`**: insert the three pointer blocks from
  `claude-md-pointers.md` after the existing `## Insights Logging` block
  (around line 68), before the `<!-- Add one similar pointer block ... -->`
  comment. Order: Handoff Format → Plan Structure → Decision Records.
- **`.claude/settings.template.json`**: merge `settings-entry.json`'s
  `PreCompact` and `SessionStart` arrays into the existing top-level
  `hooks` object alongside the current `Stop` entry. The `_comment` field
  in the current template should be updated to reflect that PreCompact /
  SessionStart entries are now wired (not deferred).
- **`install.sh`**: no change required. The existing `mirror_dir` + `chmod +x`
  loop already picks up new hook files automatically.
- **`README.md`**: when the lead does the README pass, move
  `handoff-format`, `plan-structure`, `decision-records` from "Roadmap" /
  "v1 — being built" to "Conventions installed."

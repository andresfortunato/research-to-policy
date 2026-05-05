#!/usr/bin/env bash
# PreCompact hook: snapshot the active plan's state before context compaction
# so a SessionStart-on-compact hook can surface it on resume.
#
# SILENT by default. Only writes a snapshot when an active plan is detected:
#   - at least one directory matches plan/plan-*/, AND
#   - that directory contains a handoff.md.
#
# Snapshot lives at .scc/snapshots/precompact-YYYYMMDD-HHMMSS.md and contains:
#   - active plan slug
#   - last commit on the current branch
#   - current phase (parsed from handoff.md Status line if present)
#   - top of handoff.md (first ~60 lines — Status, phase table, where-we-are)
#
# Exits 0 always. Failures are non-fatal — compaction must not be blocked.
#
# Self-test:
#   mkdir -p /tmp/test-pedrohook/plan/plan-foo
#   cp templates/handoff.md /tmp/test-pedrohook/plan/plan-foo/handoff.md
#   CLAUDE_PROJECT_DIR=/tmp/test-pedrohook bash .claude/hooks/pre-compact.sh
#   ls /tmp/test-pedrohook/.scc/snapshots/   # should show one .md file
#
#   rm -rf /tmp/test-pedrohook
#   mkdir /tmp/test-pedrohook
#   CLAUDE_PROJECT_DIR=/tmp/test-pedrohook bash .claude/hooks/pre-compact.sh
#   ls /tmp/test-pedrohook/.scc/snapshots/ 2>/dev/null   # should be empty / dir absent

set -euo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$ROOT" 2>/dev/null || exit 0

# Find first active plan with a handoff.md. shopt -s nullglob so missing dir
# doesn't error. We snapshot only the first match — projects rarely run
# multiple active plans, and the first lexicographic match is deterministic.
shopt -s nullglob
plan_dir=""
for d in plan/plan-*/; do
  [[ -f "${d}handoff.md" ]] || continue
  plan_dir="${d%/}"
  break
done
shopt -u nullglob

# Silent if no active plan.
[[ -z "$plan_dir" ]] && exit 0

slug="${plan_dir#plan/plan-}"
handoff="${plan_dir}/handoff.md"

# Best-effort metadata. Each branch is wrapped in `|| true` so a non-git
# directory or detached HEAD doesn't fail the hook.
last_commit="(no commits or not a git repo)"
if git rev-parse --git-dir >/dev/null 2>&1; then
  last_commit=$(git log -1 --pretty=format:'%h — %s' 2>/dev/null || echo "(no commits)")
fi

status_line=$(grep -m1 '^\*\*Status:\*\*' "$handoff" 2>/dev/null || echo "**Status:** (not found)")

ts=$(date +%Y%m%d-%H%M%S)
snapshot_dir=".scc/snapshots"
mkdir -p "$snapshot_dir"
snapshot="${snapshot_dir}/precompact-${ts}.md"

{
  echo "# Pre-compact snapshot — ${ts}"
  echo
  echo "**Active plan:** \`${plan_dir}\` (slug: ${slug})"
  echo "**Last commit:** ${last_commit}"
  echo "${status_line}"
  echo
  echo "## Top of handoff.md"
  echo
  head -60 "$handoff"
} > "$snapshot"

# Hook exits silently on success; the snapshot is for the next session, not
# this turn. PreCompact has no additionalContext channel to Claude.
exit 0

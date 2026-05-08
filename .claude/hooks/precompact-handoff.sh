#!/usr/bin/env bash
# PreCompact hook: nudge the model to refresh handoff and capture learnings
# before context is compacted. Fires on both auto and manual compaction.
# Informational only — cannot block compaction.
#
# SILENT when no active plan exists (no plan/plan-*/ directories).
# When a plan is active, emits two reminders:
#   1. Refresh the active plan's handoff.md (status, decisions, next steps).
#   2. Capture any session surprises as learnings/<slug>.md + index.yaml entry.

set -euo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$ROOT" 2>/dev/null || exit 0

# Silent if no plan directories exist.
shopt -s nullglob
plan_dirs=(plan/plan-*/)
shopt -u nullglob
[[ ${#plan_dirs[@]} -gt 0 ]] || exit 0

# Build a short list of active plan slugs (strip plan/plan- prefix and trailing /).
active_list=""
for d in "${plan_dirs[@]}"; do
  slug="${d#plan/plan-}"
  slug="${slug%/}"
  active_list="${active_list}  - ${slug}"$'\n'
done

read -r -d '' message <<EOF || true
Context is about to be compacted. Before losing detail:

• Refresh the active plan's handoff.md with current status, decisions made, and
  next steps. Active plan(s):
${active_list}
  Format and time-scales: .claude/conventions/handoff-format.md.

• Were there any surprises, gotchas, or hard-won discoveries this session worth
  preserving? If so, write a learning to learnings/<slug>.md and append an
  index.yaml entry — see .claude/conventions/learning-capture.md. The
  retrieval hook will surface it in future sessions when relevant trigger
  keywords appear in a prompt.
EOF

if command -v jq >/dev/null 2>&1; then
  jq -n --arg ctx "$message" '{
    hookSpecificOutput: {
      hookEventName: "PreCompact",
      additionalContext: $ctx
    }
  }'
else
  printf '%s\n' "$message"
fi

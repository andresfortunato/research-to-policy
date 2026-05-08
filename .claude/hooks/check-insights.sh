#!/usr/bin/env bash
# Stop hook: nudge Claude to write insights/NN_*.md when a session produced
# new analysis evidence (charts, panels, methods notes) without a new insights
# doc to record what was learned.
#
# SILENT by default. Only emits a nudge when:
#   1. There ARE uncommitted analysis artifacts (output/[<theme>/]0[0-9]*_*.{png,csv,meta.json}
#      or methods/*.md), AND
#   2. There are NO uncommitted insights/[<theme>/]NN_*.md changes.
#
# Both flat (output/01_*, insights/01_*.md) and theme-parallel
# (output/<theme>/01_*, insights/<theme>/01_*.md) layouts satisfy
# the tripwire. See .claude/conventions/insights-logging.md and
# docs/theme-parallel-mechanism.md.
#
# Soft warn only — hooks return non-blocking additionalContext via stdout JSON.

set -euo pipefail

# CLAUDE_PROJECT_DIR is set by Claude Code; fall back to current dir if missing.
ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$ROOT" 2>/dev/null || exit 0

# Skip if not a git repo (no way to detect "what changed this session").
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

# Look at uncommitted changes (staged + unstaged + untracked) in scope.
status=$(git status --porcelain -u 2>/dev/null || true)
[[ -z "$status" ]] && exit 0

# Tripwires for "analysis happened":
#   - notebook-numbered output artifacts: output/01_, 06c_, 06b_ etc.
#     (also accepts output/<theme>/01_* for theme-parallel layouts)
#   - methods notes (methodology docs)
#   - panel CSVs in output/ matching *_panel.csv or analytical patterns
analysis_hit=$(printf '%s\n' "$status" | grep -E \
  '^([ AM?]+|[?]+) (output/([^/]+/)?0[0-9][a-z]?_.*\.(png|csv|meta\.json)|methods/[^/]+/.*\.md|methods/[^/]+\.md)$' \
  || true)

# If no analysis evidence, exit silently.
[[ -z "$analysis_hit" ]] && exit 0

# If new/modified insights/*.md exists, the user is already capturing — silent.
# Accepts both flat (insights/NN_*.md) and theme-parallel (insights/<theme>/NN_*.md).
insights_hit=$(printf '%s\n' "$status" | grep -E \
  '^([ AM?]+|[?]+) insights/([^/]+/)?[0-9]+_.*\.md$' \
  || true)

[[ -n "$insights_hit" ]] && exit 0

# Conditions met: emit additionalContext nudge.
# Show first ~5 analysis files so Claude can see the evidence.
top_artifacts=$(printf '%s\n' "$analysis_hit" | head -5 | sed 's/^/    /')

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "additionalContext": "Insights checkpoint — uncommitted analysis evidence detected without a corresponding insights doc.\n\nAnalysis artifacts (sample):\n${top_artifacts//$'\n'/\\n}\n\nNo new insights/*.md found in git status. Before stopping:\n  1. Read .claude/conventions/insights-logging.md\n  2. Find the next free NN with: ls insights/ | sort\n  3. Write insights/NN_<slug>.md with 3–8 evidence-based findings\n  4. Append a row to insights/INDEX.md\n  5. Commit the analysis artifacts and the insights doc together\n\nIf this was research/exploration with no real new evidence, you can ignore this nudge and proceed."
  }
}
EOF

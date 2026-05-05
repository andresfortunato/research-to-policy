#!/usr/bin/env bash
# SessionStart hook (matcher: compact): surface the most recent pre-compact
# snapshot as additionalContext when a session resumes after compaction.
#
# SILENT by default. Only emits when:
#   - .scc/snapshots/precompact-*.md exists, AND
#   - the most recent snapshot is younger than 24 hours (older snapshots are
#     stale — the user has likely moved on; surfacing them would mislead).
#
# Wiring (in .claude/settings.json):
#   "SessionStart": [
#     { "matcher": "compact",
#       "hooks": [{ "type": "command",
#                   "command": "bash $CLAUDE_PROJECT_DIR/.claude/hooks/post-compact-restore.sh" }]
#     }
#   ]
#
# This is the partner to pre-compact.sh. The PreCompact hook writes the
# snapshot before context loss; this hook reads it back on resume so Claude
# does not have to reconstruct active-plan state from scratch.
#
# Self-test:
#   mkdir -p /tmp/test-restore/.scc/snapshots
#   echo "# snapshot" > /tmp/test-restore/.scc/snapshots/precompact-20260505-120000.md
#   CLAUDE_PROJECT_DIR=/tmp/test-restore bash .claude/hooks/post-compact-restore.sh
#     # → emits JSON with additionalContext containing the snapshot
#   rm -rf /tmp/test-restore/.scc/snapshots
#   CLAUDE_PROJECT_DIR=/tmp/test-restore bash .claude/hooks/post-compact-restore.sh
#     # → silent

set -euo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$ROOT" 2>/dev/null || exit 0

snapshot_dir=".scc/snapshots"
[[ -d "$snapshot_dir" ]] || exit 0

# Most recent snapshot (lexicographic sort matches chronological because of
# the YYYYMMDD-HHMMSS naming). Use ls + tail for portability across bash 3.x
# (macOS default) which doesn't support negative array indices.
latest=$(ls -1 "$snapshot_dir"/precompact-*.md 2>/dev/null | tail -1)
[[ -z "$latest" ]] && exit 0
[[ -f "$latest" ]] || exit 0

# Stale-check: skip if older than 24 hours. `find -mtime -1` would do it but
# we want portability across BSD/GNU `find`, so use stat differences.
now=$(date +%s)
if mtime=$(stat -f %m "$latest" 2>/dev/null || stat -c %Y "$latest" 2>/dev/null); then
  age=$(( now - mtime ))
  (( age > 86400 )) && exit 0
fi

# Emit snapshot as additionalContext. JSON-escape with awk: backslash, quote,
# tab, then turn each line ending into a literal "\n". Pure bash + awk; no
# python or jq dependency.
escaped=$(awk '
  BEGIN { ORS = "" }
  {
    gsub(/\\/, "\\\\")
    gsub(/"/,  "\\\"")
    gsub(/\t/, "\\t")
    print $0 "\\n"
  }
' "$latest")

cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Pre-compact snapshot restored — resuming after context compaction. The active plan and last-known state from before compaction:\\n\\n${escaped}"
  }
}
EOF

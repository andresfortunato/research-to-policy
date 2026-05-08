#!/usr/bin/env bash
# UserPromptSubmit hook: retrieve relevant learnings from learnings/index.yaml
# by matching trigger keywords against the user's prompt.
#
# SILENT by default. Only emits additionalContext when:
#   1. learnings/index.yaml exists and contains entries, AND
#   2. At least one entry has ≥2 trigger keywords matching prompt words.
#
# Up to 3 learnings are surfaced per prompt (highest match count first).
# See .claude/conventions/learning-capture.md for index format and contract.

set -euo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$ROOT" 2>/dev/null || exit 0

INDEX="learnings/index.yaml"
[[ -f "$INDEX" ]] || exit 0

# Need jq for JSON in/out (it's the framework constitution's runtime ceiling).
command -v jq >/dev/null 2>&1 || exit 0

# Read prompt from stdin JSON.
input=$(cat)
prompt=$(printf '%s' "$input" | jq -r '.prompt // empty' 2>/dev/null || true)
[[ -z "$prompt" ]] && exit 0

# Tokenize prompt: lowercase, split on non-alphanumeric/underscore, dedup.
prompt_words=$(printf '%s' "$prompt" \
  | tr '[:upper:]' '[:lower:]' \
  | tr -cs 'a-z0-9_' '\n' \
  | sort -u)
[[ -z "$prompt_words" ]] && exit 0

# Parse index.yaml into (file, triggers) pairs. Format:
#   learnings:
#     - file: <name>.md
#       triggers: "kw1 kw2 kw3"
matches_file=$(mktemp)
trap 'rm -f "$matches_file"' EXIT

current_file=""
while IFS= read -r line; do
  if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*file:[[:space:]]*(.+)$ ]]; then
    current_file="${BASH_REMATCH[1]}"
    # Strip optional surrounding quotes / trailing whitespace.
    current_file="${current_file%[[:space:]]}"
    current_file="${current_file%\"}"; current_file="${current_file#\"}"
    current_file="${current_file%\'}"; current_file="${current_file#\'}"
  elif [[ "$line" =~ ^[[:space:]]*triggers:[[:space:]]*\"(.+)\"[[:space:]]*$ ]] \
    || [[ "$line" =~ ^[[:space:]]*triggers:[[:space:]]*\'(.+)\'[[:space:]]*$ ]]; then
    triggers="${BASH_REMATCH[1]}"
    if [[ -n "$current_file" ]]; then
      hits=0
      for t in $(printf '%s' "$triggers" | tr '[:upper:]' '[:lower:]'); do
        [[ -z "$t" ]] && continue
        if grep -qFx "$t" <<< "$prompt_words"; then
          hits=$((hits + 1))
        fi
      done
      if [[ $hits -ge 2 ]]; then
        printf '%d\t%s\n' "$hits" "$current_file" >> "$matches_file"
      fi
    fi
    current_file=""
  fi
done < "$INDEX"

[[ -s "$matches_file" ]] || exit 0

# Top 3 by match count desc.
top=$(sort -t$'\t' -k1,1 -nr "$matches_file" | head -3 | cut -f2)

combined=""
sep=""
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  path="learnings/$f"
  [[ -f "$path" ]] || continue
  content=$(<"$path")
  combined="${combined}${sep}${content}"
  sep=$'\n\n---\n\n'
done <<< "$top"

[[ -z "$combined" ]] && exit 0

body=$(printf '## Relevant Learnings\n\n%s' "$combined")

jq -n --arg ctx "$body" '{
  hookSpecificOutput: {
    hookEventName: "UserPromptSubmit",
    additionalContext: $ctx
  }
}'

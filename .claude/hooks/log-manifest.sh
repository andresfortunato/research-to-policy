#!/usr/bin/env bash
# PostToolUse hook: silent reproducibility manifest.
#
# Fires on Bash tool invocations. If the command is an analytical run
# (Rscript, python, stata, ...), appends one JSON line to manifest.jsonl
# at the project root. Otherwise exits silently.
#
# CONTRACT
# --------
# - Silent on every path. No stdout. No JSON nudge. (PostToolUse uses
#   stdout for additionalContext, just like Stop. Emitting nothing
#   == emitting no context, == zero token cost.)
# - Always exits 0. A failure to log must not break the user's session.
# - Reads the PostToolUse event JSON from stdin:
#       {
#         "tool_name": "Bash",
#         "tool_input": {"command": "Rscript scripts/foo.R", ...},
#         "tool_response": {...}
#       }
#   We only need tool_input.command.
# - Hard requires: bash, jq, sha256sum (or shasum -a 256), git (optional),
#   python3 (optional, used only for env_hash if `pip` is present).
#
# DETECTION STRATEGY
# ------------------
# Allowlist on the first word of the command (after stripping leading env
# assignments and `time`/`nice`/`nohup` wrappers). If the first real word
# matches an analytical interpreter, log; else skip. We do NOT try to
# detect `cat foo | python script.py` style pipelines — researchers
# wanting reproducibility should invoke `python script.py` directly.
#
# SELF-TEST
# ---------
# Analytical:    echo '{"tool_input":{"command":"Rscript scripts/foo.R"}}' | bash log-manifest.sh
#                  → one new row in $CLAUDE_PROJECT_DIR/manifest.jsonl
# Non-analytic:  echo '{"tool_input":{"command":"ls -la"}}'              | bash log-manifest.sh
#                  → exits 0, no row appended

set -uo pipefail
# NB: no `-e`. We do not want hook errors to surface as session errors.

# -----------------------------------------------------------------------
# 0. Resolve project root and manifest path. Fail-silent if missing.
# -----------------------------------------------------------------------
ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
[[ -d "$ROOT" ]] || exit 0
MANIFEST="$ROOT/manifest.jsonl"

# Hard fail-silent if jq isn't on PATH. The convention file documents
# the dependency.
command -v jq >/dev/null 2>&1 || exit 0

# -----------------------------------------------------------------------
# 1. Read PostToolUse event JSON from stdin and extract the command.
# -----------------------------------------------------------------------
event="$(cat 2>/dev/null || true)"
[[ -z "$event" ]] && exit 0

cmd="$(printf '%s' "$event" | jq -r '.tool_input.command // empty' 2>/dev/null)"
[[ -z "$cmd" ]] && exit 0

# -----------------------------------------------------------------------
# 2. Identify the first "real" word (skip env assignments and a few
#    common wrappers). If it isn't an analytical interpreter, exit silent.
# -----------------------------------------------------------------------
# Strip leading FOO=bar BAZ=qux env-assignment tokens.
words=($cmd)
i=0
while [[ $i -lt ${#words[@]} && "${words[$i]}" == *=* && "${words[$i]}" != *' '* ]]; do
  i=$((i+1))
done
# Skip wrappers like `time`, `nice`, `nohup`, `sudo`.
while [[ $i -lt ${#words[@]} ]]; do
  case "${words[$i]}" in
    time|nice|nohup|sudo) i=$((i+1));;
    *) break;;
  esac
done
first="${words[$i]:-}"
[[ -z "$first" ]] && exit 0

# Strip path: /usr/bin/python3 → python3.
first_base="${first##*/}"

case "$first_base" in
  Rscript|R)
    language="R"
    ;;
  python|python3)
    language="python"
    ;;
  stata|stata-mp|stata-se|stata-be)
    language="stata"
    ;;
  *)
    # Not analytical. Silent exit.
    exit 0
    ;;
esac

# -----------------------------------------------------------------------
# 3. Extract script path from the command (best-effort).
#    For Rscript foo.R       → foo.R
#    For python -m pkg.mod   → pkg.mod (module form, treated as script)
#    For python foo.py       → foo.py
#    For stata -b do foo.do  → foo.do
# -----------------------------------------------------------------------
script="null"
shift_argv=("${words[@]:$((i+1))}")
j=0
while [[ $j -lt ${#shift_argv[@]} ]]; do
  arg="${shift_argv[$j]}"
  case "$arg" in
    -m)
      # python -m module → next arg is module name
      j=$((j+1))
      script="${shift_argv[$j]:-null}"
      break
      ;;
    do|run)
      # stata -b do foo.do
      j=$((j+1))
      script="${shift_argv[$j]:-null}"
      break
      ;;
    -e|--vanilla|--no-save|--no-restore|-q|--quiet|-b|-s|--slave|--silent)
      # Skip flags that don't take values. (`-e` for Rscript takes an
      # expression but has no script path; we set script to "<inline>".)
      [[ "$arg" == "-e" ]] && { script="<inline>"; break; }
      j=$((j+1))
      ;;
    -*)
      # Unknown flag — skip.
      j=$((j+1))
      ;;
    *)
      script="$arg"
      break
      ;;
  esac
done

# -----------------------------------------------------------------------
# 4. Compute the standard fields.
# -----------------------------------------------------------------------
timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# git sha (best-effort).
git_sha="null"
if git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  sha="$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || true)"
  [[ -n "$sha" ]] && git_sha="\"$sha\""
fi

# Active phase (best-effort, from .scc/status/*.md filename).
phase="null"
if [[ -d "$ROOT/.scc/status" ]]; then
  active="$(ls -1 "$ROOT/.scc/status" 2>/dev/null | head -1 || true)"
  [[ -n "$active" ]] && phase="\"${active%.md}\""
fi

# Seed extraction (best-effort, only if the script file is readable).
seed="null"
if [[ "$script" != "null" && "$script" != "<inline>" && -r "$ROOT/$script" ]]; then
  case "$language" in
    R)
      s="$(grep -Eo 'set\.seed\(\s*[0-9]+\s*\)' "$ROOT/$script" 2>/dev/null | head -1 | grep -Eo '[0-9]+' || true)"
      ;;
    python)
      s="$(grep -Eo '(np\.random\.seed|random\.seed|torch\.manual_seed)\(\s*[0-9]+\s*\)' "$ROOT/$script" 2>/dev/null | head -1 | grep -Eo '[0-9]+' || true)"
      ;;
    stata)
      s="$(grep -Eo 'set seed\s+[0-9]+' "$ROOT/$script" 2>/dev/null | head -1 | grep -Eo '[0-9]+' || true)"
      ;;
    *) s="" ;;
  esac
  [[ -n "$s" ]] && seed="$s"
fi

# env_hash: sha256 fingerprint of the language runtime.
sha256_of() {
  if command -v sha256sum >/dev/null 2>&1; then
    printf '%s' "$1" | sha256sum | awk '{print $1}'
  else
    printf '%s' "$1" | shasum -a 256 | awk '{print $1}'
  fi
}
env_input=""
case "$language" in
  R)
    if command -v Rscript >/dev/null 2>&1; then
      env_input="$(Rscript --version 2>&1)|$(Rscript -e 'cat(rownames(installed.packages()))' 2>/dev/null || true)"
    fi
    ;;
  python)
    py="$first_base"
    command -v "$py" >/dev/null 2>&1 || py="python3"
    if command -v "$py" >/dev/null 2>&1; then
      env_input="$($py --version 2>&1)|$($py -m pip freeze 2>/dev/null || true)"
    fi
    ;;
  stata)
    if command -v "$first_base" >/dev/null 2>&1; then
      env_input="$($first_base -b -q 'display c(stata_version)' 2>&1 | head -5 || true)"
    fi
    ;;
esac
[[ -z "$env_input" ]] && env_input="$first_base unavailable"
env_hash="$(sha256_of "$env_input")"

# Inputs: best-effort heuristic — any *.csv | *.parquet | *.dta | *.rds
# path appearing as a positional argument after the script.
inputs_json="null"
inputs_arr=()
for arg in "${shift_argv[@]}"; do
  case "$arg" in
    *.csv|*.parquet|*.dta|*.rds|*.feather|*.arrow|*.tsv|*.json)
      inputs_arr+=("$arg")
      ;;
  esac
done
if [[ ${#inputs_arr[@]} -gt 0 ]]; then
  inputs_json="$(printf '%s\n' "${inputs_arr[@]}" | jq -R . | jq -s -c .)"
fi

# Outputs: best-effort — files modified in `output/` in the last 60s.
# This is "good enough"; a real diff requires a pre-run snapshot which
# PostToolUse hooks cannot capture (we only fire post-run).
outputs_json="null"
output_sha="null"
if [[ -d "$ROOT/output" ]]; then
  # find with -newer is awkward; use mtime threshold instead.
  fresh=$(find "$ROOT/output" -type f -mmin -1 2>/dev/null | sed "s|^$ROOT/||" || true)
  if [[ -n "$fresh" ]]; then
    outputs_json="$(printf '%s\n' "$fresh" | jq -R . | jq -s -c .)"
    primary="$(printf '%s\n' "$fresh" | head -1)"
    if [[ -r "$ROOT/$primary" ]]; then
      output_sha="\"$(sha256_of "$(cat "$ROOT/$primary")" 2>/dev/null || echo unknown)\""
      # Use a file-based sha for binary safety:
      if command -v sha256sum >/dev/null 2>&1; then
        h="$(sha256sum "$ROOT/$primary" 2>/dev/null | awk '{print $1}')"
      else
        h="$(shasum -a 256 "$ROOT/$primary" 2>/dev/null | awk '{print $1}')"
      fi
      [[ -n "$h" ]] && output_sha="\"$h\""
    fi
  fi
fi

# -----------------------------------------------------------------------
# 5. Build the row with jq (handles JSON escaping correctly) and append.
# -----------------------------------------------------------------------
row="$(jq -c -n \
  --arg ts        "$timestamp" \
  --arg script    "$script" \
  --arg language  "$language" \
  --argjson inputs   "$inputs_json" \
  --argjson outputs  "$outputs_json" \
  --argjson out_sha  "$output_sha" \
  --argjson seed     "$seed" \
  --arg env_hash  "$env_hash" \
  --argjson git_sha  "$git_sha" \
  --argjson phase    "$phase" \
  '{
    timestamp:     $ts,
    script:        $script,
    language:      $language,
    inputs:        $inputs,
    outputs:       $outputs,
    output_sha256: $out_sha,
    seed:          $seed,
    env_hash:      $env_hash,
    git_sha:       $git_sha,
    phase:         $phase
  }' 2>/dev/null)"

# If jq couldn't build the row for any reason, exit silently rather than
# leaking a malformed line.
[[ -z "$row" ]] && exit 0

# Append atomically. `>>` is atomic for small writes on local POSIX FS.
printf '%s\n' "$row" >> "$MANIFEST" 2>/dev/null || true

exit 0

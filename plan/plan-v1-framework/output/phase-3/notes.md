# Phase 3 — implementation notes

## Files written

- `.claude/conventions/manifest-logging.md` — the protocol. JSONL row schema,
  audit-ritual `jq` queries, allowlist of analytical interpreters, discipline
  rules (append-only, never edit, commit it).
- `.claude/hooks/log-manifest.sh` — the silent PostToolUse hook. ~270 lines
  with comments. Allowlist on first-real-word of the command, after
  stripping `FOO=bar` env-assignments and `time`/`nice`/`nohup`/`sudo`
  wrappers. Builds the row with `jq` (proper JSON escaping); appends with
  `>>` (atomic for small writes). Never writes to stdout. Always exits 0.
- `docs/manifest-mechanism.md` — design doc. Covers why JSONL (vs YAML /
  SQLite / plaintext), field-by-field rationale, what this does NOT do,
  tradeoffs accepted, extension points.

## Scratch outputs (for lead to splice)

- `claude-md-pointer.md` — 5-line block in the same shape as the existing
  "## Insights Logging" block. Splice into `templates/CLAUDE.md.template`
  beneath the existing pointer (above the trailing `<!-- ... -->` comment).
- `settings-entry.json` — the PostToolUse entry. **Splice point**: add it
  as a sibling of the existing `"Stop"` array inside the `"hooks"` object
  in `.claude/settings.template.json`. The result should be:
  ```
  "hooks": {
    "Stop":        [ ... existing ... ],
    "PostToolUse": [ ... new ... ]
  }
  ```
  Don't drop the leading `_comment`.

## Verification ran (and passed)

1. **Smoke test, R**: `Rscript scripts/foo.R data.csv` produces a row with
   correct `language: "R"`, `seed: 42`, `inputs: ["data.csv"]`, real
   `env_hash` from `Rscript --version + installed.packages`, real `git_sha`.
2. **Smoke test, python**: `python3 scripts/foo.py` produces `language:
   "python"`, `seed: 123` (extracted from `np.random.seed(123)`),
   `env_hash` from `python --version + pip freeze`.
3. **Smoke test, python -m**: `python -m mypackage.train` produces
   `script: "mypackage.train"` (module form). No file to grep for seed,
   so `seed: null` — correct.
4. **Smoke test, stata**: `stata -b do scripts/run.do` produces
   `script: "scripts/run.do"`, `language: "stata"`. Stata not installed
   on dev box, so `env_hash` falls back to `sha256_of("stata-mp unavailable")`
   — graceful.
5. **Non-analytical**: `ls -la`, `git status` produce no row, no stdout.
6. **Empty stdin / malformed JSON stdin**: hook exits 0 silently.
7. **JSON validity**: every emitted row parses with `python3 -c
   "import json; json.loads(line)"`.
8. **Outputs detection**: file written to `output/` within last minute is
   picked up; `output_sha256` = `sha256sum` of that file.
9. **Stdout silence**: `out=$(...) ; [[ -z "$out" ]]` true on every path.
10. **Install.sh propagation**: fresh `install.sh /tmp/test-...-phase3`
    drops `log-manifest.sh` executable into target, seeds empty
    `manifest.jsonl`, lands convention file. End-to-end test on installed
    target produces a valid row.

## Surprises / what didn't work the first time

- **Initial install test failed** because install.sh requires the target
  dir to pre-exist (`if [[ ! -d "$TARGET" ]]; then exit 1`). Pre-existing
  Phase 1 behavior, not a regression. Fixed locally with `mkdir -p`
  before the test invocation. Worth flagging if Phase 8 README polish
  wants to soften that ergonomic.
- **Pre-run snapshot impossible from PostToolUse.** Wanted to compare
  pre/post mtime to detect outputs reliably — but PostToolUse fires
  *after* the command, so we can't snapshot beforehand. Settled for
  a 1-minute mtime window in `output/`. Good enough for typical
  fast-finishing scripts; documented as "best-effort" in both the
  convention and the design doc.
- **`set -e` removed** from the hook. With `-e`, a transient `jq`
  failure on a weird command string would exit nonzero and surface
  as a session error. The hook is wrapped in defensive `|| true` /
  `|| exit 0` patterns instead.
- **`jq` is a hard dependency.** Pure-bash JSON construction is
  available but error-prone (escaping a script path containing a
  quote). Documented. Hook fails silent if `jq` is missing — no
  log row written, but no error either. The convention file says so.
- **`env_hash` for Python uses `pip freeze` of whichever python is
  resolved by the hook process** — not necessarily the same venv
  the user actually runs the analytical script in. This is a
  fundamental limitation of running env detection from a hook
  rather than from inside the script. For exact reproduction
  guarantees, projects should commit a real lockfile alongside
  the script. Documented in the tradeoffs section.

## Nothing to escalate

No scope ambiguity. No constraint violation. No file outside the
"do NOT touch" list was modified. Phase 1's install.sh already
chmods all hooks at install time (line in install.sh: `find ... -name
"*.sh" -exec chmod +x`), so the new hook propagates executable
without any install.sh edit needed.

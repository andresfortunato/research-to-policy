# Manifest Logging — Protocol

**Trigger**: Automatic. A PostToolUse hook (`log-manifest.sh`) appends one
JSON line per analytical Bash run to `manifest.jsonl` at the project root.
This convention documents the format the hook produces and the audit
ritual researchers use to read it back.

## Where the manifest lives

- Single file: `manifest.jsonl` at the project root.
- Format: **JSON Lines** — one JSON object per line, no trailing comma,
  no surrounding array. Greppable with `grep`, queryable with `jq`,
  parseable in Python (`json.loads(line)`) and R (`jsonlite::stream_in`).
- **Append-only.** Never edit a row. Never overwrite. Never sort.
  History is the point.

## Required fields per row

Every row produced by the hook contains these keys (use `null` when a
field cannot be extracted, never omit the key):

| field | type | meaning |
|---|---|---|
| `timestamp`     | string  | ISO8601 UTC, e.g. `2026-05-05T14:32:11Z` |
| `script`        | string  | path to the analytical script (relative to project root if possible) |
| `language`      | string  | one of `R`, `python`, `stata`, `bash` |
| `inputs`        | array\|null | input file paths if extractable from the command/script, else `null` |
| `outputs`       | array\|null | output paths produced (best-effort: files newly appearing under `output/` between pre-run and post-run mtime scan) |
| `output_sha256` | string\|null | sha256 of the *primary* output (first entry of `outputs`) |
| `seed`          | int\|null | RNG seed if grep finds `set.seed(NN)` / `np.random.seed(NN)` / `set seed NN` in the script |
| `env_hash`      | string  | sha256 digest of language-runtime fingerprint (see below) |
| `git_sha`       | string\|null | `git rev-parse HEAD` (null if not a git repo or no commits) |
| `phase`         | string\|null | active plan/phase name (best-effort, from `.scc/status/*.md` or null) |

### env_hash composition per language

- **R**: sha256 of `R.version.string` plus the output of `installed.packages()[,c("Package","Version")]` (sorted). The hook approximates this cheaply: sha256 of `Rscript --version` plus `Rscript -e 'cat(rownames(installed.packages()))'`.
- **python**: sha256 of `python --version` concatenated with `pip freeze` (or `python -m pip list --format=freeze`).
- **stata**: sha256 of the Stata version string (`stata -b -q "display c(stata_version)"`).
- **bash**: sha256 of `bash --version` (rare — only logged when the analytical script is itself a shell pipeline, not for one-liners).

The hash is a fingerprint, not a full lockfile. Collisions are vanishingly
unlikely in practice; if exact reproduction matters, the corresponding
lockfile (`renv.lock`, `requirements.txt`, etc.) should be committed
alongside the script.

## Audit ritual

Reproducing a chart from N months ago:

```bash
# 1. Find the row that produced output/06c_fdi_at_entry.png
jq 'select(.outputs != null and (.outputs | index("output/06c_fdi_at_entry.png")))' manifest.jsonl

# 2. Read git_sha; check out that commit in a worktree
git worktree add /tmp/repro <git_sha>

# 3. Restore the env (use the lockfile committed at that sha; env_hash is a check, not a recipe)

# 4. Re-run the script; compute sha256 of the new output
sha256sum output/06c_fdi_at_entry.png
# Compare to output_sha256 in the manifest row
```

Common queries:

```bash
# All runs of one script
jq 'select(.script == "scripts/06c_fdi_at_entry.R")' manifest.jsonl

# All runs in the last week
jq --arg cutoff "$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ)" \
   'select(.timestamp > $cutoff)' manifest.jsonl

# Runs with no recorded seed (reproducibility risk)
jq 'select(.language == "R" or .language == "python") | select(.seed == null)' manifest.jsonl

# Distinct env_hashes seen for one script (env drift detection)
jq -r 'select(.script == "scripts/foo.R") | .env_hash' manifest.jsonl | sort -u
```

## What counts as an analytical run

The hook fires for command words on this allowlist: `Rscript`, `R`,
`python`, `python3`, `stata`, `stata-mp`, `stata-se`. Plain shell commands
(`ls`, `git`, `cat`, `grep`, `find`, `mkdir`, `cd`, `mv`, `cp`, `rm`,
`echo`, `head`, `tail`, `awk`, `sed`, `wc`, `which`, `make`) do not.
Pipelines that *include* an analytical command are detected on the first
word of the first segment (best-effort — a `cat foo | python script.py`
will be missed; document explicit `python script.py` invocations).

## Discipline

- **One row per run, written by the hook.** Researchers do not hand-edit
  this file.
- **The hook is silent.** A successful append is invisible at the chat
  layer. To verify, run `tail -1 manifest.jsonl`.
- **Commit the manifest.** It is a project-level artifact like
  `insights/INDEX.md` — co-evolves with the analytical scripts.
- **Do not gitignore `manifest.jsonl`.** Without it committed, the
  reproducibility ledger is useless to a future reader.
- **If the hook misfires** (a run produced no row, or a non-analytical
  command produced one), edit the allowlist in `.claude/hooks/log-manifest.sh`
  — never patch the manifest by hand.

## What this convention does NOT cover

- Reproduction *verification* — that's `/verify` (Phase 4), which reads
  manifest rows and re-runs scripts to compare hashes.
- Source-of-truth registry of *intended* runs — that's the plan files
  under `plan/`. The manifest records what *did* run, not what was
  supposed to.
- Snapshotting the data inputs themselves. The manifest records paths
  and an env hash; immutable raw inputs live under `raw/` (separate
  convention).

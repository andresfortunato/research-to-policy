# Manifest mechanism — design rationale

## The problem this solves

Research outputs drift from the inputs that produced them. A chart in a
ministerial briefing was made eight months ago by a script that has since
been refactored, against a dataset that has since been re-downloaded,
under an R or Python environment that has since been updated. When a
counterpart asks "can you redo this with last quarter's data?" or
"what's the source for this number?", reconstructing the answer is a
multi-day archaeology project.

The conventional fix — a `Makefile` or `dvc.yaml` plus per-script
README — is real engineering, expensive to maintain, and rarely
adopted in policy-research engagements where the team turnover is
high and the data lifecycle is messy. We need something cheaper:
a **silent ledger** that records, for every analytical run, enough
metadata to reconstruct it later.

## Why JSON Lines

Considered and rejected: YAML (slow to parse, merge-conflict-prone),
SQLite (binary, can't grep, can't review in a code editor),
plaintext logs (unparseable), one-file-per-run (clutters the tree).

JSONL wins because:
- **Append-only by construction.** No locking, no edits, no migrations.
  A bash hook with `>>` is the entire write path.
- **Greppable.** `grep '"script": "foo.R"' manifest.jsonl` works at
  3am with no tools installed.
- **Parseable from R, Python, jq.** All three first-class consumers
  (`jsonlite::stream_in`, `json.loads(line) for line in f`,
  `jq -c .` pipelines) handle JSONL natively.
- **Survives merge conflicts.** Two researchers appending in parallel
  produce a 3-way merge that git resolves trivially — both sets of
  rows kept, ordering preserved within each branch's contribution.
- **One file per project.** No sprawl. Easy to find, easy to commit,
  easy to git-blame a specific row.

## The pieces

### 1. The convention file (`.claude/conventions/manifest-logging.md`)

Documents the row schema, the audit ritual (`jq` queries to reproduce
a chart), and the discipline (append-only, never edit, commit it).
Read on demand by Claude when a researcher asks "where did this
output come from" — not loaded every session.

### 2. The PostToolUse hook (`.claude/hooks/log-manifest.sh`)

Fires on every `Bash` tool invocation. Reads the event JSON from stdin,
inspects `tool_input.command`, and routes:

- **Allowlisted analytical interpreter** (`Rscript`, `R`, `python`,
  `python3`, `stata`, `stata-mp`, `stata-se`, `stata-be`) → build a
  manifest row, append to `manifest.jsonl`, exit 0.
- **Anything else** (`ls`, `git`, `cat`, `grep`, `mkdir`, `cd`, `mv`,
  `cp`, `rm`, `make`, ...) → exit 0 silently.

The hook never writes to stdout (PostToolUse stdout = additionalContext
fed back to Claude; we don't want any of that). All side effects are
on the file system.

### 3. The CLAUDE.md pointer (~5 lines)

Tells Claude the manifest exists, points at the convention file for the
schema, and notes that the PostToolUse hook handles writes automatically.

## Field-by-field rationale

| field | why |
|---|---|
| `timestamp`     | Cheap chronological key. ISO8601 UTC so cross-timezone teams agree. |
| `script`        | The thing being run. Without this, the row is nameless. |
| `language`      | Disambiguates `foo.R` vs `foo.py` and tells the reader which env to reconstruct. |
| `inputs`        | What the run consumed. Best-effort: positional `*.csv`/`*.parquet`/`*.dta`/`*.rds` args. Imperfect — a script with hard-coded paths won't have its inputs detected — but better than nothing, and the script itself is in git so a reader can always grep it. |
| `outputs`       | What the run produced. Detected by mtime: files modified in `output/` within the last minute. Imperfect — we miss outputs to non-`output/` dirs, and we may pick up unrelated mtime touches — but again, better than the zero-information default. |
| `output_sha256` | Lets `/verify` (Phase 4) re-run the script and confirm bit-identical output. Single hash = primary output (first detected). |
| `seed`          | Reproducibility's most common silent failure: forgot `set.seed`. Recording it surfaces the gap without forcing it. |
| `env_hash`      | Coarse fingerprint of the language runtime (R version + installed packages, Python version + pip freeze, Stata version). Two runs with the same hash used the same env; two with different hashes did not. Real lockfile ≠ env hash; the hash detects drift. |
| `git_sha`       | Pins the row to a code state. Combined with `script`, this is the URL of the analytical artifact. |
| `phase`         | Optional. When the project has an active scc-style plan, the hook tags the row with the phase name so `jq` queries can group by plan-phase. |

## What this does NOT do

- **Does not run reproductions.** That's `/verify` in Phase 4. The
  manifest is data; verification is a skill.
- **Does not snapshot the data.** Inputs are recorded as paths, not as
  byte-for-byte copies. Immutable data lives under `raw/` (separate
  convention).
- **Does not sandbox the env.** `env_hash` detects drift; it does not
  prevent it. For exact reproduction, commit the lockfile alongside
  the script.
- **Does not detect indirect inputs.** A script that reads `config.yaml`
  at runtime won't have `config.yaml` in its `inputs` array. Researchers
  who care about this can pass the config explicitly as a positional arg.
- **Does not infer outputs across pipelines.** `cat foo | python | tee bar`
  will under-detect; explicit `python script.py` invocations are detected
  reliably.

## Tradeoffs accepted

- **Best-effort outputs detection.** The 1-minute mtime window catches
  the typical case (one script writes to `output/` and finishes in
  seconds). Long-running scripts that finish in >60s after the hook
  fires would miss their outputs — but the hook fires on PostToolUse,
  so by the time it runs the command has *already finished*. The
  window is "files modified before this hook ran but after the prior
  hook ran"; we approximate with `mmin -1`.
- **`env_hash` is a fingerprint, not a manifest.** Two researchers on
  different machines with materially different pkg versions could in
  principle hash to the same value. In practice, sha256 over the full
  pip-freeze string makes collisions vanishingly unlikely; the field
  is a check, not a guarantee.
- **Allowlist is conservative.** Stata variants, `Rscript`, `R`,
  `python`, `python3` — that's it. A research project using `julia`
  or `node` for analysis needs to add words to the allowlist. Easy
  fix, but a one-line edit. We chose conservative-by-default to
  prevent log spam from the long tail of "looks-like-analysis but
  isn't" tools.
- **Hard dependency on `jq`.** We could have written the JSON-emit
  path in pure bash with manual escaping, but the cost of getting
  string escaping wrong (a script path containing a quote breaks
  every downstream consumer) was higher than the cost of one extra
  brew/apt install. Documented in the convention; the hook fails
  silently if `jq` is missing.
- **Hook produces no Claude-visible output.** Researchers who want to
  see "did the manifest get a row?" must run `tail -1 manifest.jsonl`
  manually. We chose silent-by-default to keep the cost budget at
  effectively zero tokens (a chatty PostToolUse hook would charge
  per Bash invocation, which adds up fast in an analytical session).

## Extension points

- **`/verify` (Phase 4)** consumes manifest rows as its input. Given
  an output file, it queries the manifest for the row that produced it,
  re-runs the script, and compares hashes.
- **`/scan-sources` (Phase 7)** writes its own row to the same manifest
  with `script: scan-sources` and the source URL as the input. This
  unifies the reproducibility log across analytical and ingestion runs.
- **Allowlist editing.** Add `julia`, `node`, `racket`, etc. to the
  `case` block in `log-manifest.sh` if your stack uses them.
- **Phase tagging.** The hook reads `.scc/status/*.md` filenames. If
  a project uses a different active-plan marker, edit that block.
- **Per-project schema extensions.** Adding a new field is one `--arg`
  in the jq invocation; downstream consumers tolerate unknown fields
  by default.

## Provenance

The hard-won lesson behind this convention: in a Cambodia growth
diagnostics project, a chart that had been signed off by ministerial
counterparts needed to be regenerated 7 months later with updated
data. The script existed; the data existed; the env had drifted
enough that the chart came out subtly different (a different kernel
density bandwidth in a newer R version) and nobody could say whether
the new chart or the old chart was correct. The manifest mechanism
exists so the next such question takes minutes, not days.

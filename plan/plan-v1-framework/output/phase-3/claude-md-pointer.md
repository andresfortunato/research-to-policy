## Manifest Logging

Every analytical Bash run (Rscript, python, stata) is silently logged as
one JSONL row in `manifest.jsonl` at the project root by a PostToolUse
hook. Format spec + audit ritual: `.claude/conventions/manifest-logging.md`
(read on demand). Never edit `manifest.jsonl` by hand — append-only.

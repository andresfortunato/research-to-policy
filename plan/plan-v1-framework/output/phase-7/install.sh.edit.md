# Phase 7 — install.sh edit

## Summary

Three changes to `install.sh`:

1. Seed `sources/` directory in the target project, mirroring
   `templates/sources/` (registry.yaml + README.md).
2. Create empty `sources/seen.jsonl` (the dedup log) if absent — same
   pattern as the empty-seed `manifest.jsonl` block.
3. Update the `.gitignore` block to ensure `sources/` and
   `raw/sources/` are committed in target projects (they're
   project-shared knowledge, not per-researcher local state). The
   current gitignore block does NOT exclude these paths — the
   selective `.claude/*` rule only narrows the `.claude/` subtree, and
   `raw/`/`sources/` are siblings, so they're committed by default.
   Confirm by inspection; no positive `!` rules required.

## Suggested unified diff

```diff
--- a/install.sh
+++ b/install.sh
@@ -73,11 +73,12 @@ fi
 # --- 3. Project-level scaffolding (insights/, wiki/, raw/, deliverables/) --
-mkdir -p insights wiki raw deliverables
+mkdir -p insights wiki raw deliverables sources
 copy_if_absent "$SUPER_CLAUDIO/templates/insights/INDEX.md" insights/INDEX.md
 mirror_dir "$SUPER_CLAUDIO/templates/wiki"         wiki
 mirror_dir "$SUPER_CLAUDIO/templates/raw"          raw
 mirror_dir "$SUPER_CLAUDIO/templates/deliverables" deliverables
+mirror_dir "$SUPER_CLAUDIO/templates/sources"      sources

 # --- 4. manifest.jsonl (empty seed — append-only audit log) ----------------
 if [[ ! -f manifest.jsonl ]]; then
@@ -85,6 +86,14 @@ if [[ ! -f manifest.jsonl ]]; then
 else
   echo "  ~ manifest.jsonl (exists, leaving as-is)"
 fi

+# --- 4b. sources/seen.jsonl (empty seed — append-only dedup log) -----------
+if [[ ! -f sources/seen.jsonl ]]; then
+  : > sources/seen.jsonl
+  echo "  + sources/seen.jsonl (empty seed)"
+else
+  echo "  ~ sources/seen.jsonl (exists, leaving as-is)"
+fi
+
 # --- 5. CLAUDE.md (only if absent — never overwrite) -----------------------
```

## Annotated walkthrough of the changes

### Change 1: section 3 — add `sources` to mkdir list and mirror

Section 3 in the current `install.sh` (lines 73–78) seeds the
project-level scaffolding directories. Add `sources` to the `mkdir`
list and a `mirror_dir` call below the existing three. The
`mirror_dir` helper handles the `.gitkeep`-skip and idempotency for
us — same pattern as `wiki`, `raw`, `deliverables`.

This lands `sources/registry.yaml` (the four-commented-example
template) and `sources/README.md` (the how-to-register guide) in the
target project. Both are checked-in artifacts — the registry is the
project's source of truth and lives in git.

### Change 2: section 4b — empty seed for `sources/seen.jsonl`

Mirror Phase 1's `manifest.jsonl` empty-seed pattern (section 4 at
lines 81–86). The dedup log is append-only and starts empty; `:>` is
the bash idiom for "create or truncate." Skip if the file exists, so
re-running `install.sh` on an active project doesn't wipe the dedup
history.

Place this section as 4b directly after section 4 — both are
empty-seed JSONL ledgers and grouping them keeps the install script
readable.

### Change 3: gitignore block — confirm `sources/` and `raw/sources/` are committed

The current `.gitignore` block (lines 97–115) reads:

```
.claude/*
!.claude/conventions/
!.claude/conventions/**
!.claude/hooks/
!.claude/hooks/**
!.claude/skills/
!.claude/skills/**
!.claude/agents/
!.claude/agents/**
!.claude/settings.json

# Framework working state — local to each researcher's machine
plan/
brainstorms/
.scc/
```

The `.claude/*` selective-include rule applies only inside `.claude/`.
`sources/` and `raw/` are top-level siblings of `.claude/`, so they
fall through to "not gitignored" — i.e. they are committed by
default. **No positive `!` rule is required.**

The framework working-state block (`plan/`, `brainstorms/`, `.scc/`)
correctly does NOT include `sources/` or `raw/`. Both are
researcher-shared, not researcher-local — they belong in git in the
target project, just like `wiki/` and `insights/` already do.

**Action: no change to the gitignore block needed.** If the lead wants
belt-and-suspenders explicitness, an inline comment can be added:

```diff
 # Framework working state — local to each researcher's machine
 plan/
 brainstorms/
 .scc/
+
+# Note: sources/, raw/, wiki/, insights/, deliverables/, manifest.jsonl
+# are project-shared and intentionally NOT gitignored.
```

This is cosmetic. The behavior is correct without it.

## Footer message update (optional)

The "Done. Next steps:" footer (lines 128–134) lists three checks. If
the lead wants to surface the source-registry in the next-steps list,
suggested addition:

```diff
 echo "Done. Next steps:"
 echo "  1. Edit CLAUDE.md to fit your project."
 echo "  2. Verify .claude/settings.json hooks list matches what you want enabled."
 echo "  3. Test the insights hook:"
 echo "       touch output/06_test_chart.png   # simulate analysis"
 echo "       bash .claude/hooks/check-insights.sh   # should print JSON"
 echo "       rm output/06_test_chart.png"
+echo "  4. (Optional) Register sources for tracked scraping:"
+echo "       Edit sources/registry.yaml; run /scan-sources to fetch."
```

Optional — the README and convention file already cover this. Include
it only if the lead thinks the install footer should grow per phase.

## Test plan

After applying the edits:

```bash
mkdir -p /tmp/scc-phase7-test
bash install.sh /tmp/scc-phase7-test

# Verify
ls /tmp/scc-phase7-test/sources/
#   expected: README.md  registry.yaml  seen.jsonl

cat /tmp/scc-phase7-test/sources/seen.jsonl | wc -c
#   expected: 0 (empty seed)

python3 -c "import yaml; yaml.safe_load(open('/tmp/scc-phase7-test/sources/registry.yaml'))"
#   expected: no error (the four examples are commented out, sources: [] is valid)

# Re-run install.sh — should be idempotent
bash install.sh /tmp/scc-phase7-test
#   expected: "  ~ sources/seen.jsonl (exists, leaving as-is)"
#   expected: "  ~ sources/registry.yaml (exists, skipping)" (via mirror_dir's copy_if_absent)
```

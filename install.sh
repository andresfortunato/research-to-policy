#!/usr/bin/env bash
# super-claudio-research installer
#
# Usage:
#   ./install.sh <target-project-path>
#   ./install.sh                       # installs into $PWD
#
# Idempotent: safe to re-run; existing files are preserved.

set -euo pipefail
shopt -s nullglob

SUPER_CLAUDIO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-$PWD}"

if [[ ! -d "$TARGET" ]]; then
  echo "Target directory does not exist: $TARGET" >&2
  exit 1
fi

cd "$TARGET"
echo "Installing super-claudio-research into: $TARGET"

# --- helpers ---------------------------------------------------------------

# Copy a file or directory if the destination doesn't already exist. Skips
# .gitkeep placeholders (those exist only to commit empty dirs in the
# framework repo and shouldn't propagate to target projects).
copy_if_absent() {
  local src="$1" dst="$2"
  local name
  name=$(basename "$src")
  [[ "$name" == ".gitkeep" ]] && return 0
  if [[ -e "$dst" ]]; then
    echo "  ~ $dst (exists, skipping)"
  else
    cp -R "$src" "$dst"
    echo "  + $dst"
  fi
}

# Mirror the contents of $1 into $2 one level deep, idempotent.
mirror_dir() {
  local src_dir="$1" dst_dir="$2"
  [[ -d "$src_dir" ]] || return 0
  mkdir -p "$dst_dir"
  for entry in "$src_dir"/* "$src_dir"/.[!.]*; do
    [[ -e "$entry" ]] || continue
    copy_if_absent "$entry" "$dst_dir/$(basename "$entry")"
  done
}

# --- 1. Conventions, hooks, skills, agents (under .claude/) ----------------
mkdir -p .claude/conventions .claude/hooks .claude/skills .claude/agents
mirror_dir "$SUPER_CLAUDIO/.claude/conventions" .claude/conventions
mirror_dir "$SUPER_CLAUDIO/.claude/hooks"       .claude/hooks
mirror_dir "$SUPER_CLAUDIO/.claude/skills"      .claude/skills
mirror_dir "$SUPER_CLAUDIO/.claude/agents"      .claude/agents

# Hooks must be executable.
for f in .claude/hooks/*.sh; do
  [[ -f "$f" ]] && chmod +x "$f"
done

# --- 2. settings.json (only if absent — user customizations preserved) -----
if [[ ! -f .claude/settings.json ]]; then
  cp "$SUPER_CLAUDIO/.claude/settings.template.json" .claude/settings.json
  echo "  + .claude/settings.json (from template)"
else
  echo "  ~ .claude/settings.json (exists — merge new hook entries manually if needed)"
fi

# --- 3. Project-level scaffolding (insights/, wiki/, raw/, deliverables/, sources/) --
mkdir -p insights wiki raw deliverables sources
copy_if_absent "$SUPER_CLAUDIO/templates/insights/INDEX.md" insights/INDEX.md
mirror_dir "$SUPER_CLAUDIO/templates/wiki"         wiki
mirror_dir "$SUPER_CLAUDIO/templates/raw"          raw
mirror_dir "$SUPER_CLAUDIO/templates/deliverables" deliverables
mirror_dir "$SUPER_CLAUDIO/templates/sources"      sources

# --- 4. manifest.jsonl (empty seed — append-only audit log) ----------------
if [[ ! -f manifest.jsonl ]]; then
  : > manifest.jsonl
  echo "  + manifest.jsonl (empty seed)"
else
  echo "  ~ manifest.jsonl (exists, leaving as-is)"
fi

# --- 4b. sources/seen.jsonl (empty seed — append-only dedup log) -----------
if [[ ! -f sources/seen.jsonl ]]; then
  : > sources/seen.jsonl
  echo "  + sources/seen.jsonl (empty seed)"
else
  echo "  ~ sources/seen.jsonl (exists, leaving as-is)"
fi

# --- 5. CLAUDE.md (only if absent — never overwrite) -----------------------
if [[ ! -f CLAUDE.md ]]; then
  cp "$SUPER_CLAUDIO/templates/CLAUDE.md.template" CLAUDE.md
  echo "  + CLAUDE.md (from template — edit it for your project)"
else
  echo "  ~ CLAUDE.md (exists — add new convention pointer blocks manually if missing)"
fi

# --- 6. .gitignore — share framework scaffolding, hide local state --------
GITIGNORE_BLOCK=$(cat <<'GITIGNORE'
# super-claudio-research framework — share scaffolding, hide local state
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
GITIGNORE
)

if [[ -f .gitignore ]] && grep -q "super-claudio-research framework" .gitignore; then
  echo "  ~ .gitignore (framework block already present — review manually if upgrading from an older install)"
elif [[ -f .gitignore ]]; then
  printf '\n%s\n' "$GITIGNORE_BLOCK" >> .gitignore
  echo "  + .gitignore (appended framework block)"
else
  printf '%s\n' "$GITIGNORE_BLOCK" > .gitignore
  echo "  + .gitignore (created with framework block)"
fi

echo
echo "Done. Next steps:"
echo "  1. Edit CLAUDE.md to fit your project."
echo "  2. Verify .claude/settings.json hooks list matches what you want enabled."
echo "  3. Test the insights hook:"
echo "       touch output/06_test_chart.png   # simulate analysis"
echo "       bash .claude/hooks/check-insights.sh   # should print JSON"
echo "       rm output/06_test_chart.png"

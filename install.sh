#!/usr/bin/env bash
# super-claudio-research installer
#
# Usage:
#   ./install.sh <target-project-path>
#   ./install.sh                       # installs into $PWD
#
# Idempotent: safe to re-run; existing files are preserved.

set -euo pipefail

SUPER_CLAUDIO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-$PWD}"

if [[ ! -d "$TARGET" ]]; then
  echo "Target directory does not exist: $TARGET" >&2
  exit 1
fi

cd "$TARGET"
echo "Installing super-claudio-research into: $TARGET"

# 1. Conventions + hooks
mkdir -p .claude/conventions .claude/hooks
for f in "$SUPER_CLAUDIO"/.claude/conventions/*.md; do
  name=$(basename "$f")
  if [[ -f ".claude/conventions/$name" ]]; then
    echo "  ~ .claude/conventions/$name (exists, skipping)"
  else
    cp "$f" ".claude/conventions/$name"
    echo "  + .claude/conventions/$name"
  fi
done
for f in "$SUPER_CLAUDIO"/.claude/hooks/*.sh; do
  name=$(basename "$f")
  if [[ -f ".claude/hooks/$name" ]]; then
    echo "  ~ .claude/hooks/$name (exists, skipping)"
  else
    cp "$f" ".claude/hooks/$name"
    chmod +x ".claude/hooks/$name"
    echo "  + .claude/hooks/$name"
  fi
done

# 2. settings.json (only if absent — user customizations preserved)
if [[ ! -f .claude/settings.json ]]; then
  cp "$SUPER_CLAUDIO/.claude/settings.template.json" .claude/settings.json
  echo "  + .claude/settings.json (from template)"
else
  echo "  ~ .claude/settings.json (exists — merge hooks manually if needed)"
fi

# 3. insights/INDEX.md
mkdir -p insights
if [[ ! -f insights/INDEX.md ]]; then
  cp "$SUPER_CLAUDIO/templates/insights/INDEX.md" insights/INDEX.md
  echo "  + insights/INDEX.md"
else
  echo "  ~ insights/INDEX.md (exists, skipping)"
fi

# 4. CLAUDE.md (only if absent — never overwrite)
if [[ ! -f CLAUDE.md ]]; then
  cp "$SUPER_CLAUDIO/templates/CLAUDE.md.template" CLAUDE.md
  echo "  + CLAUDE.md (from template — edit it for your project)"
else
  echo "  ~ CLAUDE.md (exists — add the Insights Logging pointer manually if missing)"
fi

# 5. .gitignore — append framework block if not already present
if [[ -f .gitignore ]] && ! grep -q "super-claudio-research framework" .gitignore; then
  cat >> .gitignore <<'GITIGNORE'

# super-claudio-research framework — share conventions/hooks/settings, hide local state
.claude/*
!.claude/conventions/
!.claude/conventions/**
!.claude/hooks/
!.claude/hooks/**
!.claude/settings.json
GITIGNORE
  echo "  + .gitignore (appended framework block)"
elif [[ ! -f .gitignore ]]; then
  cat > .gitignore <<'GITIGNORE'
# super-claudio-research framework — share conventions/hooks/settings, hide local state
.claude/*
!.claude/conventions/
!.claude/conventions/**
!.claude/hooks/
!.claude/hooks/**
!.claude/settings.json
GITIGNORE
  echo "  + .gitignore (created with framework block)"
else
  echo "  ~ .gitignore (framework block already present)"
fi

echo
echo "Done. Next steps:"
echo "  1. Edit CLAUDE.md to fit your project."
echo "  2. Verify .claude/settings.json hooks list matches what you want enabled."
echo "  3. Test the insights hook:"
echo "       touch output/06_test_chart.png   # simulate analysis"
echo "       bash .claude/hooks/check-insights.sh   # should print JSON"
echo "       rm output/06_test_chart.png"

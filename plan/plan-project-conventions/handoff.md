# Handoff: project-conventions

**Status:** ✅ COMPLETE — all 3 phases shipped. Ready for archival.
**Date:** 2026-05-07
**Last commit on plan branch:** `4f03972` — "Phase 3: install.sh + README for project_conventions"

## Phase status

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Convention + design rationale | ✅ done | b4d6e4a. `.claude/conventions/project-conventions.md` (185 lines) and `docs/project-conventions-mechanism.md` (282 lines). |
| 2 | Templates + CLAUDE.md pointer block | ✅ done | 304fa87. Three seed files in `templates/project_conventions/` + replaced inline `## Visualization Conventions` placeholder with a 5-line pointer block + added `project_conventions/` to the codebase-structure tree. |
| 3 | Installer + framework-level docs | ✅ done | 4f03972. `install.sh` mkdir bump + one `mirror_dir` call; `README.md` three tree edits + one "Conventions installed" entry. |

## Where we are

Plan complete. Three commits, mirroring the just-shipped
`refdocs-conventions` shape. The third folder convention —
`project_conventions/` for project-bespoke style/process rules —
is now installed by `install.sh` and surfaced in framework
docs, with a generic `EXAMPLE_visualization.md` ready for
projects to replace with their own rules.

Phase 3 was the smallest of the three by line count:
two file edits (install.sh: 6 line changes, README.md: 9 line
additions). Verification ran against three targets (fresh
`/tmp` dir / idempotent re-run / cambodia-growth re-install)
— all passed.

The eight-pointer-blocks count in
`docs/audience-and-philosophy.md` is now technically eleven
once you count visualization → project-conventions as a
re-classification of the inline-section into a pointer block.
Audience-and-philosophy.md was deliberately NOT edited (not in
the file manifest); the count claim there is a v1 historical
statement that survived this addition without contradiction.

## What's next

**Plan complete.** Per implementation skill:

1. User confirms plan completion.
2. `touch plan/plan-project-conventions/.completed` triggers the
   Stop hook, which spawns the archivist + cleanup subagents.
3. Archivist synthesizes
   `archive/plan-project-conventions.md`, updates
   `archive/index.md`, cleans up
   `plan/plan-project-conventions/`, updates `.scc/status/`.
4. Cleanup scans the file manifest for dead code (none expected
   — every new file is intentional; the only deletion is the
   inline `## Visualization Conventions` placeholder, which was
   replaced by the pointer block).

Future framework work post-archive (deferred per plan):

- **Additional ship-with examples** (`EXAMPLE_writing_guidelines.md`,
  `EXAMPLE_slide_design.md`). Defer to v1.x — let pilot use
  surface what shape the next examples should take.
- **`/project-conventions-lint` skill.** Possible if pilot use
  shows discipline slipping (files without triggering language,
  duplicated rules across files). Not v1.
- **Cambodia migration.** None needed — Cambodia already runs
  the pattern; the framework now matches Cambodia's working
  precedent.

## Surprises

- **Cambodia `~ INDEX.md (exists, skipping)` line is the only
  "preserved existing" line in the cambodia install output.**
  The plan's load-bearing assumption was that BOTH `INDEX.md`
  and `visualization.md` would be preserved. In practice,
  `visualization.md` doesn't get listed at all because the
  source `templates/project_conventions/` only contains
  `EXAMPLE_visualization.md`, not `visualization.md` — so
  `mirror_dir` doesn't iterate that filename. The MD5 hash
  check confirms cambodia's `visualization.md` is genuinely
  untouched (same hash before and after install). The plan's
  assumption was fine; the verification path is just more
  subtle than "look for `~ visualization.md`."
- **Cambodia install dropped EXAMPLE_visualization.md and
  README.md as new files** alongside the framework-upgrade
  convention file (`+ .claude/conventions/project-conventions.md`).
  These three were untracked. Per the previous plan's pattern,
  the test-specific additions (`EXAMPLE_visualization.md`,
  `README.md`) were cleaned up after verification; the
  framework upgrade (`.claude/conventions/project-conventions.md`)
  was left as untracked for the user to review.
- **Mechanism doc came in at 282 lines.** Plan said
  "~100–200 lines". The peer mechanism docs are 229 (data-
  sources) and 284 (methods); 282 fits the actual peer band.
  The plan's stated band was loose; the peer band is the real
  constraint.
- **`SECTION_COLORS` slipped through the first draft of
  EXAMPLE_visualization.md.** The plan called this out as
  Cambodia-specific (named in the "load-bearing constraints"
  section), and the first draft used it as an illustrative
  identifier. Caught and genericized to "a sector-color dict
  in `<project>_utils.py`" before commit. Lesson: when a plan
  names specific identifiers to avoid, grep for them after
  writing, not just before.

## What didn't work

Nothing this session — the plan was a structurally-identical
clone of refdocs-conventions, and copying the rhythm worked
exactly as the previous handoff predicted.

## Verification log

- **Fresh install** — `rm -rf /tmp/test-pc-project && mkdir
  /tmp/test-pc-project && bash install.sh /tmp/test-pc-project`.
  Output included `+ project_conventions/EXAMPLE_visualization.md`,
  `+ project_conventions/INDEX.md`,
  `+ project_conventions/README.md`. The convention file
  `project-conventions.md` landed in `.claude/conventions/`.
- **Idempotency** — re-ran install in the same `/tmp` dir;
  every line for project_conventions files (and the convention
  file) starts with `~ ... (exists, skipping)`. Four total.
- **Cambodia-growth** — `bash install.sh ~/cambodia-growth`.
  Output:
  - `+ .claude/conventions/project-conventions.md` (new
    framework convention).
  - `+ project_conventions/EXAMPLE_visualization.md` (new test
    file; cleaned up after).
  - `~ project_conventions/INDEX.md (exists, skipping)`
    (existing INDEX preserved).
  - `+ project_conventions/README.md` (new test file; cleaned
    up after).
  - `visualization.md` not iterated (the source dir only has
    `EXAMPLE_visualization.md`, not `visualization.md`).
  - MD5 of `INDEX.md` and `visualization.md` unchanged
    before/after.
  `git diff --stat` on cambodia-growth showed only one
  pre-existing modification (`insights/INDEX.md`, +1 line),
  unrelated to this install.
- **Convention file content checks** — `grep -in
  "boundary|principle 9|use this document whenever"` on
  `.claude/conventions/project-conventions.md` confirmed the
  three load-bearing items: `## Boundary with neighbors`
  section opens at line 18; `Why Principle 9 does NOT bind`
  section opens at line 88; the triggering-language rule is
  named at line 78 with a worked example at line 156. The
  file naming rule is at line 75–77.
- **Example file content checks** —
  `EXAMPLE_visualization.md` opens with "Use this document
  whenever creating, editing, or reviewing charts..." at line
  9. `grep -i "cambodia|#ee3e4c|#6db5db|cambodia_utils|
  SECTION_COLORS"` returned no matches — file is generic.
- **CLAUDE.md.template pointer block** — 5 content lines
  (matches the ≤6 constraint). Pattern (name +
  when-to-apply + "see ... for protocol") matches the eight
  existing pointer blocks.
- **`git status --short`** before each commit on framework
  repo: only the intended changes plus pre-existing untracked
  `.scc/status/...` and `plan/...` directories.
- **`git diff --stat`** totals — Phase 1: 467 insertions,
  2 files. Phase 2: 154 insertions, 3 deletions, 4 files.
  Phase 3: 18 insertions, 8 deletions, 2 files.

## Hash trail

- Phase 1 work (convention + mechanism doc): `b4d6e4a`
- Phase 2 work (templates + CLAUDE.md pointer block): `304fa87`
- Phase 3 work (install.sh + README): `4f03972`
- Handoff refresh + hash-trail fill-in for completion: (this commit)

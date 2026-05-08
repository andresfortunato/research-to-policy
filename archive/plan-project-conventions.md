# Project Conventions

Completed: 2026-05-07

## What was built

Third folder convention: `project_conventions/` for project-bespoke style/process rules (visualization, eventually writing voice, slide design, naming idioms). Modeled on the working pattern in `~/cambodia-growth/project_conventions/`. After this plan, `install.sh` lays down a `project_conventions/` folder with `INDEX.md` + `README.md` + a generic `EXAMPLE_visualization.md`, and the inline `## Visualization Conventions` placeholder in `CLAUDE.md.template` was replaced by a 5-line pointer block matching every other convention.

## Key decisions

1. **Distinct from `data_sources/` and `methods/`.** `project_conventions/` is for *project decisions about how this engagement does its work* — color choices, chart-naming rules, writing voice. Not external reference docs (those are `data_sources/`, with freshness anchors). Not operational compute rules (those are `methods/`, with diagnostic counts). The convention's opening "boundary with neighbors" paragraph says this explicitly.
2. **No required internal sections.** Style rules don't fit a single template (visualization needs color/typography/legend rules; writing voice needs tone/register/active-vs-passive rules). The convention enforces only naming (`<domain>.md`, lowercase snake_case) and triggering language (every file opens with "Use this document whenever ...").
3. **Principle 9 (freshness anchors) deliberately does not bind.** These are project decisions, not external claims that rot. Don't bolt on a Status/Anchor section that doesn't apply.
4. **No new hooks, no new skills.** Reference docs, not enforcement-needing discipline. Project-conventions discipline is researcher-curated and Claude-loaded-on-demand.
5. **Generic example only.** `EXAMPLE_visualization.md` ships generic — no Cambodia red/blue rule, no engagement-specific filenames. Per Principle 8 (open-source-from-day-one).

## Methods landed

None — convention ships seeds; project-specific style rules land in target projects.

## Files added or modified

- ✚ `.claude/conventions/project-conventions.md`
- ✚ `docs/project-conventions-mechanism.md`
- ✚ `templates/project_conventions/{INDEX.md, README.md, EXAMPLE_visualization.md}`
- ✎ `templates/CLAUDE.md.template` — replaced inline `## Visualization Conventions` placeholder with 5-line pointer block; added `project_conventions/` to codebase-tree
- ✎ `install.sh` — `mkdir -p` bump + one `mirror_dir` call
- ✎ `README.md` — three tree edits + one "Conventions installed" entry

## Learnings

- **Cambodia `~ INDEX.md (exists, skipping)` was the only "preserved existing" line in the cambodia install output.** The plan's load-bearing assumption was that BOTH `INDEX.md` and `visualization.md` would be preserved. In practice, `visualization.md` doesn't get listed at all because the source `templates/project_conventions/` only contains `EXAMPLE_visualization.md`, not `visualization.md` — so `mirror_dir` doesn't iterate that filename. The MD5 hash check confirmed cambodia's `visualization.md` was genuinely untouched. Lesson: verification paths can be subtler than "look for `~ <filename>` in install output"; sometimes the absence is the proof.
- **The eight-pointer-blocks count in `audience-and-philosophy.md`** is now technically eleven once you count visualization → project-conventions as a re-classification of inline-section into pointer block. Audience-and-philosophy.md was deliberately NOT edited (not in the manifest); the count claim there is a v1 historical statement that survived this addition without contradiction.

## Metrics
- Phases: 3 (Convention / Templates / Installer)
- Sessions: 2
- Final commit: `4f03972`

# Plan: project-conventions

Add a third folder convention to the framework — `project_conventions/`
— for **project-bespoke style/process rules** (visualization, eventually
writing voice, slide design, naming). Modeled on the pattern already
working in `~/cambodia-growth/project_conventions/`. Follows the exact
shape of the just-shipped `data-sources` and `methods` conventions
(`plan/plan-refdocs-conventions/`).

## Goal

Replace the inline `## Visualization Conventions` placeholder in
`templates/CLAUDE.md.template` (lines 52–54) with a pointer block to a
new on-demand `project_conventions/` folder. After this ships,
`install.sh` lays down a `project_conventions/` folder with INDEX +
README + a generic visualization example, and the CLAUDE.md template
points at it like every other convention. Researchers stop reinventing
the structure each project (Cambodia did it manually; Córdoba shouldn't
have to).

## Constraints

- **Don't duplicate `data_sources/` or `methods/`.** This convention
  is for *project-bespoke style/process rules* — visualization color
  choices, chart-naming rules, eventually writing voice and slide
  design. It is NOT external reference docs (those are
  `data_sources/`, with freshness anchors) and NOT operational compute
  rules (those are `methods/`, with diagnostic counts). The
  convention's opening "boundary with neighbors" paragraph must say
  this explicitly.
- **No engagement-specific content in committed framework files.**
  The example file is generic — no Cambodia red/blue rule, no
  Cambodia brand-color filenames. Show the *shape*; the project fills
  in the content. Per Principle 8 (open-source-from-day-one).
- **Principle 9 (verifiable freshness anchors) does NOT bind.** These
  are project decisions, not external claims that rot. Don't bolt on
  a Status/Anchor section that doesn't apply.
- **`install.sh` stays idempotent.** Mirror the new template tree the
  same way the existing seven are mirrored. Cambodia's existing
  `project_conventions/INDEX.md` and `visualization.md` must survive
  a re-install untouched (`copy_if_absent` handles this — verify).
- **Keep CLAUDE.md.template short.** Pointer block ≤6 lines, matching
  every other block. Long protocol stays in
  `.claude/conventions/project-conventions.md`.
- **Conform to the framework constitution** in
  `docs/audience-and-philosophy.md`: silent-by-default,
  conditional-not-always-fire, composable, project-shared. No new
  hooks (these are reference docs, not enforcement-needing
  discipline). No new skills.

## Decisions Made

Settled in conversation that fed this plan; not to be re-debated.

- **Three folder conventions, not consolidated.** `data_sources/`,
  `methods/`, and `project_conventions/` are distinct content types
  with distinct required structures. Merging would muddy all three.
  See "boundary with neighbors" in Phase 1.
- **Folder name: `project_conventions/`, not `style/` or
  `house_style/`.** Cambodia is already on `project_conventions/`;
  zero migration. The name accurately scopes "things this project
  decided about how it does work" — which extends past visual style
  (writing voice, slide design, naming).
- **`INDEX.md` is required.** Same reasoning as `data_sources/`:
  the directory listing scans well at 1–3 files, but past that a
  quick-nav table saves time on every lookup. Cambodia's INDEX.md
  is the working proof of the shape.
- **No top-level required sections per file.** Unlike `data_sources/`
  (Status/Anchor/Endpoints/...) and `methods/` (Source/Rule/Why/...),
  project_conventions files are free-form per domain. Visualization
  has color rules + plotting conventions; writing has voice + tone +
  citation style. A single section template would be wrong. The
  convention enforces *naming* (one file per domain, lowercase,
  matches the INDEX) and *triggering language* (every file opens
  with "Use this document whenever ..."), not internal structure.
- **One example ships: `EXAMPLE_visualization.md`.** Visualization
  is the proven domain (Cambodia uses it daily).
  Writing-guidelines and slide-design examples can ship in v1.x
  once we have a concrete pattern from a pilot. v1 ships the
  *folder pattern* with one worked example.
- **No `/project-conventions-lint` skill.** Same reasoning as
  data-sources: the discipline is markdown shape, not enforcement.
  If pilot use shows discipline slipping, ship lint in v1.x.

## File Manifest

```
super-claudio-research/
├── .claude/conventions/
│   └── project-conventions.md                  ✚ protocol + boundary-with-data_sources/methods
├── docs/
│   └── project-conventions-mechanism.md        ✚ rationale (lightweight-skill framing, why no anchors, why no enforced sections)
├── templates/
│   ├── CLAUDE.md.template                      ✎ replace inline "Visualization Conventions" with pointer block; refresh codebase-structure tree
│   └── project_conventions/
│       ├── INDEX.md                            ✚ seed: empty quick-nav table + "how to add a convention" recipe
│       ├── README.md                           ✚ one-liner pointing at the convention
│       └── EXAMPLE_visualization.md            ✚ generic worked example: color rules / chart naming / plotting conventions, no Cambodia specifics
├── install.sh                                  ✎ add project_conventions to mkdir line + one mirror_dir call
└── README.md                                   ✎ add project_conventions to file tree (templates/ + .claude/conventions/) + "Conventions installed" entry
```

No deletions. No moves. The inline `## Visualization Conventions`
section in CLAUDE.md.template gets replaced by a pointer block; the
recommended-sections comment at the top of the template (around line
12) updates to reference the new convention.

## Repo Context

This is the third convention to ship in roughly the same shape. The
just-completed `plan/plan-refdocs-conventions/` (commits `b9c7ca7` →
`baefabc`, archived 2026-05-06) added `data-sources` and `methods` —
both following the same pattern: protocol in `.claude/conventions/`,
rationale in `docs/`, templates in `templates/<dir>/`, pointer block
in `templates/CLAUDE.md.template`, two-line edit to `install.sh`, one
entry in `README.md`. The implementer should read that plan's file
manifest and verification log before starting — this plan is the same
shape with one fewer file.

The target pattern lives in `~/cambodia-growth/project_conventions/`:

- `INDEX.md` (~9 lines) — quick-nav table with one entry, "add new
  conventions here" footer.
- `visualization.md` (~37 lines) — color rules + plotting conventions
  sections, opens with "Use this document whenever creating, editing,
  or reviewing charts...".

The implementer copies the *shape* of these files into generic
`templates/project_conventions/`, replacing all Cambodia-specific
content (red `#ee3e4c`, blue `#6db5db`, `cambodia_utils.py`,
`SECTION_COLORS`, etc.) with placeholder text or generic advice.

## Phases

Three phases, strictly sequential, mirroring the refdocs-conventions
shape. Total: 5 new files, 3 edited. Estimated context per phase
well under 30%; could be one session, but split for clean commits
and verification gates.

### Phase 1 — Convention + design rationale

- **Intent.** Write the protocol doc and the mechanism doc.
  Load-bearing content; everything in Phase 2 points at these files.
- **Files.**
  - `.claude/conventions/project-conventions.md` (new)
  - `docs/project-conventions-mechanism.md` (new)
- **Verification.**
  - Convention opens with a "boundary with neighbors" paragraph
    naming `data_sources/` (external ref docs, anchors), `methods/`
    (operational compute, diagnostic counts), and
    `.claude/conventions/` (framework-shared protocols). The
    trichotomy is spelled out, not assumed.
  - Convention says explicitly that Principle 9 (freshness anchors)
    does NOT bind — project conventions are decisions, not aging
    claims about external systems.
  - Convention names the *naming* and *triggering-language* rules
    (one file per domain, lowercase, matches INDEX; every file
    opens with "Use this document whenever ...") but does NOT
    enforce internal sections.
  - Mechanism doc covers: why a separate folder vs CLAUDE.md inline
    (token cost; per-domain reads); why no enforced sections (style
    rules don't fit a single template); why no skill (pattern is
    markdown discipline); why `project_conventions/` not `style/`
    (Cambodia precedent + scope clarity).
  - `wc -l` on the convention is in the band of existing
    conventions (~80–150 lines). The mechanism doc is in the band
    of existing mechanism docs (~100–200 lines).

### Phase 2 — Templates + CLAUDE.md pointer block

- **Intent.** Ship the seed files that `install.sh` will mirror, plus
  update `templates/CLAUDE.md.template` — replace the inline
  `## Visualization Conventions` placeholder with a pointer block
  matching existing block style.
- **Files.**
  - `templates/project_conventions/INDEX.md` (new)
  - `templates/project_conventions/README.md` (new)
  - `templates/project_conventions/EXAMPLE_visualization.md` (new)
  - `templates/CLAUDE.md.template` (edit)
- **Verification.**
  - `EXAMPLE_visualization.md` carries no Cambodia-specific
    content: no `#ee3e4c`, no `cambodia_utils.py`, no peer-country
    list, no `SECTION_COLORS`. Generic placeholders only.
  - `EXAMPLE_visualization.md` opens with "Use this document
    whenever creating, editing, or reviewing charts..." (the
    triggering-language rule).
  - `INDEX.md` has a quick-nav table with one row pointing at
    `EXAMPLE_visualization.md` and a "how to add a new convention"
    footer matching `data_sources/INDEX.md` style.
  - New CLAUDE.md.template pointer block matches existing style:
    name + when-to-apply + "see
    `.claude/conventions/project-conventions.md` for protocol";
    ≤6 lines.
  - The codebase-structure tree in CLAUDE.md.template lists
    `project_conventions/` with a one-line gloss alongside
    `data_sources/` and `methods/`.

### Phase 3 — Installer + framework-level docs

- **Intent.** Wire the new template into `install.sh` and surface
  the new convention in the framework `README.md`.
- **Files.**
  - `install.sh` (edit: add `project_conventions` to the mkdir
    line in section 3; add one `mirror_dir` call after the
    `methods` line)
  - `README.md` (edit: add `project_conventions/` to the
    `templates/` tree and `project-conventions.md` to the
    `.claude/conventions/` tree; add a "Conventions installed"
    entry between `methods` and `source-registry` matching the
    one-paragraph style of existing entries)
- **Verification.**
  - Run `bash install.sh /tmp/test-pc-project` against a fresh
    empty dir. Result: `project_conventions/INDEX.md`,
    `project_conventions/README.md`,
    `project_conventions/EXAMPLE_visualization.md` all present.
  - Re-run install in the same dir. Idempotency check: every line
    for project_conventions files starts with `~` (skip).
  - Run `bash install.sh ~/cambodia-growth`. Existing
    `project_conventions/INDEX.md` and
    `project_conventions/visualization.md` must NOT be
    overwritten — `~ exists, skipping` for both. The generic
    EXAMPLE file lands as a new file (Cambodia can delete it).
  - `README.md` "Conventions installed" list has the new entry
    in the same heading style as `methods` and `data-sources`.

## Phase Order + Dependencies

Phase 1 → Phase 2 → Phase 3, strictly sequential. Phase 2's example
file follows the convention's naming/triggering rules; Phase 3's
README blurb summarizes the convention rationale. No parallel
opportunities.

## Open Items Deferred

- **Additional ship-with examples** (`EXAMPLE_writing_guidelines.md`,
  `EXAMPLE_slide_design.md`). Defer to v1.x — ship one proven
  example (visualization) and let pilot use surface the next ones.
- **`/project-conventions-lint` skill.** Possible if pilot use
  shows discipline slipping (files without triggering language,
  duplicated rules across files). Not v1.
- **Cambodia migration.** Cambodia already runs the pattern; no
  migration needed.

## Implementation hint for next session

Read `plan/plan-refdocs-conventions/handoff.md` (or its archive) for
the exact verification log of the just-shipped pattern. This plan
deliberately mirrors that one — copying its rhythm reduces risk and
keeps framework conventions reading consistently.

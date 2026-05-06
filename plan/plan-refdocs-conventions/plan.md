# Plan: refdocs-conventions

Add two first-class folder conventions to the framework — `data_sources/`
(API/dataset reference docs) and `methods/` (project-specific methodology
specs) — modeled on the patterns proven out in `~/cambodia-growth/`.

## Goal

Codify two folder roles the framework currently assumes but doesn't define.
After this ships, a fresh `install.sh` lays down INDEX seeds, an example
doc per folder, and pointer blocks in `CLAUDE.md.template` — researchers no
longer reinvent the structure each project.

## Constraints

- **Don't duplicate the wiki layer.** `wiki/concepts/` already covers
  *distilled domain claims with citations*; `methods/` is for *operational
  project-internal rules with diagnostic counts*; `decisions/` is for
  *one-page peer-reviewable methodology calls*. Each new convention must
  open with a short "boundary with neighbors" paragraph so future researchers
  don't re-litigate.
- **Markdown-first, language-neutral.** No Python helper module bundled in
  this plan (helpers convention deferred — see Open Items).
- **Conform to the framework constitution** in `docs/audience-and-philosophy.md`:
  silent-by-default, conditional-not-always-fire, composable, project-shared.
  No new always-fire hooks.
- **`install.sh` stays idempotent.** Mirror the new template trees the same
  way the existing ones are mirrored. Don't break existing installs.
- **Keep CLAUDE.md.template short.** Each new pointer block ≤6 lines; long
  protocol stays in `.claude/conventions/<name>.md`.
- **No project-specific Cambodia content** in committed framework files.
  Example docs are generic (a fake `WORLD_BANK_API.md`, a fake
  `EXAMPLE_method/rule.md`).

## Decisions Made

Settled in the analysis conversation that fed this plan; not to be
re-debated during execution.

- **Two new conventions, not one.** `data-sources` and `methods` are
  separate concerns: data_sources is *how to access external data*; methods
  is *what we decided to compute and why*. Merging them would muddy both.
- **Required structure for each data_sources doc:** `Status: verified
  YYYY-MM-DD` line + at least one **headline anchor number** (a concrete
  value future-Claude can re-fetch as a smoke test) + workflow recipe +
  pitfalls. Modeled on `~/cambodia-growth/data_sources/imf_sdmx_api.md`.
- **Required structure for each methods doc:** Source, Rule, Why-this-version,
  Exclusions, Edge cases, Known limitations, Diagnostic counts. Modeled
  on `~/cambodia-growth/methods/electronics_entry/cohort_rule.md`.
- **Flat `data_sources/`, sub-folder-per-method `methods/`.** Cambodia's
  flat data_sources scans well at ~10 files; methods grow heterogeneous
  per-method appendages (PDFs, codebooks) that benefit from a folder.
- **`data_sources/INDEX.md` is required; `methods/` gets no top-level
  INDEX** — the directory listing is the index because each method's
  folder name is its handle.
- **Headline-anchor + freshness pattern is a cross-cutting principle**, not
  just a data_sources rule. Lift it once into `audience-and-philosophy.md`,
  then reference it from both new conventions.
- **No skill ships with this plan.** No `/scan-data-sources` or
  `/methods-lint`. The conventions are markdown discipline; tooling can
  follow if usage warrants.

## Repo Context

`super-claudio-research` is a thin Claude Code harness for research
projects. The shape:

- `.claude/conventions/<name>.md` — long-form protocol, read on demand.
- `.claude/hooks/<name>.sh` — silent-by-default Stop nudges (none new here).
- `.claude/skills/<name>/SKILL.md` — invokable slash commands (none new here).
- `templates/<dir>/...` — seed files mirrored into target projects by
  `install.sh`.
- `templates/CLAUDE.md.template` — short top-level doc with one pointer
  block per convention.
- `docs/<name>-mechanism.md` — design rationale, optional but expected for
  any new convention.
- `install.sh` — mirrors `.claude/{conventions,hooks,skills}/` and
  `templates/{insights,wiki,raw,sources,deliverables}/` into target.

Both new conventions slot into this shape without new primitives. The
only `install.sh` edit is one extra `mirror_dir` call per new template
tree (or one expansion of an existing mirror call).

The target patterns we're porting live in `~/cambodia-growth/data_sources/`
and `~/cambodia-growth/methods/electronics_entry/` — not committed to this
repo, but the user has them locally for reference during execution.

## File Manifest

```
super-claudio-research/
├── .claude/conventions/
│   ├── data-sources.md                       ✚ protocol + boundary-with-wiki
│   └── methods.md                            ✚ protocol + boundary-with-decisions/wiki
├── docs/
│   ├── audience-and-philosophy.md            ✎ add cross-cutting "verified-as-of + headline anchor" principle
│   ├── data-sources-mechanism.md             ✚ rationale (flat folder, INDEX, anchor-as-smoke-test)
│   └── methods-mechanism.md                  ✚ rationale (sub-folder, vN evolution, diagnostic counts)
├── templates/
│   ├── CLAUDE.md.template                    ✎ add two pointer blocks; refresh codebase-structure tree
│   ├── data_sources/
│   │   ├── INDEX.md                          ✚ seed: empty quick-nav table + "how to add a source"
│   │   ├── README.md                         ✚ one-liner: what this folder is for + link to convention
│   │   └── EXAMPLE_world_bank_api.md         ✚ generic worked example (Status / Anchor / Workflow / Pitfalls)
│   └── methods/
│       ├── README.md                         ✚ one-liner + link to convention
│       └── EXAMPLE_method/
│           └── rule.md                       ✚ generic worked example with all 7 required sections
├── install.sh                                ✎ add mirror_dir for templates/data_sources/ and templates/methods/
└── README.md                                 ✎ add the two new conventions to the "Conventions installed" list
```

No deletions. No moves.

## Phases

### Phase 1 — Conventions + design rationale

- **Intent.** Write the two protocol docs and the two mechanism docs.
  This is the load-bearing content; everything else in the plan is
  scaffolding that points at these files.
- **Files.**
  - `.claude/conventions/data-sources.md` (new)
  - `.claude/conventions/methods.md` (new)
  - `docs/data-sources-mechanism.md` (new)
  - `docs/methods-mechanism.md` (new)
  - `docs/audience-and-philosophy.md` (edit — add the cross-cutting
    freshness + anchor principle, ~1 short section)
- **Verification.**
  - Each convention opens with a "boundary with neighbors" paragraph
    (data-sources vs `raw/sources/`; methods vs `decisions/` vs
    `wiki/concepts/`).
  - Each convention names the required sections of a doc *and* shows them
    in the matching `templates/.../EXAMPLE*` file in Phase 2.
  - The cross-cutting principle in `audience-and-philosophy.md` is
    referenced (not duplicated) by both new conventions.
  - `wc -l` on each new convention is roughly in the band of existing
    conventions (~120–180 lines). Outliers either way are a smell.

### Phase 2 — Templates + CLAUDE.md pointer blocks

- **Intent.** Ship the seed files that `install.sh` will mirror, plus
  update the top-level CLAUDE.md template so a new project gets pointer
  blocks for both conventions.
- **Files.**
  - `templates/data_sources/INDEX.md`,
    `templates/data_sources/README.md`,
    `templates/data_sources/EXAMPLE_world_bank_api.md`
  - `templates/methods/README.md`,
    `templates/methods/EXAMPLE_method/rule.md`
  - `templates/CLAUDE.md.template` (edit — two pointer blocks, refresh
    the directory tree to surface `data_sources/` alongside `methods/`)
- **Verification.**
  - `EXAMPLE_world_bank_api.md` carries a real `Status: verified <date>`
    line and one anchor number (a generic but plausible WB indicator
    value, captioned as illustrative).
  - `EXAMPLE_method/rule.md` includes all seven required sections with
    generic-but-plausible content, including a diagnostic-counts block.
  - New CLAUDE.md.template pointer blocks match the existing block style
    (≤6 lines, name + when-to-apply + "see .claude/conventions/<name>.md").
  - The codebase-structure tree in CLAUDE.md.template lists both folders
    with one-line gloss.

### Phase 3 — Installer + framework-level docs

- **Intent.** Wire the new templates into `install.sh` and surface the
  new conventions in the framework `README.md`.
- **Files.**
  - `install.sh` (edit — `mkdir -p data_sources methods` and two
    `mirror_dir` calls)
  - `README.md` (edit — add `data-sources` and `methods` to the
    "Conventions installed" list with one-paragraph blurbs)
- **Verification.**
  - Run `bash install.sh /tmp/test-research-project` against a fresh
    empty dir. Result: `data_sources/INDEX.md`, `data_sources/README.md`,
    `data_sources/EXAMPLE_world_bank_api.md`, `methods/README.md`,
    `methods/EXAMPLE_method/rule.md` all present.
  - Re-run the install in the same dir. Idempotency check: every line
    of output for the just-installed files starts with `~` (skip).
  - Re-run the install against `~/cambodia-growth/`. Existing
    `data_sources/INDEX.md` and `methods/electronics_entry/` are NOT
    overwritten (`copy_if_absent` handles this — verify by diff).
  - `README.md` "Conventions installed" list has two new entries with
    the same heading style as existing ones.

## Phase Order + Dependencies

Phase 1 → Phase 2 → Phase 3, strictly sequential. Phase 2's example
files quote the convention's required-sections lists; Phase 3's
README blurbs summarize the convention rationale. No parallel
opportunities — this is all under ~10 files of mostly-prose changes.

## Open Items Deferred

- **Project-utility-module convention** (a `<project>_utils.py` skeleton
  + a convention saying "data_sources docs cross-link to functions
  here"). Worth shipping but language-coupled (Python-first) and would
  need an R analog; defer to a v1.2 plan that handles both.
- **`/methods-lint` or `/data-sources-lint` skills.** Possible if the
  conventions get heavy use and discipline starts slipping. Not v1.
- **Auto-extraction of headline anchors into a smoke-test runner.**
  Tempting (run all anchors weekly, alert on drift) but adds
  always-on infra; the convention is the v1 deliverable.
- **Lifting "headline anchor" into a wiki convention** (`wiki/synthesis/`
  pages getting an anchor field too). Logical extension; defer until
  synthesis pages see enough usage to know what an anchor would look
  like there.

# Refdocs Conventions

Completed: 2026-05-06

## What was built

Two first-class folder conventions: `data_sources/` (API/dataset reference docs) and `methods/` (project-specific methodology specs). Both modeled on patterns proven in `~/cambodia-growth/`. After this plan shipped, `install.sh` lays down INDEX seeds, an example doc per folder, and pointer blocks in `CLAUDE.md.template` — researchers no longer reinvent the structure each project.

## Key decisions

1. **Two new conventions, not one.** `data-sources` is *how to access external data*; `methods` is *what we decided to compute and why*. Merging them would muddy both — different required structures (Status/Anchor/Workflow vs. Source/Rule/Diagnostic counts), different aging behavior (data sources rot; methods don't).
2. **Required structure for each `data_sources/` doc**: `Status: verified YYYY-MM-DD` line + at least one **headline anchor number** (a concrete value future-Claude can re-fetch as a smoke test) + workflow recipe + pitfalls. Modeled on `~/cambodia-growth/data_sources/imf_sdmx_api.md`.
3. **Required structure for each `methods/` doc**: Source / Rule / Why-this-version / Exclusions / Edge cases / Known limitations / Diagnostic counts. Sub-folder per method (rules accrete codebooks, PDFs, helper queries); rule files evolve `v1 → v2 → v3` with prior version preserved in-doc.
4. **Flat `data_sources/`, sub-folder-per-method `methods/`.** Cambodia's working pattern; matches the volume difference (data sources are short reference docs; methods accrete supporting artifacts).
5. **Boundary discipline against neighbors.** Each convention opens with a "boundary with neighbors" paragraph: `decisions/` is peer-reviewable methodology calls; `wiki/concepts/` is distilled domain claims with citations; `methods/` is project-internal rules with diagnostic counts; `data_sources/` is how-to-access docs with freshness anchors.
6. **Principle 9 (verifiable freshness anchors)** added to the constitution — applies to `data_sources/` (and forward-compatible with future reference-doc conventions); explicitly does NOT bind project-decision conventions.

## Methods landed

None directly — the convention shipped a generic `EXAMPLE_method/rule.md` seed; project-specific methods land in target projects.

## Files added or modified

- ✚ `.claude/conventions/data-sources.md`, `.claude/conventions/methods.md`
- ✚ `docs/data-sources-mechanism.md`, `docs/methods-mechanism.md`
- ✎ `docs/audience-and-philosophy.md` — added Principle 9 (freshness anchors)
- ✚ `templates/data_sources/{INDEX.md, README.md, EXAMPLE_world_bank_api.md}`
- ✚ `templates/methods/{README.md, EXAMPLE_method/rule.md}`
- ✎ `templates/CLAUDE.md.template` — two new pointer blocks (Data Sources, Methods); codebase-tree updated
- ✎ `install.sh` — bumped `mkdir -p` to include `data_sources methods`; added two `mirror_dir` calls
- ✎ `README.md` — three tree edits + two "Conventions installed" entries

## Learnings

- **cambodia-growth install side-effect** during verification. Running `bash install.sh ~/cambodia-growth` brought every framework file the cambodia repo had been missing — because the older cambodia install had shipped only `insights-logging`. The framework-fresh-install path correctly handled the gap (idempotent helpers; `copy_if_absent` preserved cambodia's already-existing `INDEX.md`).
- **Three-pass verification** held up well: fresh `/tmp` install + idempotent re-run + cambodia-on-older-version install. The third check is what surfaced the side-effect; without it the upgrade path would have been untested.
- **Headline anchor + freshness pattern is load-bearing for `data_sources/`.** Re-fetching the anchor value proves the doc is still accurate. Without it, "verified-as-of YYYY-MM-DD" is just prose.

## Metrics
- Phases: 3 (Conventions / Templates / Installer)
- Sessions: 2
- Final commit: `baefabc`

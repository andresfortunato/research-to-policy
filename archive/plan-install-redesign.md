# Install Redesign

Completed: 2026-05-07

## What was built

Replaced `install.sh` with a Node-based CLI (`r2p`) mirroring scc's distribution model. Globally-installable via `npm install -g github:andresfortunato/research-to-policy`. Per-project `r2p init` *symlinks* shared infrastructure (skills, agents) into `~/.claude/` and *copies* project-shared scaffolding (conventions, hooks, settings, scaffolding folders) into the target project. Eliminates the manual-clone prerequisite, gives one source of truth for skills, and unbreaks the prior "skills can't be updated inside existing project installs" failure mode. Added `r2p init --upgrade` flow with `.framework-new` sidecars on divergence.

## Key decisions

1. **Distribution model**: drop `install.sh`; publish as Node package; `npm install -g github:andresfortunato/research-to-policy`. CLI binary `r2p`.
2. **Global vs. per-project split is load-bearing.** `~/.claude/{skills,agents}/` are symlinks (one source of truth, free updates). `.claude/{conventions,hooks,settings.json}`, scaffolding folders, `CLAUDE.md`, `.gitignore` block are copied per-project (committed to project repo so collaborators inherit them — Principle 4: project-shared, not user-personal). Don't blur the line.
3. **Sidecar-based `--upgrade`.** Divergent files get `<file>.framework-new` next to the original; never overwrites, never blocks on prompts. Rejected interactive y/n (breaks in CI) and hash-based "only touch unchanged" (needs install-manifest, breaks on whitespace reformatting).
4. **`r2p init --upgrade` over `r2p upgrade`.** Same code path, one extra flag. Keeps CLI surface small.
5. **`EXCLUDE` list for upgrade is the load-bearing knob.** User-managed seeds (CLAUDE.md, INDEX.md, wiki index/log, registry.yaml, project_conventions/INDEX, data_sources/INDEX, handoff.md, decision-record.md) never get sidecared on upgrade.
6. **Framework-repo guard.** `r2p init` and `r2p init --upgrade` both refuse cleanly when run against `research-to-policy` itself (guard: `package.json.name === "research-to-policy"`).
7. **Skill-name disjointness with scc verified.** `r2p` and `scc` coexist; symlinks into `~/.claude/{skills,agents}/` from both packages don't conflict. Pre-Phase-3 conflict check: research has verify/deliverable-review/wiki-{ingest,lint}/scan-sources/research-cleanup; code has brainstorming/planning/implementation/agent-teams/tdd/learning-capture. No overlap.
8. **`TODO.md` at framework root.** v1.1+ backlog moved out of README's "Roadmap" section into a discoverable single-`ls` location.
9. **Manual migration** for existing installs. `r2p init` warns if it finds an old-shape `<project>/.claude/skills/` directory; does not auto-delete.

## Methods landed

None — installer infrastructure, no project-internal methods.

## Files added or modified

- ✚ `package.json`, `src/cli.js`, `src/commands/init.js`
- ✚ `src/lib/install-project.js` — copies conventions/hooks/scaffolding seeds; idempotent
- ✚ `src/lib/install-globals.js` — symlinks `.claude/skills/` and `.claude/agents/` into `~/.claude/`
- ✚ `src/lib/upgrade.js` — sidecar-based `--upgrade` flow with EXCLUDE list and framework-repo guard
- ✚ `TODO.md` (framework root) — v1.1+ backlog
- ✎ `README.md` — Quickstart rewritten to `npm install -g …` + `r2p init`; documented `--upgrade` + `cp -R` recipe; stripped Roadmap; clarified skills are symlinked globally; updated dependency note (Node ≥18 + commander)
- ✘ `install.sh` — deleted
- ✎ Six docs/skills files — `install.sh` → `r2p init` (one-line edits)

## Learnings

- **`templates/` projection is asymmetric.** `.claude/conventions/<file>.md` lives at the same path in framework and project, but `templates/<x>` lives at `<project>/<x>` (the `templates/` prefix is dropped during install). `upgrade.js` handles both via a `toProjectRel()` projection that strips the `templates/` prefix when present. Without that, the upgrade would compare `templates/wiki/SCHEMA.md` against `<project>/templates/wiki/SCHEMA.md` (a path that doesn't exist) and emit spurious `+` lines.
- **`r2p init --upgrade` runs `installGlobals()` after the upgrade pass.** Symlinks may have gone stale if the user reinstalled the framework via `npm install -g` and the install path moved. Cheap to re-verify (idempotent), and skipping it would mean researchers have to remember to run `r2p init` (without `--upgrade`) to refresh global skill links — too easy to miss.
- **Removed `install.sh` references in docs/skills, not in `src/`.** Source-of-truth scope was "user-facing files" (README, TODO, plan/, brainstorms/, docs/, .claude/, templates/). Comments in `src/lib/install-project.js` ("ports the project-level work of install.sh into Node") are accurate historical context, kept.
- **README's "no hard external dependencies" line is now slightly less true.** Framework-installed pieces (hooks, conventions, templates) are still pure bash/markdown/JSON/YAML, but `r2p` itself needs Node ≥18 and `commander`. Updated the README sentence to draw that distinction explicitly.

## Metrics
- Phases: 4 (Bootstrap / Per-project install / Global symlinks / Upgrade flow)
- Sessions: ~3
- Final commit: `e2b84e1` Phase 3, with `--upgrade` work landing post-Phase 4

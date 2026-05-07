# Handoff — install-redesign

## Status

**Phase 4: ✅ done. Plan complete — all four phases verified.**

`src/lib/upgrade.js` lands the sidecar-based `--upgrade` flow. `src/commands/init.js` now branches on `options.upgrade` to delegate to `upgradeProject()` (followed by `installGlobals()` to refresh symlinks). README's Quickstart points at `npm install -g github:andresfortunato/super-claudio-research` + `scr init`; `--upgrade` and the project→project `cp -R` recipe are documented. `TODO.md` at the framework root holds the v1.1+ backlog plus the new globalize-conventions entry. `install.sh` deleted; references to it in current docs/skills updated to point at `scr init`.

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Bootstrap the Node package | ✅ done | package.json + install.js + src/cli.js + stubbed src/commands/init.js + .gitignore. Verified via `npm link`. |
| 2 | Per-project install (port install.sh) | ✅ done | `src/lib/install-project.js` + wired into `src/commands/init.js`. Diff vs `install.sh` output is exactly the two intended deltas. |
| 3 | Global skills/agents symlink | ✅ done | `src/lib/install-globals.js` ports scc-code's helpers near-verbatim. 6 skills symlinked into `~/.claude/skills/`; idempotent. |
| 4 | Upgrade flow + README + delete install.sh | ✅ done | `src/lib/upgrade.js`, `--upgrade` wired, README rewritten, `TODO.md` written, `install.sh` deleted, current-docs references updated. |

## Read Order

1. This file
2. `plan.md` — full plan (goal, constraints, decisions, file manifest, phases, dependencies)
3. `brainstorms/install-redesign.md` — decision rationale (do not re-debate)

## Start At

**No phases remaining.** Plan is ready for archival via the `.completed` marker.

## Key Constraints (final, for the archive record)

- The framework repo is **not** a target project. `scr init` and `scr init --upgrade` both refuse cleanly when run against `super-claudio-research` itself (guard: `package.json.name === "super-claudio-research"`).
- `scr` and `scc` coexist; both write into `~/.claude/{skills,agents}/`. Skill-name disjointness re-verified in Phase 3.
- Idempotency held end-to-end: install + immediate upgrade is a no-op; sidecars only written on real divergence; user-managed seeds (CLAUDE.md, INDEX.md, wiki index/log, registry.yaml) are never overwritten and never sidecared.
- Sidecar approach is v1's answer for divergent-file handling. Hash-based install-manifests and interactive prompts were rejected during planning.

## Open Decisions

None.

## Surprises (Phase 4)

- **`templates/` projection is asymmetric.** `.claude/conventions/<file>.md` lives at the same path in framework and project, but `templates/<x>` lives at `<project>/<x>` (the `templates/` prefix is dropped during install). `upgrade.js` handles both via a `toProjectRel()` projection that strips the `templates/` prefix when present. Without that, the upgrade would compare `templates/wiki/SCHEMA.md` against `<project>/templates/wiki/SCHEMA.md` (a path that doesn't exist) and emit spurious `+` lines.
- **EXCLUDE list is the load-bearing knob.** The plan said "exclude `templates/CLAUDE.md.template`" but the verification line ("scaffolding folders' content (insights/INDEX.md, etc.)") implied a wider exclusion. Settled list: CLAUDE.md.template, insights/INDEX.md, wiki/index.md, wiki/log.md, sources/registry.yaml, data_sources/INDEX.md, project_conventions/INDEX.md, plus the loose templates (handoff.md, decision-record.md) that have no fixed project counterpart. Verified: edits to all four user-managed seeds plus CLAUDE.md produce zero sidecars on `--upgrade`.
- **`scr init --upgrade` runs `installGlobals()` after the upgrade pass.** Symlinks may have gone stale if the user reinstalled the framework via `npm install -g github:...` and the install path moved. Cheap to re-verify (idempotent), and skipping it would mean researchers have to remember `scr init` (without `--upgrade`) to refresh global skill links — too easy to miss.
- **Removed `install.sh` references in docs/skills, not in `src/`.** Plan scope said "source-of-truth files (README, plan/, brainstorms/, docs/, .claude/, templates/)" — `src/` was excluded. Kept the comments in `src/lib/install-project.js` that explain "ports the project-level work of install.sh into Node" because they're accurate historical context for someone reading the code. Same logic for the active plan/brainstorm dir (`plan/plan-install-redesign/`, `brainstorms/install-redesign.md`) — references there describe install.sh's replacement, not promote its use.
- **README's "no hard external dependencies" line is now slightly less true.** The framework-installed pieces (hooks, conventions, templates) are still pure bash/markdown/JSON/YAML, but `scr` itself needs Node ≥18 and `commander`. Updated the README sentence to draw that distinction explicitly.

## What didn't work

Nothing this phase. Sidecar logic is straightforward (`readFile` + `Buffer.equals`); the projection function is two lines; the EXCLUDE list is a hardcoded `Set`. Most of the work was deciding what belongs on the EXCLUDE list — a one-shot reading of the plan's verification language and the templates/ contents settled it.

## Verification log (Phase 4)

- **Fresh-install + immediate `--upgrade`** — `rm -rf /tmp/test-scr-phase4 && mkdir /tmp/test-scr-phase4 && cd /tmp/test-scr-phase4 && scr init > /dev/null && scr init --upgrade`. Output: "No upgrades needed — project is in sync with the framework." No sidecars created.
- **Edited convention triggers sidecar** — `echo "EDIT BY USER" >> .claude/conventions/insights-logging.md && scr init --upgrade`. Output: `⚠ .claude/conventions/insights-logging.md.framework-new (divergent — sidecar written, original untouched)` + summary "1 file(s) have framework-new sidecars". Tail of original kept the user edit; tail of sidecar matched the framework version.
- **Excluded user-managed seeds get no sidecars** — edited `insights/INDEX.md`, `sources/registry.yaml`, `wiki/index.md`, `wiki/log.md`, and `CLAUDE.md`; ran `scr init --upgrade`. `find . -name "*.framework-new"` returned empty. Summary line: "No upgrades needed — project is in sync with the framework."
- **CLAUDE.md never sidecared** — explicit edit, then upgrade; `ls CLAUDE.md*` returns only `CLAUDE.md`; tail still has the user-customized line.
- **Old-shape skills warning** — manually `mkdir .claude/skills && touch .claude/skills/old-skill`, then `scr init --upgrade`. Output included `⚠ .claude/skills/ exists in this project — obsolete (skills now live globally in ~/.claude/skills/). Run `rm -rf .claude/skills/` to clean up. Not deleting automatically.` Directory was not deleted.
- **Framework-repo guard for upgrade** — guard added to `upgradeProject()` mirrors `installProject()`; refuses cleanly when run from the framework repo itself.
- **CLI help surfaces `--upgrade`** — `scr init --help` lists `--upgrade   Refresh framework-tracked files; emit .framework-new sidecars on divergence`.
- **README rewrite** — Quickstart is now `npm install -g github:andresfortunato/super-claudio-research` + `cd <project>` + `scr init` (3 commands). `--upgrade` documented in a follow-on section, project→project `cp -R` recipe documented after that. "Roadmap" section deleted; replaced with one-liner pointing at `TODO.md`.
- **`TODO.md` exists at framework root** — contains v1 status sentence, v1.1+ backlog (7 items previously in README's Roadmap), the new globalize-conventions entry with the open question about collaborator clones, and the build-pattern contributor note.
- **`install.sh` deleted** — `ls install.sh` returns "No such file or directory".
- **`git grep "install.sh"` clean in source-of-truth scope** — `git grep -l "install.sh" -- README.md TODO.md docs/ .claude/ templates/` returns no hits. References in `plan/plan-v1-framework/`, `plan/plan-project-conventions/`, `plan/plan-refdocs-conventions/`, `brainstorms/v1-framework-scope.md`, the active plan dir, and `src/lib/install-project.js` are intentionally left as historical context.

## Files added/modified (Phase 4)

- ✚ `src/lib/upgrade.js` — sidecar-based upgrade flow; walks `.claude/conventions/` + `templates/` (minus EXCLUDE), copies/skips/sidecars; old-skills warning; framework-repo guard.
- ✎ `src/commands/init.js` — replaced Phase 3 stub with real `--upgrade` branch (delegates to `upgradeProject` + `installGlobals`).
- ✚ `TODO.md` (framework root) — v1.1+ backlog moved from README's Roadmap + globalize-conventions entry + build-pattern note.
- ✎ `README.md` — rewrote Quickstart to `npm install -g …` + `scr init`; documented `--upgrade` + `cp -R` recipe; stripped Roadmap; clarified `skills/` is symlinked globally; updated dependency note (Node ≥18 + commander).
- ✘ `install.sh` — deleted.
- ✎ `docs/data-sources-mechanism.md`, `docs/methods-mechanism.md`, `docs/project-conventions-mechanism.md`, `docs/source-registry-mechanism.md` — `install.sh` → `scr init` (each one line).
- ✎ `.claude/skills/scan-sources/SKILL.md`, `.claude/skills/wiki-ingest/SKILL.md` — `install.sh` → `scr init` (each one line).

## Hash trail

- Phase 1 work: `e21f592`
- Handoff hash-trail fill-in for Phase 1: `3bf0476`
- Phase 2 work + handoff refresh: `9f0d3fc`
- Handoff hash-trail fill-in for Phase 2: `63563b0`
- Phase 3 work + handoff refresh: `e2b84e1`
- Handoff hash-trail fill-in for Phase 3: `cb0c1ec`
- Phase 4 work + handoff refresh: (this commit)

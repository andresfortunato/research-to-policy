# Plan: install-redesign

## Goal

Replace `install.sh` with a Node-based CLI (`scr`) that mirrors super-claudio-code's distribution model: globally-installable via `npm install -g github:andresfortunato/super-claudio-research`, exposing a per-project `scr init` that **symlinks** shared infrastructure (skills, agents) to `~/.claude/` and **copies** project-shared scaffolding (conventions, hooks, settings, folder seeds) into the target project. Eliminates the manual-clone prerequisite, gives one source of truth for skills, and unbreaks the current "skills can't be updated inside existing project installs" failure mode.

Decisions and rationale: see `brainstorms/install-redesign.md`.

## Constraints

- **All decisions in `brainstorms/install-redesign.md` are settled.** Don't re-debate during execution.
- **Idempotency is non-negotiable.** `scr init` and `scr init --upgrade` must be safe to re-run. Real files (user-edited convention files, custom CLAUDE.md, etc.) are never overwritten without explicit signal. Symlinks get refreshed when stale, never replace real files.
- **Mirror super-claudio-code's footprint.** Node ≥18, `commander` only. No new runtime deps.
- **The global/project split is load-bearing.** `~/.claude/skills/` + `~/.claude/agents/` are symlinks (one source of truth, free updates). `.claude/conventions/`, `.claude/hooks/`, `.claude/settings.json`, scaffolding folders, `CLAUDE.md`, `.gitignore` block are copied per-project (committed to the project repo so collaborators inherit them — README principle 4). Don't blur the line.
- **The framework repo is not a target project.** `scr init` is for *target research projects*. Don't pollute super-claudio-research itself with `insights/`, `wiki/`, etc. seeds. The framework repo is read by `scr`, not initialized by it.
- **`scr` and `scc` must coexist on the same machine.** Independent packages, independent bin entries, independent symlink sets in `~/.claude/{skills,agents}/`. No cross-package conflicts on skill names — quick conflict check is part of Phase 3 verification.
- **Updates from framework→project are non-destructive.** Divergent convention files get a `.framework-new` sidecar, never overwrite. Decision rationale in "Decisions resolved during planning" below.
- **README stays focused on the user-facing quickstart.** v1.1+ items move to a separate file (`TODO.md` at framework root). Item lands on the todo list: "globalize conventions (without conflicting with Claude's defaults)."
- **Don't gate `scr init` on a network call.** It must work fully offline once the package is installed (the user already has the framework repo on disk via npm install).

## Decisions Made (consumed from brainstorm)

These are settled. Cross-reference `brainstorms/install-redesign.md` for full rationale.

- **Distribution:** drop `install.sh`. Publish as a Node package; install via `npm install -g github:andresfortunato/super-claudio-research`.
- **CLI binary name:** `scr`.
- **Global** (symlinked to `~/.claude/`): `skills/`, `agents/`.
- **Per-project** (copied by `scr init`, committed to project repo): `.claude/conventions/`, `.claude/hooks/`, `.claude/settings.json`, scaffolding folders (`insights/`, `wiki/`, `raw/`, `deliverables/`, `sources/`, `data_sources/`, `methods/`, `project_conventions/`), `CLAUDE.md`, `.gitignore` block.
- **Convention sync = both flavors.** `scr init --upgrade` for framework→project; documented `cp -R` recipe in README for project→project.
- **Project-development todo list moves out of README** to a separate file in the framework repo.

### Decisions resolved during planning

These were flagged "open" in the brainstorm. Resolved here; revisit only with explicit scope-change.

- **`scr init --upgrade` divergent-file behavior: write `.framework-new` sidecars.** When the framework's version of a convention or template differs from the project's, `--upgrade` writes `<file>.framework-new` next to the existing file and prints a one-line summary at the end. Never overwrites, never blocks on prompts. *Rejected: (a) interactive y/n prompts — break in CI/non-TTY environments. Rejected: (c) hash-based "only touch unchanged files" — needs an install-manifest, breaks on whitespace reformatting, more complexity than v1 needs.* The user reviews sidecars with their preferred diff tool and merges manually.
- **Hook merging when `settings.json` already exists: append-if-missing.** For v1 there's only one hook (`check-insights.sh`). If `.claude/settings.json` exists and lacks the framework's hook entry, append it; otherwise leave alone. More elaborate merging deferred to a future hook-count threshold.
- **Upgrade is invoked as `scr init --upgrade`, not a separate `scr upgrade` command.** Same code path, one extra flag. Keeps the CLI surface small.
- **Project-development todo list location: `TODO.md` at framework repo root.** Discoverable in one `ls`, no nesting overhead. README's "Roadmap" section (`README.md:174-186`) moves there.
- **Migration for existing super-claudio-research installs:** `scr init` running against a project that already has the old `install.sh` layout detects the duplicated `.claude/skills/` directory and prints a one-line warning recommending `rm -rf .claude/skills/` (since skills now live globally). It does not auto-delete. No automated migration command needed — population is small.
- **Skill-name conflicts with super-claudio-code:** Phase 3 verification includes an explicit check that `super-claudio-research/.claude/skills/` and `super-claudio-code/skills/` share no skill names. If they ever conflict in the future, the second-installed package's symlinks would silently fail (the `installSkills` helper refuses to overwrite real files or other symlinks). Current state: no conflict (research has `verify`, `deliverable-review`, `wiki-ingest`, `wiki-lint`, `scan-sources`, `research-cleanup`; code has `brainstorming`, `planning`, `implementation`, `agent-teams`, `tdd`, `learning-capture`).

## Repo Context

**What exists today:**
- `install.sh` (`super-claudio-research/install.sh:1-136`) — the script being replaced. 4 logical sections: mirror `.claude/{conventions,hooks,skills}/`, ensure `settings.json`, copy template folders to project root, append `.gitignore` block.
- `.claude/{conventions,hooks,skills,agents}/` — the framework artifacts. `agents/` exists but is empty.
- `.claude/settings.template.json` — the project settings.json seed (`super-claudio-research/.claude/settings.template.json:1-17`). Already references hooks via `$CLAUDE_PROJECT_DIR` so it's project-relative.
- `templates/` — seed content for project-level scaffolding (CLAUDE.md, INDEX.md, SCHEMA.md, README.md, deliverable profiles, etc.). Currently mirrored by install.sh's `mirror_dir` helper.
- `README.md` — user-facing docs. The "Quickstart" (`README.md:74-82`) and "Roadmap" (`README.md:174-186`) sections both need edits.

**Reference implementation to mirror (sibling repo, `~/github/super-claudio-code/`):**
- `super-claudio-code/package.json` — package shape (`commander`, `"type": "module"`, `engines.node ≥18`, `bin: { scc: ./src/cli.js }`).
- `super-claudio-code/install.js:1-46` — npm postinstall entry. Resolves project root via `INIT_CWD` or upward `package.json` lookup, then delegates to `initCommand`. Port near-verbatim.
- `super-claudio-code/src/cli.js:1-44` — commander setup. Port the `scr init` registration pattern.
- `super-claudio-code/src/commands/init.js:128-170` — `installSkills()`, the global symlink helper. Detects existing correct symlinks, removes stale ones, refuses to overwrite real files. Port wholesale; rename target dir if needed (no — both packages target `~/.claude/skills/`, so they coexist by skill name).
- `super-claudio-code/src/commands/init.js:172-217` — `installAgents()`. Same pattern for `~/.claude/agents/`. Port wholesale.

**No conflict risk:**
- Both packages use `~/.claude/skills/` and `~/.claude/agents/`. Skill name namespaces are disjoint (verified above). The `installSkills` helper refuses to overwrite, so a future conflict would surface as a silent skip with a warning, not a clobber.
- Both packages will live in `~/.npm-global/lib/node_modules/` (or wherever the user's npm prefix points). No file overlap.

## File Manifest

```
super-claudio-research/
├── package.json                        ✚ name, version, type:module, bin: scr, dep: commander
├── install.js                          ✚ npm postinstall — port of super-claudio-code/install.js
├── src/                                ✚ new top-level dir
│   ├── cli.js                          ✚ commander entry — `scr init [--upgrade]`
│   ├── commands/
│   │   └── init.js                     ✚ orchestrates per-project + global install; --upgrade branch
│   └── lib/
│       ├── install-project.js          ✚ copy conventions, hooks, settings, scaffolding, CLAUDE.md, gitignore
│       ├── install-globals.js          ✚ symlink skills/agents to ~/.claude/ — port from scc-code
│       └── upgrade.js                  ✚ diff project↔framework convention/template files; emit .framework-new sidecars
├── install.sh                          ✘ delete after Phase 4
├── README.md                           ✎ rewrite Quickstart; document `--upgrade` + cp -R recipe; strip Roadmap
├── TODO.md                             ✚ project-development backlog (moved from README's Roadmap + new globalize-conventions entry)
├── .gitignore                          ✎ add node_modules/, .DS_Store
├── .claude/                            · unchanged
├── templates/                          · unchanged content; consumed by src/lib/install-project.js instead of install.sh
└── plan/                               · unchanged
```

The `.gitignore` block emitted *into target projects* by `scr init` (currently in `install.sh:100-115`) needs editing too — once skills + agents go global, the negation entries `!.claude/skills/` and `!.claude/skills/**` (and the implicit agents equivalents) are obsolete. The corrected block lives in `src/lib/install-project.js` as a string constant.

## Phases

### Phase 1 — Bootstrap the Node package

**Intent.** Stand up the Node package skeleton: `package.json`, `install.js`, `src/cli.js`, a stubbed `src/commands/init.js`. After this phase, `npm install -g .` from the framework repo (or `npm link`) gives a working `scr` binary that prints help text and a `scr init` that prints "not implemented yet". No real work happens — this phase only proves the distribution path is wired.

**Modifies/Adds.** `package.json` ✚, `install.js` ✚, `src/cli.js` ✚, `src/commands/init.js` ✚ (stub), `.gitignore` ✎.

**Verification.**
- `npm link` succeeds from `super-claudio-research/`; `which scr` resolves; `scr --help` prints commander-formatted output listing `init`.
- `scr init` (stub) prints a placeholder message and exits 0.
- `node_modules/` is gitignored.
- Re-running `npm link` is idempotent.

### Phase 2 — Per-project install (port install.sh's project-level work)

**Intent.** Build `src/lib/install-project.js` and wire it into `src/commands/init.js`. This subsumes everything `install.sh` does *except* the skills mirror — copies `.claude/conventions/`, `.claude/hooks/` (with chmod +x), the project-relative `.claude/settings.json` (only if absent), all `templates/` seeds (insights, wiki, raw, deliverables, sources, data_sources, methods, project_conventions), `CLAUDE.md` (only if absent), and emits the corrected `.gitignore` block (without the obsolete skills/agents negation entries).

**Modifies/Adds.** `src/lib/install-project.js` ✚, `src/commands/init.js` ✎ (replace stub).

**Verification.**
- Run `scr init` against a fresh tmpdir. Resulting layout matches what `install.sh` produces for the project-level pieces (modulo skills, which Phase 3 handles): same files in `.claude/conventions/`, `.claude/hooks/`, same settings.json, same template-seeded folders, same CLAUDE.md, same `.gitignore` block (minus the now-obsolete `.claude/skills/` and `.claude/agents/` negation entries).
- Re-running `scr init` is idempotent: existing files are preserved, console output reflects "exists, skipping".
- Hooks are executable (`stat -f '%Lp' .claude/hooks/check-insights.sh` returns a mode with the execute bit).
- Running `scr init` against the *framework repo itself* refuses or no-ops cleanly (the framework repo is not a target — guard via the presence of `package.json` with `name: "super-claudio-research"`, or just docs).

### Phase 3 — Global skills/agents symlink + gitignore cleanup

**Intent.** Build `src/lib/install-globals.js` by porting `super-claudio-code/src/commands/init.js:128-217` near-verbatim (point `skillsSource`/`agentsSource` at this package's `.claude/skills/` and `.claude/agents/`). Wire it into `src/commands/init.js` so `scr init` runs project-level then global. Confirm the gitignore block emitted in Phase 2 already handles the global shift (skills/agents are no longer in the project tree, so no negation needed for them).

**Modifies/Adds.** `src/lib/install-globals.js` ✚, `src/commands/init.js` ✎.

**Verification.**
- After `scr init` in a tmpdir: `~/.claude/skills/{verify,deliverable-review,wiki-ingest,wiki-lint,scan-sources,research-cleanup}` are all symlinks pointing into `super-claudio-research/.claude/skills/`. `~/.claude/agents/` exists (empty, since `agents/` is currently empty in the framework repo, but the dir is created).
- Re-running `scr init` is a no-op for symlinks already pointing to the right place.
- Skill name disjointness vs scc-code: `comm -12 <(ls ~/github/super-claudio-research/.claude/skills) <(ls ~/github/super-claudio-code/skills) | wc -l` returns `0`.
- Claude Code recognizes the symlinked skills (manual check: `/verify` and `/deliverable-review` show up in the slash-command list in a fresh project).
- A target project's `.gitignore` block does not contain `!.claude/skills/` or `!.claude/agents/` entries (these are now obsolete since skills/agents live globally).

### Phase 4 — Upgrade flow, README rewrite, install.sh deletion

**Intent.** Build `src/lib/upgrade.js` and wire `--upgrade` into `scr init`. Behavior: for each file under `.claude/conventions/` and `templates/` (excluding `templates/CLAUDE.md.template`, which the user customizes immediately on install), compare framework version vs project version. If absent in project: copy in. If byte-identical: skip silently. If divergent: write `<file>.framework-new` sidecar, append the file path to a tally. At end of `--upgrade`, print a one-line summary: "N files have framework-new sidecars; review with `git diff` or your editor". Then: rewrite README's Quickstart (point at `npm install -g github:...` + `scr init`), document `scr init --upgrade` + the `cp -R` recipe for project→project convention copying, strip the Roadmap section. Create `TODO.md` at framework root with the moved roadmap items + the new "globalize conventions" entry. Delete `install.sh`.

**Modifies/Adds.** `src/lib/upgrade.js` ✚, `src/commands/init.js` ✎ (add `--upgrade` flag handling), `README.md` ✎, `TODO.md` ✚, `install.sh` ✘.

**Verification.**
- Run `scr init` in tmpdir A. Edit one convention file in tmpdir A. Run `scr init --upgrade` in tmpdir A — verify the edited file gets a `.framework-new` sidecar and is not overwritten; verify unchanged files print no output.
- Run `scr init --upgrade` against a tmpdir that previously ran an old `install.sh` (simulate by manually creating an old-shape `.claude/skills/` dir in the project) — verify the warning about removing the obsolete project-local skills directory prints, and the directory is not auto-deleted.
- `--upgrade` does not touch `CLAUDE.md` (user-customized) or scaffolding folders' content (insights/INDEX.md, etc.) — only `.claude/conventions/` and pure template seeds.
- README's Quickstart is the ~5-line one-liner sequence; "Roadmap" section is gone.
- `TODO.md` exists at framework root; contains the v1.1+ items previously in README + a new entry: "globalize conventions (without conflicting with Claude's defaults) — let researchers share one set of conventions across multiple project repos. Open question: how does this interact with project-shared `.claude/conventions/` (README principle 4)?"
- `install.sh` no longer exists in the framework repo.
- `git grep "install.sh"` returns 0 hits in source-of-truth files (README, plan/, brainstorms/, docs/, .claude/, templates/) — i.e., no broken references after deletion. (Hits inside `plan/plan-v1-framework/` historical content are acceptable; scope to current docs.)

## Phase Order + Dependencies

```
Phase 1 (bootstrap)  ─→  Phase 2 (per-project)  ─→  Phase 3 (globals)  ─→  Phase 4 (upgrade + cleanup)
```

Strictly sequential. No parallelism — each phase depends on the previous. Phase 4 is the only phase that touches user-facing surfaces (README, install.sh deletion); deferring it keeps the bisection window clean if any earlier phase regresses.

## Open Items Deferred

- **Publishing to the npm registry** (vs. install via GitHub URL). Defer until v1 of the framework is stable enough to want a non-rolling release channel. `npm install -g github:andresfortunato/super-claudio-research` is sufficient for the May 2026 kickoff.
- **`scr status` / `scr plan init` / `scr learning list`** (parallel to scc commands). Defer; super-claudio-research's plans are already manually maintained and the existing pattern works. Revisit if cross-skill status tracking becomes load-bearing.
- **Hash-based install-manifest** for `--upgrade` (option (c) from the brainstorm). Sidecar-only is the v1 answer. Revisit if researchers report sidecar fatigue.
- **Globalizing conventions** to `~/.claude/conventions/` so a researcher's workflow conventions follow them across multiple project repos. Lands on `TODO.md` (Phase 4). Open design question: how does this interact with collaborators cloning a project repo who don't have `scr` installed — the project's `CLAUDE.md` would `@`-reference paths that don't exist for them. Punt until at least one researcher reports actually wanting this.
- **Migration helper command** (`scr migrate` to clean up old-install layouts). Punt — population is small enough that a one-line warning + manual `rm -rf .claude/skills/` suffices.
- **Plugin distribution via `.claude-plugin/`** (Claude Code's plugin model). super-claudio-code's `package.json` already lists `.claude-plugin/` in `files`, suggesting a future direction. Out of scope here; revisit once the plugin model is more stable.

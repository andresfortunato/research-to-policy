# Install redesign — Brainstorming Summary

## Problem

The current `install.sh` has three concrete flaws:

1. **Hidden prerequisite step.** README pretends `bash install.sh .` is a one-liner, but it requires the user to first manually clone the framework repo and remember its path.
2. **Skills are duplicated per project, not shared.** Each project gets its own copy of `.claude/skills/{verify,deliverable-review,wiki-ingest,...}`. Updating skills means re-running install in every project.
3. **Updates are silently broken inside existing skill dirs.** `install.sh:29-40` (`copy_if_absent`) skips any destination that already exists. Once `verify/` exists in a project, no new files added inside it ever reach that project.

Sibling repo `super-claudio-code` already solved this — distributed via `npm install -g`, exposes an `scc` CLI, symlinks skills/agents globally to `~/.claude/`, copies project-level scaffolding per-project. We mirror that pattern.

## Decisions Made

- **Distribution**: drop `install.sh`. Publish as a Node package installable via `npm install -g github:andresfortunato/super-claudio-research`. User gets the `scr` CLI globally — no manual cloning. *Rejected: a self-bootstrapping bash script (`curl | bash`) — security smell, less standard than npm, and the user already has Node for Claude Code so the dep cost is zero.*
- **CLI binary name: `scr`**. Two letters, parallels `scc`, no obvious conflict, easy to type frequently. *Rejected: `claudio-research`, `screc` — more typing or less obvious.*
- **Global vs per-project split** (the load-bearing decision):
  - **Global** (symlinked to `~/.claude/`): `skills/`, `agents/`. These have no project-specific paths — symlinking gives one source of truth and free updates via `npm update -g`.
  - **Per-project** (copied by `scr init`, committed to the project repo): `.claude/conventions/`, `.claude/hooks/`, `.claude/settings.json`, scaffolding folders (`insights/`, `wiki/`, `raw/`, `deliverables/`, `sources/`, `data_sources/`, `methods/`, `project_conventions/`), `CLAUDE.md`, `.gitignore` block. Settings.json references hooks via relative paths, and README principle 4 wants conventions committed so collaborators inherit them. *Rejected: globalizing conventions too — would mean a teammate cloning the project repo without `scr` installed sees a broken `CLAUDE.md`. Revisit once a "scr is required to read this repo" stance is acceptable.*
- **Convention sync mechanism = both flavors (B3)**:
  - `scr init --upgrade` re-pulls conventions from the framework into the current project, with diff prompts on files that diverge. Source of truth: the framework repo. Use case: pick up framework updates.
  - Documented `cp -R` recipe in README for project→project convention copying. Source of truth: any project. Use case: a researcher developed a tweak in project A and wants it in project B without round-tripping through the framework. *Cost is near-zero to ship both; they serve different real cases.*
- **Project-development todo list moves out of README** into its own file in the framework repo. README stays focused on the user-facing quickstart. The "Roadmap" section currently at `README.md:174-186` moves there. New item lands on it: "globalize conventions (without conflicting with Claude's defaults) for researchers wanting workflow consistency across repos."

## Research Findings

- `super-claudio-code/src/commands/init.js:128-217` — reference implementation of the global symlink pattern for skills (`~/.claude/skills/`) and agents (`~/.claude/agents/`). Idempotent: detects existing correct symlinks and skips, removes stale symlinks, refuses to overwrite real files. Worth porting wholesale.
- `super-claudio-code/install.js:1-46` — npm post-install entry point that resolves the project root and delegates to `init`. Pattern to copy.
- `super-claudio-code/package.json` — uses `commander@^13.1.0`, `"type": "module"`, `"engines": { "node": ">=18.0.0" }`, declares `"bin": { "scc": "./src/cli.js" }`. Same shape for super-claudio-research.

## Open Questions

- **Update model for conventions/templates with user edits.** `scr init --upgrade` needs a diff-and-prompt flow when a project's `.claude/conventions/<file>.md` has diverged from the framework's version. Three sub-options for planning to decide: (a) print diff and prompt y/n per file; (b) write `.framework-new` sidecar files for the user to merge; (c) only touch files unchanged from the original install (track via hash). Planning should pick.
- **Hook merging when `settings.json` already exists.** Current `install.sh` punts ("merge new hook entries manually"). scc-code has a more elaborate merger. For v1 there's only one hook (`check-insights.sh`), so a simple "if `settings.json` exists, append a hook entry only if it's missing" is probably enough — but planning should confirm.
- **Migration path for existing super-claudio-research projects** that already ran the old `install.sh`. Are there any in the wild yet? If yes, `scr init` needs to detect the old layout and clean up duplicated skills (or leave them and let the user `rm -rf .claude/skills/`).
- **Where does the project-development todo list live?** `TODO.md` at repo root vs `docs/roadmap.md`. Minor — planning picks.

## Constraints Identified

- **Idempotency is non-negotiable.** Both `scr init` and `scr init --upgrade` must be safe to re-run. Real files never get overwritten without a prompt; symlinks get refreshed when stale.
- **`.gitignore` block must continue to share `.claude/conventions/`, `.claude/hooks/`, `.claude/skills/`, `.claude/settings.json` while hiding `plan/`, `brainstorms/`, `.scc/`.** This is load-bearing for principle 4. (Note: with skills going global, `.claude/skills/` no longer needs to be committed in target projects — adjust the gitignore block accordingly.)
- **No hard external deps beyond Node ≥18 and `commander`.** Stay minimal, mirror scc-code's footprint.
- **The CLI must work whether the package was installed via `npm install -g github:...` or cloned and `npm link`-ed.** Standard for Node bin packages — just don't hard-code paths.

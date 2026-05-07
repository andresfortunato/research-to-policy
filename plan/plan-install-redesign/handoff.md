# Handoff — install-redesign

## Status

**Phase 1: ✅ done.** Node package skeleton bootstrapped. `scr` binary works via `npm link`. Phase 2 next.

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Bootstrap the Node package | ✅ done | package.json + install.js + src/cli.js + stubbed src/commands/init.js + .gitignore. Verified via `npm link`. |
| 2 | Per-project install (port install.sh) | ⏳ next | `src/lib/install-project.js` + wire into `src/commands/init.js` |
| 3 | Global skills/agents symlink | ⏳ pending | `src/lib/install-globals.js` (port from scc-code) |
| 4 | Upgrade flow + README + delete install.sh | ⏳ pending | `src/lib/upgrade.js`, README rewrite, TODO.md, delete install.sh |

## Read Order

1. This file
2. `plan.md` — full plan (goal, constraints, decisions, file manifest, phases, dependencies)
3. `brainstorms/install-redesign.md` — decision rationale (do not re-debate)
4. Reference: `~/github/super-claudio-code/{install.js,src/cli.js,src/commands/init.js}` — port targets

## Start At

**Phase 2 — Per-project install.** Build `src/lib/install-project.js`. Subsumes everything `install.sh` does *except* the skills/agents symlinks (Phase 3 owns those).

Port the four logical sections of `install.sh`:
1. Mirror `.claude/conventions/` and `.claude/hooks/` from framework→project (with `chmod +x` on hooks). Skills directory mirroring goes away — Phase 3 handles that via symlinks.
2. Ensure `.claude/settings.json` exists from `.claude/settings.template.json` (only if absent).
3. Mirror `templates/` seed dirs (`insights/`, `wiki/`, `raw/`, `deliverables/`, `sources/`, `data_sources/`, `methods/`, `project_conventions/`) into project root, plus `CLAUDE.md` (only if absent).
4. Append the corrected `.gitignore` block — **no `!.claude/skills/` or `!.claude/agents/` negation entries** (these are obsolete now that skills/agents live globally).

Then wire it into `src/commands/init.js` (replace the stub).

## Key Constraints

- All decisions in `brainstorms/install-redesign.md` are settled. Don't re-debate.
- The framework repo is **not** a target project — `scr init` is for *target research projects*. Don't pollute super-claudio-research itself with `insights/`, `wiki/`, etc. seeds when testing. Use `/tmp/test-*` dirs.
- `scr` and `scc` must coexist; both target `~/.claude/{skills,agents}/`. No skill-name conflicts today (verified in plan); guard against future ones in Phase 3 verification.
- Idempotency is non-negotiable for both `scr init` and `scr init --upgrade`. Real files never get overwritten without explicit signal.
- Phases are strictly sequential — each blocks the next. No parallelism opportunities.

## Open Decisions

None.

## Surprises (Phase 1)

- **Node 24 in use locally.** `which scr` resolved to `/Users/anf191/.nvm/versions/node/v24.15.0/bin/scr`. The `engines.node >= 18` constraint in package.json is satisfied; just noting the runtime so future-Phase verification doesn't get confused if it sees Node 24 paths in `which scr` output.
- **`scc` already has `scr` colocated as siblings under `~/.nvm/.../bin/`.** No collision — `scc` and `scr` are distinct binaries in the same npm-global bin dir. The two packages coexist exactly as the plan predicted.
- **`package-lock.json` is committed in scc-code**, so we mirror that and commit it here too. Already-present in `git status` as untracked.

## What didn't work

Nothing this phase — the bootstrap was a near-mechanical mirror of scc-code's shape.

## Verification log (Phase 1)

- `npm install` — pulled commander@13.x; 0 vulnerabilities.
- `npm link` — registered `scr` globally. `which scr` → `~/.nvm/versions/node/v24.15.0/bin/scr`.
- `scr --help` — commander-formatted output; lists `init` command.
- `scr init` — prints `scr init: not implemented yet (Phase 1 stub)` and exits 0.
- `scr init --upgrade` — prints `scr init --upgrade: not implemented yet (Phase 1 stub)` and exits 0. (Confirms `--upgrade` flag wires through.)
- `scr init --help` — lists `--upgrade` option with description.
- `git check-ignore -v node_modules/` — confirms `.gitignore:2:node_modules/` matches.
- Re-run `npm link` — `up to date, audited 3 packages` (idempotent).

## Files added/modified (Phase 1)

- ✚ `package.json` — name, version 0.1.0, type:module, bin:scr, dep:commander@^13.1.0, engines.node>=18.0.0
- ✚ `install.js` — npm postinstall entry, port of scc-code/install.js
- ✚ `src/cli.js` — commander entry, registers `scr init [--upgrade]`
- ✚ `src/commands/init.js` — Phase 1 stub
- ✚ `package-lock.json` — npm lock (committed, mirrors scc-code practice)
- ✎ `.gitignore` — added `node_modules/`

## Hash trail

- Phase 1 work: `e21f592`
- Handoff hash-trail fill-in: (this commit)

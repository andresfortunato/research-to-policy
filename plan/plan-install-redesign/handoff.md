# Handoff — install-redesign

## Status

**Phase 3: ✅ done.** `src/lib/install-globals.js` symlinks the framework's `.claude/skills/` and `.claude/agents/` subdirs into `~/.claude/{skills,agents}/`. Wired into `src/commands/init.js` to run *after* `installProject`. `scr init` now produces a complete install: per-project layout + global skill availability across all Claude Code projects. Phase 4 (upgrade flow + README rewrite + delete install.sh) next.

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Bootstrap the Node package | ✅ done | package.json + install.js + src/cli.js + stubbed src/commands/init.js + .gitignore. Verified via `npm link`. |
| 2 | Per-project install (port install.sh) | ✅ done | `src/lib/install-project.js` + wired into `src/commands/init.js`. Diff vs `install.sh` output is exactly the two intended deltas. |
| 3 | Global skills/agents symlink | ✅ done | `src/lib/install-globals.js` ports scc-code's `installSkills()`/`installAgents()` near-verbatim with sources at `<framework>/.claude/{skills,agents}/`. 6 skills symlink into `~/.claude/skills/` on first run; idempotent re-runs report "already installed". Skill-name disjointness vs scc-code re-verified (`comm -12` empty). |
| 4 | Upgrade flow + README + delete install.sh | ⏳ next | `src/lib/upgrade.js`, README rewrite, TODO.md, delete install.sh |

## Read Order

1. This file
2. `plan.md` — full plan (goal, constraints, decisions, file manifest, phases, dependencies)
3. `brainstorms/install-redesign.md` — decision rationale (do not re-debate)
4. Reference for Phase 4: `plan.md` Phase 4 section + plan.md "Decisions resolved during planning" (sidecar-based `--upgrade`, `TODO.md` at framework root, the warning-only migration path)

## Start At

**Phase 4 — Upgrade flow, README rewrite, install.sh deletion.** Concrete deliverables:

1. **`src/lib/upgrade.js`** — for each file under framework's `.claude/conventions/` and `templates/` (excluding `templates/CLAUDE.md.template`):
   - If absent in project → copy in.
   - If byte-identical → silent skip.
   - If divergent → write `<file>.framework-new` sidecar (don't overwrite), tally the path.
   - At end: print one-line summary `"N files have framework-new sidecars; review with git diff or your editor"` (or `"No upgrades needed"` if N=0).
   - Also: detect old-shape `<project>/.claude/skills/` directory and print one-line warning recommending `rm -rf .claude/skills/` (don't auto-delete).

2. **`src/commands/init.js`** — replace the `--upgrade` stub with `import { upgradeProject } from '../lib/upgrade.js'` + delegate.

3. **`README.md`** — rewrite Quickstart (`README.md:74-82`) to point at `npm install -g github:andresfortunato/super-claudio-research` + `scr init`. Document `scr init --upgrade` and the project→project `cp -R` recipe. Strip the "Roadmap" section (`README.md:174-186`).

4. **`TODO.md`** at framework root — moved roadmap items + new entry: *"globalize conventions (without conflicting with Claude's defaults) — let researchers share one set of conventions across multiple project repos. Open question: how does this interact with project-shared `.claude/conventions/` (README principle 4)?"*

5. **Delete `install.sh`.** Then `git grep "install.sh"` should return 0 hits in current docs (README, current plan/, .claude/, templates/). Hits inside `plan/plan-v1-framework/` historical content are acceptable.

**Verification (full list in `plan.md` Phase 4 section).**
- Edit a convention file in a tmpdir, run `scr init --upgrade` → sidecar appears, original untouched.
- Manually create `.claude/skills/` in a tmpdir, run `scr init --upgrade` → warning prints, dir not deleted.
- `--upgrade` does not touch `CLAUDE.md` or scaffolding folder content.
- README's Quickstart is ~5 lines; "Roadmap" gone; `TODO.md` exists.
- `git grep install.sh` returns 0 hits in current docs.

## Key Constraints

- All decisions in `brainstorms/install-redesign.md` are settled. Don't re-debate.
- The framework repo is **not** a target project — `scr init` is for *target research projects*. Verified guard works (refuses cleanly when `package.json.name === "super-claudio-research"`). Use `/tmp/test-*` dirs for testing.
- `scr` and `scc` coexist; both target `~/.claude/{skills,agents}/`. Phase 3 re-confirmed: zero skill-name overlap.
- Idempotency is non-negotiable for both `scr init` and `scr init --upgrade`. Real files never get overwritten without explicit signal — sidecars only.
- Sidecar approach is the v1 answer. Don't reach for hash-based install-manifests or interactive prompts (rejected during planning).
- Phases are strictly sequential — each blocks the next. No parallelism opportunities.

## Open Decisions

None.

## Surprises (Phase 3)

- **`installAgents` source path.** scc-code's `installAgents()` reads `agentsSource = resolve(__dirname, '../../agents')` — that's `<package-root>/agents/`. The research framework keeps agents under `.claude/agents/`, matching where skills live, so the source path here is `<framework>/.claude/agents/`. Same correction applies to `installSkills` (already noted in handoff).
- **Empty agents directory is fine.** `<framework>/.claude/agents/` exists but contains zero `*.md` files. The loop's filter `e.isFile() && e.name.endsWith('.md')` returns empty, `installed` stays at 0, and the helper prints `"agents already installed or none to install"` — slightly tweaked from scc-code's `"agents already installed"` message to cover the empty-source case clearly. `~/.claude/agents/` itself is `mkdir -p`'d, so the dir exists for future agent additions.
- **Idempotency depends on `readlink === source` exact-string match.** The helper detects existing-correct symlinks by comparing `readlink(target)` against the absolute `source` string. If a researcher had previously symlinked these via a different absolute path (e.g., a `~`-expansion that resolved differently, or a relative link), the `existing === source` check would miss, `unlink` would run, and a fresh symlink would replace it — still correct, just one extra operation. Worth knowing if upgrade verification ever shows symlink churn on no-op runs.
- **scc-code skill source is `skills/`, ours is `.claude/skills/`.** Already documented in the previous handoff but worth reiterating: anyone reading the two implementations side-by-side will see the path divergence. It's intentional — the research framework keeps Claude assets under `.claude/` consistently; scc-code hoisted `skills/` to package root.

## What didn't work

Nothing this phase. Mechanical port of scc-code's two helpers; only changes were the source-path corrections and a slightly more accurate empty-agents log message.

## Verification log (Phase 3)

- **Fresh install** — `rm -rf /tmp/test-scr-phase3 && mkdir /tmp/test-scr-phase3 && cd /tmp/test-scr-phase3 && scr init`. Per-project layout matched Phase 2 output (33 `+` lines). Then global section printed `Installing global skills/agents to ~/.claude/`, followed by `✓ ~/.claude/skills/ (6 skills linked)` and `· ~/.claude/agents/ (agents already installed or none to install)`.
- **Symlink targets** — `ls -la ~/.claude/skills/ | grep -E "(verify|deliverable-review|wiki-ingest|wiki-lint|scan-sources|research-cleanup)"` shows all 6 as `lrwxr-xr-x` symlinks pointing to `/Users/anf191/github/super-claudio-research/.claude/skills/<name>`.
- **Agents dir created (empty)** — `ls -la ~/.claude/agents/` shows the dir exists with 0 `*.md` entries.
- **Idempotency** — re-ran `scr init` in the same `/tmp/test-scr-phase3`. Per-project section all `~ ... (exists, ...)`; global section now `· ~/.claude/skills/ (skills already installed)` and `· ~/.claude/agents/ (agents already installed or none to install)`. No symlink churn (none recreated).
- **Skill-name disjointness vs scc-code** — `comm -12 <(ls /Users/anf191/github/super-claudio-research/.claude/skills | sort) <(ls /Users/anf191/github/super-claudio-code/skills | sort)` returns empty.
- **Framework-repo guard** — `cd /Users/anf191/github/super-claudio-research && scr init` prints "Refusing to run scr init against the framework repo itself." and exits without doing any work. Post-run `git status --short` shows only the intended Phase 3 file changes (`src/commands/init.js`, `src/lib/install-globals.js`) plus pre-existing `.completed` markers from other plans.
- **Gitignore content unchanged from Phase 2** — `grep -E "skills|agents" /tmp/test-scr-phase3/.gitignore` returns no hits. The Phase 2 gitignore block already omits the obsolete negation entries.

## Files added/modified (Phase 3)

- ✚ `src/lib/install-globals.js` — port of scc-code's `installSkills()` + `installAgents()`. Source paths point at `<framework>/.claude/{skills,agents}/`. Exports a single `installGlobals()` that wraps both.
- ✎ `src/commands/init.js` — added `import { installGlobals }`; calls `installGlobals()` after `installProject()` succeeds, before `printNextSteps()`.

## Hash trail

- Phase 1 work: `e21f592`
- Handoff hash-trail fill-in for Phase 1: `3bf0476`
- Phase 2 work + handoff refresh: `9f0d3fc`
- Handoff hash-trail fill-in for Phase 2: `63563b0`
- Phase 3 work + handoff refresh: `e2b84e1`
- Handoff hash-trail fill-in for Phase 3: (this commit)

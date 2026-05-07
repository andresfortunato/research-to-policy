# Handoff — install-redesign

## Status

**Phase 2: ✅ done.** `src/lib/install-project.js` ports the project-level work of `install.sh` (skills mirror dropped — Phase 3 handles globals). `scr init` now produces a working target-project layout end-to-end. Phase 3 next.

| Phase | Title | Status | Notes |
|---|---|---|---|
| 1 | Bootstrap the Node package | ✅ done | package.json + install.js + src/cli.js + stubbed src/commands/init.js + .gitignore. Verified via `npm link`. |
| 2 | Per-project install (port install.sh) | ✅ done | `src/lib/install-project.js` + wired into `src/commands/init.js`. Diff vs `install.sh` output is exactly the two intended deltas (no skills mirror, no skills negation in .gitignore). |
| 3 | Global skills/agents symlink | ⏳ next | `src/lib/install-globals.js` (port from scc-code). Wire into `src/commands/init.js` after `installProject`. |
| 4 | Upgrade flow + README + delete install.sh | ⏳ pending | `src/lib/upgrade.js`, README rewrite, TODO.md, delete install.sh |

## Read Order

1. This file
2. `plan.md` — full plan (goal, constraints, decisions, file manifest, phases, dependencies)
3. `brainstorms/install-redesign.md` — decision rationale (do not re-debate)
4. Reference: `~/github/super-claudio-code/src/commands/init.js:128-217` — `installSkills()` + `installAgents()` to port near-verbatim

## Start At

**Phase 3 — Global skills/agents symlinks.** Build `src/lib/install-globals.js` as a near-verbatim port of `super-claudio-code/src/commands/init.js:128-217`:

- `installSkills()` — symlink each subdir of `<framework>/.claude/skills/` into `~/.claude/skills/`. Detect existing correct symlinks (no-op), remove stale ones, refuse to overwrite real files. Source path is `<framework>/.claude/skills/` (NOT `<framework>/skills/` like scc-code — the research framework keeps skills under `.claude/`).
- `installAgents()` — same pattern for `~/.claude/agents/`. Source: `<framework>/.claude/agents/`. Currently empty in the research framework, so the loop will just `mkdir -p` the target and exit cleanly.

Wire it into `src/commands/init.js` to run *after* `installProject` (project install first, globals second). The order matches scc-code.

## Key Constraints

- All decisions in `brainstorms/install-redesign.md` are settled. Don't re-debate.
- The framework repo is **not** a target project — `scr init` is for *target research projects*. Verified guard works (refuses cleanly when `package.json.name === "super-claudio-research"`). Use `/tmp/test-*` dirs for testing.
- `scr` and `scc` must coexist; both target `~/.claude/{skills,agents}/`. No skill-name conflicts today (`brainstorms/install-redesign.md` verified disjoint sets); Phase 3 verification re-checks.
- Idempotency is non-negotiable for both `scr init` and `scr init --upgrade`. Real files never get overwritten without explicit signal.
- Phases are strictly sequential — each blocks the next. No parallelism opportunities.

## Open Decisions

None.

## Surprises (Phase 2)

- **`copy_if_absent` semantics on directories.** `install.sh` treats a directory as "exists" once it's present, so `mirror_dir` recurses one level deep but `copy_if_absent` on a *child directory* (like `deliverables/country-diagnostic-memo/`) does a full `cp -R`. Ported faithfully via `copyDirRecursive` in the Node version. Verified by `diff -rq` against bash output: nested deliverable subdirs (`PROFILE.md`, `template.md` inside each) match.
- **`relative()` for log paths.** `install.sh` `cd`'s into `$TARGET` and prints relative paths. Mirrored that with `path.relative(target, dst)` for log output rather than mutating `process.cwd()` from inside a library function.
- **Settings template.json path is `.claude/settings.template.json`** (not `.claude/settings.json.template` or similar). Matches `install.sh:66`.
- **Diff vs `install.sh` output reduces to exactly two intended deltas** — `Only in /tmp/test-scr-bash/.claude: skills` and `!.claude/skills/{,**}` lines absent from `.gitignore`. Both are the explicit Phase 2 plan deltas.

## What didn't work

Nothing this phase. The structural mapping from `install.sh` shell idioms to Node `fs/promises` was mechanical: `cp -R` → `copyDirRecursive`, `mkdir -p` → `mkdir({recursive: true})`, `chmod +x` → `chmod(0o755)`, heredoc gitignore block → tagged template literal.

## Verification log (Phase 2)

- **Fresh install** — `rm -rf /tmp/test-scr-phase2 && mkdir /tmp/test-scr-phase2 && cd /tmp/test-scr-phase2 && scr init`. Output: 33 `+` lines (10 conventions + 1 hook + 1 settings + scaffolding + sources/seen.jsonl + CLAUDE.md + .gitignore). All expected.
- **Idempotency** — re-ran `scr init` in the same `/tmp/test-scr-phase2`. All 33 lines now `~ ... (exists, skipping)` or `~ ... (exists, leaving as-is)` for sources/seen.jsonl and `~ ... (exists — merge new hook entries manually if needed)` for settings.json. No file overwrites.
- **Hook executability** — `stat -f '%Lp %N' /tmp/test-scr-phase2/.claude/hooks/*.sh` → `755 .../check-insights.sh`. Execute bit set as required.
- **Framework-repo guard** — `cd /Users/anf191/github/super-claudio-research && scr init` prints "Refusing to run scr init against the framework repo itself." and exits without doing any work. Confirmed via post-run `git status --short`: only the intended Phase 2 file changes (`src/commands/init.js`, `src/lib/`) — no `insights/`, `wiki/`, `raw/`, etc. seeded into the framework repo.
- **Bash-vs-Node parity** — `diff -rq /tmp/test-scr-phase2 /tmp/test-scr-bash` (where the bash dir was produced by `bash install.sh /tmp/test-scr-bash`). Output: `Only in /tmp/test-scr-bash/.claude: skills` and `Files .../.gitignore differ`. The gitignore diff is exactly two lines (`!.claude/skills/` + `!.claude/skills/**`), matching the Phase 2 plan delta.
- **Gitignore block content** — `cat /tmp/test-scr-phase2/.gitignore` confirms: no `!.claude/skills/` or `!.claude/agents/` negation entries.

## Files added/modified (Phase 2)

- ✚ `src/lib/install-project.js` — port of install.sh sections 1-6 (skills mirror dropped). Exports `installProject(target)` and `printNextSteps()`.
- ✎ `src/commands/init.js` — replaced Phase 1 stub with `installProject(process.cwd())` + `printNextSteps()`. `--upgrade` still stubbed (Phase 4).

## Hash trail

- Phase 1 work: `e21f592`
- Handoff hash-trail fill-in for Phase 1: `3bf0476`
- Phase 2 work + handoff refresh: (this commit)

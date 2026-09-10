# A migration is not done when it runs — later merges reintroduce the paths it removed, so link checking has to be a standing job, not a one-shot script

**Encoded in:** `docs/v1-to-v2-migration.md` § After the run; `templates/migration/README` header

**Discovered:** 2026-09-09, auditing the pilot 13 months after its v1→v2 migration.

## What

The v1→v2 migration shipped `templates/migration/02_repath.py` (rewrites dead v1
directory names) and `03_linkcheck.py` (reports what no longer resolves). Both
ran. Both were verified green at the time.

Thirteen months later the pilot carries **380 markdown files referencing
directories that no longer exist**:

```
decisions/  223 files
learnings/  157 files
insights/    32 files
```

None of the three has existed since v2 merged them into `research/methods/`.

## Why it bites

A repath pass is a **point-in-time** operation over the branches that exist when
it runs. It cannot see:

- **branches not checked out**, which merge later carrying the old paths;
- **branches created before the migration and merged after it**, which is the
  common case on a six-month engagement running ~13 branches across ~10
  worktrees;
- **anything a human writes afterwards from muscle memory**, or by copying an
  older doc as a template.

Each of those reintroduces exactly what the migration removed, and nothing
errors. A dead directory reference produces no symptom at all: the session simply
does not find what it was told to read, and concludes the thing is undocumented.
It is the same invisible-by-construction defect class as a dangling doc pointer,
which is why r2p's invariant 15 exists — but invariant 15 is deliberately scoped
to framework-owned files, and these 380 are researcher-authored.

## The rule

1. **Re-run the repath after the last merge, not after the first.** A migration's
   "done" condition is *no branch still open predates it*, not *the script exited
   zero*. If branches are still open, schedule a second pass.
2. **Link checking is a standing invariant, not a migration step.**
   `03_linkcheck.py --baseline HEAD` is designed to run repeatedly and reports
   `new breaks` against a baseline precisely so it can. Run it on merges, not
   only on migrations.
3. **Repath the instruction, not just the reference.** Related, and already
   recorded in `docs/v2-to-v3.md`: in three of four cases examined, a dangling
   pointer had a live v1 *instruction* underneath it. Fixing the pointer alone
   leaves an instruction that now succeeds at producing the wrong layout, which
   fails silently where a dangling reference fails visibly.

## What this is not

It is **not** an argument for adding a project-wide link invariant to
`lint-research.sh`. That was measured and rejected: a first pass scanning
everything reported 22 findings on the pilot, most of them the researcher's own
prose citing their own notes. Those are broken links in somebody's writing — a
different check with a different population, and mixing them in is how a WARN
tier trains people to ignore it. The fix is a migration discipline, not a wider
grep.

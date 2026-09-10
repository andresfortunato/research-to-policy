# v3 assessment — r2p measured on the Córdoba engagement

**Measured:** 2026-09-09, in `~/research/cordoba` at `main`.
**Acted on:** v3.1, 2026-09-10. Every change below is in the repo; this document
is the evidence they were admissible under `docs/extending.md` step 2's rule
that *the defect actually happened*.

Córdoba is r2p's largest and longest-running instance: **285 evidence docs, 194
method + source docs, 48 claims, 36 plan directories, ~6 months.** Everything
here is measured on that corpus, not inferred. It is the successor to
`docs/v2-case-study-cordoba.md`, which drove v2 and v3.

**Re-measure before citing any number here.** A baseline against a live
engagement decays in weeks, and the pilot is a *mixed* v1/v2 install — a good
donor for lint work, a bad model of a clean project.

---

## 1. The four questions

| Question | Verdict |
|---|---|
| Too much load-bearing context per session? | **No — the fixed floor is fine (~5,300 tok)** and should not be cut. The cost was in two *variable* layers: a per-prompt injection hook (~3,000–3,500 tok every time it fired) and an orientation read linear in work done (~57,500 tok). |
| Referencing irrelevant information? | **Yes, badly, and mechanically.** Two independent causes, both on the push side. |
| Too confusing? | **Yes, but locally.** Confusion concentrated in *merge scars*, not in the framework's concepts. |
| Works for long-running projects? | **Yes for six months of normal work — 5% evidence-orphan rate. No across a structural migration — 88%.** One consolidation broke the record's connective tissue and nothing detected it. |

## 2. The thesis: hooks may enforce, hooks may not inject

Sorting every r2p mechanism by whether it *checks* or *injects*:

| Mechanism | Kind | After six months |
|---|---|---|
| `evidence/INDEX.md` 120-char headline cap | check | **285/285 compliant**, max exactly 120 |
| `lint-type-scale.sh`, `lint-chart-titles.sh` (project-local) | check | holding |
| Stop-hook nudges | check | holding |
| `sources/INDEX.md` cap — prose only, no check | none | 40% of cells over 120, one at 1,759 |
| `triggers:` "4–8 keywords" — prose only, no check | none | mean 12.5, 63% over guidance |
| `UserPromptSubmit` → `retrieve-learnings.sh` | **inject** | fired on the words `no` and `a` |
| a `SessionStart` status document | **inject** | froze for 41 days, 3 dead pointers |

**Every enforced constraint survived. Every injection channel degraded. Every
unchecked prose rule drifted.** → Principle 1's 2026-09-10 revision.

## 3. Measurements

### 3.1 Context load

| Layer | Tokens |
|---|---|
| `CLAUDE.md` | 2,565 |
| project auto-memory index (30 entries) | 1,411 |
| SessionStart status injection | 1,328 |
| **Fixed floor** | **~5,300** |

The orientation read, linear in work done:

```
research/claims.md            41,565 B   ~11,234 tok
research/evidence/INDEX.md    68,215 B   ~18,436 tok
research/sources/INDEX.md     96,791 B   ~26,160 tok
research/methods/INDEX.md      6,242 B    ~1,687 tok
                                        ~57,517 tok
```

`evidence/INDEX.md` is **expensive but blameless**: 285 rows, mean headline 102
chars, max exactly 120, zero violations. That is the capped index working as
designed, and its cost is the honest price of 285 findings.
`sources/INDEX.md` is the outlier: no cap, 40% of cells over 120, longest 1,759,
a 48 KB "Quick navigation" table, and **six overlapping listings of the same 130
sources** — three named after the migrations that created them — with 62 of 142
entries appearing more than once. → invariant 20 and the `sources.md` contract.

Per-prompt injection: replayed on six realistic prompts, two fired, at
**10,997 B (~2,972 tok)** and **12,899 B (~3,486 tok)**. At a ~33% fire rate over
a 40-turn session that is **~41,000 tokens** — eight times the entire fixed
floor, recurring, with the same doc re-injectable many times.

### 3.2 Irrelevant references

**Cause A — a bag-of-words hit counter with no stopword list.** Asked to
*evaluate the framework*, the hook injected two source docs; the matching
keywords were `1` and `general`. On the next message it injected 13.4 KB; the
matching keywords were `no` and `a`. Across 94 docs with trigger lines (873
distinct tokens): **115 trigger tokens are generic or ≤3 chars**; **36 of 94
docs (38%) can fire on two generic tokens alone**; `letra` is claimed by 9 docs,
`departamento` by 8, `cordoba` by 8. Trigger lines had drifted **63% past their
own guidance** (mean 12.5 against 4–8) and nothing checked it — invariant 7
verified only that a `triggers:` line *exists*, which enforces breadth and never
precision.

**Cause B — the most privileged text in every session was frozen for 41 days.**
A gitignored status directory, last written 2026-07-30, holding one of 36 plans,
asserted the current focus was an arc that does not appear anywhere in the
preceding 45 days of work (622 commits to `research/evidence`, 533 to
`output/access_to_finance`, 208 to `output/agriculture`). It pointed at three
files that do not exist. → principle 4's revision and principle 11.

**Scope correction:** that `SessionStart` hook is **not r2p**. It comes from a
separate user-level framework wired in `~/.claude/settings.json`, and r2p had
already removed `SessionStart` hooks on exactly these grounds. **r2p was right.**
What the framework takes from it is the rule, not a code change.

### 3.3 Confusion

- **380 markdown files reference directories that no longer exist** — 223 cite
  `decisions/`, 157 `learnings/`, 32 `insights/`; all three merged into
  `research/methods/` in v2. The v1→v2 migration shipped a repath pass and a
  link checker, so either the repath did not run to completion or later merges
  reintroduced what it removed. → `docs/field-notes/a-migration-is-not-done-when-it-runs.md`.
- **The pilot's root contradicts its own `CLAUDE.md` rule** ("eight directories,
  config, and nothing else" against 12 directories and 15 root files), and its
  counts have drifted ("~40" claims against 48).
- **Córdoba runs an older linter than the framework ships** — 106 lines local
  against 621 at measurement time. Nothing tells an instance it is behind.

### 3.4 Longevity — the most important finding

Is each evidence doc cited by `claims.md`, any methods doc, or any deliverable —
still load-bearing — or is it only an index row?

```
pre-consolidation  ids   1-196    n=196   orphaned= 10   ( 5%)
renumbered/merged  ids 197-285    n= 89   orphaned= 78   (88%)
```

**5% vs 88%, with zero dangling references anywhere.** Append-only evidence with
curated claims on top works, and a 5% orphan rate over 196 docs across six
months is r2p's strongest validation. But the 2026-08-21 worktree consolidation
renumbered 77 docs, repointed eleven claims and stranded the rest: **787,621
bytes — 26% of the evidence corpus — reachable only from an index row**, and
therefore invisible to synthesis and to the final report.

The failure is **strictly one-directional**. Nothing in `claims.md` points at a
doc that does not exist; new evidence simply never got promoted *up* into the
curated layer. That is far cheaper to repair than broken links — and it was a
**detectable** condition nothing was detecting, because every check r2p had
walked the chain upward. → invariant 19.

Two more longevity signals, both pilot-side follow-ups rather than framework
bugs: the plan lifecycle has stalled completely (**36 active `plan-*/`, 0
archived, 0 `.completed` markers, 15 MB**, all 36 handoffs stamped 2026-08-21 by
the consolidation, which destroyed the staleness signal); and 45 of 285 evidence
docs have no frontmatter block at all, while the other 240 carry every documented
key at 100%.

## 4. What v3 already got right

- **The capped evidence index scales.** 285 rows, 0 violations, max exactly 120.
- **Append-only evidence + editable claims works.** 5% orphan rate over 196 docs
  and six months, zero dangling citations.
- **Frontmatter scope keys work.** All 240 compliant docs carry
  `unit`/`geography`/`period`, and the overlap rule is genuinely mechanical.
- **The sources layer is healthy**: 113 of 130 (87%) source docs are referenced
  from analysis code, scrapers, or evidence.
- **v3's `Rests on:` check passes**, and it fixed the verdict-word false positive.
- **r2p was already right about `SessionStart` hooks.**

## 5. The two linter bugs, and why nobody had wired it

The v3 linter had a **73% false-positive rate on a correct project**, which is
why it was never wired anywhere.

| Check | Reported | Real | False | Cause |
|---|---|---|---|---|
| 1 headline cap | **64 FAIL** | **0** | **64** | `length()` counts **bytes** |
| 3 frontmatter | **106 FAIL** | **45** | **61** | required an **undocumented** key |
| 4 filename-id mismatch | 11 FAIL | 11 | — | real, but re-reports check 3's defect |

**Bug 1 is a portability bug and fatal for any non-English project.** `mawk` —
Ubuntu's default — is byte-oriented *in every locale*; `LC_ALL=C.UTF-8` still
returns 10 for a 5-character accented string. Córdoba's headlines max out at
exactly 120 characters, so its authors were counting carefully and complying
perfectly; accented Spanish inflates them to 121–131 bytes. The insight was
already in the file one check away — the comment above the verdict-word scan
says mawk is byte-oriented — and had never been carried upward.

**Bug 2 — the check contradicted the convention it enforced.** `evidence.md`
documents `status / unit / geography / period / confidence`; the linter
additionally demanded `id:` and `headline:`. Córdoba's 240 frontmatter'd docs
carry all five documented keys at 100%; only 63% carry the undocumented
`headline`, which `r2p evidence new` satisfied with an unedited placeholder.
`geography` — load-bearing for the contradiction test — was unchecked.

With both fixed, Córdoba's real defect count drops from ~171 to 45 docs with no
frontmatter block plus two genuine WARNs. **Sequence matters: wiring an
inaccurate linter is what poisons it**, which is v3 Phase 3's own rule applied to
two checks that predate it.

## 6. What v3.1 changed

| Change | Kind | Where |
|---|---|---|
| Principle 1: a hook may enforce, may not inject | constitution, **first** | `audience-and-philosophy.md` |
| Principle 4: no gitignored file may feed session context | constitution | same |
| Principle 11: derive state, don't store it | constitution | same |
| Delete `UserPromptSubmit` + `retrieve-learnings.sh` | removal | settings template, `git rm`, `REMOVED_HOOKS` |
| `triggers:` becomes a documented grep, cap retired | prose | `methods.md`, `CLAUDE.md.template` |
| Lint bug 1 — count characters, not bytes | 3 lines | invariant 1 |
| Lint bug 2 — required keys match the protocol | 1 line | invariant 3; `headline:` dropped from the template |
| **Downward reachability** | **new invariant 19** | stranded evidence |
| `sources/INDEX.md` cap + one row per doc | contract + **invariant 20** | `sources.md`, template, lint |

**Not changed, deliberately.** The linter stays wired to nothing. Its findings
are worth more typed than ambient, and an unwired check that is *accurate* is a
different object from one that is merely unrun.

## Appendix — reproduction

```bash
# context load
wc -c CLAUDE.md research/claims.md research/{evidence,sources,methods}/INDEX.md

# headline cap: characters vs bytes
python3 - <<'PY'
import re
c=b=0
for l in open('research/evidence/INDEX.md',encoding='utf-8'):
    if not re.match(r'^\| *\d+ *\|',l): continue
    h=l.split('|')[2].strip()
    c+= len(h)>120; b+= len(h.encode())>120
print("over 120 chars:",c," over 120 bytes:",b)
PY

# evidence reachability (the 5% vs 88% test) — now invariant 19
python3 - <<'PY'
import re,glob,os
ev={int(re.match(r'(\d+)_',os.path.basename(f)).group(1)):f
    for f in glob.glob('research/evidence/[0-9]*_*.md')}
def refs(pats):
    t=''.join(open(f,encoding='utf-8',errors='replace').read()
              for p in pats for f in glob.glob(p,recursive=True))
    return set(int(x) for x in re.findall(r'#(\d{1,3})\b',t)) & set(ev)
reach = refs(['research/claims.md']) | refs(['research/methods/*.md']) \
      | refs(['deliverables/**/*.md'])
for lo,hi,lab in [(1,196,'pre-consolidation'),(197,285,'renumbered/merged')]:
    band=[i for i in ev if lo<=i<=hi]
    orph=[i for i in band if i not in reach]
    print(f"{lab:20s} n={len(band):3d} orphaned={len(orph):3d} ({100*len(orph)/len(band):.0f}%)")
PY

# plan lifecycle throughput
ls -d plan/plan-*/ | wc -l; ls -d plan/archive/*/ 2>/dev/null | wc -l
find plan -name .completed | wc -l
```

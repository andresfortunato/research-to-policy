# Script Header — Protocol

**Trigger**: Every analytical script in `scripts/` (R, Python, Stata, or
shell pipelines that drive analysis) starts with a header comment block
that documents what the script reads, what it writes, the random seed if
any, and a loose environment fingerprint. The header lives in the script
itself, so it travels with the code through git.

This convention replaces an earlier `manifest.jsonl` audit-log mechanism.
The argument: `git log -- output/<file>` plus a header in the script that
produced it gives you the same reproducibility trail at zero install cost
and with no language-specific machinery.

## Required fields

Every analytical script starts with these comment lines, in this order:

```
# Script:   <relative path of this file>
# Inputs:   <comma-separated list of input files this script reads>
# Outputs:  <comma-separated list of files this script writes>
# Seed:     <int, or "none" if non-stochastic>
# Env:      <language + version + 1-2 critical packages, e.g. "R 4.3.1, tidyverse 2.0">
```

If a field doesn't apply, write `none` (do not omit the line — the fixed
shape is what makes the header greppable).

## Format examples

### R

```r
# Script:   scripts/06c_fdi_at_entry.R
# Inputs:   data/clean/wdi.csv, data/raw/wdi_2024.csv
# Outputs:  output/06c_fdi_at_entry.png, output/06c_fdi_at_entry.csv
# Seed:     42
# Env:      R 4.3.1, tidyverse 2.0.0, fixest 0.11

library(tidyverse)
library(fixest)
set.seed(42)
# ... rest of the script
```

### Python

```python
# Script:   scripts/06c_fdi_at_entry.py
# Inputs:   data/clean/wdi.csv
# Outputs:  output/06c_fdi_at_entry.png
# Seed:     42
# Env:      Python 3.11, pandas 2.1, statsmodels 0.14

import pandas as pd
import numpy as np
np.random.seed(42)
# ... rest of the script
```

### Stata

```stata
* Script:   scripts/06c_fdi_at_entry.do
* Inputs:   data/clean/wdi.dta
* Outputs:  output/06c_fdi_at_entry.png
* Seed:     42
* Env:      Stata 18

use "data/clean/wdi.dta", clear
set seed 42
* ... rest of the script
```

## What counts as "analytical"

Scripts that:
- Read data and produce **outputs that show up in deliverables, insights, or memos** (charts, regression tables, summary CSVs).
- Are reproducible end-to-end (you can re-run them later).

Scripts that don't need a header:
- Build / setup scripts that only configure the environment.
- One-line wrappers (`Rscript -e 'install.packages("foo")'`).
- Pure data-cleaning scripts whose output is itself an input to another script — but adding the header anyway costs nothing and helps trace the chain.

## Why this works

Given a chart `output/06c_fdi_at_entry.png` and a question "how was this made?":

```bash
# 1. Find the commit that last touched it
git log -- output/06c_fdi_at_entry.png

# 2. Read the commit message — the analytical-commit-format convention requires
#    `Run: scripts/06c_fdi_at_entry.R` and `Out: output/06c_fdi_at_entry.png`

# 3. Read the script header — confirms inputs, seed, env

# 4. Check out the commit; reproduce
git checkout <sha>
Rscript scripts/06c_fdi_at_entry.R
sha256sum output/06c_fdi_at_entry.png
# Compare against current; mismatch = something changed (env, input data, code)
```

The header is the per-run record of *intent*; git is the per-run record
of *result*. Together they replace `manifest.jsonl`.

## Discipline

- **Update the header when you change the script.** If the script grows a new input or output, the header reflects it. A drifted header is worse than no header.
- **Don't lie about seeds.** If a script uses `set.seed(NULL)` or no seed, write `Seed: none`. Tools that scan for missing seeds rely on this.
- **One pair of eyes is enough.** This is not a peer-review checklist. The header is for the future-you who's six months out.
- **Do not make the header longer.** No "purpose" or "author" or "version" lines — git carries those. The fixed five fields are the contract.

## Cross-references

- `.claude/conventions/analytical-commit-format.md` — the matching commit-message convention; together they form the audit trail.
- `.claude/skills/verify/SKILL.md` — `/verify` reads the header to confirm an artifact's parent script and inputs.
- `docs/verification-architecture.md` — design rationale for the verification stack (`/verify` + `/deliverable-review`) without an automatic manifest.

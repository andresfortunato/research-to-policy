# Complex-tradable entrant cohort (v2)

> **This is a template / worked example.** Replace with your project's
> actual `methods/<method-slug>/rule.md` files, or delete once real
> methods are documented. The diagnostic counts below are illustrative
> placeholders — re-run the implementing script for live values.

## Source
`product.country_product_year_4` — harmonized 4-digit product-level
trade panel, years 1990–2023, ~220 reporters. **`export_rca`
(Balassa) is pre-computed** in the source table — used directly,
never recomputed locally. Population for the structural-economy
filter (below) comes from `wdi.population` (WB indicator
`SP.POP.TOTL`, gap-filled to annual where missing).

## Rule
A country is classed a **complex-tradable entrant** in year `y` if:

1. In each of `y`, `y+1`, `y+2` (an `N_YEARS_MIN=3`-year window) it
   has `n_products_rca >= 3` distinct complex-tradable 4-digit
   product codes with `export_rca >= 1.0`; AND
2. At year `y` (the entry year):
   `(complex_exports >= $100M nominal USD OR complex_share >= 0.5%)`
   **AND** `complex_exports >= $10M nominal USD` (absolute hard
   floor); AND
3. **Sustained-growth gate (new in v2)** at year `y+5`:
   `n_products_rca >= 3` AND
   `complex_exports(t+5) >= 1.2× complex_exports(t)`. If
   `y+5 > 2023` (too recent to verify), the candidate is dropped.

The first such `y` is recorded as the country's `entry_year`.
Computed independently for the narrow definition (excluding
residual "parts, n.e.s." product codes) and the broad definition
(all complex-tradable codes).

## Why this version
v1 used only steps (1) and (2). This permitted entries triggered
by 3-year RCA spikes that immediately faded — e.g. a country that
entered solely on residual "parts, n.e.s." product codes whose RCA
fell back below 1 within two years and never recovered. v2's
sustained-growth gate at `y+5` filters these out.

The `$10M` absolute floor was added in v1 after the first run
produced an inflated count where most of the excess were
micro-territories whose total exports are so small that the 0.5%
share trivially passes on trade-data noise. The hard floor
preserves real small-economy entries while dropping the noise.

The four "parts, n.e.s." 4-digit codes (`X591`, `X599`, `X649`,
`X768` — placeholder slugs) are dropped from the *narrow*
definition. The broad definition keeps them; the gap between
narrow and broad is one of the diagnostic counts below, useful for
sanity-checking whether residual-bucket re-classification is
distorting the cohort.

## Exclusions
The following ISO3 codes are **dropped from the cohort** because
their RCA in this product family reflects logistics /
transshipment, not productive capability:

```
['HKG', 'SGP', 'NLD', 'ARE', 'MAC', 'BHR', 'MLT', 'BRN', 'LUX']
```

These nine codes are the standard re-export-hub list used across
the project's tradable-cohort methods. They are retained in
`output/<method>_reexport_hubs.csv` for transparency and for
the chart caption that flags excluded countries.

## Edge cases
- **Pre-period coverage gaps.** A country with no panel observations
  before its candidate `entry_year` is recorded with the entry but
  flagged `left_censored=True`; downstream charts that depend on
  the entry-year *level* must surface the flag.
- **Population NULL throughout the panel.** Countries whose
  population data is NULL for the full window (e.g. some isolated
  reporters in some decades) are **kept** but flagged
  `pop_unverified=True` — better to retain a real country with bad
  population data than drop it.
- **Single-observation series.** If the implementing script finds a
  product-country pair with only one year of data inside the
  3-year RCA window, that pair does not count toward
  `n_products_rca`. The window must be fully observed.

## Structural-economy filter
Countries whose **maximum recorded population (1990–2023) falls
below 500,000** are dropped from the cohort. This removes
micro-jurisdictions where the trade panel attributes implausibly
large flows that almost certainly reflect re-export, transshipment,
or partner-side mirror artifacts rather than indigenous capability.

## Known limitations
- **Nominal-USD scale floor.** $100M nominal at the entry year (not
  deflated to a fixed base year). Most cohort entries are post-2000
  where the deflator effect is modest; documented as a deliberate
  simplification.
- **Right-censoring at entry+10.** Any country with `entry_year >
  2013` cannot yet be classified into sustainer / plateauer /
  faller categories at `entry_year + 10` and is marked `pending`.
- **Product-classification breaks.** The harmonized panel smooths
  the underlying classification revisions but introduces mild
  discontinuities at break years — accept as known; do not chase
  break-year wiggles in chart captions.
- **Re-export-hub list is fixed**, not data-driven. Adding or
  removing a hub is a methodology change — file a `decisions/`
  record and bump this rule to v3.

## Diagnostic counts (from `build_NN_cohort.py`)

> Illustrative placeholders. The implementing script's actual
> output replaces these on every re-run; the `analytical-commit-format`
> convention's `Run:` line ties them to the script that produced
> them.

- Narrow entrants (post-exclusion): **42**
- Broad entrants (post-exclusion): **78**
- In both: 42 | Narrow-only: 0 | Broad-only: 36
- Narrow class breakdown: `{'sustainer': 31, 'faller': 7,
  'plateauer': 3, 'pending': 1}`
- Re-export hubs dropped (narrow): `['ARE', 'HKG', 'LUX', 'MAC',
  'MLT', 'NLD', 'SGP']`
- Micro-jurisdictions dropped (population <500k): 14 ISO3 codes
  (transparency CSV: `output/<method>_micro_jurisdictions.csv`)

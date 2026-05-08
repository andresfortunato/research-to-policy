# Post-Extraction Data Pipeline

## Table of Contents
- [Cleaning Pipeline](#cleaning-pipeline)
- [Currency Detection and Correction](#currency-detection-and-correction)
- [Deduplication](#deduplication)
- [Spatial Joins](#spatial-joins)
- [Storage and Export](#storage-and-export)
- [Multi-Region Orchestration](#multi-region-orchestration)

## Cleaning Pipeline

### Standard Cleaning Steps

```python
import pandas as pd
import numpy as np

def clean_scraped_data(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Remove exact duplicates
    df = df.drop_duplicates(subset=["posting_id"])

    # 2. Parse numeric fields
    df["price_numeric"] = df["price"].apply(parse_price)

    # 3. Filter obvious bad data
    df = df[df["price_numeric"] >= 10]  # filter placeholders

    # 4. Normalize text fields
    for col in ["title", "location_name", "property_type"]:
        if col in df.columns:
            df[col] = df[col].str.strip()

    # 5. Derived fields
    df["price_per_m2"] = df["price_numeric"] / df["m2_total"].replace(0, np.nan)

    # 6. Add metadata
    df["scrape_date"] = pd.Timestamp.now().isoformat()

    return df

def parse_price(price_str) -> float:
    """Parse price string to float, handling locale formatting."""
    if pd.isna(price_str):
        return np.nan
    s = str(price_str)
    # Remove thousands separator (. in es-AR, , in en-US)
    s = s.replace(".", "").replace(",", "")
    # Remove currency symbols
    for sym in ["$", "U$S", "USD", "ARS", " "]:
        s = s.replace(sym, "")
    try:
        return float(s)
    except ValueError:
        return np.nan
```

### Outlier Detection

```python
def flag_outliers(df: pd.DataFrame, col: str, iqr_factor=1.5) -> pd.Series:
    """Flag outliers using IQR method."""
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - iqr_factor * iqr
    upper = q3 + iqr_factor * iqr
    return (df[col] < lower) | (df[col] > upper)
```

## Currency Detection and Correction

From the scraper-zonaprop project: when sites list prices in multiple currencies with unreliable labels, use price-per-unit discriminators.

### Problem

Sites like ZonaProp label prices with `$` (pesos) or `USD`, but labels are often wrong. A listing at `$2,500` labeled as pesos is likely USD based on the market.

### Solution: Price-Per-M2 Discriminator

```python
def classify_currency(row, exchange_rate=1500, min_usd_per_m2=1, max_usd_per_m2=100):
    """Infer true currency from price-per-m2 reasonableness.

    For rental properties, reasonable range is $1-100 USD/m2/month.
    Test both currency assumptions and pick the one that falls in range.
    """
    price = row["price_numeric"]
    m2 = row["m2_total"]

    if pd.isna(price) or pd.isna(m2) or m2 <= 0:
        return {"inferred_currency": row["currency"], "confidence": "low"}

    # Assume USD
    usd_per_m2_if_usd = price / m2
    usd_ok = min_usd_per_m2 <= usd_per_m2_if_usd <= max_usd_per_m2

    # Assume ARS
    usd_per_m2_if_ars = (price / exchange_rate) / m2
    ars_ok = min_usd_per_m2 <= usd_per_m2_if_ars <= max_usd_per_m2

    if usd_ok and not ars_ok:
        return {"inferred_currency": "USD", "confidence": "high"}
    elif ars_ok and not usd_ok:
        return {"inferred_currency": "ARS", "confidence": "high"}
    elif usd_ok and ars_ok:
        return {"inferred_currency": row["currency"], "confidence": "ambiguous"}
    else:
        return {"inferred_currency": row["currency"], "confidence": "outlier"}
```

### Applying Corrections

```python
def correct_currencies(df, exchange_rate=1500):
    """Apply currency corrections and normalize to USD."""
    results = df.apply(classify_currency, axis=1, result_type="expand",
                       exchange_rate=exchange_rate)
    df["inferred_currency"] = results["inferred_currency"]
    df["confidence"] = results["confidence"]
    df["currency_corrected"] = df["inferred_currency"] != df["currency"]

    # Normalize all to USD
    df["price_usd"] = df.apply(
        lambda r: r["price_numeric"] if r["inferred_currency"] == "USD"
        else r["price_numeric"] / exchange_rate,
        axis=1,
    )

    # Report
    n_corrected = df["currency_corrected"].sum()
    n_outlier = (df["confidence"] == "outlier").sum()
    print(f"Corrected: {n_corrected}, Outliers: {n_outlier}, Clean: {len(df) - n_outlier}")

    return df
```

### Adapting to Other Domains

The discriminator pattern works whenever you have:
1. A secondary signal (price/m2, price/unit, price/weight)
2. A known reasonable range for that signal
3. A known exchange rate or conversion factor

Examples: real estate (price/m2), e-commerce (price/weight), commodities (price/unit).

## Deduplication

### By Unique ID

```python
df = df.drop_duplicates(subset=["posting_id"], keep="first")
```

### By Content Hash

When no unique ID exists, hash key fields:

```python
import hashlib

def content_hash(row, fields):
    content = "|".join(str(row.get(f, "")) for f in fields)
    return hashlib.md5(content.encode()).hexdigest()

df["content_hash"] = df.apply(content_hash, axis=1,
                               fields=["title", "price", "location"])
df = df.drop_duplicates(subset=["content_hash"], keep="first")
```

### Cross-Region Deduplication

When scraping the same site across multiple regions/categories, listings may overlap:

```python
def deduplicate_across_regions(dfs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Merge DataFrames from multiple regions, removing duplicates."""
    combined = pd.concat(dfs.values(), ignore_index=True)
    # Keep first occurrence (preserves the region it was first found in)
    combined = combined.drop_duplicates(subset=["posting_id"], keep="first")
    return combined
```

## Spatial Joins

Assign geographic units (neighborhoods, districts, statistical areas) to scraped data with coordinates.

### Point-in-Polygon with GeoPandas

```python
import geopandas as gpd
from shapely.geometry import Point

def assign_geographic_units(df, shapefile_path, id_col, name_col):
    """Spatial join: assign geographic unit to each listing based on lat/lon."""
    # Filter to rows with valid coordinates
    geo_df = df.dropna(subset=["latitude", "longitude"]).copy()

    # Create geometry
    geometry = [Point(lon, lat) for lon, lat in
                zip(geo_df["longitude"], geo_df["latitude"])]
    gdf = gpd.GeoDataFrame(geo_df, geometry=geometry, crs="EPSG:4326")

    # Load shapefile
    areas = gpd.read_file(shapefile_path).to_crs("EPSG:4326")

    # Spatial join
    joined = gpd.sjoin(gdf, areas, how="left", predicate="within")

    # Handle overlapping polygons: keep smallest area (most specific)
    if joined.index.duplicated().any():
        areas["area"] = areas.geometry.area
        joined = joined.merge(areas[["area"]], left_on="index_right", right_index=True)
        joined = joined.sort_values("area").drop_duplicates(subset=gdf.index.name or "index")

    # Map back to original DataFrame
    df[id_col] = joined[id_col]
    df[name_col] = joined[name_col]

    return df
```

### Recovery for Unmatched Points

Points near boundaries may not fall within any polygon. Recover using nearest-neighbor:

```python
from shapely.ops import nearest_points

def recover_unmatched(gdf, areas, max_distance_km=5):
    """Assign nearest area to points that didn't match any polygon."""
    unmatched = gdf[gdf["area_id"].isna()]
    for idx, row in unmatched.iterrows():
        nearest_geom = nearest_points(row.geometry, areas.unary_union)[1]
        distance_km = row.geometry.distance(nearest_geom) * 111  # rough deg->km
        if distance_km <= max_distance_km:
            # Find which area contains the nearest point
            containing = areas[areas.contains(nearest_geom)]
            if len(containing) > 0:
                gdf.loc[idx, "area_id"] = containing.iloc[0]["id"]
    return gdf
```

## Storage and Export

### Dual Output Pattern

Save both complete (all columns) and curated (mapped columns) versions:

```python
from datetime import datetime

def save_results(df, columns_map, output_dir="data"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Complete: all columns
    full_path = f"{output_dir}/full_{timestamp}.csv"
    df.to_csv(full_path, index=False)

    # Curated: only mapped columns
    curated = df[list(columns_map.keys())].rename(columns=columns_map)
    curated_path = f"{output_dir}/curated_{timestamp}.csv"
    curated.to_csv(curated_path, index=False)

    return full_path, curated_path
```

### Column Mapping

Define a mapping from raw field paths to clean column names:

```python
COLUMNS_MAP = {
    "postingId": "posting_id",
    "priceOperationTypes[0].prices[0].formattedAmount": "price",
    "priceOperationTypes[0].prices[0].currency": "currency",
    "mainFeatures.CFT100.value": "m2_total",
    "mainFeatures.CFT101.value": "m2_covered",
    "mainFeatures.CFT1.value": "rooms",
    "postingLocation.postingGeolocation.geolocation.latitude": "latitude",
    "postingLocation.postingGeolocation.geolocation.longitude": "longitude",
    "realEstateType.name": "property_type",
}
```

### Incremental / Streaming Saves

For long-running scrapes, save incrementally:

```python
import csv

def append_to_csv(data: list[dict], filepath: str):
    """Append rows to CSV, creating file with headers if needed."""
    file_exists = os.path.exists(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)
```

## Multi-Region Orchestration

When scraping the same site across multiple regions/categories:

### Pattern

```python
import asyncio

REGIONS = {
    "buenos-aires": "https://example.com/buenos-aires/rentals",
    "cordoba": "https://example.com/cordoba/rentals",
    "rosario": "https://example.com/rosario/rentals",
}

async def scrape_all_regions(regions, delay_between=5):
    all_data = {}

    browser, page = await create_browser()

    for name, url in regions.items():
        print(f"Scraping {name}...")
        try:
            data = await scrape_region(page, url)
            all_data[name] = data

            # Save checkpoint per region
            save_checkpoint(data, f"data/{name}_checkpoint.csv")
        except Exception as e:
            print(f"Failed {name}: {e}")
            continue

        await asyncio.sleep(delay_between)

    await browser.close()

    # Combine and deduplicate
    combined = deduplicate_across_regions(all_data)
    save_results(combined, COLUMNS_MAP)

    # Summary
    for name, data in all_data.items():
        print(f"  {name}: {len(data)} listings")
    print(f"  Total (deduplicated): {len(combined)}")
```

### Progress Tracking

```python
class ScrapeProgress:
    def __init__(self, total_regions: int):
        self.total_regions = total_regions
        self.completed = 0
        self.failed = []
        self.total_items = 0

    def region_done(self, name: str, count: int):
        self.completed += 1
        self.total_items += count
        pct = 100 * self.completed / self.total_regions
        print(f"[{pct:.0f}%] {name}: {count} items (total: {self.total_items})")

    def region_failed(self, name: str, error: str):
        self.failed.append(name)
        print(f"[FAIL] {name}: {error}")

    def summary(self):
        print(f"\nCompleted: {self.completed}/{self.total_regions}")
        print(f"Total items: {self.total_items}")
        if self.failed:
            print(f"Failed: {', '.join(self.failed)}")
```

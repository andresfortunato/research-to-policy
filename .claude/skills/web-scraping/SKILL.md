---
name: web-scraping
description: (r2p) Build production-grade web scrapers in Python using Playwright, httpx, BeautifulSoup, and AI-powered extraction (ScrapeGraphAI, Crawl4AI). Use when the user asks to scrape websites, extract data from web pages, build crawlers, handle anti-bot detection, parse HTML/JSON, automate browser interactions, or set up data extraction pipelines. Also use when discussing scraping architecture, anti-detection strategies, proxy rotation, pagination handling, or choosing between traditional selectors and LLM-based extraction.
---

# Web Scraping

Build resilient, production-grade web scrapers. This skill covers the full pipeline: fetching, extraction, validation, storage, and anti-detection.

## Decision: Scraping Approach

Determine the right approach based on the target site:

1. **Static HTML sites** (no JS rendering needed) -> `httpx` + `BeautifulSoup`/`lxml`
2. **JavaScript-rendered / SPA sites** -> `Playwright` with stealth plugin
3. **Sites with embedded JSON state** (React/Next.js) -> Intercept `__PRELOADED_STATE__` or API calls via CDP
4. **Complex/unstructured content or rapidly changing layouts** -> LLM-based extraction (`ScrapeGraphAI` or `Crawl4AI`)
5. **Large-scale structured crawling** -> `Scrapy` framework

**Check the Network tab first**: Many modern sites load data via internal JSON APIs (XHR/Fetch). Scraping the API directly is always faster and more reliable than parsing HTML.

## Core Workflow

```
1. Analyze target site (inspect HTML, network requests, robots.txt)
2. Choose fetching strategy (HTTP client vs browser automation)
3. Implement extraction (selectors, JSON parsing, or LLM)
4. Add resilience (retries, error handling, checkpoints)
5. Validate extracted data (Pydantic schemas)
6. Store results (CSV/JSON/Parquet with metadata)
```

## Fetching Patterns

### HTTP Client (Static Sites)

```python
import httpx
from bs4 import BeautifulSoup

async def fetch_page(url: str, client: httpx.AsyncClient) -> BeautifulSoup:
    response = await client.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")
```

### Playwright Browser (JS-Rendered Sites)

```python
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def create_browser():
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(
        headless=False,  # headless=True more detectable
        args=["--disable-blink-features=AutomationControlled"]
    )
    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="en-US",
        timezone_id="America/New_York",
    )
    page = await context.new_page()
    await stealth_async(page)
    return browser, page
```

### CDP Response Interception (Embedded JSON)

Many React/Next.js sites embed data as `__PRELOADED_STATE__` or `__NEXT_DATA__` in the HTML. Intercept it via Chrome DevTools Protocol:

```python
responses = {}

async def capture_responses(page):
    client = await page.context.new_cdp_session(page)
    await client.send("Network.enable")

    def on_response(params):
        url = params.get("response", {}).get("url", "")
        request_id = params.get("requestId")
        if request_id:
            try:
                body = client.send("Network.getResponseBody", {"requestId": request_id})
                responses[url] = body
            except Exception:
                pass

    client.on("Network.responseReceived", on_response)
```

Alternatively, extract from raw HTML:

```python
import json

def extract_preloaded_state(html: str) -> dict:
    start = "__PRELOADED_STATE__ = "
    end = "window.__SITE_DATA__"  # adjust per site
    idx_start = html.find(start)
    idx_end = html.find(end, idx_start)
    if idx_start == -1:
        return {}
    raw = html[idx_start + len(start):idx_end].strip().rstrip(";")
    return json.loads(raw)
```

## Extraction Patterns

### CSS Selectors (stable sites)

```python
soup = BeautifulSoup(html, "lxml")
items = []
for card in soup.select("div.listing-card"):
    items.append({
        "title": card.select_one("h2.title").get_text(strip=True),
        "price": card.select_one("[data-testid='price']").get_text(strip=True),
        "url": card.select_one("a")["href"],
    })
```

Prefer `[data-testid]` or `[data-*]` attribute selectors -- they survive redesigns better than class names.

### Nested JSON Flattening

For deeply nested API/state JSON, flatten to tabular format:

```python
def flatten_json(obj, prefix=""):
    flat = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            flat.update(flatten_json(v, f"{prefix}{k}."))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            flat.update(flatten_json(v, f"{prefix}[{i}]."))
    else:
        flat[prefix.rstrip(".")] = obj
    return flat
```

### LLM-Based Extraction

See [references/ai-extraction.md](references/ai-extraction.md) for ScrapeGraphAI and Crawl4AI patterns.

## Resilience

### Retry with Exponential Backoff

```python
import asyncio, random

async def fetch_with_retry(fetch_fn, max_retries=3, base_delay=5):
    for attempt in range(max_retries):
        try:
            return await fetch_fn()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(delay)
```

### Circuit Breaker

Stop scraping a domain after N consecutive failures:

```python
consecutive_errors = 0
MAX_CONSECUTIVE = 5

for page_num in range(1, total_pages + 1):
    try:
        data = await scrape_page(page_num)
        consecutive_errors = 0
        all_data.extend(data)
    except Exception:
        consecutive_errors += 1
        if consecutive_errors >= MAX_CONSECUTIVE:
            break  # return partial data
```

### Progressive Saves (Checkpointing)

Save incrementally during long runs so crashes don't lose data:

```python
SAVE_INTERVAL = 50  # pages

for page_num in range(1, total_pages + 1):
    data = await scrape_page(page_num)
    all_data.extend(data)
    if page_num % SAVE_INTERVAL == 0:
        save_checkpoint(all_data, f"checkpoint_page_{page_num}.csv")
```

## Pagination

Common patterns:

```python
# URL-based: /listings.html, /listings-pagina-2.html
def build_url(base: str, page: int) -> str:
    return f"{base}.html" if page == 1 else f"{base}-pagina-{page}.html"

# Query param: /listings?page=2
def build_url(base: str, page: int) -> str:
    return f"{base}?page={page}"

# Detect total pages from first response
def get_total(soup) -> int:
    text = soup.select_one("h1").get_text()  # "1.234 listings found"
    return int(text.split()[0].replace(".", "").replace(",", ""))
```

## Data Validation

Always validate extracted data with Pydantic:

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Listing(BaseModel):
    id: str
    title: str
    price: float = Field(ge=0)
    currency: str
    url: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("currency")
    @classmethod
    def valid_currency(cls, v):
        if v not in ("USD", "ARS", "EUR"):
            raise ValueError(f"Unknown currency: {v}")
        return v
```

## Anti-Detection

See [references/anti-detection.md](references/anti-detection.md) for detailed strategies including:
- Header rotation
- Playwright stealth configuration
- Proxy rotation patterns
- Cloudflare bypass
- Behavioral simulation

## Rate Limiting

- **Conservative default**: 3-5 seconds between requests
- **Between sections/provinces**: 5-10 seconds
- **Respect `robots.txt`** `Crawl-delay` directives
- **Async concurrency**: limit with `asyncio.Semaphore(5)`
- **Adaptive**: slow down when response times increase or errors spike

## Storage

| Use Case | Format |
|---|---|
| Quick exploration | CSV |
| Nested/hierarchical data | JSON / NDJSON |
| Analytics / data lake | Parquet |
| Production pipeline | SQLite or PostgreSQL |

Always include metadata: `scrape_timestamp`, `source_url`, `scraper_version`.

Save raw HTML alongside extracted data for reprocessing.

## Reference Files

- **[references/anti-detection.md](references/anti-detection.md)**: Anti-bot evasion, stealth config, proxy rotation, Cloudflare handling
- **[references/ai-extraction.md](references/ai-extraction.md)**: LLM-powered extraction with ScrapeGraphAI, Crawl4AI, hybrid approaches
- **[references/data-pipeline.md](references/data-pipeline.md)**: Post-extraction processing -- cleaning, currency correction, deduplication, spatial joins

## Legal & Ethical

- Check `robots.txt` before scraping
- Respect Terms of Service
- Use public APIs when available
- Never scrape personal/sensitive data in violation of GDPR/CCPA
- Minimize server load with conservative rate limits
- Identify your scraper in the User-Agent for academic/research use

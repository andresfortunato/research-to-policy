# Anti-Detection Strategies

## Table of Contents
- [Header Management](#header-management)
- [Playwright Stealth](#playwright-stealth)
- [Cloudflare Bypass](#cloudflare-bypass)
- [Proxy Rotation](#proxy-rotation)
- [Behavioral Simulation](#behavioral-simulation)
- [Fingerprint Management](#fingerprint-management)

## Header Management

Rotate realistic header sets. Headers must be internally consistent (Chrome UA with Chrome-specific headers).

```python
import random

HEADER_PROFILES = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    },
]

def get_headers():
    return random.choice(HEADER_PROFILES).copy()
```

## Playwright Stealth

### Full Stealth Setup

```python
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

async def create_stealth_browser(locale="en-US", timezone="America/New_York"):
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(
        headless=False,  # headless mode is more detectable
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ]
    )
    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale=locale,
        timezone_id=timezone,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    )
    page = await context.new_page()
    await stealth_async(page)  # patches navigator.webdriver, WebGL, plugins, etc.
    return pw, browser, page
```

### What playwright-stealth Patches

- `navigator.webdriver` = false
- `navigator.plugins` (fakes plugin list)
- `navigator.languages` (matches locale)
- WebGL vendor/renderer fingerprint
- Chrome DevTools Protocol detection vectors
- `window.chrome` runtime object

### Limitations

Stealth plugins do NOT reliably bypass:
- Cloudflare Turnstile
- PerimeterX / HUMAN
- DataDome
- Advanced behavioral analysis

For these, consider managed browser services (Browserless, ScrapFly) or CAPTCHA-solving APIs.

## Cloudflare Bypass

### Detection and Wait Pattern

From the scraper-zonaprop project -- wait for Cloudflare challenge to resolve:

```python
async def wait_for_cloudflare(page, timeout=30):
    """Wait for Cloudflare challenge page to resolve."""
    start = time.time()
    while time.time() - start < timeout:
        title = await page.title()
        # Cloudflare challenge pages have specific titles
        if "just a moment" not in title.lower() and "cloudflare" not in title.lower():
            return True
        await page.wait_for_timeout(2000)
        # Try reloading if stuck
        if time.time() - start > 15:
            await page.reload()
    raise TimeoutError("Cloudflare challenge did not resolve")
```

### Tips

- Run with `headless=False` -- Cloudflare detects headless browsers more aggressively
- Set locale and timezone matching the target site's country
- Allow 2-5 seconds after Cloudflare resolves before interacting with the page
- If Cloudflare consistently blocks, the site may require residential proxies

## Proxy Rotation

### Basic Rotation

```python
import itertools

PROXIES = [
    "http://user:pass@proxy1.example.com:8080",
    "http://user:pass@proxy2.example.com:8080",
    "http://user:pass@proxy3.example.com:8080",
]

proxy_cycle = itertools.cycle(PROXIES)

# With httpx
async with httpx.AsyncClient(proxy=next(proxy_cycle)) as client:
    response = await client.get(url)

# With Playwright
context = await browser.new_context(
    proxy={"server": next(proxy_cycle)}
)
```

### Rotation Strategies

| Strategy | When to Use |
|---|---|
| Round-robin | Simple, evenly distributes load |
| Random | Avoids predictable patterns |
| Subnet-aware | Rotate by ASN/subnet, not just IP |
| Sticky session | Authenticated flows (same IP for login session) |
| Geographic | Match proxy location to target audience |

### Rotation Frequency

- **Aggressive targets** (e-commerce, social media): every 5-15 requests
- **Moderate targets** (news, listings): every 50-100 requests
- **Lenient targets** (government, academic): rarely needed

### Proxy Types

| Type | Detection Risk | Cost | Best For |
|---|---|---|---|
| Residential | Low | High | Anti-bot heavy sites |
| Datacenter | High | Low | Simple/lenient sites |
| ISP/Static residential | Low | Medium | Long sessions |
| Mobile | Very low | Very high | Toughest targets |

## Behavioral Simulation

### Random Delays

```python
import random, asyncio

async def human_delay(min_s=1.0, max_s=3.0):
    """Random delay simulating human behavior."""
    await asyncio.sleep(random.uniform(min_s, max_s))

# Between page loads
await human_delay(2.0, 5.0)

# Between interactions on same page
await human_delay(0.5, 1.5)
```

### Mouse and Scroll Simulation

```python
async def simulate_human_scroll(page):
    """Scroll down the page in random increments."""
    viewport_height = page.viewport_size["height"]
    total_scrolled = 0
    page_height = await page.evaluate("document.body.scrollHeight")

    while total_scrolled < page_height * 0.7:
        scroll_amount = random.randint(200, viewport_height)
        await page.mouse.wheel(0, scroll_amount)
        total_scrolled += scroll_amount
        await asyncio.sleep(random.uniform(0.3, 1.0))
```

### Navigation Patterns

- Occasionally visit non-target pages (homepage, about page)
- Vary the order of pages visited
- Do not scrape in sequential URL order -- randomize
- Include occasional pauses (5-30 seconds) to mimic reading

## Fingerprint Management

### Consistent Profiles

When rotating fingerprints, keep profiles internally consistent:

```python
BROWSER_PROFILES = [
    {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...",
        "viewport": {"width": 1920, "height": 1080},
        "locale": "en-US",
        "timezone": "America/New_York",
        "platform": "Win32",
    },
    {
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) ...",
        "viewport": {"width": 1440, "height": 900},
        "locale": "en-US",
        "timezone": "America/Los_Angeles",
        "platform": "MacIntel",
    },
]
```

Do NOT mix contradictory properties (e.g., Windows UA with Mac timezone).

### Detection Vectors to Watch

- **CDP detection**: Anti-bot systems can detect active Chrome DevTools Protocol sessions
- **WebGL renderer**: Must match the claimed platform
- **Canvas fingerprint**: Varies by GPU/OS
- **AudioContext fingerprint**: Varies by audio stack
- **Font enumeration**: Installed fonts vary by OS

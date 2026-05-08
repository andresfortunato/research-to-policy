# AI-Powered Data Extraction

## Table of Contents
- [When to Use AI Extraction](#when-to-use-ai-extraction)
- [ScrapeGraphAI](#scrapegraphai)
- [Crawl4AI](#crawl4ai)
- [Hybrid Approach](#hybrid-approach)
- [Pydantic Schema Validation](#pydantic-schema-validation)
- [Prompt Engineering for Extraction](#prompt-engineering-for-extraction)
- [Error Handling for LLM Extraction](#error-handling-for-llm-extraction)

## When to Use AI Extraction

| Factor | Traditional (CSS/XPath) | LLM-Based |
|---|---|---|
| Scale | High (millions of pages) | Low-Medium (<10k/month) |
| Cost per request | Near zero | $0.001-0.01+ per page |
| Maintenance | High (selectors break) | Low (adapts to changes) |
| Setup time | Hours-days | Minutes-hours |
| Accuracy on stable sites | Very high | High (occasional hallucinations) |
| Accuracy on changing sites | Degrades rapidly | Stays consistent |
| Complex/unstructured content | Difficult | Excels |

**Use AI when**: layouts change frequently, content is unstructured/semi-structured, rapid prototyping needed, or extraction logic is complex.

**Use traditional when**: scale is large (>10k pages/month), cost matters, site structure is stable, or deterministic accuracy is required.

## ScrapeGraphAI

Graph-based LLM-powered scraping. Users describe what to extract in natural language.

### Installation

```bash
pip install scrapegraphai
playwright install chromium
```

### SmartScraperGraph (Single Page)

```python
from scrapegraphai.graphs import SmartScraperGraph

graph_config = {
    "llm": {
        "model": "openai/gpt-4o-mini",
        "api_key": "your-key",
        "temperature": 0,  # deterministic for extraction
    },
    "verbose": True,
    "headless": True,
}

scraper = SmartScraperGraph(
    prompt="Extract all product names, prices, and ratings. Return as a list of objects.",
    source="https://example.com/products",
    config=graph_config,
)

result = scraper.run()
```

### SearchGraph (Multi-Page from Search)

```python
from scrapegraphai.graphs import SearchGraph

search_scraper = SearchGraph(
    prompt="Find rental apartment listings in Buenos Aires with price, location, and square meters",
    config=graph_config,
)

results = search_scraper.run()
```

### Key Configuration Options

```python
graph_config = {
    "llm": {
        "model": "openai/gpt-4o-mini",  # or "ollama/llama3.1" for local
        "api_key": "key",
        "temperature": 0,       # 0 = deterministic (best for extraction)
        "model_tokens": 8192,   # context window
    },
    "embeddings": {
        "model": "openai/text-embedding-3-small",  # for RAG
    },
    "format": "json",           # required for Ollama
    "verbose": True,
    "headless": True,
}
```

### Architecture

ScrapeGraphAI uses a directed graph pipeline:

```
FetchNode -> ParseNode -> ConditionalNode -> GenerateAnswerNode
```

- **FetchNode**: Fetches HTML/JSON via browser or HTTP
- **ParseNode**: Parses and chunks content for LLM context window
- **ConditionalNode**: Branches based on content type or state
- **GenerateAnswerNode**: Constructs prompt, calls LLM, parses response

### Using Local Models (Ollama)

```python
graph_config = {
    "llm": {
        "model": "ollama/llama3.1",
        "temperature": 0,
        "base_url": "http://localhost:11434",
    },
    "format": "json",  # required for Ollama
}
```

## Crawl4AI

Open-source, local-first crawler outputting clean Markdown for RAG pipelines. Supports CSS, XPath, and LLM extraction.

### Installation

```bash
pip install crawl4ai
crawl4ai-setup  # installs browser
```

### Basic Usage

```python
from crawl4ai import AsyncWebCrawler

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url="https://example.com")
    print(result.markdown)  # clean Markdown output
```

### LLM Extraction with Schema

```python
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    rating: float

strategy = LLMExtractionStrategy(
    provider="openai/gpt-4o-mini",
    api_token="your-key",
    schema=Product.model_json_schema(),
    instruction="Extract all products with name, price, and rating",
)

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(
        url="https://example.com/products",
        extraction_strategy=strategy,
    )
    products = result.extracted_content
```

### CSS-Based Extraction (No LLM Cost)

```python
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

schema = {
    "name": "Product listings",
    "baseSelector": "div.product-card",
    "fields": [
        {"name": "title", "selector": "h2.name", "type": "text"},
        {"name": "price", "selector": ".price", "type": "text"},
        {"name": "url", "selector": "a", "type": "attribute", "attribute": "href"},
    ],
}

strategy = JsonCssExtractionStrategy(schema)
```

## Hybrid Approach

The most cost-effective pattern: use LLMs to generate selectors, then apply selectors at scale.

### Pattern

```
1. Fetch sample pages (3-5 representative pages)
2. Use LLM to analyze HTML and extract data + suggest CSS selectors
3. Validate LLM-suggested selectors against sample data
4. Apply selectors at scale (no LLM cost)
5. Use LLM to validate edge cases and handle failures
6. When selectors break (detected via validation), regenerate with LLM
```

### Implementation

```python
import json
from openai import OpenAI

client = OpenAI()

def generate_selectors(html_sample: str, fields: list[str]) -> dict:
    """Use LLM to generate CSS selectors from sample HTML."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[{
            "role": "user",
            "content": f"""Analyze this HTML and generate CSS selectors for these fields: {fields}

Return JSON mapping field names to CSS selectors.
Example: {{"title": "h2.listing-title", "price": "span[data-price]"}}

HTML:
{html_sample[:8000]}"""
        }],
    )
    return json.loads(response.choices[0].message.content)

def validate_extraction(extracted: dict, html: str, fields: list[str]) -> bool:
    """Use LLM to validate extracted data makes sense."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[{
            "role": "user",
            "content": f"""Does this extracted data look correct for the given HTML?
Extracted: {json.dumps(extracted)}
Expected fields: {fields}
Answer YES or NO with brief explanation."""
        }],
    )
    return "YES" in response.choices[0].message.content.upper()
```

This achieves ~2x the recall of pure AI agents while reducing cost by ~3x.

## Pydantic Schema Validation

Always validate LLM-extracted data with Pydantic schemas:

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class RentalListing(BaseModel):
    posting_id: str
    title: str
    price: float = Field(ge=0, description="Monthly rental price")
    currency: str
    m2_total: Optional[float] = Field(default=None, ge=0)
    m2_covered: Optional[float] = Field(default=None, ge=0)
    rooms: Optional[int] = Field(default=None, ge=0)
    bedrooms: Optional[int] = Field(default=None, ge=0)
    bathrooms: Optional[int] = Field(default=None, ge=0)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    property_type: Optional[str] = None
    url: str

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, v):
        mapping = {"$": "ARS", "U$S": "USD", "US$": "USD"}
        return mapping.get(v, v)

    @field_validator("m2_total")
    @classmethod
    def reasonable_size(cls, v):
        if v is not None and v > 50000:
            raise ValueError(f"Unreasonable property size: {v} m2")
        return v
```

### Using with LLM Output

```python
import json

def parse_llm_output(raw: str, model: type[BaseModel]) -> list:
    """Parse and validate LLM JSON output against Pydantic schema."""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code blocks
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0]
            data = json.loads(raw)
        else:
            raise

    items = data if isinstance(data, list) else [data]
    validated = []
    errors = []
    for item in items:
        try:
            validated.append(model.model_validate(item))
        except Exception as e:
            errors.append({"item": item, "error": str(e)})

    return validated, errors
```

## Prompt Engineering for Extraction

### Principles

1. **Be specific about fields**: Name every field, its type, and format
2. **Define output structure**: Show the exact JSON shape expected
3. **Handle edge cases**: Specify what to do with missing data
4. **Include business logic**: Currency conversion, unit normalization

### Effective Prompt Template

```
Extract the following information from this web page.

Fields to extract:
- title (string): The listing title
- price (number): The monthly rental price as a number, no formatting
- currency (string): "USD" or "ARS"
- m2 (number): Total square meters, null if not available
- location (string): Neighborhood or area name

Rules:
- If price shows "$" symbol, currency is "ARS"
- If price shows "U$S" or "USD", currency is "USD"
- If a field is not found, use null
- Return a JSON array of objects

Output format:
[{"title": "...", "price": 1500, "currency": "USD", "m2": 85, "location": "Palermo"}]
```

### Anti-Hallucination Tips

- Set `temperature=0` for extraction tasks
- Ask the model to return `null` rather than guess
- Validate output against known constraints (price ranges, geographic bounds)
- Cross-check extracted counts against expected totals
- Use Pydantic validation as a second check

## Error Handling for LLM Extraction

### Common Failure Modes

| Error Type | Cause | Mitigation |
|---|---|---|
| Invalid JSON | LLM wraps in markdown or adds commentary | Strip code blocks, use `response_format=json` |
| Token limit exceeded | Page content too large for context | Chunk content, extract per-section |
| Hallucinated data | LLM invents plausible values | Validate against schema + range checks |
| Rate limit (429) | Too many API calls | Exponential backoff, queue requests |
| Incomplete extraction | LLM misses some items | Compare count vs expected, re-extract missing |

### Retry with Validation

```python
async def extract_with_retry(content, prompt, schema, max_retries=3):
    for attempt in range(max_retries):
        try:
            raw = await call_llm(content, prompt)
            validated, errors = parse_llm_output(raw, schema)
            if errors and attempt < max_retries - 1:
                # Retry with error feedback
                prompt += f"\nPrevious attempt had {len(errors)} validation errors. Be more careful with: {errors[0]['error']}"
                continue
            return validated, errors
        except json.JSONDecodeError:
            if attempt == max_retries - 1:
                raise
            continue
```

### Multi-Model Fallback

```python
MODELS = [
    {"model": "gpt-4o-mini", "provider": "openai"},      # fast + cheap
    {"model": "gpt-4o", "provider": "openai"},            # more capable
    {"model": "claude-sonnet-4-5-20250929", "provider": "anthropic"},  # alternative
]

async def extract_with_fallback(content, prompt, schema):
    for model_config in MODELS:
        try:
            return await extract(content, prompt, schema, **model_config)
        except Exception as e:
            logging.warning(f"Model {model_config['model']} failed: {e}")
    raise RuntimeError("All models failed")
```

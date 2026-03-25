# plasmate-audit

Site auditing powered by [Plasmate](https://plasmate.app) - 10x faster than Chrome-based tools.

## Install

```bash
pip install plasmate plasmate-audit
```

## Quick Start

```bash
# Audit a site (crawls up to 50 pages)
plasmate-audit https://example.com

# More pages
plasmate-audit https://example.com --max-pages 200

# JSON output
plasmate-audit https://example.com --json
```

## Python API

```python
from plasmate_audit import audit_site

result = audit_site("https://example.com", max_pages=50)
print(f"Score: {result['score']}/100")
print(f"Pages: {result['pages_crawled']}")
print(f"Issues: {result['errors']} errors, {result['warnings']} warnings")
```

## What It Checks

| Check | Severity | Description |
|-------|----------|-------------|
| missing-title | Error | Page has no title |
| title-too-long | Warning | Title >60 characters |
| title-too-short | Warning | Title <10 characters |
| no-h1 | Error | No H1 heading |
| multiple-h1 | Warning | More than one H1 |
| no-headings | Warning | No headings at all |
| empty-links | Warning | Links with no text |
| thin-content | Warning | Pages with <100 chars of content |
| images-no-alt | Error | Images without alt text |

## Why Plasmate?

Screaming Frog and Lighthouse use Chrome to render every page. Plasmate skips rendering:

| Tool | Speed (100 pages) | Memory |
|------|-------------------|--------|
| Screaming Frog | ~5 minutes | 2GB+ |
| Lighthouse | ~15 minutes | 500MB+ |
| plasmate-audit | ~30 seconds | 50MB |

## How It Works

1. **Crawl** — Start from a URL, discover internal links via Plasmate's SOM
2. **Analyze** — Run SEO/content checks against each page's structured object model
3. **Report** — Get a score, issue list, and per-page breakdown

No headless browser. No JavaScript execution. Just fast, structured analysis.

## Links

- [Plasmate](https://plasmate.app)
- [W3C Community Group](https://www.w3.org/community/web-content-browser-ai/)

## License

Apache 2.0

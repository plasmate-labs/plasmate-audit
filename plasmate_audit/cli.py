#!/usr/bin/env python3
"""CLI for plasmate-audit."""
import sys
import json
from .crawl import audit_site
from .report import format_report


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else None
    if not url or url.startswith('--'):
        print("Usage: plasmate-audit <url> [--max-pages 50] [--json]")
        sys.exit(1)

    max_pages = 50
    output_json = '--json' in sys.argv

    for i, arg in enumerate(sys.argv):
        if arg == '--max-pages' and i + 1 < len(sys.argv):
            max_pages = int(sys.argv[i + 1])

    result = audit_site(url, max_pages=max_pages)

    if output_json:
        print(json.dumps(result, indent=2))
    else:
        print(format_report(result))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Example: Audit a site and print results."""

from plasmate_audit import audit_site

# Audit a site (crawls up to 20 pages)
result = audit_site("https://example.com", max_pages=20)

# Print summary
print(f"Score: {result['score']}/100")
print(f"Pages crawled: {result['pages_crawled']}")
print(f"Errors: {result['errors']}")
print(f"Warnings: {result['warnings']}")
print()

# Print each issue
for issue in result["issues"]:
    icon = "✗" if issue["severity"] == "error" else "⚠"
    print(f"  {icon} [{issue['rule']}] {issue['message']}")
    print(f"    {issue['url']}")
print()

# Pages with most issues
print("Pages by issue count:")
for page in sorted(result["pages"], key=lambda p: -p["issues"]):
    print(f"  {page['issues']} issues — {page['title'] or '(no title)'}")
    print(f"    {page['url']}")

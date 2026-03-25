"""Crawl a site using Plasmate and run audit checks."""
import subprocess
import json
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from .checks import ALL_CHECKS


def fetch_som(url: str, timeout: int = 30) -> dict | None:
    """Fetch the SOM for a URL using Plasmate."""
    try:
        result = subprocess.run(
            ["plasmate", "fetch", url],
            capture_output=True, text=True, timeout=timeout,
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception:
        pass
    return None


def extract_internal_links(som: dict, base_url: str) -> list:
    """Extract internal links from SOM."""
    base_domain = urlparse(base_url).netloc
    links = set()
    for region in som.get('regions', []):
        for el in region.get('elements', []):
            href = el.get('attrs', {}).get('href', '')
            if href:
                full_url = urljoin(base_url, href)
                if urlparse(full_url).netloc == base_domain:
                    links.add(full_url.split('#')[0].split('?')[0])
    return list(links)


def audit_site(
    start_url: str,
    max_pages: int = 50,
    max_concurrent: int = 5,
    timeout: int = 30,
) -> dict:
    """Crawl and audit a site.

    Args:
        start_url: The URL to start crawling from.
        max_pages: Maximum number of pages to crawl.
        max_concurrent: Maximum concurrent Plasmate fetches.
        timeout: Timeout per page fetch in seconds.

    Returns:
        A dict with audit results including score, issues, and page details.
    """
    visited: set[str] = set()
    to_visit = [start_url]
    all_issues: list[dict] = []
    page_results: list[dict] = []

    while to_visit and len(visited) < max_pages:
        batch = []
        while to_visit and len(batch) < max_concurrent:
            url = to_visit.pop(0)
            if url not in visited:
                visited.add(url)
                batch.append(url)

        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            futures = {executor.submit(fetch_som, url, timeout): url for url in batch}
            for future in as_completed(futures):
                url = futures[future]
                som = future.result()
                if som:
                    # Run checks
                    page_issues: list[dict] = []
                    for check in ALL_CHECKS:
                        page_issues.extend(check(som, url))
                    all_issues.extend(page_issues)

                    page_results.append({
                        'url': url,
                        'title': som.get('title', ''),
                        'issues': len(page_issues),
                        'regions': len(som.get('regions', [])),
                    })

                    # Discover new links
                    new_links = extract_internal_links(som, url)
                    for link in new_links:
                        if link not in visited:
                            to_visit.append(link)

    errors = sum(1 for i in all_issues if i['severity'] == 'error')
    warnings = sum(1 for i in all_issues if i['severity'] == 'warning')

    return {
        'start_url': start_url,
        'pages_crawled': len(visited),
        'total_issues': len(all_issues),
        'errors': errors,
        'warnings': warnings,
        'score': max(0, 100 - (errors * 5) - (warnings * 2)),
        'issues': all_issues,
        'pages': page_results,
    }

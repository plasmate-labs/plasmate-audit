"""Site audit checks powered by Plasmate SOM analysis."""


def check_title(som: dict, url: str) -> list:
    """Check page title exists and is reasonable length."""
    issues = []
    title = som.get('title', '')
    if not title:
        issues.append({'rule': 'missing-title', 'severity': 'error', 'url': url, 'message': 'Page has no title'})
    elif len(title) > 60:
        issues.append({'rule': 'title-too-long', 'severity': 'warning', 'url': url, 'message': f'Title is {len(title)} chars (recommended: <60)', 'value': title})
    elif len(title) < 10:
        issues.append({'rule': 'title-too-short', 'severity': 'warning', 'url': url, 'message': f'Title is only {len(title)} chars', 'value': title})
    return issues


def check_headings(som: dict, url: str) -> list:
    """Check heading structure."""
    issues = []
    headings = []
    for region in som.get('regions', []):
        for el in region.get('elements', []):
            if el.get('role') == 'heading':
                headings.append(el)

    h1s = [h for h in headings if h.get('attrs', {}).get('level') == 1]
    if len(h1s) == 0:
        issues.append({'rule': 'no-h1', 'severity': 'error', 'url': url, 'message': 'Page has no H1 heading'})
    elif len(h1s) > 1:
        issues.append({'rule': 'multiple-h1', 'severity': 'warning', 'url': url, 'message': f'Page has {len(h1s)} H1 headings (should be 1)'})

    if len(headings) == 0:
        issues.append({'rule': 'no-headings', 'severity': 'warning', 'url': url, 'message': 'Page has no headings at all'})

    return issues


def check_links(som: dict, url: str) -> list:
    """Check links for issues."""
    issues = []
    links = []
    for region in som.get('regions', []):
        for el in region.get('elements', []):
            if el.get('role') == 'link':
                links.append(el)

    # Check for links with no text
    empty_links = [l for l in links if not l.get('text', '').strip()]
    if empty_links:
        issues.append({'rule': 'empty-links', 'severity': 'warning', 'url': url, 'message': f'{len(empty_links)} links have no text'})

    return issues


def check_content_length(som: dict, url: str) -> list:
    """Check that pages have sufficient content."""
    issues = []
    text_length = 0
    for region in som.get('regions', []):
        for el in region.get('elements', []):
            text_length += len(el.get('text', ''))

    if text_length < 100:
        issues.append({'rule': 'thin-content', 'severity': 'warning', 'url': url, 'message': f'Page has very little content ({text_length} chars)'})

    return issues


def check_images(som: dict, url: str) -> list:
    """Check images for alt text."""
    issues = []
    images_without_alt = 0
    total_images = 0
    for region in som.get('regions', []):
        for el in region.get('elements', []):
            if el.get('role') == 'image':
                total_images += 1
                if not el.get('attrs', {}).get('alt'):
                    images_without_alt += 1

    if images_without_alt > 0:
        issues.append({'rule': 'images-no-alt', 'severity': 'error', 'url': url, 'message': f'{images_without_alt}/{total_images} images missing alt text'})

    return issues


ALL_CHECKS = [check_title, check_headings, check_links, check_content_length, check_images]

"""Format audit results as a clean terminal report."""

# ANSI color codes
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
CYAN = "\033[96m"


def _score_color(score: int) -> str:
    if score >= 80:
        return GREEN
    elif score >= 50:
        return YELLOW
    return RED


def _severity_icon(severity: str) -> str:
    if severity == "error":
        return f"{RED}✗{RESET}"
    return f"{YELLOW}⚠{RESET}"


def format_report(result: dict) -> str:
    """Format audit results as a colored terminal report."""
    lines: list[str] = []

    # Header
    lines.append("")
    lines.append(f"{BOLD}╔══════════════════════════════════════════════════╗{RESET}")
    lines.append(f"{BOLD}║         plasmate-audit  Site Report              ║{RESET}")
    lines.append(f"{BOLD}╚══════════════════════════════════════════════════╝{RESET}")
    lines.append("")

    # Score
    score = result["score"]
    color = _score_color(score)
    lines.append(f"  {BOLD}Score:{RESET}  {color}{BOLD}{score}/100{RESET}")
    lines.append(f"  {BOLD}URL:{RESET}    {result['start_url']}")
    lines.append(f"  {BOLD}Pages:{RESET}  {result['pages_crawled']}")
    lines.append("")

    # Summary bar
    errors = result["errors"]
    warnings = result["warnings"]
    lines.append(f"  {RED}{BOLD}{errors} errors{RESET}  ·  {YELLOW}{BOLD}{warnings} warnings{RESET}")
    lines.append("")

    # Issues grouped by rule
    if result["issues"]:
        lines.append(f"{BOLD}  Issues{RESET}")
        lines.append(f"  {'─' * 48}")

        # Group by rule
        by_rule: dict[str, list[dict]] = {}
        for issue in result["issues"]:
            rule = issue["rule"]
            by_rule.setdefault(rule, []).append(issue)

        for rule, issues in sorted(by_rule.items()):
            icon = _severity_icon(issues[0]["severity"])
            count = len(issues)
            msg = issues[0]["message"]
            if count > 1:
                lines.append(f"  {icon} {BOLD}{rule}{RESET} {DIM}({count} pages){RESET}")
            else:
                lines.append(f"  {icon} {BOLD}{rule}{RESET}")
            for issue in issues[:5]:  # Show up to 5 URLs per rule
                lines.append(f"    {DIM}└ {issue['url']}{RESET}")
                if "value" in issue:
                    lines.append(f"      {DIM}{issue['value'][:80]}{RESET}")
            if count > 5:
                lines.append(f"    {DIM}└ ... and {count - 5} more{RESET}")
            lines.append("")
    else:
        lines.append(f"  {GREEN}{BOLD}✓ No issues found!{RESET}")
        lines.append("")

    # Pages summary
    lines.append(f"{BOLD}  Pages Crawled{RESET}")
    lines.append(f"  {'─' * 48}")
    for page in sorted(result["pages"], key=lambda p: -p["issues"]):
        issue_count = page["issues"]
        if issue_count > 0:
            indicator = f"{RED}{issue_count} issues{RESET}"
        else:
            indicator = f"{GREEN}✓{RESET}"
        title = page["title"][:40] if page["title"] else f"{DIM}(no title){RESET}"
        lines.append(f"  {indicator}  {title}")
        lines.append(f"         {DIM}{page['url']}{RESET}")
    lines.append("")

    # Footer
    lines.append(f"  {DIM}Powered by Plasmate · https://plasmate.app{RESET}")
    lines.append("")

    return "\n".join(lines)

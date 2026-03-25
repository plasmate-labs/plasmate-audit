"""plasmate-audit: Site auditing powered by Plasmate."""

from .crawl import audit_site
from .checks import ALL_CHECKS

__all__ = ["audit_site", "ALL_CHECKS"]
__version__ = "0.1.0"

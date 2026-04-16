"""
TokenSpot - Smart API Key Discovery & Validation for Bug Hunters
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "Find and validate exposed API keys with permission context"

from .scanner import TokenScanner
from .validators import VALIDATORS

__all__ = ["TokenScanner", "VALIDATORS"]

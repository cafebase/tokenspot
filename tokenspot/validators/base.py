"""
Base validator classes for TokenSpot.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional, List
import requests


class Severity(Enum):
    """Severity levels for findings."""
    CRITICAL = "🔴 CRITICAL"
    HIGH = "🟠 HIGH"
    MEDIUM = "🟡 MEDIUM"
    LOW = "🟢 LOW"
    INFO = "⚪ INFO"


@dataclass
class ValidationResult:
    """Standardized result from any validator."""
    service: str
    key: str
    is_valid: bool
    severity: Severity
    permissions: List[str] = field(default_factory=list)
    account_info: Optional[str] = None
    raw_response: Optional[Dict] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON output."""
        return {
            'service': self.service,
            'key': self.key[:8] + '...' + self.key[-4:] if len(self.key) > 12 else self.key,
            'full_key': self.key,  # Included in JSON for automation
            'is_valid': self.is_valid,
            'severity': self.severity.value,
            'permissions': self.permissions,
            'account_info': self.account_info,
            'error_message': self.error_message
        }


class BaseValidator(ABC):
    """Abstract base class for all API key validators."""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TokenSpot/1.0 (Security Research Tool - Educational Use Only)'
        })
    
    @abstractmethod
    def validate(self, key: str) -> ValidationResult:
        """Validate the API key and determine its permissions."""
        pass
    
    @abstractmethod
    def get_pattern(self) -> str:
        """Return regex pattern that identifies this service's keys."""
        pass
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Wrapper for HTTP requests with timeout."""
        kwargs.setdefault('timeout', self.timeout)
        return self.session.request(method, url, **kwargs)

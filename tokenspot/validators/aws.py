"""
AWS key validator for TokenSpot.
"""

import hmac
import hashlib
import datetime
from .base import BaseValidator, ValidationResult, Severity


class AWSValidator(BaseValidator):
    """Validates AWS Access Keys."""
    
    def get_pattern(self) -> str:
        return r'AKIA[A-Z0-9]{16}'
    
    def validate(self, key: str) -> ValidationResult:
        # AWS validation requires both access key AND secret key
        # We can only detect the pattern for access key
        return ValidationResult(
            service='AWS',
            key=key,
            is_valid=None,  # Cannot validate without secret
            severity=Severity.MEDIUM,
            permissions=['unknown'],
            account_info="AWS Access Key ID (requires secret for validation)",
            error_message="Secret key required for full validation"
        )

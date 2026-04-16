"""
GitHub token validator for TokenSpot.
"""

from .base import BaseValidator, ValidationResult, Severity


class GitHubValidator(BaseValidator):
    """Validates GitHub Personal Access Tokens."""
    
    def get_pattern(self) -> str:
        return r'ghp_[a-zA-Z0-9]{36}'
    
    def validate(self, key: str) -> ValidationResult:
        try:
            response = self._make_request(
                'GET',
                'https://api.github.com/user',
                headers={'Authorization': f'token {key}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                scopes = response.headers.get('X-OAuth-Scopes', '').split(', ')
                
                # Determine severity based on scopes
                if 'repo' in scopes or 'admin:org' in scopes or 'workflow' in scopes:
                    severity = Severity.CRITICAL
                elif 'user' in scopes or 'gist' in scopes or 'read:org' in scopes:
                    severity = Severity.MEDIUM
                else:
                    severity = Severity.LOW
                
                return ValidationResult(
                    service='GitHub',
                    key=key,
                    is_valid=True,
                    severity=severity,
                    permissions=scopes if scopes != [''] else ['public_only'],
                    account_info=f"{data.get('login', 'unknown')} ({data.get('type', 'User')})",
                    raw_response={'login': data.get('login'), 'id': data.get('id')},
                    error_message=None
                )
            
            elif response.status_code == 401:
                return ValidationResult(
                    service='GitHub',
                    key=key,
                    is_valid=False,
                    severity=Severity.INFO,
                    permissions=[],
                    account_info=None,
                    error_message="Invalid or expired token"
                )
            
            elif response.status_code == 403:
                return ValidationResult(
                    service='GitHub',
                    key=key,
                    is_valid=True,  # Token is valid but rate limited
                    severity=Severity.MEDIUM,
                    permissions=['rate_limited'],
                    account_info="Rate limited - cannot enumerate",
                    error_message="Rate limited"
                )
            
            else:
                return ValidationResult(
                    service='GitHub',
                    key=key,
                    is_valid=False,
                    severity=Severity.INFO,
                    permissions=[],
                    error_message=f"HTTP {response.status_code}"
                )
                
        except Exception as e:
            return ValidationResult(
                service='GitHub',
                key=key,
                is_valid=False,
                severity=Severity.INFO,
                permissions=[],
                error_message=str(e)
            )

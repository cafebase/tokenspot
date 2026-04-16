"""
OpenAI key validator for TokenSpot.
"""

from .base import BaseValidator, ValidationResult, Severity


class OpenAIValidator(BaseValidator):
    """Validates OpenAI API keys."""
    
    def get_pattern(self) -> str:
        return r'sk-[a-zA-Z0-9-_]{48}'
    
    def validate(self, key: str) -> ValidationResult:
        try:
            response = self._make_request(
                'GET',
                'https://api.openai.com/v1/models',
                headers={'Authorization': f'Bearer {key}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('data', [])
                model_count = len(models)
                
                # Check for billing/organization info
                return ValidationResult(
                    service='OpenAI',
                    key=key,
                    is_valid=True,
                    severity=Severity.CRITICAL,
                    permissions=[f'access_to_{model_count}_models'],
                    account_info=f"Valid key - {model_count} models accessible",
                    raw_response={'model_count': model_count},
                    error_message=None
                )
            
            elif response.status_code == 401:
                return ValidationResult(
                    service='OpenAI',
                    key=key,
                    is_valid=False,
                    severity=Severity.INFO,
                    permissions=[],
                    error_message="Invalid API key"
                )
            
            elif response.status_code == 429:
                return ValidationResult(
                    service='OpenAI',
                    key=key,
                    is_valid=True,  # Key is valid but rate limited
                    severity=Severity.MEDIUM,
                    permissions=['rate_limited'],
                    account_info="Rate limited - key appears valid",
                    error_message="Rate limited"
                )
                
        except Exception as e:
            return ValidationResult(
                service='OpenAI',
                key=key,
                is_valid=False,
                severity=Severity.INFO,
                permissions=[],
                error_message=str(e)
            )

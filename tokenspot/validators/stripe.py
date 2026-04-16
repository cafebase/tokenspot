"""
Stripe key validator for TokenSpot.
"""

from .base import BaseValidator, ValidationResult, Severity


class StripeValidator(BaseValidator):
    """Validates Stripe API keys and determines permissions."""
    
    def get_pattern(self) -> str:
        return r'(?:sk|pk)_(?:live|test)_[a-zA-Z0-9]{24,99}'
    
    def validate(self, key: str) -> ValidationResult:
        try:
            is_secret = key.startswith('sk_')
            is_live = '_live_' in key
            
            # Publishable keys are low risk
            if not is_secret:
                return ValidationResult(
                    service='Stripe',
                    key=key,
                    is_valid=True,
                    severity=Severity.LOW,
                    permissions=['public_only'],
                    account_info=f"{'Live' if is_live else 'Test'} mode - Publishable key",
                    error_message=None
                )
            
            # Test secret key
            response = self._make_request(
                'GET',
                'https://api.stripe.com/v1/account',
                auth=(key, '')
            )
            
            if response.status_code == 200:
                data = response.json()
                permissions = []
                
                # Check capabilities
                if data.get('charges_enabled', False):
                    permissions.append('charges')
                    permissions.append('refunds')
                if data.get('payouts_enabled', False):
                    permissions.append('payouts')
                if data.get('details_submitted', False):
                    permissions.append('verified_account')
                
                severity = Severity.CRITICAL if 'charges' in permissions else Severity.HIGH
                
                return ValidationResult(
                    service='Stripe',
                    key=key,
                    is_valid=True,
                    severity=severity,
                    permissions=permissions or ['read_only'],
                    account_info=f"{data.get('display_name', data.get('id', 'Unknown'))} ({'Live' if is_live else 'Test'})",
                    raw_response={'id': data.get('id'), 'country': data.get('country')},
                    error_message=None
                )
            
            elif response.status_code == 401:
                return ValidationResult(
                    service='Stripe',
                    key=key,
                    is_valid=False,
                    severity=Severity.INFO,
                    permissions=[],
                    error_message="Invalid API key"
                )
            
        except Exception as e:
            return ValidationResult(
                service='Stripe',
                key=key,
                is_valid=False,
                severity=Severity.INFO,
                permissions=[],
                error_message=str(e)
            )

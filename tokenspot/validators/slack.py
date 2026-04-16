"""
Slack token validator for TokenSpot.
"""

from .base import BaseValidator, ValidationResult, Severity


class SlackValidator(BaseValidator):
    """Validates Slack tokens and webhooks."""
    
    def get_pattern(self) -> str:
        return r'xox[abp]-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{24}'
    
    def validate(self, key: str) -> ValidationResult:
        try:
            # Handle webhooks differently
            if key.startswith('https://hooks.slack.com/'):
                return self._validate_webhook(key)
            
            # Test bot/user token
            response = self._make_request(
                'POST',
                'https://slack.com/api/auth.test',
                headers={'Authorization': f'Bearer {key}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('ok', False):
                    # Get scopes
                    scopes_response = self._make_request(
                        'GET',
                        'https://slack.com/api/auth.teams.list',
                        headers={'Authorization': f'Bearer {key}'}
                    )
                    
                    permissions = []
                    severity = Severity.MEDIUM
                    
                    if scopes_response.status_code == 200:
                        scopes_data = scopes_response.json()
                        # Extract scopes if available
                    
                    # Check for dangerous scopes
                    dangerous_scopes = ['admin', 'files:write', 'chat:write', 'users:read']
                    
                    return ValidationResult(
                        service='Slack',
                        key=key,
                        is_valid=True,
                        severity=Severity.HIGH if key.startswith('xoxb-') else Severity.MEDIUM,
                        permissions=['active_token'],
                        account_info=f"{data.get('user', 'Unknown')} @ {data.get('team', 'Unknown')}",
                        raw_response={'user': data.get('user'), 'team': data.get('team')},
                        error_message=None
                    )
                else:
                    return ValidationResult(
                        service='Slack',
                        key=key,
                        is_valid=False,
                        severity=Severity.INFO,
                        permissions=[],
                        error_message=data.get('error', 'Invalid token')
                    )
            
        except Exception as e:
            return ValidationResult(
                service='Slack',
                key=key,
                is_valid=False,
                severity=Severity.INFO,
                permissions=[],
                error_message=str(e)
            )
    
    def _validate_webhook(self, url: str) -> ValidationResult:
        """Validate a Slack webhook URL."""
        try:
            # Send a test message (non-intrusive)
            import json
            response = self._make_request(
                'POST',
                url,
                json={'text': 'TokenSpot validation test - please ignore'},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200 and response.text == 'ok':
                return ValidationResult(
                    service='Slack',
                    key=url,
                    is_valid=True,
                    severity=Severity.HIGH,
                    permissions=['webhook_post'],
                    account_info='Webhook URL',
                    error_message=None
                )
            else:
                return ValidationResult(
                    service='Slack',
                    key=url,
                    is_valid=False,
                    severity=Severity.INFO,
                    permissions=[],
                    error_message=f"Invalid webhook (HTTP {response.status_code})"
                )
                
        except Exception as e:
            return ValidationResult(
                service='Slack',
                key=url,
                is_valid=False,
                severity=Severity.INFO,
                permissions=[],
                error_message=str(e)
            )

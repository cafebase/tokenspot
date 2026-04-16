"""
Validator registry for TokenSpot.
"""

from .base import BaseValidator, ValidationResult, Severity
from .github import GitHubValidator
from .stripe import StripeValidator
from .aws import AWSValidator
from .slack import SlackValidator
from .openai import OpenAIValidator

# Registry mapping service names to validator classes
VALIDATORS = {
    'github': GitHubValidator,
    'github_oauth': GitHubValidator,  # Uses same validator
    'stripe': StripeValidator,
    'aws_access_key': AWSValidator,
    'slack_bot': SlackValidator,
    'slack_user': SlackValidator,
    'slack_webhook': SlackValidator,
    'openai': OpenAIValidator,
    'openai_project': OpenAIValidator,
}


def get_validator(service: str):
    """Get a validator instance for a given service."""
    validator_class = VALIDATORS.get(service.lower())
    if validator_class:
        return validator_class()
    return None


__all__ = [
    'BaseValidator',
    'ValidationResult',
    'Severity',
    'VALIDATORS',
    'get_validator',
    'GitHubValidator',
    'StripeValidator',
    'AWSValidator',
    'SlackValidator',
    'OpenAIValidator',
]

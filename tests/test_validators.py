"""
Unit tests for TokenSpot validators.
"""

import unittest
from unittest.mock import patch, MagicMock
from tokenspot.validators import (
    GitHubValidator,
    StripeValidator,
    AWSValidator,
    SlackValidator,
    OpenAIValidator,
    Severity,
    ValidationResult
)


class TestGitHubValidator(unittest.TestCase):
    """Tests for GitHub token validation."""
    
    def setUp(self):
        self.validator = GitHubValidator()
        self.sample_key = "ghp_1234567890abcdefghijklmnopqrstuvwxyz123456"
    
    def test_pattern(self):
        """Test that pattern matches GitHub tokens."""
        pattern = self.validator.get_pattern()
        self.assertIn('ghp_', pattern)
    
    @patch('requests.Session.request')
    def test_valid_token_with_scopes(self, mock_request):
        """Test validation of a valid token with scopes."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'X-OAuth-Scopes': 'repo, user'}
        mock_response.json.return_value = {'login': 'testuser', 'type': 'User'}
        mock_request.return_value = mock_response
        
        result = self.validator.validate(self.sample_key)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.severity, Severity.CRITICAL)
        self.assertIn('repo', result.permissions)
        self.assertEqual(result.account_info, 'testuser (User)')
    
    @patch('requests.Session.request')
    def test_invalid_token(self, mock_request):
        """Test validation of an invalid token."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_request.return_value = mock_response
        
        result = self.validator.validate(self.sample_key)
        
        self.assertFalse(result.is_valid)
        self.assertEqual(result.severity, Severity.INFO)
        self.assertIn('Invalid', result.error_message)
    
    @patch('requests.Session.request')
    def test_rate_limited_token(self, mock_request):
        """Test handling of rate-limited responses."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_request.return_value = mock_response
        
        result = self.validator.validate(self.sample_key)
        
        self.assertTrue(result.is_valid)  # Token likely valid but rate limited
        self.assertEqual(result.severity, Severity.MEDIUM)


class TestStripeValidator(unittest.TestCase):
    """Tests for Stripe key validation."""
    
    def setUp(self):
        self.validator = StripeValidator()
        self.secret_key = "sk_live_51ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        self.publishable_key = "pk_test_1234567890abcdefghijklmnopqrstuvwxyz"
    
    def test_pattern(self):
        """Test that pattern matches Stripe keys."""
        pattern = self.validator.get_pattern()
        # Pattern uses regex grouping - check for components
        self.assertIn('sk', pattern)
        self.assertIn('pk', pattern)
        self.assertIn('live', pattern)
        self.assertIn('test', pattern)
    
    @patch('requests.Session.request')
    def test_publishable_key(self, mock_request):
        """Test that publishable keys are flagged as low severity."""
        result = self.validator.validate(self.publishable_key)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.severity, Severity.LOW)
        self.assertIn('public_only', result.permissions)
    
    @patch('requests.Session.request')
    def test_valid_secret_key_with_charges(self, mock_request):
        """Test validation of a secret key with charge permissions."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 'acct_123',
            'display_name': 'Test Business',
            'charges_enabled': True,
            'payouts_enabled': True,
            'details_submitted': True
        }
        mock_request.return_value = mock_response
        
        result = self.validator.validate(self.secret_key)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.severity, Severity.CRITICAL)
        self.assertIn('charges', result.permissions)
        self.assertIn('refunds', result.permissions)
        self.assertIn('payouts', result.permissions)
    
    @patch('requests.Session.request')
    def test_valid_secret_key_readonly(self, mock_request):
        """Test validation of a secret key with only read access."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 'acct_123',
            'display_name': 'Test Business',
            'charges_enabled': False,
            'payouts_enabled': False
        }
        mock_request.return_value = mock_response
        
        result = self.validator.validate(self.secret_key)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.severity, Severity.HIGH)
        self.assertIn('read_only', result.permissions)
    
    @patch('requests.Session.request')
    def test_invalid_secret_key(self, mock_request):
        """Test validation of an invalid secret key."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_request.return_value = mock_response
        
        result = self.validator.validate(self.secret_key)
        
        self.assertFalse(result.is_valid)
        self.assertEqual(result.severity, Severity.INFO)


class TestAWSValidator(unittest.TestCase):
    """Tests for AWS key validation."""
    
    def setUp(self):
        self.validator = AWSValidator()
        self.access_key = "AKIAIOSFODNN7EXAMPLE"
    
    def test_pattern(self):
        """Test that pattern matches AWS access keys."""
        pattern = self.validator.get_pattern()
        self.assertIn('AKIA', pattern)
    
    def test_validation_without_secret(self):
        """Test that access key alone returns unknown status."""
        result = self.validator.validate(self.access_key)
        
        self.assertIsNone(result.is_valid)
        self.assertEqual(result.severity, Severity.MEDIUM)
        self.assertIn('Secret key required', result.error_message)


class TestSlackValidator(unittest.TestCase):
    """Tests for Slack token validation."""
    
    def setUp(self):
        self.validator = SlackValidator()
        self.bot_token = "xoxb-123456789012-123456789012-abcdefghijklmnopqrstuvwx"
        self.webhook_url = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
    
    def test_pattern(self):
        """Test that pattern matches Slack tokens."""
        pattern = self.validator.get_pattern()
        self.assertIn('xox', pattern)
    
    @patch('requests.Session.request')
    def test_valid_bot_token(self, mock_request):
        """Test validation of a valid bot token."""
        # Mock auth.test response
        mock_response1 = MagicMock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = {
            'ok': True,
            'user': 'testbot',
            'team': 'testworkspace',
            'url': 'https://testworkspace.slack.com/'
        }
        
        # Mock auth.teams.list response
        mock_response2 = MagicMock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = {'ok': True, 'teams': []}
        
        mock_request.side_effect = [mock_response1, mock_response2]
        
        result = self.validator.validate(self.bot_token)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.severity, Severity.HIGH)
        self.assertEqual(result.account_info, 'testbot @ testworkspace')
    
    @patch('requests.Session.request')
    def test_invalid_token(self, mock_request):
        """Test validation of an invalid token."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'ok': False,
            'error': 'invalid_auth'
        }
        mock_request.return_value = mock_response
        
        result = self.validator.validate(self.bot_token)
        
        self.assertFalse(result.is_valid)
        self.assertEqual(result.severity, Severity.INFO)
    
    @patch('requests.Session.request')
    def test_valid_webhook(self, mock_request):
        """Test validation of a valid webhook URL."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'ok'
        mock_request.return_value = mock_response
        
        result = self.validator.validate(self.webhook_url)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.severity, Severity.HIGH)
        self.assertIn('webhook_post', result.permissions)


class TestOpenAIValidator(unittest.TestCase):
    """Tests for OpenAI key validation."""
    
    def setUp(self):
        self.validator = OpenAIValidator()
        self.api_key = "sk-1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNO"
    
    def test_pattern(self):
        """Test that pattern matches OpenAI keys."""
        pattern = self.validator.get_pattern()
        self.assertIn('sk-', pattern)
    
    @patch('requests.Session.request')
    def test_valid_key(self, mock_request):
        """Test validation of a valid API key."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': [{'id': 'gpt-4'}, {'id': 'gpt-3.5-turbo'}, {'id': 'text-embedding'}]
        }
        mock_request.return_value = mock_response
        
        result = self.validator.validate(self.api_key)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.severity, Severity.CRITICAL)
        self.assertIn('access_to_3_models', result.permissions)
    
    @patch('requests.Session.request')
    def test_invalid_key(self, mock_request):
        """Test validation of an invalid API key."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_request.return_value = mock_response
        
        result = self.validator.validate(self.api_key)
        
        self.assertFalse(result.is_valid)
        self.assertEqual(result.severity, Severity.INFO)
    
    @patch('requests.Session.request')
    def test_rate_limited_key(self, mock_request):
        """Test handling of rate-limited responses."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_request.return_value = mock_response
        
        result = self.validator.validate(self.api_key)
        
        self.assertTrue(result.is_valid)
        self.assertEqual(result.severity, Severity.MEDIUM)
        self.assertIn('Rate limited', result.account_info)


class TestValidationResult(unittest.TestCase):
    """Tests for ValidationResult dataclass."""
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        result = ValidationResult(
            service='TestService',
            key='test_key_1234567890abcdefghijklmnopqrstuvwxyz',
            is_valid=True,
            severity=Severity.HIGH,
            permissions=['read', 'write'],
            account_info='Test Account',
            error_message=None
        )
        
        result_dict = result.to_dict()
        
        self.assertEqual(result_dict['service'], 'TestService')
        self.assertEqual(result_dict['is_valid'], True)
        self.assertEqual(result_dict['severity'], '🟠 HIGH')
        self.assertIn('read', result_dict['permissions'])
        self.assertEqual(result_dict['account_info'], 'Test Account')
        
        # Check key masking
        self.assertIn('...', result_dict['key'])
        self.assertNotEqual(result_dict['key'], 'test_key_1234567890abcdefghijklmnopqrstuvwxyz')
    
    def test_to_dict_short_key(self):
        """Test masking for very short keys."""
        result = ValidationResult(
            service='TestService',
            key='short',
            is_valid=True,
            severity=Severity.LOW,
            permissions=[],
            account_info=None,
            error_message=None
        )
        
        result_dict = result.to_dict()
        
        # Should handle short keys gracefully
        self.assertIsNotNone(result_dict['key'])


class TestSeverityEnum(unittest.TestCase):
    """Tests for Severity enum."""
    
    def test_severity_values(self):
        """Test that severity values are as expected."""
        self.assertEqual(Severity.CRITICAL.value, '🔴 CRITICAL')
        self.assertEqual(Severity.HIGH.value, '🟠 HIGH')
        self.assertEqual(Severity.MEDIUM.value, '🟡 MEDIUM')
        self.assertEqual(Severity.LOW.value, '🟢 LOW')
        self.assertEqual(Severity.INFO.value, '⚪ INFO')


if __name__ == '__main__':
    unittest.main()

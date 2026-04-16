"""
Tests for TokenScanner pattern detection.
"""

import unittest
from tokenspot.scanner import TokenScanner


class TestTokenScanner(unittest.TestCase):
    
    def test_github_pattern(self):
        content = 'const GITHUB_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz123456"'
        findings = TokenScanner.scan_text(content)
        # Filter for github findings only (may find other patterns)
        github_findings = [f for f in findings if f['service'] == 'github']
        self.assertEqual(len(github_findings), 1)
    
    def test_stripe_pattern(self):
        content = 'STRIPE_KEY=sk_live_51ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        findings = TokenScanner.scan_text(content)
        stripe_findings = [f for f in findings if f['service'] == 'stripe']
        self.assertGreaterEqual(len(stripe_findings), 1)
    
    def test_multiple_patterns(self):
        content = '''
        GITHUB_KEY=ghp_abc123def456ghi789jkl012mno345pqr678stu901
        OPENAI_KEY=sk-proj-ABCDEFGHIJKLMNOPQRSTUVWXYZ123456
        '''
        findings = TokenScanner.scan_text(content)
        # Count unique services found
        services = set(f['service'] for f in findings)
        self.assertGreaterEqual(len(services), 2)
    
    def test_deduplication(self):
        # Use a properly formatted GitHub token
        content = 'KEY=ghp_1234567890abcdefghijklmnopqrstuvwxyz123456 KEY=ghp_1234567890abcdefghijklmnopqrstuvwxyz123456'
        findings = TokenScanner.scan_text(content)
        github_findings = [f for f in findings if f['service'] == 'github']
        # Should deduplicate identical keys from same source
        self.assertEqual(len(github_findings), 1)


if __name__ == '__main__':
    unittest.main()

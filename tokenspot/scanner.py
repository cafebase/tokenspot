"""
TokenScanner - Pattern detection engine for API keys.
"""

import re
import requests
from pathlib import Path
from typing import List, Dict, Set
from urllib.parse import urlparse


class TokenScanner:
    """Scans content for API key patterns across multiple services."""
    
    # Pattern database
    PATTERNS = {
        'stripe': (r'(?:sk|pk)_(?:live|test)_[a-zA-Z0-9]{24,99}', 'Stripe API key'),
        'github': (r'ghp_[a-zA-Z0-9]{36}', 'GitHub Personal Access Token'),
        'github_oauth': (r'gho_[a-zA-Z0-9]{36}', 'GitHub OAuth Token'),
        'aws_access_key': (r'AKIA[A-Z0-9]{16}', 'AWS Access Key ID'),
        'aws_secret': (r'[A-Za-z0-9/+=]{40}', 'AWS Secret Access Key'),
        'slack_bot': (r'xoxb-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{24}', 'Slack Bot Token'),
        'slack_user': (r'xoxp-[0-9]{12}-[0-9]{12}-[a-zA-Z0-9]{24}', 'Slack User Token'),
        'slack_webhook': (r'https://hooks\.slack\.com/services/T[a-zA-Z0-9_]+/B[a-zA-Z0-9_]+/[a-zA-Z0-9_]+', 'Slack Webhook'),
        'openai': (r'sk-[a-zA-Z0-9-_]{48}', 'OpenAI API Key'),
        'openai_project': (r'sk-proj-[a-zA-Z0-9-_]{32}', 'OpenAI Project Key'),
        'google_api': (r'AIza[0-9A-Za-z-_]{35}', 'Google API Key'),
        'twilio_sid': (r'AC[a-z0-9]{32}', 'Twilio Account SID'),
        'twilio_auth': (r'[a-f0-9]{32}', 'Twilio Auth Token'),
        'mailgun': (r'key-[a-f0-9]{32}', 'Mailgun API Key'),
        'sendgrid': (r'SG\.[a-zA-Z0-9-_]{22}\.[a-zA-Z0-9-_]{43}', 'SendGrid API Key'),
        'jwt': (r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}', 'JWT Token'),
    }
    
    @classmethod
    def scan_text(cls, content: str, source: str = "unknown") -> List[Dict]:
        """Scan text content and return all potential API keys found."""
        findings = []
        
        for service, (pattern, description) in cls.PATTERNS.items():
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                key = match.group(0)
                
                findings.append({
                    'service': service,
                    'key': key,
                    'pattern_description': description,
                    'source': source,
                    'match_position': match.start()
                })
        
        # Deduplicate findings from same source
        seen = set()
        unique_findings = []
        for f in findings:
            key_source = (f['key'], f['source'])
            if key_source not in seen:
                seen.add(key_source)
                unique_findings.append(f)
                
        return unique_findings
    
    @classmethod
    def scan_file(cls, filepath: str) -> List[Dict]:
        """Scan a local file for API keys."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return cls.scan_text(content, source=filepath)
        except Exception as e:
            print(f"  [!] Error reading {filepath}: {e}")
            return []
    
    @classmethod
    def scan_url(cls, url: str, timeout: int = 10) -> List[Dict]:
        """Fetch and scan a URL for API keys."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; TokenSpot/1.0; Security Research Tool)'
            }
            response = requests.get(url, timeout=timeout, headers=headers, verify=True)
            response.raise_for_status()
            return cls.scan_text(response.text, source=url)
        except requests.exceptions.SSLError:
            print(f"  [!] SSL Error for {url}, trying without verification...")
            try:
                response = requests.get(url, timeout=timeout, verify=False)
                return cls.scan_text(response.text, source=url)
            except Exception as e:
                print(f"  [!] Error fetching {url}: {e}")
                return []
        except Exception as e:
            print(f"  [!] Error fetching {url}: {e}")
            return []
    
    @classmethod
    def scan_directory(cls, dirpath: str, extensions: List[str] = None) -> List[Dict]:
        """Recursively scan a directory for files containing API keys."""
        if extensions is None:
            extensions = ['.js', '.json', '.html', '.htm', '.txt', '.py', 
                         '.env', '.yml', '.yaml', '.xml', '.conf', '.config',
                         '.ts', '.jsx', '.tsx', '.vue', '.php', '.rb', '.go']
        
        findings = []
        path = Path(dirpath)
        
        for filepath in path.rglob('*'):
            if filepath.is_file() and filepath.suffix in extensions:
                # Skip binary files and huge files
                if filepath.stat().st_size > 10 * 1024 * 1024:  # Skip > 10MB
                    continue
                findings.extend(cls.scan_file(str(filepath)))
        
        return findings

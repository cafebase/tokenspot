#!/usr/bin/env python3
"""
TokenSpot CLI - Smart API Key Discovery & Validation
"""

import argparse
import json
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from .scanner import TokenScanner
from .validators import get_validator, VALIDATORS
from .utils import print_banner, print_table, Colors


def validate_key(finding: dict) -> dict:
    """Validate a single API key finding."""
    service = finding['service']
    key = finding['key']
    
    validator = get_validator(service)
    if not validator:
        return {
            **finding,
            'validation': {
                'is_valid': None,
                'severity': '⚪ UNKNOWN',
                'permissions': [],
                'error_message': f'No validator for {service}'
            }
        }
    
    try:
        result = validator.validate(key)
        return {**finding, 'validation': result.to_dict()}
    except Exception as e:
        return {
            **finding,
            'validation': {
                'is_valid': False,
                'severity': '⚪ ERROR',
                'permissions': [],
                'error_message': str(e)
            }
        }


def scan_target(target: str, validate: bool = True, threads: int = 5, json_output: bool = False) -> list:
    """Scan a target (URL, file, or directory) and optionally validate findings."""
    findings = []
    
    # Determine target type
    if target.startswith(('http://', 'https://')):
        if not json_output:
            print(f"{Colors.BLUE}[*] Fetching and scanning URL: {target}{Colors.RESET}")
        findings = TokenScanner.scan_url(target)
        
    else:
        path = Path(target)
        if path.is_file():
            if not json_output:
                print(f"{Colors.BLUE}[*] Scanning file: {target}{Colors.RESET}")
            findings = TokenScanner.scan_file(str(path))
            
        elif path.is_dir():
            if not json_output:
                print(f"{Colors.BLUE}[*] Scanning directory: {target}{Colors.RESET}")
            findings = TokenScanner.scan_directory(str(path))
            
        else:
            print(f"{Colors.RED}[!] Invalid target: {target}{Colors.RESET}")
            return []
    
    if not json_output:
        print(f"{Colors.GREEN}[+] Found {len(findings)} potential keys{Colors.RESET}")
    
    if validate and findings:
        if not json_output:
            print(f"{Colors.BLUE}[*] Validating findings with {threads} threads...{Colors.RESET}")
        
        validated = []
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {executor.submit(validate_key, f): f for f in findings}
            
            for i, future in enumerate(as_completed(futures), 1):
                if not json_output and i % 5 == 0:
                    print(f"  Progress: {i}/{len(findings)}")
                validated.append(future.result())
        
        return validated
    
    return findings


def main():
    parser = argparse.ArgumentParser(
        description='TokenSpot - Smart API Key Discovery & Validation for Bug Hunters',
        epilog='Example: tokenspot scan https://target.com/main.js'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan a target for API keys')
    scan_parser.add_argument('target', help='URL, file path, or directory to scan')
    scan_parser.add_argument('--validate', '-v', action='store_true', default=True,
                            help='Validate found keys (default: True)')
    scan_parser.add_argument('--no-validate', action='store_false', dest='validate',
                            help='Skip validation')
    scan_parser.add_argument('--json', '-j', action='store_true',
                            help='Output in JSON format')
    scan_parser.add_argument('--threads', '-t', type=int, default=5,
                            help='Number of validation threads (default: 5)')
    scan_parser.add_argument('--output', '-o', help='Save results to file')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List supported services')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        print_banner()
        print(f"\n{Colors.BOLD}Supported Services:{Colors.RESET}\n")
        from .scanner import TokenScanner
        for service, (_, desc) in TokenScanner.PATTERNS.items():
            has_validator = '✓' if service in VALIDATORS else '○'
            color = Colors.GREEN if service in VALIDATORS else Colors.DIM
            print(f"  {color}{has_validator} {service:<18} {desc}{Colors.RESET}")
        print(f"\n{Colors.GREEN}✓ = validation supported{Colors.RESET}")
        print(f"{Colors.DIM}○ = detection only{Colors.RESET}")
        return
    
    elif args.command == 'scan':
        if not args.json:
            print_banner()
        
        results = scan_target(
            args.target,
            validate=args.validate,
            threads=args.threads,
            json_output=args.json
        )
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_table(results)
            
            # Summary
            if args.validate and results:
                critical = sum(1 for r in results 
                              if r.get('validation', {}).get('severity', '').startswith('🔴'))
                high = sum(1 for r in results 
                          if r.get('validation', {}).get('severity', '').startswith('🟠'))
                valid = sum(1 for r in results 
                           if r.get('validation', {}).get('is_valid'))
                
                print(f"\n{Colors.BOLD}Summary:{Colors.RESET}")
                print(f"  Total found: {len(results)}")
                print(f"  Valid keys: {valid}")
                print(f"  {Colors.RED}Critical: {critical}{Colors.RESET}")
                print(f"  {Colors.YELLOW}High: {high}{Colors.RESET}")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            if not args.json:
                print(f"\n{Colors.GREEN}[+] Results saved to {args.output}{Colors.RESET}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

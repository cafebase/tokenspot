"""
Utility functions for TokenSpot - terminal output formatting.
"""

import sys
import os

# Color support detection
if os.name == 'nt':  # Windows
    try:
        import colorama
        colorama.init()
    except ImportError:
        pass

class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    
    @classmethod
    def disable(cls):
        """Disable colors (for pipe output)."""
        for attr in dir(cls):
            if not attr.startswith('_') and attr != 'disable':
                setattr(cls, attr, '')


def supports_color():
    """Check if terminal supports color."""
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


if not supports_color():
    Colors.disable()


def print_banner():
    """Print the TokenSpott ASCII banner."""
    banner = f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║  _____     _             _   _____       _     _   _         ║
║ |_   _|__ | | _____ _ __| |_/ ____| ___ | |_  | |_| |_  ___  ║
║   | |/ _ \\| |/ / _ \\ '__| __\\___ \\ / _ \\| __| | __| __|/ _ \\ ║
║   | | (_) |   <  __/ |  | |_ ____) | (_) | |_  | |_| |_|  __/ ║
║   |_|\\___/|_|\\_\\___|_|   \\__|_____/ \\___/ \\__|  \\__|\\__|\\___| ║
║                                                                  ║
║              Smart API Key Discovery & Validation                ║
╚══════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def print_table(results):
    """Print results in a formatted table."""
    if not results:
        print(f"\n{Colors.YELLOW}[!] No findings to display{Colors.RESET}")
        return
    
    # Headers
    headers = ['Service', 'Key (masked)', 'Valid', 'Severity', 'Permissions', 'Account Info']
    
    rows = []
    for r in results:
        validation = r.get('validation', {})
        key = r.get('key', '')
        
        # Mask the key for display
        masked_key = key[:8] + '...' + key[-4:] if len(key) > 12 else key[:12] + '...'
        
        # Status with color
        is_valid = validation.get('is_valid')
        if is_valid is True:
            status = f"{Colors.GREEN}✓ VALID{Colors.RESET}"
        elif is_valid is False:
            status = f"{Colors.RED}✗ INVALID{Colors.RESET}"
        else:
            status = f"{Colors.YELLOW}? UNKNOWN{Colors.RESET}"
        
        severity = validation.get('severity', '⚪ UNKNOWN')
        perms = validation.get('permissions', [])
        perm_str = ', '.join(perms[:3]) + ('...' if len(perms) > 3 else '') if perms else '-'
        account = validation.get('account_info') or '-'
        
        if len(account) > 25:
            account = account[:22] + '...'
        
        rows.append([r.get('service', 'unknown'), masked_key, status, severity, perm_str, account])
    
    # Print table
    print(f"\n{Colors.BOLD}{'Service':<12} {'Key':<20} {'Valid':<10} {'Severity':<16} {'Permissions':<28} {'Account Info':<20}{Colors.RESET}")
    print("-" * 110)
    
    for row in rows:
        print(f"{row[0]:<12} {row[1]:<20} {row[2]:<10} {row[3]:<16} {row[4]:<28} {row[5]:<20}")

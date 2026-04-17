# 🔍 TokenSpot

> Smart API key discovery and validation for bug hunters and pentesters

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 🎯 Why TokenSpot?

Traditional tools find API keys. **TokenSpot tells you what they can actually do.**

| Tool | Finds Keys? | Validates? | Shows Permissions? |
|------|-------------|------------|-------------------|
| truffleHog | ✅ | ❌ | ❌ |
| gitleaks | ✅ | ❌ | ❌ |
| **TokenSpot** | ✅ | ✅ | ✅ |

### The Problem
Bug hunters waste hours manually verifying API key findings. 95% of "detected" keys are:
- Public keys with zero privileges
- Expired/revoked tokens
- Test mode credentials

### The Solution
TokenSpot validates keys in real-time and tells you:
- ✅ **Is it valid?**
- 🔴 **What permissions does it have?**
- 👤 **Which account does it belong to?**
- ⚡ **How critical is this finding?**

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- git

### Step 1: Clone the Repository
```bash
git clone https://github.com/cafebase/tokenspot.git
cd tokenspot
```

### Step 2: Set Up Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
# Install required packages
pip install requests colorama

# Or use requirements.txt
pip install -r requirements.txt
```

### Step 4: Run TokenSpot
```bash
# Run as a module (no installation needed)
python -m tokenspot --help

# Or install globally
pip install -e .
tokenspot --help
```

---

## 🚀 Quick Test (Verify Installation)
```bash
# Create a test file
echo 'const GITHUB_KEY="ghp_1234567890abcdefghijklmnopqrstuvwxyz123456"' > test.js

# Run TokenSpot
python -m tokenspot scan test.js --validate
```

Expected output: A table showing 1 potential key found.

---

## 🖥️ Usage

### Basic Commands
```bash
# List supported services
python -m tokenspot list

# Scan a file
python -m tokenspot scan path/to/file.js

# Scan a URL
python -m tokenspot scan https://example.com/app.js

# Scan with validation
python -m tokenspot scan path/to/file.js --validate

# Output as JSON
python -m tokenspot scan path/to/file.js --json -o results.json
```

### Command Options
| Option | Description |
|--------|-------------|
| `scan` | Scan a target for API keys |
| `list` | Show supported services |
| `--validate`, `-v` | Validate found keys (default: True) |
| `--no-validate` | Skip validation (faster) |
| `--json`, `-j` | Output in JSON format |
| `--threads N`, `-t N` | Number of threads (default: 5) |
| `--output FILE`, `-o FILE` | Save results to file |

---

## 📋 Supported Services

| Service | Pattern | Validation | Permission Detection |
|---------|---------|------------|---------------------|
| **GitHub** | `ghp_*` | ✅ | repo, workflow, admin:org, user |
| **Stripe** | `sk_live_*`, `pk_*` | ✅ | charges, refunds, payouts, read_only |
| **Slack** | `xoxb-*`, `xoxp-*` | ✅ | webhook_post, active_token |
| **OpenAI** | `sk-*`, `sk-proj-*` | ✅ | model access count |
| **AWS** | `AKIA*` | 🔶 | Pattern detection (needs secret) |
| **Google** | `AIza*` | 🔶 | Pattern detection |
| **Twilio** | `AC*` | 🔶 | Pattern detection |
| **SendGrid** | `SG.*` | 🔶 | Pattern detection |
| **Mailgun** | `key-*` | 🔶 | Pattern detection |
| **JWT** | `eyJ*` | 🔶 | Pattern detection |

✅ = Full validation with permission enumeration  
🔶 = Pattern detection only

---

## 📊 Example Output

```
$ python -m tokenspot scan test.js --validate

╔══════════════════════════════════════════════════════════════╗
║  _____     _             _   _____       _     _   _         ║
║ |_   _|__ | | _____ _ __| |_/ ____| ___ | |_  | |_| |_  ___  ║
║   | |/ _ \| |/ / _ \ '__| __\___ \ / _ \| __| | __| __|/ _ \ ║
║   | | (_) |   <  __/ |  | |_ ____) | (_) | |_  | |_| |_|  __/ ║
║   |_|\___/|_|\_\___|_|   \__|_____/ \___/ \__|  \__|\__|\___| ║
║                                                                  ║
║              Smart API Key Discovery & Validation                ║
╚══════════════════════════════════════════════════════════════════╝

[*] Scanning file: test.js
[+] Found 6 potential keys
[*] Validating findings...

Service      Key (masked)         Valid      Severity         Permissions
----------------------------------------------------------------------------
stripe       sk_live_...wxyz      ✗ INVALID  ⚪ INFO           -
github       ghp_1234...wxyz      ✗ INVALID  ⚪ INFO           -
slack_bot    xoxb-123...uvwx      ✗ INVALID  ⚪ INFO           -

Summary:
  Total found: 6
  Valid keys: 0
  🔴 Critical: 0
  🟠 High: 0
```

---

## ❗ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'requests'` | Run `pip install requests colorama` |
| `tokenspot: command not found` | Use `python -m tokenspot` instead |
| `ImportError: attempted relative import` | Run from parent directory with `python -m tokenspot` |
| Virtual environment not activated | Run `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows) |
| `error: unrecognized arguments` | Make sure to include `scan` before the target: `python -m tokenspot scan test.js` |

---

## ⚠️ Ethical Use

TokenSpot is designed for:
- ✅ Bug bounty hunting on **authorized targets**
- ✅ Internal security assessments
- ✅ Educational purposes

**Never use against systems you don't own or have explicit written permission to test.**

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**⭐ If TokenSpot helped you, drop a star!**

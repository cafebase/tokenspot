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


## ⚡ Quick Start

```bash
# Clone and install
git clone https://github.com/cafebase/tokenspot.git
cd tokenspot
pip install -e .

# Scan a URL
tokenspot scan https://target.com/main.js

# Scan a directory with validation
tokenspot scan ./js-dump/ --validate

# JSON output
tokenspot scan https://target.com/app.js --json -o results.json

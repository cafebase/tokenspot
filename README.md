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

## ⚡ Quick Start

```bash
# Clone and install
git clone https://github.com/yourusername/tokenspot.git
cd tokenspot
pip install -e .

# Scan a URL
tokenspot scan https://target.com/main.js

# Scan a directory with validation
tokenspot scan ./js-dump/ --validate

# JSON output
tokenspot scan https://target.com/app.js --json -o results.json

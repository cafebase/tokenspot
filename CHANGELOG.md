# Changelog

All notable changes to TokenSpot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-04-17

### 🎉 Initial Release

First stable release of TokenSpot - Smart API Key Discovery & Validation for Bug Hunters.

### ✨ Added

#### Core Features
- **Pattern Scanner**: Detects 15+ API key types using regex patterns
- **Validation Engine**: Real-time validation with permission enumeration
- **Multi-threading**: Concurrent validation for faster results
- **CLI Interface**: User-friendly command-line tool with colored output
- **JSON Export**: Machine-readable output for automation pipelines

#### Validators (Full Validation + Permission Detection)
- **GitHub**: Validates `ghp_*` tokens, detects scopes (repo, workflow, admin:org, user)
- **Stripe**: Validates `sk_*` and `pk_*` keys, detects charges/refunds/payouts permissions
- **Slack**: Validates `xoxb-*` tokens and webhook URLs
- **OpenAI**: Validates `sk-*` and `sk-proj-*` keys, counts accessible models

#### Validators (Pattern Detection Only)
- AWS Access Keys (`AKIA*`)
- Google API Keys (`AIza*`)
- Twilio SIDs (`AC*`) and Auth Tokens
- SendGrid API Keys (`SG.*`)
- Mailgun API Keys (`key-*`)
- JWT Tokens (`eyJ*`)

#### CLI Commands
- `tokenspot scan [TARGET]` - Scan URL, file, or directory
- `tokenspot list` - Display supported services
- Options: `--validate`, `--no-validate`, `--json`, `--threads`, `--output`

#### Testing & CI/CD
- Unit tests for scanner and all validators
- GitHub Actions workflow for automated testing on Python 3.8-3.11
- Mock-based tests to avoid real API calls

#### Documentation
- Comprehensive README with examples
- Contributing guidelines for new validators
- MIT License
- This changelog

### 🔧 Technical Details
- Python 3.8+ required
- Dependencies: `requests>=2.28.0`, `colorama>=0.4.6`
- Abstract base class design for easy validator extension
- ThreadPoolExecutor for concurrent validation
- Colored terminal output with Windows support

### 📊 Stats
- **Lines of Code**: ~1,200
- **Supported Services**: 15
- **Full Validators**: 4
- **Unit Tests**: 25+

---

## [Unreleased]

### 🚧 Planned for v1.1.0

#### New Validators
- [ ] GitLab Personal Access Tokens
- [ ] Bitbucket App Passwords
- [ ] Azure/Entra ID Client Secrets
- [ ] GCP Service Account Keys
- [ ] Discord Bot Tokens
- [ ] Telegram Bot Tokens

#### Features
- [ ] Full AWS validation using boto3 (optional dependency)
- [ ] Google API key validation with permission enumeration
- [ ] Twilio key validation
- [ ] Burp Suite extension integration
- [ ] Docker image for containerized usage
- [ ] Rate limiting detection and backoff
- [ ] Progress bar for directory scanning

#### Improvements
- [ ] Cache validation results to avoid duplicate API calls
- [ ] Support for scanning password-protected ZIP files
- [ ] Better error messages with troubleshooting suggestions
- [ ] Configuration file for custom patterns

---

## Version History Reference

| Version | Date | Type | Description |
|---------|------|------|-------------|
| 1.0.0 | 2026-04-17 | Major | Initial stable release |

---

## How Versioning Works

TokenSpot follows [Semantic Versioning](https://semver.org/):

- **MAJOR** (`1.0.0` → `2.0.0`): Breaking changes that may affect existing workflows
- **MINOR** (`1.0.0` → `1.1.0`): New features in a backward-compatible manner
- **PATCH** (`1.0.0` → `1.0.1`): Bug fixes and minor improvements

### Breaking Changes
- None yet (initial release)

### Deprecations
- None yet (initial release)

---

## Contributors

### v1.0.0
- [Your Name](https://github.com/cafebase) - Initial development

---

## Links

- [GitHub Repository](https://github.com/cafebase/tokenspot)
- [Issue Tracker](https://github.com/cafebase/tokenspot/issues)
- [Pull Requests](https://github.com/cafebase/tokenspot/pulls)

---

**📝 Note for Contributors**: When adding new features, please update the `[Unreleased]` section. Upon release, move items to a new version section.

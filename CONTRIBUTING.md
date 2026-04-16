
---

### `CONTRIBUTING.md` (Copy entire block)
```markdown
# Contributing to TokenSpot

Thanks for contributing! 🎉

## Development Setup

```bash
git clone https://github.com/yourusername/tokenspot.git
cd tokenspot
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v

---
source_project: CHOPSHOP
source_project_uuid: 019accd8-cfe0-7247-860b-1b169a50a0e1
doc_uuid: 623e83ce-a56f-465e-acdd-c443d93db1cd
original_filename: chopshop_development_guide.md
created_at: 2025-11-28T23:43:26.245870+00:00
content_hash: 12c9259d55fb
topic: chopshop-project-documentation
consolidated_into: docs/DC-CHOPSHOP-PROJECT-DOCUMENTATION-RECONCILED-001.md
---

# ChopShop-CLI Development Guide
**Version:** 1.0  
**Last Updated:** November 28, 2025

---

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure](#project-structure)
4. [Coding Standards](#coding-standards)
5. [Development Workflow](#development-workflow)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation Standards](#documentation-standards)
8. [Contributing](#contributing)
9. [Release Process](#release-process)

---

## Getting Started

### Prerequisites

**Required:**
- Python 3.10 or higher
- Git
- pip or Poetry

**Recommended:**
- VS Code or PyCharm
- Docker (for containerized development)
- Linux, macOS, or WSL2 on Windows

### Quick Start

```bash
# Clone repository
git clone https://github.com/your-username/chopshop-cli.git
cd chopshop-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .[dev]

# Run tests
pytest

# Run chopshop
chopshop --help
```

---

## Development Environment Setup

### Option 1: Poetry (Recommended)

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install

# Activate virtual environment
poetry shell

# Run chopshop
chopshop --help
```

### Option 2: pip + venv

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .[dev]

# Verify installation
chopshop --version
```

### IDE Configuration

#### VS Code

Create `.vscode/settings.json`:

```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length=100"],
    "editor.formatOnSave": true,
    "editor.rulers": [100],
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": [
        "tests",
        "-v"
    ]
}
```

#### PyCharm

1. File â†’ Settings â†’ Project â†’ Python Interpreter
2. Select the virtual environment
3. Enable "Black" as code formatter
4. Configure pytest as default test runner

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        args: [--line-length=100]
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=100, --extend-ignore=E203]
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
  
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: [--maxkb=1000]
```

---

## Project Structure

```
chopshop-cli/
â”œâ”€â”€ chopshop/                    # Main package
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ __main__.py             # CLI entry point
â”‚   â”œâ”€â”€ cli/                    # CLI interface
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ commands.py         # Click commands
â”‚   â”‚   â”œâ”€â”€ menu.py             # Interactive menu
â”‚   â”‚   â”œâ”€â”€ renderer.py         # Output rendering
â”‚   â”‚   â””â”€â”€ verbose.py          # Verbose logging
â”‚   â”œâ”€â”€ core/                   # Core engine
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ orchestrator.py     # Main controller
â”‚   â”‚   â”œâ”€â”€ config.py           # Configuration
â”‚   â”‚   â””â”€â”€ exceptions.py       # Custom exceptions
â”‚   â”œâ”€â”€ detection/              # Detection engine
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ detector.py         # Main detector
â”‚   â”‚   â”œâ”€â”€ signatures.py       # Signature matching
â”‚   â”‚   â”œâ”€â”€ statistical.py      # Statistical analysis
â”‚   â”‚   â”œâ”€â”€ ml_classifier.py    # ML-based detection
â”‚   â”‚   â””â”€â”€ fusion.py           # Confidence fusion
â”‚   â”œâ”€â”€ decoding/               # Decoding engine
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ recursive.py        # Recursive decoder
â”‚   â”‚   â”œâ”€â”€ validator.py        # Result validation
â”‚   â”‚   â”œâ”€â”€ chain_tracker.py    # Chain tracking
â”‚   â”‚   â””â”€â”€ cycle_detector.py   # Loop prevention
â”‚   â”œâ”€â”€ ciphers/                # Cipher modules
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ base.py             # Base interface
â”‚   â”‚   â”œâ”€â”€ registry.py         # Module registry
â”‚   â”‚   â”œâ”€â”€ base64_cipher.py
â”‚   â”‚   â”œâ”€â”€ hex_cipher.py
â”‚   â”‚   â”œâ”€â”€ rot_cipher.py
â”‚   â”‚   â”œâ”€â”€ xor_cipher.py
â”‚   â”‚   â””â”€â”€ user_defined/       # User plugins
â”‚   â”œâ”€â”€ utils/                  # Utilities
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ entropy.py
â”‚   â”‚   â”œâ”€â”€ frequency.py
â”‚   â”‚   â”œâ”€â”€ dictionary.py
â”‚   â”‚   â””â”€â”€ helpers.py
â”‚   â””â”€â”€ assets/                 # Resources
â”‚       â”œâ”€â”€ wordlists/
â”‚       â”‚   â”œâ”€â”€ english.txt
â”‚       â”‚   â””â”€â”€ common_passwords.txt
â”‚       â””â”€â”€ models/
â”‚           â””â”€â”€ cipher_classifier.pkl
â”œâ”€â”€ tests/                      # Test suite
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ conftest.py             # Pytest configuration
â”‚   â”œâ”€â”€ unit/                   # Unit tests
â”‚   â”‚   â”œâ”€â”€ test_detection.py
â”‚   â”‚   â”œâ”€â”€ test_ciphers.py
â”‚   â”‚   â””â”€â”€ test_utils.py
â”‚   â”œâ”€â”€ integration/            # Integration tests
â”‚   â”‚   â”œâ”€â”€ test_decode_flow.py
â”‚   â”‚   â””â”€â”€ test_cli.py
â”‚   â”œâ”€â”€ fixtures/               # Test data
â”‚   â”‚   â”œâ”€â”€ encoded_samples.json
â”‚   â”‚   â””â”€â”€ expected_results.json
â”‚   â””â”€â”€ benchmarks/             # Performance tests
â”‚       â””â”€â”€ test_performance.py
â”œâ”€â”€ docs/                       # Documentation
â”‚   â”œâ”€â”€ user_guide.md
â”‚   â”œâ”€â”€ developer_guide.md
â”‚   â”œâ”€â”€ cipher_reference.md
â”‚   â””â”€â”€ api/                    # API docs (Sphinx)
â”œâ”€â”€ scripts/                    # Utility scripts
â”‚   â”œâ”€â”€ train_ml_model.py
â”‚   â”œâ”€â”€ generate_test_data.py
â”‚   â””â”€â”€ benchmark.py
â”œâ”€â”€ .github/                    # GitHub configuration
â”‚   â”œâ”€â”€ workflows/
â”‚   â”‚   â”œâ”€â”€ test.yml
â”‚   â”‚   â”œâ”€â”€ release.yml
â”‚   â”‚   â””â”€â”€ docs.yml
â”‚   â”œâ”€â”€ ISSUE_TEMPLATE/
â”‚   â””â”€â”€ PULL_REQUEST_TEMPLATE.md
â”œâ”€â”€ .gitignore
â”œâ”€â”€ .pre-commit-config.yaml
â”œâ”€â”€ pyproject.toml              # Poetry configuration
â”œâ”€â”€ setup.py                    # Setup script
â”œâ”€â”€ requirements.txt            # Pip requirements
â”œâ”€â”€ requirements-dev.txt        # Development requirements
â”œâ”€â”€ README.md
â”œâ”€â”€ LICENSE
â”œâ”€â”€ CHANGELOG.md
â””â”€â”€ CONTRIBUTING.md
```

### Key Directories Explained

**chopshop/**: Core application code
- **cli/**: Everything related to the command-line interface
- **core/**: Central orchestration and configuration
- **detection/**: Cipher detection logic
- **decoding/**: Recursive decoding engine
- **ciphers/**: Individual cipher implementations
- **utils/**: Helper functions and utilities
- **assets/**: Static resources (wordlists, ML models)

**tests/**: Complete test suite
- **unit/**: Tests for individual components
- **integration/**: End-to-end workflow tests
- **fixtures/**: Test data and expected outputs
- **benchmarks/**: Performance testing

**docs/**: All documentation
- User-facing guides
- Developer documentation
- API reference (auto-generated)

---

## Coding Standards

### Python Style Guide

We follow **PEP 8** with the following modifications:

- **Line length**: 100 characters (not 79)
- **String quotes**: Double quotes `"` preferred
- **Import order**: stdlib â†’ third-party â†’ local (enforced by isort)

### Code Formatting

All code must be formatted with **Black**:

```bash
# Format all files
black chopshop/ tests/

# Check without modifying
black --check chopshop/ tests/
```

### Type Hints

Use type hints for all function signatures:

```python
# Good
def detect_cipher(text: str, threshold: float = 0.5) -> List[CipherCandidate]:
    """Detect cipher type from text."""
    pass

# Bad
def detect_cipher(text, threshold=0.5):
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def decode_base64(text: str, validate: bool = True) -> DecodeResult:
    """Decode Base64 encoded text.
    
    Args:
        text: The Base64 encoded string to decode
        validate: Whether to validate Base64 format before decoding
        
    Returns:
        DecodeResult object containing decoded text and metadata
        
    Raises:
        ValueError: If text is not valid Base64 and validate=True
        
    Example:
        >>> result = decode_base64("SGVsbG8gV29ybGQ=")
        >>> print(result.output)
        'Hello World'
    """
    pass
```

### Error Handling

Be specific with exceptions:

```python
# Good
try:
    decoded = base64.b64decode(text)
except binascii.Error as e:
    raise ValueError(f"Invalid Base64: {e}")

# Bad
try:
    decoded = base64.b64decode(text)
except Exception:
    pass
```

### Logging

Use Python's logging module, not print statements:

```python
import logging

logger = logging.getLogger(__name__)

# Good
logger.debug(f"Attempting decode with {cipher.name}")
logger.info(f"Successfully decoded using {cipher.name}")
logger.warning(f"Low confidence detection: {confidence:.2f}")
logger.error(f"Decode failed: {error}")

# Bad
print(f"Decoding...")
```

### Constants

Use ALL_CAPS for constants:

```python
# Good
MAX_RECURSION_DEPTH = 10
DEFAULT_TIMEOUT = 30
ENGLISH_FREQUENCY = {...}

# Bad
max_recursion_depth = 10
default_timeout = 30
```

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Module | lowercase_with_underscores | `cipher_detector.py` |
| Class | CapitalizedWords | `CipherModule` |
| Function | lowercase_with_underscores | `detect_cipher()` |
| Variable | lowercase_with_underscores | `confidence_score` |
| Constant | ALL_CAPS_WITH_UNDERSCORES | `MAX_DEPTH` |
| Private | _leading_underscore | `_internal_method()` |

---

## Development Workflow

### Branch Strategy

We use **Git Flow**:

- **main**: Production-ready code
- **develop**: Integration branch for features
- **feature/**: Feature branches (`feature/add-vigenere-cipher`)
- **bugfix/**: Bug fix branches (`bugfix/fix-base64-padding`)
- **release/**: Release preparation (`release/v0.2.0`)
- **hotfix/**: Production hotfixes (`hotfix/critical-bug`)

### Creating a Feature

```bash
# Start from develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/my-new-feature

# Make changes, commit often
git add .
git commit -m "Add XYZ functionality"

# Push to remote
git push -u origin feature/my-new-feature

# Create Pull Request on GitHub
```

### Commit Messages

Follow **Conventional Commits**:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Build process, dependencies

**Examples:**

```bash
feat(ciphers): add VigenÃ¨re cipher module
fix(detection): correct Base64 padding detection
docs(readme): update installation instructions
test(xor): add test cases for multi-byte XOR
refactor(decoder): simplify recursive logic
```

### Pull Request Process

1. **Create PR** with descriptive title and description
2. **Link issue** if applicable (`Closes #123`)
3. **Pass CI checks** (tests, linting, coverage)
4. **Request review** from maintainer
5. **Address feedback** with additional commits
6. **Squash and merge** once approved

### Code Review Checklist

Reviewers should verify:

- [ ] Code follows style guide
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
- [ ] Performance impact is acceptable
- [ ] Error handling is appropriate
- [ ] Type hints are present
- [ ] Docstrings are complete

---

## Testing Guidelines

### Testing Philosophy

- **Write tests first** (TDD encouraged)
- **Test behavior, not implementation**
- **Aim for 90%+ code coverage**
- **Fast tests**: Unit tests should run in milliseconds
- **Isolated tests**: No dependencies between tests

### Test Structure

```python
# tests/unit/test_base64_cipher.py

import pytest
from chopshop.ciphers.base64_cipher import Base64Cipher

class TestBase64Cipher:
    """Test suite for Base64 cipher module."""
    
    @pytest.fixture
    def cipher(self):
        """Create Base64Cipher instance for testing."""
        return Base64Cipher()
    
    def test_detect_valid_base64(self, cipher):
        """Test detection of valid Base64 string."""
        text = "SGVsbG8gV29ybGQh"
        confidence = cipher.detect(text)
        assert confidence > 0.8
    
    def test_detect_invalid_base64(self, cipher):
        """Test rejection of non-Base64 string."""
        text = "This is not Base64!"
        confidence = cipher.detect(text)
        assert confidence < 0.3
    
    def test_decode_standard_base64(self, cipher):
        """Test decoding of standard Base64."""
        text = "SGVsbG8gV29ybGQh"
        results = cipher.decode(text)
        
        assert len(results) > 0
        assert results[0].output == "Hello World!"
        assert results[0].confidence > 0.8
    
    @pytest.mark.parametrize("encoded,expected", [
        ("SGVsbG8=", "Hello"),
        ("V29ybGQ=", "World"),
        ("Zm9v", "foo"),
    ])
    def test_decode_multiple_cases(self, cipher, encoded, expected):
        """Test decoding of multiple Base64 strings."""
        results = cipher.decode(encoded)
        assert results[0].output == expected
    
    def test_decode_url_safe_base64(self, cipher):
        """Test decoding of URL-safe Base64."""
        text = "SGVsbG8gV29ybGQh"  # URL-safe variant
        results = cipher.decode(text)
        assert len(results) > 0
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=chopshop --cov-report=html

# Run specific test file
pytest tests/unit/test_base64_cipher.py

# Run specific test
pytest tests/unit/test_base64_cipher.py::TestBase64Cipher::test_decode_standard_base64

# Run tests matching pattern
pytest -k "base64"

# Run with verbose output
pytest -v

# Run with output (print statements visible)
pytest -s

# Run in parallel (faster)
pytest -n auto
```

### Test Fixtures

Use pytest fixtures for reusable test data:

```python
# tests/conftest.py

import pytest
from chopshop.core.config import Config
from chopshop import ChopShop

@pytest.fixture
def config():
    """Default configuration for tests."""
    return Config(
        verbosity=0,  # Quiet for tests
        max_depth=5,
        timeout=10
    )

@pytest.fixture
def chopshop(config):
    """ChopShop instance for testing."""
    return ChopShop(config)

@pytest.fixture
def sample_encodings():
    """Common encoded strings for testing."""
    return {
        'base64': "SGVsbG8gV29ybGQh",
        'hex': "48656c6c6f20576f726c6421",
        'rot13': "Uryyb Jbeyq!",
        'multi_layer': "NGU2NTZjNmM2ZjIwNTc2ZjcyNmM2NDIx"  # Base64â†’Hexâ†’"Hello World!"
    }
```

### Integration Tests

```python
# tests/integration/test_decode_flow.py

def test_end_to_end_decode(chopshop, sample_encodings):
    """Test complete decode flow from input to output."""
    result = chopshop.decode(sample_encodings['base64'])
    
    assert result.final_output == "Hello World!"
    assert result.chain == ["Base64"]
    assert result.confidence > 0.9

def test_multi_layer_decode(chopshop, sample_encodings):
    """Test recursive decoding of nested encodings."""
    # Base64â†’Hexâ†’"Hello World!"
    result = chopshop.decode(sample_encodings['multi_layer'])
    
    assert result.final_output == "Hello World!"
    assert "Base64" in result.chain
    assert "Hex" in result.chain
    assert len(result.chain) == 2
```

### Performance Tests

```python
# tests/benchmarks/test_performance.py

import time
import pytest

@pytest.mark.benchmark
def test_simple_decode_performance(chopshop, benchmark):
    """Benchmark simple Base64 decode."""
    text = "SGVsbG8gV29ybGQh"
    
    result = benchmark(chopshop.decode, text)
    
    # Should complete in <100ms
    assert benchmark.stats['mean'] < 0.1

@pytest.mark.benchmark
def test_detection_performance(chopshop, benchmark):
    """Benchmark cipher detection."""
    text = "SGVsbG8gV29ybGQh"
    
    result = benchmark(chopshop.detect, text)
    
    # Should complete in <50ms
    assert benchmark.stats['mean'] < 0.05
```

---

## Documentation Standards

### Code Documentation

Every module, class, and public function must have a docstring:

```python
"""
Module docstring explaining purpose and contents.

This module implements the recursive decoding engine for ChopShop-CLI.
It handles multi-layer nested encodings through intelligent recursion
with cycle detection and chain tracking.
"""

class RecursiveDecoder:
    """
    Main decoder for handling nested encodings.
    
    The RecursiveDecoder attempts to decode input through multiple layers
    by recursively applying detected ciphers until plaintext is reached.
    
    Attributes:
        max_depth: Maximum recursion depth allowed
        timeout: Maximum time allowed for decoding
        cycle_detector: Detector for preventing infinite loops
    
    Example:
        >>> decoder = RecursiveDecoder(max_depth=5)
        >>> result = decoder.decode("SGVsbG8=")
        >>> print(result.final_output)
        'Hello'
    """
```

### User Documentation

User-facing documentation in `docs/`:

- **README.md**: Quick start and overview
- **user_guide.md**: Comprehensive usage guide
- **cipher_reference.md**: Detailed cipher documentation
- **faq.md**: Frequently asked questions
- **troubleshooting.md**: Common issues and solutions

### API Documentation

Generate API docs with Sphinx:

```bash
# Install Sphinx
pip install sphinx sphinx-rtd-theme

# Generate docs
cd docs/
make html

# View docs
open _build/html/index.html
```

### Changelog

Maintain CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/):

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- VigenÃ¨re cipher module
- Batch processing mode

### Changed
- Improved Base64 detection accuracy
- Updated CLI help text

### Fixed
- ROT cipher edge case with numbers
- Memory leak in recursive decoder

## [0.1.0] - 2025-11-28

### Added
- Initial release
- 15 cipher modules
- Recursive decoding engine
- ML-based detection
```

---

## Contributing

### First Time Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a branch** for your contribution
4. **Make changes** and commit
5. **Push** to your fork
6. **Create Pull Request** on main repository

### Finding Issues to Work On

Look for issues labeled:
- `good first issue`: Easy for beginners
- `help wanted`: Maintainers need assistance
- `enhancement`: New features
- `bug`: Bug fixes needed

### Contribution Ideas

**Easy:**
- Add new cipher module
- Improve documentation
- Add test cases
- Fix typos

**Medium:**
- Optimize detection algorithm
- Add CLI feature
- Improve error messages

**Hard:**
- ML model improvements
- Performance optimization
- Complex cipher implementations

### Community Guidelines

- **Be respectful** and inclusive
- **Ask questions** if unsure
- **Provide context** in issues/PRs
- **Accept feedback** gracefully
- **Help others** when possible

---

## Release Process

### Versioning

We use **Semantic Versioning (SemVer)**:

- **MAJOR**: Breaking changes (1.0.0 â†’ 2.0.0)
- **MINOR**: New features, backward compatible (1.0.0 â†’ 1.1.0)
- **PATCH**: Bug fixes, backward compatible (1.0.0 â†’ 1.0.1)

### Release Checklist

1. **Update version** in `pyproject.toml` and `chopshop/__init__.py`
2. **Update CHANGELOG.md** with release notes
3. **Run full test suite**: `pytest`
4. **Build package**: `python -m build`
5. **Test installation**: `pip install dist/chopshop_cli-X.Y.Z.tar.gz`
6. **Create Git tag**: `git tag -a vX.Y.Z -m "Release X.Y.Z"`
7. **Push tag**: `git push origin vX.Y.Z`
8. **Publish to PyPI**: `twine upload dist/*`
9. **Create GitHub release** with changelog

### Automated Release

GitHub Actions handles releases automatically:

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build package
      run: |
        python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
      run: |
        twine upload dist/*
    
    - name: Create GitHub Release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        draft: false
        prerelease: false
```

---

## Getting Help

### Resources

- **Documentation**: https://chopshop-cli.readthedocs.io
- **GitHub Issues**: https://github.com/user/chopshop-cli/issues
- **Discord**: [Community Server]
- **Email**: [Project Email]

### Asking Questions

When asking for help:

1. **Search existing issues** first
2. **Provide context**: What are you trying to do?
3. **Include details**: OS, Python version, chopshop version
4. **Show code/output**: Use code blocks
5. **Describe expected vs actual behavior**

### Reporting Bugs

Include:
- ChopShop version (`chopshop --version`)
- Python version (`python --version`)
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/logs

---

## Quick Reference

### Common Commands

```bash
# Development
poetry install          # Install dependencies
poetry shell           # Activate virtual environment
pytest                 # Run tests
black chopshop/        # Format code
flake8 chopshop/       # Lint code
mypy chopshop/         # Type check

# Testing
pytest -v              # Verbose test output
pytest --cov           # With coverage
pytest -k "base64"     # Run specific tests
pytest -n auto         # Parallel execution

# Documentation
cd docs && make html   # Build docs
sphinx-autobuild docs/ docs/_build/html  # Live docs

# Git
git checkout -b feature/my-feature  # New feature branch
git commit -m "feat: add XYZ"       # Commit with message
git push -u origin feature/my-feature  # Push branch

# Release
python -m build        # Build package
twine upload dist/*    # Upload to PyPI
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-28 | Toussaint | Initial development guide |

---

*This guide is a living document. Please submit updates as the project evolves.*


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/chopshop-project-documentation|chopshop-project-documentation]]

**Consolidated into:**
- [[docs/DC-CHOPSHOP-PROJECT-DOCUMENTATION-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->

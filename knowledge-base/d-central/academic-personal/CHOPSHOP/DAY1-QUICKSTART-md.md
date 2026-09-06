---
source_project: CHOPSHOP
source_project_uuid: 019accd8-cfe0-7247-860b-1b169a50a0e1
doc_uuid: 244a8346-5669-4a97-bcf5-ac400634b5e8
original_filename: DAY1_QUICKSTART.md
created_at: 2025-11-28T23:43:29.219059+00:00
content_hash: 6b8026b1885a
topic: chopshop-project-documentation
consolidated_into: docs/DC-CHOPSHOP-PROJECT-DOCUMENTATION-RECONCILED-001.md
---

# ChopShop-CLI Day 1 Quick Start Guide
**Get Started in 30 Minutes**  
**Date:** Your Week 1, Day 1  
**Goal:** Working development environment and initial project structure

---

## âš¡ Quick Setup (30 Minutes)

### Step 1: Create GitHub Repository (5 min)

```bash
# On GitHub.com:
# 1. Click "New Repository"
# 2. Name: chopshop-cli
# 3. Description: "Automated cryptographic analysis and decoding tool"
# 4. Public repository
# 5. Add README, .gitignore (Python), LICENSE (MIT)
# 6. Create repository

# Clone locally
git clone https://github.com/YOUR_USERNAME/chopshop-cli.git
cd chopshop-cli
```

### Step 2: Create Project Structure (5 min)

```bash
# Create all directories
mkdir -p chopshop/{cli,core,detection,decoding,ciphers/user_defined,utils,assets/{wordlists,models}}
mkdir -p tests/{unit/{cli,core,detection,decoding,ciphers,utils},integration,fixtures,benchmarks}
mkdir -p docs
mkdir -p scripts
mkdir -p .github/workflows

# Create __init__.py files
touch chopshop/__init__.py
touch chopshop/{cli,core,detection,decoding,ciphers,utils}/__init__.py
touch tests/__init__.py
touch tests/{unit,integration,fixtures,benchmarks}/__init__.py

# Verify structure
tree -L 3 chopshop/
```

### Step 3: Initialize Package (5 min)

Create `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "chopshop-cli"
version = "0.1.0"
description = "Automated cryptographic analysis and decoding tool"
authors = [
    {name = "Toussaint", email = "your.email@example.com"}
]
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
keywords = ["cryptography", "decoding", "ctf", "security", "analysis"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Security :: Cryptography",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "rich>=13.0.0",
    "click>=8.0.0",
    "scikit-learn>=1.3.0",
    "numpy>=1.24.0",
    "cryptography>=41.0.0",
    "pycryptodome>=3.19.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-benchmark>=4.0.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.5.0",
    "pre-commit>=3.4.0",
]

[project.scripts]
chopshop = "chopshop.__main__:main"

[tool.black]
line-length = 100
target-version = ['py310']

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "-v --cov=chopshop --cov-report=term-missing"

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

Create `requirements.txt`:

```txt
rich>=13.0.0
click>=8.0.0
scikit-learn>=1.3.0
numpy>=1.24.0
cryptography>=41.0.0
pycryptodome>=3.19.0
```

Create `requirements-dev.txt`:

```txt
-r requirements.txt
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-benchmark>=4.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
pre-commit>=3.4.0
```

### Step 4: Setup Virtual Environment (5 min)

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows PowerShell)
# .\venv\Scripts\Activate.ps1

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -e .[dev]

# Verify installation
python -c "import rich; print('âœ“ Dependencies installed')"
```

### Step 5: Create Initial Files (10 min)

**chopshop/__init__.py:**

```python
"""
ChopShop-CLI - Automated Cryptographic Analysis and Decoding Tool

A terminal-based tool for automatically detecting and decoding encrypted/encoded
strings through intelligent pattern recognition and recursive multi-layer decoding.
"""

__version__ = "0.1.0"
__author__ = "Toussaint"
__description__ = "Automated cryptographic analysis and decoding tool"
__license__ = "MIT"

from chopshop.core.config import Config
from chopshop.core.models import CipherCandidate, DecodeResult, CompleteResult

__all__ = [
    "Config",
    "CipherCandidate", 
    "DecodeResult",
    "CompleteResult",
]
```

**chopshop/__main__.py:**

```python
"""Main entry point for ChopShop-CLI."""

import sys
from chopshop.cli.commands import cli


def main():
    """Execute CLI application."""
    try:
        cli()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

**chopshop/core/config.py:**

```python
"""Configuration management for ChopShop-CLI."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Main configuration for ChopShop-CLI.
    
    Attributes:
        verbosity: Logging verbosity level (0=quiet, 1=normal, 2=verbose, 3=debug)
        max_depth: Maximum recursion depth for multi-layer decoding
        timeout: Maximum time (seconds) allowed for decoding operations
        enable_ml: Whether to use ML-based detection
        parallel: Whether to use parallel processing for decoding
        user_plugins_dir: Directory containing user-defined cipher modules
    """
    
    verbosity: int = 1
    max_depth: int = 5
    timeout: int = 30
    enable_ml: bool = True
    parallel: bool = True
    user_plugins_dir: Optional[str] = None
    
    def __post_init__(self):
        """Validate configuration values."""
        if self.verbosity < 0 or self.verbosity > 3:
            raise ValueError("Verbosity must be between 0 and 3")
        
        if self.max_depth < 1 or self.max_depth > 20:
            raise ValueError("Max depth must be between 1 and 20")
        
        if self.timeout < 1:
            raise ValueError("Timeout must be positive")
```

**chopshop/core/exceptions.py:**

```python
"""Custom exceptions for ChopShop-CLI."""


class ChopShopError(Exception):
    """Base exception for all ChopShop errors."""
    pass


class DetectionError(ChopShopError):
    """Raised when cipher detection fails."""
    pass


class DecodingError(ChopShopError):
    """Raised when decoding fails."""
    pass


class ValidationError(ChopShopError):
    """Raised when validation fails."""
    pass


class TimeoutError(ChopShopError):
    """Raised when operation exceeds timeout."""
    pass


class PluginError(ChopShopError):
    """Raised when plugin loading or execution fails."""
    pass
```

**chopshop/core/models.py:**

```python
"""Data models for ChopShop-CLI."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class CipherCandidate:
    """Represents a cipher detection candidate.
    
    Attributes:
        cipher: Name of the detected cipher (e.g., "Base64")
        confidence: Confidence score from 0.0 to 1.0
        methods: List of detection methods that identified this cipher
        metadata: Additional information about the detection
    """
    
    cipher: str
    confidence: float
    methods: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __lt__(self, other):
        """Enable sorting by confidence (descending)."""
        return self.confidence > other.confidence


@dataclass
class DecodeResult:
    """Result from a cipher decode operation.
    
    Attributes:
        output: The decoded text
        confidence: How confident we are in this result (0.0-1.0)
        metadata: Cipher-specific information
        key: The key used for decoding (if applicable)
        timestamp: When this result was generated
    """
    
    output: str
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    key: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CompleteResult:
    """Complete result from recursive decoding.
    
    Attributes:
        original_input: The original encoded text
        final_output: The final decoded plaintext
        decode_chain: List of ciphers applied in order
        total_confidence: Overall confidence in result
        depth: Number of decoding layers
        execution_time: Time taken to decode (seconds)
        intermediate_results: Results from each decoding step
    """
    
    original_input: str
    final_output: str
    decode_chain: List[str]
    total_confidence: float
    depth: int
    execution_time: float
    intermediate_results: List[DecodeResult] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'input': self.original_input[:100] + '...' if len(self.original_input) > 100 else self.original_input,
            'output': self.final_output[:500] + '...' if len(self.final_output) > 500 else self.final_output,
            'chain': self.decode_chain,
            'confidence': round(self.total_confidence, 2),
            'depth': self.depth,
            'time_ms': round(self.execution_time * 1000, 2),
            'steps': len(self.intermediate_results)
        }
```

**chopshop/cli/commands.py:**

```python
"""CLI commands for ChopShop-CLI."""

import click
from rich.console import Console

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """ChopShop-CLI - Automated Cryptographic Analysis Tool
    
    Automatically detect and decode encrypted/encoded strings using intelligent
    pattern recognition and recursive multi-layer decoding.
    """
    pass


@cli.command()
@click.argument('text')
@click.option('-v', '--verbose', count=True, help='Increase verbosity (can be used multiple times)')
@click.option('--max-depth', default=5, help='Maximum recursion depth')
@click.option('-q', '--quiet', is_flag=True, help='Quiet mode (minimal output)')
def decode(text: str, verbose: int, max_depth: int, quiet: bool):
    """Decode encoded text.
    
    TEXT: The encoded string to decode
    """
    console.print(f"[cyan]ChopShop-CLI v0.1.0[/cyan]")
    console.print(f"Input: {text}")
    console.print("[yellow]Decoding functionality coming soon![/yellow]")


@cli.command()
@click.argument('text')
def detect(text: str):
    """Detect cipher type without decoding.
    
    TEXT: The encoded string to analyze
    """
    console.print(f"[cyan]ChopShop-CLI v0.1.0[/cyan]")
    console.print(f"Analyzing: {text}")
    console.print("[yellow]Detection functionality coming soon![/yellow]")


if __name__ == '__main__':
    cli()
```

**tests/conftest.py:**

```python
"""Pytest configuration and shared fixtures."""

import pytest
from chopshop.core.config import Config


@pytest.fixture
def config():
    """Default configuration for tests."""
    return Config(
        verbosity=0,  # Quiet for tests
        max_depth=5,
        timeout=10
    )


@pytest.fixture
def sample_encodings():
    """Common encoded strings for testing."""
    return {
        'base64': "SGVsbG8gV29ybGQh",
        'hex': "48656c6c6f20576f726c6421",
        'rot13': "Uryyb Jbeyq!",
        'url': "Hello%20World%21",
    }
```

**tests/unit/test_config.py:**

```python
"""Tests for configuration module."""

import pytest
from chopshop.core.config import Config


def test_default_config():
    """Test default configuration values."""
    config = Config()
    
    assert config.verbosity == 1
    assert config.max_depth == 5
    assert config.timeout == 30
    assert config.enable_ml is True
    assert config.parallel is True


def test_custom_config():
    """Test custom configuration values."""
    config = Config(
        verbosity=2,
        max_depth=10,
        timeout=60
    )
    
    assert config.verbosity == 2
    assert config.max_depth == 10
    assert config.timeout == 60


def test_invalid_verbosity():
    """Test that invalid verbosity raises error."""
    with pytest.raises(ValueError):
        Config(verbosity=-1)
    
    with pytest.raises(ValueError):
        Config(verbosity=5)


def test_invalid_max_depth():
    """Test that invalid max_depth raises error."""
    with pytest.raises(ValueError):
        Config(max_depth=0)
    
    with pytest.raises(ValueError):
        Config(max_depth=50)
```

**.gitignore:**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Distribution
dist/
build/
*.egg-info/

# OS
.DS_Store
Thumbs.db
```

### Step 6: Initial Test (5 min)

```bash
# Run tests
pytest

# Should show:
# ===== 3 passed in 0.05s =====

# Test CLI
chopshop --help

# Should show help text

# Test decode command
chopshop decode "SGVsbG8="

# Should show placeholder message
```

### Step 7: Git Commit (5 min)

```bash
# Stage all files
git add .

# Initial commit
git commit -m "Initial project structure and configuration"

# Push to GitHub
git push origin main
```

---

## âœ… Day 1 Complete!

You now have:

- âœ… GitHub repository created
- âœ… Project structure in place
- âœ… Package configuration done
- âœ… Virtual environment setup
- âœ… Basic files created
- âœ… Tests passing
- âœ… CLI working (placeholder)
- âœ… First commit pushed

---

## ðŸŽ¯ Next Steps (Day 2)

Continue with Phase 1 Plan â†’ Week 1 â†’ Day 2:

1. Complete core architecture
2. Implement base classes
3. Write comprehensive tests
4. Add type hints and docstrings

---

## ðŸ› Troubleshooting

### Virtual Environment Issues

```bash
# If activation fails
python3 -m venv venv --clear

# Try alternative activation
source venv/bin/activate
```

### Import Errors

```bash
# Ensure you're in project root
cd /path/to/chopshop-cli

# Reinstall in development mode
pip install -e .
```

### Test Failures

```bash
# Run with verbose output
pytest -v

# Run specific test
pytest tests/unit/test_config.py -v
```

---

## ðŸ“ Daily Checklist

Use this every day:

**Morning:**
- [ ] Activate virtual environment
- [ ] Check Phase 1 Plan for today's tasks
- [ ] Review yesterday's progress

**During Development:**
- [ ] Follow coding standards (Dev Guide)
- [ ] Write tests first (Testing Strategy)
- [ ] Commit frequently

**Evening:**
- [ ] Run full test suite
- [ ] Check coverage: `pytest --cov`
- [ ] Commit day's work
- [ ] Update progress in Phase 1 Plan

---

## ðŸŽ‰ You're Set!

Your development environment is ready. Time to build ChopShop-CLI!

**Tomorrow:** Implement CipherModule base class and detection engine skeleton.

Good luck! ðŸš€

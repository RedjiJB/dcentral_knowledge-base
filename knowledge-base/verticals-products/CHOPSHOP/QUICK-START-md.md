---
source_project: CHOPSHOP
source_project_uuid: 019accd8-cfe0-7247-860b-1b169a50a0e1
doc_uuid: 741794a2-d8dd-456d-a03f-e37bd98da462
original_filename: QUICK_START.md
created_at: 2025-11-28T23:43:31.217685+00:00
content_hash: 97288d933cf0topic: decoding-cipher-chopshop
topic: chopshop-project-documentation
---

# ChopShop-CLI Quick Start Guide

**For:** Toussaint  
**Goal:** Get from documentation to working code ASAP  
**Time:** 30 minutes to first commit

---

## ðŸš€ Right Now (Next 30 Minutes)

### Step 1: Create GitHub Repository (5 minutes)

```bash
# On GitHub.com:
# 1. Go to https://github.com/new
# 2. Repository name: chopshop-cli
# 3. Description: "Intelligent terminal-based cryptography analysis tool"
# 4. Public repository
# 5. Add README, .gitignore (Python), MIT License
# 6. Create repository

# On your computer:
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/YOUR_USERNAME/chopshop-cli.git
cd chopshop-cli
```

### Step 2: Create Project Structure (5 minutes)

```bash
# Create directory structure
mkdir -p chopshop/{cli,detection,engine,ciphers/user_defined,resources/{wordlists,models}}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p docs examples

# Create __init__.py files
touch chopshop/__init__.py
touch chopshop/cli/__init__.py
touch chopshop/detection/__init__.py
touch chopshop/engine/__init__.py
touch chopshop/ciphers/__init__.py
touch tests/__init__.py

# Create main files
touch chopshop/__main__.py
touch chopshop/cli/banner.py
touch chopshop/interfaces.py

# Git tracking
touch .gitkeep chopshop/resources/wordlists/.gitkeep
touch .gitkeep chopshop/resources/models/.gitkeep
```

### Step 3: Create Basic Files (10 minutes)

**setup.py:**
```python
from setuptools import setup, find_packages

setup(
    name="chopshop-cli",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "cryptography>=41.0.0",
        "pycryptodome>=3.19.0",
        "rich>=13.7.0",
        "click>=8.1.7",
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "chopshop=chopshop.__main__:main",
        ]
    },
    author="Toussaint",
    description="Intelligent terminal-based cryptography analysis tool",
    keywords="cryptography, security, ctf, cipher, decoder",
    python_requires=">=3.8",
)
```

**pyproject.toml:**
```toml
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
target-version = ['py38', 'py39', 'py310', 'py311']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

**.gitignore:**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# Testing
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

### Step 4: Initial Code (10 minutes)

**chopshop/interfaces.py:**
```python
"""Base interfaces for ChopShop-CLI."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class DecodeCandidate:
    """Represents a potential decoded result."""
    decoded_text: str
    confidence: float
    method_details: str
    metadata: Dict[str, Any]


@dataclass
class DetectionResult:
    """Represents a cipher detection result."""
    cipher_name: str
    confidence: float
    reasoning: str
    metadata: Dict[str, Any]


class CipherModule(ABC):
    """Base interface for all cipher modules."""
    
    name: str = ""
    aliases: List[str] = []
    category: str = ""
    
    @abstractmethod
    def detect(self, text: str) -> float:
        """Return confidence score that this cipher was used."""
        pass
    
    @abstractmethod
    def decode(self, text: str) -> List[DecodeCandidate]:
        """Attempt to decode text and return candidates."""
        pass
```

**chopshop/__main__.py:**
```python
"""ChopShop-CLI entry point."""

import sys


def main():
    """Main entry point."""
    print("ðŸ”ª ChopShop-CLI v0.0.1")
    print("Crypto analysis tool initializing...")
    print("\nSetup complete! Ready for development.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**chopshop/cli/banner.py:**
```python
"""Banner and startup display."""

BANNER = """
 â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ•—  â–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ•—  â–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•— 
â–ˆâ–ˆâ•”â•â•â•â•â•â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â•â•â•â–ˆâ–ˆâ•”â•â•â•â–ˆâ–ˆâ•—â–ˆâ–ˆâ•”â•â•â•â•â•â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â•â–ˆâ–ˆâ•—â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—
â–ˆâ–ˆâ•‘     â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘     â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•”â•
â–ˆâ–ˆâ•‘     â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘     â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘â•šâ•â•â•â•â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—
â•šâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘â•šâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—â•šâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•”â•â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘â•šâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•”â•â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘
 â•šâ•â•â•â•â•â•â•šâ•â•  â•šâ•â• â•šâ•â•â•â•â•â• â•šâ•â•â•â•â•â• â•šâ•â•â•â•â•â•â•â•šâ•â•  â•šâ•â• â•šâ•â•â•â•â•â• â•šâ•â•  â•šâ•â•

                 CHOPSHOP-CLI v0.0.1
        Auto-detect. Auto-decode. Recursive. Verbose.
"""


def display_banner():
    """Display startup banner."""
    print(BANNER)
```

**tests/test_basic.py:**
```python
"""Basic tests to ensure setup works."""

def test_imports():
    """Test that modules can be imported."""
    from chopshop import interfaces
    from chopshop.cli import banner
    assert True


def test_banner():
    """Test banner display."""
    from chopshop.cli.banner import display_banner
    display_banner()  # Should not crash
    assert True
```

---

## Step 5: Set Up Environment & First Commit (5 minutes)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1

# Install in dev mode
pip install --upgrade pip
pip install -e ".[dev]"

# Run basic test
python -m chopshop

# Run tests
pytest

# Initial commit
git add .
git commit -m "Initial project structure and base interfaces

- Created project directory structure
- Added base CipherModule interface
- Implemented basic CLI entry point
- Set up testing framework
- Added development dependencies

Relates to Week 1, Day 1-2 of roadmap"

git push origin main
```

---

## âœ… You Now Have:

1. âœ… GitHub repository
2. âœ… Project structure matching architecture
3. âœ… Base interfaces defined
4. âœ… Development environment set up
5. âœ… First commit pushed
6. âœ… Tests running

---

## ðŸŽ¯ Next Steps (This Week)

### Day 1 (Today) - Remaining
- [ ] Copy documentation to `docs/` folder in repo
- [ ] Update README.md with project info
- [ ] Create GitHub issues for Week 1 tasks

### Day 2 (Tomorrow)
- [ ] Implement first cipher module (Base64)
- [ ] Add tests for Base64 module
- [ ] Test detection and decoding

### Day 3-4
- [ ] Implement 3 more cipher modules (Hex, ROT13, URL)
- [ ] Create detection engine skeleton
- [ ] Add integration tests

### Day 5-7
- [ ] Create CLI menu system
- [ ] Add verbose logger with colors
- [ ] Polish and test

---

## ðŸ“ GitHub Issues to Create

Create these issues to track work:

**Issue #1: Implement Base64 Cipher Module**
```markdown
Implement Base64 cipher detection and decoding.

**Tasks:**
- [ ] Create `chopshop/ciphers/base64_cipher.py`
- [ ] Implement `detect()` method
- [ ] Implement `decode()` method
- [ ] Add unit tests (>90% coverage)
- [ ] Add documentation

**Acceptance Criteria:**
- Detects standard Base64 with >0.8 confidence
- Decodes standard and URL-safe Base64
- All tests passing

**Reference:** CIPHER_MODULE_GUIDE.md, PHASE1_SPECIFICATION.md
```

**Issue #2: Implement Detection Engine**
```markdown
Create auto-detection engine for cipher type identification.

**Tasks:**
- [ ] Create `chopshop/detection/auto_detect.py`
- [ ] Implement signature detection
- [ ] Implement entropy analysis
- [ ] Implement scoring system
- [ ] Add tests

**Reference:** ARCHITECTURE.md, PHASE1_SPECIFICATION.md
```

---

## ðŸŽ“ Learning Resources

While you code, reference:

1. **CIPHER_MODULE_GUIDE.md** - When creating new ciphers
2. **ARCHITECTURE.md** - For design decisions
3. **PHASE1_SPECIFICATION.md** - For requirements
4. **CONTRIBUTING.md** - For code standards

---

## ðŸ’» Daily Development Workflow

```bash
# Start of day
cd ~/projects/chopshop-cli
source venv/bin/activate
git pull origin main
git checkout -b feature/your-feature

# During development
# ... write code ...
black chopshop/  # Format
pytest           # Test
git add .
git commit -m "feat: your feature"

# End of day
git push origin feature/your-feature
# Create pull request on GitHub
```

---

## ðŸ† Week 1 Goals (Reminder)

By end of Week 1:
- âœ… Repository structure complete
- âœ… Base classes implemented
- âœ… CLI displays colorful menus
- âœ… Basic tests passing

---

## ðŸš¨ If You Get Stuck

1. **Check documentation:**
   - SETUP_GUIDE.md for environment issues
   - CIPHER_MODULE_GUIDE.md for implementation help
   - ARCHITECTURE.md for design questions

2. **Review examples:**
   - See completed cipher examples in guides
   - Check test templates

3. **Take notes:**
   - Document problems and solutions
   - Will help future contributors

---

## ðŸŽ‰ Congratulations!

You're now officially started on ChopShop-CLI development!

**You have:**
- âœ… Complete documentation suite
- âœ… Initial code structure
- âœ… Development environment
- âœ… First commit
- âœ… Clear path forward

**Next milestone:** End of Week 1 with base architecture complete

---

**Ready to build something amazing? Let's go! ðŸ”ªðŸ”**

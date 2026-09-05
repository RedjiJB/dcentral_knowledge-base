---
source_project: CHOPSHOP
source_project_uuid: 019accd8-cfe0-7247-860b-1b169a50a0e1
doc_uuid: 1f988f8b-fb02-492c-b9f5-780198adf511
original_filename: SETUP_GUIDE.md
created_at: 2025-11-28T23:43:32.690028+00:00
content_hash: 98cee9df3d1e
---

# ChopShop-CLI Development Setup Guide

## Document Control

**Version:** 1.0  
**Date:** November 28, 2024  
**Audience:** Developers and Contributors

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Environment Setup](#2-environment-setup)
3. [Installation Options](#3-installation-options)
4. [Development Tools](#4-development-tools)
5. [IDE Configuration](#5-ide-configuration)
6. [Running Tests](#6-running-tests)
7. [Building Documentation](#7-building-documentation)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Prerequisites

### 1.1 System Requirements

**Operating Systems**:
- Linux (Ubuntu 20.04+, Debian 10+, Fedora 33+)
- macOS (10.15 Catalina or later)
- Windows 10/11 (with PowerShell 5.1+ or PowerShell Core)

**Hardware**:
- CPU: Any modern processor (2+ cores recommended)
- RAM: 4GB minimum, 8GB recommended
- Disk: 500MB free space for development environment
- Display: Terminal with ANSI color support

### 1.2 Required Software

**Python**:
- Version: 3.8, 3.9, 3.10, or 3.11
- Package manager: pip 21.0+
- Virtual environment: venv or virtualenv

**Version Control**:
- Git 2.25+

**Terminal**:
- Linux/macOS: Any modern terminal
- Windows: PowerShell, Windows Terminal, or Git Bash

### 1.3 Recommended Software

- **IDE/Editor**: VS Code, PyCharm, or Vim
- **Terminal Multiplexer**: tmux or screen (Linux/macOS)
- **Python Version Manager**: pyenv (optional)
- **Package Manager**: poetry (optional alternative to pip)

---

## 2. Environment Setup

### 2.1 Install Python

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install Python 3.11 and pip
sudo apt install python3.11 python3.11-venv python3-pip -y

# Verify installation
python3 --version
pip3 --version
```

#### Linux (Fedora)
```bash
# Install Python
sudo dnf install python3.11 python3-pip -y

# Verify installation
python3 --version
pip3 --version
```

#### macOS
```bash
# Using Homebrew (install from https://brew.sh if needed)
brew install python@3.11

# Verify installation
python3 --version
pip3 --version
```

#### Windows
1. Download Python from https://www.python.org/downloads/
2. Run installer, ensure "Add Python to PATH" is checked
3. Verify in PowerShell:
```powershell
python --version
pip --version
```

### 2.2 Install Git

#### Linux (Ubuntu/Debian)
```bash
sudo apt install git -y
git --version
```

#### macOS
```bash
brew install git
git --version
```

#### Windows
Download from https://git-scm.com/downloads and install.

### 2.3 Configure Git

```bash
# Set your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Enable color output
git config --global color.ui auto

# Set default editor
git config --global core.editor "nano"  # or vim, code, etc.
```

---

## 3. Installation Options

### 3.1 Option A: Clone from GitHub (Recommended for Development)

```bash
# Create development directory
mkdir -p ~/projects
cd ~/projects

# Clone repository
git clone https://github.com/YOUR_USERNAME/chopshop-cli.git
cd chopshop-cli

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
.\venv\Scripts\activate.bat

# Upgrade pip
pip install --upgrade pip

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Verify installation
chopshop --version
```

### 3.2 Option B: Using Poetry (Alternative)

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Clone repository
git clone https://github.com/YOUR_USERNAME/chopshop-cli.git
cd chopshop-cli

# Install dependencies
poetry install

# Activate environment
poetry shell

# Verify installation
chopshop --version
```

### 3.3 Option C: Docker Development Environment

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/chopshop-cli.git
cd chopshop-cli

# Build development container
docker build -t chopshop-dev -f Dockerfile.dev .

# Run container with mounted source
docker run -it --rm \
  -v $(pwd):/app \
  -w /app \
  chopshop-dev \
  /bin/bash

# Inside container, install in dev mode
pip install -e ".[dev]"
```

---

## 4. Development Tools

### 4.1 Code Formatting and Linting

```bash
# Install development tools (included in [dev] dependencies)
pip install black flake8 isort mypy

# Format code with black
black chopshop/

# Sort imports with isort
isort chopshop/

# Lint with flake8
flake8 chopshop/

# Type check with mypy
mypy chopshop/
```

### 4.2 Pre-commit Hooks

Automatically format and check code before commits:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually on all files
pre-commit run --all-files
```

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

### 4.3 Testing Framework

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=chopshop --cov-report=html --cov-report=term

# Open coverage report
# Linux/macOS:
open htmlcov/index.html
# Windows:
start htmlcov/index.html

# Run specific test file
pytest tests/test_detection.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "base64"

# Show print statements
pytest -s
```

### 4.4 Performance Profiling

```bash
# Install profiling tools
pip install py-spy memory_profiler

# Profile CPU usage
py-spy record -o profile.svg -- python -m chopshop decode "SGVsbG8="

# Profile memory usage
python -m memory_profiler chopshop/engine/recursive_decoder.py

# Benchmark with pytest-benchmark
pytest tests/benchmarks/ --benchmark-only
```

---

## 5. IDE Configuration

### 5.1 Visual Studio Code

**Install VS Code**: https://code.visualstudio.com/

**Recommended Extensions**:
- Python (Microsoft)
- Pylance (Microsoft)
- Python Test Explorer
- GitLens
- autoDocstring
- Better Comments

**Settings** (`.vscode/settings.json`):
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "88"],
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/.pytest_cache": true,
        "**/.mypy_cache": true,
        "**/venv": true
    }
}
```

**Launch Configuration** (`.vscode/launch.json`):
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "ChopShop: Decode",
            "type": "python",
            "request": "launch",
            "module": "chopshop",
            "args": ["decode", "SGVsbG8gV29ybGQ=", "--verbose"],
            "console": "integratedTerminal"
        },
        {
            "name": "ChopShop: Debug Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["-v", "--no-cov"],
            "console": "integratedTerminal"
        }
    ]
}
```

### 5.2 PyCharm

**Configuration Steps**:
1. Open Project â†’ Select chopshop-cli directory
2. Configure Python Interpreter:
   - Settings â†’ Project â†’ Python Interpreter
   - Add Interpreter â†’ Existing environment
   - Select `venv/bin/python`
3. Configure Test Runner:
   - Settings â†’ Tools â†’ Python Integrated Tools
   - Set Default test runner: pytest
4. Enable Code Inspections:
   - Settings â†’ Editor â†’ Inspections
   - Enable Python inspections
5. Configure Black:
   - Settings â†’ Tools â†’ External Tools
   - Add Black with command: `$PyInterpreterDirectory$/black $FilePath$`

### 5.3 Vim/Neovim

**Install Plugins** (using vim-plug):
```vim
" .vimrc or init.vim
call plug#begin('~/.vim/plugged')

" Python support
Plug 'davidhalter/jedi-vim'
Plug 'dense-analysis/ale'
Plug 'psf/black', { 'branch': 'stable' }
Plug 'fisadev/vim-isort'

" General development
Plug 'preservim/nerdtree'
Plug 'tpope/vim-fugitive'
Plug 'vim-airline/vim-airline'

call plug#end()

" Python settings
let g:ale_linters = {'python': ['flake8', 'mypy']}
let g:ale_fixers = {'python': ['black', 'isort']}
let g:ale_fix_on_save = 1
```

---

## 6. Running Tests

### 6.1 Quick Test Commands

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=chopshop

# Run specific test file
pytest tests/ciphers/test_base64_cipher.py

# Run specific test class
pytest tests/ciphers/test_base64_cipher.py::TestBase64Cipher

# Run specific test method
pytest tests/ciphers/test_base64_cipher.py::TestBase64Cipher::test_detect

# Run tests matching keyword
pytest -k "base64 or hex"

# Run tests verbosely
pytest -v

# Run failed tests only
pytest --lf

# Run tests in parallel (install pytest-xdist)
pytest -n auto
```

### 6.2 Test Categories

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Slow tests (marked with @pytest.mark.slow)
pytest -m slow

# Skip slow tests
pytest -m "not slow"

# Performance benchmarks
pytest tests/benchmarks/ --benchmark-only
```

### 6.3 Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=chopshop --cov-report=html

# Generate terminal coverage report
pytest --cov=chopshop --cov-report=term-missing

# Generate XML coverage report (for CI)
pytest --cov=chopshop --cov-report=xml

# Check minimum coverage threshold
pytest --cov=chopshop --cov-fail-under=85
```

---

## 7. Building Documentation

### 7.1 API Documentation (Sphinx)

```bash
# Install Sphinx
pip install sphinx sphinx-rtd-theme

# Initialize Sphinx (first time only)
cd docs/
sphinx-quickstart

# Build HTML documentation
make html

# View documentation
# Linux/macOS:
open _build/html/index.html
# Windows:
start _build/html/index.html

# Build PDF documentation (requires LaTeX)
make latexpdf

# Clean build files
make clean
```

### 7.2 User Documentation (MkDocs)

```bash
# Install MkDocs
pip install mkdocs mkdocs-material

# Serve documentation locally
mkdocs serve

# Build static documentation
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

---

## 8. Troubleshooting

### 8.1 Common Issues

**Issue: Python version not found**
```bash
# Solution: Install correct Python version
# Ubuntu/Debian:
sudo apt install python3.11 python3.11-venv

# macOS:
brew install python@3.11
```

**Issue: pip install fails with permissions error**
```bash
# Solution 1: Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Solution 2: User install (not recommended for development)
pip install --user -e ".[dev]"
```

**Issue: Import errors in IDE**
```bash
# Solution: Ensure IDE is using virtual environment Python
# VS Code: Cmd/Ctrl+Shift+P â†’ "Python: Select Interpreter"
# PyCharm: Settings â†’ Project â†’ Python Interpreter
```

**Issue: Tests fail with "ModuleNotFoundError"**
```bash
# Solution: Install package in development mode
pip install -e ".[dev]"

# Or run tests from package root
cd chopshop-cli/
pytest
```

**Issue: colorama not working on Windows**
```bash
# Solution: Initialize colorama in main
import colorama
colorama.init()
```

**Issue: Pre-commit hooks not running**
```bash
# Solution: Reinstall hooks
pre-commit uninstall
pre-commit install

# Or run manually
pre-commit run --all-files
```

### 8.2 Platform-Specific Issues

**Windows: Virtual environment activation fails**
```powershell
# Solution: Change execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.\venv\Scripts\Activate.ps1
```

**macOS: SSL certificate errors**
```bash
# Solution: Install certificates
/Applications/Python\ 3.11/Install\ Certificates.command
```

**Linux: Missing build dependencies**
```bash
# Ubuntu/Debian:
sudo apt install build-essential python3-dev libffi-dev libssl-dev

# Fedora:
sudo dnf install gcc python3-devel libffi-devel openssl-devel
```

### 8.3 Getting Help

1. **Check documentation**: README.md, CONTRIBUTING.md
2. **Search issues**: GitHub Issues tab
3. **Ask questions**: GitHub Discussions
4. **Debug mode**: Run with `--debug` flag
5. **Verbose output**: Use `-v` or `--verbose`

---

## 9. Quick Reference

### 9.1 Essential Commands

```bash
# Setup
python3 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1
pip install -e ".[dev]"

# Development
black chopshop/           # Format code
isort chopshop/           # Sort imports
flake8 chopshop/          # Lint
mypy chopshop/            # Type check
pytest                    # Run tests

# Run application
chopshop decode "SGVsbG8=" --verbose
python -m chopshop decode "SGVsbG8="

# Git workflow
git checkout -b feature/my-feature
git add .
git commit -m "feat: add my feature"
git push origin feature/my-feature
```

### 9.2 Directory Structure

```
chopshop-cli/
â”œâ”€â”€ chopshop/              # Main package
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ __main__.py       # Entry point
â”‚   â”œâ”€â”€ cli/              # CLI interface
â”‚   â”œâ”€â”€ detection/        # Detection engine
â”‚   â”œâ”€â”€ engine/           # Core engine
â”‚   â””â”€â”€ ciphers/          # Cipher modules
â”œâ”€â”€ tests/                # Test suite
â”‚   â”œâ”€â”€ unit/
â”‚   â”œâ”€â”€ integration/
â”‚   â””â”€â”€ conftest.py
â”œâ”€â”€ docs/                 # Documentation
â”œâ”€â”€ examples/             # Example scripts
â”œâ”€â”€ setup.py              # Package configuration
â”œâ”€â”€ pyproject.toml        # Build configuration
â”œâ”€â”€ requirements.txt      # Dependencies
â”œâ”€â”€ README.md
â””â”€â”€ LICENSE
```

---

## 10. Next Steps

After completing setup:

1. **Read documentation**: PROJECT_CHARTER.md, ARCHITECTURE.md
2. **Explore codebase**: Start with main modules
3. **Run examples**: Try example scripts
4. **Make a small change**: Fix a typo, add a comment
5. **Submit your first PR**: Follow CONTRIBUTING.md

**Welcome to ChopShop-CLI development!** ðŸŽ‰

---
source_project: CHOPSHOP
source_project_uuid: 019accd8-cfe0-7247-860b-1b169a50a0e1
doc_uuid: 4cb44f3b-3311-4e82-817f-ff134550dfc9
original_filename: CONTRIBUTING(1).md
created_at: 2025-11-28T23:43:28.439354+00:00
content_hash: 79bae8805607topic: decoding-cipher-chopshop
---

# Contributing to ChopShop-CLI

Thank you for your interest in contributing to ChopShop-CLI! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Contribution Types](#contribution-types)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation](#documentation)
8. [Pull Request Process](#pull-request-process)
9. [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of experience level, background, or identity.

### Expected Behavior

- Be respectful and constructive in all interactions
- Welcome newcomers and help them get started
- Focus on what is best for the community and the project
- Accept constructive criticism gracefully
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discrimination, or trolling
- Publishing others' private information
- Inappropriate sexual content or attention
- Political or off-topic discussions in project spaces
- Other conduct considered inappropriate in a professional setting

### Enforcement

Violations can be reported to the project maintainers. All complaints will be reviewed and investigated promptly and fairly.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of cryptography concepts
- Familiarity with terminal/CLI applications

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/YOUR_USERNAME/chopshop-cli.git
cd chopshop-cli
```

3. Add upstream remote:
```bash
git remote add upstream https://github.com/ORIGINAL_OWNER/chopshop-cli.git
```

### Development Environment Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Install pre-commit hooks:
```bash
pre-commit install
```

4. Verify installation:
```bash
chopshop --version
pytest
```

---

## Development Workflow

### Branch Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Individual feature branches
- `bugfix/*`: Bug fix branches
- `hotfix/*`: Urgent production fixes

### Making Changes

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name develop
```

2. Make your changes
3. Write/update tests
4. Update documentation
5. Commit with clear messages:
```bash
git commit -m "feat: add XOR cipher module

- Implement single-byte key brute force
- Add detection for XOR patterns
- Include comprehensive tests
- Update documentation

Closes #123"
```

### Commit Message Format

We follow Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no logic change)
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Build process, dependencies, etc.

**Examples**:
```
feat(cipher): add Vigenere cipher module
fix(detection): improve Base64 signature detection
docs(readme): update installation instructions
test(engine): add recursive decoding edge cases
```

### Keep Your Fork Updated

```bash
git fetch upstream
git checkout develop
git merge upstream/develop
git push origin develop
```

---

## Contribution Types

### 1. New Cipher Modules

The most common contribution! Add support for new cipher types.

**Requirements**:
- Inherit from `CipherModule` base class
- Implement `detect()` and `decode()` methods
- Include comprehensive tests (>90% coverage)
- Add cipher information (`get_info()`)
- Update documentation

**Template**: See `CIPHER_MODULE_GUIDE.md`

**Example**:
```python
# ciphers/my_cipher.py
from chopshop.interfaces import CipherModule, DecodeCandidate

class MyCipher(CipherModule):
    name = "My Cipher"
    aliases = ["mycipher", "mc"]
    category = "classical"
    
    def detect(self, text: str) -> float:
        # Your detection logic
        return confidence_score
    
    def decode(self, text: str) -> List[DecodeCandidate]:
        # Your decoding logic
        return candidates
    
    def get_info(self) -> str:
        return "Educational information about My Cipher..."
```

**Checklist**:
- [ ] Implementation complete
- [ ] Unit tests written (>90% coverage)
- [ ] Integration test added
- [ ] Documentation updated
- [ ] Example added to README
- [ ] CI tests passing

### 2. Bug Fixes

Found a bug? Here's how to fix it:

1. Check if issue already exists
2. Create issue if not (with reproduction steps)
3. Create `bugfix/*` branch
4. Write failing test that demonstrates the bug
5. Fix the bug
6. Ensure test now passes
7. Submit pull request referencing the issue

### 3. Documentation Improvements

Documentation is crucial! Contributions include:

- Fixing typos or unclear explanations
- Adding examples
- Improving API documentation
- Creating tutorials
- Translating documentation

**No code change is too small if it improves clarity!**

### 4. Performance Improvements

Optimize existing code:

1. Profile the code to identify bottlenecks
2. Implement optimization
3. Benchmark before and after
4. Ensure functionality unchanged
5. Document performance gains

**Include benchmark results in PR description.**

### 5. Feature Requests

Have an idea? Great!

1. Check existing issues/discussions
2. Create an issue describing:
   - Use case
   - Proposed solution
   - Examples
   - Potential challenges
3. Discuss with maintainers before implementing
4. Implement after approval

---

## Coding Standards

### Python Style Guide

We follow **PEP 8** with these tools:

**Formatting**: black
```bash
black chopshop/
```

**Linting**: flake8
```bash
flake8 chopshop/
```

**Type Checking**: mypy
```bash
mypy chopshop/
```

**Import Sorting**: isort
```bash
isort chopshop/
```

### Code Quality Rules

1. **Type Hints**: Required for all public APIs
```python
def decode(self, text: str) -> List[DecodeCandidate]:
    pass
```

2. **Docstrings**: Required for all public functions/classes
```python
def my_function(param: str) -> int:
    """
    Brief description.
    
    Args:
        param: Description of param
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param is invalid
    """
    pass
```

3. **Function Complexity**: Maximum McCabe complexity of 10
4. **Function Length**: Keep functions under 50 lines (guideline)
5. **DRY Principle**: Don't Repeat Yourself
6. **SOLID Principles**: Follow object-oriented best practices

### Error Handling

**Always handle exceptions gracefully**:

```python
# âŒ Bad
def decode(text):
    return base64.b64decode(text)  # Can crash!

# âœ… Good
def decode(text):
    try:
        return base64.b64decode(text)
    except Exception as e:
        logger.error(f"Decode failed: {e}")
        return None
```

### Logging

Use the built-in logging system:

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Detailed debugging information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
```

---

## Testing Guidelines

### Test Requirements

- **Coverage**: Minimum 85% for new code
- **Types**: Unit tests + integration tests
- **Edge Cases**: Test error conditions
- **Performance**: Benchmark critical paths

### Writing Tests

**Framework**: pytest

**Location**: `tests/` directory mirroring source structure

**Example**:
```python
# tests/ciphers/test_base64_cipher.py
import pytest
from chopshop.ciphers.base64_cipher import Base64Cipher

class TestBase64Cipher:
    def setup_method(self):
        self.cipher = Base64Cipher()
    
    def test_detect_valid_base64(self):
        text = "SGVsbG8gV29ybGQ="
        confidence = self.cipher.detect(text)
        assert confidence > 0.8
    
    def test_detect_invalid_base64(self):
        text = "This is not base64!"
        confidence = self.cipher.detect(text)
        assert confidence < 0.3
    
    def test_decode_standard_base64(self):
        encoded = "SGVsbG8gV29ybGQ="
        candidates = self.cipher.decode(encoded)
        assert len(candidates) > 0
        assert candidates[0].decoded_text == "Hello World"
    
    def test_decode_url_safe_base64(self):
        encoded = "SGVsbG8_V29ybGQ="
        candidates = self.cipher.decode(encoded)
        assert len(candidates) > 0
    
    @pytest.mark.parametrize("input,expected", [
        ("SGVsbG8=", "Hello"),
        ("V29ybGQ=", "World"),
        ("", ""),
    ])
    def test_decode_parameterized(self, input, expected):
        candidates = self.cipher.decode(input)
        if expected:
            assert candidates[0].decoded_text == expected
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=chopshop --cov-report=html

# Run specific test file
pytest tests/ciphers/test_base64_cipher.py

# Run specific test
pytest tests/ciphers/test_base64_cipher.py::TestBase64Cipher::test_detect_valid_base64

# Run with verbose output
pytest -v

# Run and show print statements
pytest -s
```

### Test Fixtures

Use fixtures for common test data:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_encoded_texts():
    return {
        'base64': 'SGVsbG8gV29ybGQ=',
        'hex': '48656c6c6f20576f726c64',
        'rot13': 'Uryyb Jbeyq',
    }

@pytest.fixture
def temp_config_file(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("max_depth: 5\n")
    return config_file
```

---

## Documentation

### Types of Documentation

1. **Code Documentation**: Docstrings in code
2. **API Documentation**: Auto-generated from docstrings
3. **User Documentation**: Guides and tutorials
4. **Developer Documentation**: Architecture and contributing guides

### Docstring Format

We use Google-style docstrings:

```python
def detect_cipher(text: str, confidence_threshold: float = 0.7) -> List[DetectionResult]:
    """
    Detect likely cipher types used in the given text.
    
    This function analyzes the input text using multiple detection methods
    including signature matching, entropy analysis, and frequency analysis.
    
    Args:
        text: The encoded text to analyze
        confidence_threshold: Minimum confidence score to include in results.
            Must be between 0.0 and 1.0. Default is 0.7.
    
    Returns:
        A list of DetectionResult objects sorted by confidence score in
        descending order. Each result includes the cipher name, confidence
        score, and reasoning.
    
    Raises:
        ValueError: If confidence_threshold is not between 0.0 and 1.0
        TypeError: If text is not a string
    
    Example:
        >>> results = detect_cipher("SGVsbG8gV29ybGQ=")
        >>> results[0].cipher_name
        'Base64'
        >>> results[0].confidence
        0.95
    
    Note:
        This function requires at least one detection module to be loaded.
        If no modules are available, an empty list is returned.
    """
    pass
```

### Updating Documentation

When adding features:
- [ ] Update relevant `.md` files
- [ ] Add docstrings to new code
- [ ] Update CHANGELOG.md
- [ ] Add examples to README if applicable
- [ ] Update API documentation

---

## Pull Request Process

### Before Submitting

**Checklist**:
- [ ] Code follows style guidelines (black, flake8, mypy pass)
- [ ] Tests added/updated and passing (>85% coverage)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Commit messages follow convention
- [ ] Branch is up-to-date with `develop`
- [ ] CI tests passing locally

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123
Related to #456

## Changes Made
- Added XOR cipher module
- Improved detection accuracy
- Updated documentation

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Performance Impact
- Benchmark results: detection speed improved by 15%
- Memory usage: no significant change

## Screenshots (if applicable)
[Attach screenshots of UI changes]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests passing locally
- [ ] Ready for review
```

### Review Process

1. **Automated Checks**: CI must pass
2. **Code Review**: Maintainer reviews code
3. **Discussion**: Address reviewer feedback
4. **Approval**: Maintainer approves
5. **Merge**: Squash and merge to `develop`

### Addressing Feedback

- Respond to all comments
- Make requested changes
- Mark resolved comments
- Re-request review when ready

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and discussions
- **Pull Requests**: Code contributions and reviews

### Getting Help

- Check documentation first
- Search existing issues
- Ask in GitHub Discussions
- Be specific and provide examples

### Recognition

Contributors are recognized in:
- CHANGELOG.md for each release
- Contributors section in README
- GitHub contributors graph

### Becoming a Maintainer

Active contributors may be invited to become maintainers based on:
- Consistent, quality contributions
- Helpful community engagement
- Understanding of project goals
- Commitment to the project

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

If you have questions about contributing, please:
1. Check this guide thoroughly
2. Search existing documentation
3. Ask in GitHub Discussions
4. Contact maintainers if needed

**Thank you for contributing to ChopShop-CLI! Your efforts help make cybersecurity tools more accessible to everyone.**

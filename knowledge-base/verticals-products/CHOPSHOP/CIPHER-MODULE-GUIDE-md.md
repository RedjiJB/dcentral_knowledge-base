---
source_project: CHOPSHOP
source_project_uuid: 019accd8-cfe0-7247-860b-1b169a50a0e1
doc_uuid: 3971b0ab-9fc3-4da3-b905-b84758291266
original_filename: CIPHER_MODULE_GUIDE.md
created_at: 2025-11-28T23:43:28.148161+00:00
content_hash: ef3205646859
---

# Cipher Module Development Guide

## Document Control

**Version:** 1.0  
**Date:** November 28, 2024  
**Audience:** Contributors developing cipher modules

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Module Architecture](#2-module-architecture)
3. [Implementation Guide](#3-implementation-guide)
4. [Detection Strategies](#4-detection-strategies)
5. [Decoding Strategies](#5-decoding-strategies)
6. [Testing Your Module](#6-testing-your-module)
7. [Examples](#7-examples)
8. [Best Practices](#8-best-practices)

---

## 1. Introduction

### 1.1 What is a Cipher Module?

A cipher module is a self-contained unit that:
- Detects when a specific cipher/encoding has been used
- Decodes text encoded with that cipher
- Provides educational information about the cipher
- Follows a standard interface for consistency

### 1.2 Module Categories

**Encodings** (Format conversions, not encryption):
- Base64, Hex, URL encoding, Binary, etc.
- Generally lossless and reversible
- No key required

**Classical Ciphers** (Historical cryptography):
- ROT13, Caesar, Vigenere, Atbash, etc.
- Weak by modern standards
- Can be broken with cryptanalysis

**Modern Ciphers** (Contemporary cryptography):
- AES, RSA, XOR, etc.
- Strong when properly implemented
- May require keys

**Hashes** (One-way functions):
- MD5, SHA256, bcrypt, etc.
- Not reversible (only crackable)
- Used for integrity/passwords

### 1.3 Prerequisites

Before creating a module:
- Understand the cipher algorithm thoroughly
- Know common use cases
- Identify detection patterns
- Research cryptanalysis techniques

---

## 2. Module Architecture

### 2.1 Base Interface

All cipher modules inherit from `CipherModule`:

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class DecodeCandidate:
    """Represents a potential decoded result."""
    decoded_text: str
    confidence: float  # 0.0 to 1.0
    method_details: str
    metadata: Dict[str, Any]

class CipherModule(ABC):
    """Base class for all cipher modules."""
    
    # Class attributes
    name: str = ""              # Full cipher name
    aliases: List[str] = []     # Alternative names
    category: str = ""          # encoding, classical, modern, hash
    
    @abstractmethod
    def detect(self, text: str) -> float:
        """
        Analyze text and return confidence this cipher was used.
        
        Args:
            text: Input string to analyze
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        pass
    
    @abstractmethod
    def decode(self, text: str) -> List[DecodeCandidate]:
        """
        Attempt to decode text.
        
        Args:
            text: Encoded string
            
        Returns:
            List of DecodeCandidate objects, sorted by confidence
        """
        pass
    
    def encode(self, text: str, **kwargs) -> str:
        """
        Encode text (optional, useful for testing).
        
        Args:
            text: Plaintext to encode
            **kwargs: Cipher-specific options
            
        Returns:
            Encoded string
        """
        raise NotImplementedError(f"Encoding not implemented for {self.name}")
    
    def get_info(self) -> str:
        """
        Return educational information about this cipher.
        
        Returns:
            Multi-line string with cipher details
        """
        return f"No information available for {self.name}"
```

### 2.2 File Structure

**Location**: `chopshop/ciphers/your_cipher.py`

**Template**:
```python
"""
Module for [Cipher Name] cipher detection and decoding.

This module implements [brief description of cipher].
"""

from typing import List
from chopshop.interfaces import CipherModule, DecodeCandidate
import logging

logger = logging.getLogger(__name__)


class YourCipher(CipherModule):
    """[Cipher Name] cipher implementation."""
    
    name = "Your Cipher"
    aliases = ["yourcipher", "yc"]
    category = "encoding"  # or classical, modern, hash
    
    def detect(self, text: str) -> float:
        """Detect [Cipher Name] usage."""
        # Implementation
        pass
    
    def decode(self, text: str) -> List[DecodeCandidate]:
        """Decode [Cipher Name] text."""
        # Implementation
        pass
    
    def encode(self, text: str, **kwargs) -> str:
        """Encode using [Cipher Name]."""
        # Implementation
        pass
    
    def get_info(self) -> str:
        """Return information about [Cipher Name]."""
        return """
        [Cipher Name]
        -------------
        [Description, history, uses, weaknesses]
        """
```

---

## 3. Implementation Guide

### 3.1 The `detect()` Method

**Purpose**: Analyze input and return confidence score.

**Implementation Strategy**:

```python
def detect(self, text: str) -> float:
    """
    Detection strategy for [Cipher Name].
    
    Checks performed:
    1. Empty input check
    2. Character set validation
    3. Length validation
    4. Pattern matching
    5. Statistical analysis
    """
    # Step 1: Handle edge cases
    if not text or not text.strip():
        return 0.0
    
    confidence = 0.0
    
    # Step 2: Check character set
    valid_chars = set("ABCDEF0123456789")  # Example for hex
    if not all(c.upper() in valid_chars for c in text.replace(" ", "")):
        return 0.0  # Definitely not this cipher
    
    # Step 3: Check length constraints
    if len(text) < 2:  # Too short
        return 0.1
    
    # Step 4: Pattern matching
    if self._matches_pattern(text):
        confidence += 0.5
    
    # Step 5: Statistical tests
    entropy = self._calculate_entropy(text)
    if 3.5 < entropy < 4.5:  # Good range for this cipher
        confidence += 0.3
    
    # Step 6: Domain-specific checks
    if self._passes_checksum(text):
        confidence += 0.2
    
    return min(confidence, 1.0)  # Cap at 1.0
```

**Key Principles**:
- Return 0.0 for definite non-matches
- Return high confidence (>0.8) only for strong signatures
- Consider multiple indicators
- Use statistical tests when applicable
- Handle edge cases gracefully

### 3.2 The `decode()` Method

**Purpose**: Attempt decoding and return all plausible results.

**Implementation Strategy**:

```python
def decode(self, text: str) -> List[DecodeCandidate]:
    """
    Decoding strategy for [Cipher Name].
    
    Attempts:
    1. Standard decoding
    2. Alternative formats
    3. Error correction
    """
    candidates = []
    
    # Attempt 1: Standard decoding
    try:
        decoded = self._standard_decode(text)
        candidates.append(DecodeCandidate(
            decoded_text=decoded,
            confidence=self._score_result(decoded),
            method_details="Standard [Cipher Name] decoding",
            metadata={'variant': 'standard'}
        ))
    except Exception as e:
        logger.debug(f"Standard decode failed: {e}")
    
    # Attempt 2: Alternative variant
    try:
        decoded = self._alternative_decode(text)
        candidates.append(DecodeCandidate(
            decoded_text=decoded,
            confidence=self._score_result(decoded),
            method_details="Alternative [Cipher Name] decoding",
            metadata={'variant': 'alternative'}
        ))
    except Exception as e:
        logger.debug(f"Alternative decode failed: {e}")
    
    # Attempt 3: With error correction
    if not candidates:
        try:
            decoded = self._decode_with_correction(text)
            candidates.append(DecodeCandidate(
                decoded_text=decoded,
                confidence=self._score_result(decoded) * 0.8,  # Lower confidence
                method_details="[Cipher Name] with error correction",
                metadata={'variant': 'corrected'}
            ))
        except Exception as e:
            logger.debug(f"Corrected decode failed: {e}")
    
    # Sort by confidence
    return sorted(candidates, key=lambda x: x.confidence, reverse=True)
```

**Key Principles**:
- Try multiple decoding strategies
- Catch and log exceptions
- Return all plausible results
- Score each result appropriately
- Sort results by confidence

### 3.3 Helper Methods

**Common Helper Patterns**:

```python
class YourCipher(CipherModule):
    # ... main methods ...
    
    def _validate_input(self, text: str) -> bool:
        """Validate input meets basic requirements."""
        return bool(text and text.strip())
    
    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text."""
        from collections import Counter
        import math
        
        if not text:
            return 0.0
        
        counts = Counter(text)
        total = len(text)
        entropy = -sum(
            (count / total) * math.log2(count / total)
            for count in counts.values()
        )
        return entropy
    
    def _score_result(self, text: str) -> float:
        """Score decoded result for likelihood of being plaintext."""
        if not text:
            return 0.0
        
        # Printability score
        printable = sum(c.isprintable() for c in text) / len(text)
        
        # Entropy (lower is better for plaintext)
        entropy = self._calculate_entropy(text)
        entropy_score = 1.0 - min(entropy / 8.0, 1.0)
        
        # Combine scores
        return (0.6 * printable) + (0.4 * entropy_score)
    
    def _is_likely_encoded(self, text: str) -> bool:
        """Check if text appears to be encoded (vs plaintext)."""
        # High entropy suggests encoding
        entropy = self._calculate_entropy(text)
        if entropy > 6.0:
            return True
        
        # Low printability suggests encoding
        printable = sum(c.isprintable() for c in text) / len(text) if text else 0
        if printable < 0.7:
            return True
        
        return False
```

---

## 4. Detection Strategies

### 4.1 Signature-Based Detection

**Use When**: Cipher has distinctive patterns

**Example: Base64**
```python
def detect(self, text: str) -> float:
    """Detect Base64 encoding."""
    if not text:
        return 0.0
    
    import re
    
    # Base64 charset: A-Z, a-z, 0-9, +, /, =
    base64_pattern = r'^[A-Za-z0-9+/]*={0,2}$'
    
    if not re.match(base64_pattern, text):
        return 0.0
    
    confidence = 0.0
    
    # Length should be multiple of 4
    if len(text) % 4 == 0:
        confidence += 0.5
    
    # Padding validation
    padding = text.count('=')
    if padding <= 2 and (padding == 0 or text.endswith('=' * padding)):
        confidence += 0.4
    
    return confidence
```

### 4.2 Statistical Detection

**Use When**: Cipher affects character distribution

**Example: ROT Cipher**
```python
def detect(self, text: str) -> float:
    """Detect ROT/Caesar cipher using frequency analysis."""
    if not text or not text.isalpha():
        return 0.0
    
    # English letter frequency (approximate)
    ENGLISH_FREQ = {
        'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
        'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, # ...
    }
    
    from collections import Counter
    
    # Calculate actual frequency
    text_upper = text.upper()
    counts = Counter(c for c in text_upper if c.isalpha())
    total = sum(counts.values())
    
    if total == 0:
        return 0.0
    
    actual_freq = {c: (count / total) * 100 for c, count in counts.items()}
    
    # Compare to English frequency
    chi_squared = sum(
        ((actual_freq.get(c, 0) - ENGLISH_FREQ.get(c, 0)) ** 2) / ENGLISH_FREQ.get(c, 1)
        for c in ENGLISH_FREQ
    )
    
    # High chi-squared suggests NOT English â†’ possibly ROT encoded
    if chi_squared > 50:  # Threshold determined empirically
        return 0.7
    
    return 0.2
```

### 4.3 Entropy-Based Detection

**Use When**: Cipher affects randomness

```python
def detect(self, text: str) -> float:
    """Detect based on entropy analysis."""
    entropy = self._calculate_entropy(text)
    
    # Different ciphers have different entropy signatures
    # Base64: ~6.0 bits/char
    # Hex: ~4.0 bits/char
    # Plaintext English: ~4.5 bits/char
    
    if 5.5 <= entropy <= 6.5:
        return 0.8  # Likely Base64 or similar
    elif 3.5 <= entropy <= 4.5:
        return 0.6  # Could be hex or plaintext
    
    return 0.3
```

### 4.4 Hybrid Detection

**Best Practice**: Combine multiple methods

```python
def detect(self, text: str) -> float:
    """Hybrid detection using multiple indicators."""
    if not text:
        return 0.0
    
    scores = []
    
    # Method 1: Signature matching
    if self._matches_signature(text):
        scores.append(0.4)
    
    # Method 2: Entropy analysis
    entropy = self._calculate_entropy(text)
    if self._is_target_entropy_range(entropy):
        scores.append(0.3)
    
    # Method 3: Statistical tests
    if self._passes_statistical_test(text):
        scores.append(0.3)
    
    # Combine scores
    return min(sum(scores), 1.0)
```

---

## 5. Decoding Strategies

### 5.1 Direct Decoding

**Use When**: Deterministic algorithm with no key

**Example: Base64**
```python
def decode(self, text: str) -> List[DecodeCandidate]:
    """Direct Base64 decoding."""
    import base64
    
    candidates = []
    
    try:
        decoded_bytes = base64.b64decode(text, validate=True)
        decoded_text = decoded_bytes.decode('utf-8', errors='replace')
        
        candidates.append(DecodeCandidate(
            decoded_text=decoded_text,
            confidence=self._score_result(decoded_text),
            method_details="Standard Base64 decode",
            metadata={'encoding': 'utf-8'}
        ))
    except Exception as e:
        logger.debug(f"Base64 decode failed: {e}")
    
    return candidates
```

### 5.2 Brute Force Decoding

**Use When**: Limited key space

**Example: ROT Cipher**
```python
def decode(self, text: str) -> List[DecodeCandidate]:
    """Brute force all ROT shifts."""
    candidates = []
    
    # Try all 26 possible shifts
    for shift in range(26):
        decoded = self._rot_decode(text, shift)
        score = self._score_english_text(decoded)
        
        if score > 0.5:  # Only include likely results
            candidates.append(DecodeCandidate(
                decoded_text=decoded,
                confidence=score,
                method_details=f"ROT{shift} decode",
                metadata={'shift': shift}
            ))
    
    return sorted(candidates, key=lambda x: x.confidence, reverse=True)

def _rot_decode(self, text: str, shift: int) -> str:
    """Apply ROT shift."""
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            rotated = chr((ord(char) - base - shift) % 26 + base)
            result.append(rotated)
        else:
            result.append(char)
    return ''.join(result)
```

### 5.3 Cryptanalysis Decoding

**Use When**: Can break cipher mathematically

**Example: Vigenere**
```python
def decode(self, text: str) -> List[DecodeCandidate]:
    """Decode Vigenere using cryptanalysis."""
    candidates = []
    
    # Step 1: Determine likely key length
    key_lengths = self._find_key_length(text)
    
    # Step 2: For each likely key length, crack the key
    for key_length in key_lengths[:3]:  # Try top 3
        try:
            key = self._crack_vigenere_key(text, key_length)
            decoded = self._vigenere_decode(text, key)
            score = self._score_english_text(decoded)
            
            if score > 0.6:
                candidates.append(DecodeCandidate(
                    decoded_text=decoded,
                    confidence=score,
                    method_details=f"Vigenere (key length: {key_length})",
                    metadata={'key': key, 'key_length': key_length}
                ))
        except Exception as e:
            logger.debug(f"Vigenere crack failed for length {key_length}: {e}")
    
    return sorted(candidates, key=lambda x: x.confidence, reverse=True)

def _find_key_length(self, text: str) -> List[int]:
    """Use Kasiski examination and IoC to find key length."""
    # Implementation of Kasiski examination
    # Returns list of likely key lengths sorted by probability
    pass
```

---

## 6. Testing Your Module

### 6.1 Unit Test Template

```python
# tests/ciphers/test_your_cipher.py

import pytest
from chopshop.ciphers.your_cipher import YourCipher


class TestYourCipher:
    """Tests for YourCipher module."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.cipher = YourCipher()
    
    def test_detect_valid_input(self):
        """Test detection with valid input."""
        text = "encoded_string_here"
        confidence = self.cipher.detect(text)
        assert confidence > 0.7  # High confidence
    
    def test_detect_invalid_input(self):
        """Test detection with invalid input."""
        text = "definitely not encoded"
        confidence = self.cipher.detect(text)
        assert confidence < 0.3  # Low confidence
    
    def test_detect_empty_input(self):
        """Test detection with empty input."""
        assert self.cipher.detect("") == 0.0
        assert self.cipher.detect(None) == 0.0 # If applicable
    
    def test_decode_standard(self):
        """Test standard decoding."""
        encoded = "encoded_string"
        expected = "plaintext"
        
        candidates = self.cipher.decode(encoded)
        assert len(candidates) > 0
        assert candidates[0].decoded_text == expected
        assert candidates[0].confidence > 0.8
    
    def test_decode_alternative_format(self):
        """Test alternative format decoding."""
        encoded = "alternative_format"
        candidates = self.cipher.decode(encoded)
        assert len(candidates) > 0
    
    def test_decode_invalid_input(self):
        """Test decoding with invalid input."""
        invalid = "not valid encoding"
        candidates = self.cipher.decode(invalid)
        # Should return empty list or low-confidence results
        if candidates:
            assert candidates[0].confidence < 0.5
    
    @pytest.mark.parametrize("input,expected", [
        ("test1", "result1"),
        ("test2", "result2"),
        ("test3", "result3"),
    ])
    def test_decode_parameterized(self, input, expected):
        """Test multiple inputs."""
        candidates = self.cipher.decode(input)
        assert len(candidates) > 0
        assert candidates[0].decoded_text == expected
    
    def test_encode_decode_roundtrip(self):
        """Test that encode then decode returns original."""
        original = "Hello World"
        encoded = self.cipher.encode(original)
        candidates = self.cipher.decode(encoded)
        assert len(candidates) > 0
        assert candidates[0].decoded_text == original
    
    def test_get_info(self):
        """Test cipher information."""
        info = self.cipher.get_info()
        assert len(info) > 0
        assert self.cipher.name in info
```

### 6.2 Integration Test Template

```python
# tests/integration/test_cipher_integration.py

def test_your_cipher_in_detection_engine():
    """Test cipher integrates with detection engine."""
    from chopshop.detection.auto_detect import AutoDetector
    
    detector = AutoDetector()
    results = detector.detect("encoded_string")
    
    # Your cipher should be in results
    cipher_names = [r.cipher_name for r in results]
    assert "Your Cipher" in cipher_names

def test_your_cipher_in_recursive_decoder():
    """Test cipher works in recursive decoding."""
    from chopshop.engine.recursive_decoder import RecursiveDecoder
    
    decoder = RecursiveDecoder()
    result = decoder.decode("doubly_encoded_string")
    
    # Should successfully decode through multiple layers
    assert "Your Cipher" in result.decode_chain
```

---

## 7. Examples

### 7.1 Complete Example: Hex Cipher

```python
"""
Hexadecimal encoding cipher module.
"""

from typing import List
import logging
import binascii

from chopshop.interfaces import CipherModule, DecodeCandidate

logger = logging.getLogger(__name__)


class HexCipher(CipherModule):
    """Hexadecimal encoding detection and decoding."""
    
    name = "Hexadecimal"
    aliases = ["hex", "hexadecimal"]
    category = "encoding"
    
    def detect(self, text: str) -> float:
        """
        Detect hexadecimal encoding.
        
        Hex characteristics:
        - Only characters: 0-9, A-F (case insensitive)
        - Even length (usually)
        - May have 0x prefix
        """
        if not text:
            return 0.0
        
        # Remove optional 0x prefix
        clean_text = text.removeprefix("0x").removeprefix("0X")
        
        # Remove whitespace
        clean_text = clean_text.replace(" ", "").replace("\n", "")
        
        if not clean_text:
            return 0.0
        
        # Check valid hex charset
        try:
            int(clean_text, 16)
        except ValueError:
            return 0.0
        
        confidence = 0.0
        
        # High confidence if all characters are hex
        confidence += 0.6
        
        # Bonus for even length (pairs of hex digits = bytes)
        if len(clean_text) % 2 == 0:
            confidence += 0.2
        
        # Bonus for reasonable length
        if 4 <= len(clean_text) <= 1000:
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def decode(self, text: str) -> List[DecodeCandidate]:
        """
        Decode hexadecimal encoding.
        
        Tries:
        1. Standard hex decode
        2. Hex with 0x prefix
        3. Hex with spaces
        """
        candidates = []
        
        # Try standard decode
        try:
            decoded = self._hex_to_string(text)
            candidates.append(DecodeCandidate(
                decoded_text=decoded,
                confidence=self._score_result(decoded),
                method_details="Standard hex decode",
                metadata={'format': 'standard'}
            ))
        except Exception as e:
            logger.debug(f"Standard hex decode failed: {e}")
        
        # Try with 0x prefix removed
        if text.startswith(("0x", "0X")):
            try:
                cleaned = text[2:]
                decoded = self._hex_to_string(cleaned)
                candidates.append(DecodeCandidate(
                    decoded_text=decoded,
                    confidence=self._score_result(decoded),
                    method_details="Hex decode (0x prefix removed)",
                    metadata={'format': '0x_prefix'}
                ))
            except Exception as e:
                logger.debug(f"Hex decode with prefix removal failed: {e}")
        
        # Try with spaces removed
        if " " in text:
            try:
                cleaned = text.replace(" ", "")
                decoded = self._hex_to_string(cleaned)
                candidates.append(DecodeCandidate(
                    decoded_text=decoded,
                    confidence=self._score_result(decoded) * 0.9,
                    method_details="Hex decode (spaces removed)",
                    metadata={'format': 'spaced'}
                ))
            except Exception as e:
                logger.debug(f"Hex decode with space removal failed: {e}")
        
        return sorted(candidates, key=lambda x: x.confidence, reverse=True)
    
    def encode(self, text: str, uppercase: bool = False, prefix: bool = False) -> str:
        """
        Encode to hexadecimal.
        
        Args:
            text: Plaintext to encode
            uppercase: Use uppercase hex (default: lowercase)
            prefix: Add 0x prefix (default: False)
        
        Returns:
            Hex-encoded string
        """
        hex_str = text.encode().hex()
        
        if uppercase:
            hex_str = hex_str.upper()
        
        if prefix:
            hex_str = "0x" + hex_str
        
        return hex_str
    
    def get_info(self) -> str:
        """Return information about hexadecimal encoding."""
        return """
        Hexadecimal Encoding
        --------------------
        Hexadecimal (hex) is a base-16 number system using digits 0-9 and
        letters A-F to represent values. Each hex digit represents 4 bits,
        so two hex digits represent one byte.
        
        Common Uses:
        - Color codes (#FF0000 for red)
        - Memory addresses
        - Binary data representation
        - File signatures (magic numbers)
        
        Format:
        - Standard: 48656c6c6f
        - With prefix: 0x48656c6c6f
        - Spaced: 48 65 6c 6c 6f
        
        Example:
        Text: "Hello"
        Hex:  48656c6c6f
        
        Not a cipher, just an encoding format.
        """
    
    def _hex_to_string(self, hex_str: str) -> str:
        """Convert hex string to ASCII string."""
        # Clean input
        cleaned = hex_str.replace(" ", "").replace("\n", "")
        cleaned = cleaned.removeprefix("0x").removeprefix("0X")
        
        # Convert
        bytes_data = bytes.fromhex(cleaned)
        return bytes_data.decode('utf-8', errors='replace')
    
    def _score_result(self, text: str) -> float:
        """Score decoded result."""
        if not text:
            return 0.0
        
        # Printability
        printable = sum(c.isprintable() for c in text) / len(text)
        
        # Entropy (lower is better for plaintext)
        entropy = self._calculate_entropy(text)
        entropy_score = max(0, 1.0 - (entropy / 8.0))
        
        return (0.7 * printable) + (0.3 * entropy_score)
    
    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy."""
        from collections import Counter
        import math
        
        if not text:
            return 0.0
        
        counts = Counter(text)
        total = len(text)
        entropy = -sum(
            (count / total) * math.log2(count / total)
            for count in counts.values()
        )
        return entropy
```

---

## 8. Best Practices

### 8.1 Detection Best Practices

âœ… **Do**:
- Return 0.0 for definite non-matches early
- Use multiple detection methods
- Consider edge cases
- Log debugging information
- Test with varied inputs

âŒ **Don't**:
- Return 1.0 unless absolutely certain
- Crash on invalid input
- Ignore character encoding issues
- Make assumptions about input format

### 8.2 Decoding Best Practices

âœ… **Do**:
- Try multiple decoding strategies
- Handle exceptions gracefully
- Return all plausible results
- Score results appropriately
- Document limitations

âŒ **Don't**:
- Assume input is well-formed
- Return only one result
- Crash on decode failures
- Ignore alternative formats

### 8.3 Code Quality

âœ… **Do**:
- Add type hints
- Write comprehensive docstrings
- Follow PEP 8
- Add logging
- Write tests (>90% coverage)

âŒ **Don't**:
- Use global state
- Hardcode values
- Ignore edge cases
- Skip documentation

### 8.4 Performance

âœ… **Do**:
- Use efficient algorithms
- Cache expensive computations
- Fail fast on invalid input
- Profile for bottlenecks

âŒ **Don't**:
- Use nested loops unnecessarily
- Recalculate same values
- Load large resources repeatedly

---

## 9. Submission Checklist

Before submitting your cipher module:

### Code
- [ ] Inherits from `CipherModule`
- [ ] Implements `detect()` method
- [ ] Implements `decode()` method
- [ ] Implements `get_info()` method
- [ ] Follows coding standards (black, flake8, mypy)
- [ ] Includes type hints
- [ ] Has comprehensive docstrings

### Testing
- [ ] Unit tests written (>90% coverage)
- [ ] Integration tests added
- [ ] Edge cases tested
- [ ] All tests passing

### Documentation
- [ ] Cipher information complete
- [ ] Usage examples provided
- [ ] Limitations documented
- [ ] Added to module list in README

### Quality
- [ ] No hardcoded values
- [ ] Exception handling implemented
- [ ] Logging added
- [ ] Performance acceptable

---

**Congratulations!** You're ready to create high-quality cipher modules for ChopShop-CLI. If you have questions, check existing modules or ask in GitHub Discussions.

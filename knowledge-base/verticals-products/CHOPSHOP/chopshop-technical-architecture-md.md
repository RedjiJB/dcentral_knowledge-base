---
source_project: CHOPSHOP
source_project_uuid: 019accd8-cfe0-7247-860b-1b169a50a0e1
doc_uuid: d80749d5-a82f-4575-9942-c11a7ad7b0ba
original_filename: chopshop_technical_architecture.md
created_at: 2025-11-28T23:43:27.357371+00:00
content_hash: e0617b868b30
---

# ChopShop-CLI Technical Architecture Document
**Version:** 1.0  
**Last Updated:** November 28, 2025  
**Status:** Design Phase

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Principles](#architecture-principles)
3. [System Architecture](#system-architecture)
4. [Component Specifications](#component-specifications)
5. [Data Flow](#data-flow)
6. [API Design](#api-design)
7. [Security Considerations](#security-considerations)
8. [Performance Requirements](#performance-requirements)
9. [Deployment Architecture](#deployment-architecture)
10. [Technology Stack](#technology-stack)

---

## System Overview

### Purpose
ChopShop-CLI is a terminal-based cryptographic analysis tool that automatically detects and decodes encrypted/encoded strings through intelligent pattern recognition and recursive multi-layer decoding.

### Key Capabilities
- **Auto-Detection:** Identifies cipher/encoding type from input string
- **Recursive Decoding:** Handles multi-layer nested encodings automatically
- **Verbose Analysis:** Educational explanations of detection and decoding process
- **Plugin Architecture:** Extensible cipher module system
- **ML-Enhanced:** Machine learning for improved detection accuracy
- **Cross-Platform:** Linux, macOS, Windows PowerShell support

### Target Users
- CTF competitors and security researchers
- Cybersecurity students and educators
- Penetration testers and security professionals
- Cryptography enthusiasts and researchers

---

## Architecture Principles

### 1. Modularity
**Principle:** Each component is self-contained with well-defined interfaces.

**Implementation:**
- Cipher modules are independent, pluggable components
- Detection methods are separate, composable units
- Core engine is decoupled from UI layer
- Clear separation of concerns throughout codebase

**Benefits:**
- Easy to add new cipher types
- Simple to test individual components
- Enables parallel development
- Facilitates community contributions

### 2. Extensibility
**Principle:** System accommodates new features without core changes.

**Implementation:**
- Plugin system for user-defined ciphers
- Configurable detection pipeline
- Modular scoring system
- Hook-based event system for extensions

**Benefits:**
- Community can extend functionality
- Custom cipher implementations supported
- Future-proof architecture
- Minimal technical debt

### 3. Performance
**Principle:** Optimize for speed while maintaining accuracy.

**Implementation:**
- Lazy loading of cipher modules
- Parallel processing of cipher candidates
- Result caching for repeated operations
- Efficient algorithms (avoid brute force when possible)

**Benefits:**
- Sub-second response for common cases
- Scales to complex multi-layer encodings
- Responsive terminal experience
- Suitable for batch processing

### 4. Reliability
**Principle:** Fail gracefully, provide useful error messages.

**Implementation:**
- Comprehensive input validation
- Timeout protection for infinite loops
- Graceful degradation when ML models unavailable
- Extensive error handling and logging

**Benefits:**
- Predictable behavior
- Easy debugging
- Suitable for production use
- User-friendly error messages

### 5. Transparency
**Principle:** Make decision-making process visible to users.

**Implementation:**
- Verbose mode explains each step
- Confidence scores for all detections
- Full decode chain visualization
- Detailed logging at all levels

**Benefits:**
- Educational value
- Debugging capability
- Trust in results
- Learning tool for students

---

## System Architecture

### High-Level Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                      ChopShop-CLI System                      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â”‚
        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
        â–¼                     â–¼                     â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  CLI Layer    â”‚    â”‚  API Layer     â”‚    â”‚  Library     â”‚
â”‚  (Rich/Click) â”‚    â”‚  (REST/gRPC)   â”‚    â”‚  (Python)    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
        â”‚                     â”‚                    â”‚
        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                              â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚  Orchestration   â”‚
                    â”‚  Layer           â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                             â”‚
        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
        â–¼                    â–¼                    â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Detection    â”‚   â”‚  Decoding       â”‚   â”‚  Validation  â”‚
â”‚  Engine       â”‚   â”‚  Engine         â”‚   â”‚  Engine      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜
        â”‚                    â”‚                    â”‚
        â”‚                    â–¼                    â”‚
        â”‚          â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”           â”‚
        â”‚          â”‚  Cipher Module   â”‚           â”‚
        â”‚          â”‚  Registry        â”‚           â”‚
        â”‚          â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜           â”‚
        â”‚                   â”‚                     â”‚
        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                            â–¼
               â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
               â”‚  Built-in Modules       â”‚
               â”‚  - Base64               â”‚
               â”‚  - Hex                  â”‚
               â”‚  - ROT/Caesar           â”‚
               â”‚  - XOR                  â”‚
               â”‚  - VigenÃ¨re             â”‚
               â”‚  - ... (15+ modules)    â”‚
               â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                          â”‚
               â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
               â–¼                     â–¼
        â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
        â”‚  ML Models â”‚      â”‚  User Plugins   â”‚
        â”‚  - SVM     â”‚      â”‚  - Custom       â”‚
        â”‚  - RF      â”‚      â”‚    Modules      â”‚
        â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜      â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Layer Responsibilities

#### 1. Interface Layer
**Components:** CLI, API, Library Interface

**Responsibilities:**
- User input handling and validation
- Output formatting and rendering
- Menu system and navigation
- Error presentation
- Progress indication

**Technologies:** Rich (TUI), Click (CLI), FastAPI (REST API - Phase 3)

#### 2. Orchestration Layer
**Components:** Main Controller, Workflow Manager

**Responsibilities:**
- Request routing and coordination
- Workflow orchestration (detection â†’ decoding â†’ validation)
- Result aggregation and ranking
- Configuration management
- Plugin lifecycle management

**Technologies:** Python core, dependency injection

#### 3. Detection Engine
**Components:** Signature Matcher, Statistical Analyzer, ML Classifier

**Responsibilities:**
- Cipher type identification
- Confidence scoring
- Multi-method fusion
- Feature extraction for ML

**Technologies:** scikit-learn, NumPy, custom algorithms

#### 4. Decoding Engine
**Components:** Recursive Decoder, Chain Tracker, Result Validator

**Responsibilities:**
- Multi-layer decoding
- Decode chain reconstruction
- Loop detection and prevention
- Result validation and scoring

**Technologies:** Python core, concurrent.futures for parallelism

#### 5. Cipher Module Layer
**Components:** CipherModule interface, Built-in modules, Plugin loader

**Responsibilities:**
- Specific cipher implementation
- Detection logic per cipher
- Encoding/decoding operations
- Module discovery and registration

**Technologies:** Abstract base classes, dynamic imports

---

## Component Specifications

### 1. Detection Engine

#### Architecture
```python
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚         DetectionEngine                 â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  + detect(text: str)                    â”‚
â”‚      â†’ List[CipherCandidate]            â”‚
â”‚  + add_detector(detector: Detector)     â”‚
â”‚  + configure(config: Dict)              â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
              â”‚
              â”œâ”€â”€â”€ SignatureDetector
              â”‚    â”œâ”€â”€ detect_base64()
              â”‚    â”œâ”€â”€ detect_hex()
              â”‚    â”œâ”€â”€ detect_binary()
              â”‚    â””â”€â”€ detect_morse()
              â”‚
              â”œâ”€â”€â”€ StatisticalDetector
              â”‚    â”œâ”€â”€ entropy_analysis()
              â”‚    â”œâ”€â”€ frequency_analysis()
              â”‚    â”œâ”€â”€ ioc_calculation()
              â”‚    â””â”€â”€ chi_squared_test()
              â”‚
              â”œâ”€â”€â”€ MLDetector
              â”‚    â”œâ”€â”€ extract_features()
              â”‚    â”œâ”€â”€ classify()
              â”‚    â””â”€â”€ get_confidence()
              â”‚
              â””â”€â”€â”€ HeuristicDetector
                   â”œâ”€â”€ pattern_matching()
                   â”œâ”€â”€ context_analysis()
                   â””â”€â”€ structure_detection()
```

#### Signature-Based Detection

**Purpose:** Fast, rule-based identification using patterns

**Implementation:**
```python
class SignatureDetector:
    signatures = {
        'base64': {
            'pattern': r'^[A-Za-z0-9+/]*={0,2}$',
            'validators': [
                lambda s: len(s) % 4 == 0,
                lambda s: s.count('=') <= 2,
                lambda s: not s.endswith('===')
            ],
            'confidence_base': 0.8
        },
        'hex': {
            'pattern': r'^[0-9A-Fa-f]+$',
            'validators': [
                lambda s: len(s) % 2 == 0,
                lambda s: all(c in '0123456789ABCDEFabcdef' for c in s)
            ],
            'confidence_base': 0.9
        }
        # ... more signatures
    }
    
    def detect(self, text: str) -> List[CipherCandidate]:
        candidates = []
        for cipher_name, signature in self.signatures.items():
            if re.match(signature['pattern'], text):
                if all(validator(text) for validator in signature['validators']):
                    confidence = self._calculate_confidence(text, signature)
                    candidates.append(CipherCandidate(
                        cipher=cipher_name,
                        confidence=confidence,
                        method='signature'
                    ))
        return candidates
```

**Signatures Implemented:**
- Base64 (standard, URL-safe, with/without padding)
- Base32/Base58/Base85
- Hexadecimal
- Binary (ASCII representation)
- Morse code
- URL encoding
- HTML entities
- JWT tokens
- Hash formats (MD5, SHA1, SHA256, bcrypt, etc.)

#### Statistical Analysis

**Purpose:** Mathematical analysis of text properties

**Methods:**

1. **Entropy Analysis**
```python
def calculate_entropy(text: str) -> float:
    """Shannon entropy - measures randomness"""
    freq = Counter(text)
    length = len(text)
    entropy = -sum((count/length) * math.log2(count/length) 
                   for count in freq.values())
    return entropy

# Interpretation:
# 0-2: Very low (likely plaintext or simple cipher)
# 2-4: Medium (compressed or encrypted)
# 4-5: High (random or strong encryption)
# 5-8: Very high (near-random or base-encoded binary)
```

2. **Frequency Analysis**
```python
def frequency_analysis(text: str) -> Dict[str, float]:
    """Compare character distribution to known language patterns"""
    text_freq = calculate_frequency(text)
    english_freq = ENGLISH_FREQUENCY  # Pre-loaded reference
    
    chi_squared = sum(
        ((text_freq[char] - english_freq[char]) ** 2) / english_freq[char]
        for char in string.ascii_lowercase
    )
    
    return {
        'chi_squared': chi_squared,
        'correlation': pearson_correlation(text_freq, english_freq),
        'likely_language': detect_language(text_freq)
    }
```

3. **Index of Coincidence (IoC)**
```python
def index_of_coincidence(text: str) -> float:
    """Detect polyalphabetic ciphers (VigenÃ¨re detection)"""
    n = len(text)
    frequencies = Counter(text.upper())
    
    ioc = sum(freq * (freq - 1) for freq in frequencies.values())
    ioc /= (n * (n - 1))
    
    # Interpretation:
    # ~0.065: English plaintext
    # ~0.038: Random/encrypted
    # Between: Polyalphabetic cipher
    return ioc
```

#### ML-Based Classification

**Purpose:** Learn patterns from training data for improved accuracy

**Model Architecture:**
```python
class MLCipherClassifier:
    def __init__(self):
        self.feature_extractors = [
            CharacterFrequencyExtractor(),
            EntropyExtractor(),
            NgramExtractor(n=2),
            NgramExtractor(n=3),
            StructuralFeatureExtractor()
        ]
        self.model = RandomForestClassifier(n_estimators=100)
        # Alternative: SVC(kernel='rbf', probability=True)
    
    def extract_features(self, text: str) -> np.ndarray:
        """Extract 256-dimensional feature vector"""
        features = []
        
        # Character frequency (256 features for extended ASCII)
        char_freq = np.zeros(256)
        for char in text:
            char_freq[ord(char)] += 1
        char_freq /= len(text)  # Normalize
        features.extend(char_freq)
        
        # Statistical features
        features.append(calculate_entropy(text))
        features.append(len(text))
        features.append(sum(c.isupper() for c in text) / len(text))
        features.append(sum(c.islower() for c in text) / len(text))
        features.append(sum(c.isdigit() for c in text) / len(text))
        features.append(sum(c in string.punctuation for c in text) / len(text))
        
        # N-gram features (top 50 bigrams)
        bigrams = Counter(text[i:i+2] for i in range(len(text)-1))
        bigram_features = [bigrams.get(bg, 0) for bg in TOP_BIGRAMS]
        features.extend(bigram_features)
        
        return np.array(features)
    
    def predict(self, text: str) -> List[CipherCandidate]:
        """Predict cipher type with probability distribution"""
        features = self.extract_features(text).reshape(1, -1)
        probabilities = self.model.predict_proba(features)[0]
        
        candidates = [
            CipherCandidate(
                cipher=self.model.classes_[i],
                confidence=prob,
                method='ml'
            )
            for i, prob in enumerate(probabilities)
            if prob > 0.1  # Threshold for inclusion
        ]
        
        return sorted(candidates, key=lambda x: x.confidence, reverse=True)
```

**Training Data:**
- 10,000+ samples per cipher type
- Mix of CTF challenges, real-world examples, synthetic data
- Balanced dataset to prevent bias
- Continuous improvement via user feedback

**Feature Engineering:**
| Feature Category | Features | Dimensionality |
|-----------------|----------|----------------|
| Character Frequency | ASCII frequency distribution | 256 |
| Statistical | Entropy, length, case ratio, digit ratio | 6 |
| N-grams | Top bigrams, trigrams | 100 |
| Structural | Padding, delimiters, special patterns | 20 |
| **Total** | | **382** |

#### Confidence Fusion

**Purpose:** Combine results from multiple detection methods

```python
class ConfidenceFusion:
    def fuse(self, detections: Dict[str, List[CipherCandidate]]) -> List[CipherCandidate]:
        """
        Combine signature, statistical, and ML detections
        Using weighted voting with confidence calibration
        """
        weights = {
            'signature': 0.5,   # High precision, trust it most
            'statistical': 0.2, # Good supporting evidence
            'ml': 0.3          # Powerful but needs validation
        }
        
        # Group by cipher type
        cipher_scores = defaultdict(list)
        for method, candidates in detections.items():
            for candidate in candidates:
                weighted_confidence = candidate.confidence * weights[method]
                cipher_scores[candidate.cipher].append(
                    (weighted_confidence, method)
                )
        
        # Aggregate scores
        final_candidates = []
        for cipher, scores in cipher_scores.items():
            # Bonus for multi-method agreement
            agreement_bonus = 0.1 * (len(scores) - 1)
            
            # Weighted average
            total_confidence = sum(score for score, _ in scores)
            total_confidence += agreement_bonus
            total_confidence = min(1.0, total_confidence)  # Cap at 1.0
            
            final_candidates.append(CipherCandidate(
                cipher=cipher,
                confidence=total_confidence,
                methods=[method for _, method in scores]
            ))
        
        return sorted(final_candidates, key=lambda x: x.confidence, reverse=True)
```

### 2. Decoding Engine

#### Recursive Decoder Architecture

```python
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚       RecursiveDecoder                   â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  + decode(text: str, max_depth: int)     â”‚
â”‚      â†’ List[DecodeResult]                â”‚
â”‚  + decode_layer(text: str, depth: int)   â”‚
â”‚      â†’ List[LayerResult]                 â”‚
â”‚  - detect_cycle(text: str) â†’ bool        â”‚
â”‚  - score_plaintext(text: str) â†’ float    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
              â”‚
              â”œâ”€â”€â”€ ChainTracker
              â”‚    â”œâ”€â”€ record_step()
              â”‚    â”œâ”€â”€ get_chain()
              â”‚    â””â”€â”€ visualize_chain()
              â”‚
              â”œâ”€â”€â”€ CycleDetector
              â”‚    â”œâ”€â”€ hash_state()
              â”‚    â””â”€â”€ check_cycle()
              â”‚
              â””â”€â”€â”€ ResultValidator
                   â”œâ”€â”€ is_plaintext()
                   â”œâ”€â”€ score_result()
                   â””â”€â”€ rank_results()
```

#### Recursive Decoding Algorithm

```python
class RecursiveDecoder:
    def __init__(self, detection_engine, cipher_registry):
        self.detection_engine = detection_engine
        self.cipher_registry = cipher_registry
        self.max_depth = 10
        self.timeout_seconds = 30
        self.cycle_detector = CycleDetector()
        
    def decode(self, text: str, max_depth: int = 5) -> List[DecodeResult]:
        """
        Main entry point for recursive decoding
        """
        results = []
        start_time = time.time()
        
        def _recursive_helper(current_text: str, depth: int, chain: List[str]):
            # Termination conditions
            if depth >= max_depth:
                return
            
            if time.time() - start_time > self.timeout_seconds:
                raise TimeoutError("Decoding exceeded timeout")
            
            if self.cycle_detector.is_cycle(current_text, chain):
                return  # Prevent infinite loops
            
            # Detect possible ciphers
            candidates = self.detection_engine.detect(current_text)
            
            # Try each candidate
            for candidate in candidates:
                if candidate.confidence < 0.3:
                    continue  # Skip low-confidence candidates
                
                cipher = self.cipher_registry.get(candidate.cipher)
                decoded_outputs = cipher.decode(current_text)
                
                for decoded in decoded_outputs:
                    new_chain = chain + [f"{candidate.cipher}"]
                    
                    # Check if we've reached plaintext
                    if self._is_plaintext(decoded):
                        results.append(DecodeResult(
                            plaintext=decoded,
                            chain=new_chain,
                            confidence=self._score_plaintext(decoded),
                            depth=depth + 1
                        ))
                    else:
                        # Recurse deeper
                        _recursive_helper(decoded, depth + 1, new_chain)
        
        _recursive_helper(text, 0, [])
        
        # Rank and return results
        return sorted(results, key=lambda r: r.confidence, reverse=True)
    
    def _is_plaintext(self, text: str) -> bool:
        """Determine if text is likely plaintext"""
        # Multiple heuristics
        checks = [
            self._is_printable(text),
            self._has_english_words(text),
            self._entropy_in_range(text, 3.0, 5.0),
            self._has_valid_structure(text)
        ]
        
        # Require majority of checks to pass
        return sum(checks) >= len(checks) * 0.6
    
    def _score_plaintext(self, text: str) -> float:
        """Score how likely text is valid plaintext (0.0 - 1.0)"""
        scores = []
        
        # Dictionary match score
        words = re.findall(r'\b\w+\b', text.lower())
        valid_words = sum(1 for w in words if w in ENGLISH_DICTIONARY)
        dict_score = valid_words / len(words) if words else 0
        scores.append(dict_score * 0.4)
        
        # Printability score
        printable_chars = sum(1 for c in text if c in string.printable)
        print_score = printable_chars / len(text)
        scores.append(print_score * 0.2)
        
        # Entropy score (normalized)
        entropy = calculate_entropy(text)
        entropy_score = 1.0 - abs(entropy - 4.0) / 4.0  # 4.0 is ideal
        scores.append(entropy_score * 0.2)
        
        # Structure score (has words, spaces, punctuation)
        has_structure = bool(re.search(r'\w+\s+\w+', text))
        scores.append(0.2 if has_structure else 0)
        
        return min(1.0, sum(scores))
```

#### Cycle Detection

**Purpose:** Prevent infinite loops in recursive decoding

```python
class CycleDetector:
    def __init__(self):
        self.seen_states = set()
        self.state_history = []
    
    def is_cycle(self, text: str, chain: List[str]) -> bool:
        """
        Detect if we've seen this state before
        State = (text_hash, chain_signature)
        """
        state_hash = self._hash_state(text, chain)
        
        if state_hash in self.seen_states:
            return True  # Cycle detected
        
        self.seen_states.add(state_hash)
        self.state_history.append({
            'text_preview': text[:50],
            'chain': chain.copy(),
            'hash': state_hash
        })
        
        return False
    
    def _hash_state(self, text: str, chain: List[str]) -> str:
        """Create unique identifier for state"""
        text_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
        chain_hash = hashlib.sha256('->'.join(chain).encode()).hexdigest()[:16]
        return f"{text_hash}:{chain_hash}"
    
    def reset(self):
        """Clear state for new decoding session"""
        self.seen_states.clear()
        self.state_history.clear()
```

#### Chain Tracking & Visualization

```python
class ChainTracker:
    def __init__(self):
        self.chains = []
        
    def record(self, result: DecodeResult):
        """Record successful decode chain"""
        self.chains.append({
            'input': result.original_text[:100],
            'output': result.plaintext[:100],
            'chain': result.chain,
            'depth': len(result.chain),
            'confidence': result.confidence,
            'timestamp': datetime.now()
        })
    
    def visualize_chain(self, chain: List[str]) -> str:
        """Create visual representation of decode chain"""
        # Example: Base64 â†’ Hex â†’ ROT13 â†’ Plaintext
        
        steps = []
        for i, cipher in enumerate(chain, 1):
            steps.append(f"[{i}] {cipher}")
        
        arrow = " â†’ "
        visualization = arrow.join(steps) + arrow + "Plaintext"
        
        return visualization
    
    def export_chain(self, chain: List[str], format: str = 'json') -> str:
        """Export chain for documentation/sharing"""
        if format == 'json':
            return json.dumps({
                'chain': chain,
                'length': len(chain),
                'timestamp': datetime.now().isoformat()
            }, indent=2)
        elif format == 'markdown':
            md = "# Decode Chain\n\n"
            for i, step in enumerate(chain, 1):
                md += f"{i}. **{step}**\n"
            return md
        elif format == 'cyberchef':
            # Convert to CyberChef recipe format
            recipe = [{'op': cipher, 'args': []} for cipher in chain]
            return json.dumps(recipe)
```

### 3. Cipher Module System

#### Base Interface

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class DecodeResult:
    """Result from a cipher decode operation"""
    output: str
    confidence: float
    metadata: Dict[str, Any] = None
    key: Optional[str] = None

class CipherModule(ABC):
    """Base class for all cipher modules"""
    
    # Metadata
    name: str = "BaseCipher"
    aliases: List[str] = []
    description: str = ""
    category: str = "unknown"  # encoding, classical, modern, hash
    
    # Capabilities
    can_encode: bool = True
    can_decode: bool = True
    requires_key: bool = False
    
    @abstractmethod
    def detect(self, text: str) -> float:
        """
        Determine likelihood this cipher was used
        
        Args:
            text: Input text to analyze
            
        Returns:
            Confidence score from 0.0 to 1.0
        """
        pass
    
    @abstractmethod
    def decode(self, text: str, key: Optional[str] = None) -> List[DecodeResult]:
        """
        Attempt to decode text
        
        Args:
            text: Encoded text
            key: Optional decoding key
            
        Returns:
            List of possible decodings with confidence scores
        """
        pass
    
    def encode(self, text: str, key: Optional[str] = None) -> str:
        """
        Encode plaintext (optional implementation)
        
        Args:
            text: Plaintext to encode
            key: Optional encoding key
            
        Returns:
            Encoded string
        """
        raise NotImplementedError(f"{self.name} does not support encoding")
    
    def get_info(self) -> Dict[str, Any]:
        """Return module information"""
        return {
            'name': self.name,
            'aliases': self.aliases,
            'description': self.description,
            'category': self.category,
            'capabilities': {
                'encode': self.can_encode,
                'decode': self.can_decode,
                'requires_key': self.requires_key
            }
        }
```

#### Example Implementation: Base64

```python
import base64
import re

class Base64Cipher(CipherModule):
    name = "Base64"
    aliases = ["base64", "b64"]
    description = "Base64 encoding (RFC 4648)"
    category = "encoding"
    can_encode = True
    can_decode = True
    requires_key = False
    
    # Patterns
    STANDARD_PATTERN = re.compile(r'^[A-Za-z0-9+/]*={0,2}$')
    URLSAFE_PATTERN = re.compile(r'^[A-Za-z0-9_-]*={0,2}$')
    
    def detect(self, text: str) -> float:
        """Detect Base64 encoding"""
        # Remove whitespace
        text = text.strip()
        
        # Length check (must be multiple of 4 or have valid padding)
        if len(text) % 4 != 0:
            # Check if adding padding would make it valid
            padding_needed = 4 - (len(text) % 4)
            if padding_needed > 2:
                return 0.0
        
        # Pattern matching
        is_standard = bool(self.STANDARD_PATTERN.match(text))
        is_urlsafe = bool(self.URLSAFE_PATTERN.match(text))
        
        if not (is_standard or is_urlsafe):
            return 0.0
        
        # Entropy check (Base64 has high entropy)
        entropy = calculate_entropy(text)
        if entropy < 4.0:
            return 0.3  # Low confidence
        
        # Padding check
        confidence = 0.8
        if text.endswith('=='):
            confidence = 0.95
        elif text.endswith('='):
            confidence = 0.90
        
        # Character distribution check
        char_variety = len(set(text)) / len(text)
        if char_variety > 0.5:  # Good variety suggests Base64
            confidence += 0.05
        
        return min(1.0, confidence)
    
    def decode(self, text: str, key: Optional[str] = None) -> List[DecodeResult]:
        """Decode Base64"""
        results = []
        text = text.strip()
        
        # Try standard Base64
        try:
            decoded = base64.b64decode(text, validate=True)
            # Check if result is printable
            try:
                decoded_str = decoded.decode('utf-8')
                printable_ratio = sum(c in string.printable for c in decoded_str) / len(decoded_str)
                
                results.append(DecodeResult(
                    output=decoded_str,
                    confidence=0.9 if printable_ratio > 0.95 else 0.6,
                    metadata={'variant': 'standard', 'printable_ratio': printable_ratio}
                ))
            except UnicodeDecodeError:
                # Binary data, return hex representation
                results.append(DecodeResult(
                    output=decoded.hex(),
                    confidence=0.7,
                    metadata={'variant': 'standard', 'type': 'binary'}
                ))
        except Exception as e:
            pass  # Invalid Base64
        
        # Try URL-safe Base64
        try:
            # Replace URL-safe chars with standard
            urlsafe_text = text.replace('-', '+').replace('_', '/')
            # Add padding if needed
            padding = 4 - (len(urlsafe_text) % 4)
            if padding != 4:
                urlsafe_text += '=' * padding
            
            decoded = base64.b64decode(urlsafe_text, validate=True)
            decoded_str = decoded.decode('utf-8')
            
            # Only add if different from standard
            if not results or decoded_str != results[0].output:
                results.append(DecodeResult(
                    output=decoded_str,
                    confidence=0.85,
                    metadata={'variant': 'urlsafe'}
                ))
        except Exception:
            pass
        
        return results
    
    def encode(self, text: str, key: Optional[str] = None) -> str:
        """Encode to Base64"""
        return base64.b64encode(text.encode()).decode()
```

#### Example Implementation: ROT/Caesar Cipher

```python
class ROTCipher(CipherModule):
    name = "ROT/Caesar"
    aliases = ["rot", "caesar", "rot13", "rot-n"]
    description = "ROT cipher (all rotations 1-25)"
    category = "classical"
    can_encode = True
    can_decode = True
    requires_key = False
    
    def detect(self, text: str) -> float:
        """Detect ROT cipher"""
        # Must be mostly letters
        letter_ratio = sum(c.isalpha() for c in text) / len(text)
        if letter_ratio < 0.7:
            return 0.0
        
        # Check frequency distribution
        freq_analysis = frequency_analysis(text)
        chi_squared = freq_analysis['chi_squared']
        
        # ROT ciphers maintain frequency distribution
        # but shift it, so chi-squared is moderate
        if 100 < chi_squared < 1000:
            return 0.6
        
        return 0.3
    
    def decode(self, text: str, key: Optional[str] = None) -> List[DecodeResult]:
        """Try all 25 rotations"""
        results = []
        
        for rotation in range(1, 26):
            decoded = self._rotate(text, rotation)
            score = self._score_english(decoded)
            
            if score > 0.5:  # Only include likely candidates
                results.append(DecodeResult(
                    output=decoded,
                    confidence=score,
                    metadata={'rotation': rotation},
                    key=str(rotation)
                ))
        
        return sorted(results, key=lambda r: r.confidence, reverse=True)[:3]
    
    def _rotate(self, text: str, n: int) -> str:
        """Rotate text by n positions"""
        result = []
        for char in text:
            if char.isupper():
                result.append(chr((ord(char) - ord('A') + n) % 26 + ord('A')))
            elif char.islower():
                result.append(chr((ord(char) - ord('a') + n) % 26 + ord('a')))
            else:
                result.append(char)
        return ''.join(result)
    
    def _score_english(self, text: str) -> float:
        """Score how English-like the text is"""
        words = re.findall(r'\b\w+\b', text.lower())
        if not words:
            return 0.0
        
        valid_words = sum(1 for w in words if w in ENGLISH_DICTIONARY)
        return valid_words / len(words)
    
    def encode(self, text: str, key: Optional[str] = None) -> str:
        """Encode with specified rotation (default ROT13)"""
        rotation = int(key) if key else 13
        return self._rotate(text, rotation)
```

### 4. Verbose Logging System

#### Architecture

```python
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚      VerboseLogger                 â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  + log_detection(candidates)       â”‚
â”‚  + log_decode_attempt(cipher)      â”‚
â”‚  + log_decode_result(result)       â”‚
â”‚  + log_chain(chain)                â”‚
â”‚  + set_verbosity(level)            â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
              â”‚
              â”œâ”€â”€â”€ ColorFormatter
              â”‚    â”œâ”€â”€ format_info()
              â”‚    â”œâ”€â”€ format_success()
              â”‚    â”œâ”€â”€ format_error()
              â”‚    â””â”€â”€ format_warning()
              â”‚
              â””â”€â”€â”€ ProgressTracker
                   â”œâ”€â”€ show_spinner()
                   â”œâ”€â”€ show_progress_bar()
                   â””â”€â”€ show_table()
```

#### Implementation

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree
from rich.syntax import Syntax

class VerboseLogger:
    def __init__(self, verbosity_level: int = 1):
        """
        verbosity_level:
            0 = quiet (results only)
            1 = normal (key steps)
            2 = verbose (detailed analysis)
            3 = debug (everything)
        """
        self.console = Console()
        self.verbosity = verbosity_level
        self.step_counter = 0
    
    def log_detection(self, text: str, candidates: List[CipherCandidate]):
        """Log detection phase results"""
        if self.verbosity < 1:
            return
        
        self.console.print("\n[bold cyan]ðŸ” Detection Phase[/bold cyan]")
        self.console.print(f"[dim]Input length: {len(text)} characters[/dim]")
        
        if self.verbosity >= 2:
            self.console.print(f"[dim]Entropy: {calculate_entropy(text):.2f}[/dim]")
            self.console.print(f"[dim]Printable ratio: {self._printable_ratio(text):.1%}[/dim]")
        
        # Create table of candidates
        table = Table(title="Cipher Candidates", show_header=True)
        table.add_column("Rank", style="cyan", width=6)
        table.add_column("Cipher", style="magenta")
        table.add_column("Confidence", justify="right", style="green")
        table.add_column("Method", style="yellow")
        
        for i, candidate in enumerate(candidates[:5], 1):
            confidence_bar = "â–ˆ" * int(candidate.confidence * 20)
            table.add_row(
                f"#{i}",
                candidate.cipher,
                f"{candidate.confidence:.2%} {confidence_bar}",
                ", ".join(candidate.methods)
            )
        
        self.console.print(table)
    
    def log_decode_attempt(self, cipher_name: str, input_text: str):
        """Log when attempting to decode with a cipher"""
        if self.verbosity < 2:
            return
        
        self.step_counter += 1
        self.console.print(
            f"\n[yellow]â†’ Step {self.step_counter}:[/yellow] "
            f"Attempting [bold]{cipher_name}[/bold] decode..."
        )
        
        if self.verbosity >= 3:
            preview = input_text[:80] + "..." if len(input_text) > 80 else input_text
            self.console.print(f"[dim]  Input: {preview}[/dim]")
    
    def log_decode_result(self, cipher_name: str, results: List[DecodeResult], layer: int):
        """Log decode results"""
        if self.verbosity < 1:
            return
        
        if not results:
            self.console.print(f"[red]âœ— {cipher_name}: No valid decoding[/red]")
            return
        
        best_result = results[0]
        
        if best_result.confidence > 0.8:
            icon = "âœ“"
            color = "green"
        elif best_result.confidence > 0.5:
            icon = "~"
            color = "yellow"
        else:
            icon = "?"
            color = "red"
        
        self.console.print(
            f"[{color}]{icon} {cipher_name}:[/{color}] "
            f"Decoded ({best_result.confidence:.0%} confidence)"
        )
        
        if self.verbosity >= 2:
            preview = best_result.output[:100] + "..." if len(best_result.output) > 100 else best_result.output
            self.console.print(f"[dim]  Output: {preview}[/dim]")
            
            if best_result.metadata:
                meta_str = ", ".join(f"{k}={v}" for k, v in best_result.metadata.items())
                self.console.print(f"[dim]  Metadata: {meta_str}[/dim]")
    
    def log_chain(self, chain: List[str], final_text: str):
        """Visualize complete decode chain"""
        if self.verbosity < 1:
            return
        
        self.console.print("\n[bold green]ðŸŽ‰ Decode Chain Resolved[/bold green]")
        
        # Create tree visualization
        tree = Tree("ðŸ“¥ Input")
        current = tree
        
        for cipher in chain:
            current = current.add(f"ðŸ”“ [cyan]{cipher}[/cyan]")
        
        current.add(f"ðŸ“„ [bold green]Plaintext[/bold green]")
        
        self.console.print(tree)
        
        # Show final result
        panel = Panel(
            final_text[:500] + ("..." if len(final_text) > 500 else ""),
            title="[bold]Decoded Result[/bold]",
            border_style="green"
        )
        self.console.print(panel)
    
    def log_educational_context(self, cipher_name: str):
        """Provide educational information about cipher"""
        if self.verbosity < 2:
            return
        
        context = CIPHER_EDUCATIONAL_INFO.get(cipher_name, {})
        if not context:
            return
        
        self.console.print(f"\n[blue]â„¹ï¸  About {cipher_name}:[/blue]")
        self.console.print(f"[dim]{context.get('description', 'N/A')}[/dim]")
        
        if 'common_use' in context:
            self.console.print(f"[dim]Common use: {context['common_use']}[/dim]")
        
        if 'weakness' in context:
            self.console.print(f"[dim]âš ï¸  Weakness: {context['weakness']}[/dim]")
```

#### Educational Context Database

```python
CIPHER_EDUCATIONAL_INFO = {
    'Base64': {
        'description': 'Binary-to-text encoding scheme using 64 printable ASCII characters',
        'common_use': 'Email attachments, embedding images in HTML/CSS, URL encoding',
        'weakness': 'Not encryption, trivially reversible',
        'history': 'Defined in RFC 4648 (2006), used in MIME since 1992'
    },
    'ROT13': {
        'description': 'Letter substitution cipher that replaces each letter with the letter 13 positions after it',
        'common_use': 'Obscuring spoilers, hiding puzzle solutions, simple obfuscation',
        'weakness': 'Trivially broken, offers no security',
        'history': 'Popularized on Usenet in the 1980s'
    },
    'XOR': {
        'description': 'Bitwise exclusive OR operation, symmetric cipher when used with a key',
        'common_use': 'Simple encryption, malware obfuscation, stream ciphers',
        'weakness': 'Single-byte XOR easily broken via frequency analysis',
        'history': 'Foundation of many modern ciphers (RC4, ChaCha20)'
    },
    # ... more entries
}
```

---

## Data Flow

### End-to-End Flow Diagram

```
User Input
    â”‚
    â”œâ”€> Input Validation
    â”‚       â”‚
    â”‚       â”œâ”€> Length check
    â”‚       â”œâ”€> Character encoding check
    â”‚       â””â”€> Format validation
    â”‚
    â”œâ”€> Detection Engine
    â”‚       â”‚
    â”‚       â”œâ”€> Signature Detection
    â”‚       â”‚       â””â”€> Pattern matching
    â”‚       â”‚
    â”‚       â”œâ”€> Statistical Analysis
    â”‚       â”‚       â”œâ”€> Entropy calculation
    â”‚       â”‚       â”œâ”€> Frequency analysis
    â”‚       â”‚       â””â”€> IoC calculation
    â”‚       â”‚
    â”‚       â”œâ”€> ML Classification
    â”‚       â”‚       â”œâ”€> Feature extraction
    â”‚       â”‚       â””â”€> Model prediction
    â”‚       â”‚
    â”‚       â””â”€> Confidence Fusion
    â”‚               â””â”€> Weighted combination
    â”‚
    â”œâ”€> Recursive Decoder
    â”‚       â”‚
    â”‚       â”œâ”€> For each cipher candidate:
    â”‚       â”‚   â”œâ”€> Attempt decode
    â”‚       â”‚   â”œâ”€> Validate result
    â”‚       â”‚   â””â”€> If not plaintext:
    â”‚       â”‚       â””â”€> Recurse (next layer)
    â”‚       â”‚
    â”‚       â”œâ”€> Cycle Detection
    â”‚       â”‚   â””â”€> Prevent infinite loops
    â”‚       â”‚
    â”‚       â””â”€> Chain Tracking
    â”‚           â””â”€> Record each step
    â”‚
    â”œâ”€> Result Validation
    â”‚       â”‚
    â”‚       â”œâ”€> Plaintext scoring
    â”‚       â”œâ”€> Dictionary checking
    â”‚       â”œâ”€> Structure validation
    â”‚       â””â”€> Confidence calculation
    â”‚
    â””â”€> Output Rendering
            â”‚
            â”œâ”€> Format results
            â”œâ”€> Visualize chain
            â”œâ”€> Generate verbose log
            â””â”€> Display to user
```

### Detailed Data Structures

#### CipherCandidate

```python
@dataclass
class CipherCandidate:
    cipher: str                    # Cipher name (e.g., "Base64")
    confidence: float              # 0.0 - 1.0
    methods: List[str]             # Detection methods that identified it
    metadata: Dict[str, Any]       # Additional detection info
    
    def __lt__(self, other):
        return self.confidence < other.confidence
```

#### DecodeResult

```python
@dataclass
class DecodeResult:
    output: str                    # Decoded text
    confidence: float              # How confident we are
    metadata: Dict[str, Any]       # Cipher-specific info
    key: Optional[str] = None      # Key used (if applicable)
    timestamp: datetime = field(default_factory=datetime.now)
```

#### CompleteResult

```python
@dataclass
class CompleteResult:
    original_input: str
    final_output: str
    decode_chain: List[str]
    total_confidence: float
    depth: int
    execution_time: float
    intermediate_results: List[DecodeResult]
    
    def to_dict(self) -> Dict:
        """Export as dictionary for JSON/logging"""
        return {
            'input': self.original_input[:100],
            'output': self.final_output[:500],
            'chain': self.decode_chain,
            'confidence': self.total_confidence,
            'depth': self.depth,
            'time_ms': self.execution_time * 1000,
            'steps': len(self.intermediate_results)
        }
```

---

## API Design

### CLI Interface

```bash
# Basic usage
chopshop decode "SGVsbG8gV29ybGQh"

# With verbosity
chopshop decode "SGVsbG8gV29ybGQh" -v          # verbose
chopshop decode "SGVsbG8gV29ybGQh" -vv         # very verbose
chopshop decode "SGVsbG8gV29ybGQh" -q          # quiet

# Specify max depth
chopshop decode "..." --max-depth 10

# From file
chopshop decode --file encoded.txt

# Batch mode
chopshop batch input_file.txt --output results.json

# Interactive mode
chopshop interactive

# Plugin management
chopshop plugins list
chopshop plugins install my_cipher.py
chopshop plugins info Base64

# Educational mode
chopshop learn Base64
chopshop analyze "SGVsbG8gV29ybGQh" --explain
```

### Python Library Interface (Phase 3)

```python
from chopshop import ChopShop, Config

# Initialize
cs = ChopShop(Config(
    verbosity=2,
    max_depth=5,
    timeout=30
))

# Simple decode
result = cs.decode("SGVsbG8gV29ybGQh")
print(result.final_output)  # "Hello World!"
print(result.chain)         # ["Base64"]

# Get all candidates
results = cs.decode_all("...", return_alternatives=True)
for r in results:
    print(f"{r.chain} -> {r.output} ({r.confidence:.0%})")

# Analyze without decoding
candidates = cs.detect("SGVsbG8gV29ybGQh")
for c in candidates:
    print(f"{c.cipher}: {c.confidence:.0%}")

# Use specific cipher
result = cs.decode_with("...", cipher="ROT13")
```

### REST API (Phase 3)

```python
# Endpoints
POST /api/v1/decode
{
  "text": "SGVsbG8gV29ybGQh",
  "options": {
    "max_depth": 5,
    "timeout": 30,
    "return_alternatives": false
  }
}

Response:
{
  "success": true,
  "result": {
    "input": "SGVsbG8gV29ybGQh",
    "output": "Hello World!",
    "chain": ["Base64"],
    "confidence": 0.95,
    "execution_time_ms": 42
  }
}

GET /api/v1/ciphers
Response: List of available cipher modules

POST /api/v1/detect
{
  "text": "SGVsbG8gV29ybGQh"
}

Response:
{
  "candidates": [
    {"cipher": "Base64", "confidence": 0.92},
    {"cipher": "Hex", "confidence": 0.08}
  ]
}
```

---

## Security Considerations

### Input Validation

**Risks:**
- Maliciously long inputs (DoS)
- Binary data causing crashes
- Injection attacks via plugin system

**Mitigations:**
```python
def validate_input(text: str) -> None:
    # Length limit
    MAX_INPUT_LENGTH = 10 * 1024 * 1024  # 10 MB
    if len(text) > MAX_INPUT_LENGTH:
        raise ValueError(f"Input too long (max {MAX_INPUT_LENGTH} bytes)")
    
    # Character encoding validation
    try:
        text.encode('utf-8')
    except UnicodeEncodeError:
        raise ValueError("Invalid character encoding")
    
    # Null byte protection
    if '\x00' in text:
        raise ValueError("Null bytes not allowed in input")
```

### Resource Limits

**Protection Against:**
- Infinite loops
- Memory exhaustion
- CPU abuse

**Implementation:**
```python
import resource
import signal

class ResourceLimiter:
    def __init__(self, timeout_seconds=30, memory_mb=512):
        self.timeout = timeout_seconds
        self.memory = memory_mb * 1024 * 1024
    
    def __enter__(self):
        # Set timeout
        signal.signal(signal.SIGALRM, self._timeout_handler)
        signal.alarm(self.timeout)
        
        # Set memory limit (Unix only)
        try:
            resource.setrlimit(
                resource.RLIMIT_AS,
                (self.memory, self.memory)
            )
        except:
            pass  # Windows doesn't support this
    
    def __exit__(self, *args):
        signal.alarm(0)  # Cancel timeout
    
    def _timeout_handler(self, signum, frame):
        raise TimeoutError("Operation exceeded time limit")

# Usage
with ResourceLimiter(timeout_seconds=30):
    result = decode_text(input_text)
```

### Plugin Sandboxing (Phase 2)

**Risks:**
- Malicious user plugins
- Arbitrary code execution
- File system access

**Mitigations:**
- Plugin validation and code review
- Restricted imports (no `os`, `subprocess`, `eval`)
- Read-only access to resources
- Separate process execution for untrusted plugins

```python
ALLOWED_IMPORTS = {
    're', 'string', 'math', 'collections', 'itertools',
    'base64', 'binascii', 'hashlib', 'hmac'
}

FORBIDDEN_IMPORTS = {
    'os', 'subprocess', 'sys', 'eval', 'exec', 'compile',
    '__import__', 'open', 'file', 'socket', 'urllib'
}

def validate_plugin_code(code: str) -> None:
    """Static analysis of plugin code for dangerous patterns"""
    import ast
    
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise ValueError(f"Plugin has syntax errors: {e}")
    
    for node in ast.walk(tree):
        # Check imports
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in FORBIDDEN_IMPORTS:
                    raise ValueError(f"Forbidden import: {alias.name}")
        
        # Check dangerous functions
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ['eval', 'exec', 'compile', '__import__']:
                    raise ValueError(f"Forbidden function call: {node.func.id}")
```

---

## Performance Requirements

### Response Time Targets

| Operation | Target | Maximum |
|-----------|--------|---------|
| Simple decode (1 layer) | <100ms | 500ms |
| Medium decode (3 layers) | <500ms | 2s |
| Complex decode (5+ layers) | <2s | 10s |
| Detection only | <50ms | 200ms |
| Startup time | <500ms | 1s |

### Throughput Targets (Phase 3)

| Scenario | Target |
|----------|--------|
| Batch processing | 100+ strings/second |
| API requests | 50+ requests/second |
| Concurrent users | 100+ simultaneous |

### Memory Usage

- **Base footprint:** <50 MB
- **Per operation:** <10 MB
- **ML models:** <100 MB total
- **Peak usage:** <500 MB

### Optimization Strategies

1. **Lazy Loading**
```python
class CipherRegistry:
    def __init__(self):
        self._modules = {}  # Cached instances
        self._module_paths = {}  # File paths
    
    def get(self, cipher_name: str) -> CipherModule:
        """Load module only when needed"""
        if cipher_name not in self._modules:
            module_path = self._module_paths[cipher_name]
            self._modules[cipher_name] = self._load_module(module_path)
        return self._modules[cipher_name]
```

2. **Caching**
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def calculate_entropy(text: str) -> float:
    """Cache entropy calculations"""
    # ... implementation
    
@lru_cache(maxsize=500)
def detect_cipher_type(text: str) -> List[CipherCandidate]:
    """Cache detection results"""
    # ... implementation
```

3. **Parallel Processing**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def decode_parallel(text: str, candidates: List[CipherCandidate]) -> List[DecodeResult]:
    """Try multiple ciphers in parallel"""
    results = []
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(cipher.decode, text): cipher 
            for cipher in candidates
        }
        
        for future in as_completed(futures):
            try:
                result = future.result(timeout=5)
                results.extend(result)
            except Exception as e:
                logger.warning(f"Cipher decode failed: {e}")
    
    return results
```

---

## Deployment Architecture

### Local Installation (Phase 1)

```bash
# Via pip
pip install chopshop-cli

# Via pipx (isolated)
pipx install chopshop-cli

# From source
git clone https://github.com/user/chopshop-cli
cd chopshop-cli
pip install -e .
```

### Docker Container (Phase 1)

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy application
COPY chopshop/ /app/chopshop/
COPY assets/ /app/assets/
WORKDIR /app

# Entry point
ENTRYPOINT ["python", "-m", "chopshop"]
```

```bash
# Build
docker build -t chopshop-cli .

# Run
docker run -it chopshop-cli decode "SGVsbG8gV29ybGQh"

# Interactive mode
docker run -it chopshop-cli interactive
```

### CI/CD Pipeline

```yaml
# .github/workflows/test.yml
name: Test and Build

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -e .[dev]
    
    - name: Run tests
      run: |
        pytest --cov=chopshop --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
  
  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build package
      run: |
        python -m build
    
    - name: Publish to PyPI
      if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags')
      run: |
        twine upload dist/*
```

---

## Technology Stack Summary

### Core Stack
| Component | Technology | Justification |
|-----------|-----------|---------------|
| Language | Python 3.10+ | Rich ecosystem, easy ML integration, cross-platform |
| CLI Framework | Click | Industry standard, powerful, well-documented |
| Terminal UI | Rich | Beautiful formatting, modern, actively maintained |
| ML Framework | scikit-learn | Lightweight, offline-capable, excellent for classic ML |
| Testing | pytest | De facto standard, excellent plugins, fast |
| Packaging | Poetry | Modern dependency management, build tool |

### Development Tools
| Tool | Purpose |
|------|---------|
| black | Code formatting |
| flake8 | Linting |
| mypy | Type checking |
| pytest-cov | Coverage reporting |
| pre-commit | Git hooks |
| Sphinx | Documentation generation |

### Dependencies
```toml
[tool.poetry.dependencies]
python = "^3.10"
rich = "^13.0.0"
click = "^8.0.0"
scikit-learn = "^1.3.0"
numpy = "^1.24.0"
cryptography = "^41.0.0"
pycryptodome = "^3.19.0"
colorama = "^0.4.6"

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
black = "^23.0.0"
flake8 = "^6.0.0"
mypy = "^1.5.0"
pre-commit = "^3.4.0"
sphinx = "^7.2.0"
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-28 | Toussaint | Initial technical architecture document |

---

## Next Steps

1. Review and approve this architecture document
2. Begin implementation of Phase 1 components
3. Set up development environment and CI/CD
4. Create detailed API specifications for each component
5. Begin cipher module implementation

---

*This document serves as the technical blueprint for ChopShop-CLI development. All architectural decisions should reference and update this document.*

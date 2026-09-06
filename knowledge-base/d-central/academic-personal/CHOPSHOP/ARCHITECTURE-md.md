---
source_project: CHOPSHOP
source_project_uuid: 019accd8-cfe0-7247-860b-1b169a50a0e1
doc_uuid: a9dda6b1-126e-4263-8a9e-b5880a91fe44
original_filename: ARCHITECTURE.md
created_at: 2025-11-28T23:43:22.432900+00:00
content_hash: cf66b9edbc0e
topic: chopshop-project-documentation
consolidated_into: docs/DC-CHOPSHOP-PROJECT-DOCUMENTATION-RECONCILED-001.md
---

# ChopShop-CLI Architecture Document

## Document Control

**Version:** 1.0  
**Date:** November 28, 2024  
**Author:** Toussaint  
**Status:** Draft

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Architecture Principles](#2-architecture-principles)
3. [System Architecture](#3-system-architecture)
4. [Component Design](#4-component-design)
5. [Data Flow](#5-data-flow)
6. [Technology Stack](#6-technology-stack)
7. [Security Architecture](#7-security-architecture)
8. [Performance Considerations](#8-performance-considerations)
9. [Deployment Architecture](#9-deployment-architecture)
10. [Future Architecture Evolution](#10-future-architecture-evolution)

---

## 1. System Overview

### 1.1 Purpose

ChopShop-CLI is a modular, intelligent cryptography analysis tool that automatically detects and decodes encrypted/encoded strings through recursive multi-layer analysis with educational verbose output.

### 1.2 High-Level Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                     ChopShop-CLI                            â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  CLI Layer (User Interface)                                 â”‚
â”‚    â”œâ”€â”€ Menu System                                          â”‚
â”‚    â”œâ”€â”€ Verbose Renderer                                     â”‚
â”‚    â””â”€â”€ ANSI Color Output                                    â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  Core Engine Layer                                          â”‚
â”‚    â”œâ”€â”€ Auto-Detection Engine                                â”‚
â”‚    â”œâ”€â”€ Recursive Decoder                                    â”‚
â”‚    â”œâ”€â”€ Chain Tracker                                        â”‚
â”‚    â””â”€â”€ Result Scorer/Validator                              â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  Analysis Layer                                             â”‚
â”‚    â”œâ”€â”€ Entropy Analysis                                     â”‚
â”‚    â”œâ”€â”€ Frequency Analysis                                   â”‚
â”‚    â”œâ”€â”€ Dictionary Scoring                                   â”‚
â”‚    â”œâ”€â”€ Signature Detection                                  â”‚
â”‚    â””â”€â”€ ML Classifier (optional)                             â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  Cipher Module Layer (Plugin Architecture)                  â”‚
â”‚    â”œâ”€â”€ Base Encodings (Base64, Hex, etc.)                   â”‚
â”‚    â”œâ”€â”€ Classical Ciphers (ROT, Caesar, etc.)                â”‚
â”‚    â”œâ”€â”€ Modern Ciphers (XOR, AES, etc.)                      â”‚
â”‚    â””â”€â”€ User-Defined Plugins                                 â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚  Data & Resources Layer                                     â”‚
â”‚    â”œâ”€â”€ Wordlists/Dictionaries                               â”‚
â”‚    â”œâ”€â”€ ML Models                                            â”‚
â”‚    â”œâ”€â”€ Configuration                                        â”‚
â”‚    â””â”€â”€ Cache/Session Data                                   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### 1.3 Key Architectural Characteristics

- **Modular**: Plugin-based cipher architecture
- **Extensible**: Easy to add new detection/decoding modules
- **Intelligent**: ML-augmented detection without LLM dependency
- **Recursive**: Native support for multi-layer encodings
- **Offline**: No internet dependency for core functionality
- **Educational**: Verbose logging explains every operation
- **Portable**: Single Python package, cross-platform

---

## 2. Architecture Principles

### 2.1 Design Principles

1. **Separation of Concerns**
   - CLI logic separate from core engine
   - Detection separate from decoding
   - Analysis modules independent and composable

2. **Plugin Architecture**
   - All cipher modules follow common interface
   - Hot-loading of user-defined plugins
   - No core modification needed for new ciphers

3. **Fail-Safe Operation**
   - Graceful degradation on errors
   - Never crash on malformed input
   - Always return best-effort results

4. **Educational First**
   - Every operation can be explained
   - Verbose mode as first-class feature
   - Transparency in decision-making

5. **Performance Optimization**
   - Lazy loading of heavy modules
   - Parallel processing where possible
   - Caching of expensive operations

6. **Security by Design**
   - Sandboxed plugin execution
   - No arbitrary code execution
   - Input validation at all boundaries

### 2.2 SOLID Principles Application

- **Single Responsibility**: Each module has one clear purpose
- **Open/Closed**: Open for extension (plugins), closed for modification
- **Liskov Substitution**: All cipher modules interchangeable
- **Interface Segregation**: Minimal, focused interfaces
- **Dependency Inversion**: Depend on abstractions, not concrete implementations

---

## 3. System Architecture

### 3.1 Layered Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    Presentation Layer                     â”‚
â”‚  - CLI Interface                                         â”‚
â”‚  - Menu System                                           â”‚
â”‚  - Output Formatting                                     â”‚
â”‚  - User Input Handling                                   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
             â”‚
             â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   Application Layer                       â”‚
â”‚  - Command Processing                                    â”‚
â”‚  - Workflow Orchestration                                â”‚
â”‚  - Session Management                                    â”‚
â”‚  - Configuration Management                              â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
             â”‚
             â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                    Business Logic Layer                   â”‚
â”‚  - Auto-Detection Engine                                 â”‚
â”‚  - Recursive Decoding Engine                             â”‚
â”‚  - Scoring & Validation                                  â”‚
â”‚  - Chain Tracking & Analysis                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
             â”‚
             â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   Domain Layer (Plugins)                  â”‚
â”‚  - Cipher Modules                                        â”‚
â”‚  - Analysis Modules                                      â”‚
â”‚  - Scoring Modules                                       â”‚
â”‚  - Detector Modules                                      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
             â”‚
             â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                 Infrastructure Layer                      â”‚
â”‚  - File I/O                                              â”‚
â”‚  - Logging                                               â”‚
â”‚  - Caching                                               â”‚
â”‚  - External Tool Integration                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### 3.2 Component Interaction Diagram

```
User Input
    â”‚
    â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ CLI Handler â”‚
â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”˜
       â”‚
       â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”      â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Command Parser  â”‚â”€â”€â”€â”€â”€â–¶â”‚ Config Manager   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜      â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
         â”‚
         â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚      Recursive Decoding Engine          â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚  1. Auto-Detection Engine       â”‚   â”‚
â”‚  â”‚     â”œâ”€ Signature Detector       â”‚   â”‚
â”‚  â”‚     â”œâ”€ Entropy Analyzer         â”‚   â”‚
â”‚  â”‚     â”œâ”€ Frequency Analyzer       â”‚   â”‚
â”‚  â”‚     â””â”€ ML Classifier (opt)      â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚             â–¼                           â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚  2. Cipher Module Selector      â”‚   â”‚
â”‚  â”‚     â””â”€ Load Ranked Modules      â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚             â–¼                           â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚  3. Decoding Execution          â”‚   â”‚
â”‚  â”‚     â””â”€ Apply Cipher Modules     â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚             â–¼                           â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚  4. Result Validation           â”‚   â”‚
â”‚  â”‚     â”œâ”€ Printability Check       â”‚   â”‚
â”‚  â”‚     â”œâ”€ Dictionary Score         â”‚   â”‚
â”‚  â”‚     â”œâ”€ Entropy Check            â”‚   â”‚
â”‚  â”‚     â””â”€ Confidence Score         â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â”‚             â–¼                           â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”   â”‚
â”‚  â”‚  5. Recursion Decision          â”‚   â”‚
â”‚  â”‚     â””â”€ Loop or Return Result    â”‚   â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
         â”‚
         â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Verbose Logger  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜
         â”‚
         â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Result Renderer â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜
         â”‚
         â–¼
    User Output
```

---

## 4. Component Design

### 4.1 CLI Layer Components

#### 4.1.1 Menu System (`cli/menu.py`)

**Responsibility**: Interactive menu navigation and user input

**Key Features**:
- Arrow key navigation
- Numbered menu selections
- Nested menu support
- Context-aware menus

**Interface**:
```python
class MenuSystem:
    def display_main_menu() -> str
    def display_cipher_menu() -> List[str]
    def display_settings_menu() -> Dict[str, Any]
    def get_user_input(prompt: str) -> str
```

#### 4.1.2 Verbose Renderer (`cli/verbose_renderer.py`)

**Responsibility**: Formatted, colorful logging output

**Key Features**:
- Color-coded log levels
- Real-time progress indicators
- Hierarchical log structure
- Export to file capability

**Interface**:
```python
class VerboseRenderer:
    def log_info(message: str, level: int = 0)
    def log_success(message: str, level: int = 0)
    def log_warning(message: str, level: int = 0)
    def log_error(message: str, level: int = 0)
    def log_debug(message: str, level: int = 0)
    def start_section(title: str)
    def end_section()
```

#### 4.1.3 ANSI Manager (`cli/ansi.py`)

**Responsibility**: Cross-platform ANSI color code handling

**Key Features**:
- Windows compatibility (colorama)
- Color palette management
- Style definitions (bold, underline, etc.)
- Fallback for non-ANSI terminals

### 4.2 Detection Engine Components

#### 4.2.1 Auto-Detector (`detection/auto_detect.py`)

**Responsibility**: Orchestrate all detection methods

**Interface**:
```python
class AutoDetector:
    def detect(text: str) -> List[DetectionResult]
    def get_confidence_scores(text: str) -> Dict[str, float]
    def suggest_decoders(text: str, top_n: int = 5) -> List[CipherModule]
```

**DetectionResult**:
```python
@dataclass
class DetectionResult:
    cipher_name: str
    confidence: float
    reasoning: str
    metadata: Dict[str, Any]
```

#### 4.2.2 Entropy Analyzer (`detection/entropy.py`)

**Responsibility**: Calculate Shannon entropy and randomness metrics

**Methods**:
- `calculate_entropy(text: str) -> float`
- `calculate_block_entropy(text: str, block_size: int) -> List[float]`
- `is_likely_compressed(text: str) -> bool`
- `entropy_score(text: str) -> float`

#### 4.2.3 Frequency Analyzer (`detection/frequency.py`)

**Responsibility**: Character and n-gram frequency analysis

**Methods**:
- `calculate_frequency_distribution(text: str) -> Dict[str, float]`
- `compare_to_english(text: str) -> float`
- `calculate_ioc(text: str) -> float` (Index of Coincidence)
- `suggest_shift_cipher(text: str) -> Optional[int]`

#### 4.2.4 Signature Detector (`detection/signatures.py`)

**Responsibility**: Pattern-based cipher identification

**Methods**:
- `check_base64_signature(text: str) -> float`
- `check_hex_signature(text: str) -> float`
- `check_hash_signature(text: str) -> Optional[str]`
- `check_jwt_signature(text: str) -> bool`
- `check_magic_bytes(data: bytes) -> Optional[str]`

### 4.3 Core Engine Components

#### 4.3.1 Recursive Decoder (`engine/recursive_decoder.py`)

**Responsibility**: Main decoding orchestration with recursion

**Interface**:
```python
class RecursiveDecoder:
    def decode(
        text: str,
        max_depth: int = 5,
        confidence_threshold: float = 0.7,
        verbose: bool = True
    ) -> DecodeResult
    
    def _decode_layer(
        text: str,
        depth: int,
        chain: List[str]
    ) -> List[DecodeCandidate]
    
    def _should_recurse(
        result: DecodeCandidate,
        depth: int
    ) -> bool
```

**DecodeResult**:
```python
@dataclass
class DecodeResult:
    final_text: str
    decode_chain: List[str]
    confidence: float
    metadata: Dict[str, Any]
    alternatives: List[DecodeCandidate]
```

#### 4.3.2 Chain Tracker (`engine/chain_tracker.py`)

**Responsibility**: Track and visualize decode chains

**Methods**:
- `add_step(cipher_name: str, input_text: str, output_text: str)`
- `get_chain() -> List[ChainStep]`
- `visualize_chain() -> str`
- `export_chain(format: str) -> str` (json, xml, text)

#### 4.3.3 Result Scorer (`engine/scorer.py`)

**Responsibility**: Score and rank decode results

**Scoring Components**:
```python
class ResultScorer:
    def score_printability(text: str) -> float
    def score_dictionary_match(text: str) -> float
    def score_entropy(text: str) -> float
    def score_language(text: str, language: str = 'en') -> float
    def composite_score(text: str) -> float
```

**Scoring Weights** (configurable):
- Printability: 25%
- Dictionary match: 35%
- Entropy (low is good): 20%
- Language model: 20%

### 4.4 Cipher Module Architecture

#### 4.4.1 Base Cipher Interface

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class DecodeCandidate:
    decoded_text: str
    confidence: float
    method_details: str
    metadata: Dict[str, Any]

class CipherModule(ABC):
    """Base interface for all cipher modules"""
    
    name: str = ""
    aliases: List[str] = []
    category: str = ""  # 'encoding', 'classical', 'modern', etc.
    
    @abstractmethod
    def detect(self, text: str) -> float:
        """
        Analyze text and return confidence score (0.0 to 1.0)
        that this cipher was used.
        """
        pass
    
    @abstractmethod
    def decode(self, text: str) -> List[DecodeCandidate]:
        """
        Attempt to decode text and return all plausible results.
        Results should be sorted by confidence (highest first).
        """
        pass
    
    def encode(self, text: str, **kwargs) -> str:
        """
        Optional: Encode text with this cipher.
        Useful for testing and educational purposes.
        """
        raise NotImplementedError("Encoding not supported for this cipher")
    
    def get_info(self) -> str:
        """
        Return educational information about this cipher.
        """
        return f"No information available for {self.name}"
```

#### 4.4.2 Example Cipher Module: Base64

```python
class Base64Cipher(CipherModule):
    name = "Base64"
    aliases = ["base64", "b64"]
    category = "encoding"
    
    def detect(self, text: str) -> float:
        # Check signature patterns
        if not text:
            return 0.0
        
        # Valid charset check
        valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")
        if not all(c in valid_chars for c in text):
            return 0.0
        
        # Length divisible by 4
        if len(text) % 4 != 0:
            return 0.3  # Possible but missing padding
        
        # Padding check
        padding_count = text.count('=')
        if padding_count > 2:
            return 0.0
        
        # High confidence if all checks pass
        return 0.9
    
    def decode(self, text: str) -> List[DecodeCandidate]:
        import base64
        
        candidates = []
        
        # Try standard Base64
        try:
            decoded = base64.b64decode(text, validate=True)
            candidates.append(DecodeCandidate(
                decoded_text=decoded.decode('utf-8', errors='replace'),
                confidence=0.95,
                method_details="Standard Base64 decoding",
                metadata={'variant': 'standard'}
            ))
        except Exception as e:
            pass
        
        # Try URL-safe Base64
        try:
            decoded = base64.urlsafe_b64decode(text)
            candidates.append(DecodeCandidate(
                decoded_text=decoded.decode('utf-8', errors='replace'),
                confidence=0.85,
                method_details="URL-safe Base64 decoding",
                metadata={'variant': 'urlsafe'}
            ))
        except Exception:
            pass
        
        return sorted(candidates, key=lambda x: x.confidence, reverse=True)
    
    def encode(self, text: str, url_safe: bool = False) -> str:
        import base64
        
        if url_safe:
            return base64.urlsafe_b64encode(text.encode()).decode()
        return base64.b64encode(text.encode()).decode()
    
    def get_info(self) -> str:
        return """
        Base64 Encoding
        ---------------
        Base64 is a binary-to-text encoding scheme that represents binary
        data in an ASCII string format. It uses 64 printable characters
        (A-Z, a-z, 0-9, +, /) to represent 6 bits of data.
        
        Common uses: Email attachments, data URLs, JWT tokens
        Padding: Uses '=' for padding to multiples of 4 characters
        """
```

### 4.5 Plugin System Design

#### 4.5.1 Plugin Loader (`engine/plugin_loader.py`)

```python
class PluginLoader:
    def __init__(self, plugin_dirs: List[str]):
        self.plugin_dirs = plugin_dirs
        self.loaded_modules: Dict[str, CipherModule] = {}
    
    def load_all_plugins(self) -> int:
        """Load all plugins from configured directories"""
        pass
    
    def load_plugin(self, filepath: str) -> Optional[CipherModule]:
        """Load a single plugin file"""
        pass
    
    def get_module(self, name: str) -> Optional[CipherModule]:
        """Retrieve loaded module by name"""
        pass
    
    def list_modules(self) -> List[str]:
        """List all loaded module names"""
        pass
```

#### 4.5.2 Plugin Validation

All user plugins validated for:
- Correct interface implementation
- No arbitrary code execution
- Resource limits (timeout, memory)
- Exception handling

---

## 5. Data Flow

### 5.1 Standard Decode Flow

```
1. User Input
   â””â”€â–¶ "VjJWc2JHOGdWMjl5YkdRPQ=="

2. Command Parser
   â””â”€â–¶ ParsedCommand(action='decode', text='VjJWc2...', verbose=True)

3. Auto-Detection Engine
   â”œâ”€â–¶ SignatureDetector: Base64 (0.92)
   â”œâ”€â–¶ EntropyAnalyzer: Low entropy (good for text)
   â”œâ”€â–¶ FrequencyAnalyzer: Not plaintext
   â””â”€â–¶ MLClassifier: Base64 (0.88)
   
   Result: [Base64: 0.90, Hex: 0.12, ROT: 0.05]

4. Recursive Decoder (Layer 1)
   â”œâ”€â–¶ Load Base64 module
   â”œâ”€â–¶ Execute decode()
   â””â”€â–¶ Output: "V2VsbG8gV29ybGQ="
   
   â””â”€â–¶ Validator: Not plaintext, recurse

5. Auto-Detection Engine (Layer 2)
   â””â”€â–¶ Result: [Base64: 0.91, ...]

6. Recursive Decoder (Layer 2)
   â””â”€â–¶ Output: "Hello World"
   
   â””â”€â–¶ Validator: Plaintext detected (score: 0.95)

7. Chain Tracker
   â””â”€â–¶ Chain: Base64 â†’ Base64 â†’ Plaintext

8. Result Renderer
   â””â”€â–¶ Display: "Hello World" with decode chain

9. Verbose Logger (if enabled)
   â””â”€â–¶ Full step-by-step explanation
```

### 5.2 Multi-Branch Decode Flow

```
Input: Ambiguous encoded string

Auto-Detection:
â”œâ”€â–¶ Base64: 0.75
â”œâ”€â–¶ Hex: 0.73
â””â”€â–¶ ROT13: 0.45

Parallel Decode Attempts:
â”œâ”€â–¶ Branch 1: Base64
â”‚   â””â”€â–¶ Result: "xj8Kma..."
â”‚       â””â”€â–¶ Score: 0.3 (poor)
â”‚
â”œâ”€â–¶ Branch 2: Hex
â”‚   â””â”€â–¶ Result: "The flag is..."
â”‚       â””â”€â–¶ Score: 0.92 (excellent)
â”‚
â””â”€â–¶ Branch 3: ROT13
    â””â”€â–¶ Result: "guv synt..."
        â””â”€â–¶ Score: 0.25 (poor)

Result Ranker:
â””â”€â–¶ Best: Hex decode (0.92)
    â””â”€â–¶ Alternatives: Base64 (0.3), ROT13 (0.25)

Output: "The flag is..." with confidence 0.92
```

---

## 6. Technology Stack

### 6.1 Core Technologies

**Programming Language**: Python 3.8+
- Rationale: Rich ecosystem, cross-platform, rapid development
- Version: 3.8 minimum for compatibility

**CLI Framework**: 
- **rich** (primary): Beautiful terminal output, tables, progress bars
- **click**: Command-line argument parsing
- **prompt_toolkit**: Interactive input with auto-completion

**Testing**:
- **pytest**: Unit and integration testing
- **pytest-cov**: Code coverage reporting
- **hypothesis**: Property-based testing for edge cases

### 6.2 Key Libraries

#### Cryptography & Encoding
```python
cryptography==41.0.0      # Modern crypto primitives
pycryptodome==3.19.0      # Classical cipher implementations
base58==2.1.1             # Base58 encoding
```

#### Text Analysis
```python
nltk==3.8.1               # Natural language processing
langdetect==1.0.9         # Language detection
```

#### Machine Learning (Optional)
```python
scikit-learn==1.3.0       # ML classifier
numpy==1.24.0             # Numerical operations
```

#### CLI Enhancement
```python
rich==13.7.0              # Beautiful terminal output
click==8.1.7              # CLI framework
prompt_toolkit==3.0.43    # Interactive prompts
colorama==0.4.6           # Windows color support
```

#### Utilities
```python
python-dotenv==1.0.0      # Configuration management
pyyaml==6.0.1             # YAML parsing
```

### 6.3 Development Tools

```python
# Code Quality
black==23.12.0            # Code formatting
flake8==7.0.0             # Linting
mypy==1.8.0               # Type checking
isort==5.13.0             # Import sorting

# Testing
pytest==7.4.0
pytest-cov==4.1.0
pytest-mock==3.12.0

# Documentation
sphinx==7.2.0             # API documentation
mkdocs==1.5.3             # User documentation

# Build & Distribution
setuptools==69.0.0
wheel==0.42.0
twine==4.0.2              # PyPI uploads
```

---

## 7. Security Architecture

### 7.1 Security Principles

1. **Input Validation**: All user input sanitized
2. **Sandboxed Execution**: Plugins run in restricted environment
3. **No Arbitrary Code Execution**: Limited eval/exec usage
4. **Resource Limits**: Timeouts and memory limits on operations
5. **Secure Dependencies**: Regular vulnerability scanning

### 7.2 Plugin Sandboxing

```python
class PluginSandbox:
    """Restrict plugin capabilities"""
    
    TIMEOUT_SECONDS = 5
    MAX_MEMORY_MB = 100
    
    ALLOWED_IMPORTS = [
        'base64', 'hashlib', 'binascii', 'string',
        'math', 're', 'itertools', 'collections'
    ]
    
    FORBIDDEN_OPERATIONS = [
        'eval', 'exec', 'compile', '__import__',
        'open', 'file', 'input', 'raw_input'
    ]
```

### 7.3 Threat Model

**Threats**:
1. Malicious plugin code execution
2. Resource exhaustion attacks
3. Information leakage through verbose output
4. Dependency vulnerabilities

**Mitigations**:
1. Plugin code review + sandboxing
2. Resource limits + timeouts
3. Configurable verbose output levels
4. Automated dependency scanning (Dependabot)

---

## 8. Performance Considerations

### 8.1 Performance Requirements

- Startup time: < 1 second
- Single-layer decode: < 500ms average
- Multi-layer decode: < 3 seconds for 5 layers
- Memory footprint: < 100MB typical usage
- Concurrent operations: Support 10+ parallel decodes

### 8.2 Optimization Strategies

**Lazy Loading**:
- Load cipher modules on-demand
- Load ML models only when needed
- Defer heavy library imports

**Caching**:
```python
class ResultCache:
    """LRU cache for decode results"""
    
    MAX_CACHE_SIZE = 1000
    
    def get(self, text: str, cipher: str) -> Optional[DecodeResult]
    def set(self, text: str, cipher: str, result: DecodeResult)
    def clear()
```

**Parallel Processing**:
- Multiple cipher detection in parallel
- Concurrent decode attempts for ambiguous inputs
- Thread pool for batch processing

**Profiling Points**:
- Entry/exit of major functions
- Cipher module execution time
- Detection engine performance
- I/O operations

---

## 9. Deployment Architecture

### 9.1 Distribution Formats

**PyPI Package** (primary):
```bash
pip install chopshop-cli
```

**Standalone Binary** (optional):
- PyInstaller for Windows/Linux/macOS
- Single executable with embedded Python

**Docker Container**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -e .
ENTRYPOINT ["chopshop"]
```

### 9.2 Installation Paths

```
Linux/macOS:
~/.chopshop/
â”œâ”€â”€ config.yaml
â”œâ”€â”€ plugins/
â”‚   â””â”€â”€ user_defined/
â”œâ”€â”€ wordlists/
â”œâ”€â”€ models/
â””â”€â”€ cache/

Windows:
%USERPROFILE%\.chopshop\
â”œâ”€â”€ config.yaml
â”œâ”€â”€ plugins\
â”‚   â””â”€â”€ user_defined\
â”œâ”€â”€ wordlists\
â”œâ”€â”€ models\
â””â”€â”€ cache\
```

---

## 10. Future Architecture Evolution

### 10.1 Phase 2+ Architectural Changes

**API Layer Addition**:
```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚   REST API      â”‚
â”‚   (FastAPI)     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”˜
         â”‚
         â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Core Engine    â”‚
â”‚  (Existing)     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

**Distributed Processing**:
- Job queue for batch operations
- Distributed cache (Redis)
- Horizontal scaling capability

### 10.2 ML Architecture Evolution

**Phase 1**: Simple classifier (sklearn)
**Phase 3**: Enhanced neural network classifier
- Training pipeline
- Model versioning
- A/B testing framework

### 10.3 Extensibility Points

- **Custom Scorers**: Plugin architecture for scoring modules
- **External Tool Integration**: Hooks for hashcat, john, etc.
- **LLM Integration**: Optional LLM agent for analysis
- **MCP Server**: Model Context Protocol support

---

## Appendix A: Directory Structure

```
chopshop-cli/
â”œâ”€â”€ chopshop/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ __main__.py
â”‚   â”œâ”€â”€ cli/
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ banner.py
â”‚   â”‚   â”œâ”€â”€ menu.py
â”‚   â”‚   â”œâ”€â”€ verbose_renderer.py
â”‚   â”‚   â””â”€â”€ ansi.py
â”‚   â”œâ”€â”€ detection/
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ auto_detect.py
â”‚   â”‚   â”œâ”€â”€ entropy.py
â”‚   â”‚   â”œâ”€â”€ frequency.py
â”‚   â”‚   â”œâ”€â”€ dictionary.py
â”‚   â”‚   â””â”€â”€ signatures.py
â”‚   â”œâ”€â”€ engine/
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ recursive_decoder.py
â”‚   â”‚   â”œâ”€â”€ chain_tracker.py
â”‚   â”‚   â”œâ”€â”€ scorer.py
â”‚   â”‚   â”œâ”€â”€ validator.py
â”‚   â”‚   â””â”€â”€ plugin_loader.py
â”‚   â”œâ”€â”€ ciphers/
â”‚   â”‚   â”œâ”€â”€ __init__.py
â”‚   â”‚   â”œâ”€â”€ base.py
â”‚   â”‚   â”œâ”€â”€ base64_cipher.py
â”‚   â”‚   â”œâ”€â”€ hex_cipher.py
â”‚   â”‚   â”œâ”€â”€ rot_cipher.py
â”‚   â”‚   â””â”€â”€ user_defined/
â”‚   â””â”€â”€ resources/
â”‚       â”œâ”€â”€ wordlists/
â”‚       â””â”€â”€ models/
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ unit/
â”‚   â”œâ”€â”€ integration/
â”‚   â””â”€â”€ fixtures/
â”œâ”€â”€ docs/
â”œâ”€â”€ examples/
â”œâ”€â”€ setup.py
â”œâ”€â”€ pyproject.toml
â”œâ”€â”€ README.md
â””â”€â”€ LICENSE
```

---

**Document End**


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/chopshop-project-documentation|chopshop-project-documentation]]

**Consolidated into:**
- [[docs/DC-CHOPSHOP-PROJECT-DOCUMENTATION-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->

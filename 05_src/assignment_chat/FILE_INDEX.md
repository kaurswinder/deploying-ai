# Assignment 2 - Aria Chat System - File Index

## 📚 Documentation Files (Start Here!)

### For Quick Start
- **`QUICKSTART.md`** - 5-minute setup guide
- **`DELIVERY_SUMMARY.md`** - Complete project overview
- **`readme.md`** - Full technical documentation

### For Understanding Implementation
- **`IMPLEMENTATION.md`** - Design decisions and rationale
- **`examples.py`** - Code examples showing system usage

---

## 🔧 Core Application Code

### Entry Point
- **`app.py`** - Main script to start the Gradio interface
  - Run with: `python 05_src/assignment_chat/app.py`
  - Launches at: `http://localhost:7860`

### Main Components
- **`engine.py`** - ChatEngine class that orchestrates everything
  - Integrates all services
  - Manages memory
  - Applies guardrails
  - Calls OpenAI API

- **`interface.py`** - Gradio chat interface
  - Beautiful UI with personality
  - Chat history display
  - Memory status panel
  - Clear history button

- **`services.py`** - Three services
  - `APIService`: Weather information
  - `SemanticSearchService`: ChromaDB knowledge base
  - `FunctionCallingService`: Calculator, definitions, time

- **`guardrails.py`** - Safety and protection
  - Restricted topic detection
  - System prompt protection
  - Content filtering

- **`memory.py`** - Conversation memory management
  - Message history tracking
  - Sliding window trimming
  - Token estimation
  - Memory status display

### Package Setup
- **`__init__.py`** - Package initialization with exports

---

## 🧪 Testing & Examples

### Testing
- **`test_demo.py`** - Automated test suite
  - Tests guardrails
  - Tests all services
  - Tests chat engine
  - Tests memory management
  - Run with: `python test_demo.py`

### Examples
- **`examples.py`** - Usage examples showing system capabilities
  - Example 1: Guardrails demonstration
  - Example 2: Individual services
  - Example 3: Memory management
  - Example 4: Full chat engine (requires API key)
  - Example 5: Extended conversation (memory trimming demo)
  - Run with: `python examples.py`

---

## 📦 Configuration & Data

### Configuration
- **`requirements.txt`** - List of required packages
- **`.gitignore`** - Git ignore patterns

### Data Directories
- **`data/`** - Data directory (for future use)
- **`chroma_db/`** - ChromaDB persistent storage (auto-created)
  - Contains embeddings and documents
  - Pre-populated with sample data on first run

---

## 🎯 Quick Navigation Guide

### "How do I run this?"
→ Start with **QUICKSTART.md**

### "What was implemented?"
→ Read **DELIVERY_SUMMARY.md**

### "How does the system work?"
→ See **readme.md**

### "Why were these design choices made?"
→ Review **IMPLEMENTATION.md**

### "How do I use the code programmatically?"
→ Check **examples.py**

### "How do I test it?"
→ Run **test_demo.py**

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Total Python files | 10 |
| Total lines of code | ~1,270 |
| Documentation files | 5 |
| Services implemented | 3 |
| Guardrail types | 2 |
| Test cases covered | 8+ |
| Project size | <1MB |

---

## ✅ What Each File Does

### Core Logic Files

**engine.py** (360 lines)
- Main chat orchestrator
- Routes messages to services
- Manages conversation flow
- Calls OpenAI API
- Applies guardrails

**services.py** (320 lines)
- Weather API service
- Semantic search (ChromaDB)
- Function calling tools
- Real-time data retrieval

**interface.py** (210 lines)
- Gradio UI creation
- Chat history management
- Memory display
- Event handling

**guardrails.py** (110 lines)
- Restricted topic detection
- System prompt protection
- Content filtering
- Response generation

**memory.py** (130 lines)
- Conversation history
- Sliding window trimming
- Token estimation
- Status tracking

### Supporting Files

**app.py** (15 lines)
- Entry point for launching the app

**__init__.py** (10 lines)
- Package exports and initialization

**test_demo.py** (140 lines)
- Comprehensive test suite
- Tests all components
- Demonstrates system capabilities

**examples.py** (180 lines)
- Usage examples
- Code patterns
- Integration examples

---

## 🚀 Execution Flow

```
User runs app.py
    ↓
Interface launches (Gradio UI)
    ↓
User types message
    ↓
Engine receives message
    ↓
Guardrails check (blocked or proceed)
    ↓
IF PROCEED:
  → Determine services to use
  → Call services (API, Search, Functions)
  → Build context
  → Call OpenAI API
  → Add to memory
  → Return response
    ↓
Response displayed in UI
    ↓
Memory updated with metadata
```

---

## 🔗 File Dependencies

```
app.py
  └→ interface.py
       └→ engine.py
            ├→ services.py
            ├→ guardrails.py
            ├→ memory.py
            └→ OpenAI API

test_demo.py
  ├→ engine.py
  ├→ services.py
  ├→ guardrails.py
  └→ memory.py

examples.py
  ├→ engine.py
  ├→ services.py
  ├→ guardrails.py
  └→ memory.py
```

---

## 📝 To Get Started

1. **Read**: `QUICKSTART.md` (2 minutes)
2. **Run**: `python app.py` (1 minute)
3. **Chat**: Try the examples from `QUICKSTART.md` (5 minutes)
4. **Explore**: Check `test_demo.py` or `examples.py` (optional)
5. **Learn**: Read `readme.md` for technical details (optional)

---

## 🎯 Each File's Purpose at a Glance

| File | Purpose | Lines |
|------|---------|-------|
| app.py | Start Gradio | 15 |
| interface.py | Chat UI | 210 |
| engine.py | Main logic | 360 |
| services.py | 3 Services | 320 |
| memory.py | History mgmt | 130 |
| guardrails.py | Safety | 110 |
| __init__.py | Package | 10 |
| test_demo.py | Testing | 140 |
| examples.py | Examples | 180 |

---

## 💾 File Organization

```
assignment_chat/
├─ Application Code (5 files, 1,140 lines)
│  ├─ app.py
│  ├─ engine.py
│  ├─ interface.py
│  ├─ services.py
│  ├─ guardrails.py
│  ├─ memory.py
│  └─ __init__.py
│
├─ Testing & Examples (2 files, 320 lines)
│  ├─ test_demo.py
│  └─ examples.py
│
├─ Documentation (5 files)
│  ├─ readme.md
│  ├─ QUICKSTART.md
│  ├─ IMPLEMENTATION.md
│  ├─ DELIVERY_SUMMARY.md
│  └─ FILE_INDEX.md (this file)
│
├─ Configuration (2 files)
│  ├─ requirements.txt
│  └─ .gitignore
│
└─ Data (2 directories)
   ├─ data/
   └─ chroma_db/
```

---

**All files are ready to use. Start with QUICKSTART.md!** 🚀

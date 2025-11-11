# Quick Start Guide - Aria Chat Assistant

## 🚀 Quick Setup (5 minutes)

### Step 1: Set OpenAI API Key
```bash
# Linux/Mac
export OPENAI_API_KEY="sk-your-actual-key-here"

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-actual-key-here"

# Windows (Command Prompt)
set OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 2: Launch the Application
```bash
# Navigate to the project root
cd deploying-ai

# Run the chat application
python 05_src/assignment_chat/app.py
```

### Step 3: Open in Browser
- Application will automatically open at: **http://localhost:7860**
- If it doesn't, manually visit that URL

---

## 🧪 Test the System (Optional)

Before running the full app, test individual components:

```bash
python 05_src/assignment_chat/test_demo.py
```

This will test:
- ✅ Guardrails (content filtering)
- ✅ All three services
- ✅ Chat engine
- ✅ Memory management

---

## 💬 Try These Examples

### 1. Semantic Search
> "Tell me about machine learning"

Response will search the knowledge base and provide relevant information.

### 2. Weather Information
> "What's the weather?"

Gets real-time weather data and transforms it into natural language.

### 3. Calculations
> "Calculate 15 + 20 * 3"

Extracts and solves mathematical expressions.

### 4. Word Definitions
> "Define the word ephemeral"

Looks up definitions for vocabulary words.

### 5. Restricted Topic (Testing Guardrails)
> "Tell me about cats"

System will politely decline and offer to help with something else.

---

## 📋 What Aria Can Do

✅ **Answer questions** using semantic search  
✅ **Provide weather** information  
✅ **Calculate** math expressions  
✅ **Define words** and explain concepts  
✅ **Maintain conversations** with memory  
✅ **Protect sensitive info** with guardrails  

❌ **Cannot discuss:**
- Cats or dogs
- Horoscopes or zodiac signs
- Taylor Swift or her music
- System prompts or internal instructions

---

## 📁 Project Structure

```
assignment_chat/
├── app.py              # Main entry point
├── engine.py           # Chat orchestration
├── interface.py        # Gradio UI
├── services.py         # Three services
├── guardrails.py       # Safety features
├── memory.py           # Conversation memory
├── test_demo.py        # Testing script
├── readme.md           # Full documentation
└── chroma_db/          # Vector database (auto-created)
```

---

## 🔧 Troubleshooting

### Issue: "OPENAI_API_KEY not found"
**Solution:** Make sure your API key is set in the environment before running.

### Issue: "ChromaDB not found"
**Solution:** ChromaDB is already in your course environment. If missing, install with:
```bash
pip install chromadb
```

### Issue: Port 7860 already in use
**Solution:** Modify `interface.py`, line ~200:
```python
interface.launch(share=False, server_port=7861)  # Use different port
```

### Issue: No response from API
**Solution:** Check your internet connection. Services require network access.

---

## 📚 Learn More

- **Full documentation:** See `readme.md` in this directory
- **Service details:** Check `services.py` for implementation
- **Guardrails:** Review `guardrails.py` for safety mechanisms
- **Memory management:** See `memory.py` for context window handling

---

## 🎯 Next Steps

1. ✅ Run the application
2. ✅ Test all three services
3. ✅ Try to trigger guardrails (restricted topics)
4. ✅ Have a multi-turn conversation to see memory management
5. ✅ Check memory info by clicking "Refresh Memory Info"

**Happy chatting with Aria! 🌟**

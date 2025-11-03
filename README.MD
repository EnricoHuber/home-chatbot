# 🏠 Home Assistant Chatbot

**Version 2.0** - Professional, production-ready home assistant chatbot with RAG capabilities.

An intelligent home assistant chatbot that helps with household management, natural cleaning methods, utilities information, and more. Built with Python, Telegram Bot API, and RAG (Retrieval-Augmented Generation).

---

## ✨ Key Features

- 🤖 **Telegram Bot Interface** - Interact via Telegram
- 🧠 **RAG System** - Retrieval-Augmented Generation for accurate responses
- 📚 **Persistent Knowledge Storage** - Supabase (500MB free) or local ChromaDB
- 💬 **Text Knowledge Addition** - Add knowledge via `/addknowledge` command
- 📄 **PDF Support** - Upload documents to expand knowledge base
- 🎨 **Web Admin Interface** - Streamlit-based management panel
- ⚙️ **Highly Configurable** - JSON-based configuration system
- 🚀 **Multiple Deployment Options** - Free hosting on Railway, Fly.io, Oracle Cloud

---

## � Documentation

**Complete documentation is available in the [`docs/`](docs/) folder:**

- **[� Full Documentation](docs/README_NEW.md)** - Complete guide
- **[🚀 Deployment Guide](docs/DEPLOYMENT.md)** - FREE hosting options
- **[⚡ Quick Reference](docs/QUICK_REF.md)** - Commands and setup
- **[📚 Knowledge Guide](docs/KNOWLEDGE_GUIDE.md)** - Adding knowledge via text/PDF
- **[🏗️ Architecture](docs/STRUCTURE.md)** - Project structure
- **[📋 Summary](docs/SUMMARY.md)** - What's new in v2.0

**New to the project?** Start with the [Documentation Index](docs/README.md)

---

## 🧪 Test Locally First! (Recommended)

**Before deploying, test the bot locally:**

### Option 1: Run Directly with Python

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file with your credentials
Copy-Item .env.example .env
notepad .env  # Add your GROQ_API_KEY and TELEGRAM_BOT_TOKEN

# 3. Run the bot
python src/main.py
```

**Or use the automated script:** `.\test-local.ps1`

---

### Option 2: Test in Docker (Recommended) 🐳

**Test in the exact same environment as production:**

```powershell
# Quick Docker test
.\test-docker.ps1
```

**Test with Supabase (persistent storage):**

```powershell
# Setup Supabase first (see SUPABASE_SETUP.md)
# Then test with Docker
.\test-supabase.ps1
```

**Or manually:**

```powershell
# Build and run with Docker Compose
docker-compose up --build
```

**Why Docker?**
- ✅ Same environment as Railway/Render/Fly.io
- ✅ Isolates dependencies
- ✅ Easy to reset and test again
- ✅ No Python installation conflicts
- ✅ Test Supabase integration locally

**See guides:** [LOCAL_TESTING.md](LOCAL_TESTING.md) | [DOCKER_LOCAL.md](DOCKER_LOCAL.md)

---

## 🚀 Quick Start

### 1. Setup
```bash
# Clone repository
git clone https://github.com/EnricoHuber/home-chatbot.git
cd home-chatbot

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 2. Get API Keys
- **Groq API**: https://console.groq.com/keys
- **Telegram Bot**: https://t.me/BotFather

### 3. Run
```bash
python src/main.py
```

### 4. Use the Bot
- Open Telegram and find your bot
- Send `/start` to begin
- Try: "Come pulire il forno naturalmente?"
- Add knowledge: `/addknowledge utenze Contratto luce scade 31/12/2025`

---

## 📦 Project Structure

```
src/
├── core/              # Business logic (chatbot, LLM, RAG)
├── handlers/          # Interface handlers (Telegram)
├── interfaces/        # User interfaces (Web admin)
├── utils/             # Utilities (config, logging, helpers)
└── main.py           # Entry point

configs/               # Configuration files
docs/                  # Documentation
logs/                  # Application logs
```

---

## 🎮 Bot Commands

- `/start` - Initialize the bot
- `/help` - Show available commands
- `/addknowledge` - Add text knowledge
- `/stats` - View statistics
- `/info` - Bot information

**Send a PDF** - Automatically adds to knowledge base

---

## 🚀 Deploy for FREE

Multiple free hosting options available:

| Platform | RAM | Cost | Always-On |
|----------|-----|------|-----------|
| **Railway** ⭐ | 512MB | $5/mo trial | ✅ |
| **Fly.io** | 256MB | FREE | ✅ |
| **Oracle Cloud** | 24GB | FREE | ✅ |

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

---

## 🤝 Contributing

Contributions welcome! See [docs/README_NEW.md](docs/README_NEW.md) for development setup.

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Groq for LLM API
- ChromaDB for vector database
- Sentence Transformers for embeddings

---

**For detailed documentation, visit the [`docs/`](docs/) folder! 📚**

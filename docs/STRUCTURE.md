# 📁 Project Structure Overview

```
home-chatbot/
│
├── 📂 src/                          # Source code
│   ├── 📂 core/                     # Core business logic
│   │   ├── chatbot.py              # Main chatbot (LLM + RAG)
│   │   └── __init__.py
│   │
│   ├── 📂 handlers/                 # Interface handlers
│   │   ├── telegram_handler.py     # Telegram bot logic
│   │   └── __init__.py
│   │
│   ├── 📂 interfaces/               # User interfaces
│   │   ├── web_interface.py        # Streamlit admin panel
│   │   └── __init__.py
│   │
│   ├── 📂 utils/                    # Utilities
│   │   ├── config_manager.py       # Configuration system
│   │   ├── logger.py               # Logging system
│   │   ├── helpers.py              # Helper functions
│   │   └── __init__.py
│   │
│   └── main.py                      # Application entry point
│
├── 📂 configs/                      # Configuration files
│   ├── base_config.json            # Development config
│   ├── test_small_model.json       # Testing config
│   └── production_config.json      # Production config
│
├── 📂 logs/                         # Application logs
│   └── chatbot.log
│
├── 📂 chroma_db/                    # Vector database (created at runtime)
│
├── 📄 .env.example                  # Environment variables template
├── 📄 .env                          # Your environment variables (create this)
├── 📄 requirements.txt              # Python dependencies
├── 📄 Dockerfile                    # Docker configuration
├── 📄 Procfile                      # For Railway/Heroku
├── 📄 railway.toml                  # Railway configuration
├── 📄 fly.toml                      # Fly.io configuration
├── 📄 render.yaml                   # Render.com configuration
├── 📄 runtime.txt                   # Python version
├── 📄 setup.ps1                     # Windows setup script
│
├── 📖 README_NEW.md                 # Main documentation
├── 📖 DEPLOYMENT.md                 # Deployment guide
├── 📖 MIGRATION.md                  # Migration guide
├── 📖 SUMMARY.md                    # Quick summary
└── 📖 STRUCTURE.md                  # This file
```

## 🏗️ Architecture Flow

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                    (Telegram Client)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   TELEGRAM API                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               handlers/telegram_handler.py                   │
│  • Receives messages                                         │
│  • Rate limiting                                             │
│  • User authentication                                       │
│  • Command routing                                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   core/chatbot.py                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              LLMProvider                            │   │
│  │  • Groq API integration                             │   │
│  │  • Model selection                                  │   │
│  │  • Response generation                              │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │                                    │
│  ┌─────────────────────▼──────────────────────────────┐   │
│  │              RAGSystem                              │   │
│  │  • Vector database (ChromaDB)                       │   │
│  │  • Semantic search                                  │   │
│  │  • Knowledge retrieval                              │   │
│  │  • Embeddings (SentenceTransformer)                 │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  RESPONSE TO USER                            │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### 1. Message Reception
```
User → Telegram → telegram_handler.py
```

### 2. Processing
```
telegram_handler → chatbot.py → RAGSystem (search knowledge)
                               ↓
                          LLMProvider (generate response)
```

### 3. Response
```
LLMProvider → chatbot.py → telegram_handler → User
```

## 📦 Module Dependencies

```
main.py
  ├── utils/config_manager.py
  │     └── Loads JSON configs
  │
  ├── utils/logger.py
  │     └── Sets up logging
  │
  ├── core/chatbot.py
  │     ├── LLMProvider (Groq API)
  │     └── RAGSystem (ChromaDB + Embeddings)
  │
  └── handlers/telegram_handler.py
        └── Uses chatbot.py for responses
```

## 🎯 Key Components

### 1. **ConfigManager** (`utils/config_manager.py`)
- Loads configuration from JSON
- Validates settings
- Environment-specific configs
- Generates .env template

### 2. **Logger** (`utils/logger.py`)
- Colored console output
- File rotation
- Performance tracking
- LoggerMixin for easy integration

### 3. **HomeChatbot** (`core/chatbot.py`)
- Main chatbot logic
- Integrates LLM and RAG
- Response caching
- Error handling

### 4. **LLMProvider** (`core/chatbot.py`)
- Groq API integration
- Async requests
- Retry logic
- Token management

### 5. **RAGSystem** (`core/chatbot.py`)
- Vector database management
- Semantic search
- Knowledge base
- Embedding generation

### 6. **TelegramBotHandler** (`handlers/telegram_handler.py`)
- Command handling
- Message routing
- Rate limiting
- User management
- File uploads

### 7. **Helpers** (`utils/helpers.py`)
- Rate limiter
- Cache system
- File utilities
- Validation functions

## 🔐 Security Layers

```
User Request
    │
    ├─→ Rate Limiter (prevent spam)
    │
    ├─→ User Whitelist (if configured)
    │
    ├─→ Input Validation
    │
    └─→ Process Request
```

## 💾 Data Storage

```
┌─────────────────────────────────────────┐
│         ChromaDB (Vector DB)            │
│  • Stores embeddings                    │
│  • Fast similarity search               │
│  • Persistent storage                   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         Logs (File System)              │
│  • Application logs                     │
│  • Error tracking                       │
│  • Performance metrics                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│       Cache (In-Memory)                 │
│  • Response cache (10 min)              │
│  • RAG search cache (5 min)             │
│  • Reduces API calls                    │
└─────────────────────────────────────────┘
```

## 🌐 Deployment Architecture

```
┌──────────────────────────────────────────────────┐
│           Hosting Platform                       │
│        (Railway/Fly.io/Oracle)                   │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │         Docker Container                │    │
│  │                                          │    │
│  │  ┌────────────────────────────────┐   │    │
│  │  │       Python App                │   │    │
│  │  │  • main.py                      │   │    │
│  │  │  • Flask (health checks)        │   │    │
│  │  │  • Telegram bot                 │   │    │
│  │  └────────────────────────────────┘   │    │
│  │                                          │    │
│  │  ┌────────────────────────────────┐   │    │
│  │  │    Persistent Storage           │   │    │
│  │  │  • ChromaDB                     │   │    │
│  │  │  • Logs                         │   │    │
│  │  └────────────────────────────────┘   │    │
│  └────────────────────────────────────────┘    │
└──────────────────────────────────────────────────┘
         │                           │
         ▼                           ▼
   Health Checks              External APIs
   (HTTP /health)          (Groq, Telegram)
```

## 🧪 Testing Strategy

```
Local Development
    ├── Use test_small_model.json
    ├── Enable verbose logging
    └── Test with small models

Staging
    ├── Use base_config.json
    ├── Test with production-like setup
    └── Validate deployment configs

Production
    ├── Use production_config.json
    ├── Optimized models
    └── Minimal logging
```

## 📊 Monitoring

```
Health Check Endpoint
    └─→ /health (returns status)

Logs
    ├─→ Console (colored output)
    └─→ File (logs/chatbot.log)

Metrics (Built-in)
    ├─→ Response cache hits
    ├─→ RAG search performance
    └─→ API call timing
```

## 🔄 Future Extensibility

The modular architecture makes it easy to add:

- **New Handlers**: Add to `handlers/`
  - Discord bot
  - WhatsApp integration
  - Slack bot

- **New Interfaces**: Add to `interfaces/`
  - Mobile app
  - Desktop app
  - Voice interface

- **New LLM Providers**: Modify `core/chatbot.py`
  - OpenAI
  - Anthropic
  - Local models

- **New Data Sources**: Extend `core/chatbot.py`
  - Web scraping
  - API integrations
  - Database connections

---

This structure is designed for:
- ✅ Easy maintenance
- ✅ Testing
- ✅ Scalability
- ✅ Team collaboration
- ✅ Production deployment

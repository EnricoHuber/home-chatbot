# 🏠 Home Assistant Chatbot

An intelligent home assistant chatbot with RAG (Retrieval-Augmented Generation) capabilities, designed to help with household management, natural cleaning methods, utilities information, and more.

## ✨ Features

- 🤖 **Telegram Bot Interface** - Interact via Telegram
- 🧠 **RAG System** - Retrieval-Augmented Generation for accurate responses
- 📚 **Knowledge Base** - Store and retrieve custom information
- 🔍 **Semantic Search** - Find relevant information using embeddings
- 📄 **PDF Support** - Upload documents to expand knowledge base
- 🎨 **Web Admin Interface** - Streamlit-based management panel
- ⚙️ **Highly Configurable** - JSON-based configuration system
- 📊 **Comprehensive Logging** - Track bot activity and performance
- 🚀 **Easy Deployment** - Multiple free hosting options

## 🏗️ Architecture

```
src/
├── core/
│   ├── chatbot.py          # Main chatbot logic
│   └── __init__.py
├── handlers/
│   ├── telegram_handler.py # Telegram bot handlers
│   └── __init__.py
├── interfaces/
│   ├── web_interface.py    # Streamlit admin interface
│   └── __init__.py
├── utils/
│   ├── config_manager.py   # Configuration management
│   ├── logger.py           # Logging system
│   ├── helpers.py          # Utility functions
│   └── __init__.py
└── main.py                 # Application entry point
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Groq API Key ([Get it here](https://console.groq.com/keys))
- Telegram Bot Token ([Get it from @BotFather](https://t.me/BotFather))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/EnricoHuber/home-chatbot.git
cd home-chatbot
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run the bot**
```bash
python src/main.py
```

## ⚙️ Configuration

The bot uses JSON configuration files located in `configs/`:

- `base_config.json` - Development configuration
- `test_small_model.json` - Testing with smaller models
- `production_config.json` - Production-ready configuration

### Configuration Options

```json
{
  "llm": {
    "provider": "groq",
    "model": "llama-3.1-8b-instant",
    "temperature": 0.7,
    "max_tokens": 500
  },
  "rag": {
    "enabled": true,
    "embedding_model": "all-MiniLM-L6-v2",
    "max_search_results": 3
  },
  "telegram": {
    "enabled": true,
    "rate_limit_messages": 20,
    "rate_limit_window": 60
  }
}
```

### Environment Variables

```bash
GROQ_API_KEY=your_groq_api_key
TELEGRAM_BOT_TOKEN=your_telegram_token
ENVIRONMENT=production
CONFIG_PATH=./configs/production_config.json
```

## 🎮 Usage

### Telegram Commands

- `/start` - Initialize the bot
- `/help` - Show available commands
- `/stats` - View bot statistics
- `/info` - Information about the bot

### Example Questions

- "Come pulire il forno naturalmente?"
- "Come risparmiare energia in casa?"
- "Ricetta per detergente naturale"
- "Come rimuovere il calcare?"

### Adding Knowledge

1. **Via Telegram**: Send a PDF document
2. **Via Web Interface**: Use the admin panel
3. **Programmatically**: Use the `add_knowledge()` method

## 🖥️ Web Admin Interface

Run the Streamlit admin panel:

```bash
streamlit run src/interfaces/web_interface.py
```

Features:
- Dashboard with statistics
- Knowledge base management
- Test chat interface
- Configuration viewer

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy Options

#### Railway.app (Recommended)
```bash
railway login
railway init
railway up
```

#### Fly.io
```bash
flyctl launch
flyctl secrets set GROQ_API_KEY=xxx TELEGRAM_BOT_TOKEN=xxx
flyctl deploy
```

#### Docker
```bash
docker build -t home-chatbot .
docker run -e GROQ_API_KEY=xxx -e TELEGRAM_BOT_TOKEN=xxx home-chatbot
```

## 📊 Monitoring

Health check endpoint: `http://your-domain/health`

Logs are stored in `logs/chatbot.log`

## 🔧 Development

### Project Structure

- `src/core/` - Core chatbot functionality
- `src/handlers/` - Interface handlers (Telegram, etc.)
- `src/interfaces/` - User interfaces (Web, CLI)
- `src/utils/` - Utility functions and helpers
- `configs/` - Configuration files
- `logs/` - Application logs

### Running Tests

```bash
# Use test configuration
set ENVIRONMENT=test
python src/main.py
```

## 🛠️ Customization

### Adding New Knowledge Categories

Edit the base knowledge in `src/core/chatbot.py`:

```python
base_knowledge = [
    ("Your knowledge here", "category"),
]
```

### Changing LLM Model

Edit your config file:

```json
{
  "llm": {
    "model": "llama-3.3-70b-versatile"
  }
}
```

### Disabling RAG

```json
{
  "rag": {
    "enabled": false
  }
}
```

## 📦 Dependencies

- `python-telegram-bot` - Telegram bot framework
- `groq` - LLM provider
- `chromadb` - Vector database
- `sentence-transformers` - Embeddings
- `streamlit` - Web interface
- `flask` - Health check server

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Groq for the LLM API
- ChromaDB for vector database
- Sentence Transformers for embeddings
- Python Telegram Bot library

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the [DEPLOYMENT.md](DEPLOYMENT.md) for hosting help

## 🔮 Roadmap

- [ ] Add more data sources (web scraping, APIs)
- [ ] Multi-language support
- [ ] Voice message support
- [ ] Advanced analytics dashboard
- [ ] Integration with home automation systems
- [ ] Mobile app interface

---

**Made with ❤️ for smart home management**

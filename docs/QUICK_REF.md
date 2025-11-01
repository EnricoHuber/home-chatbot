# 🚀 Quick Reference Card

## ⚡ Quick Commands

### Local Development
```bash
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Then edit with your keys

# Run
python src/main.py

# Run web interface
streamlit run src/interfaces/web_interface.py

# Check environment
.\setup.ps1
```

### Deployment - Railway (Recommended)
```bash
# Install CLI
npm install -g @railway/cli

# Login & Deploy
railway login
railway init
railway up

# Set variables
railway variables set GROQ_API_KEY=xxx
railway variables set TELEGRAM_BOT_TOKEN=xxx
railway variables set ENVIRONMENT=production

# View logs
railway logs
```

### Deployment - Fly.io
```bash
# Install CLI (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Deploy
flyctl launch
flyctl secrets set GROQ_API_KEY=xxx TELEGRAM_BOT_TOKEN=xxx
flyctl deploy

# View logs
flyctl logs
```

### Docker
```bash
# Build
docker build -t home-chatbot .

# Run
docker run -e GROQ_API_KEY=xxx -e TELEGRAM_BOT_TOKEN=xxx home-chatbot

# With environment file
docker run --env-file .env home-chatbot
```

---

## 📋 Configuration Quick Reference

### Memory Optimization (256MB RAM)
```json
{
  "llm": {"model": "llama-3.1-8b-instant"},
  "rag": {
    "enabled": true,
    "embedding_model": "all-MiniLM-L6-v2"
  }
}
```

### Development (Full Features)
```json
{
  "llm": {"model": "llama-3.3-70b-versatile"},
  "rag": {
    "enabled": true,
    "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2"
  },
  "logging": {"level": "DEBUG", "verbose": true}
}
```

### Minimal (No RAG)
```json
{
  "llm": {"model": "llama-3.1-8b-instant"},
  "rag": {"enabled": false}
}
```

---

## 🔧 Environment Variables

### Required
```bash
GROQ_API_KEY=your_groq_api_key
TELEGRAM_BOT_TOKEN=your_telegram_token
```

### Optional
```bash
ENVIRONMENT=production
CONFIG_PATH=./configs/production_config.json
PORT=10000
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `src/main.py` | Main entry point |
| `configs/production_config.json` | Production settings |
| `.env` | Environment variables |
| `requirements.txt` | Dependencies |
| `Dockerfile` | Container config |
| `Procfile` | Railway/Heroku |
| `fly.toml` | Fly.io config |

---

## 🤖 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show help |
| `/stats` | Show statistics |
| `/info` | Bot information |
| Send PDF | Add to knowledge base |

---

## 🔍 Troubleshooting

### Bot doesn't start
```bash
# Check config
python -c "from utils import ConfigManager; cm = ConfigManager(); print(cm.validate_config())"

# Check environment
python -c "import os; print('GROQ:', bool(os.getenv('GROQ_API_KEY')))"
```

### Out of memory
```json
// Use in config:
{"llm": {"model": "llama-3.1-8b-instant"}}
{"rag": {"embedding_model": "all-MiniLM-L6-v2"}}
```

### Check logs
```bash
# Local
cat logs/chatbot.log

# Railway
railway logs

# Fly.io
flyctl logs

# Docker
docker logs container_name
```

---

## 🌐 Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/` | Status info |
| `/health` | Health check |

Example:
```bash
curl http://localhost:10000/health
```

---

## 💰 Cost Breakdown

| Platform | RAM | Cost | Always-On | Best For |
|----------|-----|------|-----------|----------|
| **Railway** | 512MB | $0-5/mo | ✅ | Demos |
| **Fly.io** | 256MB | $0 | ✅ | Free hosting |
| **Oracle** | 24GB | $0 | ✅ | Power users |

---

## 📊 Performance Tips

### Reduce API Calls
- Enable caching (on by default)
- Use smaller models
- Increase cache TTL in code

### Reduce Memory
```json
{
  "llm": {"model": "llama-3.1-8b-instant"},
  "rag": {"embedding_model": "all-MiniLM-L6-v2"}
}
```

### Improve Speed
- Use faster models
- Reduce max_tokens
- Enable caching

---

## 🔗 Important Links

### Get API Keys
- **Groq**: https://console.groq.com/keys
- **Telegram**: https://t.me/BotFather

### Hosting Platforms
- **Railway**: https://railway.app
- **Fly.io**: https://fly.io
- **Oracle**: https://cloud.oracle.com

### Documentation
- Main: `README_NEW.md`
- Deploy: `DEPLOYMENT.md`
- Structure: `STRUCTURE.md`
- Summary: `SUMMARY.md`

---

## ⚡ One-Liner Deploy

```bash
# Railway (after git push)
railway login && railway init && railway up

# Fly.io
flyctl launch && flyctl secrets set GROQ_API_KEY=xxx TELEGRAM_BOT_TOKEN=xxx && flyctl deploy
```

---

## 🎯 Project Structure at a Glance

```
src/
├── core/chatbot.py          # Main logic
├── handlers/telegram_handler.py  # Telegram
├── interfaces/web_interface.py   # Web UI
├── utils/config_manager.py  # Config
└── main.py                  # Entry point
```

---

## 📞 Need Help?

1. Check `DEPLOYMENT.md` for detailed guides
2. Review logs: `logs/chatbot.log`
3. Test locally first: `python src/main.py`
4. Verify environment: `.\setup.ps1`

---

**Save this file for quick reference! 📌**

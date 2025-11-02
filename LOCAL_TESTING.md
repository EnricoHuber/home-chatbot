# 🧪 Local Testing Guide

This guide will help you test the bot locally before deploying.

---

## 📋 Prerequisites

1. **Python 3.11** installed
2. **Git** installed
3. **Groq API Key** from https://console.groq.com/keys
4. **Telegram Bot Token** from https://t.me/BotFather

---

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies

```powershell
# Install Python dependencies
pip install -r requirements.txt
```

**Note**: This will take 2-3 minutes the first time (downloads ~500MB).

---

### Step 2: Configure Environment

Create a `.env` file in the project root:

```powershell
# Copy the example file
Copy-Item .env.example .env

# Edit .env with your favorite editor (Notepad, VSCode, etc.)
notepad .env
```

**Fill in your credentials:**

```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ENVIRONMENT=dev
```

---

### Step 3: Run the Bot

```powershell
# Run the bot
python src/main.py
```

**Expected output:**
```
🚀 Starting Home Assistant Chatbot
📝 Loading configuration from: configs/base_config.json
✅ Configuration loaded successfully
✅ HomeChatbot initialized successfully
✅ Telegram bot handler initialized
✅ Telegram bot is running!
📊 Bot info: @YourBotName
🔍 Press Ctrl+C to stop
```

---

### Step 4: Test in Telegram

1. Open Telegram
2. Search for your bot (@YourBotName)
3. Send: `/start`
4. You should get a welcome message!

**Try these commands:**
```
/start    - Welcome message
/help     - List of commands
/info     - Bot information
/stats    - Usage statistics
/addknowledge generale This is a test
```

---

## 🔧 Troubleshooting

### ❌ Error: "No module named 'chromadb'"

**Solution:**
```powershell
pip install -r requirements.txt
```

---

### ❌ Error: "Missing GROQ_API_KEY environment variable"

**Solution:**
1. Make sure you created the `.env` file
2. Check that `GROQ_API_KEY` is set correctly
3. Restart the bot

---

### ❌ Error: "Invalid Telegram bot token"

**Solution:**
1. Get a new token from https://t.me/BotFather
2. Update `TELEGRAM_BOT_TOKEN` in `.env`
3. Restart the bot

---

### ❌ Error: "NameError: name 'logging' is not defined"

**Solution:** Already fixed! Make sure you have the latest code:
```powershell
git pull
```

---

### ❌ Bot doesn't respond in Telegram

**Check:**
1. Bot is running (you see "✅ Telegram bot is running!" in console)
2. You're messaging the correct bot
3. Bot token is correct
4. Your Telegram user is not restricted (check `configs/base_config.json`)

---

## 📊 Testing Checklist

Before deploying, test these features:

- [ ] Bot starts without errors
- [ ] `/start` command works
- [ ] `/help` command works
- [ ] `/info` command works
- [ ] `/stats` command works
- [ ] Bot responds to questions
- [ ] `/addknowledge` adds new knowledge
- [ ] RAG system retrieves knowledge
- [ ] Health endpoint works: http://localhost:10000/health

---

## 🧪 Advanced Testing

### Test with Different Configs

```powershell
# Test with small model (faster)
$env:ENVIRONMENT="test"
python src/main.py

# Test with production config
$env:ENVIRONMENT="production"
python src/main.py
```

---

### Test Health Endpoint

Open another PowerShell window:

```powershell
# Test health endpoint
curl http://localhost:10000/health
```

**Expected response:**
```json
{"status": "healthy"}
```

---

### Test Web Interface (Optional)

```powershell
# Run web interface
streamlit run src/interfaces/web_interface.py
```

This opens a web dashboard at http://localhost:8501

---

## 🐛 Debug Mode

Enable verbose logging:

```powershell
# Edit .env
LOG_LEVEL=DEBUG

# Run bot
python src/main.py
```

You'll see detailed logs of everything happening.

---

## 🔄 Reset Everything

If you need to start fresh:

```powershell
# Delete knowledge database
Remove-Item -Recurse -Force chroma_db

# Delete cache
Remove-Item -Recurse -Force __pycache__

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall --no-cache-dir

# Restart bot
python src/main.py
```

---

## 📝 Testing Scenarios

### Scenario 1: Basic Chat
```
You: Ciao!
Bot: [Responds in Italian]
```

### Scenario 2: Add Knowledge
```
You: /addknowledge pulizia Per pulire il forno usare bicarbonato e aceto
Bot: ✅ Knowledge added successfully!
```

### Scenario 3: Retrieve Knowledge
```
You: Come pulisco il forno?
Bot: Per pulire il forno usare bicarbonato e aceto [+ LLM elaboration]
```

### Scenario 4: PDF Upload
```
1. Send a PDF file to the bot
2. Bot processes it
3. Ask questions about the PDF content
```

---

## ✅ Ready to Deploy?

Once all tests pass:

```powershell
# Commit your changes (if any)
git add .
git commit -m "Tested locally - ready for deployment"

# Push to trigger Railway deployment
git push
```

---

## 🎯 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Slow responses | Use smaller model in config |
| High memory usage | Disable RAG or use smaller embeddings |
| Rate limit errors | Reduce requests or upgrade Groq plan |
| Connection errors | Check internet connection |
| Import errors | Run `pip install -r requirements.txt` |

---

## 📚 Next Steps

After local testing works:

1. ✅ Confirm all features work
2. 🚀 Push to GitHub
3. 🔍 Monitor Railway deployment
4. 🧪 Test production deployment
5. 📊 Monitor logs and metrics

---

## 💡 Pro Tips

- **Use `ENVIRONMENT=dev`** for local testing (uses cheaper/faster models)
- **Keep logs visible** while testing to see what's happening
- **Test one feature at a time** to isolate issues
- **Check memory usage** with Task Manager while bot runs
- **Use Ctrl+C** to stop the bot gracefully

---

## 🆘 Still Having Issues?

1. Check bot logs for errors
2. Verify all environment variables are set
3. Make sure Python 3.11 is installed
4. Try deleting and recreating `.env` file
5. Reinstall dependencies

---

**Happy Testing! 🎉**

# 🐳 Testing Supabase with Docker Compose

Quick guide to test your bot with Supabase storage using Docker.

---

## 🎯 Prerequisites

1. ✅ Docker Desktop running
2. ✅ Supabase account created (see [`SUPABASE_SETUP.md`](SUPABASE_SETUP.md))
3. ✅ Supabase credentials ready

---

## 🚀 Quick Test (2 steps)

### Step 1: Update `.env` File

```env
# Your bot credentials
GROQ_API_KEY=gsk_your_actual_key
TELEGRAM_BOT_TOKEN=123456789:ABC...

# Use production config (which uses Supabase)
ENVIRONMENT=production

# Add your Supabase credentials
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### Step 2: Run Docker Compose

```powershell
docker-compose up --build
```

**Expected output:**
```
✅ Connected to Supabase: https://abcdefghijklmnop.sup...
✅ Table 'knowledge_base' exists and is accessible
✅ Supabase storage initialized
✅ RAG system initialized with supabase backend
✅ Telegram bot is running!
```

---

## 🧪 Test Knowledge Storage

### 1. Add Knowledge via Telegram

```
/start
/addknowledge pulizia Pulire i vetri con aceto e giornale
```

Bot responds: ✅ **Knowledge added successfully!**

---

### 2. Verify in Supabase Dashboard

1. Open Supabase dashboard
2. Go to **Table Editor** → `knowledge_base`
3. You should see your new entry! 🎉

---

### 3. Query the Knowledge

In Telegram:
```
Come pulisco i vetri?
```

Bot should respond using the knowledge you just added!

---

## 🔄 Test Both Storage Types

### Test with Supabase (Production):

```powershell
# In .env, set:
ENVIRONMENT=production
SUPABASE_URL=https://...
SUPABASE_KEY=...

# Run
docker-compose up --build
```

---

### Test with ChromaDB (Local):

```powershell
# In .env, set:
ENVIRONMENT=dev
# Comment out or leave blank Supabase vars

# Run
docker-compose up --build
```

---

## 📊 Monitor in Real-Time

### View Logs:

```powershell
# Follow logs
docker-compose logs -f chatbot

# Check last 50 lines
docker-compose logs --tail 50 chatbot
```

---

### Check Health:

```powershell
curl http://localhost:10000/health
```

Expected: `{"status":"healthy"}`

---

### Get Stats:

In Telegram:
```
/stats
```

Should show:
```
📊 Bot Statistics

💾 Knowledge Base:
- Total: 11 documents
- Storage: Supabase (PostgreSQL + pgvector)
- By category:
  • pulizia: 4
  • utenze: 3
  • manutenzione: 2
  • casa: 2
```

---

## 🎛️ Configuration Modes

### Mode 1: Supabase Only (Recommended)

```yaml
# docker-compose.yml
environment:
  - ENVIRONMENT=production  # Uses production_config.json
```

```json
// configs/production_config.json
{
  "rag": {
    "storage_type": "supabase"
  }
}
```

**Result:** All knowledge stored in Supabase cloud ☁️

---

### Mode 2: ChromaDB Only (Local Testing)

```yaml
# docker-compose.yml
environment:
  - ENVIRONMENT=dev  # Uses base_config.json
```

```json
// configs/base_config.json
{
  "rag": {
    "storage_type": "chromadb"
  }
}
```

**Result:** All knowledge stored locally in `./chroma_db` folder

---

### Mode 3: Hybrid (Advanced)

Run two containers:

```yaml
# docker-compose-hybrid.yml
version: '3.8'

services:
  chatbot-dev:
    build: .
    container_name: home-chatbot-dev
    environment:
      - ENVIRONMENT=dev
    ports:
      - "10000:10000"
    volumes:
      - ./chroma_db:/app/chroma_db

  chatbot-prod:
    build: .
    container_name: home-chatbot-prod
    environment:
      - ENVIRONMENT=production
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
    ports:
      - "10001:10000"
```

Test both simultaneously!

---

## 🐛 Troubleshooting

### ❌ "Missing SUPABASE_URL or SUPABASE_KEY"

**Check:**
```powershell
# View container environment variables
docker exec home-chatbot env | Select-String "SUPABASE"
```

**Fix:**
- Ensure `.env` has the variables
- Rebuild: `docker-compose down && docker-compose up --build`

---

### ❌ "Could not connect to Supabase"

**Check:**
1. Supabase project is active (not paused)
2. API key is correct (anon/public key)
3. URL format: `https://xxxxx.supabase.co`

**Test connection:**
```powershell
curl https://your-project-id.supabase.co/rest/v1/
```

---

### ❌ "Table 'knowledge_base' does not exist"

**Fix:** Run SQL setup in Supabase (see [`SUPABASE_SETUP.md`](SUPABASE_SETUP.md) Step 4)

---

### ❌ Bot falls back to ChromaDB

**Check logs:**
```powershell
docker-compose logs chatbot | Select-String "storage"
```

Look for:
- ✅ "Supabase storage initialized" → Good!
- ⚠️ "Falling back to ChromaDB" → Check Supabase credentials

---

## 📈 Performance Testing

### Test Response Time:

```python
# In Telegram, send:
/addknowledge generale Test $(Get-Date)

# Then immediately query:
Tell me about test

# Check logs for timing:
docker-compose logs chatbot | Select-String "performance"
```

**Expected:**
- Supabase: 50-150ms
- ChromaDB: 10-50ms

---

### Test Scalability:

Add multiple items quickly:
```
/addknowledge generale Item 1
/addknowledge generale Item 2
/addknowledge generale Item 3
...
```

Check Supabase dashboard for all entries.

---

## 🧹 Cleanup

### Stop containers:
```powershell
docker-compose down
```

### Remove volumes (ChromaDB data):
```powershell
docker-compose down -v
```

### Remove images:
```powershell
docker rmi home-chatbot
```

### Clear Supabase data:
In Supabase SQL Editor:
```sql
DELETE FROM knowledge_base;
```

---

## 💡 Pro Tips

### 1. Watch Supabase Real-Time

In Supabase Dashboard:
- **Table Editor** → Enable real-time
- Add knowledge via Telegram
- Watch rows appear instantly!

---

### 2. Compare Storage Performance

```powershell
# Test ChromaDB
$env:ENVIRONMENT="dev"
docker-compose up -d
# Add 10 items, test query speed

# Test Supabase
$env:ENVIRONMENT="production"
docker-compose restart
# Add 10 items, test query speed

# Compare in logs
docker-compose logs | Select-String "search took"
```

---

### 3. Backup Before Testing

```powershell
# Backup ChromaDB
Copy-Item -Recurse chroma_db chroma_db.backup

# Backup Supabase
# In Supabase Dashboard → Database → Backups → Download
```

---

### 4. Use Different Telegram Bots

Test both storage types with different bots:

```env
# .env.dev
TELEGRAM_BOT_TOKEN=dev_bot_token
ENVIRONMENT=dev

# .env.prod
TELEGRAM_BOT_TOKEN=prod_bot_token
ENVIRONMENT=production
```

---

## ✅ Success Checklist

After docker-compose up, verify:

- [ ] Container is running: `docker ps`
- [ ] Logs show "Supabase storage initialized"
- [ ] Health check passes: `curl http://localhost:10000/health`
- [ ] `/start` works in Telegram
- [ ] `/addknowledge` adds to Supabase
- [ ] Can see data in Supabase dashboard
- [ ] Bot retrieves knowledge in responses
- [ ] `/stats` shows Supabase backend

---

## 🚀 Next: Deploy to Railway

Once local Docker test passes:

```powershell
# Add Supabase vars to Railway
railway variables set SUPABASE_URL=https://...
railway variables set SUPABASE_KEY=...

# Push and deploy
git add .
git commit -m "Add Supabase persistent storage"
git push
```

Railway will use the **same Docker setup**! ✅

---

**Your bot now has persistent, unlimited knowledge storage! 🎉**

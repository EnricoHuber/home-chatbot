# 🐳 Docker Local Testing Guide

Test your bot in Docker Desktop before deploying to production.

---

## 🚀 Quick Start (2 commands)

### Option 1: Build and Run Manually

```powershell
# Build the image
docker build -t home-chatbot .

# Run with your credentials
docker run -d `
  --name home-chatbot `
  -e GROQ_API_KEY=your_groq_api_key_here `
  -e TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here `
  -e ENVIRONMENT=dev `
  -p 10000:10000 `
  home-chatbot
```

---

### Option 2: Use Docker Compose (Recommended)

**Create `.env` file first** (if not exists):
```powershell
Copy-Item .env.example .env
notepad .env  # Add your keys
```

**Then run:**
```powershell
docker-compose up --build
```

That's it! ✅

---

## 📋 Step-by-Step

### 1. Make Sure Docker Desktop is Running

- Open Docker Desktop
- Wait for "Docker Desktop is running" status
- Check: `docker --version`

---

### 2. Build the Image

```powershell
# Build image (takes 3-5 minutes first time)
docker build -t home-chatbot .

# Verify image was created
docker images | Select-String "home-chatbot"
```

**Expected output:**
```
home-chatbot    latest    abc123def456    2 minutes ago    800MB
```

---

### 3. Run Container

```powershell
# Run in detached mode (-d)
docker run -d `
  --name home-chatbot `
  -e GROQ_API_KEY=gsk_your_actual_key `
  -e TELEGRAM_BOT_TOKEN=123456789:ABC... `
  -e ENVIRONMENT=dev `
  -p 10000:10000 `
  home-chatbot
```

---

### 4. Check Logs

```powershell
# View logs
docker logs home-chatbot

# Follow logs in real-time
docker logs -f home-chatbot
```

**Expected logs:**
```
🚀 Starting Home Assistant Chatbot
📝 Loading configuration from: configs/base_config.json
✅ Configuration loaded successfully
✅ Telegram bot is running!
```

---

### 5. Test the Bot

1. Open Telegram
2. Send `/start` to your bot
3. Bot should respond! ✅

**Also test health endpoint:**
```powershell
curl http://localhost:10000/health
```

Expected: `{"status":"healthy"}`

---

## 🛠️ Docker Commands Cheat Sheet

### View Running Containers
```powershell
docker ps
```

### View All Containers (including stopped)
```powershell
docker ps -a
```

### View Logs
```powershell
docker logs home-chatbot           # All logs
docker logs -f home-chatbot        # Follow (live)
docker logs --tail 50 home-chatbot # Last 50 lines
```

### Stop Container
```powershell
docker stop home-chatbot
```

### Start Container
```powershell
docker start home-chatbot
```

### Restart Container
```powershell
docker restart home-chatbot
```

### Remove Container
```powershell
docker stop home-chatbot
docker rm home-chatbot
```

### Remove Image
```powershell
docker rmi home-chatbot
```

### Access Container Shell
```powershell
docker exec -it home-chatbot /bin/bash
```

---

## 🐳 Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  chatbot:
    build: .
    container_name: home-chatbot
    env_file:
      - .env
    environment:
      - ENVIRONMENT=dev
    ports:
      - "10000:10000"
    volumes:
      - ./chroma_db:/app/chroma_db
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:10000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Use Docker Compose:

```powershell
# Start (builds if needed)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Remove everything (including volumes)
docker-compose down -v
```

---

## 🔍 Debugging Docker Issues

### Issue: Build fails with "No module named..."
**Solution:** Make sure `requirements.txt` is correct
```powershell
docker build --no-cache -t home-chatbot .
```

---

### Issue: Container stops immediately
**Solution:** Check logs for errors
```powershell
docker logs home-chatbot
```

Common causes:
- Missing environment variables
- Invalid API keys
- Config file errors

---

### Issue: Bot doesn't respond in Telegram
**Solution:** Check if bot is actually running
```powershell
docker logs home-chatbot | Select-String "running"
```

Verify environment variables:
```powershell
docker exec home-chatbot env | Select-String "TELEGRAM"
```

---

### Issue: "Port already in use"
**Solution:** Stop the conflicting container
```powershell
# Find what's using port 10000
netstat -ano | findstr :10000

# Stop your local Python version if running
# Or use a different port:
docker run -d -p 8080:10000 home-chatbot
```

---

## 💡 Pro Tips

### 1. Use Environment File
Create `.env`:
```env
GROQ_API_KEY=gsk_your_key
TELEGRAM_BOT_TOKEN=123:ABC
ENVIRONMENT=dev
```

Then run:
```powershell
docker run -d --name home-chatbot --env-file .env -p 10000:10000 home-chatbot
```

---

### 2. Persist Knowledge Database
Mount volume to keep knowledge between container restarts:
```powershell
docker run -d `
  --name home-chatbot `
  --env-file .env `
  -p 10000:10000 `
  -v ${PWD}/chroma_db:/app/chroma_db `
  home-chatbot
```

---

### 3. Live Code Updates (Development)
Mount source code for live changes:
```powershell
docker run -d `
  --name home-chatbot-dev `
  --env-file .env `
  -p 10000:10000 `
  -v ${PWD}/src:/app/src `
  -v ${PWD}/configs:/app/configs `
  home-chatbot
```

---

### 4. Use Different Dockerfiles
For Railway-optimized version:
```powershell
docker build -f Dockerfile.railway -t home-chatbot:railway .
```

---

## 📊 Monitoring

### Check Resource Usage
```powershell
docker stats home-chatbot
```

Shows:
- CPU usage
- Memory usage
- Network I/O
- Disk I/O

**Expected:**
- Memory: ~200-300MB
- CPU: <5% (idle), 10-30% (processing)

---

### View Container Details
```powershell
docker inspect home-chatbot
```

---

## ✅ Test Checklist

After running container:

- [ ] Container is running: `docker ps`
- [ ] Logs show "bot is running": `docker logs home-chatbot`
- [ ] Health check passes: `curl http://localhost:10000/health`
- [ ] Bot responds in Telegram: `/start`
- [ ] Can add knowledge: `/addknowledge generale Test`
- [ ] Memory usage <512MB: `docker stats home-chatbot`

---

## 🚀 Ready for Production?

Once Docker testing passes:

```powershell
# Commit changes
git add .
git commit -m "Tested in Docker - ready for deployment"
git push
```

Railway/Render/Fly.io will use the **same Dockerfile**! ✅

---

## 🎯 Quick Testing Workflow

```powershell
# 1. Build
docker build -t home-chatbot .

# 2. Run
docker run -d --name home-chatbot --env-file .env -p 10000:10000 home-chatbot

# 3. Check logs
docker logs -f home-chatbot

# 4. Test in Telegram
# Send /start to your bot

# 5. If issues, rebuild:
docker stop home-chatbot
docker rm home-chatbot
docker build --no-cache -t home-chatbot .
docker run -d --name home-chatbot --env-file .env -p 10000:10000 home-chatbot

# 6. When done:
docker stop home-chatbot
docker rm home-chatbot
```

---

## 🆘 Need Help?

**Check Docker Desktop Dashboard:**
- Click on container name
- View logs, stats, files
- Use built-in terminal

**Common Issues:**
- "Cannot connect to Docker daemon" → Start Docker Desktop
- "Image not found" → Run `docker build` first
- "Container exits immediately" → Check `docker logs` for errors

---

**Happy Docker Testing! 🐳**

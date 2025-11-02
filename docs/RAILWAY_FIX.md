# 🚂 Railway Deployment - Quick Fix Guide

## ❌ Problem: Build Timeout

The build was timing out at the `pip install` step because **PyTorch** is ~2GB and takes too long to download/install.

---

## ✅ Solution Applied

### 1. **Optimized Dockerfile**
- Installs PyTorch CPU-only version (smaller, faster)
- Better caching strategy
- Minimal dependencies

### 2. **Improved .dockerignore**
- Excludes unnecessary files from build context
- Faster upload to Railway
- Smaller build context

### 3. **Updated requirements.txt**
- Removed explicit `torch>=2.0.0` dependency
- Let sentence-transformers handle it automatically

---

## 🚀 Deploy to Railway (Try Again)

### Option 1: Push to GitHub (Easiest)

```bash
# Commit changes
git add .
git commit -m "Optimize for Railway deployment"
git push

# Railway will automatically rebuild
```

### Option 2: Railway CLI

```bash
# If you have Railway CLI installed
railway up
```

### Option 3: Manual Trigger

1. Go to Railway dashboard
2. Click your project
3. Go to "Deployments"
4. Click "Deploy" to trigger manual rebuild

---

## ⚙️ Railway Configuration

Make sure these environment variables are set in Railway dashboard:

```bash
GROQ_API_KEY=your_groq_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
ENVIRONMENT=production
```

**To set them:**
1. Go to your project in Railway
2. Click "Variables" tab
3. Add each variable
4. Click "Deploy" to apply

---

## 📊 Expected Build Time

After optimization:
- **Before**: 10+ minutes (timeout)
- **After**: 3-5 minutes ✅

---

## 🔍 Monitor the Build

Watch the build logs in Railway:
1. Go to "Deployments" tab
2. Click on the latest deployment
3. Watch the logs

You should see:
```
✓ [1/7] FROM docker.io/library/python:3.11-slim
✓ [2/7] WORKDIR /app
✓ [3/7] RUN apt-get update...
✓ [4/7] COPY requirements.txt .
✓ [5/7] RUN pip install torch... (this should complete now)
✓ [6/7] RUN pip install -r requirements.txt
✓ [7/7] COPY . .
```

---

## ⚠️ If Build Still Fails

### Try Even More Aggressive Optimization:

**Disable RAG temporarily** in `configs/production_config.json`:

```json
{
  "rag": {
    "enabled": false
  }
}
```

This removes the need for sentence-transformers and torch entirely!

**Then update requirements to minimal:**
```txt
python-telegram-bot==20.7
groq==0.4.1
flask==3.0.0
python-dotenv==1.0.0
requests==2.31.0
```

---

## 🎯 Alternative: Use Fly.io Instead

If Railway continues to timeout, try Fly.io:

```bash
# Install Fly CLI (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Deploy
flyctl launch
flyctl secrets set GROQ_API_KEY=xxx TELEGRAM_BOT_TOKEN=xxx
flyctl deploy
```

Fly.io handles builds differently and may work better.

---

## ✅ After Successful Deployment

Check if bot is running:

1. **Health Check**: Visit `https://your-app.railway.app/health`
   - Should return: `{"status": "healthy"}`

2. **Logs**: Check Railway logs
   - Should see: "✅ Telegram bot is running!"

3. **Test Bot**: Open Telegram
   - Send `/start` to your bot
   - Should respond immediately

---

## 🐛 Troubleshooting

### Build still times out?
→ Disable RAG in config (see above)

### Bot crashes after deployment?
→ Check logs for missing environment variables

### Bot doesn't respond?
→ Verify TELEGRAM_BOT_TOKEN is correct

### Out of memory?
→ Use smaller model: `llama-3.1-8b-instant`

---

## 📞 Need Help?

1. Check Railway logs
2. Verify environment variables
3. Try Fly.io as alternative
4. Disable RAG temporarily to test

---

## 🎉 Success Checklist

- [ ] Git push with optimized Dockerfile
- [ ] Railway rebuild triggered
- [ ] Build completes in 3-5 minutes
- [ ] Health check returns 200
- [ ] Bot responds in Telegram
- [ ] Can use `/addknowledge` command
- [ ] RAG works (if enabled)

---

**Your optimized deployment is ready! Push to GitHub and let Railway rebuild! 🚀**

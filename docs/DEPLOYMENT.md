# 🚀 FREE Deployment Options for Home Assistant Chatbot

This guide covers **FREE** hosting options for your Telegram bot with their pros, cons, and limitations.

---

## 🎯 Best FREE Options (Recommended)

### 1. ⭐ **Railway.app** (RECOMMENDED)
**Perfect for Telegram bots!**

#### Pros:
- ✅ **$5 FREE credit/month** (enough for small bots)
- ✅ **No sleep** - bot runs 24/7
- ✅ **512 MB RAM** (sufficient with optimizations)
- ✅ Simple deployment
- ✅ Automatic HTTPS
- ✅ Great for long-running processes
- ✅ PostgreSQL/Redis available if needed

#### Cons:
- ⚠️ After free credit, requires payment
- ⚠️ Credit card required (but not charged automatically)

#### Deployment Steps:
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
railway init

# 4. Add environment variables
railway variables set GROQ_API_KEY=your_key_here
railway variables set TELEGRAM_BOT_TOKEN=your_token_here
railway variables set ENVIRONMENT=production

# 5. Deploy
railway up
```

Or use the Railway Dashboard:
1. Go to https://railway.app
2. Create new project from GitHub
3. Add environment variables
4. Deploy automatically!

**Monthly cost with free tier:** $0 (if usage < $5/month)

---

### 2. 🔥 **Fly.io** (GREAT ALTERNATIVE)
**Excellent for always-on bots**

#### Pros:
- ✅ **Free tier:** 3 shared VMs, 256 MB RAM each
- ✅ **No sleep** - runs 24/7
- ✅ Good for Telegram bots
- ✅ Persistent storage available

#### Cons:
- ⚠️ Requires credit card
- ⚠️ 256 MB RAM (need to optimize embedding model)

#### Deployment Steps:
```bash
# 1. Install flyctl
# Windows (PowerShell):
iwr https://fly.io/install.ps1 -useb | iex

# 2. Login
flyctl auth login

# 3. Create fly.toml (see deployment/fly.toml)

# 4. Deploy
flyctl launch
flyctl secrets set GROQ_API_KEY=your_key_here
flyctl secrets set TELEGRAM_BOT_TOKEN=your_token_here
flyctl deploy
```

**Monthly cost:** FREE forever (within limits)

---

### 3. ☁️ **Oracle Cloud Free Tier** (BEST FOR POWER USERS)
**Most powerful free option!**

#### Pros:
- ✅ **FREE FOREVER** - truly free
- ✅ **24 GB RAM** available (2 ARM VMs)
- ✅ **200 GB storage**
- ✅ No credit card charging
- ✅ Full VM control

#### Cons:
- ⚠️ More complex setup (requires server management)
- ⚠️ Need to configure firewall, security, etc.
- ⚠️ Requires basic DevOps knowledge

#### Deployment Steps:
1. Create Oracle Cloud account
2. Create a VM instance (ARM - Always Free)
3. SSH into the VM
4. Install Docker
5. Deploy your container

**Monthly cost:** $0 FOREVER

---

### 4. 🐙 **GitHub Actions** (CREATIVE SOLUTION)
**For scheduled/periodic bots**

#### Pros:
- ✅ Completely FREE
- ✅ 2000 minutes/month
- ✅ Good for scheduled tasks

#### Cons:
- ❌ **NOT for 24/7 bots** (max 6 hours per run)
- ❌ Not suitable for real-time Telegram bots
- ✅ Good for: notifications, reports, scheduled updates

---

## 🚫 Options to AVOID

### ❌ **Render.com Free Tier**
- **Problem:** 512 MB RAM + **sleeps after 15 min inactivity**
- Telegram bots need to be always awake
- You'll lose messages during sleep

### ❌ **Heroku Free Tier** 
- No longer exists (discontinued Nov 2022)

### ❌ **PythonAnywhere Free**
- Doesn't support long-running processes
- Only for web apps with requests

---

## 💡 Optimizations for FREE Hosting

### To fit in 256-512 MB RAM:

1. **Use smaller embedding model:**
```json
{
  "rag": {
    "embedding_model": "all-MiniLM-L6-v2"  // ~90 MB instead of ~470 MB
  }
}
```

2. **Use smaller LLM model:**
```json
{
  "llm": {
    "model": "llama-3.1-8b-instant"  // Faster and uses less memory
  }
}
```

3. **Disable RAG if not needed initially:**
```json
{
  "rag": {
    "enabled": false  // Use only LLM without vector DB
  }
}
```

4. **Add memory optimization in Dockerfile:**
```dockerfile
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
ENV TRANSFORMERS_OFFLINE=1
```

---

## 🎯 My Recommendation for YOU

Based on your needs (demo, free, always-on):

### **Option 1: Railway.app** (Easiest & Best)
- Start with the $5/month free credit
- Should last the entire month for a demo bot
- Easy deployment
- No sleep issues
- **Best for:** Professional demos and presentations

### **Option 2: Fly.io** (Free Forever)
- Truly free, no credit required after setup
- Runs 24/7
- Need to optimize for 256 MB RAM
- **Best for:** Long-term free hosting

### **Option 3: Oracle Cloud** (Most Powerful)
- If you're comfortable with servers
- Unlimited potential
- Free forever
- **Best for:** Full control and scalability

---

## 📦 Quick Start with Railway (RECOMMENDED)

1. **Optimize config for Railway:**
```bash
cp configs/production_config.json configs/railway_config.json
```

Edit `railway_config.json`:
```json
{
  "llm": {
    "model": "llama-3.1-8b-instant"
  },
  "rag": {
    "enabled": true,
    "embedding_model": "all-MiniLM-L6-v2"
  }
}
```

2. **Deploy to Railway:**
```bash
# Push to GitHub first
git add .
git commit -m "Ready for deployment"
git push

# Then on Railway dashboard:
# - Connect GitHub repo
# - Add environment variables
# - Deploy!
```

3. **Set environment variables in Railway:**
```
GROQ_API_KEY=your_groq_api_key
TELEGRAM_BOT_TOKEN=your_telegram_token
ENVIRONMENT=production
CONFIG_PATH=./configs/production_config.json
```

---

## 🔍 Monitoring Your Bot

All platforms provide logs:
- **Railway:** Check logs in dashboard
- **Fly.io:** `flyctl logs`
- **Oracle:** `docker logs container_name`

Your bot includes health check endpoint: `http://your-domain/health`

---

## 💰 Cost Comparison

| Platform | RAM | Cost/Month | Always-On | Best For |
|----------|-----|------------|-----------|----------|
| **Railway** | 512 MB | $0-5 | ✅ Yes | **Demos** |
| **Fly.io** | 256 MB | $0 | ✅ Yes | **Long-term free** |
| **Oracle** | 24 GB | $0 | ✅ Yes | **Power users** |
| Render | 512 MB | $0 | ❌ Sleeps | ❌ Not suitable |

---

## 🆘 Troubleshooting

### "Out of Memory" errors:
1. Use smaller embedding model
2. Disable RAG initially
3. Reduce max_tokens in config

### Bot doesn't respond:
1. Check logs for errors
2. Verify environment variables are set
3. Check health endpoint: `curl https://your-app.railway.app/health`

### Deployment fails:
1. Check Python version (3.11)
2. Verify all dependencies install
3. Check build logs

---

## 📞 Need Help?

Check the logs first:
```bash
# Railway
railway logs

# Fly.io
flyctl logs

# Local testing
python src/main.py
```

---

**Ready to deploy? Start with Railway.app - it's the easiest and most reliable free option for your demo! 🚀**

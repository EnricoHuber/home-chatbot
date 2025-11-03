# 🚀 Supabase Setup Guide - FREE Persistent Knowledge Storage

This guide will help you set up Supabase as your **free, persistent, unlimited** knowledge storage backend.

---

## 🎯 Why Supabase?

✅ **FREE 500MB** (expandable to 8GB free)  
✅ **Persists forever** (survives Railway restarts)  
✅ **PostgreSQL + pgvector** (proper vector database)  
✅ **Web UI** (manage knowledge via dashboard)  
✅ **SQL queries** (powerful filtering/analytics)  
✅ **Automatic backups**  
✅ **Scales to millions of documents**  

---

## 📋 Step-by-Step Setup (10 minutes)

### Step 1: Create Supabase Account

1. Go to [https://supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign up with GitHub (recommended) or email
4. ✅ **FREE forever** - no credit card required!

---

### Step 2: Create New Project

1. Click "New Project"
2. Fill in:
   - **Name**: `home-chatbot` (or any name)
   - **Database Password**: Generate strong password (SAVE THIS!)
   - **Region**: Choose closest to you (e.g., `eu-central-1`)
   - **Pricing Plan**: **Free** (selected by default)
3. Click "Create new project"
4. ⏳ Wait 1-2 minutes for provisioning

---

### Step 3: Enable pgvector Extension

1. Go to **SQL Editor** (left sidebar)
2. Click "**+ New Query**"
3. Paste this SQL:

```sql
-- Enable pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;
```

4. Click "**Run**" or press `Ctrl+Enter`
5. ✅ Should see: "Success. No rows returned"

---

### Step 4: Create Knowledge Table

In the same SQL Editor, run this:

```sql
-- Create knowledge_base table
CREATE TABLE IF NOT EXISTS knowledge_base (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    category TEXT DEFAULT 'generale',
    embedding vector(384),  -- 384 dimensions for all-MiniLM-L6-v2
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for fast vector similarity search
CREATE INDEX IF NOT EXISTS knowledge_base_embedding_idx 
ON knowledge_base USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Create index for category filtering
CREATE INDEX IF NOT EXISTS knowledge_base_category_idx 
ON knowledge_base(category);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS knowledge_base_created_at_idx 
ON knowledge_base(created_at DESC);
```

✅ Should see: "Success. No rows returned"

---

### Step 5: Create Search Function

Create this PostgreSQL function for vector similarity search:

```sql
-- Create function for vector similarity search
CREATE OR REPLACE FUNCTION match_knowledge(
    query_embedding vector(384),
    match_count int DEFAULT 3,
    filter_category text DEFAULT NULL
)
RETURNS TABLE (
    id text,
    content text,
    category text,
    metadata jsonb,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        knowledge_base.id,
        knowledge_base.content,
        knowledge_base.category,
        knowledge_base.metadata,
        1 - (knowledge_base.embedding <=> query_embedding) AS similarity
    FROM knowledge_base
    WHERE 
        CASE 
            WHEN filter_category IS NOT NULL THEN knowledge_base.category = filter_category
            ELSE true
        END
    ORDER BY knowledge_base.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
```

✅ Should see: "Success. No rows returned"

---

### Step 6: Get API Credentials

1. Go to **Settings** → **API** (left sidebar)
2. Find these two values:

**Project URL** (looks like):
```
https://abcdefghijklmnop.supabase.co
```

**API Keys** - Use the `anon` `public` key (looks like):
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

3. **Copy both values** - you'll need them next!

---

### Step 7: Add to .env File

Add these to your `.env` file:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_anon_public_key_here
```

**Example:**
```env
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYxMjUzMjgwMCwiZXhwIjoxOTI4MTA4ODAwfQ.xxxxxxxxxxxxx
```

---

### Step 8: Update Config for Production

In `configs/production_config.json`, ensure:

```json
{
  "rag": {
    "enabled": true,
    "storage_type": "supabase",
    "embedding_model": "all-MiniLM-L6-v2",
    "max_search_results": 3,
    "similarity_threshold": 0.7
  }
}
```

---

### Step 9: Add to Railway

In Railway dashboard:

1. Go to your bot service
2. Click "**Variables**" tab
3. Add these two variables:
   - `SUPABASE_URL` = `https://your-project-id.supabase.co`
   - `SUPABASE_KEY` = `your_anon_public_key`
4. Click "**Deploy**"

---

### Step 10: Test Locally

```powershell
# Install Supabase package
pip install supabase

# Test the bot
python src/main.py
```

Expected output:
```
✅ Connected to Supabase: https://abcdefghijklmnop.sup...
✅ Table 'knowledge_base' exists and is accessible
✅ Supabase storage initialized
✅ RAG system initialized with supabase backend
```

---

## 🧪 Verify Setup

### Test in Telegram:

```
/start
/addknowledge generale This is a test from Supabase!
```

Bot should respond: ✅ Knowledge added successfully!

---

### Check in Supabase Dashboard:

1. Go to **Table Editor** (left sidebar)
2. Select `knowledge_base` table
3. You should see your test entry! 🎉

---

## 📊 View Your Knowledge

In Supabase SQL Editor, run:

```sql
-- See all knowledge
SELECT id, content, category, created_at 
FROM knowledge_base 
ORDER BY created_at DESC;

-- Count by category
SELECT category, COUNT(*) as count
FROM knowledge_base
GROUP BY category
ORDER BY count DESC;

-- Search for text
SELECT content, category
FROM knowledge_base
WHERE content ILIKE '%test%';
```

---

## 🎛️ Switch Between ChromaDB and Supabase

### Use ChromaDB (Local, for dev):

In `configs/base_config.json`:
```json
{
  "rag": {
    "storage_type": "chromadb"
  }
}
```

---

### Use Supabase (Cloud, for production):

In `configs/production_config.json`:
```json
{
  "rag": {
    "storage_type": "supabase"
  }
}
```

---

## 🔧 Troubleshooting

### ❌ "Missing SUPABASE_URL or SUPABASE_KEY"

**Solution:** Add them to `.env` file and Railway variables

---

### ❌ "Table 'knowledge_base' does not exist"

**Solution:** Run the SQL in Step 4 again

---

### ❌ "function match_knowledge does not exist"

**Solution:** Run the SQL in Step 5 again

---

### ❌ "could not open extension control file"

**Solution:** pgvector not enabled. Run Step 3 SQL again

---

### ❌ Bot falls back to ChromaDB

**Check:**
1. `pip install supabase` was run
2. `.env` has correct `SUPABASE_URL` and `SUPABASE_KEY`
3. Config has `"storage_type": "supabase"`
4. Railway variables are set

---

## 📈 Storage Limits

| Tier | Storage | Bandwidth | Cost |
|------|---------|-----------|------|
| **Free** | 500MB | 5GB/month | $0 |
| **Pro** | 8GB | 50GB/month | $25/month |
| **Team** | 100GB | 250GB/month | $599/month |

**For home chatbot:** Free tier = **500,000+ documents!** 🚀

---

## 🎯 Benefits vs ChromaDB

| Feature | ChromaDB (Local) | Supabase (Cloud) |
|---------|------------------|------------------|
| **Persistence** | ❌ Lost on restart | ✅ Forever |
| **Storage** | 512MB (Railway) | 500MB-8GB |
| **Speed** | ⚡ 10-50ms | ⚡ 50-150ms |
| **Cost** | Railway RAM | FREE |
| **Management** | Files only | 🌐 Web UI |
| **Backups** | Manual | ✅ Automatic |
| **Collaboration** | ❌ No | ✅ Yes |
| **SQL Queries** | ❌ No | ✅ Yes |

---

## 💡 Pro Tips

### 1. Monitor Usage

In Supabase Dashboard → **Settings** → **Usage**
- See database size
- Track API requests
- Monitor bandwidth

---

### 2. Backup Your Knowledge

```sql
-- Export all knowledge
COPY (
    SELECT * FROM knowledge_base
) TO '/path/to/backup.csv' WITH CSV HEADER;
```

Or use Supabase UI: **Database** → **Backups**

---

### 3. Add More Categories

```python
# In Telegram
/addknowledge finanza Investire in ETF è semplice e sicuro
/addknowledge salute Bere 2 litri di acqua al giorno
/addknowledge ricette Pasta aglio e olio: 3 minuti di cottura
```

---

### 4. Bulk Import

In Supabase SQL Editor:

```sql
INSERT INTO knowledge_base (id, content, category, embedding) VALUES
('id1', 'Content 1', 'categoria1', NULL),  -- Embeddings added by bot later
('id2', 'Content 2', 'categoria2', NULL);
```

---

### 5. Advanced Queries

```sql
-- Find similar items manually
SELECT content, 
       1 - (embedding <=> '[0.1, 0.2, ...]'::vector) AS similarity
FROM knowledge_base
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
LIMIT 5;
```

---

## ✅ Setup Complete!

Your bot now has:
- ✅ **Persistent storage** (knowledge survives restarts)
- ✅ **500MB free** (500,000+ documents)
- ✅ **Web UI** for management
- ✅ **Automatic backups**
- ✅ **Production ready**

---

## 🚀 Next Steps

1. Test adding knowledge via Telegram
2. Deploy to Railway
3. Add more documents
4. Monitor usage in Supabase dashboard
5. Optional: Set up automatic backups

---

**Your chatbot now has unlimited, persistent knowledge! 🎉**

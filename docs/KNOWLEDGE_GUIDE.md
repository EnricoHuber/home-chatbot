# 📚 Adding Knowledge to Your Bot

Your bot can now learn new information in **3 ways**!

---

## Method 1: 💬 Text Command (NEW!)

### Basic Usage:
```
/addknowledge Your information here
```

### With Category:
```
/addknowledge [category] Your information here
```

### Available Categories:
- `pulizia` - Cleaning tips
- `utenze` - Utilities & bills
- `manutenzione` - Maintenance
- `casa` - General house info
- `generale` - Miscellaneous (default)

---

## 📝 Examples

### Simple (auto-categorized as "generale"):
```
/addknowledge Il garage si apre con il codice 1234
```

### With Category - Utilities:
```
/addknowledge utenze Il contratto elettrico scade il 31/12/2025 con Enel Energia
```

### With Category - Cleaning:
```
/addknowledge pulizia Per il pavimento in parquet usare solo panni umidi, mai prodotti chimici aggressivi
```

### With Category - Maintenance:
```
/addknowledge manutenzione Il filtro del condizionatore va cambiato ogni 3 mesi, modello XXL-500
```

### With Category - House:
```
/addknowledge casa La caldaia è stata installata nel 2020 e va revisionata annualmente
```

---

## Method 2: 📄 PDF Documents

Simply send a PDF file to the bot:
1. Open chat with bot
2. Send any PDF (contracts, manuals, notes)
3. Bot processes and extracts knowledge
4. Done!

**Best for:**
- Contracts (electricity, gas, internet)
- Appliance manuals
- House documentation
- Maintenance schedules

---

## Method 3: 🌐 Web Interface

```bash
streamlit run src/interfaces/web_interface.py
```

Then go to "Knowledge Base" tab:
- Add text manually with category
- Upload PDF documents
- View all knowledge

**Best for:**
- Bulk additions
- Managing existing knowledge
- Organized entry

---

## 🎯 Demo Scenario

### Before Adding Knowledge:
```
You: "Quando scade il mio contratto elettrico?"
Bot: "Non ho informazioni specifiche sul tuo contratto..."
```

### Add Knowledge via Telegram:
```
You: /addknowledge utenze Contratto Enel Energia, scadenza 31/12/2025, potenza 3kW
Bot: ✅ Conoscenza aggiunta!
     📁 Categoria: utenze
     📝 Contenuto: Contratto Enel Energia, scadenza 31/12/2025...
```

### Now Ask Again:
```
You: "Quando scade il mio contratto elettrico?"
Bot: "Il tuo contratto elettrico con Enel Energia scade il 31 dicembre 2025..."
```

🎉 **The bot learned from you!**

---

## 💡 Pro Tips

### 1. Be Specific
❌ Bad: `/addknowledge luce scade`
✅ Good: `/addknowledge utenze Contratto luce Enel scade 31/12/2025`

### 2. Use Categories
Helps organize and retrieve info better:
```
/addknowledge pulizia Per il marmo non usare mai ammoniaca
```

### 3. Add Context
❌ Bad: `/addknowledge codice 1234`
✅ Good: `/addknowledge Il codice del garage è 1234, cambiato a ottobre 2024`

### 4. One Topic Per Command
❌ Bad: Mix multiple unrelated topics
✅ Good: One command = one piece of information

---

## 🔍 Check What You've Added

Use `/stats` to see:
- Total documents in knowledge base
- Documents per category
- Bot version and environment

---

## 🎬 Quick Start for Demo

### Preparation Phase:
```
/addknowledge utenze Contratto luce Enel, 3kW, scade 31/12/2025
/addknowledge utenze Contratto gas ENI, scade 30/06/2026
/addknowledge casa Caldaia Vaillant installata 2020, revisione annuale obbligatoria
/addknowledge pulizia Pavimento parquet: solo panni umidi, no prodotti chimici
/addknowledge manutenzione Filtri condizionatore: sostituire ogni 3 mesi
```

### Demo Phase:
Now ask questions and show how bot uses this knowledge!

```
"Quando scade il contratto della luce?"
"Come pulisco il parquet?"
"Quando devo fare la revisione caldaia?"
```

---

## ⚙️ Behind the Scenes

When you add knowledge:
1. Text is converted to **embeddings** (vectors)
2. Stored in **ChromaDB** with category metadata
3. Indexed for **semantic search**
4. Retrieved when relevant to questions
5. Used to **augment LLM responses**

Your bot gets smarter with every addition! 🧠

---

## 📊 Storage

- Each knowledge item: ~1-2 KB
- Stored permanently in `chroma_db/`
- Survives bot restarts
- Can add thousands of items

---

## 🚫 Limitations

- Minimum 10 characters
- No multimedia (images, videos)
- Text only for `/addknowledge`
- PDFs processed as text

---

## ✅ Best Practices for Your Demo

1. **Pre-load key information** before demo
2. **Show live addition** during presentation
3. **Ask question before/after** to show learning
4. **Use categories** for organization
5. **Keep entries clear** and specific

---

## 🎯 Commands Summary

| Command | What it Does |
|---------|-------------|
| `/addknowledge text` | Add knowledge (general category) |
| `/addknowledge category text` | Add with specific category |
| `/stats` | See knowledge base stats |
| `/info` | Bot capabilities info |
| `/help` | All commands |
| Send PDF | Add document knowledge |

---

**Your bot can now learn from text, PDFs, and the web interface! 🚀📚**

FROM python:3.11-slim

WORKDIR /app

# Installa dipendenze sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia codice
COPY . .

# Crea cartella per ChromaDB
RUN mkdir -p chroma_db

# Avvia bot
CMD ["python", "main.py"]
```

**`.dockerignore`**
```
__pycache__/
*.pyc
.env
.env.example
chroma_db/
venv/
.git/
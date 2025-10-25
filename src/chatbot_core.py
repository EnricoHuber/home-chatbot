import os
import json
import chromadb
from groq import AsyncGroq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from datetime import datetime
from typing import Dict, List

load_dotenv()

class HomeChatbot:
    def __init__(self, config_path: str = "./configs/test_small_model.json"):
        """Inizializza il chatbot in base al file di configurazione"""
        self.config = self.load_config(config_path)
        self.llm_config = self.config.get("llm", {})
        self.rag_config = self.config.get("rag", {})
        self.verbose = self.config.get("logging", {}).get("verbose", False)

        if self.verbose:
            print(f"⚙️ Config caricata da {config_path}")

        self.setup_llm()
        if self.rag_config.get("enabled", True):
            self.setup_rag()
            self.load_base_knowledge()

    def load_config(self, path: str) -> Dict:
        """Carica configurazione da file JSON"""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Errore nel caricamento del file di config: {e}")

    # ==== LLM SETUP ====
    def setup_llm(self):
        provider = self.llm_config.get("provider", "groq").lower()
        if provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("⚠️ Mancante GROQ_API_KEY nelle variabili d'ambiente")
            self.llm_client = AsyncGroq(api_key=api_key)
        else:
            raise NotImplementedError(f"Provider LLM '{provider}' non supportato")

    # ==== RAG SETUP ====
    def setup_rag(self):
        path = self.rag_config.get("chroma_path", "./chroma_db")
        os.makedirs(path, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(path=path)
        self.collection = self.chroma_client.get_or_create_collection(
            self.rag_config.get("collection_name", "default_collection")
        )

        model_name = self.rag_config.get("embedding_model", "all-MiniLM-L6-v2")
        if self.verbose:
            print(f"📥 Caricamento modello embeddings: {model_name}")
        self.embedder = SentenceTransformer(model_name)
        if self.verbose:
            print("✅ Modello embedding caricato!")

    # ==== KNOWLEDGE BASE ====
    def load_base_knowledge(self):
        if self.collection.count() == 0:
            base_knowledge = [
                ("Pulizia: bicarbonato e aceto per il forno.", "pulizia"),
                ("Pulizia: multiuso naturale con aceto e limone.", "pulizia"),
                ("Utenze: verifica le bollette mensilmente.", "utenze"),
            ]
            for i, (text, category) in enumerate(base_knowledge):
                self.add_knowledge(text, category)
            if self.verbose:
                print(f"✅ Aggiunte {len(base_knowledge)} conoscenze base")

    def add_knowledge(self, content: str, category: str = "generale") -> str:
        doc_id = f"{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.collection.count()}"
        embedding = self.embedder.encode(content).tolist()
        self.collection.add(
            documents=[content],
            embeddings=[embedding],
            metadatas=[{"category": category}],
            ids=[doc_id]
        )
        return doc_id

    # ==== QUERY + LLM ====
    def search_knowledge(self, query: str, n_results: int = 3) -> List[Dict]:
        query_embedding = self.embedder.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, self.collection.count())
        )
        knowledge_list = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                knowledge_list.append({
                    "content": doc,
                    "category": results["metadatas"][0][i].get("category", "generale")
                })
        return knowledge_list

    async def get_response(self, user_message: str, user_id: int) -> str:
        """Genera risposta con o senza RAG"""
        
        # 1️⃣ Se RAG disabilitato nel config
        if not self.rag_config.get("enabled", True):
            prompt = f"""Sei un assistente domestico esperto e amichevole.
    Rispondi in modo pratico, naturale e utile alla domanda seguente.

    DOMANDA UTENTE: {user_message}"""
        else:
            # 2️⃣ RAG attivo → cerca conoscenze
            try:
                relevant_knowledge = self.search_knowledge(user_message, n_results=3)
            except Exception as e:
                relevant_knowledge = []
                print(f"⚠️ Errore durante la ricerca conoscenze: {e}")
            
            if relevant_knowledge:
                context = "\n".join([f"[{k['category'].upper()}] {k['content']}" for k in relevant_knowledge])
                context_intro = "Ecco informazioni rilevanti dalla tua knowledge base:"
            else:
                context = "Nessuna informazione specifica trovata."
                context_intro = "Non ho informazioni specifiche, ma posso aiutarti con la mia conoscenza generale:"
            
            prompt = f"""Sei un assistente domestico esperto e amichevole.

    {context_intro}
    {context}

    DOMANDA UTENTE: {user_message}

    Rispondi in italiano in modo pratico, dettagliato e amichevole. Se usi informazioni dalla knowledge base, incorporale naturalmente nella risposta."""

        # 3️⃣ Chiamata LLM
        try:
            response = await self.llm_client.chat.completions.create(
                model=self.llm_config.get("model"),
                messages=[{"role": "user", "content": prompt}],
                temperature=self.llm_config.get("temperature", 0.7),
                max_tokens=self.llm_config.get("max_tokens", 500)
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"⚠️ Errore durante la generazione: {str(e)[:200]}"

    def get_stats(self) -> Dict:
        """Statistiche conoscenze"""
        return {
            "total_docs": self.collection.count(),
            "categories": list(set([m.get('category', 'generale')
                for m in self.collection.get()['metadatas']]))
        }

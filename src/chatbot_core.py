# chatbot_core.py - versione con RAG
import os
from groq import AsyncGroq
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from datetime import datetime

load_dotenv()

class HomeChatbot:
    def __init__(self):
        """Inizializza LLM + RAG"""
        self.groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        
        # Setup RAG
        self.setup_rag()
        self.load_base_knowledge()
    
    def setup_rag(self):
        """Inizializza il database vettoriale"""
        os.makedirs("chroma_db", exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_or_create_collection("home_assistant")
        
        # Modello per embeddings (scarica automaticamente al primo uso)
        print("📥 Caricamento modello embeddings...")
        self.embedder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("✅ Modello caricato!")
    
    def load_base_knowledge(self):
        """Carica conoscenze iniziali se DB vuoto"""
        if self.collection.count() == 0:
            print("📚 Caricamento conoscenze di base...")
            base_knowledge = [
                ("Pulizia: Per pulire il forno naturalmente usa bicarbonato e aceto. Spalma pasta di bicarbonato, lascia 12 ore, spruzza aceto e rimuovi.", "pulizia"),
                ("Pulizia: Detergente multiuso naturale: 500ml acqua + 250ml aceto + sapone Marsiglia + limone.", "pulizia"),
                ("Utenze: Controlla le bollette mensilmente e verifica scadenze contratti 2 mesi prima.", "utenze"),
            ]
            
            for i, (text, category) in enumerate(base_knowledge):
                self.add_knowledge(text, category)
            print(f"✅ Aggiunte {len(base_knowledge)} conoscenze base")
    
    def add_knowledge(self, content: str, category: str = "generale") -> str:
        """Aggiunge conoscenza al database"""
        doc_id = f"{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.collection.count()}"
        
        # Crea embedding
        embedding = self.embedder.encode(content).tolist()
        
        # Salva nel database
        self.collection.add(
            documents=[content],
            embeddings=[embedding],
            metadatas=[{"category": category, "timestamp": datetime.now().isoformat()}],
            ids=[doc_id]
        )
        
        return doc_id
    
    def search_knowledge(self, query: str, n_results: int = 3) -> List[Dict]:
        """Cerca conoscenze rilevanti"""
        query_embedding = self.embedder.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, self.collection.count())
        )
        
        # Formatta risultati
        knowledge_list = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                knowledge_list.append({
                    'content': doc,
                    'category': results['metadatas'][0][i].get('category', 'generale')
                })
        
        return knowledge_list
    
    async def get_response(self, user_message: str, user_id: int) -> str:
        """Genera risposta usando RAG + LLM"""
        
        # 1. Cerca conoscenze rilevanti
        relevant_knowledge = self.search_knowledge(user_message, n_results=3)
        
        # 2. Costruisci contesto
        if relevant_knowledge:
            context = "\n".join([f"[{k['category'].upper()}] {k['content']}" for k in relevant_knowledge])
            context_intro = "Ecco informazioni rilevanti dalla tua knowledge base:"
        else:
            context = "Nessuna informazione specifica trovata."
            context_intro = "Non ho informazioni specifiche, ma posso aiutarti con la mia conoscenza generale:"
        
        # 3. Prompt migliorato
        prompt = f"""Sei un assistente domestico esperto e amichevole.

{context_intro}
{context}

DOMANDA UTENTE: {user_message}

Rispondi in italiano in modo pratico, dettagliato e amichevole. Se usi informazioni dalla knowledge base, incorporale naturalmente nella risposta."""

        try:
            response = await self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            return f"⚠️ Errore: {str(e)[:100]}"
    
    def get_stats(self) -> Dict:
        """Statistiche database"""
        return {
            "total_docs": self.collection.count(),
            "categories": list(set([m.get('category', 'generale') for m in self.collection.get()['metadatas']]))
        }
"""
Core chatbot functionality with improved architecture
"""
import os
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

import chromadb
from groq import AsyncGroq
from sentence_transformers import SentenceTransformer

from utils.config_manager import AppConfig
from utils.logger import LoggerMixin, log_performance
from utils.helpers import (
    generate_document_id, 
    MemoryCache, 
    retry_async,
    create_error_response,
    create_success_response
)


class LLMProvider(LoggerMixin):
    """LLM Provider interface"""
    
    def __init__(self, config: AppConfig):
        self.config = config.llm
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        """Setup LLM client based on provider"""
        if self.config.provider.lower() == "groq":
            api_key = os.getenv(self.config.api_key_env)
            if not api_key:
                raise ValueError(f"Missing {self.config.api_key_env} environment variable")
            
            self.client = AsyncGroq(api_key=api_key)
            self.log_success(f"Groq client initialized with model: {self.config.model}")
        else:
            raise NotImplementedError(f"Provider '{self.config.provider}' not supported")
    
    @log_performance(logging.getLogger("LLMProvider"))
    async def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate response using LLM"""
        try:
            response = await retry_async(
                lambda: self.client.chat.completions.create(
                    model=self.config.model,
                    messages=messages,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
            )
            
            content = response.choices[0].message.content.strip()
            self.log_debug(f"Generated response: {len(content)} characters")
            return content
            
        except Exception as e:
            self.log_error(f"Error generating response: {e}", e)
            return f"⚠️ Error generating response: {str(e)[:200]}"


class RAGSystem(LoggerMixin):
    """RAG (Retrieval-Augmented Generation) System"""
    
    def __init__(self, config: AppConfig):
        self.config = config.rag
        self.cache = MemoryCache(default_ttl=300)  # 5 minutes cache
        
        if self.config.enabled:
            self._setup_rag()
        else:
            self.log_info("RAG system disabled")
    
    def _setup_rag(self):
        """Setup RAG components"""
        try:
            # Ensure ChromaDB path exists
            os.makedirs(self.config.chroma_path, exist_ok=True)
            
            # Initialize ChromaDB
            self.chroma_client = chromadb.PersistentClient(path=self.config.chroma_path)
            self.collection = self.chroma_client.get_or_create_collection(
                name=self.config.collection_name
            )
            
            # Initialize embedding model
            self.log_info(f"Loading embedding model: {self.config.embedding_model}")
            self.embedder = SentenceTransformer(self.config.embedding_model)
            
            self.log_success("RAG system initialized successfully")
            self._load_base_knowledge()
            
        except Exception as e:
            self.log_error(f"Failed to setup RAG system: {e}", e)
            raise
    
    def _load_base_knowledge(self):
        """Load base knowledge if collection is empty"""
        if not self.config.enabled:
            return
            
        if self.collection.count() == 0:
            base_knowledge = [
                ("Per pulire il forno naturalmente, usa bicarbonato di sodio e aceto. Crea una pasta con bicarbonato e acqua, applicala nel forno, lascia agire, poi spruzza aceto e pulisci.", "pulizia"),
                ("Multiuso naturale: mescola parti uguali di aceto bianco e acqua, aggiungi alcune gocce di olio essenziale di limone. Ottimo per superfici e vetri.", "pulizia"),
                ("Per rimuovere il calcare dai rubinetti, immergi un panno nell'aceto bianco e avvolgilo intorno al rubinetto. Lascia agire 30 minuti, poi strofina e risciacqua.", "pulizia"),
                ("Controlla le bollette di luce e gas ogni mese per verificare consumi anomali. Conserva sempre le fatture per almeno 5 anni.", "utenze"),
                ("Per risparmiare energia, usa lampadine LED, spegni sempre le luci quando esci, e regola il termostato a 19-20°C in inverno.", "utenze"),
                ("Il contratto di fornitura elettrica può essere cambiato gratuitamente. Confronta le offerte almeno una volta all'anno.", "utenze"),
                ("Per sbloccare scarichi intasati, versa bicarbonato seguito da aceto caldo. Copri lo scarico per 15 minuti, poi sciacqua con acqua bollente.", "manutenzione"),
                ("Pulisci i filtri del condizionatore ogni 2-3 mesi per mantenere l'efficienza e la qualità dell'aria.", "manutenzione"),
                ("Per eliminare odori dal frigorifero, posiziona una ciotola di bicarbonato aperta all'interno e cambiala ogni 3 mesi.", "casa"),
                ("Le piante d'appartamento come pothos e sansevieria purificano l'aria naturalmente e sono facili da curare.", "casa")
            ]
            
            for text, category in base_knowledge:
                self.add_knowledge(text, category)
            
            self.log_success(f"Added {len(base_knowledge)} base knowledge items")
    
    def add_knowledge(self, content: str, category: str = "generale", metadata: Optional[Dict] = None) -> str:
        """Add knowledge to the database"""
        if not self.config.enabled:
            self.log_warning("RAG system disabled, cannot add knowledge")
            return ""
        
        try:
            doc_id = generate_document_id(content, category)
            embedding = self.embedder.encode(content).tolist()
            
            doc_metadata = {"category": category, "timestamp": datetime.now().isoformat()}
            if metadata:
                doc_metadata.update(metadata)
            
            self.collection.add(
                documents=[content],
                embeddings=[embedding],
                metadatas=[doc_metadata],
                ids=[doc_id]
            )
            
            # Clear cache as new knowledge was added
            self.cache.clear()
            
            self.log_debug(f"Added knowledge: {doc_id}")
            return doc_id
            
        except Exception as e:
            self.log_error(f"Error adding knowledge: {e}", e)
            return ""
    
    def search_knowledge(self, query: str, n_results: Optional[int] = None) -> List[Dict]:
        """Search knowledge base"""
        if not self.config.enabled:
            return []
        
        if n_results is None:
            n_results = self.config.max_search_results
        
        # Check cache first
        cache_key = f"search_{hash(query)}_{n_results}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            self.log_debug(f"Cache hit for query: {query[:50]}...")
            return cached_result
        
        try:
            query_embedding = self.embedder.encode(query).tolist()
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(n_results, max(1, self.collection.count()))
            )
            
            knowledge_list = []
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    distance = results["distances"][0][i] if results.get("distances") else 0
                    similarity = 1 - distance  # Convert distance to similarity
                    
                    if similarity >= self.config.similarity_threshold:
                        knowledge_list.append({
                            "content": doc,
                            "category": results["metadatas"][0][i].get("category", "generale"),
                            "similarity": similarity,
                            "id": results["ids"][0][i]
                        })
            
            # Cache the results
            self.cache.set(cache_key, knowledge_list)
            
            self.log_debug(f"Found {len(knowledge_list)} relevant knowledge items")
            return knowledge_list
            
        except Exception as e:
            self.log_error(f"Error searching knowledge: {e}", e)
            return []
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        if not self.config.enabled:
            return {"enabled": False}
        
        try:
            all_data = self.collection.get()
            categories = {}
            
            for metadata in all_data.get("metadatas", []):
                category = metadata.get("category", "generale")
                categories[category] = categories.get(category, 0) + 1
            
            return {
                "enabled": True,
                "total_documents": self.collection.count(),
                "categories": categories,
                "collection_name": self.config.collection_name
            }
            
        except Exception as e:
            self.log_error(f"Error getting stats: {e}", e)
            return {"enabled": True, "error": str(e)}


class HomeChatbot(LoggerMixin):
    """Main Home Assistant Chatbot"""
    
    def __init__(self, config: AppConfig):
        self.config = config
        self.log_info(f"Initializing {config.app_name} v{config.version}")
        
        # Initialize components
        self.llm_provider = LLMProvider(config)
        self.rag_system = RAGSystem(config)
        
        # Initialize cache for responses
        self.response_cache = MemoryCache(default_ttl=600)  # 10 minutes
        
        self.log_success("Chatbot initialized successfully")
    
    async def get_response(self, user_message: str, user_id: Optional[str] = None, use_cache: bool = True) -> str:
        """Generate response to user message"""
        self.log_method_call("get_response", 
                           message_length=len(user_message), 
                           user_id=user_id)
        
        # Check cache first
        if use_cache:
            cache_key = f"response_{hash(user_message)}"
            cached_response = self.response_cache.get(cache_key)
            if cached_response:
                self.log_debug("Using cached response")
                return cached_response
        
        try:
            # Search for relevant knowledge
            relevant_knowledge = []
            if self.rag_system.config.enabled:
                relevant_knowledge = self.rag_system.search_knowledge(user_message)
            
            # Build prompt
            prompt = self._build_prompt(user_message, relevant_knowledge)
            
            # Generate response
            messages = [{"role": "user", "content": prompt}]
            response = await self.llm_provider.generate_response(messages)
            
            # Cache the response
            if use_cache:
                self.response_cache.set(cache_key, response)
            
            self.log_success(f"Generated response for user {user_id}")
            return response
            
        except Exception as e:
            self.log_error(f"Error generating response: {e}", e)
            return "⚠️ Mi dispiace, ho avuto un problema tecnico. Riprova tra poco!"
    
    def _build_prompt(self, user_message: str, relevant_knowledge: List[Dict]) -> str:
        """Build prompt for LLM"""
        if not relevant_knowledge:
            return f"""Sei un assistente domestico esperto e amichevole specializzato in:
- Consigli per la pulizia naturale della casa
- Gestione delle utenze domestiche
- Manutenzione casalinga
- Organizzazione domestica

Rispondi in italiano in modo pratico, dettagliato e amichevole.

DOMANDA UTENTE: {user_message}"""
        
        # Build context from knowledge
        context_parts = []
        for knowledge in relevant_knowledge:
            category = knowledge['category'].upper()
            content = knowledge['content']
            context_parts.append(f"[{category}] {content}")
        
        context = "\n".join(context_parts)
        
        return f"""Sei un assistente domestico esperto e amichevole specializzato in consigli per la casa.

Ecco informazioni rilevanti dalla tua base di conoscenze:
{context}

DOMANDA UTENTE: {user_message}

Rispondi in italiano incorporando naturalmente le informazioni della knowledge base quando rilevanti. 
Sii pratico, dettagliato e amichevole. Se le informazioni della knowledge base non sono sufficienti, 
integra con la tua conoscenza generale sui temi domestici."""
    
    async def add_document(self, file_path: str, category: str = "documento") -> bool:
        """Add document to knowledge base"""
        try:
            # This would normally process the document
            # For now, just add a placeholder
            content = f"Documento caricato: {os.path.basename(file_path)}"
            doc_id = self.rag_system.add_knowledge(content, category)
            
            self.log_success(f"Document added: {file_path}")
            return bool(doc_id)
            
        except Exception as e:
            self.log_error(f"Error adding document: {e}", e)
            return False
    
    def get_stats(self) -> Dict:
        """Get chatbot statistics"""
        rag_stats = self.rag_system.get_stats()
        
        return {
            "app_name": self.config.app_name,
            "version": self.config.version,
            "environment": self.config.environment,
            "rag": rag_stats,
            "cache_size": len(self.response_cache.cache),
            "uptime": "N/A"  # Would track actual uptime
        }
    
    def clear_cache(self):
        """Clear all caches"""
        self.response_cache.clear()
        self.rag_system.cache.clear()
        self.log_info("All caches cleared")
"""
Supabase Storage Backend for RAG Knowledge Base
Uses PostgreSQL with pgvector for persistent, scalable vector storage
"""
import os
from typing import List, Dict, Optional, Any
from datetime import datetime
import hashlib

from supabase import create_client, Client
from sentence_transformers import SentenceTransformer

from utils.logger import LoggerMixin
from utils.helpers import generate_document_id


class SupabaseStorage(LoggerMixin):
    """
    Supabase-based vector storage using pgvector
    
    Features:
    - Persistent storage (survives restarts)
    - Unlimited scalability (free tier: 500MB)
    - Web UI for management
    - SQL-based queries
    - Automatic backups
    """
    
    def __init__(self, config, embedder: SentenceTransformer):
        """
        Initialize Supabase storage
        
        Args:
            config: RAG configuration with supabase settings
            embedder: SentenceTransformer model for embeddings
        """
        self.config = config
        self.embedder = embedder
        self.client: Optional[Client] = None
        self.table_name = "knowledge_base"
        
        self._connect()
        self._ensure_table_exists()
    
    def _connect(self):
        """Connect to Supabase"""
        try:
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")
            
            if not supabase_url or not supabase_key:
                raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables")
            
            self.client = create_client(supabase_url, supabase_key)
            self.log_success(f"Connected to Supabase: {supabase_url[:30]}...")
            
        except Exception as e:
            self.log_error(f"Failed to connect to Supabase: {e}", e)
            raise
    
    def _ensure_table_exists(self):
        """
        Ensure the knowledge_base table exists with pgvector extension
        
        Note: You need to run this SQL in Supabase SQL Editor ONCE:
        
        -- Enable pgvector extension
        CREATE EXTENSION IF NOT EXISTS vector;
        
        -- Create knowledge_base table
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'generale',
            embedding vector(384),  -- Adjust dimension based on your model
            metadata JSONB DEFAULT '{}',
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        
        -- Create index for vector similarity search
        CREATE INDEX IF NOT EXISTS knowledge_base_embedding_idx 
        ON knowledge_base USING ivfflat (embedding vector_cosine_ops);
        
        -- Create index for category filtering
        CREATE INDEX IF NOT EXISTS knowledge_base_category_idx 
        ON knowledge_base(category);
        """
        try:
            # Try to query the table to check if it exists
            result = self.client.table(self.table_name).select("id").limit(1).execute()
            self.log_success(f"Table '{self.table_name}' exists and is accessible")
        except Exception as e:
            self.log_warning(f"Table check failed: {e}")
            self.log_warning("Please run the SQL setup script in Supabase SQL Editor (see SUPABASE_SETUP.md)")
    
    def count(self) -> int:
        """Get total number of knowledge items"""
        try:
            result = self.client.table(self.table_name).select("id", count="exact").execute()
            count = result.count if hasattr(result, 'count') else 0
            return count
        except Exception as e:
            self.log_error(f"Error counting knowledge items: {e}")
            return 0
    
    def add_knowledge(self, content: str, category: str = "generale", metadata: Optional[Dict] = None) -> str:
        """
        Add knowledge to Supabase
        
        Args:
            content: The knowledge text
            category: Category (pulizia, utenze, manutenzione, casa, generale)
            metadata: Additional metadata
        
        Returns:
            Document ID
        """
        try:
            # Generate document ID
            doc_id = generate_document_id(content, category)
            
            # Generate embedding
            embedding = self.embedder.encode(content).tolist()
            
            # Prepare metadata
            doc_metadata = metadata or {}
            doc_metadata["category"] = category
            doc_metadata["added_at"] = datetime.now().isoformat()
            
            # Insert into Supabase
            data = {
                "id": doc_id,
                "content": content,
                "category": category,
                "embedding": embedding,
                "metadata": doc_metadata
            }
            
            # Upsert (insert or update if exists)
            result = self.client.table(self.table_name).upsert(data).execute()
            
            self.log_debug(f"Added knowledge: {doc_id} (category: {category})")
            return doc_id
            
        except Exception as e:
            self.log_error(f"Error adding knowledge: {e}", e)
            return ""
    
    def search_knowledge(self, query: str, n_results: int = 3, category: Optional[str] = None) -> List[Dict]:
        """
        Search knowledge using vector similarity
        
        Args:
            query: Search query
            n_results: Number of results to return
            category: Optional category filter
        
        Returns:
            List of knowledge items with similarity scores
        """
        try:
            # Generate query embedding
            query_embedding = self.embedder.encode(query).tolist()
            
            # Call Supabase RPC function for vector similarity search
            # Note: You need to create this function in Supabase (see SUPABASE_SETUP.md)
            rpc_params = {
                "query_embedding": query_embedding,
                "match_count": n_results
            }
            
            if category:
                rpc_params["filter_category"] = category
            
            result = self.client.rpc("match_knowledge", rpc_params).execute()
            
            # Format results
            knowledge_list = []
            if result.data:
                for item in result.data:
                    knowledge_list.append({
                        "content": item["content"],
                        "category": item["category"],
                        "similarity": item.get("similarity", 0),
                        "metadata": item.get("metadata", {})
                    })
            
            self.log_debug(f"Found {len(knowledge_list)} knowledge items for query: {query[:50]}...")
            return knowledge_list
            
        except Exception as e:
            self.log_error(f"Error searching knowledge: {e}", e)
            # Fallback to basic text search if RPC fails
            return self._fallback_search(query, n_results, category)
    
    def _fallback_search(self, query: str, n_results: int = 3, category: Optional[str] = None) -> List[Dict]:
        """Fallback to basic text search if vector search fails"""
        try:
            self.log_warning("Using fallback text search (vector search unavailable)")
            
            # Basic text search using ilike (case-insensitive LIKE)
            query_builder = self.client.table(self.table_name).select("*")
            
            if category:
                query_builder = query_builder.eq("category", category)
            
            # Search in content
            query_builder = query_builder.ilike("content", f"%{query}%")
            query_builder = query_builder.limit(n_results)
            
            result = query_builder.execute()
            
            knowledge_list = []
            if result.data:
                for item in result.data:
                    knowledge_list.append({
                        "content": item["content"],
                        "category": item.get("category", "generale"),
                        "similarity": 0.5,  # Dummy score
                        "metadata": item.get("metadata", {})
                    })
            
            return knowledge_list
            
        except Exception as e:
            self.log_error(f"Fallback search failed: {e}", e)
            return []
    
    def delete_knowledge(self, doc_id: str) -> bool:
        """
        Delete knowledge by ID
        
        Args:
            doc_id: Document ID to delete
        
        Returns:
            True if successful
        """
        try:
            result = self.client.table(self.table_name).delete().eq("id", doc_id).execute()
            self.log_info(f"Deleted knowledge: {doc_id}")
            return True
        except Exception as e:
            self.log_error(f"Error deleting knowledge: {e}", e)
            return False
    
    def get_all_categories(self) -> List[str]:
        """Get list of all categories"""
        try:
            result = self.client.table(self.table_name).select("category").execute()
            categories = list(set(item["category"] for item in result.data if "category" in item))
            return categories
        except Exception as e:
            self.log_error(f"Error getting categories: {e}", e)
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        try:
            # Total count
            total = self.count()
            
            # Count by category
            categories = {}
            result = self.client.table(self.table_name).select("category").execute()
            for item in result.data:
                cat = item.get("category", "generale")
                categories[cat] = categories.get(cat, 0) + 1
            
            return {
                "total": total,
                "by_category": categories,
                "storage_backend": "Supabase (PostgreSQL + pgvector)"
            }
        except Exception as e:
            self.log_error(f"Error getting stats: {e}", e)
            return {"total": 0, "by_category": {}, "storage_backend": "Supabase (error)"}
    
    def clear_all(self) -> bool:
        """Clear all knowledge (use with caution!)"""
        try:
            result = self.client.table(self.table_name).delete().neq("id", "").execute()
            self.log_warning("Cleared all knowledge from Supabase")
            return True
        except Exception as e:
            self.log_error(f"Error clearing knowledge: {e}", e)
            return False

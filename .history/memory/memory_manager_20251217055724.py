"""
Memory Management System
Handles conversation memory, vector storage, and context retention
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import chromadb
from chromadb.config import Settings
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain_community.chat_models import ChatOllama
import json

from config import settings


class MemoryType:
    """Memory type constants"""
    CONVERSATION = "conversation"
    SUMMARY = "summary"
    VECTOR = "vector"
    FACT = "fact"


class MemoryManager:
    """
    Manages different types of memory for the multi-agent system
    - Conversation buffer: Short-term conversation history
    - Summary memory: Condensed conversation summaries
    - Vector memory: Semantic search over past interactions
    - Fact memory: Extracted facts and entities
    """
    
    def __init__(self):
        self.llm = ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            temperature=0
        )
        
        # Initialize embeddings (free local embeddings)
        self.embeddings = OllamaEmbeddings(
            base_url=settings.ollama_base_url,
            model=settings.ollama_embedding_model
        )
        
        # Initialize ChromaDB for vector storage
        self.chroma_client = chromadb.Client(Settings(
            persist_directory=settings.chroma_persist_dir,
            anonymized_telemetry=False
        ))
        
        # Memory stores per user
        self._conversation_memories: Dict[str, ConversationBufferMemory] = {}
        self._summary_memories: Dict[str, ConversationSummaryMemory] = {}
        self._vector_stores: Dict[str, Chroma] = {}
        self._fact_stores: Dict[str, List[Dict[str, Any]]] = {}
    
    def get_conversation_memory(self, user_id: str) -> ConversationBufferMemory:
        """Get or create conversation buffer memory for user"""
        if user_id not in self._conversation_memories:
            self._conversation_memories[user_id] = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                max_token_limit=2000
            )
        return self._conversation_memories[user_id]
    
    def get_summary_memory(self, user_id: str) -> ConversationSummaryMemory:
        """Get or create summary memory for user"""
        if user_id not in self._summary_memories:
            self._summary_memories[user_id] = ConversationSummaryMemory(
                llm=self.llm,
                memory_key="conversation_summary",
                return_messages=True
            )
        return self._summary_memories[user_id]
    
    def get_vector_store(self, user_id: str) -> Chroma:
        """Get or create vector store for user"""
        if user_id not in self._vector_stores:
            collection_name = f"user_{user_id}_memory"
            self._vector_stores[user_id] = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                client=self.chroma_client,
                persist_directory=settings.chroma_persist_dir
            )
        return self._vector_stores[user_id]
    
    def add_interaction(
        self,
        user_id: str,
        user_message: str,
        assistant_message: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add interaction to all memory types"""
        # Add to conversation buffer
        conv_memory = self.get_conversation_memory(user_id)
        conv_memory.save_context(
            {"input": user_message},
            {"output": assistant_message}
        )
        
        # Add to summary memory
        summary_memory = self.get_summary_memory(user_id)
        summary_memory.save_context(
            {"input": user_message},
            {"output": assistant_message}
        )
        
        # Add to vector store
        vector_store = self.get_vector_store(user_id)
        doc_metadata = metadata or {}
        doc_metadata.update({
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "type": "interaction"
        })
        
        doc = Document(
            page_content=f"User: {user_message}\nAssistant: {assistant_message}",
            metadata=doc_metadata
        )
        vector_store.add_documents([doc])
    
    def add_fact(
        self,
        user_id: str,
        fact: str,
        source: str,
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Store extracted fact"""
        if user_id not in self._fact_stores:
            self._fact_stores[user_id] = []
        
        fact_entry = {
            "fact": fact,
            "source": source,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self._fact_stores[user_id].append(fact_entry)
        
        # Also add to vector store for semantic search
        vector_store = self.get_vector_store(user_id)
        doc = Document(
            page_content=fact,
            metadata={
                "user_id": user_id,
                "type": "fact",
                "source": source,
                "confidence": confidence,
                "timestamp": datetime.now().isoformat()
            }
        )
        vector_store.add_documents([doc])
    
    def search_memory(
        self,
        user_id: str,
        query: str,
        k: int = 5,
        filter_type: Optional[str] = None
    ) -> List[Document]:
        """Search vector memory"""
        vector_store = self.get_vector_store(user_id)
        
        search_kwargs = {"k": k}
        if filter_type:
            search_kwargs["filter"] = {"type": filter_type}
        
        results = vector_store.similarity_search(query, **search_kwargs)
        return results
    
    def get_conversation_context(self, user_id: str) -> str:
        """Get formatted conversation context"""
        conv_memory = self.get_conversation_memory(user_id)
        return conv_memory.load_memory_variables({}).get("chat_history", "")
    
    def get_summary_context(self, user_id: str) -> str:
        """Get conversation summary"""
        summary_memory = self.get_summary_memory(user_id)
        return summary_memory.load_memory_variables({}).get("conversation_summary", "")
    
    def get_facts(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent facts for user"""
        facts = self._fact_stores.get(user_id, [])
        # Sort by confidence and recency
        sorted_facts = sorted(
            facts,
            key=lambda x: (x["confidence"], x["timestamp"]),
            reverse=True
        )
        return sorted_facts[:limit]
    
    def clear_memory(self, user_id: str):
        """Clear all memory for user"""
        if user_id in self._conversation_memories:
            self._conversation_memories[user_id].clear()
        if user_id in self._summary_memories:
            self._summary_memories[user_id].clear()
        if user_id in self._fact_stores:
            self._fact_stores[user_id] = []
        # Note: Vector store persists, but can be cleared if needed
    
    def get_memory_snapshot(self, user_id: str) -> Dict[str, Any]:
        """Get complete memory snapshot for user"""
        return {
            "conversation": self.get_conversation_context(user_id),
            "summary": self.get_summary_context(user_id),
            "facts": self.get_facts(user_id),
            "timestamp": datetime.now().isoformat()
        }


# Global memory manager instance
memory_manager = MemoryManager()

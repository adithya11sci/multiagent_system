"""
RAG System - Retrieval Augmented Generation
Manages vector store and retrieval for passenger intelligence
"""
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import json
import os
import numpy as np
import pickle
from config import VECTOR_STORE_PATH, EMBEDDING_MODEL, RAG_DATA_SOURCES

class RAGSystem:
    """
    RAG system for passenger intelligence
    Uses in-memory vector storage with FAISS fallback
    """
    
    def __init__(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        
        # Initialize in-memory storage
        os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
        
        # Storage dictionaries
        self.documents = {
            "timetables": [],
            "policies": [],
            "refund_rules": [],
            "route_maps": []
        }
        self.embeddings = {
            "timetables": [],
            "policies": [],
            "refund_rules": [],
            "route_maps": []
        }
        
    def initialize_data(self):
        """
        Load and index initial data from RAG data sources
        """
        # Load timetables
        if os.path.exists(RAG_DATA_SOURCES["timetables"]):
            with open(RAG_DATA_SOURCES["timetables"], 'r') as f:
                timetables = json.load(f)
                self._index_documents(timetables, "timetables")
        
        # Load policies
        if os.path.exists(RAG_DATA_SOURCES["policies"]):
            with open(RAG_DATA_SOURCES["policies"], 'r') as f:
                policies = f.read().split('\n\n')
                policy_docs = [{"content": p, "type": "policy"} for p in policies if p.strip()]
                self._index_documents(policy_docs, "policies")
        
                refund_docs = [{"content": r, "type": "refund"} for r in refund_rules if r.strip()]
                self._index_documents(refund_docs, "refund_rules")
        
        # Load route maps
        if os.path.exists(RAG_DATA_SOURCES["route_maps"]):
            with open(RAG_DATA_SOURCES["route_maps"], 'r') as f:
                route_maps = json.load(f)
                self._index_documents(route_maps, "route_maps")
        
        print(f"✅ Indexed data: {sum(len(docs) for docs in self.documents.values())} documents")
    
    def _index_documents(self, documents: List[Dict[str, Any]], collection_name: str):
        """Index documents into a collection"""
        if not documents:
            return
        
        for doc in documents:
            if isinstance(doc, dict):
                text = doc.get("content", str(doc))
            else:
                text = str(doc)
            
            # Generate embedding
            embedding = self.embedding_model.encode([text])[0]
            
            # Store
            self.documents[collection_name].append(doc)
            self.embeddings[collection_name].append(embedding)
    
    def retrieve(self, query: str, top_k: int = 5, 
                collection_name: str = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents using cosine similarity
        
        Args:
            query: Search query
            top_k: Number of results to return
            collection_name: Specific collection to search (None = search all)
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0]
        
        # Determine which collections to search
        if collection_name:
            collections = [collection_name]
        else:
            collections = ["timetables", "policies", "refund_rules", "route_maps"]
        
        all_results = []
        
        for coll_name in collections:
            if not self.embeddings[coll_name]:
                continue
            
            # Calculate cosine similarities
            embeddings_array = np.array(self.embeddings[coll_name])
            similarities = np.dot(embeddings_array, query_embedding) / (
                np.linalg.norm(embeddings_array, axis=1) * np.linalg.norm(query_embedding)
            )
            
            # Get top-k indices
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            # Format results
            for idx in top_indices:
                if similarities[idx] > 0.3:  # Similarity threshold
                    doc = self.documents[coll_name][idx]
                    all_results.append({
                        "content": doc.get("content", str(doc)) if isinstance(doc, dict) else str(doc),
                        "metadata": doc if isinstance(doc, dict) else {},
                        "similarity": float(similarities[idx]),
                        "source": coll_name
                    })
        
        # Sort by similarity (higher is better)
        all_results.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        
        return all_results[:top_k]
    
    def add_document(self, document: Dict[str, Any], collection_name: str):
        """Add a new document to a collection"""
        text = document.get("content", str(document))
        embedding = self.embedding_model.encode([text])[0]
        
        self.documents[collection_name].append(document)
        self.embeddings[collection_name].append(embedding)
    
    def search_by_metadata(self, collection_name: str, 
                          metadata_filter: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search documents by metadata filter"""
        results = []
        
        for doc in self.documents[collection_name]:
            if isinstance(doc, dict):
                # Check if all filter keys match
                if all(doc.get(k) == v for k, v in metadata_filter.items()):
                    results.append({
                        "content": doc.get("content", str(doc)),
                        "metadata": doc,
                        "source": collection_name
                    })
        
        return results


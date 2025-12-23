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
                            "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                            "distance": results["distances"][0][i] if results.get("distances") else 0,
                            "source": collection.name
                        })
            except Exception as e:
                print(f"Error querying collection {collection.name}: {e}")
        
        # Sort by distance (lower is better)
        all_results.sort(key=lambda x: x.get("distance", 999))
        
        return all_results[:top_k]
    
    def add_document(self, document: Dict[str, Any], collection_name: str):
        """
        Add a new document to a collection
        """
        collection = getattr(self, f"{collection_name}_collection")
        
        text = document.get("content", str(document))
        metadata = {k: v for k, v in document.items() if k != "content"}
        
        embedding = self.embedding_model.encode([text])[0].tolist()
        
        doc_id = f"{collection_name}_{collection.count()}"
        
        collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
    
    def search_by_metadata(self, collection_name: str, 
                          metadata_filter: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Search documents by metadata filter
        """
        collection = getattr(self, f"{collection_name}_collection")
        
        results = collection.get(
            where=metadata_filter
        )
        
        formatted_results = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"]):
                formatted_results.append({
                    "content": doc,
                    "metadata": results["metadatas"][i] if results["metadatas"] else {},
                    "source": collection.name
                })
        
        return formatted_results

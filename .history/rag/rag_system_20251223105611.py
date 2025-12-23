"""
RAG System - Retrieval Augmented Generation
Manages vector store and retrieval for passenger intelligence
"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import json
import os
from config import VECTOR_STORE_PATH, EMBEDDING_MODEL, RAG_DATA_SOURCES

class RAGSystem:
    """
    RAG system for passenger intelligence
    Uses ChromaDB for vector storage and retrieval
    """
    
    def __init__(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        
        # Initialize ChromaDB
        os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
        self.client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
        
        # Get or create collections
        self.timetables_collection = self.client.get_or_create_collection("timetables")
        self.policies_collection = self.client.get_or_create_collection("policies")
        self.refund_rules_collection = self.client.get_or_create_collection("refund_rules")
        self.route_maps_collection = self.client.get_or_create_collection("route_maps")
        
    def initialize_data(self):
        """
        Load and index initial data from RAG data sources
        """
        # Load timetables
        if os.path.exists(RAG_DATA_SOURCES["timetables"]):
            with open(RAG_DATA_SOURCES["timetables"], 'r') as f:
                timetables = json.load(f)
                self._index_documents(timetables, self.timetables_collection, "timetable")
        
        # Load policies
        if os.path.exists(RAG_DATA_SOURCES["policies"]):
            with open(RAG_DATA_SOURCES["policies"], 'r') as f:
                policies = f.read().split('\n\n')
                policy_docs = [{"content": p, "type": "policy"} for p in policies if p.strip()]
                self._index_documents(policy_docs, self.policies_collection, "policy")
        
        # Load refund rules
        if os.path.exists(RAG_DATA_SOURCES["refund_rules"]):
            with open(RAG_DATA_SOURCES["refund_rules"], 'r') as f:
                refund_rules = f.read().split('\n\n')
                refund_docs = [{"content": r, "type": "refund"} for r in refund_rules if r.strip()]
                self._index_documents(refund_docs, self.refund_rules_collection, "refund")
        
        # Load route maps
        if os.path.exists(RAG_DATA_SOURCES["route_maps"]):
            with open(RAG_DATA_SOURCES["route_maps"], 'r') as f:
                route_maps = json.load(f)
                self._index_documents(route_maps, self.route_maps_collection, "route")
    
    def _index_documents(self, documents: List[Dict[str, Any]], 
                        collection, doc_type: str):
        """
        Index documents into a collection
        """
        if not documents:
            return
        
        # Prepare documents for indexing
        texts = []
        metadatas = []
        ids = []
        
        for i, doc in enumerate(documents):
            if isinstance(doc, dict):
                text = doc.get("content", str(doc))
                metadata = {k: v for k, v in doc.items() if k != "content"}
            else:
                text = str(doc)
                metadata = {}
            
            metadata["type"] = doc_type
            
            texts.append(text)
            metadatas.append(metadata)
            ids.append(f"{doc_type}_{i}")
        
        # Generate embeddings
        embeddings = self.embedding_model.encode(texts).tolist()
        
        # Add to collection
        try:
            collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
        except Exception as e:
            print(f"Error indexing documents: {e}")
    
    def retrieve(self, query: str, top_k: int = 5, 
                collection_name: str = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Search query
            top_k: Number of results to return
            collection_name: Specific collection to search (None = search all)
            
        Returns:
            List of relevant documents with metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])[0].tolist()
        
        # Determine which collections to search
        if collection_name:
            collections = [getattr(self, f"{collection_name}_collection")]
        else:
            collections = [
                self.timetables_collection,
                self.policies_collection,
                self.refund_rules_collection,
                self.route_maps_collection
            ]
        
        all_results = []
        
        for collection in collections:
            try:
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k
                )
                
                # Format results
                if results["documents"] and results["documents"][0]:
                    for i, doc in enumerate(results["documents"][0]):
                        all_results.append({
                            "content": doc,
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

"""RAG pipeline implementation with Gemini embeddings and FAISS vector store."""

import os
import pickle
import numpy as np
from typing import List, Dict, Tuple
import google.generativeai as genai
import faiss
from config import *
from safety_validator import SafetyValidator


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline for court document queries."""
    
    def __init__(self, api_key: str):
        """Initialize RAG pipeline with Gemini API."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(MODEL_NAME)
        self.embeddings_cache = {}
        self.vector_store = None
        self.document_chunks = []
        self.safety_validator = SafetyValidator()
        
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings using Gemini embedding model."""
        try:
            embeddings = []
            
            for text in texts:
                # Check cache first
                if text in self.embeddings_cache:
                    embeddings.append(self.embeddings_cache[text])
                    continue
                
                # Generate embedding with retry logic
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        result = genai.embed_content(
                            model=EMBEDDING_MODEL,
                            content=text,
                            task_type="retrieval_document"
                        )
                        
                        embedding = np.array(result['embedding'])
                        embeddings.append(embedding)
                        self.embeddings_cache[text] = embedding
                        break
                        
                    except Exception as e:
                        print(f"Embedding attempt {attempt + 1} failed: {str(e)}")
                        if attempt == max_retries - 1:
                            # If all retries fail, create a dummy embedding
                            print("Creating dummy embedding for failed text")
                            dummy_embedding = np.random.normal(0, 1, 768)  # Standard embedding size
                            embeddings.append(dummy_embedding)
                            self.embeddings_cache[text] = dummy_embedding
            
            return np.array(embeddings)
        
        except Exception as e:
            print(f"Error generating embeddings: {str(e)}")
            return np.array([])
    
    def build_vector_store(self, document_chunks: List[Dict[str, str]]):
        """Build FAISS vector store from document chunks."""
        self.document_chunks = document_chunks
        
        if not document_chunks:
            print("No document chunks provided")
            return
        
        print("Generating embeddings for document chunks...")
        texts = [chunk['content'] for chunk in document_chunks]
        embeddings = self.generate_embeddings(texts)
        
        if embeddings.size == 0:
            print("Failed to generate embeddings")
            return
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.vector_store = faiss.IndexFlatIP(dimension)  # Inner product for similarity
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        self.vector_store.add(embeddings)
        
        print(f"Vector store built with {len(document_chunks)} chunks")
        
        # Save vector store and chunks
        self._save_vector_store()
    
    def _save_vector_store(self):
        """Save vector store and document chunks to disk."""
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.vector_store, os.path.join(VECTOR_DB_PATH, "index.faiss"))
        
        # Save document chunks
        with open(os.path.join(VECTOR_DB_PATH, "chunks.pkl"), "wb") as f:
            pickle.dump(self.document_chunks, f)
        
        print("Vector store saved successfully")
    
    def load_vector_store(self) -> bool:
        """Load existing vector store from disk."""
        try:
            index_path = os.path.join(VECTOR_DB_PATH, "index.faiss")
            chunks_path = os.path.join(VECTOR_DB_PATH, "chunks.pkl")
            
            if not (os.path.exists(index_path) and os.path.exists(chunks_path)):
                return False
            
            # Load FAISS index
            self.vector_store = faiss.read_index(index_path)
            
            # Load document chunks
            with open(chunks_path, "rb") as f:
                self.document_chunks = pickle.load(f)
            
            print(f"Vector store loaded with {len(self.document_chunks)} chunks")
            return True
        
        except Exception as e:
            print(f"Error loading vector store: {str(e)}")
            return False
    
    def retrieve_relevant_chunks(self, query: str, k: int = MAX_CHUNKS_RETRIEVED) -> List[Dict[str, str]]:
        """Retrieve most relevant document chunks for a query."""
        if not self.vector_store or not self.document_chunks:
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.generate_embeddings([query])
            if query_embedding.size == 0:
                return []
            
            # Normalize query embedding
            faiss.normalize_L2(query_embedding)
            
            # Search vector store
            scores, indices = self.vector_store.search(query_embedding, k)
            
            # Return relevant chunks with more lenient threshold
            relevant_chunks = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.document_chunks):
                    chunk = self.document_chunks[idx].copy()
                    chunk['similarity_score'] = float(score)
                    relevant_chunks.append(chunk)
                    print(f"Retrieved chunk with score {score:.3f}: {chunk['content'][:100]}...")
            
            # If no chunks meet threshold, return top chunks anyway
            if not relevant_chunks and len(scores[0]) > 0:
                print("No chunks met similarity threshold, returning top results anyway")
                for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                    if i >= 3:  # Limit to top 3
                        break
                    if idx < len(self.document_chunks):
                        chunk = self.document_chunks[idx].copy()
                        chunk['similarity_score'] = float(score)
                        relevant_chunks.append(chunk)
            
            return relevant_chunks
        
        except Exception as e:
            print(f"Error retrieving chunks: {str(e)}")
            return []
    
    def generate_response(self, query: str, retrieved_chunks: List[Dict[str, str]]) -> Tuple[str, List[str], List[str]]:
        """Generate response using retrieved chunks and Gemini with safety validation."""
        # First validate the query
        is_appropriate, safety_message = self.safety_validator.validate_query(query)
        if not is_appropriate:
            return safety_message, [], ["Safety validation"]
        
        if not retrieved_chunks:
            return "I don't have that information in the available court documents.", [], []
        
        # Prepare context from retrieved chunks
        context = "\n\n".join([
            f"Document: {chunk['source']}\nContent: {chunk['content']}"
            for chunk in retrieved_chunks
        ])
        
        # Create prompt with system instructions and context
        prompt = f"""{SYSTEM_PROMPT}

RETRIEVED COURT DOCUMENTS:
{context}

USER QUESTION: {query}

Based ONLY on the retrieved court documents above, provide a clear explanation of the court procedure or process. If the information is not in the documents, say you don't have that information."""
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                )
            )
            
            # Validate the generated response for safety
            is_safe, warnings, safe_response = self.safety_validator.validate_response(
                response.text, query
            )
            
            # Extract source documents
            sources = list(set([chunk['source'] for chunk in retrieved_chunks]))
            
            # Return the safe response and any warnings
            return safe_response, sources, warnings
        
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error processing your question.", [], [f"Generation error: {str(e)}"]
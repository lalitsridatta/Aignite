"""Simple RAG pipeline using text-based search as fallback when embeddings fail."""

import os
import pickle
import re
from typing import List, Dict, Tuple
import google.generativeai as genai
from config import *
from safety_validator import SafetyValidator


class SimpleRAGPipeline:
    """Simple RAG pipeline with text-based search fallback."""
    
    def __init__(self, api_key: str):
        """Initialize RAG pipeline with Gemini API."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(MODEL_NAME)
        self.document_chunks = []
        self.safety_validator = SafetyValidator()
        
    def build_text_index(self, document_chunks: List[Dict[str, str]]):
        """Build simple text-based index from document chunks."""
        self.document_chunks = document_chunks
        
        if not document_chunks:
            print("No document chunks provided")
            return
        
        print(f"Text index built with {len(document_chunks)} chunks")
        
        # Save chunks
        self._save_text_index()
    
    def _save_text_index(self):
        """Save document chunks to disk."""
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
        
        # Save document chunks
        with open(os.path.join(VECTOR_DB_PATH, "text_chunks.pkl"), "wb") as f:
            pickle.dump(self.document_chunks, f)
        
        print("Text index saved successfully")
    
    def load_text_index(self) -> bool:
        """Load existing text index from disk."""
        try:
            chunks_path = os.path.join(VECTOR_DB_PATH, "text_chunks.pkl")
            
            if not os.path.exists(chunks_path):
                return False
            
            # Load document chunks
            with open(chunks_path, "rb") as f:
                self.document_chunks = pickle.load(f)
            
            print(f"Text index loaded with {len(self.document_chunks)} chunks")
            return True
        
        except Exception as e:
            print(f"Error loading text index: {str(e)}")
            return False
    
    def retrieve_relevant_chunks_text(self, query: str, k: int = MAX_CHUNKS_RETRIEVED) -> List[Dict[str, str]]:
        """Retrieve relevant chunks using simple text matching."""
        if not self.document_chunks:
            return []
        
        try:
            # Normalize query for better matching
            query_words = set(re.findall(r'\b\w+\b', query.lower()))
            
            # Score each chunk based on word overlap
            scored_chunks = []
            for chunk in self.document_chunks:
                content_words = set(re.findall(r'\b\w+\b', chunk['content'].lower()))
                
                # Calculate similarity score based on word overlap
                overlap = len(query_words.intersection(content_words))
                total_words = len(query_words.union(content_words))
                
                if total_words > 0:
                    similarity_score = overlap / len(query_words)  # Jaccard-like similarity
                else:
                    similarity_score = 0.0
                
                # Also check for exact phrase matches
                if query.lower() in chunk['content'].lower():
                    similarity_score += 0.5
                
                chunk_copy = chunk.copy()
                chunk_copy['similarity_score'] = similarity_score
                scored_chunks.append(chunk_copy)
            
            # Sort by similarity score and return top k
            scored_chunks.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            # Return chunks with reasonable similarity
            relevant_chunks = []
            for chunk in scored_chunks[:k]:
                if chunk['similarity_score'] > 0.1:  # Minimum threshold
                    relevant_chunks.append(chunk)
                    print(f"Retrieved chunk with score {chunk['similarity_score']:.3f}: {chunk['content'][:100]}...")
            
            # If no good matches, return top 3 anyway
            if not relevant_chunks and scored_chunks:
                print("No high-scoring chunks found, returning top results")
                for chunk in scored_chunks[:3]:
                    relevant_chunks.append(chunk)
                    print(f"Fallback chunk with score {chunk['similarity_score']:.3f}: {chunk['content'][:100]}...")
            
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
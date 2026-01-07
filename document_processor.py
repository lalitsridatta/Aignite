"""Document processing module for PDF ingestion and text chunking."""

import os
import re
from typing import List, Dict
import PyPDF2
from io import BytesIO


class DocumentProcessor:
    """Handles PDF processing and text chunking for RAG pipeline."""
    
    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 75):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from a PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return self._clean_text(text)
        
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {str(e)}")
            return ""
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might interfere
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', ' ', text)
        # Normalize spacing
        text = text.strip()
        return text
    
    def chunk_text(self, text: str, document_name: str) -> List[Dict[str, str]]:
        """Split text into overlapping chunks for better retrieval."""
        words = text.split()
        chunks = []
        
        if len(words) <= self.chunk_size:
            return [{
                'content': text,
                'source': document_name,
                'chunk_id': 0
            }]
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            chunks.append({
                'content': chunk_text,
                'source': document_name,
                'chunk_id': len(chunks)
            })
            
            # Break if we've reached the end
            if i + self.chunk_size >= len(words):
                break
        
        return chunks
    
    def process_documents_folder(self, folder_path: str) -> List[Dict[str, str]]:
        """Process all PDF documents in a folder."""
        all_chunks = []
        
        if not os.path.exists(folder_path):
            print(f"Documents folder not found: {folder_path}")
            return all_chunks
        
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        
        if not pdf_files:
            print("No PDF files found in documents folder")
            return all_chunks
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_path, pdf_file)
            print(f"Processing: {pdf_file}")
            
            text = self.extract_text_from_pdf(pdf_path)
            if text:
                chunks = self.chunk_text(text, pdf_file)
                all_chunks.extend(chunks)
                print(f"Created {len(chunks)} chunks from {pdf_file}")
        
        print(f"Total chunks created: {len(all_chunks)}")
        return all_chunks
"""Debug script to test document retrieval and embeddings."""

from document_processor import DocumentProcessor
from rag_pipeline import RAGPipeline
import os

def debug_system():
    """Debug the retrieval system step by step."""
    
    print("🔍 Debugging Retrieval System")
    print("=" * 50)
    
    # Step 1: Test document processing
    print("1. Testing document processing...")
    processor = DocumentProcessor()
    chunks = processor.process_documents_folder("documents")
    
    if not chunks:
        print("❌ No chunks created from documents")
        return
    
    print(f"✅ Created {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
        print(f"   Chunk {i}: {chunk['content'][:100]}...")
    
    # Step 2: Test RAG pipeline initialization
    print("\n2. Testing RAG pipeline...")
    api_key = "AIzaSyA4ab4LWNuXmLjZQudwby3APbQtTRIALnk"
    rag = RAGPipeline(api_key)
    
    # Step 3: Build vector store
    print("\n3. Building vector store...")
    rag.build_vector_store(chunks)
    
    if not rag.vector_store:
        print("❌ Failed to build vector store")
        return
    
    print("✅ Vector store built successfully")
    
    # Step 4: Test queries
    print("\n4. Testing queries...")
    test_queries = [
        "court process",
        "filing lawsuit", 
        "hearing",
        "case stages",
        "legal procedure"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        
        # Test retrieval
        chunks = rag.retrieve_relevant_chunks(query)
        print(f"   Retrieved {len(chunks)} chunks")
        
        if chunks:
            for i, chunk in enumerate(chunks):
                print(f"   Chunk {i+1} (score: {chunk['similarity_score']:.3f}): {chunk['content'][:80]}...")
            
            # Test response generation
            response, sources, warnings = rag.generate_response(query, chunks)
            print(f"   Response: {response[:100]}...")
            print(f"   Sources: {sources}")
        else:
            print("   ❌ No chunks retrieved")
    
    print("\n" + "=" * 50)
    print("🏁 Debug complete")

if __name__ == "__main__":
    debug_system()
"""Test the simple text-based RAG system."""

from document_processor import DocumentProcessor
from simple_rag_pipeline import SimpleRAGPipeline

def test_simple_system():
    """Test the simple RAG system."""
    
    print("🔍 Testing Simple Text-Based RAG System")
    print("=" * 50)
    
    # Step 1: Process documents
    print("1. Processing documents...")
    processor = DocumentProcessor()
    chunks = processor.process_documents_folder("documents")
    
    if not chunks:
        print("❌ No chunks created")
        return False
    
    print(f"✅ Created {len(chunks)} chunks")
    
    # Step 2: Initialize simple RAG
    print("\n2. Initializing simple RAG...")
    api_key = "AIzaSyA4ab4LWNuXmLjZQudwby3APbQtTRIALnk"
    rag = SimpleRAGPipeline(api_key)
    
    # Step 3: Build text index
    print("\n3. Building text index...")
    rag.build_text_index(chunks)
    
    # Step 4: Test queries
    print("\n4. Testing queries...")
    test_queries = [
        "court process",
        "filing lawsuit", 
        "hearing",
        "case stages",
        "legal procedure",
        "what is a motion",
        "how to file",
        "court hearing process"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        
        # Test retrieval
        chunks = rag.retrieve_relevant_chunks_text(query)
        print(f"   Retrieved {len(chunks)} chunks")
        
        if chunks:
            # Test response generation
            response, sources, warnings = rag.generate_response(query, chunks)
            print(f"   Response: {response[:150]}...")
            print(f"   Sources: {sources}")
        else:
            print("   ❌ No chunks retrieved")
    
    print("\n" + "=" * 50)
    print("🏁 Test complete")
    return True

if __name__ == "__main__":
    test_simple_system()
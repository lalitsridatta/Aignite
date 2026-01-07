"""Quick script to test the system with a new API key."""

from simple_rag_pipeline import SimpleRAGPipeline
from document_processor import DocumentProcessor
import sys

def test_with_new_key(api_key):
    """Test the system with a new API key."""
    
    print("🔍 Testing System with New API Key")
    print("=" * 50)
    
    # Step 1: Test API key
    print("1. Testing API key...")
    try:
        rag = SimpleRAGPipeline(api_key)
        print("✅ API key accepted")
    except Exception as e:
        print(f"❌ API key failed: {str(e)}")
        return False
    
    # Step 2: Load or build document index
    print("\n2. Loading document index...")
    if rag.load_text_index():
        print("✅ Document index loaded")
    else:
        print("Building new document index...")
        processor = DocumentProcessor()
        chunks = processor.process_documents_folder("documents")
        if chunks:
            rag.build_text_index(chunks)
            print(f"✅ Built index with {len(chunks)} chunks")
        else:
            print("❌ No documents found")
            return False
    
    # Step 3: Test a simple query
    print("\n3. Testing query...")
    test_query = "What are the stages of a case?"
    
    try:
        chunks = rag.retrieve_relevant_chunks_text(test_query)
        print(f"✅ Retrieved {len(chunks)} chunks")
        
        if chunks:
            response, sources, warnings = rag.generate_response(test_query, chunks)
            print(f"✅ Generated response: {response[:150]}...")
            print(f"📚 Sources: {sources}")
            
            print(f"\n🎉 System is working perfectly with the new API key!")
            print("You can now run: python -m streamlit run app.py")
            return True
        else:
            print("⚠️  No relevant chunks found")
            return False
            
    except Exception as e:
        print(f"❌ Query failed: {str(e)}")
        if "quota" in str(e).lower():
            print("💡 Quota exceeded. Try waiting or use another API key.")
        return False

def main():
    """Main function."""
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        test_with_new_key(api_key)
    else:
        print("Usage: python run_with_new_key.py YOUR_API_KEY")
        print("Or just run: python -m streamlit run app.py")
        print("And enter your API key in the web interface")

if __name__ == "__main__":
    main()
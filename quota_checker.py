"""Check API quota and test basic functionality."""

import google.generativeai as genai
import sys

def test_api_key(api_key):
    """Test if an API key works and check basic functionality."""
    
    print(f"🔍 Testing API Key: {api_key[:20]}...")
    
    try:
        # Configure API
        genai.configure(api_key=api_key)
        
        # Test 1: List models
        print("\n1. Testing model access...")
        models = list(genai.list_models())
        generation_models = [m for m in models if 'generateContent' in m.supported_generation_methods]
        print(f"✅ Found {len(generation_models)} generation models")
        
        # Test 2: Simple generation
        print("\n2. Testing content generation...")
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content("What is a court? Answer in one sentence.")
        print(f"✅ Generation successful: {response.text[:100]}...")
        
        # Test 3: Check embedding (if quota allows)
        print("\n3. Testing embeddings...")
        try:
            result = genai.embed_content(
                model="models/embedding-001",
                content="test text",
                task_type="retrieval_document"
            )
            print("✅ Embeddings working")
        except Exception as e:
            if "quota" in str(e).lower():
                print("⚠️  Embeddings quota exceeded (text search will be used)")
            else:
                print(f"❌ Embeddings error: {str(e)}")
        
        print(f"\n🎉 API Key is working! You can use this key in the application.")
        return True
        
    except Exception as e:
        print(f"\n❌ API Key test failed: {str(e)}")
        if "quota" in str(e).lower():
            print("💡 This appears to be a quota issue. Try a different API key.")
        elif "invalid" in str(e).lower():
            print("💡 This appears to be an invalid API key.")
        return False

def main():
    """Main function to test API keys."""
    print("🔑 Gemini API Key Tester")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # API key provided as command line argument
        api_key = sys.argv[1]
        test_api_key(api_key)
    else:
        # Interactive mode
        print("Enter your Gemini API key to test:")
        api_key = input("API Key: ").strip()
        
        if api_key:
            test_api_key(api_key)
        else:
            print("No API key provided.")

if __name__ == "__main__":
    main()
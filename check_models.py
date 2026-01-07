"""Check available Gemini models."""

import google.generativeai as genai

def check_models():
    """Check available models."""
    api_key = "AIzaSyA4ab4LWNuXmLjZQudwby3APbQtTRIALnk"
    genai.configure(api_key=api_key)
    
    print("Available models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"- {model.name}")

if __name__ == "__main__":
    check_models()
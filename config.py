"""Configuration settings for the Judicial Court Process Explainer Bot."""

# RAG Configuration
CHUNK_SIZE = 600  # tokens per chunk
CHUNK_OVERLAP = 75  # overlap between chunks
MAX_CHUNKS_RETRIEVED = 5  # number of relevant chunks to retrieve

# Gemini Configuration
MODEL_NAME = "gemini-2.5-flash"
EMBEDDING_MODEL = "models/embedding-001"
MAX_TOKENS = 1000
TEMPERATURE = 0.1  # Low temperature for factual responses

# Vector Database Configuration
VECTOR_DB_PATH = "vector_store"
SIMILARITY_THRESHOLD = 0.3  # Lowered threshold for better retrieval

# Safety Configuration
SYSTEM_PROMPT = """You are a Judicial Process Explainer Bot.

STRICT RULES:
1. You ONLY explain court procedures based on the retrieved documents provided
2. You do NOT provide legal advice, opinions, predictions, or interpretations
3. You do NOT analyze individual cases or give case-specific guidance
4. If the answer is not in the retrieved documents, say "I don't have that information in the available court documents"
5. Use simple, neutral language that anyone can understand
6. Focus only on procedural explanations and general court processes

Your responses should be:
- Factual and document-based only
- Clear and easy to understand
- Neutral in tone
- Focused on procedures, not outcomes"""

# UI Configuration
APP_TITLE = "Judicial Court Process & Case Flow Explainer"
DISCLAIMER = "⚠️ This system provides procedural explanations only and does not constitute legal advice."
Deploy Link :- https://aignite-gc9kf4dxhxrcxmmfxtp2kq.streamlit.app/


# Judicial Court Process & Case Flow Explainer Bot

## Problem Statement
Legal procedures can be complex and intimidating for the general public. Many people struggle to understand basic court processes, hearing stages, and case lifecycles, creating barriers to accessing justice and legal awareness.

## Solution
An AI-powered chatbot that explains court procedures in simple, neutral language using Retrieval-Augmented Generation (RAG) to ensure accuracy and safety.

## Why RAG is Used
- **Accuracy**: Responses are grounded in official court documents
- **Safety**: Prevents hallucination and ensures factual information
- **Transparency**: Shows source documents for verification
- **Compliance**: Maintains strict boundaries against legal advice

## Safety & Ethical Constraints
- **NO LEGAL ADVICE**: Only explains procedures, never advises
- **NO OPINIONS**: Neutral, factual explanations only
- **NO PREDICTIONS**: Cannot predict case outcomes
- **NO CASE ANALYSIS**: Does not analyze individual cases
- **DOCUMENT-BOUND**: Only uses information from provided documents

## Technical Architecture
```
User Query → Vector Search → Document Retrieval → Gemini Flash → Safe Response
```

## Features
- RAG-powered document retrieval
- PDF ingestion and processing
- Vector similarity search
- Safety guardrails and prompt engineering
- Clean Streamlit interface
- Source document attribution

## Quick Start (Automated Deployment)

### Option 1: One-Click Deployment
```bash
python deploy.py
```
This script will:
- Install all dependencies
- Copy documents from Desktop/hackiee folder
- Run system tests
- Launch the application

### Option 2: Manual Setup

#### Prerequisites
```bash
pip install -r requirements.txt
```

#### Document Setup
```bash
# Copy documents from hackiee folder
python setup_documents.py

# OR manually copy PDF files to documents/ folder
```

#### Run Application
```bash
streamlit run app.py
```

#### Run Tests (Optional)
```bash
python test_system.py
```


## Usage
1. Enter your Gemini API key when prompted
2. Upload or ensure court documents are in the documents folder
3. Ask questions about court procedures
4. Receive factual, document-based explanations

## Disclaimer
This system provides procedural explanations only and does not constitute legal advice.

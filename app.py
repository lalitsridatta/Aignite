"""Streamlit web application for Judicial Court Process Explainer Bot."""

import streamlit as st
import os
from document_processor import DocumentProcessor
from simple_rag_pipeline import SimpleRAGPipeline
from config import *


def apply_custom_css():
    """Apply custom CSS for pink/coral theme similar to Meyme UI."""
    # Check if dark mode is enabled
    dark_mode = st.session_state.get('dark_mode', False)
    
    if dark_mode:
        # Dark mode styles
        st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles - Dark Mode */
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #fff !important;
        }
        
        /* Override all Streamlit text colors - Dark Mode */
        .stApp * {
            color: #fff !important;
        }
        
        /* Override specific Streamlit elements - Dark Mode */
        .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #fff !important;
        }
        
        .stText, .stCaption {
            color: #fff !important;
        }
        
        /* Input labels - Dark Mode */
        .stTextInput label, .stTextArea label, .stSelectbox label {
            color: #fff !important;
        }
        
        /* Header Styles - Dark Mode */
        .main-header {
            background: rgba(30, 30, 50, 0.8);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 107, 157, 0.3);
            box-shadow: 0 10px 30px rgba(255, 107, 157, 0.2);
        }
        
        .main-title {
            color: #ff6b9d !important;
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .main-subtitle {
            color: #fff !important;
            font-size: 1.2rem;
            text-align: center;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }
        
        /* Feature Cards - Dark Mode */
        .feature-card {
            background: rgba(30, 30, 50, 0.9);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 107, 157, 0.2);
            transition: transform 0.3s ease;
            text-align: center;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            border: 1px solid rgba(255, 107, 157, 0.4);
        }
        
        .feature-icon {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: white !important;
            margin: 0 auto 1rem;
            position: relative;
        }
        
        .feature-icon.api {
            background: linear-gradient(135deg, #ff6b9d, #ff8fab);
        }
        
        .feature-icon.docs {
            background: linear-gradient(135deg, #a855f7, #c084fc);
        }
        
        .feature-icon.query {
            background: linear-gradient(135deg, #06b6d4, #67e8f9);
        }
        
        .feature-icon.safety {
            background: linear-gradient(135deg, #22c55e, #4ade80);
        }
        
        .feature-title {
            color: #fff !important;
            font-size: 1.3rem;
            font-weight: 600;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .feature-desc {
            color: #ccc !important;
            text-align: center;
            line-height: 1.5;
        }
        
        /* Buttons - Dark Mode */
        .stButton > button {
            background: linear-gradient(135deg, #ff6b9d, #ff8fab);
            color: white !important;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(255, 107, 157, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 107, 157, 0.4);
        }
        
        /* Input Fields - Dark Mode */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 15px;
            border: 2px solid rgba(255, 107, 157, 0.3);
            background: rgba(30, 30, 50, 0.8) !important;
            backdrop-filter: blur(10px);
            color: #fff !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #ff6b9d;
            box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.2);
        }
        
        /* Sidebar - Dark Mode */
        .css-1d391kg {
            background: rgba(20, 20, 35, 0.9) !important;
            backdrop-filter: blur(10px);
        }
        
        /* Success/Error Messages - Dark Mode */
        .stSuccess {
            background: rgba(34, 197, 94, 0.2) !important;
            border: 1px solid rgba(34, 197, 94, 0.4) !important;
            border-radius: 15px;
            color: #fff !important;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.2) !important;
            border: 1px solid rgba(239, 68, 68, 0.4) !important;
            border-radius: 15px;
            color: #fff !important;
        }
        
        .stWarning {
            background: rgba(245, 158, 11, 0.2) !important;
            border: 1px solid rgba(245, 158, 11, 0.4) !important;
            border-radius: 15px;
            color: #fff !important;
        }
        
        .stInfo {
            background: rgba(6, 182, 212, 0.2) !important;
            border: 1px solid rgba(6, 182, 212, 0.4) !important;
            border-radius: 15px;
            color: #fff !important;
        }
        
        /* Expander - Dark Mode */
        .streamlit-expanderHeader {
            background: rgba(255, 107, 157, 0.2) !important;
            border-radius: 15px;
            border: 1px solid rgba(255, 107, 157, 0.3) !important;
            color: #fff !important;
        }
        
        /* Metrics - Dark Mode */
        .metric-card {
            background: rgba(30, 30, 50, 0.9) !important;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 107, 157, 0.2);
        }
        
        /* Dark mode toggle */
        .dark-mode-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 999;
            background: rgba(255, 107, 157, 0.9);
            border-radius: 50px;
            padding: 10px 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom scrollbar - Dark Mode */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(30, 30, 50, 0.3);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #ff6b9d, #ff8fab);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #ff5a8a, #ff7a9a);
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Light mode styles (original)
        st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .stApp {
            background: linear-gradient(135deg, #ffeef0 0%, #f8e8ea 100%);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: #000 !important;
        }
        
        /* Override all Streamlit text colors */
        .stApp * {
            color: #000 !important;
        }
        
        /* Override specific Streamlit elements */
        .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #000 !important;
        }
        
        .stText, .stCaption {
            color: #000 !important;
        }
        
        /* Input labels */
        .stTextInput label, .stTextArea label, .stSelectbox label {
            color: #000 !important;
        }
        
        /* Header Styles */
        .main-header {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 182, 193, 0.2);
            box-shadow: 0 10px 30px rgba(255, 107, 157, 0.1);
        }
        
        .main-title {
            color: #000 !important;
            font-size: 3rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .main-subtitle {
            color: #000 !important;
            font-size: 1.2rem;
            text-align: center;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }
        
        /* Feature Cards */
        .feature-card {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 182, 193, 0.1);
            transition: transform 0.3s ease;
            text-align: center;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-icon {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: white !important;
            margin: 0 auto 1rem;
            position: relative;
        }
        
        .feature-icon.api {
            background: linear-gradient(135deg, #ff6b9d, #ff8fab);
        }
        
        .feature-icon.docs {
            background: linear-gradient(135deg, #a855f7, #c084fc);
        }
        
        .feature-icon.query {
            background: linear-gradient(135deg, #06b6d4, #67e8f9);
        }
        
        .feature-icon.safety {
            background: linear-gradient(135deg, #22c55e, #4ade80);
        }
        
        .feature-title {
            color: #000 !important;
            font-size: 1.3rem;
            font-weight: 600;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .feature-desc {
            color: #000 !important;
            text-align: center;
            line-height: 1.5;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #ff6b9d, #ff8fab);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(255, 107, 157, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 107, 157, 0.4);
        }
        
        /* Input Fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 15px;
            border: 2px solid rgba(255, 107, 157, 0.2);
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #ff6b9d;
            box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.1);
        }
        
        /* Sidebar */
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
        }
        
        /* Success/Error Messages */
        .stSuccess {
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 15px;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 15px;
        }
        
        .stWarning {
            background: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 15px;
        }
        
        .stInfo {
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.3);
            border-radius: 15px;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: rgba(255, 107, 157, 0.1);
            border-radius: 15px;
            border: 1px solid rgba(255, 107, 157, 0.2);
        }
        
        /* Metrics */
        .metric-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 182, 193, 0.1);
        }
        
        /* Dark mode toggle */
        .dark-mode-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 999;
            background: rgba(255, 107, 157, 0.9);
            border-radius: 50px;
            padding: 10px 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 182, 193, 0.1);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #ff6b9d, #ff8fab);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #ff5a8a, #ff7a9a);
        }
        </style>
        """, unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'rag_pipeline' not in st.session_state:
        st.session_state.rag_pipeline = None
    if 'documents_loaded' not in st.session_state:
        st.session_state.documents_loaded = False
    if 'api_key_set' not in st.session_state:
        st.session_state.api_key_set = False
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False


def toggle_dark_mode():
    """Toggle dark mode on/off."""
    st.session_state.dark_mode = not st.session_state.dark_mode


def setup_api_key():
    """Handle API key setup with custom styling."""
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon api">🔑</div>
        <h3 class="feature-title">API Key Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if we already have a working API key
    if st.session_state.api_key_set and st.session_state.rag_pipeline:
        st.success("✅ Gemini API is already configured!")
        
        # Option to change API key
        if st.button("🔄 Change API Key"):
            st.session_state.api_key_set = False
            st.session_state.rag_pipeline = None
            st.rerun()
        return True
    
    # API key input
    api_key = st.text_input(
        "Enter your Gemini API Key:",
        type="password",
        placeholder="AIzaSy...",
        help="Get your API key from https://ai.google.dev/"
    )
    
    # Default fallback key
    if not api_key:
        api_key = "AIzaSyA4ab4LWNuXmLjZQudwby3APbQtTRIALnk"
        st.info("Using default API key. Enter your own key above for better quota limits.")
    
    if st.button("🚀 Configure API"):
        if api_key:
            try:
                st.session_state.rag_pipeline = SimpleRAGPipeline(api_key)
                st.session_state.api_key_set = True
                st.success("✅ Gemini API configured successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error configuring Gemini API: {str(e)}")
                return False
        else:
            st.error("Please enter an API key")
            return False
    
    return st.session_state.api_key_set


def load_documents():
    """Load and process court documents."""
    if st.session_state.documents_loaded:
        return True
    
    documents_folder = "documents"
    
    # Check if documents folder exists
    if not os.path.exists(documents_folder):
        st.warning("📁 Documents folder not found. Creating documents folder...")
        os.makedirs(documents_folder)
        st.info("Please add your court procedure PDF files to the 'documents' folder and restart the app.")
        return False
    
    # Check for existing text index
    if st.session_state.rag_pipeline.load_text_index():
        st.session_state.documents_loaded = True
        st.success("📚 Existing document index loaded successfully!")
        return True
    
    # Process documents if no existing index
    with st.spinner("🔄 Processing court documents... This may take a few minutes."):
        processor = DocumentProcessor(CHUNK_SIZE, CHUNK_OVERLAP)
        chunks = processor.process_documents_folder(documents_folder)
        
        if not chunks:
            st.error("❌ No PDF documents found in the documents folder.")
            st.info("Please add court procedure PDF files to the 'documents' folder.")
            return False
        
        # Build text index
        st.session_state.rag_pipeline.build_text_index(chunks)
        st.session_state.documents_loaded = True
        st.success(f"✅ Successfully processed {len(chunks)} document chunks!")
        return True


def display_header():
    """Display application header and disclaimer with custom styling."""
    # Apply custom CSS
    apply_custom_css()
    
    # Dark mode toggle
    col1, col2, col3 = st.columns([1, 2, 1])
    with col3:
        dark_mode_icon = "🌙" if not st.session_state.dark_mode else "☀️"
        dark_mode_text = "Dark Mode" if not st.session_state.dark_mode else "Light Mode"
        if st.button(f"{dark_mode_icon} {dark_mode_text}", key="dark_mode_toggle"):
            toggle_dark_mode()
            st.rerun()
    
    # Main header with custom styling
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">⚖️ Judicial Court Process Explainer</h1>
        <p class="main-subtitle">
            Your AI assistant for understanding court procedures, hearing stages, and case lifecycles 
            in simple, neutral language based on official court documents.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Prominent disclaimer with custom styling
    st.error(DISCLAIMER)
    
    # Features overview with cards
    color = "#fff" if st.session_state.dark_mode else "#000"
    st.markdown(f"""
    <div style="margin: 2rem 0;">
        <h2 style="color: {color}; text-align: center; font-size: 2rem; margin-bottom: 2rem;">
            🌟 System Features
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create feature cards in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon api">🔑</div>
            <h3 class="feature-title">AI-Powered Analysis</h3>
            <p class="feature-desc">Gemini 1.5 Flash for intelligent document processing</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon query">💬</div>
            <h3 class="feature-title">Natural Language Queries</h3>
            <p class="feature-desc">Ask questions in plain English about court procedures</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon docs">📚</div>
            <h3 class="feature-title">Document Processing</h3>
            <p class="feature-desc">RAG-based retrieval from official court documents</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon safety">🛡️</div>
            <h3 class="feature-title">Safety & Accuracy</h3>
            <p class="feature-desc">Document-grounded responses with source attribution</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")


def handle_user_query():
    """Handle user queries and generate responses with custom styling."""
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon query">💬</div>
        <h3 class="feature-title">Ask About Court Procedures</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Example queries
    with st.expander("📝 Example Questions"):
        st.markdown("""
        - What are the steps in filing a civil lawsuit?
        - How does the hearing process work?
        - What happens during case discovery?
        - What are the stages of an appeal?
        - How do I prepare for a court hearing?
        """)
    
    # Query input
    user_query = st.text_area(
        "Enter your question about court procedures:",
        placeholder="e.g., What are the steps involved in filing a motion?",
        height=100
    )
    
    if st.button("🔍 Get Explanation", type="primary"):
        if not user_query.strip():
            st.warning("Please enter a question.")
            return
        
        with st.spinner("🔍 Searching court documents..."):
            # Retrieve relevant chunks
            relevant_chunks = st.session_state.rag_pipeline.retrieve_relevant_chunks_text(user_query)
            
            if not relevant_chunks:
                st.info("I don't have that information in the available court documents.")
                return
            
            # Generate response
            response, sources, warnings = st.session_state.rag_pipeline.generate_response(user_query, relevant_chunks)
        
        # Display response in styled container
        st.markdown("""
        <div class="feature-card">
            <h3 class="feature-title">📋 Explanation</h3>
        </div>
        """, unsafe_allow_html=True)
        st.write(response)
        
        # Display any safety warnings (for development/monitoring)
        if warnings and st.checkbox("Show system diagnostics", key="show_warnings"):
            st.warning("System diagnostics:")
            for warning in warnings:
                st.caption(f"⚠️ {warning}")
        
        # Display sources
        if sources:
            st.markdown("""
            <div class="feature-card">
                <h3 class="feature-title">📚 Source Documents</h3>
            </div>
            """, unsafe_allow_html=True)
            for source in sources:
                st.caption(f"• {source}")
        
        # Display retrieved chunks for transparency
        with st.expander("🔍 Retrieved Document Sections"):
            for i, chunk in enumerate(relevant_chunks):
                st.markdown(f"**Source:** {chunk['source']}")
                st.markdown(f"**Similarity Score:** {chunk['similarity_score']:.3f}")
                st.text_area(
                    f"Content {i+1}:",
                    chunk['content'][:500] + "..." if len(chunk['content']) > 500 else chunk['content'],
                    height=100,
                    key=f"chunk_{i}"
                )
                st.markdown("---")


def display_system_info():
    """Display system information and status with custom styling."""
    with st.sidebar:
        color = "#fff" if st.session_state.dark_mode else "#000"
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: {color}; font-size: 1.5rem;">🔧 System Status</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # API Status
        if st.session_state.api_key_set:
            st.success("✅ Gemini API Connected")
        else:
            st.error("❌ Gemini API Not Connected")
        
        # Documents Status
        if st.session_state.documents_loaded:
            st.success("✅ Documents Loaded")
            if st.session_state.rag_pipeline and st.session_state.rag_pipeline.document_chunks:
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: {color}; margin: 0;">📊 Document Chunks</h4>
                    <p style="font-size: 1.5rem; font-weight: bold; margin: 0.5rem 0; color: {color};">
                        {len(st.session_state.rag_pipeline.document_chunks)}
                    </p>
                    <p style="color: {color}; margin: 0;">chunks indexed</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Documents Not Loaded")
        
        st.markdown("---")
        
        # System Information
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <h2 style="color: {color}; font-size: 1.5rem;">ℹ️ About This System</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: {'rgba(30, 30, 50, 0.9)' if st.session_state.dark_mode else 'white'}; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; box-shadow: 0 5px 15px rgba(0,0,0,{'0.3' if st.session_state.dark_mode else '0.1'}); border: 1px solid rgba(255, 107, 157, {'0.2' if st.session_state.dark_mode else '0.1'});">
            <h4 style="color: {color}; margin-bottom: 1rem;">Technology Stack:</h4>
            <ul style="color: {color}; line-height: 1.8;">
                <li>🤖 Gemini 1.5 Flash</li>
                <li>🔍 Text-based RAG</li>
                <li>📊 Simple Text Search</li>
                <li>🎨 Streamlit Interface</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: {'rgba(30, 30, 50, 0.9)' if st.session_state.dark_mode else 'white'}; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; box-shadow: 0 5px 15px rgba(0,0,0,{'0.3' if st.session_state.dark_mode else '0.1'}); border: 1px solid rgba(255, 107, 157, {'0.2' if st.session_state.dark_mode else '0.1'});">
            <h4 style="color: {color}; margin-bottom: 1rem;">Safety Features:</h4>
            <ul style="color: {color}; line-height: 1.8;">
                <li>Document-grounded responses</li>
                <li>No legal advice provided</li>
                <li>Neutral, factual explanations</li>
                <li>Source attribution</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Refresh button
        if st.button("🔄 Refresh System"):
            st.session_state.documents_loaded = False
            st.rerun()


def main():
    """Main application function."""
    st.set_page_config(
        page_title="Judicial Court Process Explainer",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Display header with custom styling
    display_header()
    
    # Setup API key
    if not st.session_state.api_key_set:
        if not setup_api_key():
            st.stop()
    
    # Load documents
    if not load_documents():
        st.stop()
    
    # Display system info in sidebar
    display_system_info()
    
    # Handle user queries
    handle_user_query()
    
    # Footer with custom styling
    st.markdown("---")
    color = "#fff" if st.session_state.dark_mode else "#000"
    bg_color = "rgba(30, 30, 50, 0.8)" if st.session_state.dark_mode else "rgba(255, 255, 255, 0.8)"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem; background: {bg_color}; border-radius: 15px; margin-top: 2rem;">
        <p style="color: {color}; font-size: 0.9rem; margin: 0;">
            <strong>Disclaimer:</strong> This system provides general procedural information only. 
            For specific legal matters, please consult with a qualified attorney.
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
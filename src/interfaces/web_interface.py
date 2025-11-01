"""
Web Interface for Home Assistant Chatbot
Streamlit-based admin interface
"""
import sys
from pathlib import Path
import asyncio

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from dotenv import load_dotenv

from utils import ConfigManager
from core import HomeChatbot

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Home Assistant Chatbot - Admin",
    page_icon="🏠",
    layout="wide"
)

@st.cache_resource
def get_chatbot():
    """Get or create chatbot instance"""
    config_manager = ConfigManager()
    return HomeChatbot(config_manager.config), config_manager.config

def main():
    """Main web interface"""
    st.title("🏠 Home Assistant Chatbot - Admin Panel")
    
    # Load chatbot
    try:
        chatbot, config = get_chatbot()
    except Exception as e:
        st.error(f"❌ Error initializing chatbot: {e}")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("📊 Navigation")
        page = st.radio(
            "Select page",
            ["Dashboard", "Knowledge Base", "Test Chat", "Configuration"]
        )
    
    # Dashboard Page
    if page == "Dashboard":
        st.header("📊 Dashboard")
        
        stats = chatbot.get_stats()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Version", stats.get('version', 'N/A'))
        
        with col2:
            st.metric("Environment", stats.get('environment', 'N/A'))
        
        with col3:
            rag_stats = stats.get('rag', {})
            if rag_stats.get('enabled'):
                st.metric("Documents", rag_stats.get('total_documents', 0))
            else:
                st.metric("RAG Status", "Disabled")
        
        # RAG Information
        if rag_stats.get('enabled'):
            st.subheader("📚 Knowledge Base")
            categories = rag_stats.get('categories', {})
            if categories:
                st.write("**Documents by Category:**")
                for cat, count in categories.items():
                    st.write(f"• {cat}: {count}")
            else:
                st.info("No documents in knowledge base yet")
    
    # Knowledge Base Page
    elif page == "Knowledge Base":
        st.header("📚 Knowledge Base Management")
        
        tab1, tab2 = st.tabs(["Add Knowledge", "Upload Document"])
        
        with tab1:
            st.subheader("✏️ Add Knowledge Manually")
            
            with st.form("add_knowledge_form"):
                knowledge_text = st.text_area(
                    "Knowledge Content",
                    placeholder="Enter information you want to add to the knowledge base...",
                    height=150
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    category = st.selectbox(
                        "Category",
                        ["pulizia", "utenze", "manutenzione", "casa", "generale"]
                    )
                
                submitted = st.form_submit_button("Add Knowledge")
                
                if submitted and knowledge_text:
                    if chatbot.rag_system.config.enabled:
                        doc_id = chatbot.rag_system.add_knowledge(knowledge_text, category)
                        if doc_id:
                            st.success(f"✅ Knowledge added successfully! ID: {doc_id}")
                            st.rerun()
                        else:
                            st.error("❌ Error adding knowledge")
                    else:
                        st.warning("⚠️ RAG system is disabled in configuration")
        
        with tab2:
            st.subheader("📄 Upload PDF Document")
            
            uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
            
            if uploaded_file:
                col1, col2 = st.columns(2)
                with col1:
                    doc_category = st.selectbox(
                        "Document Category",
                        ["documento", "manuale", "contratto", "utenze", "generale"],
                        key="doc_category"
                    )
                
                if st.button("Process Document"):
                    if chatbot.rag_system.config.enabled:
                        with st.spinner("Processing document..."):
                            # Save temp file
                            temp_path = f"temp_{uploaded_file.name}"
                            with open(temp_path, "wb") as f:
                                f.write(uploaded_file.getvalue())
                            
                            # Process
                            success = asyncio.run(chatbot.add_document(temp_path, doc_category))
                            
                            # Cleanup
                            import os
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                            
                            if success:
                                st.success("✅ Document processed successfully!")
                            else:
                                st.error("❌ Error processing document")
                    else:
                        st.warning("⚠️ RAG system is disabled in configuration")
    
    # Test Chat Page
    elif page == "Test Chat":
        st.header("💬 Test Chat Interface")
        
        st.info("Test your chatbot here. This interface simulates how the bot responds.")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask your question..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = asyncio.run(chatbot.get_response(prompt, "web_test"))
                    st.markdown(response)
            
            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Configuration Page
    elif page == "Configuration":
        st.header("⚙️ Configuration")
        
        st.subheader("Current Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**LLM Settings:**")
            st.write(f"• Provider: {config.llm.provider}")
            st.write(f"• Model: {config.llm.model}")
            st.write(f"• Temperature: {config.llm.temperature}")
            st.write(f"• Max Tokens: {config.llm.max_tokens}")
        
        with col2:
            st.write("**RAG Settings:**")
            st.write(f"• Enabled: {config.rag.enabled}")
            st.write(f"• Embedding Model: {config.rag.embedding_model}")
            st.write(f"• Collection: {config.rag.collection_name}")
            st.write(f"• Max Results: {config.rag.max_search_results}")
        
        st.subheader("Cache Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Clear Response Cache"):
                chatbot.response_cache.clear()
                st.success("✅ Response cache cleared!")
        
        with col2:
            if st.button("Clear RAG Cache"):
                if chatbot.rag_system.config.enabled:
                    chatbot.rag_system.cache.clear()
                    st.success("✅ RAG cache cleared!")
                else:
                    st.warning("RAG system is disabled")
        
        st.subheader("System Information")
        st.json(chatbot.get_stats())

if __name__ == "__main__":
    main()

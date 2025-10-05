import streamlit as st
from chatbot_core import HomeChatbot

def main():
    st.title("🏠 Gestione Chatbot Domestico")
    
    chatbot = HomeChatbot()
    
    st.sidebar.header("Operazioni")
    
    # Upload documenti
    st.header("📄 Carica Documenti")
    uploaded_file = st.file_uploader("Scegli un PDF", type="pdf")
    
    if uploaded_file:
        if st.button("Aggiungi al Database"):
            # Salva temporaneamente
            with open(f"temp_{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # Processa
            success = asyncio.run(chatbot.add_document(f"temp_{uploaded_file.name}"))
            
            if success:
                st.success("✅ Documento aggiunto!")
            else:
                st.error("❌ Errore nell'aggiunta")
    
    # Aggiungi conoscenza manuale
    st.header("✏️ Aggiungi Conoscenza")
    new_knowledge = st.text_area("Scrivi informazione da aggiungere")
    category = st.selectbox("Categoria", ["pulizia", "utenze", "generale", "ricette"])
    
    if st.button("Aggiungi Conoscenza"):
        chatbot.add_knowledge(new_knowledge, category)
        st.success("✅ Conoscenza aggiunta!")
    
    # Statistiche database
    st.header("📊 Statistiche Database")
    count = chatbot.collection.count()
    st.metric("Documenti nel database", count)

if __name__ == "__main__":
    main()
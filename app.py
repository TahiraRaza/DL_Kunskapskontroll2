# Beskrivning: Streamlit-app för att ställa frågor inom finans och få svar via en RAG-modell som använder Gemini.

import streamlit as st
from rag_model import load_vectorstore, retrieve_relevant_chunks, answer_with_gemini
from dotenv import load_dotenv
import os

# Hämta API-Key från .env-fil
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Konfigurera Streamlit
st.set_page_config(page_title="Finansassistent", layout="centered")
st.title("📊 Finansassistent - Investeringsrådgivare för nybörjare")
st.markdown(
    """
    Ställ frågor om fonder, aktier och sparstrategier.  
    Svaren genereras med hjälp av en AI-modell baserad på information från verifierade svenska finanskällor.
    """
)

# Kontrollera API-nyckel
if not API_KEY:
    st.error("❌ API-nyckel saknas. Kontrollera att .env-filen innehåller en giltig API_KEY.")
    st.stop()

# Ladda vektorindex
@st.cache_resource
def get_vectorstore():
    return load_vectorstore()

vectorizer, chunks, vectors = get_vectorstore()

# Användarens fråga
user_question = st.text_input("❓ Ställ din fråga:")

# När användaren klickar på knappen
if st.button("📨 Skicka fråga"):
    if not user_question.strip():
        st.warning("⚠️ Vänligen skriv en fråga innan du skickar.")
    else:
        with st.spinner("🔍 Hämtar relevanta dokument..."):
            relevant_chunks = retrieve_relevant_chunks(user_question, vectorizer, chunks, vectors)

        with st.spinner("🤖 Genererar svar med Gemini..."):
            try:
                answer = answer_with_gemini(user_question, relevant_chunks)
                if answer.startswith("❌"):
                    st.error(answer)
                    answer = None
                else:
                    st.success("✅ Svar genererat!")
            except Exception as e:
                st.error(f"❌ Ett oväntat fel uppstod vid generering: {e}")
                answer = None

        if answer:
            st.subheader("💬 Svar från AI-rådgivaren")
            st.write(answer)

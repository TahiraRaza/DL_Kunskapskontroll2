# Beskrivning: Innehåller funktioner för dokumentinläsning, chunkning, indexering, vektorsökning och svarsgenerering med Gemini för en RAG-modell.

import os
import google.generativeai as genai
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# Hämta API-Key från .env-fil
load_dotenv()
GENAI_API_KEY = os.getenv("API_KEY")

# Kontrollera att nyckeln finns
if not GENAI_API_KEY:
    raise ValueError("❌ Ingen API-nyckel funnen. Kontrollera att .env innehåller en variabel 'API_KEY'.")

# Konfigurera Gemini
genai.configure(api_key=GENAI_API_KEY)

# Laddar dokument från mapp (endast .txt-filer)
def load_documents_from_folder(folder_path):
    documents = []
    sources = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                documents.append(content)
                sources.append(filename)
    return documents, sources


# Delar upp dokument i överlappande chunkar
def chunk_documents(documents, chunk_size=500, overlap=100):
    chunks = []
    for doc in documents:
        for i in range(0, len(doc), chunk_size - overlap):
            chunk = doc[i:i + chunk_size]
            chunks.append(chunk)
    return chunks

# Skapar och sparar TF-IDF-baserat vektorindex
def build_vector_index(chunks, index_path="vector_index.pkl"):
    vectorizer = TfidfVectorizer().fit(chunks)
    vectors = vectorizer.transform(chunks)
    with open(index_path, "wb") as f:
        pickle.dump((vectorizer, chunks, vectors), f)
    print("[✔] Vektorindex sparat.")

# Laddar vektorindex från fil
def load_vectorstore(index_path="vector_index.pkl"):
    with open(index_path, "rb") as f:
        vectorizer, chunks, vectors = pickle.load(f)
    return vectorizer, chunks, vectors


# Hämtar mest relevanta dokumentutdrag baserat på användarens fråga
def retrieve_relevant_chunks(query, vectorizer, chunks, vectors, top_k=3):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, vectors).flatten()
    top_indices = similarities.argsort()[-top_k:][::-1]
    return [chunks[i] for i in top_indices]

# Genererar svar med hjälp av Gemini och kontext från dokument 
def answer_with_gemini(query, context_chunks):
    context_text = "\n\n".join(context_chunks)

    prompt = (
        "Du är en pedagogisk och korrekt investeringsrådgivare för nybörjare. "
        "Besvara frågan med hjälp av den tillhandahållna kontexten. "
        "Var tydlig och använd ett enkelt språk.\n\n"
        "### Kontext:\n"
        f"{context_text}\n\n"
        f"### Fråga:\n{query}\n\n"
        "### Svar:"
    )

    try:
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                top_p=1,
                top_k=1,
                max_output_tokens=1024
            )
        )

        # Kontrollera att svaret finns
        if hasattr(response, "text") and response.text:
            return response.text.strip()
        else:
            return "❌ Inget svar genererades. Kontrollera API-nyckeln och modellens svar."

    except Exception as e:
        return f"❌ Ett fel uppstod vid svarsgenerering: {e}"

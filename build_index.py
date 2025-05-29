# Beskrivning: Skript för att bygga ett vektorindex från dokument i en angiven mapp.

from rag_model import load_documents_from_folder, chunk_documents, build_vector_index

if __name__ == "__main__":
    # Ange din dokumentmapp
    folder_path = "data/investeringsguider"
    
    # Läs in dokumenten
    docs, _ = load_documents_from_folder(folder_path)
    
    # Gör chunkar av dokumenten
    chunks = chunk_documents(docs)
    
    # Bygg och spara vektorindex
    build_vector_index(chunks)

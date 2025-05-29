# Beskrivning: Skript för att utvärdera en RAG-modell genom att jämföra AI-genererade svar med önskade svar.

import os
import google.generativeai as genai
from dotenv import load_dotenv
from rag_model import retrieve_relevant_chunks, answer_with_gemini  # Importera funktioner från rag_model.py

# Hämta API-Key från .env-fil
load_dotenv()
GENAI_API_KEY = os.getenv("API_KEY")

if not GENAI_API_KEY:
    raise ValueError("❌ Ingen API-nyckel funnen. Kontrollera att .env innehåller en variabel 'API_KEY'.")

genai.configure(api_key=GENAI_API_KEY)

# Systemprompt för utvärdering 
evaluation_system_prompt = """Du är ett intelligent utvärderingssystem vars uppgift är att utvärdera en AI-assistents svar.

Om svaret är väldigt nära det önskade svaret, sätt poängen 1. Om svaret är felaktigt eller inte bra nog, sätt poängen 0. Om svaret är delvis i linje med det önskade svaret, sätt poängen 0.5. Motivera kort varför du sätter den poäng du gör."""

# Testdata för utvärdering 
validation_data = [
    {
        "question": "Vad är en aktie?",
        "ideal_answer": "En aktie är en ägarandel i ett företag. Genom att äga aktier kan man få utdelning och ta del av företagets vinst."
    },
    {
        "question": "Vad är riskspridning?",
        "ideal_answer": "Riskspridning innebär att man investerar i flera olika tillgångar för att minska risken."
    }
]

def generate_response(system_prompt, user_prompt):
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    
    response = model.generate_content(
        full_prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.0,
            max_output_tokens=256
        )
    )
    return response.text.strip()

def evaluate_answer(question, ai_answer, ideal_answer):
    evaluation_prompt = f"""Fråga: {question}
AI-assistentens svar: {ai_answer}
Önskat svar: {ideal_answer}"""
    
    return generate_response(evaluation_system_prompt, evaluation_prompt)

def evaluate_rag_model(validation_data):
    
    from rag_model import load_vectorstore
    
    vectorizer, chunks, vectors = load_vectorstore("vector_index.pkl")
    
    results = []
    
    for item in validation_data:
        question = item["question"]
        ideal_answer = item["ideal_answer"]
        
        # Hämta relevant kontext
        relevant_chunks = retrieve_relevant_chunks(question, vectorizer, chunks, vectors, top_k=3)
        
        # Generera AI-svar med Gemini
        ai_answer = answer_with_gemini(question, relevant_chunks)
        
        # Utvärdera svaret
        evaluation = evaluate_answer(question, ai_answer, ideal_answer)
        
        print("="*60)
        print(f"Fråga: {question}")
        print(f"AI-svar: {ai_answer}")
        print(f"Utvärdering:\n{evaluation}")
        print("="*60)
        
        results.append({
            "question": question,
            "ai_answer": ai_answer,
            "ideal_answer": ideal_answer,
            "evaluation": evaluation
        })
    
    return results

if __name__ == "__main__":
    evaluate_rag_model(validation_data)

# DL_Kunskapskontroll 2
# Finansassistent – En interaktiv investeringsrådgivare för nybörjare

Detta projekt är en interaktiv finansapplikation byggd med Streamlit och RAG-teknik (Retrieval-Augmented Generation). Syftet är att erbjuda nybörjare stöd i att förstå grunderna inom investeringar och sparande, baserat på pålitliga källor som Finansinspektionen, Avanza och Advisa.

## Funktioner

- Chattbaserad rådgivning kring aktier, fonder, risknivåer och sparstrategier.
- Använder RAG-teknik för att hämta relevant information från svenska finansdokument och webbsidor.
- Integrerar Gemini API för att generera svar i naturligt språk.
- Innehåll hämtas från:
  - Finansinspektionen (webbsidor)
  - Avanza & Advisa (webbinnehåll om investeringar)
  - PDF-dokument: *Den svenska finansmarknaden 2024* och *Ordlista till finansmarknadsstatistik 2024*

## Teknisk översikt

- **Språk**: Python
- **Ramverk**: Streamlit
- **LLM**: Gemini (via Google AI Studio API)
- **RAG-komponenter**: Dokumentinläsning, chunkning, embedding, indexering, vektorsökning och svarsgenerering
- **Filstruktur**:
  - `rag_model.py` – kärnan i RAG-modellen
  - `app.py` – Streamlit-applikationen
  - `data/investeringsguider` – innehåller källdokument

## Målgrupp

- Privatpersoner med liten eller ingen tidigare kunskap om finans
- Studenter eller nyanställda inom bank, finans eller ekonomi

## Status

Projektet är under aktiv utveckling. Grundläggande funktionalitet är på plats och vidare förbättringar sker löpande.

## Kom igång

```bash
pip install -r requirements.txt
streamlit run app.py

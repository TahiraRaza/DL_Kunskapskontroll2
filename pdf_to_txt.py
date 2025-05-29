# Beskrivning: Skript för att konvertera PDF-dokument till textfiler (.txt) för vidare användning i RAG-systemet.

import fitz  # pymupdf
import os

def pdf_till_txt(pdf_sökväg, txt_sökväg):
    try:
        doc = fitz.open(pdf_sökväg)
        text = ""
        for sida in doc:
            text += sida.get_text()
        doc.close()
        
        with open(txt_sökväg, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[✔] Sparade text från {pdf_sökväg} till {txt_sökväg}")
    except Exception as e:
        print(f"[✘] Kunde inte bearbeta {pdf_sökväg}: {e}")

if __name__ == "__main__":
    basmapp = r"D:\HV-filesync\tara0001\Desktop\Data Scientist\Deep Learning\Kunskapskontroll_2\genai-projekt\data\investeringsguider"
    
    pdf_mappar = {
        "den-svenska-finansmarknaden-2024": os.path.join(basmapp, "den-svenska-finansmarknaden-2024.pdf"),
        "ordlista_till_finansmarknadsstatistik_2024": os.path.join(basmapp, "ordlista_till_finansmarknadsstatistik_20241125.pdf")
    }

    # Skapa mappen för txt-filer om den inte finns
    txt_output_dir = os.path.join(basmapp)
    if not os.path.exists(txt_output_dir):
        os.makedirs(txt_output_dir)

    for namn, pdf_fil in pdf_mappar.items():
        if not os.path.isfile(pdf_fil):
            print(f"[✘] Filen finns inte: {pdf_fil}")
        else:
            txt_fil = os.path.join(txt_output_dir, namn + ".txt")
            pdf_till_txt(pdf_fil, txt_fil)

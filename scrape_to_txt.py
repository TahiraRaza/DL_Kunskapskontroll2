# Beskrivning: Skript för att hämta innehåll från webbsidor (web scraping) och spara det som .txt-filer för användning i RAG-modellen.

import os
import requests
from bs4 import BeautifulSoup

webbplatser = {
    "bristande_kunskap_fonder": "https://www.fi.se/sv/publicerat/nyheter/2023/bristande-kunskap-om-fonder/",
    "fem_saker_att_tanka_pa": "https://www.fi.se/sv/publicerat/nyheter/2023/fem-saker-att-tanka-pa-for-dig-som-vill-investera-i-aktier/",
    "advisa_aktier_guide": "https://advisa.se/privatekonomi/investera-i-aktier/",
    "avanza_aktier": "https://www.avanza.se/lar-dig-mer/avanza-akademin/aktier.html",
    "avanza_fonder": "https://www.avanza.se/lar-dig-mer/avanza-akademin/fonder.html",
    "avanza_sparstrategi": "https://www.avanza.se/lar-dig-mer/avanza-akademin/sparstrategi.html"
}

målmapp = os.path.join("data", "investeringsguider")
os.makedirs(målmapp, exist_ok=True)

def spara_webbsida_som_txt(namn, url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n")
        filnamn = os.path.join(målmapp, f"{namn}.txt")
        with open(filnamn, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[✔] Sparade text från: {url}")
    except Exception as e:
        print(f"[!] Misslyckades att hämta {url}: {e}")

for namn, url in webbplatser.items():
    spara_webbsida_som_txt(namn, url)

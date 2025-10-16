# scraper.py
import requests
from bs4 import BeautifulSoup
import datetime
import json
import os

def load_list(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def get_period():
    hour = datetime.datetime.now().hour
    return "AM" if hour < 12 else "PM"

def scrape_site(url, keywords):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text.lower(), "html.parser")
        text = soup.get_text(separator=" ").lower()
        found = [kw for kw in keywords if kw.lower() in text]
        return found
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return None

def main():
    sites = load_list("sites.txt")
    keywords = load_list("keywords.txt")

    period = get_period()
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"results/{date_str}_{period}.json"
    os.makedirs("results", exist_ok=True)

    all_results = []

    for site in sites:
        found_keywords = scrape_site(site, keywords)
        if found_keywords:
            all_results.append({
                "site": site,
                "keywords_found": found_keywords
            })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"Scraping concluído. Resultados salvos em {filename}")

if __name__ == "__main__":
    main()

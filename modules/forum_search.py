import requests
from bs4 import BeautifulSoup
import time
from utils.logger import logger

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OSINTTool/1.0; +https://github.com/)"
}

def google_site_search(query, site, max_results=5):
    """
    Effectue une recherche Google "site:site query" en scrappant les résultats.
    Attention: scraping Google peut être instable, utiliser avec précaution.
    """
    results = []
    base_url = "https://www.google.com/search"
    params = {
        "q": f"site:{site} {query}",
        "num": max_results,
        "hl": "fr"
    }

    try:
        response = requests.get(base_url, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for g in soup.find_all('div', class_='g'):
            link = g.find('a')
            snippet = g.find('span', class_='aCOpRe')
            if link and snippet:
                results.append({
                    "url": link['href'],
                    "snippet": snippet.text
                })
        logger.info(f"Recherche Google site:{site} {query} retourné {len(results)} résultats")
    except Exception as e:
        logger.error(f"Erreur recherche Google: {e}")

    time.sleep(2)  # Respect délai
    return results

def search_mentions(identifier, sites=None):
    """
    Recherche des mentions d’un pseudo ou email dans une liste de sites (forums/blogs).
    Si sites non fourni, utilise un set de sites classiques.
    """
    if sites is None:
        sites = [
            "reddit.com",
            "stackoverflow.com",
            "quora.com",
            "medium.com",
            "github.com"
        ]

    all_results = {}
    for site in sites:
        results = google_site_search(identifier, site)
        if results:
            all_results[site] = results
    return all_results

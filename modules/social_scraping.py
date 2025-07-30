import requests
from bs4 import BeautifulSoup
import re
from utils.logger import logger
import time

# Liste simplifiée de sites sociaux à scanner
SOCIAL_SITES = {
    "Twitter": "https://twitter.com/{}",
    "GitHub": "https://github.com/{}",
    "Instagram": "https://www.instagram.com/{}",
    "LinkedIn": "https://www.linkedin.com/in/{}",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OSINTTool/1.0; +https://github.com/)"
}

def check_profile_exists(url):
    """
    Vérifie si le profil existe en testant le code HTTP.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            logger.info(f"Profil trouvé : {url}")
            return True, response.text
        else:
            logger.info(f"Profil non trouvé (code {response.status_code}): {url}")
            return False, None
    except Exception as e:
        logger.error(f"Erreur accès profil {url}: {e}")
        return False, None

def extract_emails_from_text(text):
    """
    Extraction simple des emails dans un texte.
    """
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return list(set(emails))

def extract_phone_numbers(text):
    """
    Extraction basique des numéros de téléphone.
    (Exemple simplifié, peut être amélioré)
    """
    phones = re.findall(r"\+?\d[\d\s\-\(\)]{7,}\d", text)
    return list(set(phones))

def scrape_social_profiles(identifier):
    """
    Recherche les profils sociaux publics pour un pseudo ou email.
    Retourne un dict {site: {url, emails, phones}}.
    """
    results = {}

    for site, url_template in SOCIAL_SITES.items():
        url = url_template.format(identifier)
        exists, content = check_profile_exists(url)
        if exists:
            emails = extract_emails_from_text(content)
            phones = extract_phone_numbers(content)
            results[site] = {
                "url": url,
                "emails": emails,
                "phones": phones
            }
            time.sleep(1)  # Respect des délais de scraping
    return results

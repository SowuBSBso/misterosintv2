import requests
from bs4 import BeautifulSoup
from utils.logger import logger

def get_http_headers(url):
    """
    Récupère les headers HTTP d’une URL.
    """
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        logger.info(f"Headers récupérés pour {url}")
        return response.headers
    except Exception as e:
        logger.error(f"Erreur récupération headers HTTP {url}: {e}")
        return {}

def detect_server(headers):
    """
    Détecte le serveur web via l’en-tête 'Server'.
    """
    server = headers.get("Server", "Inconnu")
    return server

def detect_cms(content):
    """
    Analyse le contenu HTML pour détecter un CMS connu (WordPress, Joomla, Drupal, etc.)
    """
    cms_signatures = {
        "WordPress": ["wp-content", "wp-includes", "wp-json"],
        "Joomla": ["Joomla!", "index.php?option=com_"],
        "Drupal": ["drupal-settings-json", "drupal.js"],
        "Magento": ["Mage.Cookies", "magento"],
        "Shopify": ["cdn.shopify.com", "Shopify.theme"],
    }

    soup = BeautifulSoup(content, "html.parser")
    text = soup.prettify().lower()

    detected = []
    for cms, signatures in cms_signatures.items():
        for sig in signatures:
            if sig.lower() in text:
                detected.append(cms)
                break
    return detected if detected else ["Non détecté"]

def analyze_technologies(url):
    """
    Analyse l’URL donnée pour détecter serveur et CMS.
    Retourne un dict résumé.
    """
    headers = get_http_headers(url)
    server = detect_server(headers)
    
    try:
        response = requests.get(url, timeout=10)
        content = response.text
    except Exception as e:
        logger.error(f"Erreur récupération page {url}: {e}")
        content = ""

    cms = detect_cms(content)

    return {
        "server": server,
        "cms": cms
    }

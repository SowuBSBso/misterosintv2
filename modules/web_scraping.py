import requests
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from utils.logger import logger
from utils.http_utils import safe_get

# Regex pour extraction emails et téléphones
EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_REGEX = r'(?:\+?\d{1,3}[-.\s]?|\()?\d{1,4}[-.\s)]?\d{1,4}[-.\s]?\d{1,9}'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OSINT-Tool/1.0; +https://example.com/osint-tool)"
}

def fetch_page(url, delay=2):
    """
    Récupère le contenu HTML d’une page web avec un délai respecté.
    """
    logger.info(f"Fetching page: {url}")
    time.sleep(delay)  # Respect délai entre requêtes
    try:
        resp = safe_get(url, headers=HEADERS)
        if resp and resp.status_code == 200:
            return resp.text
        else:
            logger.warning(f"Échec récupération page {url} - Status {resp.status_code if resp else 'no response'}")
            return ""
    except Exception as e:
        logger.error(f"Exception lors fetch page {url}: {e}")
        return ""

def extract_emails(html):
    """
    Extrait toutes les adresses email du contenu HTML.
    """
    emails = set(re.findall(EMAIL_REGEX, html, re.I))
    logger.info(f"Emails extraits: {len(emails)}")
    return list(emails)

def extract_phones(html):
    """
    Extrait numéros de téléphone (format simple) du contenu HTML.
    """
    phones = set(re.findall(PHONE_REGEX, html))
    logger.info(f"Téléphones extraits: {len(phones)}")
    return list(phones)

def extract_links(html, base_url=None):
    """
    Extrait tous les liens sortants (href) de la page HTML.
    Convertit liens relatifs en absolus si base_url fourni.
    """
    soup = BeautifulSoup(html, 'lxml')
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href'].strip()
        if base_url:
            href = urljoin(base_url, href)
        links.add(href)
    logger.info(f"Liens extraits: {len(links)}")
    return list(links)

def fetch_robots_txt(url):
    """
    Récupère le fichier robots.txt à la racine du domaine.
    """
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    logger.info(f"Fetching robots.txt: {robots_url}")
    time.sleep(1)
    try:
        resp = safe_get(robots_url, headers=HEADERS)
        if resp and resp.status_code == 200:
            return resp.text
        else:
            logger.warning(f"robots.txt non trouvé ou inaccessible ({resp.status_code if resp else 'no response'})")
            return ""
    except Exception as e:
        logger.error(f"Exception lors fetch robots.txt: {e}")
        return ""

def fetch_sitemap_xml(url):
    """
    Récupère le fichier sitemap.xml à la racine du domaine.
    """
    parsed = urlparse(url)
    sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
    logger.info(f"Fetching sitemap.xml: {sitemap_url}")
    time.sleep(1)
    try:
        resp = safe_get(sitemap_url, headers=HEADERS)
        if resp and resp.status_code == 200:
            return resp.text
        else:
            logger.warning(f"sitemap.xml non trouvé ou inaccessible ({resp.status_code if resp else 'no response'})")
            return ""
    except Exception as e:
        logger.error(f"Exception lors fetch sitemap.xml: {e}")
        return ""

def search_wayback(domain, max_results=5):
    """
    Scraping simple de Wayback Machine pour récupérer les URLs archivées.
    (sans API, via scraping des pages publiques)
    """
    results = []
    base_url = f"https://web.archive.org/web/*/{domain}"
    logger.info(f"Scraping Wayback Machine pour {domain}")
    try:
        resp = safe_get(base_url, headers=HEADERS)
        if resp and resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'lxml')
            links = soup.find_all('a', href=True)
            for a in links:
                href = a['href']
                if href.startswith("/web/") and domain in href:
                    full_url = "https://web.archive.org" + href
                    if full_url not in results:
                        results.append(full_url)
                    if len(results) >= max_results:
                        break
        else:
            logger.warning(f"Échec scraping Wayback ({resp.status_code if resp else 'no response'})")
    except Exception as e:
        logger.error(f"Exception scraping Wayback: {e}")
    return results


import socket
import concurrent.futures
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from utils.logger import logger
from utils.http_utils import safe_get

# Liste basique de sous-domaines courants pour bruteforce
COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "smtp", "webmail", "ns1", "ns2",
    "test", "dev", "portal", "admin", "vpn", "shop", "blog",
    "m", "api", "secure", "server", "support", "beta", "demo"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; OSINT-Tool/1.0; +https://example.com/osint-tool)"
}

def is_valid_domain(domain):
    """
    Valide si une chaîne est un domaine valide (simple regex ou check basique)
    """
    if len(domain) == 0 or len(domain) > 253:
        return False
    if " " in domain:
        return False
    # Pas de vérification exhaustive ici
    return True

def resolve_domain(domain):
    """
    Tente de résoudre un domaine en IP.
    Retourne True si réussi, False sinon.
    """
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def brute_force_subdomains(domain, subdomains_list=COMMON_SUBDOMAINS, max_workers=10):
    """
    Tente de découvrir des sous-domaines en bruteforce sur la liste fournie.
    """
    found = []

    def check(sub):
        fqdn = f"{sub}.{domain}"
        if resolve_domain(fqdn):
            logger.info(f"Découvert sous-domaine: {fqdn}")
            return fqdn
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check, sub) for sub in subdomains_list]
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                found.append(res)
    return found

def scrape_subdomains_from_page(url, domain):
    """
    Récupère la page donnée et tente d’extraire des sous-domaines présents dans les liens.
    """
    subdomains = set()
    logger.info(f"Scraping liens pour trouver sous-domaines dans {url}")
    html = safe_get(url, headers=HEADERS)
    if not html:
        return []

    soup = BeautifulSoup(html.text, 'lxml')
    for a in soup.find_all('a', href=True):
        href = a['href']
        parsed = urlparse(href)
        if parsed.netloc.endswith(domain) and parsed.netloc != domain:
            subdomains.add(parsed.netloc)
    return list(subdomains)

def find_subdomains(domain):
    """
    Combine bruteforce + scraping simple (page d’accueil) pour trouver sous-domaines.
    """
    logger.info(f"Démarrage de l’énumération sous-domaines pour {domain}")

    # 1) Brute force classique
    bruteforce_results = brute_force_subdomains(domain)

    # 2) Scraping page d’accueil
    homepage = f"http://{domain}"
    scraped_subdomains = scrape_subdomains_from_page(homepage, domain)

    # Fusion des résultats sans doublons
    combined = set(bruteforce_results) | set(scraped_subdomains)
    logger.info(f"Total sous-domaines trouvés: {len(combined)}")
    return list(combined)

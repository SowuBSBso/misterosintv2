import socket
import re
from utils.logger import logger

def query_whois_server(domain, server):
    response = ""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((server, 43))
        sock.send((domain + "\r\n").encode())
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data.decode(errors="ignore")
        sock.close()
    except Exception as e:
        logger.error(f"Erreur WHOIS serveur {server} : {e}")
    return response

def get_whois(domain):
    # Liste simplifiée serveurs WHOIS selon TLD (à étendre)
    tld = domain.split('.')[-1].lower()
    servers = {
        "com": "whois.verisign-grs.com",
        "net": "whois.verisign-grs.com",
        "org": "whois.pir.org",
        "info": "whois.afilias.net",
        "fr": "whois.afnic.fr",
        # Ajouter d’autres TLD
    }
    server = servers.get(tld, "whois.iana.org")  # fallback

    logger.info(f"Interrogation WHOIS de {domain} sur {server}")
    result = query_whois_server(domain, server)
    if not result or "No match" in result:
        logger.warning(f"Pas d’enregistrement WHOIS trouvé pour {domain}")
        return "Aucun résultat WHOIS trouvé."
    # Nettoyage et simplification
    return result

import socket
import dns.resolver
import dns.reversename
from utils.logger import logger

def query_dns(domain):
    """
    Recherche DNS basique sur le domaine.
    Retourne un dict avec les types d’enregistrements A, MX, TXT, NS, SOA.
    """
    records = {
        "A": [],
        "MX": [],
        "TXT": [],
        "NS": [],
        "SOA": []
    }
    resolver = dns.resolver.Resolver()
    try:
        for record_type in records.keys():
            try:
                answers = resolver.resolve(domain, record_type, lifetime=5)
                for rdata in answers:
                    if record_type == "MX":
                        records[record_type].append(str(rdata.exchange).rstrip('.'))
                    elif record_type == "SOA":
                        records[record_type].append(str(rdata))
                    else:
                        records[record_type].append(str(rdata))
            except Exception as e:
                logger.debug(f"Pas d'enregistrements {record_type} pour {domain}: {e}")
    except Exception as e:
        logger.error(f"Erreur DNS globale pour {domain}: {e}")
    return records

def get_ip_addresses(domain):
    """
    Résout les adresses IP (A) associées au domaine.
    """
    ips = []
    try:
        answers = dns.resolver.resolve(domain, "A", lifetime=5)
        for rdata in answers:
            ips.append(rdata.address)
    except Exception as e:
        logger.error(f"Erreur résolution IP pour {domain}: {e}")
    return ips

def reverse_dns(ip):
    """
    Reverse DNS lookup pour une IP donnée.
    Retourne le hostname associé ou un message d’erreur.
    """
    try:
        rev_name = dns.reversename.from_address(ip)
        answers = dns.resolver.resolve(rev_name, "PTR", lifetime=5)
        hostnames = [str(rdata) for rdata in answers]
        return hostnames
    except Exception as e:
        logger.error(f"Erreur reverse DNS pour {ip}: {e}")
        return [f"Aucun nom PTR trouvé pour {ip}"]


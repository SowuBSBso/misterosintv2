import socket
import ssl
from datetime import datetime
from utils.logger import logger

def get_ssl_certificate_info(hostname, port=443, timeout=5):
    """
    Récupère et analyse le certificat SSL/TLS d’un serveur.
    Renvoie un dict avec les informations clés.
    """
    context = ssl.create_default_context()
    cert_info = {}

    try:
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Parsing des champs principaux
                cert_info['subject'] = dict(x[0] for x in cert.get('subject', []))
                cert_info['issuer'] = dict(x[0] for x in cert.get('issuer', []))
                
                # Dates de validité
                not_before = cert.get('notBefore')
                not_after = cert.get('notAfter')
                cert_info['not_before'] = datetime.strptime(not_before, "%b %d %H:%M:%S %Y %Z") if not_before else None
                cert_info['not_after'] = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z") if not_after else None

                # SAN - Subject Alternative Names
                san = []
                for ext in cert.get('subjectAltName', []):
                    san.append(ext[1])
                cert_info['san'] = san
                
                # Serial Number (pas toujours présent dans dict)
                cert_info['serial_number'] = cert.get('serialNumber', 'N/A')

                logger.info(f"Certificat SSL récupéré pour {hostname}")
    except ssl.SSLError as e:
        logger.error(f"Erreur SSL pour {hostname}: {e}")
        return None
    except socket.error as e:
        logger.error(f"Erreur socket pour {hostname}: {e}")
        return None
    except Exception as e:
        logger.error(f"Erreur inattendue lors récupération certificat SSL pour {hostname}: {e}")
        return None

    return cert_info

def print_cert_info(cert_info):
    """
    Affiche joliment les informations du certificat.
    """
    if not cert_info:
        print("Pas d'information de certificat disponible.")
        return
    
    print("----- Certificat SSL/TLS -----")
    print(f"Sujet : {cert_info.get('subject', {})}")
    print(f"Émetteur : {cert_info.get('issuer', {})}")
    print(f"Valide du : {cert_info.get('not_before')} au {cert_info.get('not_after')}")
    print(f"Noms alternatifs (SAN) : {cert_info.get('san')}")
    print(f"Numéro de série : {cert_info.get('serial_number')}")
    print("------------------------------")

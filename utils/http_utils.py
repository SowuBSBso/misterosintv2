import requests
import time
from utils.logger import logger

def safe_get(url, headers=None, max_retries=3, timeout=10):
    """
    Fonction get HTTP avec gestion simple des erreurs et retries.
    """
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            if resp.status_code == 200:
                return resp
            else:
                logger.debug(f"Code HTTP {resp.status_code} pour {url}")
        except requests.RequestException as e:
            logger.debug(f"Erreur requête {url} attempt {attempt+1}: {e}")
        time.sleep(1)
    logger.error(f"Échec final requête {url}")
    return None

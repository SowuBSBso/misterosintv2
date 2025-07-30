import subprocess
import platform
from utils.logger import logger

def ping_host(host, count=4, timeout=2):
    """
    Ping un hôte (IP ou domaine) et retourne True si répond, False sinon.
    Compatible Windows/Linux/macOS.
    """
    param_count = "-n" if platform.system().lower() == "windows" else "-c"
    param_timeout = "-w" if platform.system().lower() == "windows" else "-W"
    try:
        command = ["ping", param_count, str(count), param_timeout, str(timeout), host]
        logger.info(f"Exécution ping : {' '.join(command)}")
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Erreur ping {host}: {e}")
        return False

def traceroute(host, max_hops=30):
    """
    Effectue un traceroute vers l’hôte donné.
    Retourne la liste des hops sous forme [(hop_number, ip, hostname), ...].
    """
    system = platform.system().lower()
    hops = []

    try:
        if system == "windows":
            command = ["tracert", "-d", host]
        else:
            command = ["traceroute", "-n", "-m", str(max_hops), host]

        logger.info(f"Exécution traceroute : {' '.join(command)}")
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            # Analyse selon OS
            if system == "windows":
                # Ligne Windows exemple:  1    <1 ms    <1 ms    <1 ms  192.168.1.1
                parts = line.split()
                if parts and parts[0].isdigit():
                    hop_num = int(parts[0])
                    ip = parts[-1]
                    hops.append((hop_num, ip, None))
            else:
                # Linux/macOS : 1  192.168.1.1  1.123 ms  1.456 ms  1.789 ms
                parts = line.split()
                if parts and parts[0].isdigit():
                    hop_num = int(parts[0])
                    ip = parts[1]
                    hops.append((hop_num, ip, None))
        proc.wait()
        return hops
    except Exception as e:
        logger.error(f"Erreur traceroute vers {host}: {e}")
        return []

def map_ip_connections(host):
    """
    Renvoie la cartographie simple des connexions IP jusqu’à l’hôte via traceroute.
    Format : liste d’adresses IP en ordre.
    """
    hops = traceroute(host)
    ips = [hop[1] for hop in hops if hop[1] != "*"]
    logger.info(f"Cartographie IP pour {host}: {ips}")
    return ips

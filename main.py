import time
from rich.console import Console
from rich.theme import Theme
from modules import dns_tools
from modules import (
    whois, web_scraping, subdomain_enum, ssl_analysis,
    image_analysis, social_scraping, forum_search, network_tools,
    tech_detection, report_generator
)
from utils.logger import setup_logger

logger = setup_logger()

custom_theme = Theme({
    "title": "bold violet",
    "menu_option": "white",
    "input_prompt": "bold violet",  # Violet pour prompt aussi
    "error": "bold red",
    "success": "bold green",
    "highlight": "bold magenta",
    "prompt_prefix": "bold violet",  # Ligne prompt en violet
})
console = Console(theme=custom_theme)

ASCII_TITLE = r"""
 ____    ____                    ___              _               _    
|_   \  /   _|                 .'   `.           (_)             / |_  
  |   \/   |    _ .--.        /  .-.  \  .--.    __    _ .--.   `| |-' 
  | |\  /| |   [ `/'`\]       | |   | | ( (`\]  [  |  [ `.-. |   | |   
 _| |_\/_| |_   | |      _    \  `-'  /  `'.'.   | |   | | | |   | |,  
|_____||_____| [___]    (_)    `.___.'  [\__) ) [___] [___||__]  \__/ 
"""

def print_title():
    console.print(ASCII_TITLE, style="title", justify="center")
    console.print()  # ligne vide

def main_menu():
    console.print("[input_prompt]Choisir une option :[/input_prompt]\n", justify="left")

    options = [
        "1. Recherche WHOIS",
        "2. Recherche DNS (A, MX, TXT, NS, SOA)",
        "3. Recherche IP liées à un domaine",
        "4. Reverse DNS lookup",
        "5. Analyse page web (emails, téléphone, liens)",
        "6. Recherche sous-domaines",
        "7. Analyse certificat SSL/TLS",
        "8. Extraction métadonnées images",
        "9. Scraping profils sociaux publics",
        "10. Recherche mentions forums/blogs",
        "11. Traceroute / Ping",
        "12. Analyse technologies web",
        "13. Analyse fichiers robots.txt / sitemap.xml",
        "14. Quitter",
    ]

    for opt in options:
        console.print(f"[menu_option]{opt}[/menu_option]", justify="left")

    console.print()  # ligne vide

    user = "unknow"
    host = "misterosintv2"
    cwd = "~/Windows/Menu"
    top_line = f"┌──({user}@{host})─[{cwd}]"
    bottom_line = "└─$ "

    console.print(top_line, style="prompt_prefix")
    choice = input(bottom_line)
    return choice.strip()

def main():
    while True:
        console.clear()  # Nettoyer l'écran à chaque boucle
        print_title()

        choice = main_menu()
        if choice == "1":
            domain = input("Entrer un nom de domaine: ").strip()
            result = whois.get_whois(domain)
            console.print(result, style="success")
        elif choice == "2":
            domain = input("Entrer un nom de domaine: ").strip()
            result = dns_tools.query_dns(domain)
            console.print(result, style="success")
        elif choice == "3":
            domain = input("Entrer un nom de domaine: ").strip()
            ips = dns_tools.get_ip_addresses(domain)
            console.print(f"IPs: {ips}", style="success")
        elif choice == "4":
            ip = input("Entrer une adresse IP: ").strip()
            result = dns_tools.reverse_dns(ip)
            console.print(result, style="success")
        elif choice == "5":
            url = input("Entrer URL (avec http(s)://): ").strip()
            page_content = web_scraping.fetch_page(url)
            if page_content:
                emails = web_scraping.extract_emails(page_content)
                phones = web_scraping.extract_phone_numbers(page_content)
                links = web_scraping.extract_outgoing_links(page_content, url)
                console.print(f"Emails: {emails}", style="success")
                console.print(f"Téléphones: {phones}", style="success")
                console.print(f"Liens sortants: {links}", style="success")
            else:
                console.print("Erreur récupération de la page.", style="error")
        elif choice == "6":
            domain = input("Entrer un nom de domaine: ").strip()
            subdomains = subdomain_enum.find_subdomains(domain)
            console.print(f"Sous-domaines: {subdomains}", style="success")
        elif choice == "7":
            domain = input("Entrer un nom de domaine: ").strip()
            ssl_info = ssl_analysis.analyze_ssl(domain)
            console.print(ssl_info, style="success")
        elif choice == "8":
            path = input("Entrer le chemin vers une image: ").strip()
            meta = image_analysis.extract_metadata(path)
            console.print(meta, style="success")
        elif choice == "9":
            pseudo = input("Entrer un pseudo ou email: ").strip()
            profiles = social_scraping.scrape_profiles(pseudo)
            console.print(profiles, style="success")
        elif choice == "10":
            term = input("Entrer un terme à rechercher dans forums/blogs: ").strip()
            mentions = forum_search.search_mentions(term)
            console.print(mentions, style="success")
        elif choice == "11":
            host = input("Entrer une IP ou domaine: ").strip()
            # Traceroute
            hops = network_tools.traceroute(host)
            if hops:
                console.print("[highlight]Traceroute résultats:[/highlight]")
                for hop_num, ip_addr, hostname in hops:
                    console.print(f"{hop_num}: {ip_addr} {hostname if hostname else ''}")
            else:
                console.print("Erreur ou aucun résultat pour le traceroute.", style="error")

            # Ping
            ping_result = network_tools.ping_host(host)
            if ping_result:
                console.print(f"Ping réussi pour {host}", style="success")
            else:
                console.print(f"Ping échoué pour {host}", style="error")
        elif choice == "12":
            url = input("Entrer URL (avec http(s)://): ").strip()
            techs = tech_detection.detect_technologies(url)
            console.print(f"Technologies détectées: {techs}", style="success")
        elif choice == "13":
            domain = input("Entrer un nom de domaine (ex: example.com): ").strip()
            robots = web_scraping.fetch_robots_txt(domain)
            sitemap = web_scraping.fetch_sitemap_xml(domain)
            console.print("[highlight]robots.txt:[/highlight]\n" + (robots or "Aucun contenu trouvé"))
            console.print("[highlight]sitemap.xml:[/highlight]\n" + (sitemap or "Aucun contenu trouvé"))
        elif choice == "14":
            console.print("Bye!", style="highlight")
            break
        else:
            console.print("Option invalide.", style="error")

        input("\nAppuyez sur [ENTER] pour revenir au menu principal...")

if __name__ == "__main__":
    main()

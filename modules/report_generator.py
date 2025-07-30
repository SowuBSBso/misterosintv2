import datetime
from utils.logger import logger

def generate_text_report(data, filename="rapport_osint.txt"):
    """
    Génère un rapport texte simple à partir d’un dict de données.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Rapport OSINT généré le {datetime.datetime.now()}\n\n")
            for section, content in data.items():
                f.write(f"=== {section.upper()} ===\n")
                if isinstance(content, dict):
                    for key, value in content.items():
                        f.write(f"{key}: {value}\n")
                elif isinstance(content, list):
                    for item in content:
                        f.write(f"- {item}\n")
                else:
                    f.write(str(content) + "\n")
                f.write("\n")
        logger.info(f"Rapport texte généré : {filename}")
        return filename
    except Exception as e:
        logger.error(f"Erreur génération rapport texte: {e}")
        return None

def generate_html_report(data, filename="rapport_osint.html"):
    """
    Génère un rapport HTML simple à partir d’un dict de données.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"<html><head><meta charset='utf-8'><title>Rapport OSINT</title></head><body>")
            f.write(f"<h1>Rapport OSINT généré le {datetime.datetime.now()}</h1>")

            for section, content in data.items():
                f.write(f"<h2>{section}</h2>")
                if isinstance(content, dict):
                    f.write("<ul>")
                    for key, value in content.items():
                        f.write(f"<li><strong>{key}:</strong> {value}</li>")
                    f.write("</ul>")
                elif isinstance(content, list):
                    f.write("<ul>")
                    for item in content:
                        f.write(f"<li>{item}</li>")
                    f.write("</ul>")
                else:
                    f.write(f"<p>{content}</p>")

            f.write("</body></html>")
        logger.info(f"Rapport HTML généré : {filename}")
        return filename
    except Exception as e:
        logger.error(f"Erreur génération rapport HTML: {e}")
        return None

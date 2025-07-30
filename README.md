# Mister OSINT - v2

<img width="1697" height="832" alt="Capture d'écran 2025-07-30 172104" src="https://github.com/user-attachments/assets/06514752-8bbf-43b1-a19f-dd1ff235e5eb" />

*Un outil puissant d’investigation OSINT (Open Source Intelligence)*

---

## Présentation

**Mister OSINT v2** est une suite d’outils d’investigation en sources ouvertes destinée aux chercheurs, analystes, et passionnés de cybersécurité. Ce programme permet d’extraire et d’analyser des informations sur des domaines, adresses IP, sites web, réseaux sociaux, forums, et plus encore.

---

## Fonctionnalités principales

- Recherche WHOIS approfondie
- Résolutions DNS (A, MX, TXT, NS, SOA)
- Résolution d’adresses IP liées à un domaine
- Reverse DNS lookup (recherche PTR)
- Analyse et extraction d’emails, téléphones, liens sur pages web
- Recherche et énumération de sous-domaines
- Analyse SSL/TLS des certificats de site web
- Extraction des métadonnées des images
- Scraping des profils sociaux publics
- Recherche de mentions sur forums et blogs
- Traceroute et Ping réseau (diagnostic de connectivité)
- Analyse des technologies web utilisées (CMS, frameworks, etc.)
- Analyse des fichiers robots.txt et sitemap.xml
- Génération de rapports synthétiques

---

## Installation

1. **Cloner le dépôt :**

   ```bash
   git clone https://github.com/tonrepo/misterosintv2.git
   cd misterosintv2
Installer les dépendances :

Ce projet nécessite Python 3.8+ et les modules listés dans requirements.txt :

bash
Copier
Modifier
pip install -r requirements.txt
Utilisation
Lancez simplement le script principal :

bash
Copier
Modifier
python main.py
Un menu interactif vous guidera à travers les différentes fonctionnalités.

Structure du projet
main.py : Point d’entrée principal, menu interactif.

modules/ : Contient tous les modules fonctionnels (dns_tools, network_tools, whois, etc.)

utils/ : Utilitaires communs (logger, helpers).

requirements.txt : Liste des bibliothèques Python nécessaires.

Notes importantes & Avertissements légaux
Usage responsable uniquement : Cet outil est conçu pour des investigations légales et éthiques, telles que des tests de sécurité sur vos propres systèmes ou des analyses OSINT publiques.

Respect des lois : Il est de votre responsabilité de vous assurer que vous respectez les législations locales et internationales en vigueur concernant la collecte d’informations et la vie privée.

Aucune responsabilité :
L’auteur et les contributeurs de Mister OSINT déclinent toute responsabilité quant à l’utilisation illégale, non autorisée ou abusive de cet outil par des tiers.

Usage éducatif et professionnel : Veuillez toujours obtenir les autorisations nécessaires avant d’exécuter des scans ou analyses sur des systèmes tiers.

Contribution
Les contributions sont les bienvenues !
Merci d’ouvrir une issue ou un pull request pour proposer vos améliorations, corrections ou nouvelles fonctionnalités.

Contact
Pour toute question, merci de me contacter via discord, 452213119.

Merci d’utiliser Mister OSINT v2 !

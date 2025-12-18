"""
Auteurs: Livio Dadone, Gabriel Bragança De Oliveira
Nom du fichier: remove_v2.py
Objectif du programme: Prendre les fichiers avec l'extension .stp et créer à partir de ceux-ci un fichier HTML bien formaté
"""

from pathlib import Path
import html

# Répertoire de base
SCRIPT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = SCRIPT_DIR.parent / "Collection"
LIST_FILE = BASE_DIR / "Collection"
OUTPUT_FILE = SCRIPT_DIR.parent/"outputs"/"Collection2.html"   # version sans mots vides

# Lecture de la liste des documents
doc_ids = []
with LIST_FILE.open(encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            doc_ids.append(line)

# Ouverture du fichier HTML de sortie
with OUTPUT_FILE.open("w", encoding="utf-8") as out:
    out.write("<!DOCTYPE html>\n")
    out.write("<html>\n<head>\n<meta charset=\"utf-8\">\n")
    out.write("<title>Collection2 - CACM (sans mots vides)</title>\n</head>\n<body>\n")

    for doc_id in doc_ids:

        # Parcourt seulement les fichiers texte et non les fichiers HTML
        if not doc_id.startswith("CACM"):
            continue
        
        # Version filtrée par remove → .stp
        text_path = BASE_DIR / f"{doc_id}.stp"
        if not text_path.exists():
            print(f"ATTENTION : fichier manquant {text_path}, ignoré.")
            continue

        # Lecture du texte .stp
        text = text_path.read_text(encoding="utf-8")
        text = html.escape(text)

        # Ajout du numéro du document au début
        texte_final = f"[{doc_id}] " + text

        # Écriture dans un <article> avec classe cacm
        out.write(f"<article class=\"cacm\" id=\"{doc_id}\">\n")
        out.write(texte_final)
        out.write("\n</article>\n\n")

    out.write("</body>\n</html>\n")

print("Créé :", OUTPUT_FILE)

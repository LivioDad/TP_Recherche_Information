"""
Auteurs: Livio Dadone, Gabriel Bragança De Oliveira
Nom du fichier: scrape_cacm_html.py
Objectif du programme:
    Extraire automatiquement le contenu des documents CACM
    à partir des fichiers HTML de la collection.
"""

from pathlib import Path
from bs4 import BeautifulSoup

# Fichier HTML source
HTML_FILE = Path("outputs/Collection2.html")

# Nouveau dossier de collection à créer
OUT_DIR = Path("Collection_html")
OUT_COLLECTION_LIST = OUT_DIR / "Collection"


def extraire_texte_article(article) -> str:
    """
    À adapter à la structure exacte de ton HTML.
    Approche générique :
      - on enlève les balises de mise en forme
      - on récupère le texte brut avec get_text()
    """
    texte = article.get_text(" ", strip=True)
    return texte


def main() -> None:
    if not HTML_FILE.is_file():
        raise SystemExit(f"Fichier HTML introuvable : {HTML_FILE}")

    # Lecture du HTML avec BeautifulSoup
    with HTML_FILE.open("r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Tous les articles CACM
    corpus = soup.find_all("article", class_="cacm-doc")

    # Création du dossier de sortie
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Liste des IDs pour la nouvelle Collection
    ids_docs = []

    for article in corpus:
        doc_id = article.get("id")
        if not doc_id:
            continue

        texte = extraire_texte_article(article)
        if not texte:
            continue

        # Fichier de sortie pour ce document
        out_file = OUT_DIR / f"{doc_id}.txt"
        out_file.write_text(texte + "\n", encoding="utf-8")

        ids_docs.append(doc_id)

    # Fichier liste de documents, style "Collection"
    with OUT_COLLECTION_LIST.open("w", encoding="utf-8") as f:
        for doc_id in ids_docs:
            f.write(doc_id + "\n")

    print(f"{len(ids_docs)} documents extraits dans {OUT_DIR}")


if __name__ == "__main__":
    main()

"""
porter_lemmatise_cacm.py

Crée une troisième version de la collection CACM à partir du HTML,
en appliquant le stemmer de Porter (NLTK) sur le texte des articles.

Entrée :
  - outputs/CollectionX.html   (balises <article class="cacm" id="...">)

Sortie :
  - Dossier "Collection_porter/"
       * <ID>.stp       : texte stemmé par Porter
       * Collection     : liste des IDs de docs
"""

from pathlib import Path
from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer
import re

HTML_FILE = Path("outputs/Collection2.html") # dans 1 il y a les stopwords, dans 2 non 

OUT_DIR = Path("Collection_porter")
OUT_COLLECTION_LIST = OUT_DIR / "Collection"


def extraire_texte_article(article) -> str:
    """Même logique que dans scrape_cacm_html.py."""
    texte = article.get_text(" ", strip=True)
    return texte


def tokenizer_simple(texte: str):
    """
    Tokenisation simple :
      - tout en minuscules
      - enlève ponctuation de base
      - split sur les espaces
    Pour quelque chose de plus riche, on peut utiliser nltk.tokenize.:contentReference[oaicite:4]{index=4}
    """
    texte = texte.lower()
    # Remplacer tout ce qui n'est pas lettre ou chiffre par un espace
    texte = re.sub(r"[^a-z0-9]+", " ", texte)
    tokens = [t for t in texte.split() if t]
    return tokens


def main() -> None:
    if not HTML_FILE.is_file():
        raise SystemExit(f"Fichier HTML introuvable : {HTML_FILE}")

    with HTML_FILE.open("r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    corpus = soup.find_all("article", class_="cacm-doc")


    OUT_DIR.mkdir(parents=True, exist_ok=True)

    stemmer = PorterStemmer()
    ids_docs = []

    for article in corpus:
        doc_id = article.get("id")
        if not doc_id:
            continue

        texte = extraire_texte_article(article)
        if not texte:
            continue

        tokens = tokenizer_simple(texte)

        # Enlever les # pour filtrer les stopwords
        # from nltk.corpus import stopwords
        # stops = set(stopwords.words("english"))
        # tokens = [t for t in tokens if t not in stops]

        stems = [stemmer.stem(t) for t in tokens]
        texte_stem = " ".join(stems)

        out_file = OUT_DIR / f"{doc_id}.stp"
        out_file.write_text(texte_stem + "\n", encoding="utf-8")

        ids_docs.append(doc_id)

    with OUT_COLLECTION_LIST.open("w", encoding="utf-8") as f:
        for doc_id in ids_docs:
            f.write(doc_id + "\n")

    print(f"{len(ids_docs)} documents stemmés écrits dans {OUT_DIR}")


if __name__ == "__main__":
    main()

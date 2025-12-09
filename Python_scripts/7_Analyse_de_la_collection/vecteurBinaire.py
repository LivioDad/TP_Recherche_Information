"""
vecteurBinaire.py

Construit la représentation vectorielle binaire des documents.

Entrées :
  - "vocabulaire.txt" : un mot par ligne.
  - "Collection/Collection" : liste des documents (ex : CACM-0001).
  - "Collection/<doc>.stp" : textes nettoyés et sans mots vides.

Sortie :
  - "vecteurBinaire.txt" : une ligne par document.
    Chaque ligne contient les couples "idTerme:1" triés par idTerme,
    par exemple : 1:1 3:1 7:1
"""

from pathlib import Path

# Constantes de chemins
COLLECTION_DIR = Path("Collection")
DOC_LIST_FILE = COLLECTION_DIR / "Collection"
VOCAB_FILE = Path("outputs/vocabulaire.txt")
OUTPUT_FILE = Path("outputs/vecteurBinaire.txt")


def charger_vocabulaire(path_vocab: Path) -> dict:
    """
    Charge le vocabulaire depuis 'vocabulaire.txt' et
    renvoie un dictionnaire {mot: idTerme}, avec idTerme à partir de 1.
    """
    mots = []

    with path_vocab.open("r", encoding="utf-8") as f:
        for line in f:
            mot = line.strip()
            if mot:
                mots.append(mot)

    # numérotation des termes à partir de 1
    index_vocab = {mot: i + 1 for i, mot in enumerate(mots)}
    return index_vocab


def vecteur_binaire_pour_document(doc_path: Path, index_vocab: dict) -> str:
    """
    Construit la représentation binaire pour un document donné.

    Retourne une chaîne de la forme "id1:1 id2:1 id3:1 ..."
    """
    texte = doc_path.read_text(encoding="utf-8", errors="ignore")
    mots = texte.split()

    # Ensemble des mots uniques dans le document
    mots_doc = set(mots)

    # Ensemble des indices de termes présents dans ce document
    indices_doc = set()

    for mot in mots_doc:
        if mot in index_vocab:
            indices_doc.add(index_vocab[mot])

    # On trie les indices pour avoir un ordre déterministe
    indices_tries = sorted(indices_doc)

    # Construction de la ligne "id:1 id:1 ..."
    couples = [f"{idx}:1" for idx in indices_tries]
    return " ".join(couples)


def main() -> None:
    # Vérification de l'existence du dossier Collection
    if not COLLECTION_DIR.is_dir():
        raise SystemExit(f"Dossier introuvable : {COLLECTION_DIR}")

    # Chargement du vocabulaire
    if not VOCAB_FILE.is_file():
        raise SystemExit(f"Fichier vocabulaire introuvable : {VOCAB_FILE}")
    index_vocab = charger_vocabulaire(VOCAB_FILE)

    # Ouverture des fichiers de liste de docs et de sortie
    if not DOC_LIST_FILE.is_file():
        raise SystemExit(f"Fichier de liste de documents introuvable : {DOC_LIST_FILE}")

    with DOC_LIST_FILE.open("r", encoding="utf-8") as f_docs, \
         OUTPUT_FILE.open("w", encoding="utf-8") as f_out:

        for line in f_docs:
            nom_doc = line.strip()
            if not nom_doc:
                continue

            # On suppose que le texte filtré est dans "Collection/<nom>.stp"
            doc_path = COLLECTION_DIR / f"{nom_doc}.stp"

            if not doc_path.is_file():
                # On peut choisir de sauter ou d'afficher un avertissement
                # Ici on saute silencieusement
                continue

            vecteur = vecteur_binaire_pour_document(doc_path, index_vocab)
            f_out.write(vecteur + "\n")


if __name__ == "__main__":
    main()

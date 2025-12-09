"""
vecteurTF.py

Construit la représentation vectorielle en fréquence (tf) des documents.

Entrées :
  - "vocabulaire.txt" : un mot par ligne.
  - "Collection/Collection" : liste des documents (ex : CACM-0001).
  - "Collection/<doc>.stp" : textes nettoyés et sans mots vides.

Sortie :
  - "vecteurTF.txt" : une ligne par document.
    Chaque ligne contient les couples "idTerme:tf" triés par idTerme,
    par exemple : 1:2 3:5 7:1
"""

from pathlib import Path

COLLECTION_DIR = Path("Collection")
DOC_LIST_FILE = COLLECTION_DIR / "Collection"
VOCAB_FILE = Path("outputs/vocabulaire.txt")
OUTPUT_FILE = Path("outputs/vecteurTF.txt")


def charger_vocabulaire(path_vocab: Path) -> dict:
    """Retourne un dict {mot: idTerme} avec idTerme à partir de 1."""
    mots = []
    with path_vocab.open("r", encoding="utf-8") as f:
        for line in f:
            mot = line.strip()
            if mot:
                mots.append(mot)
    return {mot: i + 1 for i, mot in enumerate(mots)}


def vecteur_tf_pour_document(doc_path: Path, index_vocab: dict) -> str:
    """
    Construit la représentation TF pour un document :
    renvoie une chaîne "id1:tf1 id2:tf2 ..."
    """
    texte = doc_path.read_text(encoding="utf-8", errors="ignore")
    mots = texte.split()

    # compteur idTerme -> fréquence dans ce document
    counter = {}

    for mot in mots:
        if mot in index_vocab:
            idx = index_vocab[mot]
            counter[idx] = counter.get(idx, 0) + 1

    # indices triés pour une sortie déterministe
    indices_tries = sorted(counter.keys())
    couples = [f"{idx}:{counter[idx]}" for idx in indices_tries]
    return " ".join(couples)


def main() -> None:
    if not COLLECTION_DIR.is_dir():
        raise SystemExit(f"Dossier introuvable : {COLLECTION_DIR}")
    if not VOCAB_FILE.is_file():
        raise SystemExit(f"Fichier vocabulaire introuvable : {VOCAB_FILE}")
    if not DOC_LIST_FILE.is_file():
        raise SystemExit(f"Fichier de liste de documents introuvable : {DOC_LIST_FILE}")

    index_vocab = charger_vocabulaire(VOCAB_FILE)

    with DOC_LIST_FILE.open("r", encoding="utf-8") as f_docs, \
         OUTPUT_FILE.open("w", encoding="utf-8") as f_out:

        for line in f_docs:
            nom_doc = line.strip()
            if not nom_doc:
                continue

            doc_path = COLLECTION_DIR / f"{nom_doc}.stp"
            if not doc_path.is_file():
                # Document filtré manquant -> on saute
                continue

            vecteur = vecteur_tf_pour_document(doc_path, index_vocab)
            f_out.write(vecteur + "\n")


if __name__ == "__main__":
    main()

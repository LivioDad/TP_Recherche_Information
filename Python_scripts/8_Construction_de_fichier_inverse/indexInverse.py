"""
Auteurs: Livio Dadone, Gabriel Bragança De Oliveira
Nom du fichier: indexInverse.py
Objectif du programme:
    Construire un index inversé associant chaque terme du vocabulaire
    à la liste des documents dans lesquels il apparaît.
"""


from pathlib import Path

# Chemins
COLLECTION_DIR = Path("Collection")
DOC_LIST_FILE = COLLECTION_DIR / "Collection"
VOCAB_FILE = Path("outputs/vocabulaire.txt")
OUTPUT_FILE = Path("outputs/indexInverse.txt")


def charger_vocabulaire(path_vocab: Path):
    """
    Charge le vocabulaire et retourne :
      - index_vocab : dict {mot: idTerme}
      - id_to_mot   : dict {idTerme: mot}
    """
    mots = []
    with path_vocab.open("r", encoding="utf-8") as f:
        for line in f:
            mot = line.strip()
            if mot:
                mots.append(mot)

    index_vocab = {mot: i + 1 for i, mot in enumerate(mots)}
    id_to_mot = {i + 1: mot for i, mot in enumerate(mots)}
    return index_vocab, id_to_mot


def charger_liste_docs(path_doc_list: Path):
    """
    Retourne une liste de noms de documents (sans suffixe .stp),
    dans l'ordre où ils apparaissent dans Collection/Collection.
    """
    noms_docs = []
    with path_doc_list.open("r", encoding="utf-8") as f:
        for line in f:
            nom = line.strip()
            if nom:
                noms_docs.append(nom)
    return noms_docs


def construire_paires(index_vocab: dict, noms_docs: list):
    """
    Phase 1 : extraction des paires (idTerme, idDoc)
    en parcourant tous les documents.
    """
    paires = []  # liste de tuples (idTerme, idDoc)

    for id_doc, nom_doc in enumerate(noms_docs, start=1):
        doc_path = COLLECTION_DIR / f"{nom_doc}.stp"
        if not doc_path.is_file():
            continue

        texte = doc_path.read_text(encoding="utf-8", errors="ignore")
        mots = texte.split()

        for mot in mots:
            if mot in index_vocab:
                id_terme = index_vocab[mot]
                paires.append((id_terme, id_doc))

    return paires


def construire_index_inverse(paires: list, nb_termes: int):
    """
    Phases 2 et 3 :
      - tri des paires (idTerme, idDoc),
      - regroupement pour construire l'index inversé.

    Retourne un dict {idTerme: [liste triée de docIDs]}.
    """
    # Tri par idTerme puis idDoc
    paires.sort()  # tri lexicographique (idTerme, idDoc)

    index_inv = {i: [] for i in range(1, nb_termes + 1)}

    prev_terme = None
    prev_doc = None

    for id_terme, id_doc in paires:
        # éviter les doublons (même terme, même doc)
        if id_terme == prev_terme and id_doc == prev_doc:
            continue

        index_inv[id_terme].append(id_doc)
        prev_terme = id_terme
        prev_doc = id_doc

    return index_inv


def main() -> None:
    # Vérifications de base
    if not COLLECTION_DIR.is_dir():
        raise SystemExit(f"Dossier introuvable : {COLLECTION_DIR}")
    if not VOCAB_FILE.is_file():
        raise SystemExit(f"Fichier vocabulaire introuvable : {VOCAB_FILE}")
    if not DOC_LIST_FILE.is_file():
        raise SystemExit(f"Fichier de liste de documents introuvable : {DOC_LIST_FILE}")

    # Chargement vocabulaire et docs
    index_vocab, id_to_mot = charger_vocabulaire(VOCAB_FILE)
    noms_docs = charger_liste_docs(DOC_LIST_FILE)
    nb_termes = len(id_to_mot)

    # 1. Extraction des paires (idTerme, idDoc)
    paires = construire_paires(index_vocab, noms_docs)

    # 2–3. Tri + regroupement
    index_inv = construire_index_inverse(paires, nb_termes)

    # Écriture du fichier inversé
    with OUTPUT_FILE.open("w", encoding="utf-8") as f_out:
        for id_terme in range(1, nb_termes + 1):
            mot = id_to_mot[id_terme]
            docs = index_inv.get(id_terme, [])
            # ligne : idTerme mot doc1 doc2 doc3 ...
            if docs:
                docs_str = " ".join(str(d) for d in docs)
                f_out.write(f"{id_terme} {mot} {docs_str}\n")
            else:
                # terme sans occurrences (optionnel)
                f_out.write(f"{id_terme} {mot}\n")


if __name__ == "__main__":
    main()

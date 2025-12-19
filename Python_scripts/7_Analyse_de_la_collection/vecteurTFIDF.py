"""
Auteurs: Livio Dadone, Gabriel Bragança De Oliveira
Nom du fichier: vecteurTFIDF.py
Objectif du programme:
    Construire les vecteurs TF-IDF des documents en combinant
    la fréquence des termes et la fréquence documentaire.
"""


from pathlib import Path
import math

# Chemins
COLLECTION_DIR = Path("Collection")
DOC_LIST_FILE = COLLECTION_DIR / "Collection"
VOCAB_FILE = Path("outputs/vocabulaire.txt")
DF_FILE = Path("outputs/df.txt")
OUTPUT_FILE = Path("outputs/vecteurTFIDF.txt")


def charger_vocabulaire(path_vocab: Path) -> dict:
    """
    Charge le vocabulaire et retourne un dict {mot: idTerme}
    avec idTerme numéroté à partir de 1.
    """
    mots = []
    with path_vocab.open("r", encoding="utf-8") as f:
        for line in f:
            mot = line.strip()
            if mot:
                mots.append(mot)
    return {mot: i + 1 for i, mot in enumerate(mots)}


def charger_df(path_df: Path) -> dict:
    """
    Charge le fichier df.txt et retourne un dict {mot: df}.
    On suppose des lignes "mot df".
    """
    df_mot = {}
    with path_df.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            mot = parts[0]
            try:
                valeur_df = int(parts[1])
            except ValueError:
                continue
            df_mot[mot] = valeur_df
    return df_mot


def compter_documents(path_doc_list: Path) -> int:
    """Compte le nombre de documents dans Collection/Collection."""
    n = 0
    with path_doc_list.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                n += 1
    return n


def construire_idf(index_vocab: dict, df_mot: dict, nb_docs: int) -> dict:
    """
    Construit un dict {idTerme: idf}.
    idf = log(nb_docs / df) si df > 0, sinon 0.
    """
    idf_par_id = {}

    for mot, idx in index_vocab.items():
        df = df_mot.get(mot, 0)
        if df > 0:
            idf = math.log(nb_docs / df)
        else:
            idf = 0.0
        idf_par_id[idx] = idf

    return idf_par_id


def tfidf_pour_document(doc_path: Path, index_vocab: dict, idf_par_id: dict) -> str:
    """
    Construit la représentation tf.idf pour un document :
    renvoie une chaîne "id1:tfidf1 id2:tfidf2 ..."
    """
    texte = doc_path.read_text(encoding="utf-8", errors="ignore")
    mots = texte.split()

    # compteur idTerme -> tf dans ce document
    tf = {}

    for mot in mots:
        if mot in index_vocab:
            idx = index_vocab[mot]
            tf[idx] = tf.get(idx, 0) + 1

    # calcul tf.idf pour chaque idTerme
    valeurs = {}
    for idx, freq in tf.items():
        idf = idf_par_id.get(idx, 0.0)
        valeurs[idx] = freq * idf

    # indices triés pour sortie déterministe
    indices_tries = sorted(valeurs.keys())

    # formatage des valeurs (par ex. 6 décimales)
    couples = [f"{idx}:{valeurs[idx]:.6f}" for idx in indices_tries]
    return " ".join(couples)


def main() -> None:
    # Vérifications de base
    if not COLLECTION_DIR.is_dir():
        raise SystemExit(f"Dossier introuvable : {COLLECTION_DIR}")
    if not VOCAB_FILE.is_file():
        raise SystemExit(f"Fichier vocabulaire introuvable : {VOCAB_FILE}")
    if not DF_FILE.is_file():
        raise SystemExit(f"Fichier df introuvable : {DF_FILE}")
    if not DOC_LIST_FILE.is_file():
        raise SystemExit(f"Fichier de liste de documents introuvable : {DOC_LIST_FILE}")

    # Chargements
    index_vocab = charger_vocabulaire(VOCAB_FILE)
    df_mot = charger_df(DF_FILE)
    nb_docs = compter_documents(DOC_LIST_FILE)
    idf_par_id = construire_idf(index_vocab, df_mot, nb_docs)

    # Construction du fichier tf.idf
    with DOC_LIST_FILE.open("r", encoding="utf-8") as f_docs, \
         OUTPUT_FILE.open("w", encoding="utf-8") as f_out:

        for line in f_docs:
            nom_doc = line.strip()
            if not nom_doc:
                continue

            doc_path = COLLECTION_DIR / f"{nom_doc}.stp"
            if not doc_path.is_file():
                continue

            vecteur = tfidf_pour_document(doc_path, index_vocab, idf_par_id)
            f_out.write(vecteur + "\n")


if __name__ == "__main__":
    main()

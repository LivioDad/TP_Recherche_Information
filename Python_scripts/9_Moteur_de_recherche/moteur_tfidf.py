"""
Moteur de recherche basé sur la pondération tf.idf + similarité cosinus.

Références :
- tf.idf classique avec idf(t) = log(N / df(t)) (Sparck Jones, repris par Savoy).:contentReference[oaicite:2]{index=2}
- Normalisation par le cosinus / produit scalaire sur les vecteurs pondérés.:contentReference[oaicite:3]{index=3}

Entrées :
  - Collection/Collection            : liste des documents (ex. CACM-0001)
  - Collection/<doc>.stp             : texte nettoyé
  - outputs/vocabulaire.txt          : un mot par ligne
  - outputs/df.txt                   : "mot df"
  - outputs/vecteurTF.txt            : "id:tf id:tf ..." une ligne par doc

Usage :
  python moteur_tfidf.py
  (puis saisir une requête en texte libre)
"""

from pathlib import Path
import math

# Chemins
COLLECTION_DIR = Path("Collection")
DOC_LIST_FILE = COLLECTION_DIR / "Collection"
VOCAB_FILE = Path("outputs/vocabulaire.txt")
DF_FILE = Path("outputs/df.txt")
VECT_TF_FILE = Path("outputs/vecteurTF.txt")


def charger_vocabulaire(path_vocab: Path):
    """Retourne deux structures : mot->idTerme, idTerme->mot."""
    mot2id = {}
    id2mot = {}

    with path_vocab.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            mot = line.strip()
            if mot:
                mot2id[mot] = idx
                id2mot[idx] = mot

    return mot2id, id2mot


def charger_df(path_df: Path):
    """Charge df(t) : renvoie dict mot -> df, et N_docs (nb total doc)."""
    df_mot = {}

    with path_df.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # format : "mot df"
            parts = line.split()
            if len(parts) != 2:
                continue
            mot, df_str = parts
            try:
                df = int(df_str)
            except ValueError:
                continue
            df_mot[mot] = df

    # N_docs = max df possible => on le prendra plutôt depuis Collection
    return df_mot


def charger_liste_docs(path_doc_list: Path):
    docs = []
    with path_doc_list.open("r", encoding="utf-8") as f:
        for line in f:
            nom = line.strip()
            if nom:
                docs.append(nom)
    return docs


def charger_vecteurs_tfidf(vect_tf_path: Path,
                           docs,
                           id2mot,
                           df_mot,
                           n_docs: int):
    """
    À partir de vecteurTF.txt et df, calcule les poids tf.idf pour chaque document.
    Renvoie :
      - doc_vectors : liste (par index doc) de dict {idTerme: poids_tfidf}
      - doc_norms   : liste des normes L2 des vecteurs doc
    """
    doc_vectors = []
    doc_norms = []

    with vect_tf_path.open("r", encoding="utf-8") as f:
        for doc_idx, line in enumerate(f):
            line = line.strip()
            if not line:
                # vecteur vide
                doc_vectors.append({})
                doc_norms.append(0.0)
                continue

            tfidf_vec = {}
            for chunk in line.split():
                if ":" not in chunk:
                    continue
                id_str, tf_str = chunk.split(":", 1)
                try:
                    term_id = int(id_str)
                    tf = int(tf_str)
                except ValueError:
                    continue

                mot = id2mot.get(term_id)
                if mot is None:
                    continue

                df = df_mot.get(mot)
                if not df or df == 0:
                    continue

                # idf classique log(N/df)
                idf = math.log(n_docs / df)
                poids = tf * idf
                tfidf_vec[term_id] = poids

            # norme L2
            norm_sq = sum(w * w for w in tfidf_vec.values())
            norm = math.sqrt(norm_sq) if norm_sq > 0 else 0.0

            doc_vectors.append(tfidf_vec)
            doc_norms.append(norm)

    # Sanity check : nombre de lignes == nombre de docs
    if len(doc_vectors) != len(docs):
        print("Attention : nombre de lignes dans vecteurTF.txt différent du nombre de documents.")

    return doc_vectors, doc_norms


def construire_vecteur_requete(query: str,
                               mot2id,
                               df_mot,
                               n_docs: int):
    """
    Construit le vecteur tf.idf de la requête et sa norme.
    Retourne (vec, norm) avec vec : {idTerme: poids_tfidf}.
    """
    # nettoyage minimal (les docs .stp sont déjà en minuscules sans ponctuation)
    mots = query.lower().split()

    # tf dans la requête
    tf_q = {}
    for mot in mots:
        if mot in mot2id:
            tf_q[mot] = tf_q.get(mot, 0) + 1

    vec = {}
    for mot, tf in tf_q.items():
        df = df_mot.get(mot)
        if not df or df == 0:
            continue
        idf = math.log(n_docs / df)
        term_id = mot2id[mot]
        vec[term_id] = tf * idf

    norm_sq = sum(w * w for w in vec.values())
    norm = math.sqrt(norm_sq) if norm_sq > 0 else 0.0
    return vec, norm


def recherche_tfidf(query: str,
                    docs,
                    doc_vectors,
                    doc_norms,
                    mot2id,
                    df_mot,
                    n_docs: int,
                    max_resultats: int = 20):
    """
    Renvoie une liste [(score, nom_doc), ...] triée par score décroissant.
    """
    q_vec, q_norm = construire_vecteur_requete(query, mot2id, df_mot, n_docs)
    if not q_vec or q_norm == 0.0:
        return []

    resultats = []

    for doc_idx, (d_vec, d_norm) in enumerate(zip(doc_vectors, doc_norms)):
        if d_norm == 0.0:
            continue

        # produit scalaire sur les termes de la requête
        num = 0.0
        for term_id, w_q in q_vec.items():
            w_d = d_vec.get(term_id)
            if w_d is not None:
                num += w_q * w_d

        if num <= 0.0:
            continue

        score = num / (q_norm * d_norm)
        if score > 0.0:
            resultats.append((score, docs[doc_idx]))

    # tri décroissant
    resultats.sort(reverse=True, key=lambda x: x[0])
    return resultats[:max_resultats]


def main():
    if not COLLECTION_DIR.is_dir():
        raise SystemExit(f"Dossier introuvable : {COLLECTION_DIR}")
    if not DOC_LIST_FILE.is_file():
        raise SystemExit(f"Fichier introuvable : {DOC_LIST_FILE}")
    if not VOCAB_FILE.is_file():
        raise SystemExit(f"Fichier introuvable : {VOCAB_FILE}")
    if not DF_FILE.is_file():
        raise SystemExit(f"Fichier introuvable : {DF_FILE}")
    if not VECT_TF_FILE.is_file():
        raise SystemExit(f"Fichier introuvable : {VECT_TF_FILE}")

    docs = charger_liste_docs(DOC_LIST_FILE)
    n_docs = len(docs)

    mot2id, id2mot = charger_vocabulaire(VOCAB_FILE)
    df_mot = charger_df(DF_FILE)
    doc_vectors, doc_norms = charger_vecteurs_tfidf(VECT_TF_FILE, docs, id2mot, df_mot, n_docs)

    print("Moteur tf.idf (cosinus). Tapez une requête, ou ligne vide pour quitter.")
    while True:
        try:
            query = input("\nRequête > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nFin.")
            break

        if not query:
            print("Fin.")
            break

        res = recherche_tfidf(query, docs, doc_vectors, doc_norms,
                              mot2id, df_mot, n_docs, max_resultats=20)

        if not res:
            print("Aucun document trouvé.")
            continue

        print("\nTop documents :")
        for score, nom_doc in res:
            # On construit un lien HTML vers le fichier local
            lien = f"Collection/{nom_doc}.stp"
            print(f"- {nom_doc}  (score = {score:.4f})  -> {lien}")


if __name__ == "__main__":
    main()

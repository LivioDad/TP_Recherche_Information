"""
Moteur de recherche basé sur la proximité floue (Annabelle Mercier, Michel Beigbeder).

Idée :
  - Chaque occurrence d'un terme de la requête a une "zone d'influence" (fonction triangulaire).
  - À chaque position x du document, on garde la proximité max aux occurrences
    de tous les termes de la requête : p_q^d(x).
  - Score du document : s(q,d) = somme_x p_q^d(x).

Entrées :
  - Collection/Collection   : liste des documents
  - Collection/<doc>.stp    : texte nettoyé, tokens séparés par des espaces

Usage :
  python moteur_proximite.py            # k = 5 par défaut
  python moteur_proximite.py 10         # k = 10

Puis saisir une requête en texte libre.
"""

from pathlib import Path
import sys

COLLECTION_DIR = Path("Collection")
DOC_LIST_FILE = COLLECTION_DIR / "Collection"


def charger_liste_docs(path_doc_list: Path):
    docs = []
    with path_doc_list.open("r", encoding="utf-8") as f:
        for line in f:
            nom = line.strip()
            if nom:
                docs.append(nom)
    return docs


def lire_tokens_doc(doc_name: str):
    """
    Lit Collection/<doc>.stp et renvoie la liste de tokens (mots).
    On suppose que le fichier est déjà nettoyé (minuscules, pas de ponctuation).
    """
    path = COLLECTION_DIR / f"{doc_name}.stp"
    try:
        texte = path.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return []
    # split() suffit : les .stp sont déjà filtrés
    return texte.split()


def score_proximite_fuzzy(tokens, query_terms, k: int):
    """
    Implémentation simplifiée de la proximité floue pour une requête "OU" de mots-clés.

    - query_terms : ensemble de termes de la requête (minuscules).
    - k : paramètre de largeur de la zone d'influence (en nombre de termes).

    Retourne un score réel >= 0.
    """
    if not tokens or not query_terms:
        return 0.0

    L = len(tokens)
    # Proximité p_q^d(x) pour chaque position x
    prox = [0.0] * L

    # Pour chaque position où un terme de la requête apparaît,
    # on ajoute une "pyramide" triangulaire de largeur k.
    for pos, mot in enumerate(tokens):
        if mot not in query_terms:
            continue

        # Influence triangulaire pour cette occurrence
        # f(delta) = max((k - |delta|) / k, 0) pour |delta| < k
        start = max(0, pos - (k - 1))
        end = min(L, pos + (k - 1) + 1)

        for x in range(start, end):
            delta = abs(x - pos)
            val = (k - delta) / k  # > 0 car delta < k
            if val > prox[x]:
                prox[x] = val

    # Score = somme des proximités locales
    return sum(prox)


def recherche_proximite(query: str, docs, k: int, max_resultats: int = 20):
    """
    Retourne liste [(score, nom_doc), ...] triée par score décroissant.
    """
    # requête : ensemble de mots en minuscules
    query_terms = {w for w in query.lower().split() if w}

    resultats = []
    for nom_doc in docs:
        tokens = lire_tokens_doc(nom_doc)
        if not tokens:
            continue

        score = score_proximite_fuzzy(tokens, query_terms, k)
        if score > 0.0:
            resultats.append((score, nom_doc))

    resultats.sort(reverse=True, key=lambda x: x[0])
    return resultats[:max_resultats]


def main():
    if not COLLECTION_DIR.is_dir():
        raise SystemExit(f"Dossier introuvable : {COLLECTION_DIR}")
    if not DOC_LIST_FILE.is_file():
        raise SystemExit(f"Fichier introuvable : {DOC_LIST_FILE}")

    # Paramètre k : portée de l'influence des occurrences
    # k ~ 5 => proximité type "expression", k ~ 15–30 => "phrase".:contentReference[oaicite:8]{index=8}
    if len(sys.argv) >= 2:
        try:
            k = int(sys.argv[1])
        except ValueError:
            raise SystemExit("Usage : python moteur_proximite.py [k]")
    else:
        k = 5

    docs = charger_liste_docs(DOC_LIST_FILE)

    print(f"Moteur à proximité floue (k = {k}). Tapez une requête, ou ligne vide pour quitter.")
    while True:
        try:
            query = input("\nRequête > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nFin.")
            break

        if not query:
            print("Fin.")
            break

        res = recherche_proximite(query, docs, k, max_resultats=20)

        if not res:
            print("Aucun document trouvé.")
            continue

        print("\nTop documents (proximité floue) :")
        for score, nom_doc in res:
            lien = f"Collection/{nom_doc}.stp"
            print(f"- {nom_doc}  (score = {score:.4f})  -> {lien}")


if __name__ == "__main__":
    main()

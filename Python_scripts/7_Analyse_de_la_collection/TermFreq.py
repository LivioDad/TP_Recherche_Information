"""
Auteurs: Livio Dadone, Gabriel Bragança De Oliveira
Nom du fichier: TermFreq.py
Objectif du programme:
Calculer, pour un ou plusieurs termes, la moyenne d'apparitions
dans les documents où ils apparaissent (version générique par type de fichier).
"""

from pathlib import Path

# Répertoires et fichiers
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent / "Collection"
OUTPUT_FILE = SCRIPT_DIR.parent / "outputs" / "termfreq.txt"

# Choisir la version des fichiers à analyser : ".stp" (sans mots vides) ou ".flt" (nettoyés)
INPUT_FILE_TYPE = ".stp"

# Liste des termes à tester
TERMS = [
    "algorithm",
    "system",
    "computer",
]

# Ouverture du fichier de sortie
with OUTPUT_FILE.open("a", encoding="utf-8") as out:

    # Petite separation pour une nouvelle série de tests
    out.write("\n# Nouvelle série de mesures (fichiers " + INPUT_FILE_TYPE + ")\n")

    for term in TERMS:
        total_occurrences = 0   # nombre total de fois où le terme apparaît
        docs_with_term = 0      # nombre de documents contenant le terme au moins une fois

        # Parcourir la collection
        for fichier in BASE_DIR.iterdir():

            # On ne s'intéresse qu'aux fichiers CACM
            if not fichier.name.startswith("CACM"):
                continue

            # Filtrer par extension (.stp ou .flt)
            if not fichier.name.endswith(INPUT_FILE_TYPE):
                continue

            # Lire le contenu du fichier
            with fichier.open(encoding="utf-8") as f:
                contenu = f.read()

            # Découper en mots
            mots = contenu.split()

            # Compter les occurrences du terme dans ce document
            count_in_doc = 0
            for mot in mots:
                if mot == term:
                    count_in_doc += 1

            # Mettre à jour les compteurs globaux
            if count_in_doc > 0:
                docs_with_term += 1
                total_occurrences += count_in_doc

        # Calcul de la moyenne
        if docs_with_term > 0:
            moyenne = total_occurrences / docs_with_term
        else:
            # Le terme n'apparaît dans aucun document
            moyenne = 0.0

        # Écriture dans le fichier de sortie
        # Format: terme total_occurrences docs_with_term moyenne
        out.write(f"{term} {total_occurrences} {docs_with_term} {moyenne:.4f}\n")

        # Affichage pour vérification
        print(f"Terme : {term}")
        print("  Total d'occurrences      :", total_occurrences)
        print("  Nombre de documents      :", docs_with_term)
        print("  Moyenne par document     :", moyenne)
        print("-" * 40)
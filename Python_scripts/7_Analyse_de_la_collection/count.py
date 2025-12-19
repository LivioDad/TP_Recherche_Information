"""
Auteurs: Livio Dadone, Gabriel Bragança De Oliveira
Nom du fichier: count.py
Objectif du programme: Compter le nombre d'occurrences de chaque mot dans la collection
et écrire dans counter.txt les lignes: rang  compte  mot, triées par fréquence décroissante.
"""

from pathlib import Path

# Répertoires et fichiers
SCRIPT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = SCRIPT_DIR.parent / "Collection"
OUTPUT_FILE = SCRIPT_DIR.parent / "outputs" / "counter.txt"

# Choisir le type de fichiers à analyser : ".stp" (sans mots vides) ou ".flt" (nettoyés)
INPUT_FILE_TYPE = ".stp"

# Dictionnaire des comptes globaux: mot -> nombre total d'occurrences
counter = {}

# Parcourir tous les fichiers de la collection
for fichier in BASE_DIR.iterdir():

    # On ne s'intéresse qu'aux fichiers CACM
    if not fichier.name.startswith("CACM"):
        continue

    # On filtre par extension (.stp ou .flt)
    if not fichier.name.endswith(INPUT_FILE_TYPE):
        continue

    # Lecture du contenu du document
    with fichier.open(encoding="utf-8") as f:
        contenu = f.read()

    # Découper en mots (séparateur: espaces/blancs)
    mots = contenu.split()

    # Mettre à jour le compteur global pour chaque mot (on garde toutes les occurrences)
    for mot in mots:
        if mot == "":
            continue
        if mot not in counter:
            counter[mot] = 1
        else:
            counter[mot] += 1

# Optionnel: suppression d'un éventuel mot parasite "cacm" dans les .stp
if INPUT_FILE_TYPE == ".stp" and "cacm" in counter:
    del counter["cacm"]

# Trier les mots par fréquence décroissante
# Chaque élément est un tuple (mot, compte)
counter_tries = sorted(counter.items(), key=lambda x: x[1], reverse=True)

# Écrire les résultats dans counter.txt sous la forme:
# rang compte mot
with OUTPUT_FILE.open("w", encoding="utf-8") as out:
    rang = 1
    for mot, compte in counter_tries:
        out.write(f"{rang} {compte} {mot}\n")
        rang += 1

print("Fichier counter.txt créé avec", len(counter), "mots différents.")
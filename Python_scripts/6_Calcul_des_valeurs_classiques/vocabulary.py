"""
Auteurs: Livio Dadone, Gabriel Bragança De Oliveira
Nom du fichier: vocabulary.py
Objectif du programme:
    Construire le vocabulaire de la collection en extrayant l’ensemble des mots distincts
    à partir des documents textuels.
"""

from pathlib import Path

vocabulaire = []
SCRIPT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = SCRIPT_DIR.parent / "Collection"
OUTPUT_FILE = SCRIPT_DIR.parent/"outputs"/"vocabulaire.txt"

# Parcourir uniquement les fichiers .flt
for fichier in BASE_DIR.iterdir():
    # Parcourt seulement les fichiers texte et non les fichiers HTML
    if not fichier.name.startswith("CACM"):
        continue

    if not fichier.name.endswith(".flt"):
        continue

    with fichier.open(encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            mots = ligne.split(" ")

            for mot in mots:
                if mot == "":
                    continue
                if mot not in vocabulaire:
                    vocabulaire.append(mot)

# Trier le vocabulaire en ordre alphabétique
vocabulaire.sort()

# Écrire dans vocabulaire.txt
with OUTPUT_FILE.open("w", encoding="utf-8") as out:
    for mot in vocabulaire:
        out.write(mot + "\n")

print("Fichier vocabulaire.txt créé avec", len(vocabulaire), "mots.")

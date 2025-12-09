from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent / "Collection"
OUTPUT_FILE = SCRIPT_DIR.parent/"outputs"/"df.txt"
INPUT_FILE_TYPE = ".stp" # Choisir entre ".stp" et ".flt"
df = {}

for fichier in BASE_DIR.iterdir():

    if not fichier.name.startswith("CACM"):
        continue
    if not fichier.name.endswith(INPUT_FILE_TYPE):
        continue

    with fichier.open(encoding="utf-8") as f:
        contenu = f.read()

    # Extraire les mots du document
    mots = contenu.split()

    # Conserver chaque mot une seule fois par document
    mots_uniques = set(mots)

    # Mettre à jour le dictionnaire df
    for mot in mots_uniques:
        if mot not in df:
            df[mot] = 1
        else:
            df[mot] += 1

if INPUT_FILE_TYPE == ".stp":
    df.pop("cacm")

# Trier par fréquence documentaire décroissante
df_tries = sorted(df.items(), key=lambda x: x[1], reverse=True)

# Écrire les résultats TRIÉS dans df.txt
with OUTPUT_FILE.open("w", encoding="utf-8") as out:
    for mot, freq in df_tries:
        out.write(f"{mot} {freq}\n")

print("Fichier df.txt créé avec", len(df), "mots.")
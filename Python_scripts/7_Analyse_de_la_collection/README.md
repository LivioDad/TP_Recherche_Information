# 7 — Analyse de la collection

Auteurs : **Livio Dadone**, **Gabriel Bragança De Oliveira**

## Objectif
Analyser la collection :
- fréquence des termes, terme(s) les plus fréquents,
- visualisation de la **loi de Zipf**,
- création de représentations vectorielles (binaire, TF, TF-IDF). fileciteturn1file1

## Scripts
### `count.py`
- Compte le nombre d’occurrences de chaque mot dans la collection
- **Sortie** : `outputs/counter.txt` (rang, compte, mot)

```bash
python count.py
```

### `TermFreq.py`
- Calcule la moyenne d’apparition d’un terme (quand il apparaît dans un document)
- **Sortie** : `outputs/termfreq.txt`

```bash
python TermFreq.py
```

### `zipf_plot.py`
- Trace fréquence (y) vs rang (x) à partir des résultats de `count.py`
- **Sortie** : `outputs/zipf_plot.png`

```bash
python zipf_plot.py
```

### `vecteurBinaire.py`
- Produit une représentation binaire par document (format `idTerme:1`)
- **Sortie** : `outputs/vecteurBinaire.txt`

```bash
python vecteurBinaire.py
```

### `vecteurTF.py`
- Produit une représentation TF (format `idTerme:tf`)
- **Sortie** : `outputs/vecteurTF.txt`

```bash
python vecteurTF.py
```

### `vecteurTFIDF.py`
- Produit TF-IDF (format `idTerme:tfidf`) en utilisant `df`
- **Sortie** : `outputs/vecteurTFIDF.txt`

```bash
python vecteurTFIDF.py
```

## Notes importantes
- Ces scripts utilisent typiquement `outputs/vocabulaire.txt` et `outputs/df.txt` : exécuter d’abord le dossier `6_...`.
- Supprimer `tempCodeRunnerFile.py` de la version finale (fichier VSCode, non demandé).

# 6 - Calcul des valeurs classiques (Vocabulaire & DF)

Auteurs : **Livio Dadone**, **Gabriel Bragança De Oliveira**

## Objectif
Calculer les valeurs de base pour la RI :
- **vocabulaire** de la collection (un mot par ligne),
- **df** (document frequency) : pour chaque terme, le nombre de documents qui le contiennent. fileciteturn1file1

## Scripts
### `vocabulary.py`
- **Entrée** : documents de la collection (version choisie, typiquement `.stp`)
- **Sortie** : `outputs/vocabulaire.txt` (un mot par ligne)

```bash
python vocabulary.py
```

### `df.py`
- **Entrées** :
  - `outputs/vocabulaire.txt`
  - la collection de documents
- **Sortie** : `outputs/df.txt` au format :
  - `mot df` (un mot par ligne)

```bash
python df.py
```
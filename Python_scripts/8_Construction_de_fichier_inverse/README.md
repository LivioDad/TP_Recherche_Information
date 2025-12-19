# 8 — Construction de fichier inverse (Index inversé)

Auteurs : **Livio Dadone**, **Gabriel Bragança De Oliveira**

## Objectif
Construire l’**index inversé** : pour chaque terme du vocabulaire, lister les documents qui le contiennent. fileciteturn1file1

## Script
### `indexInverse.py`
Méthode (conforme aux indications du TP) :
1. extraction des paires (idTerme, idDoc) par parcours complet,
2. tri (idTerme puis idDoc),
3. regroupement par terme.

- **Entrées** :
  - `outputs/vocabulaire.txt`
  - `Collection/Collection` + fichiers documents (version choisie)
- **Sortie** : `outputs/indexInverse.txt`

Exécution :
```bash
python indexInverse.py
```

## Sortie attendue
Un fichier texte où chaque terme (ou idTerme) est associé à une liste triée d’identifiants documents.

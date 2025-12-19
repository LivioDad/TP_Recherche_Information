# 9 - Moteur de recherche

Auteurs : **Livio Dadone**, **Gabriel Bragança De Oliveira**

## Objectif
Interroger la collection CACM avec une requête et produire :
- un classement des documents,
- un fichier HTML de résultats avec liens vers les documents. fileciteturn1file1

Deux approches :
1) **TF-IDF + cosinus** (baseline améliorée),  
2) **Proximité** (prise en compte des positions des termes).

## Scripts
### `moteur_tfidf.py` (TF-IDF cosinus)
- **Entrées** :
  - `outputs/vocabulaire.txt`
  - `outputs/df.txt`
  - `outputs/vecteurTF.txt`
  - `Collection/Collection` (+ documents)
- **Mode** : interactif (saisie de requêtes)
- **Sortie** : `outputs/resultats_tfidf.html`

Exécution :
```bash
python moteur_tfidf.py
```

### `moteur_proximite.py` (scoring par proximité)
- **Entrées** : similaires + informations de positions (selon implémentation)
- **Mode** : interactif
- **Sortie** : `outputs/resultats_proximite.html`

Exécution :
```bash
python moteur_proximite.py
```

## Utilisation
Après lancement, saisir une requête (mots) dans le terminal.
- Le programme affiche un **Top-N** des documents
- Génère/écrase un fichier HTML de résultats dans `outputs/`

## Dépannage
Si le script affiche “Fichier introuvable” :
- vérifier que `outputs/` contient bien `vocabulaire.txt`, `df.txt`, `vecteurTF.txt`
- vérifier que `Collection/Collection` existe

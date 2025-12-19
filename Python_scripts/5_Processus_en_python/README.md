# 5 — Processus en Python (Préparation des documents)

Auteurs : **Livio Dadone**, **Gabriel Bragança De Oliveira**

## Objectif
Mettre en place le **processus de préparation de la collection CACM** :
1) décoder `cacm.all` en un fichier par document,  
2) nettoyer le texte (ponctuation/accents/blancs),  
3) retirer les mots vides,  
4) produire une V2 regroupant toute la collection en **HTML** (`Collection1.html`, `Collection2.html`).

## Scripts
### `DecodeCACMXX.pl`
- **Entrée** : `cacm.all`
- **Sorties** :
  - répertoire `Collection/` (un fichier par doc, ex `CACM-123`)
  - fichier `Collection/Collection` (liste des identifiants)

Exécution :
```bash
perl DecodeCACMXX.pl
```

### `clean.pl`
- Nettoyage : suppression/remplacement caractères spéciaux + normalisation des espaces
- **Entrées** : `Collection/Collection` + fichiers `Collection/CACM-*`
- **Sorties** : fichiers avec extension nettoyée (selon le script)

```bash
perl clean.pl
```

### `remove.pl`
- Suppression des mots vides à partir du fichier `common_words` / `commonwords`
- **Entrées** : fichiers nettoyés + stoplist
- **Sorties** : fichiers sans mots vides

```bash
perl remove.pl
```

### `clean_v2.py`  (V2 HTML)
- Construit **un seul fichier HTML** contenant tous les documents nettoyés sous forme :
  - `<article class="cacm" id="CACM-XXX"> ... </article>`
- **Sortie** : `outputs/Collection1.html`

```bash
python clean_v2.py
```

### `remove_v2.py`  (V2 HTML sans mots vides)
- Variante basée sur la version “sans mots vides”
- **Sortie** : `outputs/Collection2.html`

```bash
python remove_v2.py
```

## Fichiers produits
- `outputs/Collection1.html`
- `outputs/Collection2.html`

## Notes
- Les scripts Perl supposent généralement d’être lancés dans le dossier où se trouve `cacm.all`.
- Les scripts V2 Python écrivent dans `outputs/` (créer le dossier si besoin).

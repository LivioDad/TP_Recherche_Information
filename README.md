# TP Recherche d’Informations (CACM) - Scripts & Résultats

Auteurs : **Livio Dadone**, **Gabriel Bragança De Oliveira**

## Objectif
Ce projet met en œuvre un pipeline complet de **préparation d’une collection de test (CACM)**, d’**analyse statistique**, d’**indexation (fichier inverse)** et d’**interrogation** (moteur de recherche) conformément au sujet du TP.

## Structure du dépôt
- `5_Processus_en_python/` : décodage CACM → nettoyage → suppression des mots vides + versions HTML (V2)
- `6_Calcul_des_valeurs_classiques/` : vocabulaire & df
- `7_Analyse_de_la_collection/` : comptage, fréquences, Zipf, vecteurs (binaire / TF / TF-IDF)
- `8_Construction_de_fichier_inverse/` : index inversé
- `9_Moteur_de_recherche/` : moteurs (TF-IDF cosinus + proximité)
- `10_Informations_MAIL/` : scraping HTML & lemmatisation (Porter)

> **Important** : la collection CACM et les fichiers intermédiaires peuvent être volumineux. Pour l’archive de rendu, suivre la consigne et **ne pas inclure** le répertoire `Collection/` ni les multiples versions de fichiers nettoyés, sauf demande explicite.

## Prérequis
- **Python 3.10+** (recommandé)
- **Perl** (pour `DecodeCACMXX.pl`, `clean.pl`, `remove.pl`)
- Librairies Python (selon scripts) :
  - `matplotlib` (graphe Zipf)
  - `beautifulsoup4` (scraping HTML)
  - `nltk` (PorterStemmer) + ressources NLTK si nécessaire

Exemple d’installation :
```bash
pip install matplotlib beautifulsoup4 nltk
```

## Données attendues / entrées principales
- `cacm.all` (source CACM)
- Répertoire `Collection/` (un fichier par doc + fichier liste `Collection`)
- Répertoire `outputs/` (fichiers produits : vocabulaire, df, vecteurs, index, résultats HTML, etc.)

## Pipeline recommandé (ordre d’exécution)
1. **Construire les documents** (Perl) : `DecodeCACMXX.pl`
2. **Nettoyer** (Perl ou Python V2) : `clean.pl` ou `clean_v2.py`
3. **Retirer les mots vides** (Perl ou Python V2) : `remove.pl` ou `remove_v2.py`
4. **Vocabulaire** : `vocabulary.py`
5. **DF** : `df.py`
6. **Analyse / Zipf / Vecteurs** : scripts de `7_Analyse_de_la_collection/`
7. **Index inversé** : `indexInverse.py`
8. **Moteur de recherche** : `moteur_tfidf.py` puis `moteur_proximite.py`

Chaque dossier contient un README local avec les détails (paramètres, fichiers produits).

## Sorties principales
- `outputs/Collection1.html` : version nettoyée (sans caractères spéciaux / blancs superflus)
- `outputs/Collection2.html` : version sans mots vides
- `outputs/vocabulaire.txt`, `outputs/df.txt`
- `outputs/vecteurBinaire.txt`, `outputs/vecteurTF.txt`, `outputs/vecteurTFIDF.txt`
- `outputs/indexInverse.txt`
- `outputs/resultats_tfidf.html`, `outputs/resultats_proximite.html`
- `outputs/zipf_plot.png`

## Aide / Dépannage
- Si un script ne trouve pas `Collection/` ou `outputs/`, vérifier :
  - que vous lancez les commandes **depuis la racine** du projet, ou
  - adapter les chemins dans les scripts (utiliser `Path(__file__).resolve()` pour rendre les chemins robustes).
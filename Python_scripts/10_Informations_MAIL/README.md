# 10 - Informations MAIL (Scraping & Lemmatisation)

Auteurs : **Livio Dadone**, **Gabriel Bragança De Oliveira**

## Objectif
Exploiter la version HTML de la collection (V2) pour :
- **scraper** les documents via BeautifulSoup,
- produire une nouvelle version textuelle,
- appliquer une lemmatisation/racinisation (Porter) avec NLTK. fileciteturn1file1

## Scripts
### `scrape_cacm_html.py`
- Lit un fichier HTML type `outputs/Collection1.html` / `outputs/Collection2.html`
- Extrait les `<article class="cacm">` et reconstruit une version exploitable

Exécution :
```bash
python scrape_cacm_html.py
```

### `porter_lemmatise_cacm.py`
- Applique `PorterStemmer` (NLTK) sur le texte extrait
- Produit une troisième version (selon configuration du script)

Exécution :
```bash
python porter_lemmatise_cacm.py
```

## Prérequis
```bash
pip install beautifulsoup4 nltk
```

> Selon votre environnement, NLTK peut demander le téléchargement de ressources (tokenizers, etc.).
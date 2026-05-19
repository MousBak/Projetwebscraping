# Books Explorer - Web scraping et MongoDB

> Web Scraping / Streamlit / MongoDB

## Vue d'ensemble

Projet de scraping de livres avec stockage MongoDB et interface Streamlit. L'application permet de rechercher des titres, filtrer par prix, disponibilité et catégorie, puis exporter les résultats en CSV.

## Objectifs du projet

- Scraper des informations de livres depuis le web.
- Stocker les données dans MongoDB.
- Créer une interface de recherche et filtrage.
- Permettre l’export des résultats pour analyse.

## Démarche

- Scraping par catégorie et livre.
- Insertion ou lecture depuis MongoDB.
- Construction de filtres dynamiques dans Streamlit.
- Export CSV des résultats filtrés.

## Stack technique

- Python
- Streamlit
- MongoDB
- Pandas
- Web Scraping
- CSV Export

## Structure du dépôt

- `dbmongo.py`
- `i.txt`
- `requirements.txt`
- `scraper_books.py`
- `scraper_books_by_category.py`
- `streamlit_app.py`

## Lancer ou consulter le projet

```bash
pip install -r requirements.txt
Démarrer MongoDB localement
python scraper_books.py
streamlit run streamlit_app.py
```

## Compétences démontrées

- Collecte automatisée de données web.
- Persistance MongoDB.
- Interface analytique Streamlit.
- Filtrage et export de données.

## Pistes d'amélioration

- Ajouter un fichier .env.example pour la connexion MongoDB.
- Documenter le schéma de collection.
- Ajouter une pagination et une gestion d’erreurs réseau.

## Auteur

**Bakayoko Moussa**  
Data Analyst / BI Analyst / Analytics Engineering Jr  
Portfolio : https://mousbak.github.io/  
GitHub : https://github.com/MousBak

import streamlit as st
import pandas as pd
from dbmongo import get_collection  # Correction de l'import

st.set_page_config(page_title="Books Explorer", layout="wide")
st.title("📚 Librairie MongoDB - Books to Scrape")

collection = get_collection()

# Filtres utilisateur
titre = st.text_input("🔍 Rechercher un titre...")
prix_max = st.number_input("💰 Prix maximum (£)", min_value=0.0, step=1.0)
disponibilites = collection.distinct("availability")
choix_dispo = st.selectbox("📦 Choisir la disponibilité", ["Toutes"] + disponibilites)
categories = collection.distinct("category")
choix_cat = st.selectbox("📚 Choisir une catégorie", ["Toutes"] + sorted(categories))
tri_prix = st.checkbox("↘️ Trier par prix croissant")

# Construction de la requête MongoDB
query = {}

if titre:
    query["title"] = {"$regex": titre, "$options": "i"}

if prix_max > 0:
    query["$expr"] = {
        "$lte": [
            {"$toDouble": {"$substr": ["$price", 1, 10]}},
            prix_max
        ]
    }

if choix_dispo != "Toutes":
    query["availability"] = choix_dispo

if choix_cat != "Toutes":
    query["category"] = choix_cat

# Exécution de la requête
cursor = collection.find(query)

if tri_prix:
    cursor = cursor.sort([("price", 1)])

livres = list(cursor.limit(100))

st.write(f"📄 {len(livres)} livres trouvés")

# DataFrame pour CSV
df = pd.DataFrame(livres)

# Ajoute les colonnes manquantes si besoin
for col in ["title", "price", "availability", "link"]:
    if col not in df.columns:
        df[col] = ""

for livre in livres:
    # Si le lien existe, le titre est cliquable
    if "link" in livre and livre["link"]:
        st.subheader(f"[{livre['title']}]({livre['link']})")
    else:
        st.subheader(livre["title"])
    st.write(f"💰 Prix : {livre['price']}")
    st.write(f"📦 Disponibilité : {livre['availability']}")
    st.markdown("---")

# Export CSV
if df.shape[0] > 0:
    csv = df[["title", "price", "availability", "link"]].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Télécharger les résultats en CSV",
        data=csv,
        file_name="livres_export.csv",
        mime="text/csv"
    )

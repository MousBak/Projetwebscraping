import streamlit as st
from db.mongo import get_mongo_connection

st.set_page_config(page_title="IMDb Explorer", layout="wide")
st.title("🎬 IMDb Top 250 - Interface MongoDB")

db = get_mongo_connection()
collection = db["top_250_imdb"]

# Filtres
titre_filtre = st.text_input("🔍 Rechercher par titre")
genre_filtre = st.text_input("📂 Rechercher par genre")
realisateur_filtre = st.text_input("🎬 Rechercher par réalisateur")

# Requête MongoDB
query = {}
if titre_filtre:
    query["titre"] = {"$regex": titre_filtre, "$options": "i"}
if genre_filtre:
    query["genres"] = {"$regex": genre_filtre, "$options": "i"}
if realisateur_filtre:
    query["realisateur"] = {"$regex": realisateur_filtre, "$options": "i"}

films = list(collection.find(query).limit(100))
st.write(f"🎥 {len(films)} films trouvés")

for film in films:
    st.subheader(f"{film['titre']} ({film['annee']}) ⭐ {film['note']}")
    st.write(f"**Réalisateur :** {film['realisateur']}")
    st.write(f"**Genres :** {film['genres']}")
    st.write(f"**Résumé :** {film['resume']}")
    st.markdown(f"[🔗 Lien IMDb]({film['lien']})")
    st.markdown("---")

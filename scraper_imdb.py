from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from db_mongo import get_mongo_connection

BASE_URL = "https://www.imdb.com/chart/top"

def scrape_imdb_top_250():
    db = get_mongo_connection()
    collection = db["top_250_imdb"]

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)
    time.sleep(3)  # Laisse le temps au JS de charger

    soup = BeautifulSoup(driver.page_source, "html.parser")
    movies = soup.select("tbody.lister-list tr")
    print(f"{len(movies)} films trouvés sur la page IMDb")

    for movie in movies:
        try:
            title_column = movie.find("td", class_="titleColumn")
            rating_column = movie.find("td", class_="ratingColumn imdbRating")

            if not title_column or not rating_column:
                continue

            title = title_column.a.text.strip()
            year = title_column.span.text.strip("()")
            rating = rating_column.strong.text.strip() if rating_column.strong else "N/A"
            relative_link = title_column.a['href']
            full_link = "https://www.imdb.com" + relative_link

            doc = {
                "titre": title,
                "annee": year,
                "note": rating,
                "lien": full_link
            }

            collection.insert_one(doc)
            print(f"✅ {title} inséré")
        except Exception as e:
            print(f"❌ Erreur sur un film : {e}")

    driver.quit()

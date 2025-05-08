import requests
from bs4 import BeautifulSoup
from dbmongo import get_collection

BASE_URL = "https://books.toscrape.com/catalogue/"
PAGE_URL = BASE_URL + "page-{}.html"

collection = get_collection()
page = 1
total_inserted = 0

while True:
    print(f"🔄 Scraping page {page}...")
    response = requests.get(PAGE_URL.format(page))
    if response.status_code != 200:
        print("📄 Aucune autre page.")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.select("article.product_pod")

    if not books:
        break

    for book in books:
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text
        availability = book.select_one(".availability").text.strip()

        doc = {
            "title": title,
            "price": price,
            "availability": availability
        }

        collection.insert_one(doc)
        total_inserted += 1

    page += 1

print(f"\n✅ {total_inserted} livres insérés dans MongoDB.")

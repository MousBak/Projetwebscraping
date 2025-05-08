import requests
from bs4 import BeautifulSoup
from dbmongo import get_collection

BASE_URL = "https://books.toscrape.com/"

def get_categories():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    categories = []
    for cat in soup.select("div.side_categories ul li ul li a"):
        name = cat.text.strip()
        link = BASE_URL + cat["href"]
        categories.append({"name": name, "link": link})
    return categories

def scrape_category(category, collection):
    page_url = category["link"]
    while True:
        print(f"Scraping {category['name']} : {page_url}")
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.select("article.product_pod")
        if not books:
            break
        for book in books:
            title = book.h3.a["title"]
            price = book.select_one("p.price_color").text.strip()
            availability = book.select_one("p.instock.availability").text.strip()
            link = BASE_URL + "catalogue/" + book.h3.a["href"].replace("../", "")
            doc = {
                "title": title,
                "price": price,
                "availability": availability,
                "link": link,
                "category": category["name"]
            }
            collection.update_one(
                {"title": title, "category": category["name"]},
                {"$set": doc},
                upsert=True
            )
        # Pagination
        next_btn = soup.select_one("li.next a")
        if next_btn:
            next_href = next_btn["href"]
            page_url = page_url.rsplit("/", 1)[0] + "/" + next_href
        else:
            break
if __name__ == "__main__":
    collection = get_collection()
    categories = get_categories()
    for category in categories:
        scrape_category(category, collection)
    print("✅ Scraping terminé !")
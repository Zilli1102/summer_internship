import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
import time
from urllib.parse import urljoin

# Base URLs
BASE_URL = "https://books.toscrape.com/"
PAGE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

# Set up CSV
csv_file = open("books_scraped.csv", "w", newline="", encoding="utf-8")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Title", "Rating", "Price", "Availability"])

# Function to convert rating class to number
def get_rating(rating_class):
    mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    for word in mapping:
        if word in rating_class:
            return mapping[word]
    return 0

# Fake User Agent
ua = UserAgent()

# Loop through pages (1 to 5)
for page_num in range(1, 6):
    try:
        url = PAGE_URL.format(page_num)
        headers = {"User-Agent": ua.random}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a['title']
            price = book.find("p", class_="price_color").text.strip()
            availability = book.find("p", class_="instock availability").text.strip()
            rating_class = book.find("p", class_="star-rating")["class"]
            rating = get_rating(rating_class)

            csv_writer.writerow([title, rating, price, availability])
            print(f"✔ Scraped: {title} | Rating: {rating} | {price} | {availability}")

        time.sleep(1)  # Be polite to server

    except Exception as e:
        print(f"❌ Error scraping page {page_num}: {e}")

csv_file.close()

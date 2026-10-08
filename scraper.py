import requests

BASE_URL = "https://quotes.toscrape.com/"


def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text

        else:
            print(f"Failed to fetch {url} - Status: {response.status_code}")
            return None

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None


if __name__ == "__main__":
    html = fetch_page(BASE_URL)
    print(html[:500])

from bs4 import BeautifulSoup
import time


def parse_quotes(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes = []
    quote_blocks = soup.find_all("div", class_="quote")
    for block in quote_blocks:
        text = block.find("span", class_="text").get_text(strip=True)
        author = block.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in block.find_all("a", class_="tag")]

        quotes.append({"text": text, "author": author, "tags": tags})
    return quotes


if __name__ == "__main__":
    html = fetch_page(BASE_URL)
    if html:
        quotes = parse_quotes(html)
        for q in quotes:
            print(q)

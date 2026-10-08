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

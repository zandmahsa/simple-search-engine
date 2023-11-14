import requests
from bs4 import BeautifulSoup

def crawl(url, base_url, visited, index):
    """
    Recursively crawls a web page and updates the visited set and index.
    """
    if url in visited or not url.startswith(base_url):
        return

    try:
        response = requests.get(url)
        visited.add(url)

        # Skip if page not found or not HTML
        if response.status_code == 404 or 'text/html' not in response.headers.get('Content-Type', ''):
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        words = text.split()
        for word in words:
            index.setdefault(word, set()).add(url)

        for link in soup.find_all('a', href=True):
            full_link = base_url + link['href'].lstrip('/')
            crawl(full_link, base_url, visited, index)

    except requests.RequestException:
        pass

def search(query, index):
    """
    Search for pages containing all words in the query.
    """
    words = query.split()
    if not words:
        return []

    results = index.get(words[0], set())
    for word in words[1:]:
        results = results.intersection(index.get(word, set()))

    return list(results)

    
# Base URL of the site to crawl
base_url = 'https://vm009.rz.uos.de/crawl/'
visited_urls = set()
index = {}

crawl(base_url, base_url, visited_urls, index)

print(search("platypus", index))


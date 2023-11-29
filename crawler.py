import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, STORED
import os
from config import index_dir



# Define the schema for Whoosh
schema = Schema(url=ID(stored=True, unique=True), title=TEXT(stored=True), content=TEXT, teaser=TEXT(stored=True))



if not os.path.exists(index_dir):
    os.mkdir(index_dir)
ix = create_in(index_dir, schema)
writer = ix.writer()

def crawl(url, base_url, visited):
    """
    Recursively crawls a web page and calls index_page for each page.
    """
    if url in visited or not url.startswith(base_url) or url == base_url + 'index.html':
        return

    try:
        response = requests.get(url)
        visited.add(url)

        if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
            soup = BeautifulSoup(response.text, 'html.parser')
            index_page(url, soup)
            
            for link in soup.find_all('a', href=True):
                full_link = base_url + link['href'].lstrip('/')
                crawl(full_link, base_url, visited)

    except requests.RequestException:
        pass

def index_page(url, soup):
    
    title = soup.title.string if soup.title else url  # Using URL as title if <title> tag is missing
    content = soup.get_text()
    teaser = content[:100]  # First 200 characters of content as a teaser
    writer.add_document(url=url, title=title, content=content, teaser=teaser)

# Start the crawling process
base_url = 'https://vm009.rz.uos.de/crawl/'
visited_urls = set()
crawl(base_url, base_url, visited_urls)

# Committing the changes to the index
writer.commit()

'''
Artificial Intelligence and the web course(winter 2023) 
Mahsa Zand-khaneh shahri and Mitra Farajimashaallah

A web crawler that navigates through web pages starting from the base URL, 
extracts data from each page, and indexes this data for searching. 
It uses requests for HTTP requests, BeautifulSoup for HTML parsing, and Whoosh for indexing and search functionality.

libraries: 
Imports the requests library to make HTTP requests.
Imports BeautifulSoup from the bs4 library for parsing HTML.
Imports create_in to create a Whoosh index.
from whoosh.fields import Schema, TEXT, ID, STORED: Imports necessary components to define a Whoosh schema.
Imports the os library for interacting with the operating system.
Imports the path of the index directory from a config.py file.

'''
import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, STORED
import os
from config import index_dir



# Define the schema for Whoosh
schema = Schema(url=ID(stored=True, unique=True), title=TEXT(stored=True), content=TEXT, teaser=TEXT(stored=True))


# Checks if the index directory exists
if not os.path.exists(index_dir):

    # Creates the directory if it doesn't exist 
    os.mkdir(index_dir) 

# Creates a new Whoosh index in the specified directory using the defined schema
ix = create_in(index_dir, schema)

# Creates a writer object to add documents to the index
writer = ix.writer()



"""
    Defines a recursive function to crawl web pages. 
    It takes the current URL, the base URL, and a set of visited URLs.
    The function checks if the URL has been visited, is outside the base_url domain ,
    or is the index page and returns if any of these conditions are true.
"""
def crawl(url, base_url, visited):
    
    if url in visited or not url.startswith(base_url) or url == base_url + 'index.html':
        return

    try:
        # HTTP GET request to the URL.
        response = requests.get(url)

        # Adds the URL to the set of visited URLs
        visited.add(url)

        # If the response is an HTML page (text/html), it parses the page with BeautifulSoup and calls index_page.
        # And because we observe that there is a page with 404 responce and we have to handle it too
        if response.status_code == 200 and 'text/html' in response.headers.get('Content-Type', ''):
            soup = BeautifulSoup(response.text, 'html.parser')

            index_page(url, soup)

            # The function then finds all hyperlinks a tags on the page and recursively calls crawl on each link.
            for link in soup.find_all('a', href=True):
                full_link = base_url + link['href'].lstrip('/')
                crawl(full_link, base_url, visited)

    except requests.RequestException:
        pass


"""
    Index Page Function:
    Extracts the title from the page's title tag, or uses the URL as the title if the tag is missing.
    Extracts the content of the page and uses the first 100 characters as a teaser.
    Adds these details to the Whoosh index using the writer.
"""
def index_page(url, soup):
    
    #Extracts the title from the page's title tag, or uses the URL as the title if the tag is missing.
    title = soup.title.string if soup.title else url  
    content = soup.get_text()

    # First 200 characters of content as a teaser
    teaser = content[:100]  

    # Adds these details to the Whoosh index using the writer.
    writer.add_document(url=url, title=title, content=content, teaser=teaser)

# Start the crawling
base_url = 'https://vm009.rz.uos.de/crawl/'
visited_urls = set()
crawl(base_url, base_url, visited_urls)

# Committing the changes to the index
writer.commit()

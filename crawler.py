import requests
from bs4 import BeautifulSoup
import re




#pages = ['page1', 'index', 'page2', 'page3', 'page4', 'page5', 'page6', 'page7', 'https://www.uni-osnabrueck.de/startseite/']

def soup_page(url):
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    else:
        return None
    
def index(soup):
    index_dict = {}
    words = re.findall(r'\w+', soup.get_text())
    for word in words:
        word = word.lower()
        if word in index_dict:
            index_dict[word] += 1
        else:
            index_dict[word] = 1
    return index_dict

def remove_words(input1):
    stop_words = {'a', 'an', 'the', 'and', 'or', 'in', 'on', 'at'}
    for stop_word in stop_words:
        if stop_word in input1:
            del input1[stop_word]
    return input1

def search(query, input1):
    input_query = re.findall(r'\w+', query.lower())
    results = {}
    for word in input_query:
        if word in input1:
            results[word] = input1[word]
    return results

def web_search(url, query):
    soup = soup_page(url)
    if soup is None:
        return "404"
    input1 = index(soup)
    input1 = remove_words(input1)
    results = search(query, input1)
    return results


'''for i in range(0, (len(pages))):
    if i < (len(pages)-1):
        url = 'https://vm009.rz.uos.de/crawl/{pages[i]}.html'
    else:
        url = pages[i]
'''

url = 'https://vm009.rz.uos.de/crawl/index.html'
query = 'platypus'
results = web_search(url, query)
print(results)

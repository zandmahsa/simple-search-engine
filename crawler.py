import requests
from bs4 import BeautifulSoup


pages = ['page1', 'index','page2', 'page3', 'page4', 'page5', 'page6', 'page7']
results = {}

"""
uni_osna = "https://www.uni-osnabrueck.de/startseite/"
re = requests.get(uni_osna)
soup2 = BeautifulSoup(re.content, 'html.parser')
results[uni_osna] = soup2.find_all('p')
"""

for i in pages:
    r = requests.get(f'https://vm009.rz.uos.de/crawl/{i}.html')
    soup1 = BeautifulSoup(r.content, 'html.parser')
    results[f'https://vm009.rz.uos.de/crawl/{i}.html']= soup1.find_all('p')
    


print(results)
for i in results.values():
    for j in i:
        for p in j:
            k = [p]
            for i in k:
                if i == "platypus":
                    print(i)


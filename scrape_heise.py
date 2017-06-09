from collections import Counter
from bs4 import BeautifulSoup
import requests
import csv

base_url = "https://www.heise.de/thema/https?seite={0}"

def getPage(url):
    r = requests.get(url)
    data = r.text
    spobj = BeautifulSoup(data, "lxml")
    return spobj


def main():
    page = 0
    fobj = open('heise.csv', 'w')
    csvw = csv.writer(fobj, delimiter = ';')
    words = []
    while True:
        content = getPage(base_url.format(page))
        div = content.find("div", {"id": "mitte_uebersicht"})
        nav = div.find("nav")
        if nav is None:
            break
        headers = nav.findAll("header")
        for header in headers:
            header_stripped = header.text.strip()
            header_words = [word.lower() for word in header_stripped.split(" ")]
            words += header_words
            csvw.writerow([header_stripped])
        page += 1
    fobj.close()
    counter = Counter(words)
    print("Top three words are : " + str(counter.most_common()[0:3]))

if __name__ == '__main__':
    main()
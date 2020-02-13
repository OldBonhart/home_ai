import requests
from bs4 import BeautifulSoup
import re

class SearchInfo:
    def __init__(self, *data):
        self.data = data

    def get_info(self):

        data = " ".join(self.data)
        url = f"https://en.wikipedia.org/wiki/{data}"
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        info = soup.find(id="mw-content-text").p.text
        info = re.sub(r'\(.+\)', '', info)
        
        return info.strip()

    def get_mentions(self):

        url = f"https://en.wikipedia.org/w/index.php?sort=relevance&search={self.data}&title=Special:Search&profile=advanced&fulltext=1&advancedSearch-current={self.data}"
        r = requests.get(url)

        data = BeautifulSoup(r.text, "lxml")
        mentions = data.find_all("li", "mw-search-result")[1].text
        mentions = re.sub(r'\(.+\)', '', mentions)
        return mentions.strip()


import requests
from requests.utils import requote_uri

from bs4 import BeautifulSoup
import re

class SearchInfo:
    def __init__(self, *data):
        self.data = data

    def get_info(self):
        data = " ".join(self.data)
        url = f"https://ru.wikipedia.org/wiki/{data}"
        print(url)
        r = requests.get(requote_uri(url))
        soup = BeautifulSoup(r.text, "lxml")
        info = soup.find(id="mw-content-text").p.text
        info = re.sub(r'\(.+\)', '', info)

        return info.strip()

    def get_mentions(self):

        url = f"https://ru.wikipedia.org/w/index.php?sort=relevance&search={self.data}&title=Служебная:Поиск&profile=advanced&fulltext=1&advancedSearch-current=трансгум"
        r = requests.get(requote_uri(url))

        data = BeautifulSoup(r.text, "lxml")
        mentions = data.find_all("li", "mw-search-result")[1].text
        mentions = re.sub(r'\(.+\)', '', mentions)
        return mentions.strip()
    


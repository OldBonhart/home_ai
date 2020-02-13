import requests
from bs4 import BeautifulSoup
import random


class PubMed:
    def __init__(self, topic_url, article_url):
        self.topic_url = topic_url
        self.article_url = article_url

    def get_links(self):
        res = requests.get(self.topic_url)
        soup = BeautifulSoup(res.text, "lxml")
        pub_soup = soup.find_all("a", class_="labs-docsum-title")

        all_links = []
        for s in pub_soup:
            label = s["data-ga-label"]
            link_line = [self.article_url[i:i+1] for i in range(0, len(self.article_url), 1)]

            link_tail = "".join(link_line[40:])
            link_line[32:] = label
            link = ''.join(link_line)+link_tail
            all_links.append(link)
        return all_links

    def get_data(self):
        data = {}
        all_links = self.get_links()
        for l in all_links:
            try:
                num = random.randint(0,9)
                res = requests.get(l)
                soup = BeautifulSoup(res.text, "lxml")
                soup = soup.find("div", {"id": "article-page"})
                title = soup.h1.text.strip()
                text = soup.p.text.strip()
                data[title] = text

                title = list(data.keys())[num]
                text = list(data.values())[num]
            except Exception as e:
                print("Exception: " + str(e))
                continue
            return title, text
import requests
from bs4 import BeautifulSoup
import random

class MTW2Quotes:
    def get_data(self):
        num = random.randint(0, 217)
        res = requests.get("https://wiki.totalwar.com/w/Loading_Screen_Quotes_(M2TW).html")
        soup = BeautifulSoup(res.text, "lxml")

        html_text = soup.find("div", {"id": "mw-content-text"})
        quotes = text.find_all("p")[num].text.strip()
        quote = self.cleaning(quotes)

        return quote.replace("\n", "")
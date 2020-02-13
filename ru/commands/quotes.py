# Класс парсит цитаты из серии игр Medival Toatal War 2
# из сайта https://steamcommunity.com/sharedfiles/filedetails/?id=1716011492
# Английская версия - https://wiki.totalwar.com/w/Loading_Screen_Quotes_(M2TW).html

import requests
from bs4 import BeautifulSoup

import random
import re
import os

class M2TWQuotes:
    def __init__(self):
        self.resp = requests.get("https://steamcommunity.com/sharedfiles/filedetails/?id=1716011492")
        self.all_quotes = []

    def soup_of_quotes(self):
        html = self.resp.text
        soup = BeautifulSoup(html, "lxml")
        soup = soup.find_all("div", "subSectionDesc")
        return soup

    def cleaning(self, html): 
        reg = re.compile(r'<[^>]+>')
        quote = reg.sub('', str(html))
        s = quote.rstrip(os.linesep)
        self.all_quotes.append(s.strip())

    def get_quote(self):
        num = random.randint(0,120)
        soup = self.soup_of_quotes()
        for s in soup:
            category = [q for q in s]
            list(map(self.cleaning, category))

        quotes = list(filter(None, self.all_quotes))
        quotes = list(set(quotes))

        quotes.remove("Цитаты Total War Medieval II Kingdoms: Teutonic Campaing (вроде все собрал тут):")
        return quotes[num]

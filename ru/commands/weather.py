# Класс парсит метеорологический и "народный" прогноз погоды 
# из https://sinoptik.ua/погода-киев.

import requests
from requests.utils import requote_uri
from bs4 import BeautifulSoup

class Weather:
    def __init__(self, url):
        self.url = url
    
    def get_weather(self):
        resp = requests.get(requote_uri(self.url))
        html = resp.text
        soup = BeautifulSoup(html, "lxml")
        soup = soup.find_all("div", class_="description")
        if len(soup) > 2:
            weather = soup[1].text
            narod_w = soup[2].text
        else:
            weather = soup[0].text
            narod_w = soup[1].text
        return  weather, narod_w

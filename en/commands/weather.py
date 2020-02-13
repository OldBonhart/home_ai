import requests
from bs4 import BeautifulSoup
import random

class Weather:
    def __init__(self, url):
        self.url = url
    
    def get_weather(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, "lxml")
        soup = soup.find("table", class_="b-forecast__table js-forecast-table")
        return soup.td.text
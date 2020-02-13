import requests
from bs4 import BeautifulSoup

import random

def get_advice():
    num = random.randint(0, 99)
    resp = requests.get("https://stalker.fandom.com/ru/wiki/100_%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D0%BE%D0%B2_%D0%BF%D0%BE_%D0%B2%D1%8B%D0%B6%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D1%8E_%D0%B2_%D0%97%D0%BE%D0%BD%D0%B5")
    soup = BeautifulSoup(resp.text, "lxml")
    return soup.find_all("cite")[num].text

# Класс парсит последние опубликованные новости из http://neuronovosti.ru/

import requests
from bs4 import BeautifulSoup
import random
import re

class NeuroNews:
    def __init__(self):
        """
        resp: main url
        num: number for choosing one of the 10
        most recently published articles
        """
        self.url = "http://neuronovosti.ru/"

    def get_news(self):
        """
        Get news list
        """
        resp = requests.get(self.url)
        html = resp.text
        soup = BeautifulSoup(html, "lxml")
        news = soup.body.find_all("div", class_="home-news-wrapper")
        news = [i.find("h3") for i in news]
        all_news = [i.a["href"] for i in news[:10]]
        print(len(all_news))
        return all_news
    
    def random_fresh_news(self):
        """
        Get random fresh news
        """
        num = random.randint(1, 9)
        all_news = self.get_news()
        print(num)
        fresh_resp = requests.get(all_news[num])
        fresh_html = fresh_resp.text
        fresh_soup = BeautifulSoup(fresh_html, "lxml")

        fresh = fresh_soup.body.find_all("div", class_="wp-content")
        fresh_news = [i.text for i in fresh]
        
        fresh_news = fresh_news[0].replace("\n", " ")
        fresh_news = re.sub(r'\(.+\)', '', fresh_news)
        
        return fresh_news

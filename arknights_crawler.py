import urllib.request as ulib_request
import json

from bs4 import BeautifulSoup
from bs4.element import Tag as htmlTag
from collections import deque
from datetime import datetime
from typing import List
from elasticsearch import Elasticsearch
from loguru import logger

from config import Config, ElasticSearchConfig
import util

es_client = Elasticsearch(ElasticSearchConfig.ES_SERVER_URL)

class Content:

    content_id: int
    image_url: str | None = None
    text_list: List[str | None] = []

    def __init__(self, content_id, image_url, texts):
        self.content_id = content_id
        self.image_url = image_url
        self.text_list = texts

        util.download_image(image_url, "./temp/images")

    def __str__(self):
        return f"{'='*20} Content image: {self.image_url} {'='*20} \n {'='*20} Content text: {self.text_list} {'='*20}"

class Article:
    
    page_url: str = None
    created_date: str = None
    title: str = None
    content: List[Content] = []
    soup: BeautifulSoup = None

    def __init__(self, url: str, title, date):
        self.title = title
        self.created_date = date
        self.page_url = url

        headers = Config.header

        req = ulib_request.Request(url=self.page_url,headers=headers,method="GET") 
        html = ulib_request.urlopen(req).read().decode('utf-8')
        self.soup = BeautifulSoup(html, 'html.parser')
    
    def parse_content(self):

        article_container = self.soup.find("div", {"class": "article-content"})

        def get_image(paragraph: htmlTag):
            image_div = paragraph.find("img")

            # actually just realized there could be a whole article composed of only text
            try:
                image_div["src"]
            except Exception as e:
                logger.debug("Failed to find image ", e)
                return None

            return image_div["src"] if image_div else None

        def get_text(paragraph: htmlTag):
            return paragraph.text
        
        texts, prev_image = [], None

        """ 
        -   logically a content is composed of an image first followed by text
        -   tho there are cases where texts are at the top of an article, or text
            segments exist without image 
        """
        for index, paragraph in enumerate(article_container):
            text = get_text(paragraph)
            cur_image = get_image(paragraph)

            if text: texts.append(text)
            
            if cur_image and prev_image:
                segment = Content(content_id=index, image_url=prev_image, texts=texts)
                self.content.append(segment)
                texts = []
            
            if cur_image and not prev_image and texts:
                # meaning we have a text segment at the top
                segment = Content(content_id=index, image_url=None, texts=texts)
                self.content.append(segment)
                texts = []

            if cur_image: prev_image = cur_image
        
        segment = Content(content_id=index, image_url=prev_image, texts=texts)
        self.content.append(segment)

    def save(self, article_id):
        contents = [vars(item) for item in self.content]
        doc = {
            "created": datetime.now(),
            "article_id": article_id,
            "title": self.title,
            "page_url": self.page_url,
            "article_date": self.created_date,
            "content": contents
        }

        es_client.index(index="arknights-news", document=doc)
        logger.debug(f"Saved {doc} to ES")
    
    def __str__(self): return json.dumps(self.__dict__)

    

class NewsCrawler:

    soup: BeautifulSoup = None
    base_url: str = None
    articles = deque([])

    def __init__(self, base_url):
        self.base_url = base_url
        headers = Config.header

        req = ulib_request.Request(url=base_url,headers=headers,method="GET") 
        html = ulib_request.urlopen(req).read().decode('utf-8')
        self.soup = BeautifulSoup(html, 'html.parser')
    
    def parse_articles(self):
        news_articles = self.soup.find("ol", {"data-category-key": "ACTIVITY"})
        
        for index, child_node in enumerate(news_articles):
            date: htmlTag = child_node.find("span", {"class": "articleItemDate"})
            href: htmlTag = child_node.find("a", {"class": "articleItemLink"})
            title: htmlTag = child_node.find("h1", {"class": "articleItemTitle"})
            url: str = self.base_url + href["href"].split("/")[-1]
            
            article = Article(date=date.text, url=url, title=title.text)
            article.parse_content()
            article.save(index)

if __name__ == "__main__":

    akurl = "https://ak.hypergryph.com/news/"

    news_crawler = NewsCrawler(base_url=akurl)
    news_crawler.parse_articles()

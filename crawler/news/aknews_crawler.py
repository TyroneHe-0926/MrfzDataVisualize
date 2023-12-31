import json
import urllib.request as ulib_request
from bs4 import BeautifulSoup
from bs4.element import Tag as htmlTag
from datetime import datetime
from typing import List
from loguru import logger

import sys, os
import uuid
from hashlib import md5
#run from repo root for now
sys.path.insert(1, os.getcwd())

from crawler.crawler import Crawler, Task
from crawler.util.config import Config, es_client
from crawler.util import util


class Content:

    content_id: int
    image_url: str | None = None
    text_list: List[str | None] = []

    def __init__(self, content_id, image_url, texts, download=False):
        self.content_id = content_id
        self.image_url = image_url
        self.text_list = texts

        if download: util.download_image(image_url, "./temp/images/news")

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
        self.content = []

        headers = Config.header

        req = ulib_request.Request(url=self.page_url,headers=headers,method="GET") 
        html = ulib_request.urlopen(req).read().decode('utf-8')
        self.soup = BeautifulSoup(html, 'html.parser')
    
    def parse_content(self, download=False):

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
                segment = Content(content_id=index, image_url=prev_image, texts=texts, download=download)
                self.content.append(segment)
                texts = []
            
            if cur_image and not prev_image and texts:
                # meaning we have a text segment at the top
                segment = Content(content_id=index, image_url=None, texts=texts, download=download)
                self.content.append(segment)
                texts = []

            if cur_image: prev_image = cur_image
        
        segment = Content(content_id=index, image_url=prev_image, texts=texts, download=download)
        self.content.append(segment)

    def save(self, article_id):
        doc = self.to_json(article_id=article_id)
        doc.update({"created": datetime.now()})

        es_client.index(index="arknights-news", document=doc)
        logger.debug(f"Saved {doc} to ES")
    
    def to_json(self, article_id):
        contents = [vars(item) for item in self.content]
        return {
            "article_id": article_id,
            "title": self.title,
            "page_url": self.page_url,
            "article_date": self.created_date,
            "content": contents
        }

    def __str__(self): return json.dumps(self.__dict__)

class NewsCrawler(Crawler):
    
    def __init__(self, base_url):
        super().__init__(base_url)
    
    def parse_articles(self, **task):
        news_articles = self.soup.find("ol", {"data-category-key": "ACTIVITY"})
        
        for _, child_node in enumerate(news_articles):
            date: htmlTag = child_node.find("span", {"class": "articleItemDate"})
            href: htmlTag = child_node.find("a", {"class": "articleItemLink"})
            title: htmlTag = child_node.find("h1", {"class": "articleItemTitle"})
            url: str = self.base_url + href["href"].split("/")[-1]
            article_id: str = md5(url.encode("utf-8")).hexdigest()

            if task["name"] == "sync":
                if es_client.search(index="arknights-news", query={
                    "match": { "article_id.keyword": article_id }
                })["hits"]["total"]["value"] > 0: 
                    logger.info(f"Article {article_id} hit, skipping")
                    continue
            
            article = Article(date=date.text, url=url, title=title.text)
            article.parse_content(download=task["save_img"])
            
            if task["mode"] == "prod": article.save(article_id)
            if task["mode"] == "dev": 
                util.save_json(f"./temp/news/article_{uuid.uuid4()}.json", article.to_json(article_id))

def dispatch(task: Task):
    akurl = "https://ak.hypergryph.com/news/"
    news_crawler = NewsCrawler(base_url=akurl)

    logger.info(f"Running News {task.name}")

    news_crawler.parse_articles(**task.model_dump())  

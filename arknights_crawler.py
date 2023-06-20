import urllib.request as ulib_request
import json

from bs4 import BeautifulSoup
from bs4.element import Tag as htmlTag
from collections import deque
from typing import List

class Config:

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

class Content:

    image_url: str | None = None
    text_list: List[str | None] = []

    def __init__(self, image_url, texts):
        self.image_url = image_url
        self.text = texts

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

            return image_div["src"] if image_div else None

        def get_text(paragraph: htmlTag):
            return paragraph.text
        
        text, prev_image = None, None

        """ 
        -   logically a content is composed of an image first followed by text
        -   tho there are cases where texts are at the top of an article, or text
            segments exist without image 
        """
        for paragraph in article_container:
            text = get_text(paragraph)    
            cur_image = get_image(paragraph)
            
            

            prev_image = image

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
        
        for child_node in news_articles:
            date: htmlTag = child_node.find("span", {"class": "articleItemDate"})
            href: htmlTag = child_node.find("a", {"class": "articleItemLink"})
            title: htmlTag = child_node.find("h1", {"class": "articleItemTitle"})
            url: str = self.base_url + href["href"].split("/")[-1]
            
            article = Article(date=date.text, url=url, title=title.text)
            # TODO write to es for meta article info here

            article.parse_content()

        
if __name__ == "__main__":

    akurl = "https://ak.hypergryph.com/news/"

    news_crawler = NewsCrawler(base_url=akurl)
    news_crawler.parse_articles()

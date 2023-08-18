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

class ArticleCrawler(Crawler):

    def infer_type(self, title: str):
        maintenance_type = {
            "封禁处理": "player ban",
            "闪断更新": "hot update",
            "停机维护": "down for maintenance",
            "异常": "hot fix",
            "游戏限时": "underage time limit",
            "标签强制刷新": "agent recruit tag refresh",
            "限时": "limited edition agent recruit"
        }

        for k, v in maintenance_type.items():
            if k in title: return v
        
        return "other"

    def __init__(self, base_url):
        super().__init__(base_url)
    
    def parse_content(self):
        pass
    
    def save(self):
        pass

class AnnouncementCrawler(Crawler):
    
    def __init__(self, base_url):
        super().__init__(base_url)
    
    def parse_articles(self, **task):
        articles = self.soup.find("ol", {"data-category-key": "ANNOUNCEMENT"})

        for node in articles:
            href: htmlTag = node.find("a", {"class": "articleItemLink"})
            url: str = self.base_url + href["href"].split("/")[-1]

            ArticleCrawler(base_url=url).parse_content(**task)
    
def dispatch(task: Task):
    akurl = "https://ak.hypergryph.com/news/"
    news_crawler = AnnouncementCrawler(base_url=akurl)

    logger.info(f"Running News {task.name}")

    news_crawler.parse_articles(**task.model_dump())

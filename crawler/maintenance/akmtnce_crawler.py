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

class MaintenanceCrawler(Crawler):
    
    def __init__(self, base_url):
        super().__init__(base_url)
    
    def parse_articles(self, **task):
        pass
    
def dispatch(task: Task):
    akurl = "https://ak.hypergryph.com/news/"
    news_crawler = MaintenanceCrawler(base_url=akurl)

    logger.info(f"Running News {task.name}")

    news_crawler.parse_articles(**task.model_dump())  

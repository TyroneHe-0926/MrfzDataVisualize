import urllib.request as ulib_request
import json

from bs4 import BeautifulSoup
from bs4.element import Tag as htmlTag
from datetime import datetime
from typing import List
from elasticsearch import Elasticsearch
from loguru import logger

import sys, os
#run from repo root for now
sys.path.insert(1, os.getcwd())

from crawler.util.config import Config, ElasticSearchConfig
from crawler.util import util

es_client = Elasticsearch(ElasticSearchConfig.ES_SERVER_URL)

class AgentCrawler:
    pass
    

if __name__ == "__main__":
    pass
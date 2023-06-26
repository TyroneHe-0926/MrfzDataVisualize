import urllib.request as ulib_request
import json

from bs4 import BeautifulSoup
from bs4.element import Tag as htmlTag
from datetime import datetime
from typing import List, Dict
from elasticsearch import Elasticsearch
from loguru import logger

import sys, os
#run from repo root for now
sys.path.insert(1, os.getcwd())

from crawler.util.config import Config, ElasticSearchConfig
from crawler.util import util
from crawler.crawler import Crawler

es_client = Elasticsearch(ElasticSearchConfig.ES_SERVER_URL)

class Agent:

    def __init__(self, **kwargs):
        self.avatar: str = kwargs["avatar"]
        self.star: int = kwargs["star"]
        self.agent_class: str = kwargs["agent_class"]
        self.faction: str = kwargs["faction"]
        self.gender: str = kwargs["gender"]
        self.race: str = kwargs["race"]

class AgentCrawler(Crawler):
    
    agents: List[Dict[str, List[Agent]]] = []

    def __init__(self, base_url):
        super().__init__(base_url)
    
    def parse_agent(self, agent_tabs: List[htmlTag]):
        for agent_tab in agent_tabs:
            agent_name = agent_tab.find("p", {"class": "handbook-item-name"}).text
            agent_avatar = agent_tab.find("img", {"alt": agent_name}).get("src")
            print(agent_name, agent_avatar)

    def get_agent_list(self):
        agent_tabs: htmlTag = self.soup.find("div", {"class": "resp-tabs-container"})

        for tab in agent_tabs:
            if(isinstance(tab, htmlTag)):
                tab_agents = tab.find_all("div", {"class": "handbook-item-container"})
                self.parse_agent(tab_agents)
                break
    
    def parse_agents(self):
        pass

    def crawl(self):
        self.get_agent_list()

if __name__ == "__main__":
    akurl = "https://wiki.biligame.com/arknights/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88"

    agentCrawler = AgentCrawler(base_url=akurl)
    agentCrawler.crawl()
import urllib.request as ulib_request
import urllib.parse as ulib_parse
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

attr_lookup_table = {
    "职业": "agent_class",
    "星级": "star",
    "阵营": "faction",
    "性别": "gender",
    "画师": "drawer",
    "CV列表": "cv_list",
    "干员编号": "agent_number",
    "特性": "ability",
    "标签": "tag",
    "实装日期": "release_date",
    "获取途径": "obtain"
}

class Agent:

    def __init__(self, **kwargs):
        self.name: str = kwargs["name"]
        self.avatar: str = kwargs["avatar"]
        self.star: int = kwargs["star"]
        self.agent_class: str = kwargs["agent_class"]
        self.faction: str = kwargs["faction"]
        self.gender: str = kwargs["gender"]
        self.race: str = kwargs["race"]
        self.drawer: str = kwargs["drawer"]
        self.cv_list: str = kwargs["cv_list"]
        self.agent_number = kwargs["agent_number"]
        self.ability = kwargs["ability"]
        self.tag = kwargs["tag"]
        self.release_date = kwargs["release_date"]
        self.obtain = kwargs["obtain"]
        self.profile = kwargs["profile"]
        self.experience = kwargs["experience"]

class AgentInfoCrawler(Crawler):
    
    def __init__(self, base_url):
        super().__init__(base_url)
    
    def set_agent_attr(self, info_dict: dict):
        attr_tables = self.soup.find_all("table", {
            "class": "wikitable",
            "style": "display:none;width:100%"
        })

        util_table = attr_tables[0].find("tbody").find_all("tr")
        spec_table = attr_tables[1].find("tbody").find_all("tr")

        for row in util_table:
            print(row, "\n\n")

        print("Now at spec table")

        for row in spec_table:
            print(row, "\n\n")

        return info_dict

    def get_agent_info(self):
        info_dict = {}

        # get agent basic info from the profile tables
        basic_info_table: List[htmlTag] = self.soup.find("table",{
            "class": "wikitable",
            "style": "width:100%;text-align:left;color: #fff;"
        }).find("tbody").find_all("tr")

        # update info dict by all basic info parsed
        for tr in basic_info_table:
            curkey, curval = None, None
            for row in tr:
                if(row.name == "th"): curkey = row.text.replace("\n", "")
                if(row.name == "td" and curkey in attr_lookup_table): 
                    curval = row.text.replace("\n", "")
                    info_dict.update({
                        attr_lookup_table[curkey]: curval
                    })
        
        # update profile section
        profile = self.soup.find("td", {"style": "padding:5px 0px 0px 0px;text-align:left;line-height:24px"}).text
        profile = profile.replace("\n", "").replace("】", ":").replace("【", "\n")
        info_dict.update({"profile": profile})

        # update exp section
        experience = self.soup.find("td", {"style": "padding:5px 0px 0px 5px;text-align:left;line-height:24px"}).text
        info_dict.update({"experience": experience})

        info_dict = self.set_agent_attr(info_dict)


class AgentCrawler(Crawler):
    
    agents: List[Dict[str, List[Agent]]] = []

    def __init__(self, base_url):
        super().__init__(base_url)
        
    def parse_agent(self, agent_tabs: List[htmlTag]):
        for agent_tab in agent_tabs:
            agent_name = agent_tab.find("p", {"class": "handbook-item-name"}).text
            agent_avatar = agent_tab.find("img", {"alt": agent_name}).get("src")
           
            agent_page_url = "https://wiki.biligame.com/arknights/"+agent_name
            encoded_url = ulib_parse.quote(agent_page_url, safe=':/?=&')
            infoCrawler = AgentInfoCrawler(encoded_url)
            infoCrawler.get_agent_info()
            break #TODO DEBUG
            
    def get_agent_list(self):
        agent_tabs: htmlTag = self.soup.find("div", {"class": "resp-tabs-container"})

        for tab in agent_tabs:
            if(isinstance(tab, htmlTag)):
                tab_agents = tab.find_all("div", {"class": "handbook-item-container"})
                self.parse_agent(tab_agents)
                break #TODO DEBUG
    
    def parse_agents(self):
        pass

    def crawl(self):
        self.get_agent_list()

if __name__ == "__main__":
    akurl = "https://wiki.biligame.com/arknights/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88"

    agentCrawler = AgentCrawler(base_url=akurl)
    agentCrawler.crawl()

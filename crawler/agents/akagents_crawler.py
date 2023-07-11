import urllib.parse as ulib_parse
import json

from bs4.element import Tag as htmlTag
from datetime import datetime
from typing import List
from elasticsearch import Elasticsearch
from loguru import logger

import sys, os
#run from repo root for now
sys.path.insert(1, os.getcwd())

from crawler.util.config import ElasticSearchConfig, Config
from crawler.util import util
from crawler.crawler import Crawler, Task

es_client = Elasticsearch(ElasticSearchConfig.ES_SERVER_URL)

class AgentSpec:
    
    class WrongSpecsException(Exception):

        def __init__(): pass

    class Spec:
        """
        Spec shoud take in a list of 5 elements
        Each represent a different level
        """
        def __init__(self, specs: list):
            
            if len(specs) != 5: raise AgentSpec.WrongSpecsException()
            
            self.initial = specs[0]
            self.initial_max = specs[1]
            self.e1_max = specs[2]
            self.e2_max = specs[3]
            self.boost = specs[4]

    def __init__(self, **kwargs):
        self.health = vars(self.Spec(kwargs["health"]))
        self.attack = vars(self.Spec(kwargs["attack"]))
        self.defense = vars(self.Spec(kwargs["defense"]))
        self.resistance = vars(self.Spec(kwargs["resistance"]))

class AgentUtil:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

class Agent:

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def set_agent_util(self, agent_util: AgentUtil):
        self.agent_util = vars(agent_util)
    
    def set_agent_spec(self, agent_spec: AgentSpec):
        self.agent_spec = vars(agent_spec)

    def save(self):
        doc = vars(self)
        doc.update({"created": datetime.now()})
        es_client.index(index="arknights-agents", document=doc)
        logger.debug(f"Saved {doc} to ES \n\n")
        
class AgentInfoCrawler(Crawler):
    
    def __init__(self, base_url):
        super().__init__(base_url)
    
    @staticmethod
    def create_dict(table: List[htmlTag]):
        """Create a dict with key value pair from th td html tag pair"""
        ret = {}

        for tr in table:
            curkey, curval = None, None
            for row in tr:
                if(row.name == "th"): curkey = row.text.replace("\n", "")
                if(row.name == "td" and curkey in util.attr_lookup_table): 
                    curval = row.text.replace("\n", "")
                    ret.update({
                        util.attr_lookup_table[curkey]: curval
                    })
        
        return ret
    
    def get_spec_dict(self, spec_table: List[htmlTag]):
        spec_dict = {}

        for row in spec_table:
            td_list = row.find_all("td")
            for index, td in enumerate(td_list):
                spec_name = td.text.replace("\n", "")
                if spec_name in util.attr_lookup_table:
                    specs = [tag.text.replace("\n", "") for tag in td_list[index+1: index+6]]
                    spec_dict.update({util.attr_lookup_table[spec_name]: specs})
        
        return spec_dict

    def get_agent_us(self) -> tuple[AgentUtil, AgentSpec]:
        """stands for get agent util and spec"""
        attr_tables = self.soup.find_all("table", {
            "class": "wikitable",
            "style": "text-align:center;width:100%"
        })

        util_table = attr_tables[0].find("tbody").find_all("tr")
        spec_table = attr_tables[1].find("tbody").find_all("tr")

        # create agent util dict from html table
        agent_util = AgentUtil(**(AgentInfoCrawler.create_dict(util_table)))
        spec_dict = self.get_spec_dict(spec_table)
        agent_spec = AgentSpec(**spec_dict)
        
        return agent_util, agent_spec

    def get_agent_info(self, agent_name, agent_avatar, mode):
        # get agent basic info from the profile tables
        basic_info_table: List[htmlTag] = self.soup.find("table",{
            "class": "wikitable",
            "style": "width:100%;text-align:left;color: #fff;"
        }).find("tbody").find_all("tr")

        # update info dict by all basic info parsed
        agent_dict = AgentInfoCrawler.create_dict(basic_info_table)
        agent_dict.update({"name": agent_name})
        agent_dict.update({"avatar": agent_avatar})

        # update profile section
        profile = self.soup.find("td", {"style": "padding:5px 0px 0px 0px;text-align:left;line-height:24px"}).text
        profile = profile.replace("\n", "").replace("】", ":").replace("【", "\n")
        agent_dict.update({"profile": profile})

        # update exp section
        experience = self.soup.find("td", {"style": "padding:5px 0px 0px 5px;text-align:left;line-height:24px"}).text
        agent_dict.update({"experience": experience})

        # update agent util and specs
        agent_util, agent_spec = self.get_agent_us()
        
        # update agent e1 e2 upgrades
        upgrades = self.soup.find_all("td", {
            "style": "text-align:left",
            "colspan": "2"
        })

        e1_upgrades = upgrades[0].text
        e2_upgrades = "not avaliable"

        # check if an agent has an e2 upgrade
        if len(upgrades) >= 2: e2_upgrades = upgrades[1].text

        agent_dict.update({"e1_upgrades": e1_upgrades})
        agent_dict.update({"e2_upgrades": e2_upgrades})
        
        # get mod info
        mod = self.soup.find("div", {
            "style": "width:80%;padding:5px;background-color:#e1e1e1;display: flex;align-items: center;"
        }).text
        agent_dict.update({"mod": mod})

        agent = Agent(**agent_dict)
        agent.set_agent_spec(agent_spec)
        agent.set_agent_util(agent_util)
        if mode == "prod": agent.save()
        if mode == "dev": util.save_json(f"./temp/agents/{agent_name}.json", vars(agent))

class AgentCrawler(Crawler):

    def __init__(self, base_url):
        super().__init__(base_url)
        
    def parse_agent(self, agent_tabs: List[htmlTag], mode, save_img):
        for agent_tab in agent_tabs:
            agent_name = agent_tab.find("p", {"class": "handbook-item-name"}).text
            agent_avatar = agent_tab.find("img", {"alt": agent_name}).get("src")

            if save_img: util.download_image(agent_avatar, "./temp/images/agents")
           
            agent_page_url = "https://wiki.biligame.com/arknights/"+agent_name
            encoded_url = ulib_parse.quote(agent_page_url, safe=':/?=&')
            infoCrawler = AgentInfoCrawler(encoded_url)
            infoCrawler.get_agent_info(agent_name, agent_avatar, mode)
            
    def parse_agent_list(self, mode, save_img):
        agent_tabs: htmlTag = self.soup.find("div", {"class": "resp-tabs-container"})

        for tab in agent_tabs:
            if(isinstance(tab, htmlTag)):
                tab_agents = tab.find_all("div", {"class": "handbook-item-container"})
                self.parse_agent(tab_agents, mode, save_img)

def dispatch(task: Task):
    if task.name == "crawl":
        logger.info("Running Agents Crawler")

        akurl = "https://wiki.biligame.com/arknights/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88"
        agentCrawler = AgentCrawler(base_url=akurl)
        agentCrawler.parse_agent_list(mode=task.mode, save_img=task.save_img)

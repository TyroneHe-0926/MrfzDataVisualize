from bs4 import BeautifulSoup
from pydantic import BaseModel
import urllib.request as ulib_request
from abc import ABC

import sys, os
#run from repo root for now
sys.path.insert(1, os.getcwd())

from crawler.util.config import Config

class Task(BaseModel):
    name: str
    mode: str
    save_img: bool

    def json(self):
        return {
            "mode": self.mode,
            "save_img": self.save_img,
            "name": self.name
        }

class Crawler(ABC):
    
    soup: BeautifulSoup = None
    base_url: str = None

    def __init__(self, base_url):
        self.base_url = base_url
        headers = Config.header

        req = ulib_request.Request(url=base_url,headers=headers,method="GET") 
        html = ulib_request.urlopen(req).read().decode('utf-8')
        self.soup = BeautifulSoup(html, 'html.parser')

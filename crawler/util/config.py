import os
from elasticsearch import Elasticsearch

class Config:
    host = "localhost"

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

class ElasticSearchConfig:
    ES_SERVER_PORT = "9200"
    ES_USERNAME = "elastic"
    ES_PASSWORD=  os.environ.get("ES_PASSWORD")
    ES_SERVER_URL = f'http://{ES_USERNAME}:{ES_PASSWORD}@{Config.host}:{ES_SERVER_PORT}'

es_client = Elasticsearch(ElasticSearchConfig.ES_SERVER_URL)
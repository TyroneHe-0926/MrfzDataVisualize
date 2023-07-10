import os
import json
from loguru import logger

attr_lookup_table = {
    "职业": "agent_class",
    "星级": "star",
    "阵营": "faction",
    "性别": "gender",
    "设定性别": "gender",
    "画师": "drawer",
    "CV列表": "cv_list",
    "干员编号": "agent_number",
    "特性": "ability",
    "标签": "tag",
    "实装日期": "release_date",
    "获取途径": "obtain",
    "阻挡数": "block",
    "初始费用": "cost",
    "攻击间隔": "attack_interval",
    "攻击速度": "attack_speed",
    "再部署时间": "cooldown",
    "完美部署费用": "max_cost",
    "生命": "health",
    "攻击": "attack",
    "防御": "defense",
    "法抗": "resistance"
}

def run(command: str): os.system(command)

def download_image(image_url, path):
    download_img = f"wget {image_url} -P {path}"
    run(download_img)

def get_news_mock():
    from datetime import datetime

    content1 = {
        "content_id": 1,
        "image_url": "helloworld.com",
        "text_list": ["1", "2", "3", "test"]
    }

    content2 = {
        "content_id": 2,
        "image_url": "helloworld.com",
        "text_list": ["1", "2", "3", "test2"]
    }

    content3 = {
        "content_id": 3,
        "image_url": "helloworld.com",
        "text_list": ["1", "2", "3", "test3"]
    }   

    mock_data = {
        "created": datetime.now(),
        "article_id": 8,
        "title": "something",
        "page_url": "helloworld.com",
        "article_date": "something",
        "content": [content1, content2, content3]
    }

    return mock_data

def save_json(path, content):
    logger.info(f"Saving {content} to file {path} \n")

    with open(path, "w+") as fp:
        fp.write(json.dumps(content, sort_keys=True, indent=4))
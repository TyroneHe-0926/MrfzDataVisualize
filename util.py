import os

def run(command: str): os.system(command)

def download_image(image_url, path):
    download_img = f"wget {image_url} -P {path}"
    run(download_img)

def get_mock():
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
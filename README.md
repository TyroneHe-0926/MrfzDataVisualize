## MrfzDataVisualize

* The arknights_crawler gets the released arknights news up untill 2023.6.25.
* Auto saves the images and articles locally
* Indexes to ES following the arknights news mapping
* Visualizes with Kibana Dashboard
* Quick set up of ES and Kibana refer to https://github.com/deviantony/docker-elk

### Arknights News Mapping
```
{
  "arknights-news": {
    "aliases": {},
    "mappings": {
      "properties": {
        "article_date": {
          "type": "date"
        },
        "article_id": {
          "type": "long"
        },
        "content": {
          "properties": {
            "content_id": {
              "type": "long"
            },
            "image_url": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "text_list": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            }
          }
        },
        "created": {
          "type": "date"
        },
        "page_url": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "title": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        }
      }
    }
```

### Sample Dashboard
![Dashboard Screenshot](https://github.com/TyroneHe-0926/MrfzDataVisualize/blob/main/assets/dashboard.png?raw=true)

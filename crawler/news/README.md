## Arknights News Mapping

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

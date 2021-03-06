# mediascraper
Project aims to determine sentiment and subjectivity of articles on hotnews.ro using natural language processing. Articles are scraped from RSS feed using Scrapy framework and posted to Elastic.

1. Install dependencies via pip

```pip install scrapy
pip install TextBlob
pip install elasticsearch
pip install ScrapyElasticSearch
```

2. Put elastic index template below using Kibana Dev Tools or curl request to _template endpoint

```
PUT _template/hotnews
{
    "order": 0,
    "template": "hotnews*",
    "settings": {},
    "mappings": {
      "type1": {
        "_source": {
          "enabled": false
        },
        "properties": {
          "artTitle": {
            "type": "text"
          },
          "artLink": {
            "type": "text"
          },
         "artDescription": {
            "type": "text"
          },
          "artPubDate": {
            "type": "date",
            "format": "dd MMM yyyy HH:mm:ss"
          },
          "artPolarity": {
            "type": "float",
            "coerce": false
          },
          "artSubjectivity": {
            "type": "float",
            "coerce": false
          },
          "artText": {
            "type": "text"
          }
        }
      }
    },
    "aliases": {}
  }
```

3. Activate virtual environment

```
source bin/activate
```

4. Run Spider
```
scrapy crawl hotsnews
```

5. Create an index pattern if you want to visualize your data in Kibana

![index_pattern](https://user-images.githubusercontent.com/22353083/34921394-c8cafd28-f981-11e7-8f3c-63887a6ff37b.png)

6. View documents in Kibana

![documents](https://user-images.githubusercontent.com/22353083/34921396-caa7e520-f981-11e7-8ab2-67fd1e558d28.png)

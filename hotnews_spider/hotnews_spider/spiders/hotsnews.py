# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from time import gmtime, strftime, sleep
import random
import datetime
from time import sleep
import random
from scrapy.spiders import XMLFeedSpider
from textblob import TextBlob


from elasticsearch import Elasticsearch
from elasticsearch import helpers

class HotsnewsSpider(XMLFeedSpider):
    name = 'hotsnews'
    allowed_domains = ['hotnews.ro']
    start_urls = ['http://hotnews.ro/rss']
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'item'

    def parse_node(self, response, node):
        artTitle = node.xpath('title/text()').extract()
        artLink = node.xpath('link/text()').extract()
        artDescription = node.xpath('description/text()').extract()
        artPubDate = node.xpath('pubDate/text()').extract_first()
        # time format from "Sat, 23 Dec 2017 16:01:00 GMT" to "3 Dec 2017 16:01:00"
        artPubDate = artPubDate.split(',')[1:]
        artPubDate = ''.join(artPubDate)
        artPubDate = artPubDate.strip()
        artPubDate = artPubDate[:-4]
        artDescription = ''.join(artDescription)
        artDescription_en = TextBlob(artDescription)
        artDescription_en = artDescription_en.translate(to='en')
        artDescription_en_polarity = artDescription_en.sentiment.polarity
        artDescription_en_subjectivity = artDescription_en.sentiment.subjectivity
        yield {
            'artTitle': artTitle,
            'artLink': artLink,
            'artDescription': artDescription,
            'artPubDate': artPubDate,
            'artPolarity': artDescription_en_polarity,
            'artSubjectivity': artDescription_en_subjectivity
            }
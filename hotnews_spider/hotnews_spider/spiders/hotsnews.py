# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from time import gmtime, strftime, sleep
import random
import datetime
from time import sleep
import random
from scrapy.spiders import XMLFeedSpider


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
        artPubDate = node.xpath('pubDate/text()').extract()
        yield {
            'artTitle': artTitle,
            'artLink': artLink,
            'artDescription': artDescription,
            'pubDate': artPubDate
            }
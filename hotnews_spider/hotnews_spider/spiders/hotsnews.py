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

    def parse_node(self,response,node):
        artLinks = node.xpath('link/text()').extract()
        artTitle = node.xpath('title/text()').extract_first()
        artDescription = node.xpath('description/text()').extract_first()
        artPubDate = node.xpath('pubDate/text()').extract_first()
        # time format from "Sat, 23 Dec 2017 16:01:00 GMT" to "23 Dec 2017 16:01:00"
        artPubDate = artPubDate.split(',')[1:]
        artPubDate = ''.join(artPubDate)
        artPubDate = artPubDate.strip()
        artPubDate = artPubDate[:-4]
        artDescription = ''.join(artDescription)
        for artLink in artLinks:
            yield Request(artLink, meta={'artLink': artLink,
                                     'artTitle': artTitle,
                                     'artDescription': artDescription,
                                     'artPubDate': artPubDate }, callback=self.parse_item)

    def parse_item(self, response):
        #artTitle=response.xpath('//head/title/text()').extract_first()
        artTitle = response.meta['artTitle']
        artDescription = response.meta['artDescription']
        artPubDate = response.meta['artPubDate']
        artLink=response.meta['artLink']
        artText = response.xpath('.//div[@id="articleContent"]//text()').extract()
        artText = ''.join(artText)
        artText_en = TextBlob(artText)
        artText_en = artText_en.translate(to='en')
        artText_en_polarity = artText_en.sentiment.polarity
        artText_en_subjectivity = artText_en.sentiment.subjectivity
        yield {
            'artTitle': artTitle,
            'artLink': artLink,
            'artDescription': artDescription,
            'artPubDate': artPubDate,
            'artText': artText,
            'artPolarity': artText_en_polarity,
            'artSubjectivity': artText_en_subjectivity
        }

       #  artLink = node.xpath('link/text()').extract()
       #  artTitle = node.xpath('title/text()').extract()
       #  artLink = node.xpath('link/text()').extract()
       #  artDescription = node.xpath('description/text()').extract()
       #  artPubDate = node.xpath('pubDate/text()').extract_first()
       #  # time format from "Sat, 23 Dec 2017 16:01:00 GMT" to "23 Dec 2017 16:01:00"
       #  artPubDate = artPubDate.split(',')[1:]
       #  artPubDate = ''.join(artPubDate)
       #  artPubDate = artPubDate.strip()
       #  artPubDate = artPubDate[:-4]
       #  artDescription = ''.join(artDescription)
       #  artDescription_en = TextBlob(artDescription)
       #  artDescription_en = artDescription_en.translate(to='en')
       #  artDescription_en_polarity = artDescription_en.sentiment.polarity
       #  artDescription_en_subjectivity = artDescription_en.sentiment.subjectivity
       #  yield {
       #      'artTitle': artTitle,
       #      'artLink': artLink,
       #      'artDescription': artDescription,
       #      'artPubDate': artPubDate,
       #      'artPolarity': artDescription_en_polarity,
       #      'artSubjectivity': artDescription_en_subjectivity
       #      }
       #

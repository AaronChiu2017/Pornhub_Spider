#coding:utf-8

import logging
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.selector import Selector
from PornHub.items import PornVideoItem
from scrapy.http import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import re
import json
# import random
class Spider(RedisCrawlSpider):
    name = 'pornHubSpider'
    allowed_domains = ['pornhub.com']

    # start_urls = ['https://www.pornhub.com/video?o=mv&cc=jp']
    redis_key = 'pornHubSpider:start_urls'
    # lpush pornHubSpider:start_urls https://www.pornhub.com
    logging.getLogger("requests").setLevel(logging.WARNING)  # 将requests的日志级别设成WARNING
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='cataline.log',
                filemode='w')
    # test = True
    rules = (
        Rule(LinkExtractor(allow=r'https://www\.pornhub\.com/video\?.+?page.+?'), callback='parse_ph_key', follow=True),
        Rule(LinkExtractor(allow=r'https://www\.pornhub\.com/embed/.+?'), callback='parse_ph_info'),
    )

    def parse_ph_key(self,response):
        selector = Selector(response)
        logging.debug('request url:------>' + response.url)
        # logging.info(selector)
        divs = selector.xpath('//a[@title]')
        for div in divs:
            s = div.extract()
            if 'viewkey' in s :
                viewkey = re.findall(r'viewkey=(ph.+?)"', s)
                if viewkey:
                    print viewkey[0]
                    yield Request(url='https://www.pornhub.com/embed/%s' % viewkey[0],callback = self.parse_ph_info, priority=100)

    def parse_ph_info(self,response):
        phItem = PornVideoItem()
        selector = Selector(response)
        _ph_info = re.findall('flashvars_.*?=(.*?);\n',selector.extract())
        logging.debug('PH信息的JSON:')
        logging.debug(_ph_info)
        if _ph_info:
            _ph_info_json = json.loads(_ph_info[0])
            duration = _ph_info_json.get('video_duration')
            phItem['video_duration'] = duration
            title = _ph_info_json.get('video_title')
            phItem['video_title'] = title
            image_url = _ph_info_json.get('image_url')
            phItem['image_url'] = image_url
            link_url = _ph_info_json.get('link_url')
            phItem['link_url'] = link_url
            quality_480p = _ph_info_json.get('quality_480p')
            phItem['quality_480p'] = quality_480p
            logging.info('duration:' + duration + ' title:' + title + ' image_url:' + image_url + ' link_url:' + link_url)
            yield phItem


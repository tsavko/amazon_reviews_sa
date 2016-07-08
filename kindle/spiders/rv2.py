# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
from kindle.items import KindleItem
import string


class Rv2Spider(CrawlSpider):
    """
    To start extracting data:
        * cd to kindle_reviews/kindle
        * scrapy crawl -o FILENAME.csv -t csv rv2

    """

    DOWNLOADER_MIDDLEWARES = {
            'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 300,
            'myspider.comm.random_proxy.RandomProxyMiddleware': 200,
    }

    RETRY_TIMES = 250

    name = 'rv2'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/Amazon-Kindle-6-Inch-4GB-eReader/product-reviews/B00I15SB16/ref=cm_cr_getr_d_show_all/188-9790737-3604954?ie=UTF8&showViewpoints=1&sortBy=helpful&pageNumber=1']

    rules = (
        Rule(LxmlLinkExtractor(restrict_xpaths=('//div[@id="cm_cr-pagination_bar"]')), callback='parse_item', follow=True),
    )



    def parse_item(self, response):
        i = KindleItem()
        review_list = response.xpath('//div[@id="cm_cr-review_list"]')
        review_list = review_list.xpath('//div[@class="a-section review"]')

        for rev in range(len(review_list)):
            soup = BeautifulSoup(review_list[rev].extract(), 'html.parser')

            i['Rating'] = float(soup.find('span', { "class" : "a-icon-alt" }).get_text()[:3])
            title_raw = soup.find('a', { "class" : "a-size-base a-link-normal review-title a-color-base a-text-bold" }).get_text().lower()
            exclude = set(string.punctuation)
            try:
                title_raw = ''.join(ch for ch in title_raw if ch not in exclude).replace('  ', ' ').decode('unicode_escape').encode('ascii','ignore')
            except UnicodeError:
                title_raw = ''.join(ch for ch in title_raw if ch not in exclude).replace('  ', ' ').replace(u'\\u2019', '')
            i['Title'] = title_raw
            review_raw = soup.find('span', { "class" : "a-size-base review-text" }).get_text().lower()#.replace('\\', '')#.encode('utf-8').replace('\\', '')
            try:
                review_raw = ''.join(ch for ch in review_raw if ch not in exclude).replace('  ', ' ').decode('unicode_escape').encode('ascii','ignore')
            except UnicodeError:
                review_raw = ''.join(ch for ch in review_raw if ch not in exclude).replace('  ', ' ').replace(u'\\u2019', '')
            i['Review'] = review_raw
            print '----------------------------------------------------------------------------------------------------------------'
            yield i

        print '================================================================================================================'
        

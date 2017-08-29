# -*- coding: utf8 -*-
from __future__ import absolute_import

from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from spider.spiders.goods import GoodsSpider
from spider.spiders.category import CategorySpider
from netease_spider.celery import app as celery_app

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})


@celery_app.task
def sync_goods():
    """
        异步任务爬取商品信息
    :return:
    """
    process = CrawlerProcess(get_project_settings())
    process.crawl(GoodsSpider)
    process.start()


@celery_app.task
def sync_category_banner():
    """
        异步任务爬取分类与Banner
    :return:
    """
    process = CrawlerProcess(get_project_settings())
    process.crawl(CategorySpider)
    process.start()

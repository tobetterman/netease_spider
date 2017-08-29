# -*- coding: utf8 -*-
from __future__ import absolute_import, print_function
import requests
from random import choice
from gevent.pool import Pool

from django.utils import timezone
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from spider.models import Proxy
from spider.spiders.proxy import ProxySpider
from netease_spider.celery import app as celery_app

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
_POOL_SIZE = 10


@celery_app.task
def sync_proxy():
    """
        定时任务爬取代理
    :return:
    """
    process = CrawlerProcess(get_project_settings())
    process.crawl(ProxySpider)
    process.start()


def check_proxy(proxy, timeout=30):
    _test_hosts = ('https://www.toutiao.com/'
                   , 'https://www.baidu.com'
                   , 'https://www.so.com/'
                   , 'https://www.sogou.com/')

    test_host = choice(_test_hosts)
    s = requests.session()
    proxies = {
        'http': proxy.host,
    }
    status = Proxy.ST_CHECKED
    try:
        s.get(test_host, timeout=timeout, proxies=proxies)
    except requests.Timeout:
        status = Proxy.ST_FAILD
    proxy.status, proxy.check_time = status, timezone.now()
    proxy.save()


@celery_app.task
def sync_check_proxy():
    """
        定时检查代理
    :return:
    """
    proxies = Proxy.objects.all()
    poll = Pool(_POOL_SIZE)
    poll.map(check_proxy, proxies)

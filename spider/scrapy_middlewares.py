# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from random import choice

from scrapy import signals
from scrapy.exceptions import NotConfigured

from spider.models import Proxy


class RotateUserAgentMiddleware(object):
    """
        user agent 随机
    """

    def __init__(self, user_agents):
        self.enabled = False
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        user_agents = crawler.settings.get('USER_AGENT_LIST', [])
        if not user_agents:
            raise NotConfigured("USER_AGENT_CHOICES not set or empty")

        o = cls(user_agents)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        self.enabled = getattr(spider, 'rotate_user_agent', self.enabled)

    def process_request(self, request, spider):
        if not self.enabled or not self.user_agents:
            return
        request.headers['user-agent'] = choice(self.user_agents)


class ProxyMiddleware(object):
    """
        随机从代理库中选取代理
    """

    def process_request(self, request, spider):
        # 选取最近刚检查过的代理中随机选取一个
        proxy = choice(Proxy.objects.filter(status=Proxy.ST_CHECKED).
                       order_by('-check_time')[:20])
        if proxy:
            request.meta['proxy'] = "http://{host}".format(proxy.host)

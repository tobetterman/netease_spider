# -*- coding:utf-8 -*-
import scrapy
import urlparse

from django.utils import timezone

from spider.models import Proxy


class ProxySpider(scrapy.Spider):
    """
        从快代理网站上爬取免费的代理
    """
    name = "proxy"

    start_urls = [
        'http://www.kuaidaili.com/free/intr/1/'
    ]

    PAGE_URL = 'http://www.kuaidaili.com/free/intr/{page}/'
    _MAX_PAGE = 3
    _MAX_FILED_DAY = 1
    _LAST_PAGE_INDEX = -2

    def parse(self, response):
        path = urlparse.urlparse(response.url).path
        curl_page = int(path.strip('/').split('/')[-1])
        if curl_page > self._MAX_PAGE:
            return
        proxies = response.xpath('//table/tbody/tr')
        # 爬取本页的所有代理
        for proxy in proxies:
            ip, port = proxy.xpath('td[@data-title="IP"]/text()').extract()[0], \
                       int(proxy.xpath('td[@data-title="PORT"]/text()').extract()[0])
            proxy = Proxy.objects.filter(ip=ip).first()
            if proxy and proxy.status in (Proxy.ST_INIT, Proxy.ST_CHECKED):
                continue
            # 如果存在这个记录, 当时check_time距离当前时间为一天,则重新置为新添加状态
            if proxy and proxy.status == Proxy.ST_FAILD:
                now = timezone.now()
                if (now - proxy.check_time).days >= self._MAX_FILED_DAY:
                    proxy.status = Proxy.ST_INIT
                    proxy.save()
            else:
                Proxy.objects.create(ip=ip, port=port)

        page_li = response.xpath('//div[@id="listnav"]/ul/li')
        last_page_num = int(page_li[self._LAST_PAGE_INDEX].xpath('a/text()')[0].extract())
        if curl_page > last_page_num:
            return

        next_page = curl_page + 1
        yield scrapy.Request(url=self.PAGE_URL.format(page=next_page), callback=self.parse)

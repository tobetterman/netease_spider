# -*- coding: utf8 -*-
from scrapy.utils.log import configure_logging
from django.core.management.base import BaseCommand

from spider.tasks import sync_proxy

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})


class Command(BaseCommand):

    help = u'从快代理同步代理信息'

    def handle(self, *args, **options):
        sync_proxy()

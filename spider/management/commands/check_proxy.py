# -*- coding: utf8 -*-
from scrapy.utils.log import configure_logging
from django.core.management.base import BaseCommand

from spider.tasks import sync_check_proxy

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})


class Command(BaseCommand):

    help = u'检查代理库中的状态'

    def handle(self, *args, **options):
        sync_check_proxy()

# -*- coding: utf8 -*-
from scrapy.utils.log import configure_logging
from django.core.management.base import BaseCommand

from goods.tasks import sync_goods

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})


class Command(BaseCommand):

    help = u'从严选同步商品信息'

    def handle(self, *args, **options):
        sync_goods()

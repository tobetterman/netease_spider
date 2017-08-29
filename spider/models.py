# -*- coding: utf8 -*-
import hashlib

from django.db import models

# Create your models here.


class CrawlLog(models.Model):
    """
        爬取网站的记录, 每次请求时根据hash去判断爬取的内容是否更新, 如果更新
        则更新hash和last_sync_time
    """

    PF_NETEASE = 1

    PF_CHOICE = (
        (PF_NETEASE, u'严选'),
    )

    TI_GOODS = 1
    TI_BANNER = 2
    TI_CATEGORY = 3

    TI_CHOICE = (
        (TI_GOODS, u'商品'),
        (TI_BANNER, u'banner'),
        (TI_CATEGORY, u'分类'),
    )

    platform_type = models.SmallIntegerField(u'爬取平台', choices=PF_CHOICE, default=PF_NETEASE)
    type_item = models.SmallIntegerField(u'爬取类型', choices=TI_CHOICE, null=False)
    item_id = models.BigIntegerField(null=False)
    hash = models.CharField(max_length=32, default='')
    create_time = models.DateTimeField(auto_now_add=True)
    last_sync_time = models.DateTimeField(default=None, null=True)

    class Meta:
        unique_together = ('platform_type', 'type_item', 'item_id')

    @staticmethod
    def gen_hash(params):
        valid_keys = sorted(k for k, v in params.iteritems() if v)
        msg = ['%s=%s' % (k, params[k]) for k in valid_keys]
        return hashlib.md5('&'.join(msg).encode('utf8')).hexdigest()


class Proxy(models.Model):
    """
        代理model
    """
    ST_INIT = 1
    ST_CHECKED = 2
    ST_FAILD = 3

    ST_CHOICE = (
        (ST_INIT, u'新添加'),
        (ST_CHECKED, u'已检查通过'),
        (ST_FAILD, u'失效'),
    )

    ip = models.IPAddressField(null=False, unique=True)
    port = models.IntegerField(null=False)
    status = models.IntegerField(choices=ST_CHOICE, default=ST_INIT)
    check_time = models.DateTimeField(default=None, null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    @property
    def host(self):
        return "{ip}:{port}".format(ip=self.ip, port=self.port)

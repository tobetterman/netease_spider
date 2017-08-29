# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from utils.storage import UniqueFileStorage


class Banner(models.Model):
    """
        首页轮播图
    """
    ST_STOP = 1
    ST_SHOW = 2

    ST_CHOICE = (
        (ST_STOP, u'停止展示'),
        (ST_SHOW, u'展示中')
    )

    href = models.URLField(default=None, blank=True, null=True)
    desc = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='banner/original/%Y/%m%d', max_length=70, storage=UniqueFileStorage())
    status = models.SmallIntegerField(default=ST_STOP, choices=ST_CHOICE)
    rank = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(default=None, blank=True, null=True)
    end_time = models.DateTimeField(default=None, blank=True, null=True)

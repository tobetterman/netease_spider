# -*- coding:utf8 -*-
from __future__ import unicode_literals
import json

from django.db import models

from utils.storage import UniqueFileStorage

PIL_TYPE_JPEG = 'jpeg'
PIL_TYPE_PNG = 'png'

DJANGO_TYPES = {
    PIL_TYPE_JPEG: 'image/jpg',
    PIL_TYPE_PNG: 'image/png'
}


class Photo(models.Model):
    """
        图片model 相同内容文件不保存
    """
    image = models.ImageField(upload_to='goods/original/%Y/%m%d', max_length=70, storage=UniqueFileStorage())
    img_hash = models.CharField(unique=True, max_length=32)
    add_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.image.url


class Tag(models.Model):
    """
        商品的tag
    """
    rank = models.IntegerField('排序标识, 降序', default=0)
    name = models.CharField("标签", max_length=16)
    cover = models.ImageField(upload_to="tag/%Y/%m%d", max_length=70, null=True, storage=UniqueFileStorage())
    note = models.CharField("标签说明", max_length=36, default='')

    @property
    def cover_img(self):
        if not self.cover or not self.cover.image:
            return Goods.DEFAULT_GOODS_IMAGE
        return self.cover.image.url


class CategoryManager(models.Manager):

    def get_category_by_level(self, level):
        level = level or []
        if not isinstance(level, (tuple, list)):
            level = [level]

        return self.filter(level__in=level)


class Category(models.Model):

    objects = CategoryManager()

    LEVEL_FIRST = 1
    LEVEL_SECOND = 2
    LEVEL_CHOICES = (
        (LEVEL_FIRST, u'一级分类'),
        (LEVEL_SECOND, u'二级分类'),
    )

    level = models.SmallIntegerField(u'分类级别', choices=LEVEL_CHOICES, default=LEVEL_FIRST, db_index=True)
    parent = models.IntegerField(u'父级分类遍号', db_index=True, null=True)
    rank = models.IntegerField('排序标识, 降序', default=0)
    name = models.CharField("类别", max_length=16)
    cover = models.ForeignKey("Photo", null=True, related_name='cover_goods')
    note = models.CharField("分类说明", max_length=36, default='')
    banner = models.ImageField(upload_to="category/banner/%Y/%m%d", max_length=70, null=True,
                               storage=UniqueFileStorage())
    icon = models.ImageField(upload_to="category/icon/%Y/%m%d", max_length=70, null=True,
                             storage=UniqueFileStorage())

    class Meta:
        unique_together = ('level', 'name', 'parent')

    @property
    def cover_img(self):
        if not self.cover or not self.cover.image:
            return None
        return self.cover.image.url


class GoodsCoverIntermediate(models.Model):

    photo = models.ForeignKey('Photo', related_name="intermediate_photo")
    goods = models.ForeignKey('Goods')
    rank = models.FloatField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)


class Goods(models.Model):

    ST_DELETED = 1
    ST_FOR_SALE = 2
    ST_CHOICES = (
        (ST_DELETED,     u'删除/下架'),
        (ST_FOR_SALE,    u'上架'),
    )
    name = models.CharField(max_length=60)
    status = models.SmallIntegerField('状态', choices=ST_CHOICES,
                                      db_index=True, default=ST_FOR_SALE)
    product_place = models.CharField(max_length=60, default='')
    price = models.IntegerField('参考价格，单位-分', default=0)

    cover = models.ManyToManyField("Photo", through=GoodsCoverIntermediate, null=True, related_name='goods')
    list_cover = models.ForeignKey("Photo", null=True, related_name='list_goods')

    unit = models.CharField("单位", max_length=10, default='')
    category = models.ForeignKey("Category", null=True)
    alias = models.CharField(u'别名', default='', max_length=80)
    rank = models.IntegerField("排序权重", default=1)
    sec_category = models.ForeignKey("Category", null=True, related_name='sec_goods')
    detail_html = models.TextField("详情图片Html", default='')
    json_attr = models.TextField(u'商品属性', default='')
    brief = models.CharField("简介", max_length=200, default='')

    @property
    def attr_list(self):
        return json.loads(self.json_attr)


class Comment(models.Model):
    """
        严选返回的评论内容中, 没有评论id, 没有用户id, 没有sku的id
    """
    DEFAULT_AVATAR = '/static/netease/img/default.jpg'

    goods = models.ForeignKey(Goods, related_name='comments')
    sku_info = models.TextField(u"保存sku的Json数据", default="")
    user_name = models.CharField(u"用户昵称", max_length=40)
    user_avatar = models.ImageField(upload_to="user/avatar/%Y/%m%d", max_length=70, null=True,
                               storage=UniqueFileStorage())
    photos = models.ManyToManyField("Photo", null=True, related_name='photo_comments')
    star = models.IntegerField(default=0)
    comment_time = models.DateTimeField(default=None, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=500, default='')

    @property
    def sku_dict(self):
        return json.loads(self.sku_info)

    @property
    def avator_url(self):
        if not self.user_avatar:
            return self.DEFAULT_AVATAR
        return self.user_avatar.url


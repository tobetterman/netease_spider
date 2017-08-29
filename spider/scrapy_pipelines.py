# -*- coding: utf-8 -*-
import json
import random
import hashlib
import requests
import datetime

from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from utils import img
from spider.scrapy_settings import USER_AGENT_LIST
from goods.models import (Photo, Category, Goods, GoodsCoverIntermediate
                          , Comment)
from spider.models import CrawlLog


class ExPipeline(object):
    """
        使用django ORM 将数据同步到数据库中
    """

    _LEVEL_MAPPING = {
        "L1":  Category.LEVEL_FIRST,
        "L2":  Category.LEVEL_SECOND,
    }

    _COMMENT_URI = 'http://you.163.com/xhr/comment/listByItemByTag.json'
    _PLATFORM = CrawlLog.PF_NETEASE

    def _get_category(self, item):
        """
            从商品详情中获取商品的分类信息
        :param item:
        :return:
        """
        if not item.get('categoryList'):
            raise
        cate_list = [category_info['id'] for category_info in item['categoryList']]
        return cate_list

    @staticmethod
    def _get_photo(url):
        """
            获取图片, 图片内容相同的直接返回Photo id
        :param url:
        :return:
        """
        rep = requests.get(url)
        if not rep:
            return
        content = rep.content
        md5 = hashlib.md5(content).hexdigest()
        photo = Photo.objects.values('id').filter(img_hash=md5).first()
        if photo:
            return photo['id']
        photo = Photo()
        file_name = '%s.png' % md5
        suf = SimpleUploadedFile(file_name, content)
        photo.img_hash = md5
        photo.image.save(file_name, suf, save=True)
        return photo.id

    def _get_goods_comments(self, goods):
        """
            url为http://you.163.com/xhr/comment/listByItemByTag.json?__timestamp=1503914650685&itemId=1079012
            获取商品的评论信息, 严选返回的评论信息中, 不包含评论的id,或者
            唯一能代表每一条评论的表示, 所以不是实现多次爬取, 所以仅能够通过判断
            商品上次同步中,是否含有评论, 如果没有则在爬评论, 否则代表已经爬过, 并且
            目前只爬取一页(多页有可能会爬到多重的评论)
        :param goods:
        :return:
        """
        url = self._COMMENT_URI.format(goods_id=goods.id)
        params = {"itemId": goods.id}
        ua = random.choice(USER_AGENT_LIST)

        headers = {
            'content-type': 'application/json',
            'User-Agent': ua
        }
        rep = requests.get(url, params=params, headers=headers)
        if not rep:
            return
        ret = rep.json()
        if ret['code'] != '200':
            return
        for comment_info in ret['data']['result']:
            comment = Comment.objects.create(
                goods_id=goods.id, sku_info=json.dumps(comment_info['skuInfo']), user_name=comment_info['frontUserName'],
                star=comment_info['star'], content=comment_info['content'],
                comment_time=datetime.datetime.fromtimestamp(int(comment_info['createTime'])/1000.0)
            )
            for pic_url in comment_info['picList']:
                comment.photos.add(self._get_photo(pic_url))
            if comment_info['frontUserAvatar']:
                file_name, suf = img.gen_django_img(comment_info['frontUserAvatar'])
                comment.user_avatar.save(file_name, suf, save=True)

    def _get_goods(self, item, fi_category, sec_category):
        goods, _ = Goods.objects.get_or_create(id=item['id'])

        goods.name, goods.price, goods.unit, goods.category_id, goods.sec_category_id\
            , goods.product_place, goods.rank, goods.detail_html, goods.json_attr, goods.brief = item['name'], item['retailPrice']\
            , item['pieceUnitDesc'], fi_category, sec_category, item['productPlace'], item['rank']\
            , item["itemDetail"]['detailHtml'], json.dumps(item['attrList']), item['simpleDesc']
        goods.save()
        photo_value = 0
        for key, value in item['itemDetail'].iteritems():
            if key == "detailHtml" or not value:
                continue
            photo_id = self._get_photo(value)
            imtermediate, _ = GoodsCoverIntermediate\
                .objects.get_or_create(photo_id=photo_id, goods_id=goods.id)
            imtermediate.order = photo_value
            imtermediate.save()
            photo_value += 1
        list_pic_url = item['listPicUrl']

        list_photo_id = self._get_photo(list_pic_url)
        goods.list_cover_id = list_photo_id
        goods.save()

        if not goods.comments.all():
            self._get_goods_comments(goods)

    def process_item(self, item, spider):
        fi_category, sec_category = self._get_category(item)
        param_hash = CrawlLog.gen_hash(item)

        crawl_log, _ = CrawlLog.objects.get_or_create(
            platform_type=self._PLATFORM, type_item=CrawlLog.TI_GOODS, item_id=item['id']
        )
        if crawl_log and crawl_log.hash == param_hash:
            return

        self._get_goods(item, fi_category, sec_category)
        crawl_log.hash, crawl_log.last_sync_time = param_hash, timezone.now()
        crawl_log.save()

# -*- coding:utf-8 -*-
from __future__ import absolute_import

import json
import scrapy

from spider.scrapy_settings import DEFAULT_TOP_CATEGORY


class GoodsSpider(scrapy.Spider):
    """
        爬取商品信息
    """
    name = "goods"
    allowed_domains = ["you.163.com"]
    # 商品详情页url
    item_base_url = "http://you.163.com/item/detail?id={id}"

    _GOOD_FILED = ('attrList', 'categoryList', 'id', 'itemDetail', 'itemTagList', 'name', 'listPicUrl',
                   'pieceUnitDesc', 'productPlace', 'rank', 'retailPrice', 'simpleDesc', 'retailPrice')

    def __init__(self, category=None, *args, **kwargs):
        super(GoodsSpider, self).__init__(*args, **kwargs)
        category = category if category else DEFAULT_TOP_CATEGORY
        self.start_urls = [
            "http://you.163.com/item/list?categoryId={category_id}".format(category_id=category)
        ]

    @classmethod
    def _get_subcategory_list(cls, response):
        """
            数据在script标签中, 获取script标签内容含有 var json_Data的数据
        :param response:
        :return:
        """
        ret = []
        data_content = response.xpath('//body/script/text()').re(r'\s*var\s*json_Data=(.*);')[0]
        if data_content:
            ret = json.loads(data_content)
        return ret

    @classmethod
    def _get_goods_detail(cls, response):
        """
            数据在script标签中, 获取script标签内容含有 var JSON_DATA_FROMFTL 的数据
        :param response:
        :return:
        """
        ret = {}
        data_content = response.xpath('//body/script/text()').re(r'.*JSON_DATA_FROMFTL\s*=\s*([\s\S]*);')[0]
        if data_content:
            ret = json.loads(data_content)
        return cls._format_goods_dict(ret['item']) if ret.get('item') else {}

    @classmethod
    def _format_goods_dict(cls, origin_goods):
        """
            从原始返回值中取出需要的字段,生成新字典
        :param origin_goods:
        :return:
        """
        return {key: value for key, value in origin_goods.iteritems() if key in cls._GOOD_FILED}

    def parse(self, response):
        data = self._get_subcategory_list(response)
        # 遍历分类下的二级分类内的商品, 构造商品详情页面url, 爬取商品数据
        for category_goods_list in iter(data["categoryItemList"]):
            for goods in category_goods_list["itemList"]:
                goods_id = goods.get('id', None)
                if not goods_id:
                    continue
                yield scrapy.Request(url=self.item_base_url.format(id=goods_id), callback=self.parse_goods)

    def parse_goods(self, response):
        yield self._get_goods_detail(response)

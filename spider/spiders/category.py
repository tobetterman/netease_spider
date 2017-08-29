# -*- coding:utf-8 -*-
from __future__ import absolute_import

import json
import scrapy
import urlparse

from django.utils import timezone
from django.core.urlresolvers import reverse

from utils import img
from netease.models import Banner
from spider.models import CrawlLog
from goods.models import Category, Goods
from spider.scrapy_settings import DEFAULT_TOP_CATEGORY


class CategorySpider(scrapy.Spider):
    """
        爬取所有服饰下的二级分类与一级分类下的banner图
    """
    name = "category"
    allowed_domains = ["you.163.com"]
    # 商品详情页url
    item_base_url = "http://you.163.com/item/detail?id={id}"

    _PLATFORM = CrawlLog.PF_NETEASE

    _VALID_BANNER_PATH = ('/item/list', '/item/detail')
    _VALID_HOST = ("you.163.com", )

    _LEVEL_MAPPING = {
        "L1":  Category.LEVEL_FIRST,
        "L2":  Category.LEVEL_SECOND,
    }

    def __init__(self, category=None, *args, **kwargs):
        super(CategorySpider, self).__init__(*args, **kwargs)
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

    def _format_category_condition_dict(self, category):
        category_id = category.get('id')
        if not category_id:
            return None
        return {
            "id": category_id, "name": category["name"], "parent": category["superCategoryId"],
            "level": self._LEVEL_MAPPING.get(category["level"]), "rank": category["showIndex"],
            "note": category['frontDesc']
        }

    def _format_banner_condition_dict(self, banner):
        """
            对banner的参数进行解析, 主要是分析bannel targetUrl
        :param banner:
        :return:
        """
        banner_id = banner.get('id')
        if not banner_id:
            return None
        target_url, href = banner["targetUrl"], None
        if target_url:
            target_parse = urlparse.urlparse(target_url)
            # 仅解析能够商品分类页面和商品详情页面
            if target_parse.hostname in self._VALID_HOST\
                    and target_parse.path in self._VALID_BANNER_PATH:
                query_dict = urlparse.parse_qs(target_parse.query)
                if 'subCategoryId' in query_dict:
                    category_id, sec_category_id = query_dict['categoryId'][0], query_dict['subCategoryId'][0]
                    # 如果存在参数中的一级分类和二级分类, 则将href转换为本站的url
                    if Category.objects.filter(pk__in=(category_id, sec_category_id)).exists():
                        href = reverse('category_view', kwargs={
                            "category_id": category_id, "sec_category_id": sec_category_id
                        })
                elif 'id' in query_dict:
                    goods_id = query_dict['id'][0]
                    if Goods.objects.filter(pk=goods_id).exists():
                        href = reverse('detail_view', kwargs={'id': goods_id})

        return {
            "id": banner_id, "desc": banner["name"], "href": href
        }

    def parse(self, response):
        data = self._get_subcategory_list(response)

        banner_list, sub_category_info_list = data["focusList"]\
            , [sub_category_info["category"] for sub_category_info in data["categoryItemList"]]

        for sub_category_info in sub_category_info_list:
            param_hash = CrawlLog.gen_hash(sub_category_info)
            crawl_log, _ = CrawlLog.objects.get_or_create(
                platform_type=self._PLATFORM, type_item=CrawlLog.TI_CATEGORY, item_id=sub_category_info['id']
            )
            # 更新过并且内容没有改变, 则不再更新
            if crawl_log and crawl_log.hash == param_hash:
                continue
            category_cond = self._format_category_condition_dict(sub_category_info)
            cate, _ = Category.objects.update_or_create(**category_cond)
            banner_url, icon_url = sub_category_info["bannerUrl"], sub_category_info["iconUrl"]
            if banner_url:
                file_name, suf = img.gen_django_img(banner_url)
                cate.banner.save(file_name, suf, save=True)
            if icon_url:
                file_name, suf = img.gen_django_img(banner_url)
                cate.icon.save(file_name, suf, save=True)

            crawl_log.hash, crawl_log.last_sync_time = param_hash, timezone.now()
            crawl_log.save()

        for banner_info in banner_list:
            try:
                banner_cond = self._format_banner_condition_dict(banner_info)
            except (ValueError, IndexError):
                continue

            param_hash = CrawlLog.gen_hash(banner_info)
            crawl_log, _ = CrawlLog.objects.get_or_create(
                platform_type=self._PLATFORM, type_item=CrawlLog.TI_BANNER, item_id=banner_info['id']
            )
            # 更新过并且内容没有改变, 则不再更新
            if crawl_log and crawl_log.hash == param_hash:
                continue
            banner_url = banner_info["picUrl"]
            if not banner_url:
                continue

            banner, _ = Banner.objects.update_or_create(**banner_cond)
            file_name, suf = img.gen_django_img(banner_url)
            banner.image.save(file_name, suf, save=True)
            crawl_log.hash, crawl_log.last_sync_time = param_hash, timezone.now()
            crawl_log.save()



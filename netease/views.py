# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.core.paginator import PageNotAnInteger

from netease.models import Banner
from goods.models import Category, Goods


class IndexView(TemplateView):
    """
        首页
    """
    template_name = "netease/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        category = Category.objects.all()
        goods = Goods.objects.filter(status=Goods.ST_FOR_SALE).order_by('rank')
        banners = Banner.objects.filter().order_by('rank')
        limit = 20
        paginator = Paginator(goods, limit)
        page = self.request.GET.get('page')
        try:
            goods = paginator.page(page)
        except PageNotAnInteger:
            goods = paginator.page(1)
        except Exception:
            goods = paginator.page(paginator.num_pages)

        context.update({
            "goods": goods,
            "category": category,
            'banners': banners

        })
        return context


class GoodsDetailView(TemplateView):
    """
        商品详情页
    """
    template_name = "netease/detail.html"

    def get_context_data(self, id, **kwargs):
        context = super(GoodsDetailView, self).get_context_data(**kwargs)
        goods = Goods.objects.get(pk=id)
        category = Category.objects.all()
        context.update({
            "goods": goods,
            "category": category
        })

        return context


class CategoryListView(TemplateView):
    """
        分类页
    """
    template_name = "netease/index.html"

    def get_context_data(self, category_id, sec_category_id, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        goods = Goods.objects.filter(category=category_id, sec_category=sec_category_id)
        category = Category.objects.all()
        limit = 20
        paginator = Paginator(goods, limit)
        page = self.request.GET.get('page')
        banners = Banner.objects.filter().order_by('rank')
        try:
            goods = paginator.page(page)
        except PageNotAnInteger:
            goods = paginator.page(1)
        except Exception:
            goods = paginator.page(paginator.num_pages)

        context.update({
            "goods": goods,
            "category": category,
            "banners": banners
        })

        return context


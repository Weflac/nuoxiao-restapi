# coding:utf-8

import django_filters
from nuoxiao.models import *

'''
    自定义过滤器
'''
class BlogsFilter(django_filters.rest_framework.FilterSet):
    # 点赞数 < or >
    min_link = django_filters.NumberFilter(name="links", lookup_expr='gte')
    max_link = django_filters.NumberFilter(name="links", lookup_expr='lte')
    class Meta:
        model = Article
        fields = ['min_link', 'max_link']


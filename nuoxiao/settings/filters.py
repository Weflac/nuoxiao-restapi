# coding:utf-8

import django_filters
from django_filters.rest_framework import FilterSet
from nuoxiao.models import *

'''
    Filter: 自定义过滤器
    搜索分页，条件查询
'''

class BlogsFilter(FilterSet):
    # 点赞数 < or >
    min_link = django_filters.NumberFilter(name="links", lookup_expr='gte')
    max_link = django_filters.NumberFilter(name="links", lookup_expr='lte')
    class Meta:
        model = Article
        fields = ['min_link', 'max_link']


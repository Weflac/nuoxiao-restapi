# coding:utf-8

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


'''
    自定义分页
'''

# 默认分页
class DefaultSetPagination(PageNumberPagination):
     page_size = 10
     max_page_size = 1000
     page_size_query_param = 'page_size'

# 自定义分页
class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })

# # 设置自定义分页、
# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS': 'my_project.apps.core.pagination.CustomPagination',
#     'PAGE_SIZE': 100
# }

# 特殊定制
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
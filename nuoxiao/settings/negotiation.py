# coding:utf-8

from rest_framework.negotiation import BaseContentNegotiation

'''
    Negotiation：内容协商
    内容协商是基于客户端或服务器偏好选择多种可能的表示之一以返回客户端的过程。
    部分由客户端驱动，部分由服务器驱动。

    1.更具体的媒体类型优先于较不特定的媒体类型。
    2.如果多种媒体类型具有相同的特性，则优先根据为给定视图配置的渲染器排序。
    Accept header:
    application/json; indent=4, application/json, application/yaml, text/html, */*
'''

# 自定义内容协商类
class IgnoreClientContentNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        return parsers[0]

    def select_renderer(self, request, renderers, format_suffix=None):
        return (renderers[0], renderers[0].media_type)
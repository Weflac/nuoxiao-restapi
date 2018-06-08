# coding:utf-8

from rest_framework import renderers
from rest_framework.parsers import BaseParser, FormParser
from rest_framework.exceptions import ParseError
from rest_framework.settings import api_settings
from rest_framework.utils import json

from django.conf import settings
import codecs
import six



'''
    Parser:解析器:
    就是对请求体进行解析。 为什么要有解析器？原因很简单，
    当后台和前端进行交互的时候数据类型不一定都是表单数据或者json，
    当然也有其他类型的数据格式，比如xml，所以需要解析这类数据格式就需要用到解析器(也可以将请求体拿到，然后利用其他模块进行解析)。
'''

class JSONParser(BaseParser):

    media_type = 'application/json'
    renderer_class = renderers.JSONRenderer
    strict = api_settings.STRICT_JSON

    def parse(self, stream, media_type=None, parser_context=None):  # 在源码中解读过，该方法用于解析请求体
        """
        Parses the incoming bytestream as JSON and returns the resulting data.
        """
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            decoded_stream = codecs.getreader(encoding)(stream)
            parse_constant = json.strict_constant if self.strict else None
            return json.load(decoded_stream, parse_constant=parse_constant)  # 本质使用json类进行解析
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % six.text_type(exc))



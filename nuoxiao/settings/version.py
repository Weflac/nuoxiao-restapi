# coding:utf-8

from rest_framework import exceptions
from rest_framework.utils.urls import replace_query_param
from rest_framework.versioning import BaseVersioning

'''
    Version:版本控制
    在我们给外部提供的API中，可会存在多个版本，
    不同的版本可能对应的功能不同，所以这时候版本使用就显得尤为重要
'''

class DefaultVersioning(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        version=request.query_params.get('version')
        return version

class QueryParameterVersioning(BaseVersioning):
    """
    GET /something/?version=0.1 HTTP/1.1
    Host: example.com
    Accept: application/json
    """
    invalid_version_message = ('Invalid version in query parameter.')  ## 当setting.py配置了允许的版本时候，不匹配版本返回的错误信息，可以自己定义

    ## 获取版本方法
    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get(self.version_param, self.default_version) # 通过request.query_paras方法获取（本质request.MATE.get），  default_version默认是version，是在settings中配置的

        if not self.is_allowed_version(version):     #不允许的版本抛出异常
            raise exceptions.NotFound(self.invalid_version_message)
        return version  #无异常则返回版本号

    def reverse(self, viewname, args=None, kwargs=None, request=None, format=None, **extra):  #url 反解析，可以通过该方法生成请求的url，后面会有示例
        url = super(QueryParameterVersioning, self).reverse(
            viewname, args, kwargs, request, format, **extra
        )
        if request.version is not None:
            return replace_query_param(url, self.version_param, request.version)
        return url

class URLPathVersioning(BaseVersioning):
    """
    To the client this is the same style as `NamespaceVersioning`.
    The difference is in the backend - this implementation uses
    Django's URL keyword arguments to determine the version.

    An example URL conf for two views that accept two different versions.

    urlpatterns = [
        url(r'^(?P<version>[v1|v2]+)/users/$', users_list, name='users-list'),
        url(r'^(?P<version>[v1|v2]+)/users/(?P<pk>[0-9]+)/$', users_detail, name='users-detail')
    ]

    GET /1.0/something/ HTTP/1.1
    Host: example.com
    Accept: application/json
    """
    invalid_version_message = ('Invalid version in URL path.')  # 不允许的版本信息，可定制

    def determine_version(self, request, *args, **kwargs):    ## 同样实现determine_version方法获取版本
        version = kwargs.get(self.version_param, self.default_version) # 由于传递的版本在url的正则中，所以从kwargs中获取，self.version_param默认是version

        if not self.is_allowed_version(version):
            raise exceptions.NotFound(self.invalid_version_message)     # 没获取到，抛出异常
        return version                                                  # 正常获取，返回版本号

    def reverse(self, viewname, args=None, kwargs=None, request=None, format=None, **extra):    # url反解析，后面会有示例
        if request.version is not None:
            kwargs = {} if (kwargs is None) else kwargs
            kwargs[self.version_param] = request.version
        return super(URLPathVersioning, self).reverse(viewname, args, kwargs, request, format, **extra)
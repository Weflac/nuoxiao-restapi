# coding:utf-8

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from nuoxiao.models import UserToken


class Authentication(BaseAuthentication):
    """
    认证类
    """
    def authenticate(self, request):
        token = request._request.GET.get("token")
        toke_obj = UserToken.objects.filter(token=token).first()
        if not toke_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        return (toke_obj.user, toke_obj)  # 这里返回值一次给request.user,request.auth

    def authenticate_header(self, val):
        pass

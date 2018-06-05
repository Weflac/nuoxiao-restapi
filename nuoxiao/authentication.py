from django.shortcuts import  HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from . import models
from rest_framework import exceptions
import hashlib
import time


class Authentication(BaseAuthentication):
    """
    认证类
    """
    def authenticate(self, request):
        token = request._request.GET.get("token")
        toke_obj = models.UserToken.objects.filter(token=token).first()
        if not toke_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        return (toke_obj.user, toke_obj)  # 这里返回值一次给request.user,request.auth

    def authenticate_header(self, val):
        pass

def md5(user):
    ctime = str(time.time())
    m = hashlib.md5(bytes(user,encoding="utf-8"))
    m.update(bytes(ctime,encoding="utf-8"))
    return m.hexdigest()

class AuthView(APIView):
    """登陆认证"""
    def dispatch(self, request, *args, **kwargs):
        return super(AuthView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse('get')

    def post(self, request, *args, **kwargs):

        ret = {'code': 1000, 'msg': "登录成功"}
        try:
            user = request._request.POST.get("username")
            pwd = request._request.POST.get("password")
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = "用户名或密码错误"
            else:
                token = md5(user)
                models.UserToken.objects.update_or_create(user=obj, defaults={"token": token})
                ret['token'] = token

        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = "请求异常"

        return JsonResponse(ret)


#
# class OrderView(APIView):
#     '''查看订单'''
#     from utils.permissions import MyPremission
#     from utils.version import Myversion
#     authentication_classes = [Authentication,]    #添加认证
#     permission_classes = [MyPremission,]           #添加权限控制
#     versioning_class = Myversion
#     def get(self,request,*args,**kwargs):
#         print(request.version)
#
#         ret = {'code':1000,'msg':"你的订单已经完成",'data':"买了一个mac"}
#         return JsonResponse(ret,safe=True)
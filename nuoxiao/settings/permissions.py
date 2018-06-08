# coding:utf-8

from rest_framework import permissions
from nuoxiao.models import Blacklist

"""
    使用方法：

    继承BasePermission类(推荐)
    重写has_permission方法
    has_permission方法返回True表示有权访问，False无权访问

    ###全局使用
    REST_FRAMEWORK = {
       #权限
        "DEFAULT_PERMISSION_CLASSES":['API.utils.permission.MyPremission'],
    }

    ##单一视图使用,为空代表不做权限验证
    permission_classes = [MyPremission,]

    ###优先级
    单一视图>全局配置

"""

'''
    对象级权限,访问权限控制
    **允许登录的用户访问请求权限，session名=users_id
'''
class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if  request.method in permissions.SAFE_METHODS:
            return True
        return request.session.get('users_id') is not None

    # def has_object_permission(self, request, view, obj):
    #     # Read permissions are allowed to any request,
    #     # so we'll always allow GET, HEAD or OPTIONS requests.
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #      # return obj.author == request.users
    #     return obj.author.id == request.session.get('users_id')

    # def has_object_permission(self, request, view, obj):
    #     # Read permissions are allowed to any request,
    #     # so we'll always allow GET, HEAD or OPTIONS requests.
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #
    #     # Instance must have an attribute named `owner`.
    #     return obj.owner == request.user


'''
    使用实例，检查用户IP是否在黑名单中
'''
class BlacklistPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """
    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']  # 用户IP地址
        blacklisted = Blacklist.objects.filter(ip_addr=ip_addr).exists()
        return not blacklisted
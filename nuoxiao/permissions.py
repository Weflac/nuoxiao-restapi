from rest_framework import permissions

'''
    访问权限控制
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



"""restapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.urls import path, include
from django.contrib import admin
from nuoxiao.views import *

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework.urlpatterns import format_suffix_patterns

API_TITLE = '自定义接口视图(API)'
API_DESCRIPTION = '用于创建和查看突出显示的代码片段的Web API'
schema_view = get_schema_view(title=API_TITLE)


snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list = UsersViewSet.as_view({
    'get': 'list'
})
user_detail = UsersViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path(r'snippets/', snippet_list, name='snippet-list'),
    path(r'snippets/(?P<pk>[0-9]+)/', snippet_detail, name='snippet-detail'),
    path(r'snippets/(?P<pk>[0-9]+)/highlight/', snippet_highlight, name='snippet-highlight'),
    path(r'users/', user_list, name='user-list'),
    path(r'users/(?P<pk>[0-9]+)/', user_detail, name='user-detail'),

    # ViewSet and Routers
    path(r'api/v1/', include('nuoxiao.urls')),
    # View
    path(r'admin/', admin.site.urls),
    # APIView
    path(r'api/v1/register/', UserRegisterAPIView.as_view()),
    path(r'api/v1/login/', UserLoginAPIView.as_view()),
    path(r'api/v1/logout/', LogoutAPIView.as_view()),

    path(r'api/v1/snippet/', SnippetList.as_view()),
    path(r'api/v1/snippet/<int:id>/', SnippetDetail.as_view()),

    path(r'api/v1/userlist/', ListUsers.as_view()),
    path(r'api/v1/roles/', RoleView.as_view()),
    # @api_view
    path(r'api/v1/hello/', hello_world),
    path(r'api/v1/tag-list/', tag_list),
    path(r'api/v1/tag-detail/', tag_detail),
    path(r'api/v1/userinfo/', UserinfoView.as_view()),
    path(r'api/v1/userinfo-model/', UserinfoModelView.as_view()),

    # system
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'schema/',schema_view),
    path(r'docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    path(r'api-token-auth/', views.obtain_auth_token)
]

#
# urlpatterns = format_suffix_patterns([
#     path(r'snippets/', snippet_list, name='snippet-list'),
#     path(r'snippets/(?P<pk>[0-9]+)/', snippet_detail, name='snippet-detail'),
#     path(r'snippets/(?P<pk>[0-9]+)/highlight/', snippet_highlight, name='snippet-highlight'),
#     path(r'users/', user_list, name='user-list'),
#     path(r'users/(?P<pk>[0-9]+)/', user_detail, name='user-detail'),
#
#     # ViewSet and Routers
#     path(r'api/v1/', include('nuoxiao.urls')),
#     # View
#     path(r'admin/', admin.site.urls),
#     # APIView
#     path(r'api/v1/register/', UserRegisterAPIView.as_view()),
#     path(r'api/v1/login/', UserLoginAPIView.as_view()),
#     path(r'api/v1/logout/', LogoutAPIView.as_view()),
#
#     path(r'api/v1/snippet/', SnippetList.as_view()),
#     path(r'api/v1/snippet-detail/', SnippetDetail.as_view()),
#
#     path(r'api/v1/userlist/', ListUsers.as_view()),
#     path(r'api/v1/roles/', RoleView.as_view()),
#     # @api_view
#     path(r'api/v1/hello/', hello_world),
#     path(r'api/v1/tag-list/', tag_list),
#     path(r'api/v1/tag-detail/', tag_detail),
#     path(r'api/v1/userinfo/', UserinfoView.as_view()),
#     path(r'api/v1/userinfo-model/', UserinfoModelView.as_view()),
#
#     path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#     path(r'schema/', schema_view),
#     path(r'docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION))
# ])

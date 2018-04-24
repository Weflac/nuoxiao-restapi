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
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

API_TITLE = '引擎收录 API'
API_DESCRIPTION = '用于创建和查看突出显示的代码片段的Web API'
schema_view = get_schema_view(title=API_TITLE)

urlpatterns = [
    path(r'', include('nuoxiao.urls')),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'schema/',schema_view),
    path(r'docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION))
]
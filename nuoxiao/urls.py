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
from rest_framework.routers import DefaultRouter
from nuoxiao import views

router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

router.register(r'users', views.UsersViewSet)
router.register(r'garden', views.GardenViewSet)
router.register(r'blogs', views.BlogsViewSet)
router.register(r'Commons', views.CommonsViewSet)

# router.register(r'users', views.UserSerializer, base_name='users')

urlpatterns = [
    # path(r'demo/', views.demo),
    path(r'',include(router.urls)),
    # path(r'snippets/', views.snippet_list),
    # path(r'snippets/(?P<pk>[0-9]+)/', views.snippet_detail),
]
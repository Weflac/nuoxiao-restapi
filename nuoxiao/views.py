from django.contrib.auth.models import User, Group

from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import detail_route,action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from nuoxiao.models import Snippet
from nuoxiao.permissions import IsOwnerOrReadOnly
from nuoxiao.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    # @action(detail=True)
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# 用户登录
class UserLoginAPIView(APIView):
    queryset = Users.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        users = Users.objects.get(username__exact=username)
        if users.password == password:
            serializer = UserLoginSerializer(users)
            new_data = serializer.data
            # 记忆已登录用户
            self.request.session['users_id'] = users.id
            return Response(new_data, status=HTTP_200_OK)
        return Response('password error', HTTP_400_BAD_REQUEST)

# 用户登出
class LogoutAPIView(APIView):
    def post(self, requests, format=None):
        if self.request.session['users_id'] is not None:
            self.request.session['users_id'] = None
            return Response({"message":"登出成功"}, status=HTTP_200_OK)
        else:
            return Response({"message":"暂未登陆，无需登出"}, status=HTTP_400_BAD_REQUEST)

# 用户注册
class UserRegisterAPIView(APIView):
    queryset = Users.objects.all()
    serializer_class = UsersRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format = None):
        data = request.data
        username = data.get('username')
        if Users.objects.filter(username__exact=username):
            return Response("用户名已存在", HTTP_400_BAD_REQUEST)

        serializer = UsersRegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# 用户信息列表
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

# 园子信息
class GardenViewSet(viewsets.ModelViewSet):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer

# 用于博客的增删改查  除了查看，其他都需要权限
class BlogsViewSet(viewsets.ModelViewSet):
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer
    permission_classes = (IsOwnerOrReadOnly,)   # 添加权限控制

    # def perform_create(self, serializer):
    #     serializer.save(author=Users.objects.get(id=self.request.session.get('users_id')))


class CommontViewSet
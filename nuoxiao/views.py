from django.contrib.auth.models import User, Group
from django.http import Http404

from rest_framework import status, viewsets, permissions, renderers, authentication
from rest_framework.decorators import detail_route
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

class SnippetList(APIView):
    """
    列出所有代码片段(snippets), 或者新建一个代码片段(snippet).
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
    """
    读取, 更新 or 删除一个代码片段(snippet)实例(instance).
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

# 基于类的视图
class ListUsers(APIView):

    """
   列出系统中的所有用户

   * 需要 token 认证。
   * 只有 admin 用户才能访问此视图。
   """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser)

    def get(self, request, format = None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all().values('id','username')]

        return Response(usernames)



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

# 评论
class CommonsViewSet(viewsets.ModelViewSet):
    queryset = Commons.objects.all()
    serializer_class = CommonsSerializer


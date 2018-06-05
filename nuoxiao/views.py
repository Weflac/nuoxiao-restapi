from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, permissions, renderers, authentication, filters
from rest_framework.decorators import api_view, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView


from nuoxiao.permissions import IsOwnerOrReadOnly
from nuoxiao.serializers import *

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
    # Premissions
    # 顾名思义就是权限管理，用来给
    # ViewSet
    # 设置权限，使用
    # premissions
    # 可以方便的设置不同级别的权限：
    #
    # 全局权限控制
    # ViewSet
    # 的权限控制
    # Method
    # 的权限
    # Object
    # 的权限
    # 被
    # premission
    # 拦截的请求会有如下的返回结果：
    #
    # 当用户已登录，但是被
    # premissions
    # 限制，会返回
    # HTTP
    # 403
    # Forbidden
    # 当用户未登录，被
    # premissions
    # 限制会返回
    # HTTP
    # 401
    # Unauthorized
    # 默认的权限
    # rest_framework
    # 中提供了七种权限
    #
    # AllowAny  # 无限制
    # IsAuthenticated  # 登陆用户
    # IsAdminUser  # Admin 用户
    # IsAuthenticatedOrReadOnly  # 非登录用户只读
    # DjangoModelPermissions  # 以下都是根据 Django 的 ModelPremissions
    # DjangoModelPermissionsOrAnonReadOnly
    # DjangoObjectPermissions
    #

    #  http://127.0.0.1:1314/api/v1/snippets/1/highlight/ 自定义方法
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetList(APIView):
    """
    列出所有代码片段(snippets), 或者新建一个代码片段(snippet).
    """
    def get(self, request ):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(instance=snippets, many=True, context={'request': request} )
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


'''
  APIView 视图
'''
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
    # authentication_classes = (authentication.TokenAuthentication,)                  # Token 认证
    permission_classes = (permissions.IsAdminUser)                              #  权限策略属性

    def check_permissions(self, request):
        return Response()

    def get(self, request, format = None):
        """
        Return a list of all users.
        """
        print('user=', Users.objects.all())
        usernames = [user.username for user in Users.objects.all()]
        return Response(usernames)

# 自定义视图
class UserinfoView(APIView):
    """用户信息"""
    def get(self, request, *args, **kwargs):
        users= Users.objects.all() # models.UserInfo.objects.all()
        res=UserinfoSerializer(instance=users,many=True) # instance接受queryset对象或者单个model对象，当有多条数据时候，使用many=True,单个对象many=False
        return Response(res.data, status=status.HTTP_200_OK)

class UserinfoModelView(APIView):
    """用户信息"""
    def get(self,request,*args,**kwargs):
        users= Users.objects.all()  # models.UserInfo.objects.all()
        res=UserinfoModelSerializer(instance=users,many=True) #instance接受queryset对象或者单个model对象，当有多条数据时候，使用many=True,单个对象many=False
        return Response( res.data,  status=status.HTTP_200_OK )


'''
  @api_view() 方法视图
'''
@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})

@api_view(['GET', 'POST'])
def tag_list(request):

    if request.method == 'GET':
        tag = Tag.objects.all()
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def tag_detail(request, name):
    """
    读取, 更新 或 删除 一个代码片段实例（snippet instance）。
    """
    try:
        tag = Tag.objects.get(name=name)
    except Tag.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

'''
    ViewSet 和 Routers
    ModelViewSet
    自身提供了六种方法
    list
    create
    retrieve
    update
    partial_update
    destroy
'''
# 角色
class RoleView(APIView):
    def get(self, request, format=None):
        roles = Role.objects.all()
        serializers = RoleSerializer(roles, many=True, context={request:request})
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = RoleSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# 用户信息
class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    filter_backends = (filters.SearchFilter) # 过滤筛选
    search_fields = ('title', 'title')
    # '^'开始 - 搜索。
    # '='完全匹配。
    # '@'全文搜索。（目前只支持Django的MySQL后端。）
    # '$'正则表达式搜索。
    # 例如：
    # search_fields = ('=username', '=email')


# 角色
class RolesViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

# 权限
class PermissionsViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

# 组织
class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class =  OrganizationSerializer

# 园子信息
class GardenViewSet(viewsets.ModelViewSet):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer

# 用于博客的增删改查  除了查看，其他都需要权限
class BlogsViewSet(viewsets.ModelViewSet):
    queryset = Blogs.objects.all()
    serializer_class = BlogsSerializer
    filter_backends = (DjangoFilterBackend,)  # 过滤
    filter_fields = ('title', 'subtitle')

    permission_classes = (IsOwnerOrReadOnly,)   # 添加权限控制

    # def perform_create(self, serializer):
    #     serializer.save(author=Users.objects.get(id=self.request.session.get('users_id')))

# 评论
class CommonsViewSet(viewsets.ModelViewSet):
    queryset = Commons.objects.all()
    serializer_class = CommonsSerializer

# 标签
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

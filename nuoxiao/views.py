# coding:utf-8


# django 模块
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
# rest framework 模块
from rest_framework import status, viewsets, renderers, filters
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
# 自定义模块
from nuoxiao.settings.permissions import *
from nuoxiao.serializers import *
from nuoxiao.settings.filters import *
from nuoxiao.settings.pagination import *
from nuoxiao.utils import commons
from nuoxiao.settings import version, throttle

from numpy import unicode

'''
    实例 Snippet
'''
class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # 权限认证
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )
    #  http://127.0.0.1:1314/api/v1/snippets/1/highlight/
    # 自定义的方法，用来处理不是标准create/update/delete的请求，默认处理get请求，可以通过参数methods=POST来处理POST请求，或其他
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer], methods='GET')
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet)

    def get(self, inst, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet)

class SnippetList(APIView):
    """
    列出所有代码片段(snippets), 或者新建一个代码片段(snippet).
    """
    versioning_class = version.URLPathVersioning    # 添加版本控制

    def get(self, request ):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(instance=snippets, many=True, context={'request': request} )
        url = request.versioning_scheme.reverse(viewname='user_view', request=request)
        # versioning_scheme已经在源码中分析过了，就是版本类实例化的对象
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
    def get_object(self, id):
        try:
            return Snippet.objects.get(id=id)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None, **kwargs):
        snippet = self.get_object(id)
        serializer = SnippetSerializer(instance=snippet, data=request.data, context={'request': request}, **kwargs)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None, **kwargs):
        snippet = self.get_object(id)
        serializer = SnippetSerializer(instance=snippet, data=request.data, context={'request': request}, **kwargs)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        snippet = self.get_object(id)
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

class AuthView(APIView):
    """登陆认证"""
    def dispatch(self, request, *args, **kwargs):
        return super(AuthView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return Response('get')

    def post(self, request, *args, **kwargs):

        ret = {'code': 1000, 'msg': "登录成功"}
        try:
            name = request._request.POST.get("username")
            pwd = request._request.POST.get("password")
            user = Users.objects.filter(username=name, password=pwd).first()
            if not user:
                ret['code'] = 1001
                ret['msg'] = "用户名或密码错误"
            else:
                token = commons.md5(user)
                UserToken.objects.update_or_create(user=user, defaults={"token": token})
                ret['token'] = token

        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = "请求异常"

        return Response(ret)



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
#         return Response(ret, safe=True)
#

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
    authentication_classes = (SessionAuthentication, BasicAuthentication, )  # Token 认证
    permission_classes = (permissions.IsAdminUser,)      # 权限策略属性
    versioning_class = version.URLPathVersioning    # 添加版本控制

    def check_permissions(self, request):
        return Response()

    def get(self, request, format = None):
        """
        Return a list of all users.
        """
        print('version=', request.version)
        url = request.versioning_scheme.reverse(viewname='user_view', request=request)  # url反解析
        print('url=', url)
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
def tag_list(request, *args, **kwargs):

    if request.method == 'GET':
        tag = Tags.objects.all()
        serializer = TagSerializer(instance=tag,data=request.data, context={'request': request}, **kwargs)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def tag_detail(request, *args, **kwargs):
    """
    读取, 更新 或 删除 一个代码片段实例（snippet instance）。
    """
    try:
        tag = Tags.objects.get(*args)
    except Tags.DoesNotExist:
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

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)   # 过滤筛选
    filter_fields = ('subject', 'username')
    search_fields = ('=username', '=subject')
    ordering_fields = ('username', 'dateTime',)

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

# 园子
class GardenViewSet(viewsets.ModelViewSet):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer

# 用于博客的增删改查  除了查看，其他都需要权限
class ArticlesViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticlesSerializer

    pagination_class = DefaultSetPagination  # 分页

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)  # 过滤,搜索，排序
    filter_fields = ('title', 'subtitle')
    # 在ViewSet中添加自定义过滤
    filter_class = BlogsFilter
    search_fields = ('title', 'subtitle')
    ordering_fields = ('reads', 'links', 'dateTime',)


    permission_classes = (IsOwnerOrReadOnly,)   # 添加权限控制

    def perform_create(self, serializer):
        serializer.save(author=Users.objects.get(id=self.request.session.get('users_id')))

# 评论
class CommonsViewSet(viewsets.ModelViewSet):
    queryset = Commons.objects.all()
    serializer_class = CommonsSerializer

'''
    标签
    #permissions.AllowAny: 允许所有
    #路径：rest_framework.permissions
    ##基本权限验证
    class BasePermission(object)

    ##允许所有
    class AllowAny(BasePermission)

    ##基于django的认证权限，官方示例
    class IsAuthenticated(BasePermission):

    ##基于django admin权限控制
    class IsAdminUser(BasePermission)

    ##也是基于django admin
    class IsAuthenticatedOrReadOnly(BasePermission)
'''
@permission_classes((permissions.AllowAny,))
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer

    permission_classes = (permissions.IsAuthenticated, ) # 添加权限控制 # IsOwnerOrReadOnly, permissions.IsAdminUser,
    authentication_classes = (SessionAuthentication, BasicAuthentication)   # 添加认证
    throttle_classes = (throttle.VisitThrottle,)    # 添加访问频率， #单一视图使用 ，#优先级  单一视图 > 全局
    versioning_class = (version.URLPathVersioning,)    # 添加版本

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        print('测试：',content)
        return Response(content)

    # def get(self, *args, **kwargs):
    #     return  Response()

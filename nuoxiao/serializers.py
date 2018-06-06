
from rest_framework import serializers
from nuoxiao.models import *

'''
    自定义序列化
'''
class UserinfoSerializer(serializers.Serializer): #定义序列化类
    id=serializers.IntegerField()  #定义需要提取的序列化字段,名称和model中定义的字段相同

    username=serializers.CharField()
    password=serializers.CharField()
    #sss=serializers.CharField(source='user_type') #该方法只能拿到user_type的ID
    sss=serializers.CharField(source='roles.name') #自定义字段名称，和数据模型不一致，需要指定source本质调用get_user_type_display()方法获取数据
    gp=serializers.CharField(source='organization.name') #本质拿到group对象，取对象的name,
    #rl=serializers.CharField(source='roles.all.first.name')
    rl=serializers.SerializerMethodField()   #多对多序列化方法一

    def get_rl(self,obj): #名称固定：get_定义的字段名称
        """
        自定义序列化
        :param obj:传递的model对象，这里已经封装好的
        :return:
        """
        roles=obj.roles.all().values() #获取所有的角色

        return list(roles)  #返回的结果一定有道是json可序列化的对象

class UserinfoModelSerializer(serializers.ModelSerializer):  # 定义序列化类
    id = serializers.IntegerField()  # 定义需要提取的序列化字段,名称和model中定义的字段相同

    username = serializers.CharField()
    password = serializers.CharField()
    # sss=serializers.CharField(source='user_type') #该方法只能拿到user_type的ID
    sss = serializers.CharField(
        source='roles.name')  # 自定义字段名称，和数据模型不一致，需要指定source本质调用get_user_type_display()方法获取数据
    gp = serializers.CharField(source='organization.name')  # 本质拿到group对象，取对象的name,
    # rl=serializers.CharField(source='roles.all.first.name')
    rl = serializers.SerializerMethodField()  # 多对多序列化方法一

    def get_rl(self, obj):  # 名称固定：get_定义的字段名称
        """
        自定义序列化
        :param obj:传递的model对象，这里已经封装好的
        :return:
        """
        roles = obj.roles.all().values()  # 获取所有的角色

        return list(roles)  # 返回的结果一定有道是json可序列化的对象

    class Meta:
        model = Users
        fields = ['id', 'username', 'password', 'sss', 'rl', 'gp']  # 配置要序列化的字段
        # fields = "__all__" 使用model中所有的字段

'''
    url 关联链接序列化
'''
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight',lookup_field='name', lookup_url_kwarg='pk', format='html')
    # look = serializers.HyperlinkedIdentityField(view_name='snippet-list', lookup_field='name', lookup_url_kwarg='pk')
    # view_name，urls.py目标url的视图别名（name），这里是UserGroup的视图别名
    # lookup_field 给url传递的参数，也就是正则匹配的字段
    # lookup_url_kwarg，url中正则名称，也就是kwargs中的key

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style')
        # extra_kwargs = {'highlight','lookup_field','title'}

class SnippetHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
    look = serializers.HyperlinkedIdentityField(view_name='snippet-list', lookup_field='name', lookup_url_kwarg='pk')
    # view_name，urls.py目标url的视图别名（name），这里是UserGroup的视图别名
    # lookup_field 给url传递的参数，也就是正则匹配的字段
    # lookup_url_kwarg，url中正则名称，也就是kwargs中的key

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style', 'look')
        # extra_kwargs = {'highlight','lookup_field','title'}

'''
    model序列化
'''
# 用户注册
class UsersRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'username', 'password')

    # def list(self, request):
    #     queryset = Users.objects.all().values('id','username')
    #     serializer = UserSerializer(queryset, context={'request': request}, many=True)
    #     return Response(serializer.data)

# 用户登录
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__" # 使用model中所有的字段
        # fields = ('id','username','password')
        read_only_fields = ('password',)  # 指定只读的 field

# 自定义相关字段
class BlogsListField(serializers.RelatedField):
    def to_representation(self, value):
        return 'blogs_id:%d,blogs_title:%s' % (value.id, value.title)

# 用户
class UsersSerializer(serializers.ModelSerializer):
    # blog_set = serializers.PrimaryKeyRelatedField(many=True, queryset=Blog.objects.all())
    # blog_set = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='blog-detail')
    # blog_set = serializers.StringRelatedField(many=True)
    # blog_set = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    # blog_listing = serializers.HyperlinkedIdentityField(view_name='blog-detail')
    blogs_set = BlogsListField(many=True,  read_only=True)

    class Meta:
        model = Users
        fields = ('id', 'username', 'nickname', 'subject', 'introduce', 'icon', 'dateTime', 'blogs_set', 'organization', 'roles')  # 'blogs_set'

# 角色
class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.ReadOnlyField(source='permission.name')

    class Meta:
        model = Role
        # fields = "__all__" # 使用model中所有的字段
        fields = ('id', 'name', 'default', 'permissions')
        depth = 1  # 系列化深度，1~10，建议使用不超过3

# 权限
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name', 'code', 'enable', 'parentId')

# 组织
class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'enable', 'parentId')


# 园子
class GardenSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Garden
        fields = ( 'id', 'name', 'introduce', 'cover_url', 'description', 'dateTime', 'author')
# 博客
class BlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ('id', 'title', 'subtitle', 'introduction', 'description', 'imgurl', 'dateTime', 'links', 'reads', 'garden',  'author')

    def create(self, validated_data):
        """响应 POST 请求"""
        # 自动为用户提交的 model 添加 owner
        validated_data['author'] = self.context['request'].author
        return Blogs.objects.create(**validated_data)

    def update(self, blogs, validated_data):
        """响应 PUT 请求"""
        blogs.field = validated_data.get('subtitle', blogs.subtitle)
        blogs.save()
        return blogs

    def destroy(self, pk):
        """响应 delete 请求"""
        blogs = Blogs.objects.get(id=pk)
        blogs.delete()

# 评论
class CommonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commons
        # fields = "__all__"
        fields = ('id', 'parentId', 'title', 'contnet', 'references', 'replys', 'dateTime', 'links', 'blogs',  'author')
# 标签
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('url','id', 'name', 'slug')
















# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

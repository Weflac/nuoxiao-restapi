from django.contrib.auth.models import User, Group
from rest_framework import serializers
from nuoxiao.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style')

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
        fields = ('id','username','password')


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
        fields = ('id', 'username', 'nickname', 'subject', 'introduce', 'icon', 'dateTime','blogs_set')  # 'blogs_set'
# 园子
class GardenSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Garden
        fields = ( 'id', 'name', 'introduce', 'cover_url', 'description', 'dateTime','author')
# 博客
class BlogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = ( 'id', 'title', 'subtitle', 'introduction', 'description', 'imgurl', 'dateTime', 'links', 'reads', 'garden',  'author')

# 评论
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commons
        fields = "__all__"



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

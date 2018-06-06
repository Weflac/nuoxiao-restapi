from django.db import models
from django.urls import reverse

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class Snippet(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField(null=True)
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES,default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES,default='friendly', max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()


    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter( style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)

        super(Snippet, self).save(*args, **kwargs)


# 组织
class Organization(models.Model):
    name = models.CharField(max_length=50, verbose_name='组织名称')
    enable = models.BooleanField(verbose_name='启用', default=True)
    parentId = models.IntegerField(verbose_name='引用ID')

    def __str__(self):
        return self.name

# 权限
class Permission(models.Model):
    name = models.CharField(max_length=50, verbose_name='权限名称')
    code = models.CharField(max_length=36, verbose_name='权限编码')
    enable = models.BooleanField(verbose_name='启用', default=True)
    parentId = models.IntegerField(verbose_name='引用ID')

    def __str__(self):
        return self.name

# 角色
class Role(models.Model):
    name = models.CharField(max_length=50, verbose_name='角色名称')
    default = models.BooleanField(verbose_name='是否默认角色')
    permission = models.ManyToManyField(Permission, verbose_name='权限')

    def __str__(self):
        return self.name


# 用户
class Users(models.Model):
    username = models.CharField(max_length=20, unique=True, null=True, verbose_name='用户名')
    password = models.CharField(max_length=20, null=True, verbose_name='密码')
    phone = models.CharField(max_length=11, null=True, verbose_name='手机号码')
    email = models.EmailField(max_length=50, null=True, verbose_name='邮箱')
    nickname = models.CharField(max_length=50, null=True, verbose_name='昵称')
    subject = models.CharField(max_length=50, null=True, verbose_name='主题')
    introduce = models.CharField(max_length=140, null=True, verbose_name='简介')
    icon = models.CharField(max_length=50, null=True, verbose_name='头像图片')
    dateTime = models.DateTimeField(verbose_name='时间')

    organization = models.ManyToManyField(Organization, verbose_name='组织')
    roles = models.ManyToManyField(Role, verbose_name='角色')

    def __str__(self):
        return self.username


# 园子
class Garden(models.Model):
    name = models.CharField(max_length=50, verbose_name='名称')
    introduce = models.CharField(max_length=140, verbose_name='介绍')
    cover_url = models.CharField(max_length=500, null=True, verbose_name='介绍')
    description = models.TextField(verbose_name='描述')
    dateTime = models.DateTimeField(verbose_name='时间')
    author = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='作者')

    def __str__(self):
        return self.name

# Tag 标签
class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='标签名称')
    slug = models.SlugField(max_length=50, default='', blank=False) # slug 指有效 URL 的一部分，能使 URL 更加清晰易懂
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('blogs:tag', kwargs={'slug':self.slug})

# 博客
class Blogs(models.Model):
    title = models.CharField(max_length=20, verbose_name='标题')
    subtitle = models.CharField(max_length=50, verbose_name='副标题')
    introduction = models.CharField(max_length=400, verbose_name='简介')
    description = models.TextField(verbose_name='描述')
    imgurl = models.CharField(max_length=500, verbose_name='图片')
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    dateTime = models.DateTimeField(verbose_name='日期')
    links = models.IntegerField(verbose_name='点赞数')
    reads = models.IntegerField(verbose_name='阅读数')
    author = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='作者')
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, verbose_name='园子')

    def __str__(self):
        return self.title

# 评论
class Commons(models.Model):
    parentId = models.IntegerField(verbose_name='引用ID')
    title = models.CharField(max_length=50, null=True, verbose_name='标题')
    contnet = models.CharField(max_length=500, verbose_name='内容')
    references = models.IntegerField(verbose_name='引用数')
    replys = models.IntegerField(verbose_name='回复数/评论数')
    dateTime = models.DateTimeField(verbose_name='日期')
    links = models.IntegerField(verbose_name='点赞数')
    author = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='作者')
    blogs = models.ForeignKey(Blogs, on_delete=models.CASCADE, verbose_name='博客')

    def __str__(self):
        return self.title

# 主题
class Theme(models.Model):
    themeName = models.CharField(max_length=50, verbose_name='主题名')
    icon = models.CharField(max_length=50, verbose_name='主题图片')
    introduce = models.CharField(max_length=140, verbose_name='介绍')
    description = models.TextField(verbose_name='规则描述')
    members = models.IntegerField(verbose_name='成员数')
    author = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='作者')
    datetime = models.DateTimeField(verbose_name='时间')

    def __str__(self):
        return self.themeName

# 主题文章
class ThemeBlogs(models.Model):
    title = models.CharField(max_length=20, verbose_name='标题')
    subtitle = models.CharField(max_length=50, verbose_name='副标题')
    introduction = models.CharField(max_length=140, verbose_name='简介')
    description = models.TextField(verbose_name='描述')
    imgurl = models.CharField(max_length=500, verbose_name='图片')
    dateTime = models.DateTimeField(verbose_name='日期')
    links = models.IntegerField(verbose_name='点赞数')
    reads = models.IntegerField(verbose_name='阅读数')
    author = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='作者')
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, verbose_name='园子')

    def __str__(self):
        return self.title

# 讨论主题问题
class DiscussTopic(models.Model):
    title = models.CharField(max_length=50, verbose_name='讨论标题')
    links = models.IntegerField(verbose_name='点赞数')
    dateTime = models.DateTimeField(verbose_name='时间')
    author = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='作者')
    themeBlog = models.ForeignKey(ThemeBlogs, on_delete=models.CASCADE, null=True, verbose_name='主题')

    def __str__(self):
        return self.title

# 主题和讨论关联表 （1：n ）
class Discuss(models.Model):
    parentId = models.IntegerField(verbose_name='引用ID')
    content = models.CharField(max_length=500, null=True, verbose_name='内容')
    references = models.IntegerField(verbose_name='引用数')
    links = models.IntegerField(verbose_name='点赞数')
    dateTime = models.DateTimeField(verbose_name='时间')
    author = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='作者')
    topic = models.ForeignKey(DiscussTopic, on_delete=models.CASCADE, verbose_name='讨论主题')

    def __str__(self):
        return self.content
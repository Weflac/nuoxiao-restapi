from django.db import models

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES,default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES,default='friendly', max_length=100)
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


# 用户
class Users(models.Model):
    username = models.CharField(max_length=20, unique=True)  # 用户名
    password = models.CharField(max_length=20)  # 密码
    phone = models.CharField(max_length=11, null=True)  # 手机号码
    email = models.EmailField(max_length=50, null=True)  # 邮箱
    nickname = models.CharField(max_length=50, null=True)  # 昵称
    subject = models.CharField(max_length=50, null=True)  # 主题
    introduce = models.CharField(max_length=140, null=True)  # 用户名
    icon = models.CharField(max_length=50, null=True)  # icon
    dateTime = models.DateTimeField()  # 时间

    def __str__(self):
        return self.username

# 园子
class Garden(models.Model):
    name = models.CharField(max_length=50)  # 名称
    introduce = models.CharField(max_length=140)  # 介绍
    cover_url = models.CharField(max_length=500, null=True)  # 图片
    description = models.TextField()  # 描述
    dateTime = models.DateTimeField()  # 时间
    author = models.ForeignKey(Users, on_delete=models.CASCADE)  # 作者

    def __str__(self):
        return self.name

# 博客
class Blogs(models.Model):
    title = models.CharField(max_length=20)  # 标题
    subtitle = models.CharField(max_length=50)  # 副标题
    introduction = models.CharField(max_length=400)  # 简介
    description = models.TextField()  # 描述
    imgurl = models.CharField(max_length=500)   # 图片
    dateTime = models.DateTimeField()  # 日期
    links = models.IntegerField()   # 点赞数
    reads = models.IntegerField()    # 阅读数
    author = models.ForeignKey(Users, on_delete=models.CASCADE)  # 作者
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE)  # 园子主键

    def __str__(self):
        return self.title

# 评论
class Commons(models.Model):
    parentId = models.IntegerField() # 引用ID
    title = models.CharField(max_length=50, null=True)  # 标题
    contnet = models.CharField(max_length=500)  # 内容
    references = models.IntegerField()   # 引用数
    replys = models.IntegerField()  # 回复数/评论数
    dateTime = models.DateTimeField()  # 日期
    links = models.IntegerField()   # 点赞数
    author = models.ForeignKey(Users, on_delete=models.CASCADE)  # 作者
    blogs = models.ForeignKey(Blogs, on_delete=models.CASCADE)  # 博客

    def __str__(self):
        return self.title

# 主题
class Theme(models.Model):
    themeName = models.CharField(max_length=50)  # 主题名
    icon = models.CharField(max_length=50)  # 主题名
    introduce = models.CharField(max_length=140)  # 介绍
    description = models.TextField()  # 规则描述
    members = models.IntegerField()  # 成员数
    author = models.ForeignKey(Users, on_delete=models.CASCADE)  # 作者
    datetime = models.DateTimeField()  # 时间

    def __str__(self):
        return self.themeName

# 主题文章
class ThemeBlogs(models.Model):
    title = models.CharField(max_length=20)  # 标题
    subtitle = models.CharField(max_length=50)  # 副标题
    introduction = models.CharField(max_length=140)  # 简介
    description = models.TextField()  # 描述
    imgurl = models.CharField(max_length=500)  # 图片
    dateTime = models.DateTimeField()  # 日期
    links = models.IntegerField()  # 点赞数
    reads = models.IntegerField()  # 阅读数
    author = models.ForeignKey(Users, on_delete=models.CASCADE)  # 作者
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)  # 园子主键

    def __str__(self):
        return self.title

# 讨论主题问题
class DiscussTopic(models.Model):
    title = models.CharField(max_length=50)  # 讨论标题
    links = models.IntegerField()   # 点赞数
    dateTime = models.DateTimeField()  # 时间
    author = models.ForeignKey(Users, on_delete=models.CASCADE)  # 作者
    themeBlog = models.ForeignKey(ThemeBlogs, on_delete=models.CASCADE, null=True)  # 主题主键ID

    def __str__(self):
        return self.title

# 主题和讨论关联表 （1：n ）
class Discuss(models.Model):
    parentId = models.IntegerField()  # 引用ID
    content = models.CharField(max_length=500, null=True)  # 内容
    references = models.IntegerField()  # 引用数
    links = models.IntegerField()   # 点赞数
    dateTime = models.DateTimeField()  # 时间
    author = models.ForeignKey(Users, on_delete=models.CASCADE)  # 作者
    topic = models.ForeignKey(DiscussTopic, on_delete=models.CASCADE)  # 讨论主题

    def __str__(self):
        return self.content
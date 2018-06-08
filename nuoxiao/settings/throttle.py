# coding:utf-8

from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
import time

'''
    # Throttle:频率控制
'''

REQUEST_RECORD = {}  # 访问记录，可使用nosql数据库

class DemoThrottle(SimpleRateThrottle):
    """5秒内最多访问三次"""
    scope = "WD"  #settings配置文件中的key,用于获取配置的频率

    def get_cache_key(self, request, view):
        return self.get_ident(request)

# 自定义频率控制, 60s内最多能访问5次
class VisitThrottle(BaseThrottle):
    '''60s内最多能访问5次'''

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        # 获取用户ip (get_ident)
        remote_addr = self.get_ident(request)
        ctime = time.time()

        if remote_addr not in REQUEST_RECORD:
            REQUEST_RECORD[remote_addr] = [ctime, ]  # 保持请求的时间，形式{ip:[时间,]}
            return True  # True表示可以访问

        # 获取当前ip的历史访问记录
        history = REQUEST_RECORD.get(remote_addr)

        self.history = history


        while history and history[-1] < ctime - 60:
            # while循环确保每列表中是最新的60秒内的请求

            history.pop()
        # 访问记录小于5次，将本次请求插入到最前面，作为最新的请求
        if len(history) < 5:
            history.insert(0, ctime)
            return True

    def wait(self):
        '''返回等待时间'''
        ctime = time.time()
        return 60 - (ctime - self.history[-1])

# 基于SimpleRateThrottle，对用户的频率控制
class UserRateThrottle(SimpleRateThrottle):
    """
    Limits the rate of API calls that may be made by a given user.

    The user id will be used as a unique cache key if the user is
    authenticated.  For anonymous requests, the IP address of the request will
    be used.
    """
    scope = 'user'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

# 匿名用户频率控制
class AnonRateThrottle(SimpleRateThrottle):
    """
    Limits the rate of API calls that may be made by a anonymous users.

    The IP address of the request will be used as the unique cache key.
    """
    scope = 'anon'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None  # Only throttle unauthenticated requests.

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request)
        }


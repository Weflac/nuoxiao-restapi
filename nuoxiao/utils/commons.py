# coding:utf-8

from nuoxiao.utils.response_code import RET

import hashlib
import time
import base64
import functools


'''
    Commons: 公用帮助包
'''

# MD5加密
def md5(obj):
    ctime = str(time.time())
    m = hashlib.md5(bytes(obj,encoding="utf-8"))
    m.update(bytes(ctime,encoding="utf-8"))
    return m.hexdigest()

# MD5解密

# 装饰器封装是否登录
def required_login(fun):
    # 保证被装饰的函数对象的__name__不变
    @functools.wraps(fun)
    def wrapper(request_handler_obj, *args, **kwargs):
        # 调用get_current_user方法判断用户是否登录
        if not request_handler_obj.get_current_user():
        # session = Session(request_handler_obj)
        # if not session.data:
            request_handler_obj.write(dict(errcode=RET.SESSIONERR, errmsg="用户未登录"))
        else:
            fun(request_handler_obj, *args, **kwargs)
    return wrapper

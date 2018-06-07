# coding:utf-8
import hashlib
import time


'''
    MD5加密
'''
def md5(obj):
    ctime = str(time.time())
    m = hashlib.md5(bytes(obj,encoding="utf-8"))
    m.update(bytes(ctime,encoding="utf-8"))
    return m.hexdigest()

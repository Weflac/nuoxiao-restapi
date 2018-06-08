# coding:utf-8

from django.conf import settings
from django.core.mail import send_mail

import random

'''
    # 邮箱验证码
'''

class EmailVerifyCode():
    verifycode_range = "1234567890"

    def generation_verifycode(self, length=6):
        return "".join(random.sample(self.verifycode_range, length))

    def send_verifycode(self, to):
        code = self.generation_verifycode()
        try:
            send_mail("重置密码", "Hi,您的验证码为:\n\t{}".format(code),
                      settings.SEND_EMAIL,
                      [to],
                      fail_silently=False)
            return code
        except Exception as exc:
            raise Exception("Email send fail!")
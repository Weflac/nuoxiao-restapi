from rest_framework.views import exception_handler

'''
    自定义异常
'''

def custom_exception_handler(exc, content):

    response = exception_handler(exc, content)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response
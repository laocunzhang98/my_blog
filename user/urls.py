from django.urls import path
from user.views import *

app_name = 'user'

urlpatterns = [
    path('register', register.as_view(), name='register'),
    path('login', user_login, name='login'),# 密码登陆
    path('logout', user_logout, name='logout'), # 注销
    path('zhuce', user_zhuce, name='zhuce'), # 测试注册
    path('codelogin', code_login, name='codelogin'), # 验证码登陆
    path('sendcode', send_code, name='send_code'),
    path('forget_pwd', forget_password, name='forget_pwd'), # 更改密码
    path('valide_code', valide_code, name='valide_code'), # 验证验证码
    path('update_pwd', update_pwd, name='update_pwd'), # 更新密码
    path('center', user_center, name='center'),  # 本地存储
    path('center1', user_center1, name='center1'),  # 阿里云存储
]

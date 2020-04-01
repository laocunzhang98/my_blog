import time
import uuid

from celery import Celery
from django.conf import settings
from django.core.mail import send_mail


import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()
from user.models import UserProfile


app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/4')


@app.task
def send_email(email, username, ran_code):
    subject = '个人博客找回密码'
    # user = UserProfile.objects.filter(email=email).first()
    # ran_code = uuid.uuid4()
    # print(ran_code)
    # print(type(ran_code))
    # ran_code = str(ran_code)
    # print(type(ran_code))
    # ran_code = ran_code.replace('-', '')
    # request.session[ran_code] = user.id
    sender = settings.EMAIL_FROM
    receiver = [email]
    message = '''
     可爱的%s:
            您好！此链接用户找回密码，请点击链接: <a href='http://127.0.0.1:8000/user/update_pwd?c=%s'>更新密码</a>，
            如果链接不能点击，请复制：
            http://127.0.0.1:8000/user/update_pwd?c=%s

           个人博客团队
    ''' % (username, ran_code, ran_code)
    send_mail(subject, "", sender, receiver, html_message=message)
    time.sleep(10)

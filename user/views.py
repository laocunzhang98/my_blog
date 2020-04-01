import os
import uuid

import requests
from captcha.models import CaptchaStore
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
# from django.contrib.auth.views import logout
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django import views

# Create your views here.
from django.urls import reverse

from article.models import Article
from blog.settings import MEDIA_URL
from user.forms import UserRegisterForm, RegisterForm, LoginForm, CaptchaTestForm
from user.models import UserProfile
from user.utils import util_sendmsg, upload_image
from celery_tasks.tasks import send_email

def index(request):
    farticles = Article.objects.all().order_by('-click_num')
    darticles = Article.objects.all().order_by('-date')[:8]
    return render(request, 'index.html', context={'figure_articles': farticles[:3], 'darticles': darticles})

# 注册
class register(views.View):

    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        # rform = RegisterForm(request.POST)  # 使用form获取数据
        # if rform.is_valid():  # 进行数据的校验
            # 从干净的数据中取值
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        if not UserProfile.objects.filter(Q(username=username) | Q(mobile=mobile)).exists():
            # 注册到数据库中
            password = make_password(password)  # 密码加密
            user = UserProfile.objects.create(username=username, password=password, email=email, mobile=mobile)
            if user:
                return HttpResponse('注册成功')
        else:
            return render(request, 'user/register.html', context={'msg': '用户名或者手机号码已经存在！'})
        # return render(request, 'user/register.html', context={'msg': '注册失败，重新填写！'})


# 用户登录
def user_login(request):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    else:
        lform = LoginForm(request.POST)
        if lform.is_valid():
            username = lform.cleaned_data.get('username')
            password = lform.cleaned_data.get('password')
            # 进行数据库的查询
            # user = UserProfile.objects.filter(username=username).first()
            # flag = check_password(password, user.password)
            # if flag:
            #     # 保存session信息
            #     request.session['username'] = username

            # 方式二前提是继承了AbstractUser
            user = authenticate(username=username, password=password)
            # lform.errors = "用户名或者密码错误"
            error = lform.errors
            if user:
                login(request, user)  # 将用户对象保存在底层的request中  （session）
                next_url = request.GET.get('next', reverse('index'))
                return redirect(next_url)
            else:
                error = "用户名或者密码错误"
        return render(request, 'user/login.html', context={'errors': error})


# 用户注销
def user_logout(request):
    # request.session.clear()  # 删除字典
    # request.session.flush()  # 删除django_session + cookie +字典
    logout(request)

    return redirect(reverse('index'))


@login_required
def user_center(request):
    user = request.user
    if request.method == 'GET':

        return render(request, 'user/center.html', context={'user': user})
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        icon = request.FILES.get('icon')
        user = UserProfile.objects.filter(username=username).first()

        # 更新用户
        user.username = username
        user.email = email
        user.mobile = mobile
        if icon != None:
            save_path = upload_image(icon)
            user.yunicon = save_path
        user.save()

        return render(request, 'user/center.html', context={'user': user})

# 云存储
@login_required
def user_center1(request):
    user = request.user
    if request.method == 'GET':

        return render(request, 'user/center.html', context={'user': user})
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        icon = request.FILES.get("icon")
        user = UserProfile.objects.filter(username=username).first()

        # 更新用户
        user.username = username
        user.email = email
        user.mobile = mobile

        if icon != '':
            yunicon = "https://wangweiblog.oss-cn-beijing.aliyuncs.com/" + username + icon.name
            key = username + icon.name
            upload_image(key, icon)

            user.yunicon = yunicon
        user.save()

        return render(request, 'user/center.html', context={'user': user, "yunicon":user.yunicon})



# 手机验证码登录
def code_login(request):
    if request.method == 'GET':
        return render(request, 'user/codelogin.html')
    else:
        mobile = request.POST.get('mobile')
        code = request.POST.get('code')

        # 根据mobile去session中取值
        check_code = request.session.get(mobile)
        if code == check_code:
            user = UserProfile.objects.filter(mobile=mobile).first()
            # user = authenticate(username=user.username, password=user.password)
            print(user)
            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return HttpResponse('验证失败！')
        else:
            return render(request, 'user/codelogin.html', context={'msg': '验证码有误！'})


def update_pwd(request):
    if request.method == 'GET':
        c = request.GET.get('c')
        return render(request, 'user/update_pwd.html', context={'c': c})
    else:
        code = request.POST.get('code')
        uid = request.session.get(code)
        user = UserProfile.objects.get(pk=uid)
        # 获取密码
        pwd = request.POST.get('password')
        repwd = request.POST.get('repassword')
        if pwd == repwd and user:
            pwd = make_password(pwd)
            user.password = pwd
            user.save()
            return render(request, 'user/update_pwd.html', context={'msg':'用户密码更新成功！'})
        else:
            return render(request, 'user/update_pwd.html', context={'msg': '更新失败！'})

# 发送验证码路由  ajax发过来的请求
def send_code(request):
    mobile = request.GET.get('mobile')
    data = {}
    if UserProfile.objects.filter(mobile=mobile).exists():
        # 发送验证码  第三方
        json_result = util_sendmsg(mobile)
        # 取值：
        status = json_result.get('code')
        if status == 200:
            check_code = json_result.get('obj')
            # 使用session保存
            request.session[mobile] = check_code

            data['status'] = 200
            data['msg'] = '验证码发送成功'
        else:
            data['status'] = 500
            data['msg'] = '验证码发送失败'
    else:
        data['status'] = 501
        data['msg'] = '用户不存在'

    return JsonResponse(data)


# 忘记密码
def forget_password(request):
    if request.method == 'GET':
        form = CaptchaTestForm()
        return render(request, 'user/forget_pwd.html', context={'form': form})
    else:
        # 获取提交的邮箱，发送邮件，通过发送的邮箱链接设置新的密码
        email = request.POST.get('email')
        if UserProfile.objects.filter(Q(email=email)).exists():
            user = UserProfile.objects.filter(email=email).first()
            ran_code = uuid.uuid4()
            print(ran_code)
            print(type(ran_code))
            ran_code = str(ran_code)
            print(type(ran_code))
            print(user.username)
            ran_code = ran_code.replace('-', '')
            print(ran_code)
            request.session[ran_code] = user.id
            form = CaptchaTestForm()
            # 给此邮箱地址发送邮件
            send_email.delay(email, user.username, ran_code)

            msg = '邮件发送成功,快去修改密码吧'
            return render(request, "user/forget_pwd.html", context={"msg": msg, 'form': form})
        else:
            msg = "该邮箱没有注册"
            form = CaptchaTestForm()
            return render(request, "user/forget_pwd.html", context={"msg": msg, 'form': form})

# 定义一个路由验证验证码
def valide_code(request):
    if request.is_ajax():
        key = request.GET.get('key')
        code = request.GET.get('code')

        captche = CaptchaStore.objects.filter(hashkey=key).first()
        if captche.response == code.lower():
            # 正确
            data = {'status': 1}
        else:
            # 错误的
            data = {'status': 0}
        print(data["status"])
        return JsonResponse(data)


def page_not_found(request, exception):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})  # first/404.html html页面
    response.status_code = 404
    return response


# 全局500
def page_error(exception):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
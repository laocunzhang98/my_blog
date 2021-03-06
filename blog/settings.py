"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j=9*fmd10b&5j*7nm4#*d6dvpqx!4=-xwz!i+-gao=j!8_q^6x'

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'article',
    'captcha',
    'xadmin', # xadmin
    'crispy_forms',
    'ckeditor', # 富文本编辑器
    'mdeditor',
    'ckeditor_uploader', # 进行文件上传
    'qiniustorage',    # 七牛云存储]
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'
AUTH_USER_MODEL = 'user.UserProfile'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_blog',
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': '127.0.0.1',
        'PORT': 3306

    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CKEDITOR_UPLOAD_PATH = "uploads/"

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/4' # BACKEND配置，这里使用redis


CELERY_TASK_SERIALIZER = 'pickle'

CELERY_RESULT_SERIALIZER = 'pickle'

CELERY_ACCEPT_CONTENT = ['pickle', 'json']
# 发送邮件配置
# Host for sending email.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
# Port for sending email.
EMAIL_PORT = 465
EMAIL_HOST_USER = '782984630@qq.com'
EMAIL_HOST_PASSWORD = 'rnbgvxpsynsqbchb'
# EMAIL_USE_TLS = True #必须为True
EMAIL_USE_SSL = True
EMAIL_FROM = '村长个人博客<782984630@qq.com>'

# 中间件路由
LOGIN_URL = '/user/login'
# QINIU_ACCESS_KEY='jc21N9zuCHLGz9bwQAN9rIFkb-ad8zZNMs6uLSMT'
# #七牛给开发者分配的 AccessKey
#
# QINIU_SECRET_KEY='a-9A_t7kEQfqNhB-0Govnp1AgsQ7OGhDtM1fIiHA'
# #七牛给开发者分配的 Secret
#
# QINIU_BUCKET_NAME='canteenblog'
# #用来存放文件的七牛空间(bucket)的名字
#
# QINIU_BUCKET_DOMAIN='q83ghz9j3.bkt.clouddn.com'
# #七牛空间(bucket)的域名
#
# QINIU_SECURE_URL = False      #使用http
# PREFIX_URL = 'http://'
#
# MEDIA_URL = PREFIX_URL + QINIU_BUCKET_DOMAIN + '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, '/media/')
#
# DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuMediaStorage'
#
# STATIC_URL = QINIU_BUCKET_DOMAIN + '/static/'
# # STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATIC_ROOT = os.path.join(BASE_DIR, '/static/')
# STATICFILES_STORAGE = 'qiniustorage.backends.QiniuStaticStorage'
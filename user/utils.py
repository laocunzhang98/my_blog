# 向网易云信发送请求
import hashlib
import json
import os


from time import time

import requests
import oss2

from blog.settings import MEDIA_URL, MEDIA_ROOT


def util_sendmsg(mobile):
    url = 'https://api.netease.im/sms/sendcode.action'
    data = {'mobile': mobile}
    # 4部分组成 headers： AppKey  Nonce  CurTime  CheckSum
    AppKey = '3e8864a7099b5b723675320349f2595c'
    Nonce = '843hjfd87fdfshdjfhs5433'
    CurTime = str(time())
    AppSecret = '971bb55f2095'
    content = AppSecret + Nonce + CurTime
    CheckSum = hashlib.sha1(content.encode('utf-8')).hexdigest()

    headers = {'AppKey': AppKey, 'Nonce': Nonce, 'CurTime': CurTime, 'CheckSum': CheckSum}

    response = requests.post(url, data, headers=headers)
    # json
    str_result = response.text  # 获取响应体

    json_result = json.loads(str_result)  # 转成json
    print(json_result)
    return json_result

# 创建阿里云存储空间
def create_bucket():
    '''创建阿里云存储空间'''
    auth = oss2.Auth('LTAI4FvFFwEspZ1LTcSrDZnD', 'tXReoTqRCZAsSwWVR6iOkEmdyWLWat')
    bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'wangweiblog')
    bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)
from oss2.models import PutObjectResult
# 上传图片到阿里云
def upload_image(key, storeobj):
    '''上传图片到云'''
    auth = oss2.Auth('LTAI4FvFFwEspZ1LTcSrDZnD', 'tXReoTqRCZAsSwWVR6iOkEmdyWLWat')
    bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'wangweiblog')
    # local_file = os.path.join(MEDIA_ROOT, image_path)



    bucket.put_object(key, storeobj)


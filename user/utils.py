# 向网易云信发送请求
import hashlib
import json
import os
from time import time
import requests
import oss2
from qiniu import put_data, Auth

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
# def create_bucket():
#     '''创建阿里云存储空间'''
#     auth = oss2.Auth('LTAI4FvFFwEspZ1LTcSrDZnD', 'tXReoTqRCZAsSwWVR6iOkEmdyWLWat')
#     bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'wangweiblog')
#     bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)
# from oss2.models import PutObjectResult
# # 上传图片到阿里云
# def upload_image(key, storeobj):
#     '''上传图片到云'''
#     auth = oss2.Auth('LTAI4FvFFwEspZ1LTcSrDZnD', 'tXReoTqRCZAsSwWVR6iOkEmdyWLWat')
#     bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', 'wangweiblog')
#     # local_file = os.path.join(MEDIA_ROOT, image_path)
#     bucket.put_object(key, storeobj)

# 上传图片到七牛云
def upload_image(storeobj):
    access_key = 'jc21N9zuCHLGz9bwQAN9rIFkb-ad8zZNMs6uLSMT'
    secret_key = 'a-9A_t7kEQfqNhB-0Govnp1AgsQ7OGhDtM1fIiHA'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'canteenblog'

    # 上传后保存的文件名
    key = storeobj.name

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    # localfile = os.path.join(MEDIA_ROOT, imagepath)  # 本地图片
    ret, info = put_data(token, key, storeobj.read())

    filename = ret.get('key')
    save_path = 'http://q83ghz9j3.bkt.clouddn.com/'+filename
    return save_path


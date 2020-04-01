from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class UserProfile(AbstractUser):
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    #icon = models.ImageField(upload_to='uploads/%Y/%m/%d')
    yunicon = models.CharField(max_length=200, blank=True)
    class Meta:
        db_table = 'userprofile'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
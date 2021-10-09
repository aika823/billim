from django.db import models
import datetime
import os
from django.utils.deconstruct import deconstructible

@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        now = datetime.datetime.now()
        date_time = now.strftime("%y%m%d_%H%M%S")
        filename = 'img_product_{}.{}'.format(str(date_time), str(ext))
        return os.path.join(self.path, filename)

class User(models.Model):
    username = models.CharField(max_length=32, verbose_name='사용자명')
    email = models.EmailField(max_length=128, verbose_name='사용자이메일')
    password = models.CharField(max_length=256, verbose_name='비밀번호', default=None, null=True)
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    social_login = models.CharField(max_length=32, verbose_name='소셜로그인', default='', null=True)
    social_id = models.CharField(max_length=256, verbose_name='소셜 아이디', default=None, null=True)
    naver_id = models.CharField(max_length=128, verbose_name='네이버 유저 키', default=None, null=True) 
    image = models.ImageField(upload_to=PathAndRename("user/"),blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name = '유저'
        verbose_name_plural = '유저입니다'
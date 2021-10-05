from django.db import models

class User(models.Model):
    username = models.CharField(max_length=32, verbose_name='사용자명')
    email = models.EmailField(max_length=128, verbose_name='사용자이메일')
    password = models.CharField(max_length=64, verbose_name='비밀번호', default=None, null=True)
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')
    social_login = models.CharField(max_length=32, verbose_name='소셜로그인', default='', null=True)
    naver_id = models.CharField(max_length=128, verbose_name='네이버 유저 키', default=None, null=True) 
    profile_img = models.ImageField(upload_to='product/',blank=True, null=True)


    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name = '유저'
        verbose_name_plural = '유저입니다'

class DropBox(models.Model):
    title = models.CharField(max_length=30)
    document = models.FileField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = 'Drop Boxes'
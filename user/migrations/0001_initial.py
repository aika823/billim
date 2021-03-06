# Generated by Django 3.2.7 on 2021-10-06 06:24

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='사용자명')),
                ('email', models.EmailField(max_length=128, verbose_name='사용자이메일')),
                ('password', models.CharField(default=None, max_length=64, null=True, verbose_name='비밀번호')),
                ('registered_dttm', models.DateTimeField(auto_now_add=True, verbose_name='등록시간')),
                ('social_login', models.CharField(default='', max_length=32, null=True, verbose_name='소셜로그인')),
                ('naver_id', models.CharField(default=None, max_length=128, null=True, verbose_name='네이버 유저 키')),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to=user.models.PathAndRename('user/'))),
            ],
            options={
                'verbose_name': '유저',
                'verbose_name_plural': '유저입니다',
                'db_table': 'user',
            },
        ),
    ]

from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'
    verbose_name = '사용자'

INSTALLED_APPS = [
    'main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
import os
from pathlib import Path
import json

# BASE, ROOT, URL
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = os.path.dirname(BASE_DIR)
PROJECT_ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# BILLIM_URL = 'http://localhost:8000'
BILLIM_URL = 'http://billim.co.kr'

IMAGE_URL = 'http://static.billim.co.kr'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)1iesg7saya73$5@3+zj_eg4(hojew#^g$u_q72h*!0ywa6ba^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED HOSTS
ALLOWED_HOSTS = [
    'billim.ap-northeast-2.elasticbeanstalk.com',
    'billim.co.kr',
    '127.0.0.1',
    'localhost',
]

# Application definition    
BATON = {
    'SITE_HEADER': '빌림 - 백오피스',
    'SITE_TITLE': '빌림 - 백오피스입니다.',
    'INDEX_TITLE': '빌림 관리자페이지',
    'SUPPORT_HREF': 'https://billim.co.kr',
    'COPYRIGHT': 'copyright © 2021 Billim',
    'POWERED_BY': '<a href="https://billim.co.kr">Billim</a>',
    'MENU_TITLE': '빌림 메뉴',
    'MENU': (
        { 'type': 'title', 'label': 'main' },
        {
            'type': 'app',
            'name': 'user',
            'label': '사용자',
            'icon': 'fa fa-lock',
            'models': (
                {
                    'name': 'user',
                    'label': '사용자'
                },
            )
        },
        {
            'type': 'free', 'label': '주문', 'default_open': True, 'children': [
                { 'type': 'free', 'label': '주문', 'url': '/admin/order/order/' },
                { 'type': 'free', 'label': '주문 날짜 뷰', 'url': '/admin/order/order/date_view/' },
            ]
        },
        {
            'type': 'app',
            'name': 'product',
            'label': '상품',
            'models': (
                {
                    'name': 'product',
                    'label': '상품'
                },
            )
        },
        { 'type': 'free', 'label': '매뉴얼', 'url': '/admin/manual' },
    ),
}

INSTALLED_APPS = [
    # 'baton',

    # Django autocomplete light
    'dal',
    'dal_select2',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',

    'allauth', 
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.google',

    'rest_framework',
    'user.apps.UserConfig',
    'order.apps.OrderConfig',
    'product.apps.ProductConfig',
    'baton.autodiscover',

    # 'user',
    'board',
    'tag',
    'storages',
    'seller',
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

ROOT_URLCONF = 'billim.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'billim.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'billim',
        'USER': 'admin',
        'PASSWORD': 'billim1!',
        'HOST': 'billim.czal2yo4w2nq.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
         'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SECRET
SECRET_DIR = os.path.join(PROJECT_ROOT, 'secret')
SECRETS = json.load(open(os.path.join(SECRET_DIR, 'secret.json'), 'rb'))

# AWS SETTINGS
AWS_ACCESS_KEY_ID = SECRETS['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = SECRETS['AWS_SECRET_ACCESS_KEY']
AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'static.billim.co.kr'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME,AWS_REGION)
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# MEDIA
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "https://%s/" % AWS_STORAGE_BUCKET_NAME

# AUTHENTICATION
ACCOUNT_ADAPTER = 'user.adapter.MyAccountAdapter'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend', 
) 
LOGIN_REDIRECT_URL = '/'
SITE_ID = 2
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]

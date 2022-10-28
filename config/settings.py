"""
import library
"""
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv
import socket
from datetime import timedelta
load_dotenv(find_dotenv())
import sys
"""
Path and keys config
"""
SECRET_KEY = os.environ['SECRET_KEY']
BASE_DIR = Path(__file__).resolve().parent.parent


"""
Development settings
"""
socket.getaddrinfo('localhost', 8080)
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Application definition
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth', 
    'allauth.account',
    'dj_rest_auth.registration',
    'drf_yasg',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'drf_multiple_model',
    'corsheaders',
    'phonenumber_field',
]

LOCAL_APPS = [
    'apiauth',
    'events',
    'marketplace',
    'carpool',
    
]

PHONENUMBER_DEFAULT_REGION ='AR'

# Application definition
INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

REST_SESSION_LOGIN = False 

SITE_ID = 1
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
        
    ],
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

}


"""
JWT configs
"""
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'upf-authtoken'
JWT_AUTH_REFRESH_COOKIE = 'upf-refresh-token'

SIMPLE_JWT = {
'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
'REFRESH_TOKEN_LIFETIME' : timedelta(days=2),

}


AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

"""
Account confirmations
"""
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_CONFIRM_EMAIL_ON_GET = True
LOGIN_URL = 'https://main.dtlgaufp375aa.amplifyapp.com/'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'config.urls'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = [
    "*",
    "Bearer"
]

CORS_EXPOSE_HEADERS = [
    "Bearer",
    "*"
]



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'apiauth/templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'


"""
Custom serializers from third party libraryes
"""
REST_AUTH_REGISTER_SERIALIZERS = { 
    'REGISTER_SERIALIZER': 'apiauth.serializers.RegisterSerializer', 
    }

REST_AUTH_SERIALIZERS = {
    # Changed
    'USER_DETAILS_SERIALIZER': 'apiauth.serializers.CustomUserDetailsSerializer',
}
"""
Database config
"""

DATABASES = {
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': os.environ['DATABASE_NAME'] , 
        'USER': os.environ['DATABASE_USER'],  
        'PASSWORD': os.environ['DATABASE_PASSWORD'],  
        'HOST': os.environ['DATABASE_HOST'],  
        'PORT': '3306',
        #'OPTIONS': {  
        #    'init_command': "SET sql_mode='STRICT_TRANS_TABLES"  
        #} 
    }  
}

if 'test' in sys.argv or 'test_coverage' in sys.argv: #Covers regular testing and django-coverage
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'


"""
Internationalization (LANG, TIMEZONE)
"""

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


"""
Email Configurations
"""
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'fatmailsender2@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

"""
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/")
]
"""


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ['S3_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['S3_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['S3_STORAGE_BUCKET_NAME']
AWS_QUERYSTRING_AUTH = False
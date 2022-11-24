import os
from os.path import join, dirname
from dotenv import load_dotenv
from pathlib import Path



#Сбор переменных окружения из .env файла
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from .databases_settings import *
from .redis_settings import REDIS_LINK




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.0.18', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'CRUD_app',
]

CACHES = {
    "default": {
        "BACKEND": 'django.core.cache.backends.redis.RedisCache',
        "LOCATION": REDIS_LINK,
    }
}

MIDDLEWARE = [
    'api_app.middleware.auth_middleware.CookiesCheckMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api_app.urls'

WSGI_APPLICATION = 'api_app.wsgi.application'
ASGI_APPLICATION = 'api_app.asgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCESS_COOKIE =  os.environ.get("ACCESS_COOKIE")

REFRESH_COOKIE = os.environ.get("REFRESH_COOKIE")
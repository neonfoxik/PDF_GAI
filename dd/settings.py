import os
from os import getenv

import dotenv

from telebot.types import BotCommand

from pathlib import Path

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
SECRET_KEY = '(tu7fvnsgmyk*9)dnre_qp4&6@sgu#$18u=yp3m+2c=tvkj9+w'
# SECURITY WARNING: keep the secret key used in production secret!

ASSISTANT_PROMPT="""Ты — эксперт в области юриспруденции. Твоя задача — отвечать на вопросы, касающиеся юрисдикции, законодательства и правовых норм. Пожалуйста, предоставляй точные и обоснованные ответы на все вопросы, связанные с юрисдикцией.

Если вопрос не относится к юрисдикции или праву, просто отвечай: "Извините, я могу ответить только на вопросы по юрисдикции."

Приведите примеры вопросов, на которые ты можешь ответить:
1. "Какова юрисдикция для судебного разбирательства в данном случае?"
2. "Какие законы регулируют эту юрисдикцию?"
3. "Как определить, какая юрисдикция применима в данной ситуации?"

Помни, что ты не должен отвечать на вопросы, касающиеся других тем, таких как наука, искусство, спорт и пр. Не ленись где нужно уместно используй смайлики
"""
PROVIDER_NAME = "vsegpt"
PROVIDER = "https://api.vsegpt.ru/v1"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOCAL = getenv('LOCAL')

ALLOWED_HOSTS = ["*"]

BOT_TOKEN = getenv('BOT_TOKEN')
OWNER_ID = getenv('OWNER_ID')
HOOK = getenv('HOOK')


BOT_COMMANDS = [
    BotCommand("start", "Меню"),
    BotCommand("documents_menu", "Действия с документами")
]
INSTALLED_APPS = [
    'bot',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'dd.urls'

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

WSGI_APPLICATION = 'dd.wsgi.application'

if LOCAL == 'True':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("NAME_DB"),
            "USER": os.getenv("NAME_DB"),
            "PASSWORD": os.getenv("PASS_DB"),
            "HOST": "127.0.0.1",
        }
    }

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

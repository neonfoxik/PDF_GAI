import os

import dotenv
from os import getenv

from pathlib import Path
from telebot.types import BotCommand
import pymysql

pymysql.install_as_MySQLdb()

dotenv.load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'a2(tfzdu=a-%$+8w+%w3^7j!@eibw8e0-ydahz6d9)lt=ervew'


STATIC_URL = '/static/'  # Добавлено для настройки статических файлов


DEBUG = True  # Изменено на True для отладки

ALLOWED_HOSTS = ['*']

# Определяем корневой URL-конфигуратор
ROOT_URLCONF = 'bot.urls'  # Указываем путь к главному urls.py файлу

BOT_TOKEN = getenv("BOT_TOKEN")
HOOK = getenv("HOOK")
OWNER_ID = getenv("OWNER_ID")

REQUESTS_AMOUNT_BASE = 10

MENU_LIST = [
    ["Моя подписка", "plan"],
    ["Выбор модели ИИ 🤖", "choice"],
    ["Сгененировать изображение 🖼️", "image_gen"],
    ["Оплатить 💸", "payment"],
    ["Реферальная ссылка 🔗", "referal"],
]

BOT_COMMANDS = [
    BotCommand("start", "Меню 📋 / 🔄"),
    BotCommand("balance", "История транзакций 👀"),
    BotCommand("help", "Помощь 🆘"),
    BotCommand("clear", "Очистить контекст 🧹"),
]

# Application definition

INSTALLED_APPS = [
    'bot',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
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

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

LOCAL = True

if LOCAL:
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
            "NAME": getenv("NAME_DB"),
            "USER": getenv("NAME_DB"),
            "PASSWORD": getenv("PASS_DB"),
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

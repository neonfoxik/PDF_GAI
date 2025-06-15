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
ASSISTANT_PROMPT = """Ты - дружелюбный помощник по правилам дорожного движения и юридическим вопросам. 

Твои основные задачи:
1. Отвечать на вопросы, используя:
   - Правила дорожного движения (ПДД)
   - Кодекс об административных правонарушениях (КоАП)
   - Закон о безопасности дорожного движения
   - Федеральный закон "О полиции"
   - Приказ МВД РФ от 02.05.2023 N 264

2. Стиль общения:
   - Используй смайлики для создания дружелюбной атмосферы
   - Будь вежливым и приветливым
   - Объясняй сложные вещи простым языком
   - При ответе на юридические вопросы будь максимально точным и профессиональным

3. Форматирование текста:
   **жирный текст** - для важной информации
   __курсив__ - для дополнительных пояснений
   ~~зачеркнутый текст~~ - для устаревшей информации
   `моноширинный текст` - для цитат из законов и правил

4. Работа с документами:
   - Всегда используй прикрепленные документы как основной источник информации
   - При цитировании указывай точный источник в формате:
     "Название документа" - статья X, пункт Y
   - При работе с юридическими документами:
     * Всегда указывай актуальную редакцию закона
     * При цитировании КоАП РФ указывай номер статьи и части
     * При ссылке на ФЗ "О полиции" указывай номер статьи и пункта
     * При использовании Приказа МВД РФ указывай номер пункта
   - Если информация есть в нескольких документах, укажи все источники
   - При противоречиях между документами:
     * Укажи на существующие противоречия
     * Объясни, какой документ имеет приоритет
     * Предоставь актуальную информацию
   - При отсутствии информации в документах, честно признайся в этом

5. Структура ответа на юридические вопросы:
   - Начни с прямого ответа на вопрос
   - Укажи все релевантные статьи и пункты из документов
   - Добавь пояснения и комментарии
   - При необходимости укажи на возможные исключения или особые случаи
   - В конце дай краткое резюме"""


PROVIDER_NAME = "vsegpt"
PROVIDER = "https://api.vsegpt.ru/v1"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOCAL = os.getenv('LOCAL')

ALLOWED_HOSTS = ["*"]

BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = os.getenv('OWNER_ID')
HOOK = os.getenv('HOOK')


BOT_COMMANDS = [
    BotCommand("start", "Меню"),
    BotCommand("documents_menu", "Работа с документами")
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

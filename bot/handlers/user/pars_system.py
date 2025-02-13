import datetime
from docxtpl import DocxTemplate

from bot import bot, logger
from bot.texts import WE_ARE_WORKING, LC_TEXT
from bot.models import Documents
from django.conf import settings
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


def parsing(callback_query: CallbackQuery):
    _, file_name = callback_query.data.split('_')
    document = Documents.objects.get(name_for_customer=file_name)


    # Загружаем шаблон
    doc = DocxTemplate("template.docx")

    # Данные для замены
    context = {
        'name': 'Иван',
        'date': '1 января 2023'
    }

    # Замена переменных
    doc.render(context)

    # Сохранение нового документа
    doc.save("result.docx")


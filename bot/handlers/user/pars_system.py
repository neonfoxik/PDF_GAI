import datetime
from docxtpl import DocxTemplate
import re
import os
import tempfile

from bot import bot, logger
from bot.texts import WE_ARE_WORKING, LC_TEXT
from bot.models import Documents, User, UserTemplateVariable
from django.conf import settings
from django.db import models
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
    
def parsing(callback: CallbackQuery):
    user_id = callback.from_user.id  # Получаем ID пользователя из чата
    user = User.objects.get(telegram_id=user_id)  # Получаем пользователя из базы данных
    doc_name = callback.data.split('_')[3]
    document = Documents.objects.filter(name=doc_name).first()
    address = document.address
    
    # Получаем файл документа из модели DocumentFile
    document_file = document.files.first()
    if not document_file:
        bot.send_message(user_id, "Файл документа не найден")
        return
        
    # Используем путь к файлу из модели
    doc = DocxTemplate(document_file.file.path)

    context = {}
    fields_need_to_create = []

    # Получаем все переменные пользователя
    user_variables = UserTemplateVariable.objects.filter(user=user)
    
    # Проходим по всем полям документа
    for template_field, display_name in document.template_fields.items():
        # Ищем значение у пользователя
        user_var = user_variables.filter(template_field=template_field).first()
        
        if user_var:
            # Если значение найдено, используем его
            context[template_field] = user_var.value
        else:
            # Если значение не найдено, добавляем в список для создания
            fields_need_to_create.append((template_field, display_name))
    
    if fields_need_to_create:
        bot.send_message(user.telegram_id, "Необходимо создать следующие переменные:")
        # Запрашиваем первую переменную
        ask_next_variable(user, fields_need_to_create, 0, address, context)
        return
    
    # Если все переменные есть, рендерим документ
    render_document(doc, context, user.telegram_id)


def ask_next_variable(user: User, fields: list, index: int, address: str, context: dict):
    if index >= len(fields):
        # Все переменные собраны, можно рендерить документ
        document = Documents.objects.get(address=address)
        document_file = document.files.first()
        if not document_file:
            bot.send_message(user.telegram_id, "Файл документа не найден")
            return
            
        doc = DocxTemplate(document_file.file.path)
        render_document(doc, context, user.telegram_id)
        return

    template_field, display_name = fields[index]
    msg = bot.send_message(user.telegram_id, f"{display_name} - {template_field}")
    bot.register_next_step_handler(msg, get_base_variable, user, template_field, display_name, fields, index, address, context)


def get_base_variable(message: Message, user: User, template_field: str, display_name: str, fields: list, index: int, address: str, context: dict):
    message_text = message.text
    
    # Создаем или обновляем переменную пользователя
    template_var, created = UserTemplateVariable.objects.get_or_create(
        user=user,
        template_field=template_field,
        defaults={
            'display_name': display_name,
            'value': message_text
        }
    )
    
    if not created:
        template_var.value = message_text
        template_var.save()
    
    # Добавляем значение в контекст
    context[template_field] = message_text
    
    # Запрашиваем следующую переменную
    ask_next_variable(user, fields, index + 1, address, context)


def render_document(doc: DocxTemplate, context: dict, chat_id: int):
    # Замена переменных
    doc.render(context)
    
    # Сохраняем результат во временный файл
    tmp_file = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
    doc.save(tmp_file.name)
    tmp_file.close()
    
    # Отправляем документ
    with open(tmp_file.name, 'rb') as f:
        bot.send_document(chat_id, f)
    
    # Планируем удаление файла через некоторое время
    import threading
    import time
    
    def delayed_delete():
        time.sleep(5)  # Даем время на отправку
        try:
            os.unlink(tmp_file.name)
        except:
            pass
    
    threading.Thread(target=delayed_delete).start()

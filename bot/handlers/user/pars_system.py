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
    
# Определяем путь к директории с документами
DOCUMENTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "documents")

def parsing(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        user = User.objects.get(telegram_id=user_id)
        doc_address = callback.data.split('_')[3]
        
        # Проверяем существование документа
        document = Documents.objects.filter(address=doc_address).first()
        if not document:
            bot.send_message(user_id, "Документ не найден.")
            return
            
        doc_path = os.path.join(DOCUMENTS_DIR, f"{document.address}.docx")
        if not os.path.exists(doc_path):
            bot.send_message(user_id, "Файл документа не найден.")
            return
            
        doc = DocxTemplate(doc_path)

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
            ask_next_variable(user, fields_need_to_create, 0, document.address, context)
            return
        
        # Если все переменные есть, рендерим документ
        render_document(doc, context, user.telegram_id)
    except Exception as e:
        logger.error(f"Ошибка в parsing: {e}")
        bot.send_message(user_id, "Произошла ошибка при обработке документа.")


def ask_next_variable(user: User, fields: list, index: int, address: str, context: dict):
    if index >= len(fields):
        # Все переменные собраны, можно рендерить документ
        document = Documents.objects.get(address=address)
        doc_path = os.path.join(DOCUMENTS_DIR, f"{address}.docx")
        if not os.path.exists(doc_path):
            bot.send_message(user.telegram_id, "Файл документа не найден.")
            return
            
        doc = DocxTemplate(doc_path)
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
    try:
        # Замена переменных
        doc.render(context)
        
        # Создаем временный файл для docx
        tmp_docx = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
        
        # Сохраняем docx
        doc.save(tmp_docx.name)
        tmp_docx.close()
        
        # Отправляем DOCX документ
        with open(tmp_docx.name, 'rb') as f:
            bot.send_document(chat_id, f, caption="Ваш документ")
        
        # Планируем удаление временного файла
        def delayed_delete():
            import time
            time.sleep(5)  # Даем время на отправку
            try:
                os.unlink(tmp_docx.name)
            except:
                pass
        
        import threading
        threading.Thread(target=delayed_delete).start()
        
    except Exception as e:
        logger.error(f"Ошибка при рендеринге документа: {e}")
        bot.send_message(chat_id, "Произошла ошибка при создании документа.")

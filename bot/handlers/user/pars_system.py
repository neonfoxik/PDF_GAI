import datetime
from docxtpl import DocxTemplate
import re

from bot import bot, logger
from bot.texts import WE_ARE_WORKING, LC_TEXT
from bot.models import Documents, User
from django.conf import settings
from django.db import models
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


def choose_document(callback: CallbackQuery):
    document = Documents.objects.get(address=callback.data)
    user = User.objects.get(telegram_id=callback.from_user.id)
    

def create_template_variables(address: str, user: User):
    document = Documents.objects.get(address=address)

    # Загружаем шаблон
    doc = DocxTemplate(f"{settings.SRS}{address}")
    
    # Получаем текст документа
    xml_content = doc.get_xml()
    
    # Ищем все переменные в формате {{ variable }}
    template_vars = re.findall(r'\{\{\s*([^}]+)\s*\}\}', xml_content)
    
    # Удаляем дубликаты и пробелы
    template_vars = list(set([var.strip() for var in template_vars]))
    
    # Создаем записи для каждой найденной переменной
    for var in template_vars:
        # Проверяем, есть ли базовое значение у пользователя
        base_var = UserTemplateVariable.objects.filter(
            user=user,
            template_field=var,
            is_base=True,
            document__isnull=True
        ).first()

        # Создаем или получаем переменную для документа
        template_var, created = UserTemplateVariable.objects.get_or_create(
            document=document,
            template_field=var,
            user=user,
            defaults={
                'display_name': var.replace('_', ' ').title(),
                'value': base_var.value if base_var else ''
            }
        )

    # Получаем все значения переменных
    variables = document.template_variables.filter(user=user)
    context = {var.template_field: var.value for var in variables}
    
    # Замена переменных
    doc.render(context)

    doc.save(f"{settings.SRS}{address}")


def set_base_variable(user: User, template_field: str, value: str, display_name: str = None):
    """Установить базовое значение переменной для пользователя"""
    if display_name is None:
        display_name = template_field.replace('_', ' ').title()
        
    var, created = UserTemplateVariable.objects.get_or_create(
        user=user,
        template_field=template_field,
        document__isnull=True,
        is_base=True,
        defaults={
            'display_name': display_name,
            'value': value
        }
    )
    if not created:
        var.value = value
        var.save()
    return var


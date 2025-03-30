import os
from docx import Document
from telegram import CallbackQuery
from bot.models import Documents, User, UserTemplateVariable
from bot import bot
import tempfile

def parse_document(callback_query: CallbackQuery):
    user_id = callback_query.message.chat.id
    _, num = callback_query.data.split("_")
    
    try:
        # Получаем документ и его файл
        doc = Documents.objects.get(address=num)
        document_file = doc.files.first()  # Получаем первый файл документа
        
        if not document_file:
            bot.send_message(user_id, "Файл документа не найден")
            return
            
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
            temp_file.write(document_file.file.read())
            temp_path = temp_file.name
            
        try:
            # Парсим документ
            docx = Document(temp_path)
            fields = {}
            for paragraph in docx.paragraphs:
                text = paragraph.text
                if ":" in text:
                    key, value = text.split(":", 1)
                    fields[key.strip()] = value.strip()
            
            # Сохраняем поля в документе
            doc.template_fields = fields
            doc.save()
            
            # Создаем переменные для пользователя
            user = User.objects.get(telegram_id=str(user_id))
            for key, value in fields.items():
                UserTemplateVariable.objects.create(
                    user=user,
                    display_name=key,
                    template_field=key,
                    value=value
                )
            
            bot.send_message(user_id, "Документ успешно распарсен")
        finally:
            # Удаляем временный файл
            os.unlink(temp_path)
            
    except Documents.DoesNotExist:
        bot.send_message(user_id, "Документ не найден")
    except Exception as e:
        bot.send_message(user_id, f"Ошибка при парсинге документа: {str(e)}") 
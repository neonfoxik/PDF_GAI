import os
from docx import Document
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import CANCELBUTTON, cancellation
from bot.texts import FIELDS_FOR_DOCS
from bot.models import Documents, DocumentFile
from bot import bot

loc_counter = 0
DOCUMENTS_DIR = os.path.dirname(__file__), "..", "..", "documents"

def parse_template_fields(fields_str: str) -> dict:
    """Преобразует строку формата 'ключ : значение; ключ2 : значение2' в словарь"""
    result = {}
    if not fields_str.strip():
        return result
        
    # Разбиваем строку по разделителю ';'
    pairs = fields_str.split(';')
    for pair in pairs:
        if ':' in pair:
            # Разбиваем пару по ':' и убираем лишние пробелы
            key, value = pair.split(':', 1)
            key = key.strip()
            value = value.strip()
            if key and value:  # Проверяем, что ключ и значение не пустые
                result[key] = value
    return result

def change_documents(callback_query: CallbackQuery):
    user_id = callback_query.message.chat.id
    documents = Documents.objects.all()
    buttons = InlineKeyboardMarkup(row_width=2)
    for document in documents:
        button = InlineKeyboardButton(document.name, callback_data=f"chsDoc_{document.address}")
        buttons.add(button)

    bot.send_message(user_id, text="Выберете документ", reply_markup=buttons)

def choose_move(callback_query: CallbackQuery):
    user_id = callback_query.message.chat.id
    _, num = callback_query.data.split("_")

    admin_markup = InlineKeyboardMarkup(row_width=1)
    change_name = InlineKeyboardButton(text='Изменить название', callback_data=f"document_Name_{num}")
    change_fields = InlineKeyboardButton(text="Изменить поля", callback_data=f"document_Fields_{num}")
    change_document = InlineKeyboardButton(text="Изменить документ", callback_data=f"document_Content_{num}")
    del_document = InlineKeyboardButton(text="Удалить документ", callback_data=f"document_Delete_{num}")

    admin_markup.add(change_name, change_fields, change_document, del_document, cancellation)
    bot.send_message(user_id, text="Что нужно сделать с этим документом?", reply_markup=admin_markup)

def changing(callback_query: CallbackQuery):
    bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    user_id = callback_query.message.chat.id
    callback = callback_query.data

    _, act, num = callback.split("_")

    if act == "Name":
        bot.send_message(user_id, "Напишите новое названия")
        bot.register_next_step_handler(callback_query.message, change_name, num)
    elif act == "Fields":
        bot.send_message(user_id, f"Напишите новые поля. {FIELDS_FOR_DOCS}")
        bot.register_next_step_handler(callback_query.message, change_fields, num)
    elif act == "Delete":
        delete_document(num)
        bot.send_message(user_id, "Документ успешно удален")
    else:
        bot.send_message(user_id, "Отправьте новый файл")
        bot.register_next_step_handler(callback_query.message, redc_document, num)

def change_name(message: Message, num: int):
    new_name = message.text

    doc = Documents.objects.get(address=num)
    doc.name = new_name
    doc.save()
    bot.send_message(message.chat.id, "Название обновлено.")

def change_fields(message: Message, num: int):
    fields_str = message.text

    try:
        fields_dict = parse_template_fields(fields_str)
        doc = Documents.objects.get(address=num)
        doc.template_fields = fields_dict
        doc.save()
        bot.send_message(message.chat.id, "Поля успешно обновлены.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обновлении полей: {str(e)}\nУбедитесь, что формат соответствует 'ключ : значение; ключ2 : значение2'")

def delete_document(num):
    doc = Documents.objects.get(address=num)
    # Удаляем все связанные файлы
    doc.files.all().delete()
    # Удаляем сам документ
    doc.delete()

def redc_document(message: Message, num: int):
    try:
        doc = Documents.objects.get(address=num)
        # Удаляем старые файлы
        doc.files.all().delete()

        # Получаем и сохраняем новый файл
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Создаем временный файл
        temp_path = f"temp_{num}.docx"
        with open(temp_path, 'wb') as f:
            f.write(downloaded_file)
        
        # Создаем новый DocumentFile
        with open(temp_path, 'rb') as f:
            document_file = DocumentFile(
                document=doc,
                file_name=message.document.file_name,
                file_size=message.document.file_size,
                file_type=message.document.mime_type
            )
            document_file.file.save(message.document.file_name, f)
            document_file.save()
        
        # Удаляем временный файл
        os.remove(temp_path)

        bot.reply_to(message, "Сохранено")
        bot.send_message(message.chat.id, "Документ обновлен.")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")

def create_document(callback_query: CallbackQuery):
    global loc_counter
    loc_counter += 1
    doc = Document()
    
    try:
        # Создаем новый документ в базе данных
        new_doc = Documents.objects.create(
            address=str(loc_counter),
            name=str(loc_counter),
            template_fields={}
        )
        
        # Создаем временный файл
        temp_path = f"temp_{loc_counter}.docx"
        doc.save(temp_path)
        
        # Открываем файл и создаем DocumentFile
        with open(temp_path, 'rb') as f:
            document_file = DocumentFile(
                document=new_doc,
                file_name=f"{loc_counter}.docx",
                file_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            document_file.file.save(f"{loc_counter}.docx", f)
            document_file.save()
        
        # Удаляем временный файл
        os.remove(temp_path)
        
        bot.send_message(callback_query.message.chat.id, "Новый документ создан")
    except Exception as e:
        bot.send_message(callback_query.message.chat.id, f"Ошибка при создании документа: {str(e)}")

def add_new_document(call: CallbackQuery):
    user_id = call.message.chat.id
    bot.send_message(user_id, "Отправьте документ")
    bot.register_next_step_handler(call.message, add_new_document_doc)

def add_new_document_doc(message: Message):
    global loc_counter
    loc_counter += 1
    num = str(loc_counter)
    
    try:
        # Создаем новый документ в базе данных
        new_doc = Documents.objects.create(
            address=num,
            name=message.document.file_name,
            template_fields={}
        )
        
        # Получаем и сохраняем файл
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Создаем временный файл
        temp_path = f"temp_{num}.docx"
        with open(temp_path, 'wb') as f:
            f.write(downloaded_file)
        
        # Создаем DocumentFile
        with open(temp_path, 'rb') as f:
            document_file = DocumentFile(
                document=new_doc,
                file_name=message.document.file_name,
                file_size=message.document.file_size,
                file_type=message.document.mime_type
            )
            document_file.file.save(message.document.file_name, f)
            document_file.save()
        
        # Удаляем временный файл
        os.remove(temp_path)
        
        bot.reply_to(message, "Документ успешно добавлен")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при добавлении документа: {str(e)}")

def add_new_document_name(message: Message, num: str):
    new_name = message.text

    try:
        doc = Documents.objects.get(address=num)
        doc.name = new_name
        doc.save()
        bot.send_message(message.chat.id, f"Название обновлено. Теперь введите поля.\n{FIELDS_FOR_DOCS}", reply_markup=CANCELBUTTON)
        bot.register_next_step_handler(message, add_new_document_fields, num)
    except Documents.DoesNotExist:
        bot.send_message(message.chat.id, f"Документ с номером {num} не найден.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обновлении имени документа: {str(e)}")

def add_new_document_fields(message: Message, num: str):
    fields_str = message.text

    try:
        fields_dict = parse_template_fields(fields_str)
        doc = Documents.objects.get(address=num)
        doc.template_fields = fields_dict
        doc.save()
        bot.send_message(message.chat.id, "Поля успешно добавлены. Теперь можете пользоваться документом")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при добавлении полей: {str(e)}\nУбедитесь, что формат соответствует 'ключ : значение; ключ2 : значение2'")
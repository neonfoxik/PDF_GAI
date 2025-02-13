import os
from functools import wraps
from docx import Document


from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.models import Documents
from bot.settings import SRS
from bot import bot, logger

loc_counter = 0
user_data = {}


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

    admin_markup = InlineKeyboardMarkup()
    change_name = InlineKeyboardButton(text='Изменить название', callback_data=f"document_Name_{num}")
    change_fields = InlineKeyboardButton(text="Изменить поля", callback_data=f"document_Fields_{num}")
    change_document = InlineKeyboardButton(text="Изменить документ", callback_data=f"document_Content_{num}")

    admin_markup.add(change_name, change_fields, change_document)


def changing(callback_query: CallbackQuery):
    user_id = callback_query.message.chat.id
    callback = callback_query.data

    _, act, num = callback.split("_")
    user_data[user_id] = num

    if act == "Name":
        bot.send_message(callback_query.message, "Напишите новое названия")
        bot.register_next_step_handler(callback_query.message, change_name)
    elif act == "Fields":
        bot.send_message(callback_query.message, "Напишите новые поля")
        bot.register_next_step_handler(callback_query.message, change_fields)
    else:
        bot.send_message(callback_query.message, "Отправьте новый файл")
        bot.register_next_step_handler(callback_query.message, redc_document)


def change_name(message):
    num = user_data.get(message.from_user.id)
    new_name = message.text

    doc = Documents.objects.get(address=num)
    doc.name = new_name
    doc.save()
    bot.send_message(message.chat.id, "Название обновлено.")
    del user_data[message.from_user.id]


def change_fields(message):
    num = user_data.get(message.from_user.id)
    fields = message.text

    doc = Documents.objects.get(address=num)
    doc.fields = fields
    doc.save()
    bot.send_message(message.chat.id, "Поля обновлены обновлено.")
    del user_data[message.from_user.id]


def redc_document(message):
    num = user_data.get(message.from_user.id)
    fields = message.text

    try:
        os.remove(f"{SRS}/{num}.docx")
    except:
        pass
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = SRS + num
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Сохранено")
    except Exception as e:
        bot.reply_to(message, e)

    bot.send_message(message.chat.id, "Документ обновлен.")
    del user_data[message.from_user.id]


def create_document(callback_query: CallbackQuery):
    global loc_counter
    loc_counter += 1
    doc = Document()
    doc.save(SRS+str(loc_counter)+".docx")
    Documents.objects.create(
        address=str(loc_counter),
        name=str(loc_counter),
        fields=''
    )
    bot.send_message(callback_query.message.chat.id, "Новый документ создан")






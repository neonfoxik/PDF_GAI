import os
from docx import Document


from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import CANCELBUTTON, cancellation
from bot.models import Documents
from bot.settings import SRS
from bot import bot

loc_counter = 0


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
    user_id = callback_query.message.chat.id
    callback = callback_query.data

    _, act, num = callback.split("_")

    if act == "Name":
        bot.send_message(user_id, "Напишите новое названия")
        bot.register_next_step_handler(callback_query.message, change_name, num)
    elif act == "Fields":
        bot.send_message(user_id, "Напишите новые поля")
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
    fields = message.text

    doc = Documents.objects.get(address=num)
    doc.fields = fields
    doc.save()
    bot.send_message(message.chat.id, "Поля обновлены обновлено.")


def delete_document(num):
    Documents.objects.get(address=num).delete()
    try:
        os.remove(SRS+num+".docx")
    except:
        pass


def redc_document(message: Message, num: int):
    fields = message.text

    try:
        os.remove(f"{SRS}{num}.docx")
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


def add_new_document(call: CallbackQuery):
    user_id = call.message.chat.id
    bot.send_message(user_id, "Отправьте документ")
    bot.register_next_step_handler(call.message, add_new_document_doc)


def add_new_document_doc(message: Message):
    global loc_counter
    loc_counter += 1
    num = str(loc_counter)
    chat_id = message.chat.id

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = SRS + num
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    Documents.objects.create(
        address=str(num),
        name=str(num),
        fields=''
    )

    bot.reply_to(message, "Сохранено, отправьте название документа", reply_markup=CANCELBUTTON)
    bot.register_next_step_handler(message, add_new_document_name, num)


def add_new_document_name(message: Message, num: int):
    new_name = message.text

    doc = Documents.objects.get(address=num)
    doc.name = new_name
    doc.save()
    bot.send_message(message.chat.id, "Название обновлено. Теперь отправьте поля", reply_markup=CANCELBUTTON)
    bot.register_next_step_handler(message, add_new_document_fields, num)


def add_new_document_fields(message: Message, num: int):
    fields = message.text

    doc = Documents.objects.get(address=num)
    doc.fields = fields
    doc.save()
    bot.send_message(message.chat.id, "Поля обновлены. Теперь можете пользоваться документом")

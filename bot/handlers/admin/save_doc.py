from functools import wraps


from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import bot, logger


def save_document(callback_query: CallbackQuery) -> None:
    user_id = callback_query.message.chat.id

    bot.send_message(user_id, text="Отправьте документ")
    bot.register_next_step_handler(callback_query.message, handle_docs_photo)


def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = "C:/Users/Iskander/Desktop/Progects/PDF_GAI/documents/" + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, e)
from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)


def documents_main_menu(message) -> None:
    try:
        gfdgdfsgfds = InlineKeyboardMarkup()

        gfdgdfsgfds.add(InlineKeyboardButton(text='sdfgdfsgdfsgsdfgdfsg', callback_data='sdfgfdgsdfsgfgsd'))
        
        bot.send_message(message.chat.id, f'главное меню', reply_markup=gfdgdfsgfds)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

@bot.callback_query_handler(func=lambda call: call.data == "sdfgfdgsdfsgfgsd")
def efdsadafdgfasfgds_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        efdsadafdgfasfgds = InlineKeyboardMarkup()

        efdsadafdgfasfgds.add(InlineKeyboardButton(text='dfsadfsafasd', callback_data='gsdfgfsddfgs'))
                
        bot.send_message(call.message.chat.id, f'главное меню', reply_markup=efdsadafdgfasfgds)

    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

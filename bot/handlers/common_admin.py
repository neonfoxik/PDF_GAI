from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message, 
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.models import User, Button, ButtonGroup, Texts


def main_menu(message) -> None:
    try:
        dhhdhdh = InlineKeyboardMarkup()

        bot.send_message(message.chat.id, f'главное меню', reply_markup=dhhdhdh)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

@bot.callback_query_handler(func=lambda call: call.data == "")
def dhhdhdhdh_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        dhhdhdhdh = InlineKeyboardMarkup()

        bot.send_message(call.message.chat.id, f'главное меню', reply_markup=dhhdhdhdh)

    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

@bot.callback_query_handler(func=lambda call: call.data == "")
def hdhdhdhdhdj_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        hdhdhdhdhdj = InlineKeyboardMarkup()

        hdhdhdhdhdj.add(InlineKeyboardButton(text='djjdjdjdhdhhdhd', callback_data='djdhhdhdhdhdhdh'))
                
        bot.send_message(call.message.chat.id, f'главное меню', reply_markup=hdhdhdhdhdj)

    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

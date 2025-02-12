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
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text='привет', callback_data='sdfasdasdf'))
        if isinstance(message, CallbackQuery):
            bot.edit_message_text(
                chat_id=message.message.chat.id,
                message_id=message.message.message_id,
                text='Главное меню:',
                reply_markup=keyboard
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text='Главное меню:',
                reply_markup=keyboard
            )
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')



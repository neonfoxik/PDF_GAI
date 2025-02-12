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
        test1 = InlineKeyboardMarkup()

        test1.add(InlineKeyboardButton(text='короче кнопка 1', callback_data='tefdsad'))
        
        test1.add(InlineKeyboardButton(text='adssdaadsdas', callback_data='dasdsadas'))
        
        bot.send_message(message.chat.id, f'главное меню', reply_markup=test1)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

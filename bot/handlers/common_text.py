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
        gfdsgdfsdfgsfdgs = InlineKeyboardMarkup()

        gfdsgdfsdfgsfdgs.add(InlineKeyboardButton(text='dfsgdfgsdfgsfdgs', callback_data='fdgsdfgsdsfgfdgs'))
        
        bot.send_message(message.chat.id, f'главное меню', reply_markup=gfdsgdfsdfgsfdgs)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

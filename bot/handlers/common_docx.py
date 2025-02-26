from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message, 
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.models import User, Button, ButtonGroup, Texts
from bot.settings import SRS

def documents_main_menu(message) -> None:
    try:
        dfgsgdfsgsdf = InlineKeyboardMarkup()

        dfgsgdfsgsdf.add(InlineKeyboardButton(text='sgdffgdsdfsggdfs', callback_data='dfgsfgdssdfgdfsgsdfg'))
        
        bot.send_message(message.chat.id, f'главное меню', reply_markup=dfgsgdfsgsdf)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

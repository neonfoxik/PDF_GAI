from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message, 
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.keyboards import MENU_BUTTON
from bot.models import User, Button, ButtonGroup, Texts


def main_menu(message) -> None:
    try:
        bot.send_message(message.chat.id, "Главное меню", reply_markup=MENU_BUTTON)
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

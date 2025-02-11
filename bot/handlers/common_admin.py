from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message, 
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.models import User, Button, ButtonGroup

def main_menu(callback_query: CallbackQuery) -> None:
    keyboard = InlineKeyboardMarkup()

    # Группа кнопок: sdfsdf
    keyboard.add(InlineKeyboardButton(text='', callback_data='sdfsdf'))

def sdfsdf_handler(callback_query: CallbackQuery) -> None:
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.message.chat.id, '')

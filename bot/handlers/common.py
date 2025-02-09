from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.models import User
from bot.handlers.user.registration import start_registration
from bot.texts import FAQ, LC_TEXT


def start(message: Message) -> None:
    """Обработчик команды /start."""
    start_registration(message)
    bot.send_message(chat_id=message.chat.id, text=FAQ, parse_mode='Markdown')



def help_(message: Message) -> None:
    """Обработчик команды /help."""
    bot.send_message(chat_id=message.chat.id, text=FAQ, parse_mode='Markdown')

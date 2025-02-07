import datetime

from bot import bot, logger
from bot.texts import WE_ARE_WORKING, LC_TEXT
from bot.models import User
from django.conf import settings



def start_registration(message, delete=True):
    """ Функция для регистрации пользователей """
    user_id = message.from_user.id

    user = User.objects.filter(telegram_id=user_id)

    if not user.exists():
        user = User.objects.create(
            telegram_id=user_id,
            name=message.from_user.first_name,
        )
        user.save()
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")
        keyboard.add(button)
        bot.send_message(chat_id=message.chat.id, text="Вы успешно зарегистрированы!", parse_mode='Markdown', reply_markup=keyboard)
    else:
        user = User.objects.get(telegram_id=user_id)
    
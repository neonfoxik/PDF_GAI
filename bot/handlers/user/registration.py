from bot import bot
from bot.models import User
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.handlers.common_admin import (
    main_menu
)


def start_registration(message):
    """ Функция для регистрации пользователей """
    user_id = message.from_user.id

    user, created = User.objects.get_or_create(
        telegram_id=user_id,
        defaults={'name': message.from_user.first_name}
    )

    if created:
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Главное меню", callback_data="main_menu")
        keyboard.add(button)
        bot.send_message(chat_id=message.chat.id, text="Вы успешно зарегистрированы!", parse_mode='Markdown',
                         reply_markup=keyboard)
    else:
        main_menu(message)

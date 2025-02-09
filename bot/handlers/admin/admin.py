from functools import wraps

from django.conf import settings
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot import bot, logger
from bot.models import User
from bot.keyboards import SAVE_BUTTON

def admin_permission(func):
    """
    Проверка прав администратора для доступа к функции.
    """

    @wraps(func)
    def wrapped(message: Message) -> None:
        user_id = message.from_user.id
        logger.info(f'Попытка отправки сообщения пользователю с ID: {user_id}')  # Логирование ID пользователя
        try:
            user = User.objects.get(telegram_id=user_id)
        except User.DoesNotExist:
            bot.send_message(user_id, '⛔ Пользователь не найден в системе')
            logger.warning(f'Пользователь с ID {user_id} не найден')
            return
        if not user.is_admin:
            bot.send_message(user_id, '⛔ У вас нет администраторского доступа')
            logger.warning(f'Попытка доступа к админ панели от {user_id}')
            return
        return func(message)

    return wrapped

@admin_permission
def add_button(message: Message) -> None:
    msg = bot.send_message(message.chat.id, 'Укажите название группы кнопок английскими буквами')
    bot.register_next_step_handler(msg, Get_button_group_name)

@admin_permission
def Get_button_group_name(message: Message) -> None:
    global button_group_name
    button_group_name = message.text
    msg = bot.send_message(message.chat.id, 'Укажите название кнопки английскими буквами')
    bot.register_next_step_handler(msg, Get_button_name)

@admin_permission
def Get_button_name(message: Message) -> None:
    global button_name
    button_name = message.text
    msg = bot.send_message(message.chat.id, 'Укажите текст кнопки')
    bot.register_next_step_handler(msg, Get_button_text)

@admin_permission
def Get_button_text(message: Message) -> None:
    global button_text
    button_text = message.text
    bot.send_message(message.chat.id, 'Хотите ли вы подтвердить создание кнопки?', reply_markup=SAVE_BUTTON)

@admin_permission
def save_button_to_file(message: Message) -> None:
    group_name = button_group_name
    name = button_name
    text = button_text
    bot.answer_callback_query(message.id, "Кнопка успешно создана!")
    with open('.admin_keyboards.py', 'a', encoding='utf-8') as f:
        if not hasattr(bot, group_name):
            f.write(f'{group_name}_BUTTONS = InlineKeyboardMarkup()\n')
        f.write(f'{name.upper()}_BUTTON = InlineKeyboardButton(text="{text}", callback_data="{name}")\n')
        f.write(f'{group_name}_BUTTONS.add({name.upper()}_BUTTON)\n')



    

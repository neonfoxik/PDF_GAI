from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message, 
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.models import User, Button, ButtonGroup, Texts
from bot.keyboards import UNIVERSAL_BUTTONS




def main_menu_call(call: CallbackQuery) -> None:
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Главное меню')
        jdjdjdj = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                jdjdjdj.add(InlineKeyboardButton(text='Включить режим редактирования', callback_data='edit_main_menu'))
        except User.DoesNotExist:
            pass

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=jdjdjdj)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

def main_menu_message(message: Message) -> None:
    try:
        jdjdjdj = InlineKeyboardMarkup()

        user_id = message.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                jdjdjdj.add(InlineKeyboardButton(text='Включить режим редактирования', callback_data='edit_main_menu'))
        except User.DoesNotExist:
            pass

        bot.send_message(message.chat.id, 'Главное меню', reply_markup=jdjdjdj)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

def main_menu_edit(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        jdjdjdj = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                jdjdjdj.add(InlineKeyboardButton(text='Выключить режим редактирования', callback_data='main_menu'))
        except User.DoesNotExist:
            pass

        bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=jdjdjdj)

    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

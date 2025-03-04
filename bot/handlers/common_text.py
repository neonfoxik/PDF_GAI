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
        bnkl = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                bnkl.add(InlineKeyboardButton(text='Включить режим редактирования', callback_data='edit_main_menu'))
        except User.DoesNotExist:
            pass


        bnkl.add(InlineKeyboardButton(text='sfddsfdsf', callback_data='gygyg'))
            
        
        
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=bnkl)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

def main_menu_message(message: Message) -> None:
    try:
        bnkl = InlineKeyboardMarkup()

        user_id = message.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                bnkl.add(InlineKeyboardButton(text='Включить режим редактирования', callback_data='edit_main_menu'))
        except User.DoesNotExist:
            pass

        bnkl.add(InlineKeyboardButton(text='sfddsfdsf', callback_data='gygyg'))
            
        
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=bnkl)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

def main_menu_edit(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bnkl = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                bnkl.add(InlineKeyboardButton(text='Выключить режим редактирования', callback_data='main_menu'))
        except User.DoesNotExist:
            pass

        

        bnkl.add(InlineKeyboardButton(text='sfddsfdsf', callback_data='edit_button_main_gygyg'))

        bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=bnkl)

    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

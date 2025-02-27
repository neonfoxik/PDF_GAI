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


class IsEdit:
    def __init__(self):
        self.IsEdit = False
        
    @property
    def is_edit(self):
        return self.IsEdit
        
    @is_edit.setter 
    def is_create_button(self, value):
        self.IsEdit = value


def main_menu_call(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        djsjhdhdh = InlineKeyboardMarkup()
        if is_edit == True:
            djsjhdhdh.add(InlineKeyboardButton(text='привет', callback_data='edit_jdjdjdjjd'))
        else:
            djsjhdhdh.add(InlineKeyboardButton(text='привет', callback_data='jdjdjdjjd'))

        bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=djsjhdhdh)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

def main_menu_message(message: Message) -> None:
    try:
        djsjhdhdh = InlineKeyboardMarkup()

        djsjhdhdh.add(InlineKeyboardButton(text='привет', callback_data='jdjdjdjjd'))
        
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=djsjhdhdh)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

@bot.callback_query_handler(func=lambda call: call.data == "jdjdjdjjd")
def sggshshsh_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'привет я крутой', reply_markup=UNIVERSAL_BUTTONS)


    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

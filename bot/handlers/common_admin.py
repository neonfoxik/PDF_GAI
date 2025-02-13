from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message, 
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.models import User, Button, ButtonGroup, Texts


def main_menu(message) -> None:
    try:
        test = InlineKeyboardMarkup()

        test.add(InlineKeyboardButton(text='привет', callback_data='test1'))
        
        bot.send_message(message.chat.id, f'главное меню', reply_markup=test)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

@bot.callback_query_handler(func=lambda call: call.data == "test1")
def test2_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        test2 = InlineKeyboardMarkup()

        test2.add(InlineKeyboardButton(text='fdsadfasdfasdf', callback_data='test321'))
                
        bot.send_message(call.message.chat.id, f'главное меню', reply_markup=test2)

    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

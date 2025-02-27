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
from bot.keyboards import UNIVERSAL_BUTTONS


def main_menu_call(call: CallbackQuery) -> None:
    try:
        cjjdjdjdjdjxjdhhd = InlineKeyboardMarkup()

        cjjdjdjdjdjxjdhhd.add(InlineKeyboardButton(text='djjdjdjdjjdjdhd', callback_data='dhhdhdjdjdjsjjddkjd'))
        
        bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=cjjdjdjdjdjxjdhhd)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

def main_menu_message(message: Message) -> None:
    try:
        cjjdjdjdjdjxjdhhd = InlineKeyboardMarkup()

        cjjdjdjdjdjxjdhhd.add(InlineKeyboardButton(text='djjdjdjdjjdjdhd', callback_data='dhhdhdjdjdjsjjddkjd'))
        
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=cjjdjdjdjdjxjdhhd)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

@bot.callback_query_handler(func=lambda call: call.data == "dhhdhdjdjdjsjjddkjd")
def duhdhdhdjdjd_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'этого бота сделал я', reply_markup=UNIVERSAL_BUTTONS)


    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

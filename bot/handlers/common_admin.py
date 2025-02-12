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
        test1 = InlineKeyboardMarkup()

        test1.add(InlineKeyboardButton(text='короче кнопка 1', callback_data='tefdsad'))
        
        test1.add(InlineKeyboardButton(text='adssdaadsdas', callback_data='dasdsadas'))
        
        test1.add(InlineKeyboardButton(text='sdffsd', callback_data='sdffds'))
        
        test1.add(InlineKeyboardButton(text='fdsfds', callback_data='button'))
        
        test1.add(InlineKeyboardButton(text='fdgdfgfdg', callback_data='dfggdffgd'))
        
        bot.send_message(message.chat.id, f'главное меню', reply_markup=test1)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

@bot.callback_query_handler(func=lambda call: call.data == "")
def gedfgdfsgsdf_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        gedfgdfsgsdf = InlineKeyboardMarkup()

        gedfgdfsgsdf.add(InlineKeyboardButton(text='dfgsdfgsfdgs', callback_data='sdfggsfdsdfg'))
                
        bot.send_message(call.message.chat.id, f'главное меню', reply_markup=gedfgdfsgsdf)

    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

@bot.callback_query_handler(func=lambda call: call.data == "tefdsad")
def gdfgdffgdfdgdfg_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        gdfgdffgdfdgdfg = InlineKeyboardMarkup()

        gdfgdffgdfdgdfg.add(InlineKeyboardButton(text='dsfaadsfdfas', callback_data='dfsasffdasasdf'))
                
        bot.send_message(call.message.chat.id, f'главное меню', reply_markup=gdfgdffgdfdgdfg)

    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

@bot.callback_query_handler(func=lambda call: call.data == "dsfaadsfdfas")
def fghdgfdrgtfd_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        fghdgfdrgtfd = InlineKeyboardMarkup()

        fghdgfdrgtfd.add(InlineKeyboardButton(text='gsdffgdsfdgssfgd', callback_data='fgdgdfsfdgsgfds'))
                
        bot.send_message(call.message.chat.id, f'главное меню', reply_markup=fghdgfdrgtfd)

    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

@bot.callback_query_handler(func=lambda call: call.data == "dasadsdas")
def admin_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        admin = InlineKeyboardMarkup()

        bot.send_message(call.message.chat.id, f'главное меню', reply_markup=admin)

    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

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
        adsfdasfsdaf = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                adsfdasfsdaf.add(InlineKeyboardButton(text='Выключить режим редактирования', callback_data='main_menu'))
        except User.DoesNotExist:
            pass


        adsfdasfsdaf.add(InlineKeyboardButton(text='adsffsdadfsadsfasdfaasdf', callback_data='adsffadssfdaasdf'))
            
        
        
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=adsfdasfsdaf)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

def main_menu_message(message: Message) -> None:
    try:
        adsfdasfsdaf = InlineKeyboardMarkup()

        user_id = message.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                adsfdasfsdaf.add(InlineKeyboardButton(text='Включить режим редактирования', callback_data='edit_main_menu'))
        except User.DoesNotExist:
            pass

        adsfdasfsdaf.add(InlineKeyboardButton(text='adsffsdadfsadsfasdfaasdf', callback_data='adsffadssfdaasdf'))
            
        
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=adsfdasfsdaf)
        
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

def main_menu_edit(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        adsfdasfsdaf = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                adsfdasfsdaf.add(InlineKeyboardButton(text='Выключить режим редактирования', callback_data='main_menu'))
        except User.DoesNotExist:
            pass

        

        adsfdasfsdaf.add(InlineKeyboardButton(text='adsffsdadfsadsfasdfaasdf', callback_data='edit_button_main_adsffadssfdaasdf'))

        bot.send_message(call.message.chat.id, 'Главное меню', reply_markup=adsfdasfsdaf)

    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

@bot.callback_query_handler(func=lambda call: call.data == "adsffadssfdaasdf")
def sfdasdfasdfafsdasdfadsfa_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        sfdasdfasdfafsdasdfadsfa = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                sfdasdfasdfafsdasdfadsfa.add(InlineKeyboardButton(text='Включить режим редактирования', callback_data='edit_sfdasdfasdfafsdasdfadsfa_handler'))
        except User.DoesNotExist:
            pass

        
        sfdasdfasdfafsdasdfadsfa.add(InlineKeyboardButton(text='dasffdasdfsasdaf', callback_data='dsafasdfdasfdsf'))

        bot.send_message(call.message.chat.id, f'главное меню', reply_markup=sfdasdfasdfafsdasdfadsfa)

    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

@bot.callback_query_handler(func=lambda call: call.data == "edit_sfdasdfasdfafsdasdfadsfa_handler")
def edit_sfdasdfasdfafsdasdfadsfa_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        sfdasdfasdfafsdasdfadsfa = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                sfdasdfasdfafsdasdfadsfa.add(InlineKeyboardButton(text='Выключить режим редактирования', callback_data='edit_sfdasdfasdfafsdasdfadsfa_handler'))
        except User.DoesNotExist:
            pass

        
        sfdasdfasdfafsdasdfadsfa.add(InlineKeyboardButton(text='dasffdasdfsasdaf', callback_data='edit_button_main_dsafasdfdasfdsf'))

        bot.send_message(call.message.chat.id, f'главное меню', reply_markup=sfdasdfasdfafsdasdfadsfa)

    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

@bot.callback_query_handler(func=lambda call: call.data == "dsafasdfdasfdsf")
def fgsgdfgdf_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        fgsgdfgdf = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                fgsgdfgdf.add(InlineKeyboardButton(text='Включить режим редактирования', callback_data='edit_fgsgdfgdf_handler'))
        except User.DoesNotExist:
            pass

        
        fgsgdfgdf.add(InlineKeyboardButton(text='привет', callback_data='gfddfgdfg'))

        bot.send_message(call.message.chat.id, f'главное меню', reply_markup=fgsgdfgdf)

    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

@bot.callback_query_handler(func=lambda call: call.data == "edit_fgsgdfgdf_handler")
def edit_fgsgdfgdf_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        fgsgdfgdf = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                fgsgdfgdf.add(InlineKeyboardButton(text='Выключить режим редактирования', callback_data='edit_fgsgdfgdf_handler'))
        except User.DoesNotExist:
            pass

        
        fgsgdfgdf.add(InlineKeyboardButton(text='привет', callback_data='edit_button_main_gfddfgdfg'))

        bot.send_message(call.message.chat.id, f'главное меню', reply_markup=fgsgdfgdf)

    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')

from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.models import User, Button, ButtonGroup, Texts


def documents_main_menu(message) -> None:
    try:
        fgddsfgsdf = InlineKeyboardMarkup()

        fgddsfgsdf.add(InlineKeyboardButton(text='fgdsfdsgfdgfgsdfgds', callback_data='fsgdgfssfdgfgdsfgds'))

        fgddsfgsdf.add(InlineKeyboardButton(text='fdsggdfsfdgssdfg', callback_data='dsfgsfdgfdsggfdsgdfsfdgsdgfs'))

        bot.send_message(message.chat.id, f'главное меню', reply_markup=fgddsfgsdf)

    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')

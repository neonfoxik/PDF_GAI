import os

import requests
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from datetime import datetime


from django.conf import settings
from bot import AI_ASSISTANT, bot, logger
from bot.core import check_registration
from bot.models import User

from bot.texts import NOT_IN_DB_TEXT
from bot.apis.long_messages import split_message
from bot.keyboards import LONGMESSAGE_BUTTONS


@check_registration
def chat_with_ai(message: Message) -> None:
    """Chatting with AI handler."""
    user_id = message.chat.id
    user_message = message.text
    msg = bot.send_message(message.chat.id, 'Думаю над ответом 💭')
    bot.send_chat_action(user_id, 'typing')

    try:
        response = AI_ASSISTANT.get_response(chat_id=user_id, text=user_message)
        if not response:
            raise Exception("Не удалось получить ответ от AI")

        response_message = response['message']
        user = User.objects.get(telegram_id=user_id)

        if len(response_message) > 4096:
            user.ai_response = response_message
            user.save()
            bot.edit_message_text(
                "Ответ ИИ слишком длинный, выберте как вы хотите его получить: ",
                user_id,
                msg.message_id,
                reply_markup=LONGMESSAGE_BUTTONS
            )
        else:
            try:
                bot.edit_message_text(
                    text=response_message,
                    chat_id=user_id,
                    message_id=msg.message_id,
                    parse_mode='Markdown')
            except Exception as e:
                logger.critical(f"Ошибка при редактировании сообщения: {e}")
                bot.edit_message_text(text=response_message, chat_id=user_id, message_id=msg.message_id)

    except Exception as e:
        bot.send_message(user_id, 'Пока мы чиним бот. Если это продолжается слишком долго, напишите нам - /help')
        logger.critical(e)

import os
import base64
import json

import dotenv
import openai

from io import BytesIO
from django.conf import settings
from bot.models import User

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

ASSISTANT_PROMPT = 'settings.ASSISTANT_PROMPT'

openai.base_url = "https://api.vsegpt.ru:6070/v1/"

def get_chat_history(user_id):
    user = User.objects.get(telegram_id=user_id)
    return user.message_context or []

def save_chat_history(user_id, messages):
    user = User.objects.get(telegram_id=user_id)
    user.message_context = messages
    user.save()

def generate_response(prompt, user_id):
    chat_history = get_chat_history(user_id)

    # Добавляем системный промпт в начало истории, если история пуста
    if not chat_history:
        chat_history = [{"role": "system", "content": settings.ASSISTANT_PROMPT}]

    # Добавляем новое сообщение пользователя
    chat_history.append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model="openai/gpt-4o-mini",
        messages=chat_history
    )

    assistant_response = completion.choices[0].message.content

    # Добавляем ответ ассистента в историю
    chat_history.append({"role": "assistant", "content": assistant_response})

    # Сохраняем обновленную историю
    save_chat_history(user_id, chat_history)

    return assistant_response

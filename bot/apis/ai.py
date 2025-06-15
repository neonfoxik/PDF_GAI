import os
import base64

import dotenv
import openai

from io import BytesIO

from django.conf import settings
from .document_processor import DocumentProcessor

dotenv.load_dotenv()

openai.api_key = "sk-or-vv-9d90950af188ed57252dbbc413034c8038f982ddf17e9f6d187e2ca03c227f3f"

ASSISTANT_PROMPT = settings.ASSISTANT_PROMPT

openai.base_url = "https://api.vsegpt.ru:6070/v1/"


class BaseAIAPI:
    def __init__(self, ) -> None:
        self._ASSISTANT_PROMPT: str = ASSISTANT_PROMPT
        self.chat_history: dict = {}
        self._TEMPERATURE = 0.7
        self.document_processor = DocumentProcessor()

    def clear_chat_history(self, chat_id: int) -> None:
        self.chat_history.pop(chat_id, None)

    def _get_documents_content(self) -> str:
        """
        Получает содержимое всех юридических документов
        """
        documents_content = self.document_processor.process_documents()
        return "\n\n".join([
            f"=== {doc_name} ===\n{content[:2000]}..."  # Ограничиваем размер каждого документа
            for doc_name, content in documents_content.items()
        ])


class OpenAIAPI(BaseAIAPI):
    def __init__(self, ) -> None:
        super().__init__()

    def _get_or_create_user_chat_history(self, chat_id: int, new_user_message: str = "") -> list:
        if not self.chat_history.get(chat_id, False):
            self.chat_history[chat_id] = []
            # Добавляем содержимое документов в системный промпт
            documents_content = self._get_documents_content()
            system_prompt = f"{self._ASSISTANT_PROMPT}\n\nСодержимое юридических документов:\n{documents_content}"
            self.chat_history[chat_id].append({"role": "system", "content": system_prompt})
            self.chat_history[chat_id].append({"role": "user", "content": new_user_message})
            return self.chat_history[chat_id]

        self.chat_history[chat_id].append({"role": "user", "content": new_user_message})
        chat_history = self.chat_history[chat_id]
        return chat_history

    def get_response(self, chat_id: int, text: str, max_token: int = 1024) -> dict:
        user_chat_history = self._get_or_create_user_chat_history(chat_id, text)

        try:
            response = (
                openai.chat.completions.create(
                    model='openai/gpt-4o-mini',
                    messages=user_chat_history,
                    temperature=self._TEMPERATURE,
                    n=1,
                    max_tokens=max_token, )
            )

            answer = {"message": response.choices[0].message.content}
            self.chat_history[chat_id].append({"role": "assistant", "content": answer["message"]})

            return answer

        except Exception as e:
            print("Не удалось получить ответ от AI:", e)

    def add_txt_to_user_chat_history(self, chat_id: int, text: str) -> None:
        try:
            self._get_or_create_user_chat_history(chat_id, text)
        except Exception as e:
            print("Ошибка при добавлении текста в историю чата пользователя:", e)

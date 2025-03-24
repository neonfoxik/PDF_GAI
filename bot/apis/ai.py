import os
import base64

import dotenv
import openai

from io import BytesIO

from django.conf import settings

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

ASSISTANT_PROMPT = 'settings.ASSISTANT_PROMPT'

openai.base_url = "https://api.vsegpt.ru:6070/v1/"


class BaseAIAPI:
    def __init__(self, ) -> None:
        self._ASSISTANT_PROMPT: str = ASSISTANT_PROMPT
        self.chat_history: dict = {}
        self._TEMPERATURE = 0.7

    def clear_chat_history(self, chat_id: int) -> None:
        self.chat_history.pop(chat_id)


class OpenAIAPI(BaseAIAPI):
    def __init__(self, ) -> None:
        super().__init__()

    def _get_or_create_user_chat_history(self, chat_id: int, new_user_message: str = "") -> list:
        if not self.chat_history.get(chat_id, False):
            self.chat_history[chat_id] = []
            self.chat_history[chat_id].append({"role": "system", "content": self._ASSISTANT_PROMPT})
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
            print(e)

    def add_txt_to_user_chat_history(self, chat_id: int, text: str) -> None:
        try:
            self._get_or_create_user_chat_history(chat_id, text)
        except Exception as e:
            print("Error occurred while adding text to user chat history")

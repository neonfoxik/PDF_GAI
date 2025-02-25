import os
import base64

import dotenv
import openai

from io import BytesIO

from django.conf import settings

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

ASSISTANT_PROMPT = 'settings.ASSISTANT_PROMPT'
ANALYTIC_PROMPT = 'settings.ANALYTIC_PROMPT'

openai.base_url = "https://api.vsegpt.ru:6070/v1/"



def generate_response(prompt):
    completion = openai.ChatCompletion.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content


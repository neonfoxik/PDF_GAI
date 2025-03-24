import logging
import telebot
from django.conf import settings
from bot.apis.ai import OpenAIAPI

AI_ASSISTANT = OpenAIAPI()
commands = settings.BOT_COMMANDS

bot = telebot.TeleBot(
    settings.BOT_TOKEN,
    threaded=False,
    skip_pending=True,
)

def init_bot():
    try:
        bot.set_my_commands(commands)
        logging.info(f'@{bot.get_me().username} started')
    except Exception as e:
        logging.error(f'Failed to initialize bot commands: {e}')

logger = telebot.logger
logger.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO, filename="ai_log.log", filemode="w")
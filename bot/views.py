from traceback import format_exc
from bot.handlers import *
from bot.handlers.admin import *
from bot.handlers.admin.admin import *
from bot.handlers.user.long_messages import long_message_get_send_option, long_message_get_send_option_docs
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from telebot.apihelper import ApiTelegramException
from telebot.types import Update

from bot import bot, logger


@require_GET
def set_webhook(request: HttpRequest) -> JsonResponse:
    """Setting webhook."""
    bot.set_webhook(url=f"{settings.HOOK}/bot/{settings.BOT_TOKEN}")
    bot.send_message(settings.OWNER_ID, "webhook set")
    return JsonResponse({"message": "OK"}, status=200)


@require_GET
def status(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"message": "OK"}, status=200)


@csrf_exempt
@require_POST
@sync_to_async
def index(request: HttpRequest) -> JsonResponse:
    if request.META.get("CONTENT_TYPE") != "application/json":
        return JsonResponse({"message": "Bad Request"}, status=403)

    json_string = request.body.decode("utf-8")
    update = Update.de_json(json_string)
    try:
        bot.process_new_updates([update])
    except ApiTelegramException as e:
        logger.error(f"Telegram exception. {e} {format_exc()}")
    except ConnectionError as e:
        logger.error(f"Connection error. {e} {format_exc()}")
    except Exception as e:
        bot.send_message(settings.OWNER_ID, f'Error from index: {e}')
        logger.error(f"Unhandled exception. {e} {format_exc()}")
    return JsonResponse({"message": "OK"}, status=200)


"""
Common
"""

admin_panel = bot.message_handler(commands=["admin"])(admin_panel)
clear_chat_history = bot.message_handler(commands=["clear"])(clear_chat_history)
start = bot.message_handler(commands=["start"])(start)
help_ = bot.message_handler(commands=["help"])(help_)
transaction = bot.message_handler(commands=["balance"])(balance)


files_to_text_ai = bot.message_handler(content_types=["document"])(files_to_text_ai)

get_sum = bot.callback_query_handler(lambda c: c.data.startswith('accept_'))(get_sum)

pay_for_mode = bot.callback_query_handler(lambda call: call.data.startswith("pay_"))(pay_for_mode)

choice = bot.callback_query_handler(lambda c: c.data == "choice")(choice)
image_gen = bot.callback_query_handler(lambda c: c.data == 'image_gen')(image_gen)

image_gen = bot.callback_query_handler(lambda c: c.data == 'image_gen')(image_gen)
long_message_get_send_option = bot.callback_query_handler(lambda c: c.data.startswith("lngmsg_"))(long_message_get_send_option)
long_message_get_send_option_docs = bot.callback_query_handler(lambda c: c.data.startswith("documents_"))(long_message_get_send_option_docs)

broadcast_message = bot.callback_query_handler(lambda c: c.data == "broadcast_message")(broadcast_message)
admin_panelCall = bot.callback_query_handler(lambda c: c.data == "admin_panel")(admin_panel)
monthMarkup = bot.callback_query_handler(lambda c: c.data == "monthMarkup")(monthMarkup)
month_statistic = bot.callback_query_handler(lambda c: c.data.startswith("month_"))(month_statistic)
choice_handler = bot.callback_query_handler(lambda c: c.data.startswith('choice_'))(choice_handler)
back_handler = bot.callback_query_handler(lambda c: c.data == "back")(back_handler)




accept_subscribe_payment = bot.callback_query_handler(lambda c: c.data.startswith('accept-sucribe_'))(accept_subscribe_payment)

reject_payment = bot.callback_query_handler(lambda c: c.data.startswith('reject_'))(reject_payment)

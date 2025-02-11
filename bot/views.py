from traceback import format_exc
from bot.handlers import *
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
start = bot.message_handler(commands=["start"])(start)
help_ = bot.message_handler(commands=["help"])(help_)
admin = bot.message_handler(commands=["admin"])(admin_menu)

create_button = bot.callback_query_handler(lambda c: c.data == 'create_button')(add_button)
save_button = bot.callback_query_handler(lambda c: c.data == 'save_button')(save_button_to_file)
cancellation_button = bot.callback_query_handler(lambda c: c.data == 'cancellation')(cancellation_button)

button_actions = bot.callback_query_handler(lambda c: c.data.startswith('list_'))(button_actions)
edit_button_callback_name = bot.callback_query_handler(lambda c: c.data.startswith('edit_name_'))(edit_button_callback_name)

delete_button_from_file = bot.callback_query_handler(lambda c: c.data.startswith('delete_button_'))(delete_button_from_file)
list_buttons = bot.callback_query_handler(lambda c: c.data == 'edit_buttons')(list_buttons)
edit_button_menu = bot.callback_query_handler(lambda c: c.data.startswith('edit_button_'))(edit_button_menu)

button_group_actions = bot.callback_query_handler(lambda c: c.data.startswith('list_group_'))(button_group_actions)
delete_group_from_file = bot.callback_query_handler(lambda c: c.data.startswith('delete_group_'))(delete_group_from_file)
list_button_group = bot.callback_query_handler(lambda c: c.data == 'edit_group_button')(list_button_group)
analyze_and_fill_common_admin = bot.callback_query_handler(lambda c: c.data == 'upload_buttons')(analyze_and_fill_common_admin )





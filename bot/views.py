from traceback import format_exc
from bot.handlers import *
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from telebot.apihelper import ApiTelegramException
from telebot.types import Update
from bot.handlers.user.long_messages import long_message_get_send_option, long_message_get_send_option_docs
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
documents_admin_menu = bot.message_handler(commands=["admin"])(documents_admin_menu)
documents_main_menu = bot.message_handler(commands=["documents_menu"])(documents_main_menu)
next_button_menu = bot.callback_query_handler(lambda c: c.data.startswith('bim_'))(next_button_menu)
old_button_menu = bot.callback_query_handler(lambda c: c.data.startswith('back_btn_'))(old_button_menu)
main_menu_call = bot.callback_query_handler(lambda c: c.data == 'main_menu_call')(main_menu_call)
documents_menu_call = bot.callback_query_handler(lambda c: c.data == 'documents_menu_call')(documents_menu_call)
cancellation = bot.callback_query_handler(lambda c: c.data == 'cancellation')(admin_menu_call)
change_documents = bot.callback_query_handler(lambda c: c.data == 'load_file')(change_documents)
choose_move = bot.callback_query_handler(lambda c: c.data.startswith('chsDoc'))(choose_move)
changing = bot.callback_query_handler(lambda c: c.data.startswith('document_'))(changing)
new_document = bot.callback_query_handler(lambda c: c.data == "create_new_document")(create_document)

add_new_document = bot.callback_query_handler(lambda c: c.data == "add_new_doc")(add_new_document)

documents_sender = bot.callback_query_handler(lambda c: c.data.startswith('doc_sender_'))(documents_sender)



parsing = bot.callback_query_handler(lambda c: c.data.startswith('markup_choose_document_'))(parsing)


choose_default_user_values = bot.callback_query_handler(lambda c: c.data == "ChangeDefaultUserValue111")\
    (choose_default_user_values)
change_default_user_values = bot.callback_query_handler(lambda c: c.data.startswith("ChangeDefaultUserValue_"))\
    (change_default_user_value)

chat_with_ai = bot.message_handler(func=lambda message: True)(chat_with_ai)



long_message_get_send_option = bot.callback_query_handler(lambda c: c.data.startswith("lngmsg_"))\
    (long_message_get_send_option)
long_message_get_send_option_docs = bot.callback_query_handler(lambda c: c.data.startswith("documents_"))\
    (long_message_get_send_option_docs)


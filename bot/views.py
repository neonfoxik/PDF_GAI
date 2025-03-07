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
admin = bot.message_handler(commands=["admin"])(admin_menu)
documents_main_menu = bot.message_handler(commands=["documents_menu"])(documents_main_menu)


admin_menu_call = bot.callback_query_handler(lambda c: c.data == "admin_menu")(admin_menu_call)
users_action_main = bot.callback_query_handler(lambda c: c.data == "users_action")(users_action_main)
create_button = bot.callback_query_handler(lambda c: c.data == 'create_button')(add_button)
save_button = bot.callback_query_handler(lambda c: c.data == 'save_button')(save_button_to_file)
cancellation_button = bot.callback_query_handler(lambda c: c.data == 'cancellation')(cancellation_button)
change_documents = bot.callback_query_handler(lambda c: c.data == 'load_file')(change_documents)
choose_move = bot.callback_query_handler(lambda c: c.data.startswith('chsDoc'))(choose_move)
changing = bot.callback_query_handler(lambda c: c.data.startswith('document_'))(changing)
new_document = bot.callback_query_handler(lambda c: c.data == "create_new_document")(create_document)
view_button_group_in_select_txt = bot.callback_query_handler(lambda c: c.data == "view_button_group_in_select_txt")\
    (view_button_group_in_select_txt)
is_sending_to_admin = bot.callback_query_handler(lambda c: c.data.startswith('setbuy'))(is_sending_to_admin)
accept = bot.callback_query_handler(lambda c: c.data.startswith("accept"))(accept)
add_new_document = bot.callback_query_handler(lambda c: c.data == "add_new_doc")(add_new_document)

documents_sender = bot.callback_query_handler(lambda c: c.data.startswith('doc_sender_'))(documents_sender)

edit_text_main = bot.callback_query_handler(lambda c: c.data.startswith('edit_text_main_'))(edit_text_main)


delete_text = bot.callback_query_handler(lambda c: c.data.startswith('delete_text_'))(delete_text)
confirm_delete_text = bot.callback_query_handler(lambda c: c.data.startswith('confirm_delete_text_'))\
    (confirm_delete_text)

edit_text_text = bot.callback_query_handler(lambda c: c.data.startswith('edit_text_text_'))(edit_text_text)


edit_button_main = bot.callback_query_handler(lambda c: c.data.startswith('edit_button_main_'))(edit_button_main)

delete_button = bot.callback_query_handler(lambda c: c.data.startswith('delete_button_'))(delete_button)
confirm_delete_button = bot.callback_query_handler(lambda c: c.data.startswith('confirm_delete_button_'))\
    (confirm_delete_button)
edit_button_text = bot.callback_query_handler(lambda c: c.data.startswith('edit_button_text_'))(edit_button_text)

delete_button_group = bot.callback_query_handler(lambda c: c.data.startswith('delete_group_button_'))(delete_button_group)
confirm_delete_group = bot.callback_query_handler(lambda c: c.data.startswith('confirm_delete_group_'))(confirm_delete_group)


analyze_and_fill_common_admin = bot.callback_query_handler(lambda c: c.data == 'upload_buttons_txt')\
    (analyze_and_fill_common_admin)
main_menu = bot.callback_query_handler(lambda c: c.data == 'main_menu')(main_menu_call)
main_menu_edit = bot.callback_query_handler(lambda c: c.data == 'edit_main_menu')(main_menu_edit)
view_all_buttons_in_button_group = bot.callback_query_handler(lambda c: c.data == 'view_all_buttons')\
    (view_all_buttons_in_button_group)
create_button_group = bot.callback_query_handler(lambda c: c.data == 'create_new_group')(create_button_group)


select_buttongroup_in_create_group = bot.callback_query_handler(
    lambda c: c.data.startswith('select_parent_in_create_group_'))(select_buttongroup_in_create_group)
select_buttongroup_in_create_button = bot.callback_query_handler\
    (lambda c: c.data.startswith('select_parent_in_button_'))(select_buttongroup_in_create_button)
select_parent_in_create_text = bot.callback_query_handler(lambda c: c.data.startswith('select_parent_in_text_'))\
    (select_parent_in_create_text)


select_button_group = bot.callback_query_handler(lambda c: c.data.startswith('select_group_'))(select_button_group)

view_all_buttons_for_text = bot.callback_query_handler(lambda c: c.data == 'view_all_buttons_for_text')\
    (view_all_buttons_for_text)

documents_admin_menu = bot.callback_query_handler(lambda c: c.data == 'documents_actions')(documents_admin_menu)


parsing = bot.callback_query_handler(lambda c: c.data.startswith('markup_choose_document_'))(parsing)


choose_default_user_values = bot.callback_query_handler(lambda c: c.data == "ChangeDefaultUserValue111")\
    (choose_default_user_values)
change_default_user_values = bot.callback_query_handler(lambda c: c.data.startswith("ChangeDefaultUserValue_"))\
    (change_default_user_value)

chat_with_ai = bot.message_handler(func=lambda message: True)(chat_with_ai)

add_text_to_file = bot.callback_query_handler(lambda c: c.data == 'create_new_text')(add_text_to_file)


long_message_get_send_option = bot.callback_query_handler(lambda c: c.data.startswith("lngmsg_"))\
    (long_message_get_send_option)
long_message_get_send_option_docs = bot.callback_query_handler(lambda c: c.data.startswith("documents_"))\
    (long_message_get_send_option_docs)


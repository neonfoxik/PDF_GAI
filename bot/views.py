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
upload_admin_menu = bot.callback_query_handler(lambda c: c.data == "upload_main")(upload_admin_menu)
users_action_main = bot.callback_query_handler(lambda c: c.data == "users_action")(users_action_main)
create_button = bot.callback_query_handler(lambda c: c.data == 'create_button')(add_button)
save_button = bot.callback_query_handler(lambda c: c.data == 'save_button')(save_button_to_file)
cancellation_button = bot.callback_query_handler(lambda c: c.data == 'cancellation')(cancellation_button)
change_documents = bot.callback_query_handler(lambda c: c.data == 'load_file')(change_documents)
choose_move = bot.callback_query_handler(lambda c: c.data.startswith('chsDoc'))(choose_move)
changing = bot.callback_query_handler(lambda c: c.data.startswith('document_'))(changing)
new_document = bot.callback_query_handler(lambda c: c.data == "create_new_document")(create_document)
select_txt_or_docx_in_view_button_group = bot.callback_query_handler\
    (lambda c: c.data == "select_txt_or_docx_in_view_button_group")(select_txt_or_docx_in_view_button_group)
view_button_group_in_select_txt = bot.callback_query_handler(lambda c: c.data == "view_button_group_in_select_txt")\
    (view_button_group_in_select_txt)
view_button_group_in_select_docx = bot.callback_query_handler(lambda c: c.data == "view_button_group_in_select_docx")\
    (view_button_group_in_select_docx)
is_sending_to_admin = bot.callback_query_handler(lambda c: c.data.startswith('confirm'))(is_sending_to_admin)
accept = bot.callback_query_handler(lambda c: c.data.startswith("accept"))(accept)
add_new_document = bot.callback_query_handler(lambda c: c.data == "add_new_doc")(add_new_document)

button_actions = bot.callback_query_handler(lambda c: c.data.startswith('list_button_'))(button_actions)
edit_button_callback_name = bot.callback_query_handler(lambda c: c.data.startswith('edit_name_')) \
    (edit_button_callback_name)

delete_button_from_file = bot.callback_query_handler(lambda c: c.data.startswith('delete_button_')) \
    (delete_button_from_file)
list_buttons = bot.callback_query_handler(lambda c: c.data == 'edit_buttons')(list_buttons)
edit_button_menu = bot.callback_query_handler(lambda c: c.data.startswith('edit_button_'))(edit_button_menu)

button_group_actions = bot.callback_query_handler(lambda c: c.data.startswith('list_group_'))(button_group_actions)
delete_group_from_file = bot.callback_query_handler(lambda c: c.data.startswith('delete_group_'))\
    (delete_group_from_file)
edit_group = bot.callback_query_handler(lambda c: c.data.startswith('edit_group_all_'))(edit_group)
edit_group_name = bot.callback_query_handler(lambda c: c.data.startswith('edit_group_name_'))(edit_group_name)
list_button_group = bot.callback_query_handler(lambda c: c.data == 'edit_group_button')(list_button_group)
analyze_and_fill_common_admin = bot.callback_query_handler(lambda c: c.data == 'upload_buttons_txt') \
    (analyze_and_fill_common_admin)
analyze_and_fill_common_admin_docx = bot.callback_query_handler(lambda c: c.data == 'upload_buttons_docx') \
    (analyze_and_fill_common_admin_docx)
main_menu = bot.callback_query_handler(lambda c: c.data == 'main_menu')(main_menu)

view_all_buttons_in_button_group = bot.callback_query_handler(lambda c: c.data == 'view_all_buttons') \
    (view_all_buttons_in_button_group)
create_button_group = bot.callback_query_handler(lambda c: c.data == 'create_new_group')(create_button_group)


select_buttongroup_in_create_group = bot.callback_query_handler(
    lambda c: c.data.startswith('select_parent_in_create_group_'))(select_buttongroup_in_create_group)
select_buttongroup_in_create_button = bot.callback_query_handler(lambda c: c.data.startswith('select_parent_in_button_'))\
    (select_buttongroup_in_create_button)
get_is_document_group = bot.callback_query_handler(lambda c: c.data.startswith('is_document_'))(get_is_document_group)
select_button_group = bot.callback_query_handler(lambda c: c.data.startswith('select_group_'))(select_button_group)

texts_admin_menu = bot.callback_query_handler(lambda c: c.data == 'texts_actions')(texts_admin_menu)
documents_admin_menu = bot.callback_query_handler(lambda c: c.data == 'documents_actions')(documents_admin_menu)
button_admin_menu = bot.callback_query_handler(lambda c: c.data == 'buttons_actions')(button_admin_menu)
chat_with_ai = bot.message_handler(func=lambda message: True)(chat_with_ai)

add_text_to_file = bot.callback_query_handler(lambda c: c.data == 'create_new_text')(add_text_to_file)


long_message_get_send_option = bot.callback_query_handler(lambda c: c.data.startswith("lngmsg_"))(long_message_get_send_option)
long_message_get_send_option_docs = bot.callback_query_handler(lambda c: c.data.startswith("documents_"))(long_message_get_send_option_docs)
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

"""SystemInlineKeyboards"""

MENU_PARS_BUTTON = InlineKeyboardMarkup()
menu = InlineKeyboardButton(text="В меню", callback_data="menu")
document_menu = InlineKeyboardButton(text="Отправить документ", callback_data="marckup_choose_document")
change_base_values  = InlineKeyboardButton(text="Изменить базовые значения", callback_data="ChangeDefaultUserValue111")
MENU_PARS_BUTTON.add(menu).add(document_menu).add(change_base_values)

UNIVERSAL_BUTTONS = InlineKeyboardMarkup()
back = InlineKeyboardButton(text="Назад в меню 🔙", callback_data="main_menu")
UNIVERSAL_BUTTONS.add(back)



ADMIN_BUTTONS_DOC = InlineKeyboardMarkup()
add_doc = InlineKeyboardButton(text="Создать документ", callback_data="add_new_doc")
load_file = InlineKeyboardButton(text="Редактировать документы", callback_data="load_file")
ADMIN_BUTTONS_DOC.add(add_doc).add(load_file)


CANCELBUTTON = InlineKeyboardMarkup()
cancellation = InlineKeyboardButton(text="Отмена", callback_data="cancellation")
CANCELBUTTON.add(cancellation)

LONGMESSAGE_BUTTONS = InlineKeyboardMarkup()
message = InlineKeyboardButton(text="Сообщениями", callback_data="lngmsg_msg")
documents = InlineKeyboardButton(text="Файлом", callback_data="lngmsg_docs")
LONGMESSAGE_BUTTONS.add(message, documents)

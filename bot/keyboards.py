from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

"""SystemInlineKeyboards"""

MENU_PARS_BUTTON = InlineKeyboardMarkup()
menu = InlineKeyboardButton(text="В меню", callback_data="menu")
document_menu = InlineKeyboardButton(text="Парсинг документов", callback_data="marckup_choose_document")
change_base_values  = InlineKeyboardButton(text="Изменить базовые значения", callback_data="ChangeDefaultUserValue111")
MENU_PARS_BUTTON.add(menu).add(document_menu).add(change_base_values)

UNIVERSAL_BUTTONS = InlineKeyboardMarkup()
back = InlineKeyboardButton(text="Назад в меню 🔙", callback_data="main_menu")
UNIVERSAL_BUTTONS.add(back)

SAVE_BUTTONS = InlineKeyboardMarkup()
save = InlineKeyboardButton(text="Сохранить кнопку", callback_data="save_button")
cancellation = InlineKeyboardButton(text="Отмена", callback_data="cancellation")
SAVE_BUTTONS.add(save).add(cancellation)

ADMIN_BUTTONS_MAIN = InlineKeyboardMarkup()
buttons_act = InlineKeyboardButton(text="Создать кнопку", callback_data="buttons_actions")
create_button_group = InlineKeyboardButton(text="Создать группу кнопок", callback_data="create_new_group")
documents_act = InlineKeyboardButton(text="Документы", callback_data="documents_actions")
texts_act = InlineKeyboardButton(text="Новый текст", callback_data="create_new_text")
upload = InlineKeyboardButton(text="Обновить кнопки", callback_data="upload_buttons_txt")
add_user = InlineKeyboardButton(text="Действия с пользователями", callback_data="users_action")
ADMIN_BUTTONS_MAIN.add(buttons_act).add(documents_act).add(texts_act).add(upload).add(add_user).add(create_button_group)


ADMIN_BUTTONS_DOC = InlineKeyboardMarkup()
add_doc = InlineKeyboardButton(text="Создать документ", callback_data="add_new_doc")
new_document = InlineKeyboardButton(text="Создать пустой документ", callback_data="create_new_document")
load_file = InlineKeyboardButton(text="Редактировать документы", callback_data="load_file")
admin_main_menu = InlineKeyboardButton(text="Вернуться в главное меню администратора", callback_data="admin_menu")
ADMIN_BUTTONS_DOC.add(new_document).add(load_file).add(admin_main_menu).add(add_doc)


CANCELBUTTON = InlineKeyboardMarkup()
cancellation = InlineKeyboardButton(text="Отмена", callback_data="cancellation")
CANCELBUTTON.add(cancellation)

LONGMESSAGE_BUTTONS = InlineKeyboardMarkup()
message = InlineKeyboardButton(text="Сообщениями", callback_data="lngmsg_msg")
documents = InlineKeyboardButton(text="Файлом", callback_data="lngmsg_docs")
LONGMESSAGE_BUTTONS.add(message, documents)

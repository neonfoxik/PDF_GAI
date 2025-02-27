from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

"""SystemInlineKeyboards"""
MENU_BUTTON = InlineKeyboardMarkup()
menu = InlineKeyboardButton(text="В меню", callback_data="menu")
document_menu = InlineKeyboardButton(text="Парсинг документов", callback_data="marckup_choose_document")
change_base_values  = InlineKeyboardButton(text="Изменить базовые значения", callback_data="ChangeDefaultUserValue111")

MENU_BUTTON.add(menu).add(document_menu).add(change_base_values)

UNIVERSAL_BUTTONS = InlineKeyboardMarkup()
back = InlineKeyboardButton(text="Назад в меню 🔙", callback_data="back")
UNIVERSAL_BUTTONS.add(back)

SAVE_BUTTONS = InlineKeyboardMarkup()
save = InlineKeyboardButton(text="Сохранить кнопку", callback_data="save_button")
cancellation = InlineKeyboardButton(text="Отмена", callback_data="cancellation")
SAVE_BUTTONS.add(save).add(cancellation)

ADMIN_BUTTONS_MAIN = InlineKeyboardMarkup()
buttons_act = InlineKeyboardButton(text="Действия с кнопками", callback_data="buttons_actions")
documents_act = InlineKeyboardButton(text="Документы", callback_data="documents_actions")
texts_act = InlineKeyboardButton(text="Тексты", callback_data="texts_actions")
upload_txt = InlineKeyboardButton(text="Обновить главное меню методички у пользователя", callback_data="upload_buttons_txt")
upload_docx = InlineKeyboardButton(text="Обновить главное меню документов у пользователя", callback_data="upload_buttons_docx")
ADMIN_BUTTONS_MAIN.add(buttons_act).add(documents_act).add(texts_act).add(upload_txt).add(upload_docx)

ADMIN_BUTTONS_BUTTON = InlineKeyboardMarkup()
create_button = InlineKeyboardButton(text="Создать кнопку", callback_data="create_button")
create_button_group = InlineKeyboardButton(text="Создать группу кнопку", callback_data="create_new_group")
edit_buttons = InlineKeyboardButton(text="Редактировать кнопки", callback_data="edit_buttons")
edit_button_group = InlineKeyboardButton(text="Редактировать группы кнопок", callback_data="edit_group_button")
admin_main_menu = InlineKeyboardButton(text="Вернуться в главное меню администратора", callback_data="admin_menu")
ADMIN_BUTTONS_BUTTON.add(create_button).add(edit_buttons).add(create_button_group).add(edit_button_group)\
    .add(admin_main_menu)

ADMIN_BUTTONS_DOC = InlineKeyboardMarkup()
add_doc = InlineKeyboardButton(text="Создать документ", callback_data="add_new_doc")
new_document = InlineKeyboardButton(text="Создать пустой документ", callback_data="create_new_document")
load_file = InlineKeyboardButton(text="Редактировать документы", callback_data="load_file")
admin_main_menu = InlineKeyboardButton(text="Вернуться в главное меню администратора", callback_data="admin_menu")
ADMIN_BUTTONS_DOC.add(new_document).add(load_file).add(admin_main_menu).add(add_doc)

ADMIN_BUTTONS_TXT = InlineKeyboardMarkup()
new_text = InlineKeyboardButton(text="Новый текст", callback_data="create_new_text")
edit_text = InlineKeyboardButton(text="Редактировать тексты", callback_data="edit_text")
admin_main_menu = InlineKeyboardButton(text="Вернуться в главное меню администратора", callback_data="admin_menu")
ADMIN_BUTTONS_TXT.add(new_text).add(load_file).add(admin_main_menu)


CANCELBUTTON = InlineKeyboardMarkup()
cancellation = InlineKeyboardButton(text="Отмена", callback_data="cancellation")
CANCELBUTTON.add(cancellation)

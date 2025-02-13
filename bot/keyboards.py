from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

"""SystemInlineKeyboards"""
MENU_BUTTON = InlineKeyboardMarkup()
menu = InlineKeyboardButton(text="В меню", callback_data="menu")
MENU_BUTTON.add(menu)

UNIVERSAL_BUTTONS = InlineKeyboardMarkup()
back = InlineKeyboardButton(text="Назад в меню 🔙", callback_data="back")
UNIVERSAL_BUTTONS.add(back)

SAVE_BUTTONS = InlineKeyboardMarkup()
save = InlineKeyboardButton(text="Сохранить кнопку", callback_data="save_button")
cancellation = InlineKeyboardButton(text="Отмена", callback_data="cancellation")
SAVE_BUTTONS.add(save).add(cancellation)

ADMIN_BUTTONS = InlineKeyboardMarkup()
create_button = InlineKeyboardButton(text="Создать кнопку", callback_data="create_button")
create_button_group = InlineKeyboardButton(text="Создать группу кнопку", callback_data="create_new_group")
edit_buttons = InlineKeyboardButton(text="Редактировать кнопки", callback_data="edit_buttons")
edit_button_group = InlineKeyboardButton(text="Редактировать группы кнопок", callback_data="edit_group_button")
new_document = InlineKeyboardButton(text="Создать пустой документ", callback_data="create_new_document")
load_file = InlineKeyboardButton(text="Редактировать документы", callback_data="load_file")
upload = InlineKeyboardButton(text="Обновить кнопки у пользователей", callback_data="upload_buttons")
ADMIN_BUTTONS.add(create_button).add(edit_buttons).add(load_file).add(edit_button_group).add(upload). \
    add(create_button_group).add(load_file).add(new_document)


CANCELBUTTON = InlineKeyboardMarkup()
cancellation = InlineKeyboardButton(text="Отмена", callback_data="cancellation")
CANCELBUTTON.add(cancellation)

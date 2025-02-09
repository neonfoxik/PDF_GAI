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

SAVE_BUTTON = InlineKeyboardMarkup()
save = InlineKeyboardButton(text="Сохранить кнопку", callback_data="save_button")
cancellation = InlineKeyboardButton(text="Отмена", callback_data="cancellation")
SAVE_BUTTON.add(save).add(cancellation)
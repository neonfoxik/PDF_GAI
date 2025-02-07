from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

"""InlineKeyboards"""
MENU_BUTTON = InlineKeyboardMarkup()
menu = InlineKeyboardButton(text="В меню", callback_data="menu")
MENU_BUTTON.add(menu)

UNIVERSAL_BUTTONS = InlineKeyboardMarkup()
back = InlineKeyboardButton(text="Назад в меню 🔙", callback_data="back")

UNIVERSAL_BUTTONS.add(back)

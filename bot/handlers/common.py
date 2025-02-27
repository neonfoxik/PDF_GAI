from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.models import User, Button, ButtonGroup
from bot.handlers.common_text import (
    main_menu_message
)
from bot.texts import FAQ, LC_TEXT


def start(message: Message) -> None:
    """Обработчик команды /start."""
    user_id = message.from_user.id

    user, created = User.objects.get_or_create(
        telegram_id=user_id,
        defaults={'name': message.from_user.first_name}
    )

    if user.has_plan:
        main_menu_message(message)
    else:
        buy_plan(message)


def help_(message: Message) -> None:
    """Обработчик команды /help."""
    bot.send_message(chat_id=message.chat.id, text=FAQ, parse_mode='Markdown')


def buy_plan(message):
    user_id = message.chat.id

    bot.send_message(user_id, text="Для использования этого бота необходимо скинуть X рублей по моему номеру телефона."
                                   "Когда оплатите, отправьте скрин в чат")
    bot.register_next_step_handler(message, confirmation_to_send_admin)


def confirmation_to_send_admin(message: Message) -> None:
    user_id = message.from_user.id
    keyboard = InlineKeyboardMarkup(row_width=2)
    yes_btn = InlineKeyboardButton(text="Да", callback_data=f"confirm_y_{message.id}")
    no_btn = InlineKeyboardButton(text="Нет", callback_data=f"confirm_n_{message.id}")
    keyboard.add(yes_btn, no_btn)
    bot.send_message(
        chat_id=user_id,
        reply_markup=keyboard,
        text="Вы уверенны что вы отправили чек и мы можем его проверить",
    )


def share_with_admin(msg_id: str, user_id: str):
    bot.forward_message(settings.OWNER_ID, user_id, msg_id)

    kb = InlineKeyboardMarkup()
    btn_accept = InlineKeyboardButton(text='Одобрить ✅', callback_data=f'accept_{user_id}')
    btn_reject = InlineKeyboardButton(text='Отказать ❌', callback_data=f'reject_{user_id}')

    kb.add(btn_accept).add(btn_reject)

    bot.send_message(text=f'Новая оплата!', chat_id=settings.OWNER_ID, reply_markup=kb)


def is_sending_to_admin(call: CallbackQuery) -> None:
    _, bool_, msg_id = call.data.split("_")
    bot.delete_message(message_id=call.message.message_id, chat_id=call.from_user.id)
    if bool_ == "y":
        share_with_admin(user_id=call.from_user.id, msg_id=msg_id)


def accept(call: CallbackQuery):
    _, user_id = call.data.split("_")
    user = User.objects.get(telegram_id=user_id)
    user.has_plan = True
    user.save()
    bot.send_message(user_id, text="Теперь вы можете пользоваться ботом")

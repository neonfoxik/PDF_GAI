from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from bot.keyboards import MENU_PARS_BUTTON
from bot.models import User, Button, ButtonGroup, UserTemplateVariable, Documents
from bot.handlers.common_text import (
    main_menu_message
)
from bot.texts import FAQ, LC_TEXT


def documents_main_menu(message: Message) -> None:
    documents = Documents.objects.all()
    markup = InlineKeyboardMarkup(row_width=2)
    for document in documents:
        button = InlineKeyboardButton(document.name, callback_data=f"doc_sender_{document.name}")
        markup.add(button)
    bot.send_message(message.chat.id, "Документы", reply_markup=markup)

def documents_sender(callback_query: CallbackQuery) -> None:
    doc_name = callback_query.data.split('_')[2]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="В меню", callback_data="menu"))
    keyboard.add(InlineKeyboardButton(text="Парсинг документов", callback_data=f"markup_choose_document_{doc_name}"))
    keyboard.add(InlineKeyboardButton(text="Изменить записанные значения переменных документа",
                                      callback_data="ChangeDefaultUserValue111"))
    try:
        document = Documents.objects.get(name=doc_name)
        bot.send_message(callback_query.message.chat.id,
                         "Вы можете скачать документ так или выбрать над ним действие ниже",
                         reply_markup=keyboard)
    except Documents.DoesNotExist:
        bot.send_message(callback_query.message.chat.id, "Документ не найден.")
    except Exception as e:
        logger.error(f"Ошибка при отправке документа: {e}")
        bot.send_message(callback_query.message.chat.id, "Произошла ошибка при отправке документа.")

def choose_default_user_values(callback_query: CallbackQuery) -> None:
    user_id = callback_query.from_user.id
    user = User.objects.get(telegram_id=user_id)
    user_variables = UserTemplateVariable.objects.filter(user=user)
    markup = InlineKeyboardMarkup(row_width=2)

    for variable in user_variables:
        button = InlineKeyboardButton(variable.display_name, callback_data=f"ChangeDefaultUserValue_{variable.template_field}")
        markup.add(button)
    bot.send_message(user_id, "Выберете переменную которую хотите изменить", reply_markup=markup)


def change_default_user_value(callback_query: CallbackQuery) -> None:
    _, template_field = callback_query.data.split("_")
    user = User.objects.get(telegram_id=callback_query.from_user.id)
    user_variables = UserTemplateVariable.objects.filter(user=user).filter(template_field=template_field).first()
    bot.send_message(user.telegram_id, f"Выберете значение для {user_variables.display_name}")
    bot.register_next_step_handler(callback_query.message, change_default_user_value_step, template_field)


def change_default_user_value_step(message: Message, template_field) -> None:
    user = User.objects.get(telegram_id=message.from_user.id)
    user_variables = UserTemplateVariable.objects.filter(user=user).filter(template_field=template_field).first()
    user_variables.value = message.text
    user_variables.save()
    bot.send_message(user.telegram_id, "Значение изменено")

def start(message: Message) -> None:
    """Обработчик команды /start."""
    try:
        user_id = message.from_user.id

        user, created = User.objects.get_or_create(
            telegram_id=user_id,
            defaults={'name': message.from_user.first_name}
        )

        if user.has_plan:
            main_menu_message(message)
        else:
            buy_plan(message)
    except Exception as e:
        logger.error(f"Ошибка в обработчике start: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при обработке команды")


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
    yes_btn = InlineKeyboardButton(text="Да", callback_data=f"setbuy_y_{message.id}")
    no_btn = InlineKeyboardButton(text="Нет", callback_data=f"setbuy_n_{message.id}")
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

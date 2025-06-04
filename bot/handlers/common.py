from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from bot.keyboards import MENU_PARS_BUTTON
from bot.models import User, UserTemplateVariable, Documents, Content, Button
from bot.texts import FAQ


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
        bot.send_message(message.chat.id, f"Произошла ошибка при обработке команды {e}")



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


def main_menu_message(message: Message) -> None:
    """Отправка главного меню с кнопками без родителя"""
    buttons = Button.objects.filter(parent__isnull=True)
    if not buttons.exists():
        bot.send_message(message.chat.id, "В главном меню нет кнопок. Пожалуйста, обратитесь к администратору.")
        return
        
    markup = InlineKeyboardMarkup(row_width=1)
    for button in buttons:
        markup.add(InlineKeyboardButton(text=button.text, callback_data=f"bim_{button.button_id}"))
    
    # Отправляем приветственное сообщение
    welcome_text = "Добро пожаловать! Выберите нужный раздел:"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


def main_menu_call(callback_query: CallbackQuery) -> None:
    buttons = Button.objects.filter(parent__isnull=True)
    markup = InlineKeyboardMarkup(row_width=1)
    
    # Добавляем кнопки главного меню
    for button in buttons:
        markup.add(InlineKeyboardButton(text=button.text, callback_data=f"bim_{button.button_id}"))
    
    welcome_text = "Добро пожаловать! Выберите нужный раздел:"
    bot.edit_message_text(chat_id=callback_query.from_user.id, 
                         text=welcome_text,
                         reply_markup=markup, 
                         message_id=callback_query.message.message_id)


def next_button_menu(callback_query: CallbackQuery) -> None:
    try:
        button_id = int(callback_query.data.split("_")[-1])
        button = Button.objects.filter(button_id=button_id).first()
        if not button:
            bot.send_message(callback_query.message.chat.id, "Кнопка не найдена. Пожалуйста, обратитесь к администратору.")
            return

        child_content = button.child
        if not child_content:
            bot.send_message(callback_query.message.chat.id, "Для этой кнопки не настроен контент. Пожалуйста, обратитесь к администратору.")
            return

        # Удаляем сообщение, на котором была нажата кнопка
        bot.delete_message(message_id=callback_query.message.message_id, chat_id=callback_query.from_user.id)

        # Разбиваем длинный текст на части по 4096 символов
        text_parts = [child_content.content_text[i:i+4096] for i in range(0, len(child_content.content_text), 4096)]

        # Получаем все кнопки для текущего контента
        child_content_buttons = Button.objects.filter(parent=child_content)

        # Создаем разметку с кнопками
        markup = InlineKeyboardMarkup(row_width=1)

        # Добавляем кнопки контента
        for child_button in child_content_buttons:
            markup.add(InlineKeyboardButton(text=child_button.text, callback_data=f"bim_{child_button.button_id}"))

        # Добавляем кнопку "Назад" если есть родитель
        if button.parent:
            markup.add(InlineKeyboardButton(text="◀️ Назад", callback_data=f"back_btn_{button.button_id}"))

        # Всегда добавляем кнопку "В главное меню"
        markup.add(InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu_call"))

        # Отправляем части текста. Кнопки прикрепляем только к последней части.
        for i, part in enumerate(text_parts):
            if i == len(text_parts) - 1:
                bot.send_message(chat_id=callback_query.from_user.id, text=part, reply_markup=markup)
            else:
                bot.send_message(chat_id=callback_query.from_user.id, text=part)

    except Exception as e:
        logger.error(f"Ошибка в next_button_menu: {e}")
        bot.send_message(callback_query.message.chat.id, f"Произошла ошибка при обработке запроса: {e}")


def old_button_menu(callback_query: CallbackQuery) -> None:
    try:
        button_id = int(callback_query.data.split("_")[-1])
        current_button = Button.objects.get(button_id=button_id)
        
        # Если у текущей кнопки нет родителя, возвращаемся в главное меню, удаляя предыдущее сообщение
        if not current_button.parent:
            main_menu_call(callback_query)
            return
        
        # Удаляем сообщение, на котором была нажата кнопка
        bot.delete_message(message_id=callback_query.message.message_id, chat_id=callback_query.from_user.id)

        # Получаем родительский контент
        parent_content = current_button.parent
        
        # Получаем все кнопки для родительского контента
        buttons = Button.objects.filter(parent=parent_content)
        
        # Создаем разметку
        markup = InlineKeyboardMarkup(row_width=1)
        
        # Добавляем кнопки контента
        for btn in buttons:
            markup.add(InlineKeyboardButton(text=btn.text, callback_data=f"bim_{btn.button_id}"))
        
        # Добавляем кнопку "Назад" если у родительского контента есть свой родитель
        parent_button = Button.objects.filter(child=parent_content).first()
        if parent_button:
            markup.add(InlineKeyboardButton(text="◀️ Назад", callback_data=f"back_btn_{parent_button.button_id}"))
        else:
            # Если нет родительской кнопки, добавляем кнопку "Назад" в главное меню
            markup.add(InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu_call"))
        
        # Всегда добавляем кнопку "В главное меню"
        markup.add(InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu_call"))
        
        # Разбиваем длинный текст на части
        text_parts = [parent_content.content_text[i:i+4096] for i in range(0, len(parent_content.content_text), 4096)]
        
        # Отправляем части текста. Кнопки прикрепляем только к последней части.
        for i, part in enumerate(text_parts):
            if i == len(text_parts) - 1:
                bot.send_message(chat_id=callback_query.from_user.id, text=part, reply_markup=markup)
            else:
                bot.send_message(chat_id=callback_query.from_user.id, text=part)

    except Exception as e:
        logger.error(f"Ошибка в old_button_menu: {e}")
        bot.send_message(callback_query.message.chat.id, f"Произошла ошибка при обработке запроса: {e}")


def help_(message: Message) -> None:
    """Обработчик команды /help."""
    bot.send_message(chat_id=message.chat.id, text=FAQ, parse_mode='Markdown')


def documents_main_menu(message: Message) -> None:
    documents = Documents.objects.all()
    markup = InlineKeyboardMarkup(row_width=2)
    for document in documents:
        button = InlineKeyboardButton(document.name, callback_data=f"doc_sender_{document.name}")
        markup.add(button)
    bot.send_message(message.chat.id, "Документы", reply_markup=markup)

def documents_menu_call(call: CallbackQuery) -> None:
    documents = Documents.objects.all()
    markup = InlineKeyboardMarkup(row_width=2)
    for document in documents:
        button = InlineKeyboardButton(document.name, callback_data=f"doc_sender_{document.name}")
        markup.add(button)
    bot.edit_message_text(chat_id=call.message.chat.id, text="Документы", reply_markup=markup
                          , message_id=call.message.message_id)



def documents_sender(callback_query: CallbackQuery) -> None:
    doc_name = callback_query.data.split('_')[2]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="В меню", callback_data="documents_menu_call"))
    keyboard.add(InlineKeyboardButton(text="Парсинг документов", callback_data=f"markup_choose_document_{doc_name}"))
    keyboard.add(InlineKeyboardButton(text="Изменить записанные значения переменных документа",
                                      callback_data="ChangeDefaultUserValue111"))
    try:
        bot.edit_message_text(chat_id=callback_query.message.chat.id,
                         text="Вы можете скачать документ так или выбрать над ним действие ниже",
                         reply_markup=keyboard, message_id=callback_query.message.message_id)
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
        button = InlineKeyboardButton(variable.display_name,
                                      callback_data=f"ChangeDefaultUserValue__{variable.template_field}")
        markup.add(button)
    bot.send_message(user_id, "Выберете переменную которую хотите изменить", reply_markup=markup)


def change_default_user_value(callback_query: CallbackQuery) -> None:
    data_parts = callback_query.data.split("__")
    print(data_parts)
    if len(data_parts) < 2:
        bot.send_message(callback_query.message.chat.id, "Ошибка: неверные данные.")
        return
    template_field = data_parts[1]
    user = User.objects.get(telegram_id=callback_query.from_user.id)
    user_variables = UserTemplateVariable.objects.filter(user=user, template_field=template_field).first()
    
    if user_variables is None:
        bot.send_message(callback_query.message.chat.id, "Ошибка: переменная не найдена.")
        return

    bot.send_message(user.telegram_id, f"Выберете значение для {user_variables.display_name}")
    bot.register_next_step_handler(callback_query.message, change_default_user_value_step, template_field)


def change_default_user_value_step(message: Message, template_field) -> None:
    user = User.objects.get(telegram_id=message.from_user.id)
    user_variables = UserTemplateVariable.objects.filter(user=user, template_field=template_field).first()
    
    if user_variables is None:
        bot.send_message(message.chat.id, "Ошибка: переменная не найдена.")
        return

    user_variables.value = message.text
    user_variables.save()
    bot.send_message(user.telegram_id, "Значение изменено")

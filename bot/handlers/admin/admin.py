from functools import wraps
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot, logger
from bot.models import User, Button, ButtonGroup, Texts, Documents
from bot.keyboards import SAVE_BUTTONS, ADMIN_BUTTONS_MAIN, CANCELBUTTON, ADMIN_BUTTONS_DOC

button_data = {}
button_group_data = {}
texts_data = {}

class ButtonState:
    def __init__(self):
        self._is_create_button = False
        
    @property
    def is_create_button(self):
        return self._is_create_button
        
    @is_create_button.setter 
    def is_create_button(self, value):
        self._is_create_button = value

button_state = ButtonState()


def admin_permission(func):
    """
    Проверка прав администратора для доступа к функции.
    """

    @wraps(func)
    def wrapped(message: Message) -> None:
        user_id = message.from_user.id
        logger.info(f'Попытка отправки сообщения пользователю с ID: {user_id}')  # Логирование ID пользователя
        try:
            user = User.objects.get(telegram_id=user_id)
        except User.DoesNotExist:
            bot.send_message(user_id, '⛔ Пользователь не найден в системе')
            logger.warning(f'Пользователь с ID {user_id} не найден')
            return
        if not user.is_admin:
            bot.send_message(user_id, '⛔ У вас нет администраторского доступа')
            logger.warning(f'Попытка доступа к админ панели от {user_id}')
            return
        return func(message)

    return wrapped


def validate_user_message(message: Message) -> None:
    if message.text and len(message.text) > 0 and message.text.isalnum():  # Проверка на наличие специальных символов
        return message
    else:
        bot.send_message(message.chat.id, 'Название содержало некорректные символы, измените его',
                         reply_markup=ADMIN_BUTTONS_MAIN)
        return None

def validate_user_call(callback_query: CallbackQuery) -> None:
    if callback_query.message.text and len(callback_query.message.text) > 0 and callback_query.message.text.isalnum():  # Проверка на наличие специальных символов
        return callback_query.message
    else:
        bot.send_message(callback_query.message.chat.id, 'Название содержало некорректные символы, измените его',
                         reply_markup=ADMIN_BUTTONS_MAIN)
        return None


"""админ панель"""
@admin_permission
def admin_menu_call(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    try:
        bot.send_message(callback_query.message.chat.id, 'Главное меню админа', reply_markup=ADMIN_BUTTONS_MAIN)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в admin_menu: {e}')


@admin_permission
def admin_menu(message: Message) -> None:
    try:
        bot.send_message(message.chat.id, 'Главное меню админа', reply_markup=ADMIN_BUTTONS_MAIN)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в admin_menu: {e}')


@admin_permission
def documents_admin_menu(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    try:
        bot.send_message(callback_query.message.chat.id, 'Документы', reply_markup=ADMIN_BUTTONS_DOC)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в documents_admin_menu: {e}')


#дописать функцию
@admin_permission
def users_action_main(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    keyboards = InlineKeyboardMarkup()
    try:
        bot.send_message(callback_query.message.chat.id, 'Выберите действие', reply_markup=keyboards)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в texts_admin_menu: {e}')


"""создание групп кнопок"""


@admin_permission
def get_or_create_button_group_name(callback_query: CallbackQuery) -> None:
    try:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text='Создать новую группу', callback_data='create_new_group'))
        keyboard.add(InlineKeyboardButton(text="Просмотреть существующие группы кнопок",
                                          callback_data="select_txt_or_docx_in_view_button_group"))
        keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancellation"))
        bot.send_message(callback_query.message.chat.id,
                         'Выберите существующую группу или создайте новую, группу кнопок можно всегда изменить:',
                         reply_markup=keyboard)
    except Exception as e:
        logger.error(f'Ошибка при получении групп кнопок: {e}')
        bot.send_message(callback_query.message.chat.id, 'Произошла ошибка при получении групп кнопок')


@admin_permission
def view_button_group_in_select_txt(callback_query: CallbackQuery) -> None:
    button_groups = ButtonGroup.objects.filter(is_document=False)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='create_button'))
    if button_groups.exists():
        for group in button_groups:
            keyboard.add(InlineKeyboardButton(text=group.name, callback_data=f'select_group_{group.name}'))
        try:
            bot.send_message(callback_query.message.chat.id, 'Выберите группу кнопок к которой '
                                                             'будет принадлежать ваша кнопка', reply_markup=keyboard)
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в view_button_group_in_select: {e}')

    else:
        try:
            bot.send_message(callback_query.message.chat.id, 'Нет доступных групп, создайте новую группу кнопок.')
            bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
            msg = bot.send_message(callback_query.message.chat.id, 'Укажите название группы кнопок английскими буквами',
                                   reply_markup=CANCELBUTTON)
            bot.register_next_step_handler(msg, get_group_name)
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в view_button_group_in_select: {e}')


@admin_permission
def create_button_group(callback_query: CallbackQuery) -> None:
    try:
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        msg = bot.send_message(callback_query.message.chat.id, 'Укажите название группы кнопок английскими буквами',
                               reply_markup=CANCELBUTTON)
        bot.register_next_step_handler(msg, get_group_name)
    except Exception as e:
        logger.error(f'Ошибка при создании группы кнопок: {e}')


@admin_permission
def get_group_name(message: Message) -> None:
    validated_message = validate_user_message(message)
    if not validated_message:
        return
    button_group_data['group_name'] = validated_message.text
    all_buttons = Button.objects.all()
    all_groups = ButtonGroup.objects.all()
    if all_groups.exists():
        if all_buttons.exists():
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text="Просмотреть все кнопки", callback_data="view_all_buttons"))
            keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancellation"))
            try:
                bot.send_message(message.chat.id,
                                'Выберите способ указания родительской кнопки, то есть '
                                'кнопки после нажатия на которую будет открываться меню с этими кнопками',
                                reply_markup=keyboard)
            except Exception as e:
                logger.error(f'Ошибка при отправке сообщения в get_is_document_group: {e}')
        else:
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text="Создать кнопку к существующей группе",
                                              callback_data="select_txt_or_docx_in_view_button_group"))
            keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancellation"))
            bot.send_message(message.chat.id,
                             'У вас нет зарегестрированых кнопок создайте их ниже',
                             reply_markup=keyboard)
    else:
        try:
            bot.send_message(message.chat.id,
                                'У вас нет зарегистрированных групп кнопок: группе кнопок будет присвоено значение '
                                'Главное меню')
            group_name = button_group_data.get('group_name')
            button_group, created = ButtonGroup.objects.get_or_create(
                name=group_name,
                parent_button="main_menu",
                is_main_group=True
            )
            button_group.save()
            if button_state.is_create_button:
                button_data['group_name'] = group_name
                msg = bot.send_message(message.chat.id,
                                        'Укажите название кнопки английскими буквами',
                                        reply_markup=CANCELBUTTON)
                bot.register_next_step_handler(msg, get_button_name)
            else:
                bot.send_message(message.chat.id, 'Главное меню админа',
                                        reply_markup=ADMIN_BUTTONS_MAIN)
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в get_is_document_group: {e}')

@admin_permission
def view_all_buttons_in_button_group(callback_query: CallbackQuery) -> None:
    try:
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        all_buttons = Button.objects.all()
        parent_buttons_groups = ButtonGroup.objects.values_list('parent_button', flat=True)
        parent_buttons_texts = Texts.objects.values_list('parent_button', flat=True)
        all_parent_buttons = set(list(parent_buttons_groups) + list(parent_buttons_texts))
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancellation"))
        if button_state.is_create_button == True:
            if all_buttons.exists():
                for button in all_buttons:
                    if button.button_name not in all_parent_buttons:
                        keyboard.add(InlineKeyboardButton(
                            text=f"{button.button_name} ({button.button_text})",
                            callback_data=f"select_parent_in_button_{button.button_name}"
                        ))
            else:
                keyboard.add(InlineKeyboardButton(text="Создать новую кнопку", callback_data="create_button"))
        else:
            if all_buttons.exists():
                for button in all_buttons:
                    if button.button_name not in all_parent_buttons:
                        keyboard.add(InlineKeyboardButton(
                            text=f"{button.button_name} ({button.button_text})",
                            callback_data=f"select_parent_in_create_group_{button.button_name}"
                        ))
            else:
                keyboard.add(InlineKeyboardButton(text="Создать новую кнопку", callback_data="create_button"))
        try:
            bot.send_message(callback_query.message.chat.id,
                             f'Выберите кнопку которая будет родительской:{button_state.is_create_button}',
                             reply_markup=keyboard)
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в view_all_buttons_in_button_group: {e}')
    except Exception as e:
        logger.error(f'Ошибка при получении списка кнопок: {e}')
        bot.send_message(callback_query.message.chat.id, 'Произошла ошибка при получении списка кнопок')

@admin_permission
def select_buttongroup_in_create_group(callback_query: CallbackQuery) -> None:
    parent_name = callback_query.data.split('_')[5]
    group_name = button_group_data.get('group_name')
    button_group, created = ButtonGroup.objects.get_or_create(name=group_name, parent_button=parent_name,
                                                              is_main_group=False)
    button_group.save()
    try:
        bot.send_message(callback_query.message.chat.id, 'Группа кнопок успешно создана Меню админки',
                         reply_markup=ADMIN_BUTTONS_MAIN)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в select_buttongroup_increategroup: {e}')


@admin_permission
def select_buttongroup_in_create_button(callback_query: CallbackQuery) -> None:
    parent_name = callback_query.data.split('_')[4]
    group_name = button_group_data.get('group_name')
    button_group, created = ButtonGroup.objects.get_or_create(name=group_name, parent_button=parent_name,
                                                              is_main_group=False)
    button_group.save()
    button_data['group_name'] = group_name
    msg = bot.send_message(callback_query.message.chat.id, 'Укажите название кнопки английскими буквами',
                           reply_markup=CANCELBUTTON)
    bot.register_next_step_handler(msg, get_button_name)


"""Добавление кнопки"""
@admin_permission
def add_button(callback_query: CallbackQuery) -> None:
    button_state.is_create_button = True
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    get_or_create_button_group_name(callback_query)



@admin_permission
def select_button_group(callback_query: CallbackQuery) -> None:
    group_name = callback_query.data.split('_')[2]
    button_data['group_name'] = group_name
    msg = bot.send_message(callback_query.message.chat.id, 'Укажите название кнопки английскими буквами',
                           reply_markup=CANCELBUTTON)
    bot.register_next_step_handler(msg, get_button_name)

@admin_permission
def select_button_group_message(message: Message) -> None:
    msg = bot.send_message(message.chat.id, 'Укажите название кнопки английскими буквами', reply_markup=CANCELBUTTON)
    bot.register_next_step_handler(msg, get_button_name)

@admin_permission
def get_button_name(message: Message) -> None:
    validated_message = validate_user_message(message)
    if not validated_message:
        return
        
    button_data['name'] = validated_message.text
    msg = bot.send_message(message.chat.id, 'Укажите текст кнопки', reply_markup=CANCELBUTTON)
    bot.register_next_step_handler(msg, get_button_text)

@admin_permission
def get_button_text(message: Message) -> None:
    validated_message = validate_user_message(message)
    if not validated_message:
        return
        
    button_data['text'] = validated_message.text
    try:
        bot.send_message(message.chat.id, 'Хотите ли вы подтвердить создание кнопки?', reply_markup=SAVE_BUTTONS)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в get_button_text: {e}')

@admin_permission
def cancellation_button(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    try:
        bot.send_message(callback_query.message.chat.id, 'Действие отменено', reply_markup=ADMIN_BUTTONS_MAIN)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в cancellation_button: {e}')

@admin_permission
def save_button_to_file(callback_query: CallbackQuery) -> None:
    button_state.is_create_button = False
    group_name = button_data.get('group_name')
    name = button_data.get('name')
    text = button_data.get('text')
    new_button = Button(button_name=name, button_group=group_name, button_text=text)
    new_button.save()
    bot.answer_callback_query(callback_query.id, "Кнопка успешно создана!")
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    try:
        bot.send_message(callback_query.message.chat.id, 'Меню админки', reply_markup=ADMIN_BUTTONS_MAIN)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в save_button_to_file: {e}')


# Добавление текстов

@admin_permission
def add_text_to_file(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    msg = bot.send_message(callback_query.message.chat.id, 'Введите имя текста:')
    bot.register_next_step_handler(msg, choose_parent_button_for_text)


@admin_permission
def choose_parent_button_for_text(message: Message) -> None:
    texts_data['text_name'] = message.text
    all_buttons = Button.objects.all()
    if all_buttons.exists():
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="Просмотреть все кнопки", callback_data="view_all_buttons_for_text"))
        keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancellation"))
        try:
            bot.send_message(message.chat.id, 'Выберите способ указания родительской кнопки тоесть кнопки после'
                                              f' нажатия на которую будет открываться меню с этими кнопками ',
                             reply_markup=keyboard)
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в get_group_name: {e}')
    else:
        bot.send_message(message.chat.id, 'У вас нерт зарегестрированных кнопок создайте хотя бы одну',
                         reply_markup=ADMIN_BUTTONS_MAIN)

@admin_permission
def view_all_buttons_for_text(callback: CallbackQuery) -> None:
    try:
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        parent_buttons_groups = ButtonGroup.objects.values_list('parent_button', flat=True)
        parent_buttons_texts = Texts.objects.values_list('parent_button', flat=True)
        buttons = Button.objects.exclude(
            button_name__in=list(parent_buttons_groups) + list(parent_buttons_texts)
        )

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancellation"))
        if buttons.exists():
            for button in buttons:
                keyboard.add(InlineKeyboardButton(
                    text=f"{button.button_name} ({button.button_text})",
                    callback_data=f"select_parent_in_text_{button.button_name}"
                ))
        else:
            keyboard.add(InlineKeyboardButton(text="Создать новую кнопку", callback_data="create_button"))
            
        try:
            bot.send_message(callback.message.chat.id,
                           'Выберите кнопку которая будет родительской:',
                           reply_markup=keyboard)
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в view_all_buttons_in_button_group: {e}')
    except Exception as e:
        logger.error(f'Ошибка при получении списка кнопок: {e}')
        bot.send_message(callback.message.chat.id, 'Произошла ошибка при получении списка кнопок')


@admin_permission
def select_parent_in_create_text(callback_query: CallbackQuery) -> None:
    parent_name = callback_query.data.split('_')[4]
    texts_data['text_parent_name'] = parent_name
    msg = bot.send_message(callback_query.message.chat.id, 'Введите текст который будет высвечиваться пользователю')
    bot.register_next_step_handler(msg, get_text_content)

@admin_permission
def get_text_content(message: Message) -> None:
    text_content = message.text
    text_name = texts_data.get('text_name')
    parent = texts_data.get("text_parent_name")
    try:
        new_text = Texts(name_txt=text_name, txt_text=text_content, parent_button=parent)
        new_text.save()
        bot.send_message(message.chat.id, f'Текст "{text_name}" успешно добавлен!', reply_markup=ADMIN_BUTTONS_MAIN)
    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка при добавлении текста')
        logger.error(f'Ошибка при добавлении текста: {e}')

@admin_permission
def edit_text_main(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    text_name = callback_query.data.split('_')[3]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="удалить текст", callback_data=f"delete_text_{text_name}"))
    keyboard.add(InlineKeyboardButton(text="редактировать текст текста", callback_data=f"edit_text_text_{text_name}"))
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancellation"))
    bot.send_message(callback_query.message.chat.id, "Выберите действие", reply_markup=keyboard)

#удаление текстов
@admin_permission
def delete_text(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    text_name = callback_query.data.split('_')[2]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Да, удалить", callback_data=f"confirm_delete_text_{text_name}"))
    keyboard.add(InlineKeyboardButton(text="Нет, отмена", callback_data="cancellation"))
    try:
        bot.send_message(
            callback_query.message.chat.id,
            f'Вы уверены что хотите удалить текст "{text_name}"?',
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Ошибка при удалении текста: {e}")
        bot.send_message(callback_query.message.chat.id, "Произошла ошибка при удалении текста")
@admin_permission
def confirm_delete_text(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    text_name = callback_query.data.split('_')[3]
    try:
        text = Texts.objects.filter(name_txt=text_name).first()
        text.delete()
        bot.send_message(
            callback_query.message.chat.id,
            f'Текст "{text_name}" успешно удален!',
            reply_markup=ADMIN_BUTTONS_MAIN
        )
    except Exception as e:
        logger.error(f"Ошибка при удалении текста: {e}")
        bot.send_message(
            callback_query.message.chat.id,
            "Произошла ошибка при удалении текста"
        )

#редактирование текста
@admin_permission
def edit_text_text(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    text_name = callback_query.data.split('_')[3]
    texts_data['text_name'] = text_name
    try:
        bot.send_message(
            callback_query.message.chat.id,
            f'Введите новый текст для текста "{text_name}":'
        )
        bot.register_next_step_handler(callback_query.message, process_new_text_text)
    except Exception as e:
        logger.error(f"Ошибка при редактировании имени текста: {e}")
        bot.send_message(callback_query.message.chat.id, "Произошла ошибка при редактировании имени текста")

@admin_permission 
def process_new_text_text(message: Message) -> None:
    bot.delete_message(message.chat.id, message.message_id)
    new_text = message.text
    old_text_name = texts_data.get('text_name')
    try:
        text = Texts.objects.filter(name_txt=old_text_name).first()
        text.txt_text = new_text
        text.save()
        bot.send_message(
            message.chat.id,
            f'Текст текста успешно изменено с "{old_text_name}" на "{new_text}"!',
            reply_markup=ADMIN_BUTTONS_MAIN
        )
    except Exception as e:
        logger.error(f"Ошибка при сохранении нового имени текста: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при сохранении нового имени текста")

@admin_permission
def edit_button_main(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    button_name = callback_query.data.split('_')[3]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="удалить кнопку", callback_data=f"delete_button_{button_name}"))
    keyboard.add(InlineKeyboardButton(text="редактировать текст кнопки", callback_data=f"edit_button_text_{button_name}"))
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancellation"))
    bot.send_message(callback_query.message.chat.id, f"Выберите действие над кнопкой {button_name}", reply_markup=keyboard)

#удаление кнопок
@admin_permission
def delete_button(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    button_name = callback_query.data.split('_')[2]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Да, удалить", callback_data=f"confirm_delete_button_{button_name}"))
    keyboard.add(InlineKeyboardButton(text="Нет, отмена", callback_data="cancellation"))
    try:
        bot.send_message(
            callback_query.message.chat.id,
            f'Вы уверены что хотите удалить кнопку "{button_name}"?',
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Ошибка при удалении кнопки: {e}")
        bot.send_message(callback_query.message.chat.id, "Произошла ошибка при удалении кнопки")

@admin_permission
def confirm_delete_button(callback_query: CallbackQuery) -> None:
    try:
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        button_name = callback_query.data.split('_')[3]
        button = Button.objects.filter(button_name=button_name).first()
        
        # Проверяем использование кнопки как родительской
        texts_using_button = Texts.objects.filter(parent_button=button_name).exists()
        button_groups_using_button = ButtonGroup.objects.filter(parent_button=button_name).exists()

        if texts_using_button or button_groups_using_button:
            bot.send_message(
                callback_query.message.chat.id,
                "Невозможно удалить кнопку, так как она используется как родительская для других объектов",
                reply_markup=ADMIN_BUTTONS_MAIN
            )
            return

        if button:
            button.delete()
            bot.send_message(
                callback_query.message.chat.id,
                f'Кнопка "{button_name}" успешно удалена!',
                reply_markup=ADMIN_BUTTONS_MAIN
            )
        else:
            bot.send_message(
                callback_query.message.chat.id,
                "Кнопка не найдена"
            )
    except Exception as e:
        logger.error(f"Ошибка при удалении кнопки: {e}")
        bot.send_message(
            callback_query.message.chat.id,
            "Произошла ошибка при удалении кнопки"
        )


#редактирование кнопки
@admin_permission
def edit_button_text(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    button_name = callback_query.data.split('_')[3]
    try:
        bot.send_message(
            callback_query.message.chat.id,
            f'Введите новый текст для кнопки "{button_name}":'
        )
        button_data['old_name'] = button_name
        bot.register_next_step_handler(callback_query.message, process_new_button_text)
    except Exception as e:
        logger.error(f"Ошибка при редактировании текста кнопки: {e}")
        bot.send_message(callback_query.message.chat.id, "Произошла ошибка при редактировании текста кнопки")

@admin_permission 
def process_new_button_text(message: Message) -> None:
    bot.delete_message(message.chat.id, message.message_id)
    new_button_text = message.text
    old_button_name = button_data.get('old_name')
    try:
        button = Button.objects.filter(button_name=old_button_name).first()
        if button:
            button.button_text = new_button_text
            button.save()
            bot.send_message(
                message.chat.id,
                f'Текст кнопки успешно изменен!',
                reply_markup=ADMIN_BUTTONS_MAIN
            )
        else:
            bot.send_message(message.chat.id, "Кнопка не найдена")
    except Exception as e:
        logger.error(f"Ошибка при сохранении нового текста кнопки: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при сохранении нового текста кнопки")


@admin_permission
def delete_button_group(callback_query: CallbackQuery) -> None:
    group_name = callback_query.data.split('_')[3]
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Да, удалить", callback_data=f"confirm_delete_group_{group_name}"))
    keyboard.add(InlineKeyboardButton(text="Нет, отмена", callback_data="cancellation"))
    try:
        bot.send_message(
            callback_query.message.chat.id,
            f'Вы уверены что хотите удалить группу "{group_name}"?',
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Ошибка при удалении группы: {e}")
        bot.send_message(callback_query.message.chat.id, "Произошла ошибка при удалении группы")


@admin_permission
def confirm_delete_group(callback_query: CallbackQuery) -> None:
    try:
        group_name = callback_query.data.split('_')[3]
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        group = ButtonGroup.objects.filter(name=group_name).first()
        if group:
            group.delete()
            bot.send_message(
                callback_query.message.chat.id,
                f'Группа "{group_name}" успешно удалена!',
                reply_markup=ADMIN_BUTTONS_MAIN
            )
        else:
            bot.send_message(
                callback_query.message.chat.id,
                "Группа не найдена"
            )
    except Exception as e:
        logger.error(f"Ошибка при удалении группы: {e}")
        bot.send_message(
            callback_query.message.chat.id,
            "Произошла ошибка при удалении группы"
        )


#Обновление скриптов
@admin_permission
def analyze_and_fill_common_admin(callback_query: CallbackQuery) -> None:
    """
    Анализирует базу данных и создает файл common_admin.py с обработчиками для всех кнопок
    """
    common_admin_template = """from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message, 
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from bot.models import User, Button, ButtonGroup, Texts
from bot.keyboards import UNIVERSAL_BUTTONS



"""
    try:
        # Создаем основное меню
        mainGroup = ButtonGroup.objects.filter(is_main_group=True).first()
        if not mainGroup:
            raise Exception("Не найдена основная группа кнопок")

        # Добавляем функцию main_menu
        common_admin_template += f"""
def main_menu_call(call: CallbackQuery) -> None:
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Главное меню')
        {mainGroup.name} = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                {mainGroup.name}.add(InlineKeyboardButton(text='Включить режим редактирования', callback_data='edit_main_menu'))
        except User.DoesNotExist:
            pass
"""
        main_buttons = Button.objects.filter(button_group=mainGroup.name)
        for button in main_buttons:
            common_admin_template += f"""

        {mainGroup.name}.add(InlineKeyboardButton(text='{button.button_text}', callback_data='{button.button_name}'))
            
        
        """
        common_admin_template += f"""
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup={mainGroup.name})
        """
        common_admin_template += """
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')
"""


        common_admin_template += f"""
def main_menu_message(message: Message) -> None:
    try:
        {mainGroup.name} = InlineKeyboardMarkup()

        user_id = message.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                {mainGroup.name}.add(InlineKeyboardButton(text='Включить режим редактирования', callback_data='edit_main_menu'))
        except User.DoesNotExist:
            pass
"""
        main_buttons = Button.objects.filter(button_group=mainGroup.name)
        for button in main_buttons:
            common_admin_template += f"""
        {mainGroup.name}.add(InlineKeyboardButton(text='{button.button_text}', callback_data='{button.button_name}'))
            
        """
        common_admin_template += f"""
        bot.send_message(message.chat.id, 'Главное меню', reply_markup={mainGroup.name})
        """
        common_admin_template += """
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')
"""



        common_admin_template += f"""
def main_menu_edit(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        {mainGroup.name} = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                {mainGroup.name}.add(InlineKeyboardButton(text='Выключить режим редактирования', callback_data='main_menu'))
        except User.DoesNotExist:
            pass
"""
        main_buttons = Button.objects.filter(button_group=mainGroup.name)
        for button in main_buttons:
            common_admin_template += f"""
        

        {mainGroup.name}.add(InlineKeyboardButton(text='{button.button_text}', callback_data='edit_button_main_{button.button_name}'))
"""
        common_admin_template += f"""
        bot.send_message(call.message.chat.id, 'Главное меню', reply_markup={mainGroup.name})
"""
        common_admin_template += """
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')
"""
        # начало обработчика всех груп кнопок
        all_groups = ButtonGroup.objects.filter(is_main_group=False)
        for group in all_groups:
            common_admin_template += f"""
@bot.callback_query_handler(func=lambda call: call.data == "{group.parent_button}")
def {group.name}_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        {group.name} = InlineKeyboardMarkup()
        
"""
            all_group_buttons = Button.objects.filter(button_group=group.name)
            if all_group_buttons.exists():
                common_admin_template += f"""
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                {group.name}.add(InlineKeyboardButton(text='Включить режим редактирования', callback_data='edit_{group.name}_handler'))
        except User.DoesNotExist:
            pass
"""
            else:
                common_admin_template += f"""
        {group.name}.add(InlineKeyboardButton(text='Удалить группу кнопок', callback_data='delete_group_button_{group.name}'))
"""
                for button in all_group_buttons:
                    common_admin_template += f"""
        
        {group.name}.add(InlineKeyboardButton(text='{button.button_text}', callback_data='{button.button_name}'))
"""
            common_admin_template += f"""
        bot.send_message(call.message.chat.id, f'главное меню', reply_markup={group.name})
"""
            common_admin_template += """
    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')
"""
            common_admin_template += f"""
@bot.callback_query_handler(func=lambda call: call.data == "edit_{group.name}_handler")
def edit_{group.name}_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        {group.name} = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                {group.name}.add(InlineKeyboardButton(text='Выключить режим редактирования', callback_data='edit_{group.name}_handler'))
        except User.DoesNotExist:
            pass
"""

            all_group_buttons = Button.objects.filter(button_group=group.name)
            if all_group_buttons.exists():
                for button in all_group_buttons:
                    common_admin_template += f"""
        
        {group.name}.add(InlineKeyboardButton(text='{button.button_text}', callback_data='edit_button_main_{button.button_name}'))
"""

            common_admin_template += f"""
        bot.send_message(call.message.chat.id, f'главное меню', reply_markup={group.name})
"""
            common_admin_template += """
    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')
"""

        # начало обработчика всех текстов
        all_texts = Texts.objects.all()
        for text in all_texts:
            common_admin_template += f"""
@bot.callback_query_handler(func=lambda call: call.data == "{text.parent_button}")
def {text.name_txt}_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        keyboard = InlineKeyboardMarkup()
        user_id = call.from_user.id
        try:
            user = User.objects.get(telegram_id=user_id)
            if user.is_admin:
                keyboard.add(InlineKeyboardButton(text='Редактировать текст', callback_data='edit_text_main_{text.name_txt}'))
        except User.DoesNotExist:
            pass
        keyboard.add(InlineKeyboardButton(text='В главное меню', callback_data='main_menu'))
        bot.send_message(call.message.chat.id, '{text.txt_text}', reply_markup=keyboard)
"""
            common_admin_template += """
    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')
"""

        # Записываем сгенерированный код в файл
        with open('bot/handlers/common_text.py', 'w', encoding='utf-8') as file:
            file.write(common_admin_template)
            
        bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                            message_id=callback_query.message.message_id, 
                            text='Файл common_admin.py успешно обновлен с обработчиками для всех кнопок')
        bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id, 
                                    message_id=callback_query.message.message_id, 
                                    reply_markup=ADMIN_BUTTONS_MAIN)
        logger.info('Файл common_admin.py успешно обновлен')

    except Exception as error:
        logger.error(f'Ошибка при обновлении common_admin.py: {error}')
        try:
            bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=f'Произошла ошибка при обновлении файла: {str(error)}')
            bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=ADMIN_BUTTONS_MAIN)
        except Exception as send_error:
            logger.error(f'Ошибка при отправке сообщения об ошибке: {send_error}')


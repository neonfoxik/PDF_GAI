from functools import wraps
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot, logger
from bot.models import User, Button, ButtonGroup, Texts, Documents
from bot.keyboards import SAVE_BUTTONS, ADMIN_BUTTONS_MAIN, CANCELBUTTON, ADMIN_BUTTONS_DOC, ADMIN_BUTTONS_BUTTON

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
def button_admin_menu(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    try:
        bot.send_message(callback_query.message.chat.id, 'Кнопки', reply_markup=ADMIN_BUTTONS_BUTTON)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в button_admin_menu: {e}')

@admin_permission
def documents_admin_menu(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    try:
        bot.send_message(callback_query.message.chat.id, 'Документы', reply_markup=ADMIN_BUTTONS_DOC)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в documents_admin_menu: {e}')

@admin_permission
def texts_admin_menu(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    try:
        bot.send_message(callback_query.message.chat.id, 'Тексты', reply_markup=ADMIN_BUTTONS_DOC)
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
def select_txt_or_docx_in_view_button_group(callback_query: CallbackQuery) -> None:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='Посмотреть все группы кнопок для текстов'
                                      , callback_data='view_button_group_in_select_txt'))
    keyboard.add(InlineKeyboardButton(text='Посмотреть все группы кнопок для документов'
                                      , callback_data='view_button_group_in_select_docx'))
    bot.send_message(callback_query.message.chat.id,
                     'Выберите какой тип груп кнопок вы хотите посмотреть',
                     reply_markup=keyboard)

@admin_permission
def view_button_group_in_select_docx(callback_query: CallbackQuery) -> None:
    button_groups = ButtonGroup.objects.filter(is_document=True)
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
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Для документов", callback_data="is_document_True"))
    keyboard.add(InlineKeyboardButton(text="Не для документов", callback_data="is_document_False"))
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancellation"))
    bot.send_message(message.chat.id, 'Выберите в каком меню будет находиться ваша группа кнопок',
                     reply_markup=keyboard)

@admin_permission
def get_is_document_group(callback_query: CallbackQuery) -> None:
    is_document = callback_query.data.split('_')[2] == 'True'
    button_group_data['is_document'] = is_document
    all_buttons = Button.objects.all()

    if not is_document:
        all_groups = ButtonGroup.objects.filter(is_document=False)
        if all_groups.exists():
            if all_buttons.exists():
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton(text="Просмотреть все кнопки", callback_data="view_all_buttons"))
                keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancellation"))
                try:
                    bot.send_message(callback_query.message.chat.id,
                                     'Выберите способ указания родительской кнопки, то есть '
                                     'кнопки после нажатия на которую будет открываться меню с этими кнопками',
                                     reply_markup=keyboard)
                except Exception as e:
                    logger.error(f'Ошибка при отправке сообщения в get_is_document_group: {e}')
        else:
            try:
                bot.send_message(callback_query.message.chat.id,
                                    'У вас нет зарегистрированных групп кнопок: группе кнопок будет присвоено значение '
                                    'Главное меню', reply_markup=ADMIN_BUTTONS_MAIN)
                group_name = button_group_data.get('group_name')
                button_group, created = ButtonGroup.objects.get_or_create(
                    name=group_name,
                    parent_button="main_menu",
                    is_main_group=True,
                    is_document=is_document
                )
                button_group.save()
                if button_state.is_create_button:
                    button_data['group_name'] = group_name
                    msg = bot.send_message(callback_query.message.chat.id,
                                            'Укажите название кнопки английскими буквами',
                                            reply_markup=CANCELBUTTON)
                    bot.register_next_step_handler(msg, get_button_name)
                else:
                    bot.send_message(callback_query.message.chat.id, 'Главное меню админа',
                                         reply_markup=ADMIN_BUTTONS_MAIN)
            except Exception as e:
                logger.error(f'Ошибка при отправке сообщения в get_is_document_group: {e}')
    else:
        all_groups = ButtonGroup.objects.filter(is_document=True)
        if all_groups.exists():
            if all_buttons.exists():
                keyboard = InlineKeyboardMarkup()
                keyboard.add(InlineKeyboardButton(text="Просмотреть все кнопки", callback_data="view_all_buttons"))
                keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancellation"))
                try:
                    bot.send_message(callback_query.message.chat.id,
                                     'Выберите способ указания родительской кнопки, то есть '
                                     'кнопки после нажатия на которую будет открываться меню с этими кнопками',
                                     reply_markup=keyboard)
                except Exception as e:
                    logger.error(f'Ошибка при отправке сообщения в get_is_document_group: {e}')
        else:
            try:
                bot.send_message(callback_query.message.chat.id,
                                 'У вас нет зарегистрированных групп кнопок: группе кнопок будет присвоено значение '
                                 'Главное меню', reply_markup=ADMIN_BUTTONS_MAIN)
                group_name = button_group_data.get('group_name')
                button_group, created = ButtonGroup.objects.get_or_create(
                    name=group_name,
                    parent_button="main_menu",
                    is_main_group=True,
                    is_document=is_document
                )
                button_group.save()
                if button_state.is_create_button:
                    button_data['group_name'] = group_name
                    msg = bot.send_message(callback_query.message.chat.id,
                                           'Укажите название кнопки английскими буквами',
                                           reply_markup=CANCELBUTTON)
                    bot.register_next_step_handler(msg, get_button_name)
                else:
                    bot.send_message(callback_query.message.chat.id, 'Главное меню админа',
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
    is_document = button_group_data.get('is_document')
    button_group, created = ButtonGroup.objects.get_or_create(name=group_name, parent_button=parent_name,
                                                              is_main_group=False, is_document=is_document)
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
    is_document = button_group_data.get('is_document')
    button_group, created = ButtonGroup.objects.get_or_create(name=group_name, parent_button=parent_name,
                                                              is_main_group=False, is_document=is_document)
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


"""список всех кнопок / груп кнопок для редактирования"""

@admin_permission
def list_buttons(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    try:
        buttons = Button.objects.all()
        if buttons.exists():
            keyboard = InlineKeyboardMarkup()
            for button in buttons:
                button_name = button.button_name
                keyboard.add(InlineKeyboardButton(text=button_name, callback_data=f"list_button_{button_name}"))
            try:
                keyboard.add(InlineKeyboardButton(text="Отмена", callback_data=f"cancellation"))
                bot.send_message(callback_query.message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)
            except Exception as e:
                logger.error(f'Ошибка при отправке сообщения в list_buttons: {e}')
        else:
            try:
                bot.send_message(callback_query.message.chat.id, 'Нет доступных кнопок.')
            except Exception as e:
                logger.error(f'Ошибка при отправке сообщения в list_buttons: {e}')
    except FileNotFoundError:
        bot.send_message(callback_query.message.chat.id, '⛔ Файл с кнопками не найден')
        logger.error('Файл с кнопками не найден')


def list_button_group(callback_query: CallbackQuery) -> None:
    try:
        groups = ButtonGroup.objects.all()
        if groups.exists():
            keyboard = InlineKeyboardMarkup()
            for group in groups:
                group_name = group.name
                keyboard.add(InlineKeyboardButton(text=group_name, callback_data=f"list_group_{group_name}"))
            try:
                keyboard.add(InlineKeyboardButton(text="Отмена", callback_data=f"cancellation"))
                bot.send_message(callback_query.message.chat.id, 'Выберите группу:', reply_markup=keyboard)
            except Exception as e:
                logger.error(f'Ошибка при отправке сообщения в list_button_group: {e}')
        else:
            try:
                bot.send_message(callback_query.message.chat.id, 'Нет доступных групп кнопок.')
            except Exception as e:
                logger.error(f'Ошибка при отправке сообщения в list_button_group: {e}')
    except FileNotFoundError:
        bot.send_message(callback_query.message.chat.id, '⛔ Файл с группами кнопок не найден')
        logger.error('Файл с группами кнопок не найден')

"""редактирование груп кнопок"""

@admin_permission
def button_group_actions(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    group_name = callback_query.data.split('_')[2]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Редактировать", callback_data=f"edit_group_all_{group_name}"))
    keyboard.add(InlineKeyboardButton(text="Удалить", callback_data=f"delete_group_{group_name}"))
    keyboard.add(InlineKeyboardButton(text="Отмена",
                                      callback_data=f"cancellation"))

    try:
        bot.send_message(callback_query.message.chat.id,
                         f'Выберите действие для группы {group_name} УДАЛЯЯ ГРУППУ КНОПКИ, '
                         f'ВСЕ КНОПКИ С ДАННОЙ ГРУППОЙ ОСТАНУТСЯ В БАЗЕ ДАНННЫХ НО НЕ БУДУТ РАБОТАТЬ'
                         f'ЕСЛИ ОНИ ВАМ НУЖНЫ ПРОСТО РЕДАКТИРУЙТЕ ГРУППУ КНОПОК, НО ЕСЛИ ВЫ УДАЛИЛИ, ТО'
                         f'МОЖНО СОЗДАТЬ ГРУППУ КНОПОК С АНАЛОГИЧНЫМ НАЗВАНИЕМ КАК БЫЛА ДО ЭТОГО, И ВСЕ ПОЧИНИТСЯ',
                         reply_markup=keyboard)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в button_group_actions: {e}')

@admin_permission
def edit_group(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    group_name = callback_query.data.split('_')[3]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Редактировать название группы кнопок",
                                      callback_data=f"edit_group_name_{group_name}"))
    keyboard.add(InlineKeyboardButton(text="Редактировать родительскую кнопку",
                                      callback_data=f"edit_parent_button_group_{group_name}"))
    keyboard.add(InlineKeyboardButton(text="Отмена",
                                      callback_data=f"cancellation"))
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    try:
        bot.send_message(callback_query.message.chat.id,f'Выберите действие для группы {group_name}',
                         reply_markup=keyboard)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в edit_group: {e}')

@admin_permission
def edit_group_name(callback_query: CallbackQuery) -> None:
    group_name = callback_query.data.split('_')[3]
    button_group_data['group_name'] = group_name
    msg = bot.send_message(callback_query.message.chat.id, 'Пожалуйста, введите новое название группы кнопок:')
    bot.register_next_step_handler(msg, get_new_group_name)

@admin_permission
def get_new_group_name(message: Message) -> None:
    validated_message = validate_user_message(message)
    if not validated_message:
        return
        
    new_group_name = validated_message.text
    old_group_name = button_group_data.get('group_name')
    ButtonGroup.objects.filter(name=old_group_name).update(name=new_group_name)
    Button.objects.filter(button_group=old_group_name).update(button_group=new_group_name)
    try:
        bot.send_message(message.chat.id, f'Название группы изменено на "{new_group_name}".',
                         reply_markup=ADMIN_BUTTONS_MAIN)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в get_new_group_name: {e}')


@admin_permission
def delete_group_from_file(callback_query: CallbackQuery) -> None:
    try:
        group_name = callback_query.data.split('_')[2]
        button_group = ButtonGroup.objects.filter(name=group_name)
        button_group.delete()
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        try:
            bot.send_message(callback_query.message.chat.id, f'Группа "{group_name}" успешно удалена.',
                             reply_markup=ADMIN_BUTTONS_MAIN)
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в delete_group_from_file: {e}')
    except FileNotFoundError:
        bot.send_message(callback_query.message.chat.id, '⛔ Файл с группами не найден')
        logger.error('Файл с группами не найден')


"""Редактирование кнопок"""

@admin_permission
def button_actions(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    button_name = callback_query.data.split('_')[2]  # Получаем имя кнопки из callback_data
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Редактировать", callback_data=f"edit_button_{button_name}"))
    keyboard.add(InlineKeyboardButton(text="Удалить", callback_data=f"delete_button_{button_name}"))
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    try:
        bot.send_message(callback_query.message.chat.id, f'Выберите действие для кнопки {button_name}:',
                         reply_markup=keyboard)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в button_actions: {e}')


@admin_permission
def delete_button_from_file(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    try:
        name = callback_query.data.split('_')[2]
        button = Button.objects.filter(button_name=name)  # Получаем первую кнопку с этим именем
        button.delete()  # Удаляем кнопку из модели
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        try:
            bot.send_message(callback_query.message.chat.id, f'Кнопка "{name}" успешно удалена.',
                             reply_markup=ADMIN_BUTTONS_MAIN)
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в delete_button_from_file: {e}')
    except FileNotFoundError:
        bot.send_message(callback_query.message.chat.id, '⛔ Файл с кнопками не найден')
        logger.error('Файл с кнопками не найден')


@admin_permission
def edit_button_menu(callback_query: CallbackQuery) -> None:
    button_name = callback_query.data.split('_')[2]
    EDIT_BUTTONS = InlineKeyboardMarkup()
    edit_text = InlineKeyboardButton(text="Редактировать текст", callback_data=f"edit_text_{button_name}")
    edit_name = InlineKeyboardButton(text="Редактировать имя кнопки", callback_data=f"edit_name_{button_name}")
    edit_group = InlineKeyboardButton(text="Редактировать группу в которой находиться кнопка",
                                      callback_data=f"edit_group_{button_name}")
    EDIT_BUTTONS.add(edit_text).add(edit_group).add(edit_name)
    try:
        bot.send_message(callback_query.message.chat.id, 'меню редактирования кнопки', reply_markup=EDIT_BUTTONS)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в edit_button_menu: {e}')


@admin_permission
def edit_button_callback_name(callback_query: CallbackQuery) -> None:
    button_name = callback_query.data.split('_')[2]  # Получаем имя кнопки из callback_data
    msg = bot.send_message(callback_query.message.chat.id, 'Введите новую callback_data для кнопки будет изменен'
                                                           ' параметр name он никак не отобразится у пользователей')
    bot.register_next_step_handler(msg, process_new_callback_data, button_name)


@admin_permission
def process_new_callback_data(message: Message, button_name: str) -> None:
    new_callback_data = message.text
    try:
        # Обновляем callback_data в модели
        button = Button.objects.get(button_name=button_name)
        button.name = new_callback_data
        button.save()
        try:
            bot.send_message(message.chat.id,
                             f'Callback data для кнопки "{button_name}" успешно обновлена на "{new_callback_data}"')
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в process_new_callback_data: {e}')
    except Button.DoesNotExist:
        bot.send_message(message.chat.id, 'Кнопка не найдена')
    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка при обновлении callback data')
        logger.error(f'Ошибка при обновлении callback data: {e}')


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
def choose_and_view_parent_txt(callback: CallbackQuery) -> None:
    bot.send_message(callback.message.chat.id, 'У вас нерт зарегестрированных кнопок создайте хотя бы одну',
                     reply_markup=ADMIN_BUTTONS_MAIN)

@admin_permission
def get_text_name(message: Message) -> None:
    msg = bot.send_message(message.chat.id, 'Введите текст который будет высвечиваться пользователю')
    bot.register_next_step_handler(msg, get_text_content)

@admin_permission
def get_text_content(message: Message) -> None:
    text_content = message.text
    text_name = texts_data.get('text_name')
    try:
        new_text = Texts(name_txt=text_name, txt_text=text_content, parent_button="")
        new_text.save()
        bot.send_message(message.chat.id, f'Текст "{text_name}" успешно добавлен!')
    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка при добавлении текста')
        logger.error(f'Ошибка при добавлении текста: {e}')



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

"""
    try:
        # Создаем основное меню
        mainGroup = ButtonGroup.objects.filter(is_document=False, is_main_group=True).first()
        if not mainGroup:
            raise Exception("Не найдена основная группа кнопок")

        # Добавляем функцию main_menu
        common_admin_template += f"""
def main_menu(message) -> None:
    try:
        {mainGroup.name} = InlineKeyboardMarkup()
"""
        main_buttons = Button.objects.filter(button_group=mainGroup.name)
        for button in main_buttons:
            common_admin_template += f"""
        {mainGroup.name}.add(InlineKeyboardButton(text='{button.button_text}', callback_data='{button.button_name}'))
        """
        common_admin_template += f"""
        bot.send_message(message.chat.id, f'главное меню', reply_markup={mainGroup.name})
        """
        common_admin_template += """
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')
"""

        # начало обработчика всех груп кнопок
        all_groups = ButtonGroup.objects.filter(is_main_group=False, is_document=False)
        for group in all_groups:
            common_admin_template += f"""
@bot.callback_query_handler(func=lambda call: call.data == "{group.parent_button}")
def {group.name}_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        {group.name} = InlineKeyboardMarkup()
"""
            all_group_buttons = Button.objects.filter(button_group=group.name)
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

        # начало обработчика всех текстов
        all_texts = Texts.objects.all()
        for text in all_texts:
            common_admin_template += f"""
@bot.callback_query_handler(func=lambda call: call.data == "{text.parent_button}")
def {text.name}_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f'главное меню', reply_markup={text.name})

"""
            common_admin_template += """
    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')
"""

        # Записываем сгенерированный код в файл
        with open('bot/handlers/common_text.py', 'w', encoding='utf-8') as file:
            file.write(common_admin_template)
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        try:
            bot.send_message(
                callback_query.message.chat.id,
                'Файл common_admin.py успешно обновлен с обработчиками для всех кнопок',
                reply_markup=ADMIN_BUTTONS_MAIN
            )
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в analyze_and_fill_common_admin: {e}')
        logger.info('Файл common_admin.py успешно обновлен')

    except Exception as error:
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        try:
            bot.send_message(
                callback_query.message.chat.id,
                f'Произошла ошибка при обновлении файла: {str(error)}',
                reply_markup=ADMIN_BUTTONS_MAIN
            )
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в analyze_and_fill_common_admin: {e}')
        logger.error(f'Ошибка при обновлении common_admin.py: {error}')


@admin_permission
def analyze_and_fill_common_admin_docx(callback_query: CallbackQuery) -> None:
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
from bot.settings import SRS
"""
    try:
        # Создаем основное меню
        mainGroupDocument = ButtonGroup.objects.filter(is_document=True, is_main_group=True).first()
        if not mainGroupDocument:
            raise Exception("Не найдена основная группа кнопок для кнопок")

        # Добавляем функцию main_menu
        common_admin_template += f"""
def documents_main_menu(message) -> None:
    try:
        {mainGroupDocument.name} = InlineKeyboardMarkup()
"""
        main_buttons = Button.objects.filter(button_group=mainGroupDocument.name)
        for button in main_buttons:
            common_admin_template += f"""
        {mainGroupDocument.name}.add(InlineKeyboardButton(text='{button.button_text}', callback_data='{button.button_name}'))
        """
        common_admin_template += f"""
        bot.send_message(message.chat.id, f'главное меню', reply_markup={mainGroupDocument.name})
        """
        common_admin_template += """
    except Exception as e:
        logger.error(f'Ошибка в main_menu: {e}')
"""

        # начало обработчика всех груп кнопок
        all_groups = ButtonGroup.objects.filter(is_main_group=False, is_document=True)
        for group in all_groups:
            common_admin_template += f"""
@bot.callback_query_handler(func=lambda call: call.data == "{group.parent_button}")
def {group.name}_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        {group.name} = InlineKeyboardMarkup()
"""
            all_group_buttons = Button.objects.filter(button_group=group.name)
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

        # начало обработчика всех документов
        all_documents = Documents.objects.all()
        for document in all_documents:
            common_admin_template += f"""
@bot.callback_query_handler(func=lambda call: call.data == "{document.parent_button}")
def {document.name}_handler(call: CallbackQuery) -> None:
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'главное меню', reply_markup={document.name})
"""
            common_admin_template += f"""
        bot.send_document(message.chat.id, open(r'SRS/{document.name}.docx', 'rb'))
"""
            common_admin_template += """
    except Exception as e:
        logger.error(f'Ошибка в обработчике : {e}')
"""

        # Записываем сгенерированный код в файл
        with open('bot/handlers/common_docx.py', 'w', encoding='utf-8') as file:
            file.write(common_admin_template)
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        try:
            bot.send_message(
                callback_query.message.chat.id,
                'Файл common_admin.py успешно обновлен с обработчиками для всех кнопок',
                reply_markup=ADMIN_BUTTONS_MAIN
            )
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в analyze_and_fill_common_admin: {e}')
        logger.info('Файл common_admin.py успешно обновлен')

    except Exception as error:
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        try:
            bot.send_message(
                callback_query.message.chat.id,
                f'Произошла ошибка при обновлении файла: {str(error)}',
                reply_markup=ADMIN_BUTTONS_MAIN
            )
        except Exception as e:
            logger.error(f'Ошибка при отправке сообщения в analyze_and_fill_common_admin_docx: {e}')
        logger.error(f'Ошибка при обновлении common_admin.py: {error}')

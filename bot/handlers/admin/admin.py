from functools import wraps
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot, logger
from bot.models import User, Button, ButtonGroup, Texts
from bot.keyboards import SAVE_BUTTONS, ADMIN_BUTTONS, CANCELBUTTON

button_data = {}
button_group_data = {}

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
        bot.send_message(message.chat.id, 'Название кнопки содержало некоректные символы измените его',
                         reply_markup=ADMIN_BUTTONS)
        return None


"""админ панель"""


@admin_permission
def admin_menu(message: Message) -> None:
    bot.send_message(message.chat.id, 'Меню админки', reply_markup=ADMIN_BUTTONS)


"""создание групп кнопок"""


@admin_permission
def get_or_create_button_group_name(callback_query: CallbackQuery) -> None:
    try:
        button_groups = ButtonGroup.objects.all()
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text='Создать новую группу', callback_data='create_new_group'))
        keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancellation"))

        if button_groups.exists():
            for group in button_groups:
                keyboard.add(InlineKeyboardButton(text=group.name, callback_data=f'select_group_{group.name}'))
            bot.send_message(callback_query.message.chat.id,
                             'Выберите существующую группу или создайте новую, группу кнопок можно всегда изменить:',
                             reply_markup=keyboard)
        else:
            bot.send_message(callback_query.message.chat.id, 'Нет доступных групп, создайте новую группу кнопок.')
            create_button_group(callback_query)
    except Exception as e:
        logger.error(f'Ошибка при получении групп кнопок: {e}')
        bot.send_message(callback_query.message.chat.id, 'Произошла ошибка при получении групп кнопок')


@admin_permission
def create_button_group(callback_query: CallbackQuery) -> None:
    try:
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        msg = bot.send_message(callback_query.message.chat.id, 'Укажите название группы кнопок английскими буквами',
                               reply_markup=CANCELBUTTON)
        bot.register_next_step_handler(msg, get_group_name)
    except Exception as e:
        msg = bot.send_message(callback_query.message.chat.id, 'Укажите название группы кнопок английскими буквами',
                               reply_markup=CANCELBUTTON)
        bot.register_next_step_handler(msg, get_group_name)


@admin_permission
def get_group_name(message: Message) -> None:
    button_group_data['group_name'] = message.text
    all_buttons = all_buttons = Button.objects.all()
    if all_buttons.exists():
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="Просмотреть все кнопки", callback_data="view_all_buttons"))
        keyboard.add(InlineKeyboardButton(text="Ввести название кнопки вручную", callback_data="enter_button_manually"))
        keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="cancellation"))
        bot.send_message(message.chat.id, 'Выберите способ указания родительской кнопки'
                                          f' тоесть кнопки после нажатия на которую будет открываться меню с этими кнопками {button_state.is_create_button}',
                         reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id,
                         'у вас нет зарегестрированых кнопок: так что группе кнопок будет присвоено значение '
                         'Главное меню')
        group_name = button_group_data.get('group_name')
        button_group, created = ButtonGroup.objects.get_or_create(name=group_name, parent_button="main_menu",
                                                                  is_main_group=True)
        button_group.save()
        if button_state.is_create_button == True:
            button_data['group_name'] = group_name
            bot.register_next_step_handler(message.chat.id, select_button_group_message)
        else:
            admin_menu(message)


@admin_permission
def enter_button_manually(callback_query: CallbackQuery) -> None:
    msg = bot.send_message(callback_query.message.chat.id,
                           'Укажите название кнопоки которую хотите назначить в качестве родительской')
    bot.register_next_step_handler(msg, save_button_grooup_in_django)


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
                            callback_data=f"select_parent_{button.button_name}"
                        ))
            else:
                keyboard.add(InlineKeyboardButton(text="Создать кнопку", callback_data="create_button"))
        else:
            if all_buttons.exists():
                for button in all_buttons:
                    if button.button_name not in all_parent_buttons:
                        keyboard.add(InlineKeyboardButton(
                            text=f"{button.button_name} ({button.button_text})",
                            callback_data=f"select_parent_increategroup_{button.button_name}"
                        ))
            else:
                keyboard.add(InlineKeyboardButton(text="Создать кнопку", callback_data="create_button"))#тут в общем нужно добавить создание кнопок к существующим группам и потом заполять группу кнопок этой информацией

        bot.send_message(callback_query.message.chat.id, 'Выберите кнопку которая будет родительской:',
                         reply_markup=keyboard)
    except Exception as e:
        logger.error(f'Ошибка при получении списка кнопок: {e}')
        bot.send_message(callback_query.message.chat.id, 'Произошла ошибка при получении списка кнопок')

@admin_permission
def select_buttongroup_increategroup(callback_query: CallbackQuery) -> None:
    parent_name = callback_query.data.split('_')[3]
    group_name = button_group_data.get('group_name')
    button_group, created = ButtonGroup.objects.get_or_create(name=group_name, parent_button=parent_name,
                                                              is_main_group=False)
    button_group.save()
    bot.send_message(callback_query.message.chat.id, 'Кнопка успешно создана Меню админки', reply_markup=ADMIN_BUTTONS)


@admin_permission
def save_button_grooup_in_django(message: Message) -> None:
    group_name = button_group_data.get('group_name')
    parent_name = message.text
    button_group, created = ButtonGroup.objects.get_or_create(name=group_name, parent_button=parent_name,
                                                              is_main_group=False)
    button_group.save()
    if button_state.is_create_button == False:
        bot.send_message(message.chat.id, 'Кнопка успешно создана Меню админки', reply_markup=ADMIN_BUTTONS)
    else:
        button_data['group_name'] = group_name
        bot.register_next_step_handler(message.chat.id, select_button_group_message)


"""создание кнопок"""


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
    button_data['name'] = message.text
    msg = bot.send_message(message.chat.id, 'Укажите текст кнопки', reply_markup=CANCELBUTTON)
    bot.register_next_step_handler(msg, get_button_text)


@admin_permission
def get_button_text(message: Message) -> None:
    button_data['text'] = message.text
    bot.send_message(message.chat.id, 'Хотите ли вы подтвердить создание кнопки?', reply_markup=SAVE_BUTTONS)


@admin_permission
def cancellation_button(callback_query: CallbackQuery) -> None:
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    bot.send_message(callback_query.message.chat.id, 'Создание кнопки отменено', reply_markup=ADMIN_BUTTONS)


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
    bot.send_message(callback_query.message.chat.id, 'Меню админки', reply_markup=ADMIN_BUTTONS)


"""список всех кнопок / груп кнопок для редактирования"""


@admin_permission
def list_buttons(callback_query: CallbackQuery) -> None:
    try:
        buttons = Button.objects.all()  # Получаем все кнопки из модели
        if buttons.exists():
            keyboard = InlineKeyboardMarkup()  # Создаем клавиатуру
            for button in buttons:
                button_name = button.button_name
                # Добавляем callback_data в формате "list_{button_name}" для перехода к действиям
                keyboard.add(InlineKeyboardButton(text=button_name, callback_data=f"list_{button_name}"))
            bot.send_message(callback_query.message.chat.id, 'Выберите кнопку:', reply_markup=keyboard)
        else:
            bot.send_message(callback_query.message.chat.id, 'Нет доступных кнопок.')
    except FileNotFoundError:
        bot.send_message(callback_query.message.chat.id, '⛔ Файл с кнопками не найден')
        logger.error('Файл с кнопками не найден')


def list_button_group(callback_query: CallbackQuery) -> None:
    try:
        buttons = Button.objects.all()  # Получаем все кнопки из модели
        if buttons.exists():
            keyboard = InlineKeyboardMarkup()  # Создаем клавиатуру
            for button in buttons:
                button_name = button.button_group
                # Добавляем callback_data в формате "list_{button_name}" для перехода к действиям
                keyboard.add(InlineKeyboardButton(text=button_name, callback_data=f"list_group_{button_name}"))
            bot.send_message(callback_query.message.chat.id, 'Выберите группу:', reply_markup=keyboard)
        else:
            bot.send_message(callback_query.message.chat.id, 'Нет доступных кнопок.')
    except FileNotFoundError:
        bot.send_message(callback_query.message.chat.id, '⛔ Файл с кнопками не найден')
        logger.error('Файл с кнопками не найден')


"""редактирование груп кнопок"""


@admin_permission
def button_group_actions(callback_query: CallbackQuery) -> None:
    group_name = callback_query.data.split('_')[2]  # Получаем имя кнопки из callback_data
    keyboard1 = InlineKeyboardMarkup()
    keyboard1.add(InlineKeyboardButton(text="Редактировать", callback_data=f"edit_group_{group_name}"))
    keyboard1.add(InlineKeyboardButton(text="Удалить", callback_data=f"delete_group_{group_name}"))
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    bot.send_message(callback_query.message.chat.id,
                     f'Выберите действие для группы {group_name} УДАЛЯЯ ГРУППУ КНОПКИ, У ВАС ОТВЯЖУТСЯ ВСЕ КНОПКИ С ДАННОЙ ГРУППОЙ, ЕСЛИ У ВАС ЕСТЬ КНОПКИ КОТОРЫЕ ВАМ НУЖНЫ НО ГРУППА ВАМ НЕ НУЖНА ПРЕДВАРИТЕЛЬНО ПЕРЕНЕСИТЕ ИХ',
                     reply_markup=keyboard1)


@admin_permission
def delete_group_from_file(callback_query: CallbackQuery) -> None:
    try:
        group_name = callback_query.data.split('_')[2]
        button = ButtonGroup.objects.filter(name=group_name)  # Получаем первую кнопку с этим именем
        for button in button:  # ТУТ НУЖНО ПЕРЕЗАПИСЫВАТЬ ГРУППУ ВСЕХ КНОПОК КОТОРАЯ group_name на ""
            button.delete()
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        bot.send_message(callback_query.message.chat.id, f'Группа "{group_name}" успешно удалена.',
                         reply_markup=ADMIN_BUTTONS)
    except FileNotFoundError:
        bot.send_message(callback_query.message.chat.id, '⛔ Файл с группами не найден')
        logger.error('Файл с группами не найден')


"""редактирование кнопок"""


@admin_permission
def button_actions(callback_query: CallbackQuery) -> None:
    button_name = callback_query.data.split('_')[1]  # Получаем имя кнопки из callback_data
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Редактировать", callback_data=f"edit_button_{button_name}"))
    keyboard.add(InlineKeyboardButton(text="Удалить", callback_data=f"delete_button_{button_name}"))
    bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    bot.send_message(callback_query.message.chat.id, f'Выберите действие для кнопки {button_name}:',
                     reply_markup=keyboard)


@admin_permission
def delete_button_from_file(callback_query: CallbackQuery) -> None:
    try:
        name = callback_query.data.split('_')[2]
        button = Button.objects.filter(button_name=name)  # Получаем первую кнопку с этим именем
        button.delete()  # Удаляем кнопку из модели
        bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        bot.send_message(callback_query.message.chat.id, f'Кнопка "{name}" успешно удалена.',
                         reply_markup=ADMIN_BUTTONS)
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
    bot.send_message(callback_query.message.chat.id, 'меню редактирования кнопки', reply_markup=EDIT_BUTTONS)


@admin_permission
def edit_button_callback_name(callback_query: CallbackQuery) -> None:
    button_name = callback_query.data.split('_')[2]  # Получаем имя кнопки из callback_data
    msg = bot.send_message(callback_query.message.chat.id,
                           'Введите новую callback_data для кнопки будет изменен параметр name он никак не отобразится у пользователей')
    bot.register_next_step_handler(msg, process_new_callback_data, button_name)


@admin_permission
def process_new_callback_data(message: Message, button_name: str) -> None:
    new_callback_data = message.text
    try:
        # Обновляем callback_data в модели
        button = Button.objects.get(button_name=button_name)
        button.name = new_callback_data
        button.save()
        bot.send_message(message.chat.id,
                         f'Callback data для кнопки "{button_name}" успешно обновлена на "{new_callback_data}"')
    except Button.DoesNotExist:
        bot.send_message(message.chat.id, 'Кнопка не найдена')
    except Exception as e:
        bot.send_message(message.chat.id, 'Произошла ошибка при обновлении callback data')
        logger.error(f'Ошибка при обновлении callback data: {e}')


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
        mainGroup = ButtonGroup.objects.filter(is_main_group=True).first()
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

        # обработчик документов

        # Записываем сгенерированный код в файл
        with open('bot/handlers/common_admin.py', 'w', encoding='utf-8') as file:
            file.write(common_admin_template)

        bot.send_message(
            callback_query.message.chat.id,
            'Файл common_admin.py успешно обновлен с обработчиками для всех кнопок',
            reply_markup=ADMIN_BUTTONS
        )
        logger.info('Файл common_admin.py успешно обновлен')

    except Exception as error:
        bot.send_message(
            callback_query.message.chat.id,
            f'Произошла ошибка при обновлении файла: {str(error)}',
            reply_markup=ADMIN_BUTTONS
        )
        logger.error(f'Ошибка при обновлении common_admin.py: {error}')

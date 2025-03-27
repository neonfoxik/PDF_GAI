from functools import wraps
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot import bot, logger
from bot.models import User
from bot.keyboards import CANCELBUTTON, ADMIN_BUTTONS_DOC



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


@admin_permission
def documents_admin_menu(message: Message) -> None:
    try:
        bot.send_message(message.chat.id, 'Документы', reply_markup=ADMIN_BUTTONS_DOC)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в documents_admin_menu: {e}')

@admin_permission
def admin_menu_call(call: CallbackQuery) -> None:
    try:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text='Документы',
                              reply_markup=ADMIN_BUTTONS_DOC, message_id=call.message.message_id)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения в documents_admin_menu: {e}')

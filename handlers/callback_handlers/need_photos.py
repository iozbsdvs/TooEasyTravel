from loader import bot
from telebot.types import CallbackQuery
from states.user_states import get_state_class_based_on_sort
from handlers.search_handlers.lowprice import calendar


@bot.callback_query_handler(func=lambda call: call.data.isalpha())
def need_photo_call(call: CallbackQuery) -> None:
    """
    Функция обрабатывает ответ пользователя на вопрос, нужно ли выводить фотографии отелей.

    :param call: объект типа CallbackQuery, содержащий информацию о нажатии пользователем кнопки в чате Telegram.
    :return: None
    """
    if call.data == 'yes':
        with bot.retrieve_data(call.message.chat.id) as data:
            data["photo_need"] = call.data
            StateClass = get_state_class_based_on_sort(data)

        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, StateClass.photo_count)
        bot.send_message(call.message.chat.id, 'Сколько вывести фотографий? От 1 до 10!')
    elif call.data == 'no':
        with bot.retrieve_data(call.message.chat.id) as data:
            data["photo_need"] = call.data
            data["photo_count"] = "0"
        bot.delete_message(call.message.chat.id, call.message.message_id)
        calendar(call.message, 'заезда')

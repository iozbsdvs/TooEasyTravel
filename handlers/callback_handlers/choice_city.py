from loader import bot
from telebot.types import CallbackQuery
from states.user_states import get_state_class_based_on_sort


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def destination_id_callback(call: CallbackQuery) -> None:
    """
    Функция-обработчик нажатия на кнопку "Выбрать" в меню выбора городов.

    :param call: Объект CallbackQuery, содержащий информацию о нажатии на кнопку.

    :return: None

       """
    with bot.retrieve_data(call.message.chat.id) as data:
        StateClass = get_state_class_based_on_sort(data)
        if call.data:
            data["destinationId"] = call.data

        bot.set_state(call.message.chat.id, StateClass.destinationId)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, StateClass.quantity_hotels)
        bot.send_message(call.message.chat.id, 'Укажите, сколько отелей вывести в чат: (не более 25!)')
from loader import bot
from telebot.types import CallbackQuery
from states.user_states import LowPriceInputState


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def destination_id_callback(call: CallbackQuery) -> None:
    if call.data:
        bot.set_state(call.message.chat.id, LowPriceInputState.destinationId)
        with bot.retrieve_data(call.message.chat.id) as data:
            data["destinationId"] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, LowPriceInputState.quantity_hotels)
        bot.send_message(call.message.chat.id, 'Укажите, сколько отелей вывести в чат: (не более 25!)')

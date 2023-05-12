from loader import bot
from telebot import types
from telebot.types import Message, Dict


def show_cities_buttons(message: Message, possible_cities: Dict) -> None:
    """
    Отображает кнопки с возможными городами в виде InlineKeyboardButton в сообщении, которое отправляется пользователю.

    :param message: объект сообщения telegram.Message, куда нужно отправить клавиатуру с кнопками.
    :param possible_cities: словарь с возможными городами, где ключ - gaiaId, значение - словарь с информацией о городе.
           Словарь города содержит ключи "regionNames" и "gaiaId".
    :type message: telegram.Message
    :type possible_cities: dict

    :return: None
    """
    keyboards_cities = types.InlineKeyboardMarkup()
    for key, value in possible_cities.items():
        keyboards_cities.add(types.InlineKeyboardButton(text=value["regionNames"], callback_data=value["gaiaId"]))
    bot.send_message(message.from_user.id, 'Пожалуйста выберите город', reply_markup=keyboards_cities)

from loader import bot
from telebot import types
from telebot.types import Message


def show_photo_need_buttons(message: Message) -> None:
    """
    Отправляет пользователю запрос на показ фотографий отеля и предоставляет соответствующие кнопки.

    :param message: объект сообщения от пользователя.
    :type message: telegram.Message

    :return: None
    """
    keyboards_photo_need = types.InlineKeyboardMarkup()
    keyboards_photo_need.add(types.InlineKeyboardButton(text='ДА', callback_data='yes'))
    keyboards_photo_need.add(types.InlineKeyboardButton(text='НЕТ', callback_data='no'))
    bot.send_message(message.chat.id, 'Показать фотографии отеля?', reply_markup=keyboards_photo_need)

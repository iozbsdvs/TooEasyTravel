from telebot.handler_backends import State, StatesGroup


class UserInputState(StatesGroup):
    """
    Класс, описывающий состояния пользователя в ходе ввода параметров для поиска самых дешевых отелей.

    :param command: команда, которую ввел пользователь
    :param input_city: город, который ввел пользователь
    :param destinationId: id города
    :param quantity_hotels: количество отелей, которое нужно пользователю
    :param photo_count: количество фотографий
    :param input_date: дата заезда/выезда
    :param history_select: выбор истории поиска
    """
    command = State()
    input_city = State()
    destinationId = State()
    quantity_hotels = State()
    photo_count = State()
    input_date = State()
    history_select = State()

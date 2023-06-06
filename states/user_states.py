from telebot.handler_backends import State, StatesGroup
from loader import bot


class UserInputState(StatesGroup):
    """
    Класс, описывающий состояния пользователя в ходе ввода параметров для поиска самых дешевых отелей.

    :param command: команда, которую ввел пользователь
    :param input_city: город, который ввел пользователь
    :param destinationId: id города
    :param quantity_hotels: количество отелей, которое нужно пользователю
    :param photo_count: количество фотографий
    :param input_date: дата заезда/выезда
    :param priceMin: минимальная стоимость отеля
    :param priceMax: максимальная стоимость отеля
    :param landmarkIn: начало диапазона расстояния от центра
    :param landmarkOut:  конец диапазона расстояния от центра
    :param history_select: выбор истории поиска
    """
    command = State()
    input_city_best = State()
    input_city = State()
    destinationId = State()
    quantity_hotels = State()
    photo_count = State()
    input_date = State()
    history_select = State()


class UserInputStateAdvanced(StatesGroup):
    """
    Класс, описывающий состояния пользователя в ходе ввода параметров для поиска самых дешевых отелей.

    :param command: команда, которую ввел пользователь
    :param input_city: город, который ввел пользователь
    :param destinationId: id города
    :param quantity_hotels: количество отелей, которое нужно пользователю
    :param photo_count: количество фотографий
    :param input_date: дата заезда/выезда
    :param priceMin: минимальная стоимость отеля
    :param priceMax: максимальная стоимость отеля
    :param landmarkIn: начало диапазона расстояния от центра
    :param landmarkOut:  конец диапазона расстояния от центра
    :param history_select: выбор истории поиска
    """
    command = State()
    input_city_best = State()
    input_city = State()
    destinationId = State()
    quantity_hotels = State()
    photo_count = State()
    priceMin = State()
    priceMax = State()
    input_date = State()
    landmarkIn = State()
    landmarkOut = State()
    history_select = State()


def get_state_class_based_on_sort(data):
    return UserInputStateAdvanced if data['sort'] == 'DISTANCE' else UserInputState
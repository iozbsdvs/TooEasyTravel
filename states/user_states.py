from telebot.handler_backends import State, StatesGroup


class LowPriceInputState(StatesGroup):
    command = State()  # Команда, которую ввел пользователь
    input_city = State()  # Город, который ввел пользователь
    destinationId = State()  # id города
    quantity_hotels = State()  # Количество отелей, которое нужно пользователю
    photo_count = State()  # Количество фотографий
    input_date = State()  # Дата заезда/выезда
    history_select = State()  # Выбор истории поиска

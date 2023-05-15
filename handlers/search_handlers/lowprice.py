from loader import bot
from telebot.types import Message
import datetime
from states.user_states import LowPriceInputState
import keyboards.inline
import api
from keyboards.calendar.calendar import Calendar
# from utils.print_data import print_data


@bot.message_handler(commands=["lowprice"])
def low_high_handler(message: Message) -> None:
    """
    Обработчик команды "/lowprice". Сохраняет необходимые данные в состояние бота и
    запрашивает у пользователя ввод города для поиска отелей.

    :param message: Объект сообщения, полученного от пользователя.
    :type message: telebot.types.Message
    :return: None
    """
    bot.set_state(message.chat.id, LowPriceInputState.command)
    with bot.retrieve_data(message.chat.id) as data:
        data.clear()
        data["command"] = message.text
        data["sort"] = 'PRICE_LOW_TO_HIGH'
        data["filters"] = {'availableFilter': 'SHOW_AVAILABLE_ONLY'}
        data['date_time'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        data["chat_id"] = message.chat.id

    bot.set_state(message.chat.id, LowPriceInputState.input_city)
    bot.send_message(message.from_user.id, "Введите город для поиска отелей: ")


@bot.message_handler(state=LowPriceInputState.input_city)
def input_city(message: Message) -> None:
    """
    Функция обрабатывает сообщение пользователя с названием города для поиска отелей.

    Если запрос на поиск города прошел успешно, выводит клавиатуру с возможными вариантами городов.
    Если возникли ошибки при запросе, выводит сообщение об ошибке и предлагает повторить попытку.

    :param message: Сообщение от пользователя с названием города.
    :type message: telebot.types.Message
    :return: None
    """
    with bot.retrieve_data(message.chat.id) as data:
        data['input_city'] = message.text
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": message.text, "locale": "ru_RU"}
        response_cities = api.core.request('GET', url, querystring)
        if response_cities.status_code == 200:
            possible_cities = api.request_processing.get_cities.get_cities(response_cities.text)
            keyboards.inline.city_buttons.show_cities_buttons(message, possible_cities)
        else:
            bot.send_message(message.chat.id, f"Что-то пошло не так, код ошибки: {response_cities.status_code}")
            bot.send_message(message.from_user.id, "Проверьте введённые данные и попробуйте еще раз!")
            data.clear()


@bot.message_handler(state=LowPriceInputState.quantity_hotels)
def input_quantity_hotels(message: Message) -> None:
    """
    Обрабатывает ввод пользователем количества отелей, которое нужно вывести.
    Проверяет, что введенное значение является числом в диапазоне от 1 до 25.
    Если значение не удовлетворяет требованиям, отправляет пользователю сообщение с ошибкой.
    Если значение корректно, сохраняет его в контексте чата и отправляет пользователю кнопки для выбора
    нужно ли ему фотографии отелей.

    :param message: Объект сообщения, содержащий введенный пользователем текст и информацию о чате.
    :type message: telebot.types.Message
    :return: None
    """
    if message.text.isdigit():
        if 0 < int(message.text) <= 25:
            with bot.retrieve_data(message.chat.id) as data:
                data['quantity_hotels'] = message.text
            keyboards.inline.photo_need.show_photo_need_buttons(message)
        else:
            bot.send_message(message.chat.id, 'Ошибка! Введите число от 1 до 25!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число!')


@bot.message_handler(state=LowPriceInputState.photo_count)
def input_quantity_photo(message: Message) -> None:
    """
    Запрашивает у пользователя количество фотографий, которые он хочет получить.
    Если пользователь ввел число от 1 до 10, то записывает это число в `data` (хранит информацию для данного пользователя).
    Иначе, бот отправляет сообщение об ошибке.

    :param message: сообщение пользователя
    :type message: telebot.types.Message
    :return: None
    """
    if message.text.isdigit():
        if 0 < int(message.text) <= 10:
            with bot.retrieve_data(message.chat.id) as data:
                data["photo_count"] = message.text
            calendar(message, 'заезда')
        else:
            bot.send_message(message.chat.id, 'Ошибка! Введите число от 1 до 10!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число!')


bot_calendar = Calendar()


def calendar(message: Message, word: str) -> None:
    """
    Отправляет сообщение пользователю с запросом выбора даты через календарь.

    :param message: сообщение пользователя
    :type message: telebot.types.Message
    :param word: слово, которое определяет, для какого события нужно выбрать дату.
    :type word: str
    :return: None
    """
    bot.send_message(message.chat.id, f'Выберите дату {word}:', reply_markup=bot_calendar.create_calendar())

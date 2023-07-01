import keyboards.inline
import api
import datetime
from database.add_to_db import add_user
from loader import bot
from telebot.types import Message
from keyboards.calendar.calendar import Calendar
from states.user_states import UserInputStateAdvanced
from utils.info import print_info


@bot.message_handler(commands=["bestdeal"])
def low_high_handler(message: Message) -> None:
    """
    Обработчик команды "/lowprice". Сохраняет необходимые данные в состояние бота и
    запрашивает у пользователя ввод города для поиска отелей.

    :param message: Объект сообщения, полученного от пользователя.
    :type message: telebot.types.Message
    :return: None
    """
    bot.set_state(message.chat.id, UserInputStateAdvanced.command)
    with bot.retrieve_data(message.chat.id) as data:
        data.clear()
        data["command"] = message.text
        data["sort"] = 'DISTANCE'
        data['date_time'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        data["chat_id"] = message.chat.id

        add_user(message.chat.id, message.from_user.username, message.from_user.full_name)
        bot.set_state(message.chat.id, UserInputStateAdvanced.input_city_best)
        bot.send_message(message.from_user.id, "Введите город для поиска отелей: ")


@bot.message_handler(state=UserInputStateAdvanced.input_city_best)
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


@bot.message_handler(state=UserInputStateAdvanced.quantity_hotels)
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
            bot.set_state(message.chat.id, UserInputStateAdvanced.priceMin)
            bot.send_message(message.chat.id, 'Введите минимальную стоимость отеля в долларах США:')
        else:
            bot.send_message(message.chat.id, 'Ошибка! Введите число от 1 до 25!!!!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число!')


@bot.message_handler(state=UserInputStateAdvanced.priceMin)
def input_price_min(message: Message) -> None:
    """
    Ввод минимальной стоимости отеля и проверка чтобы это было число.
    : param message : Message
    : return : None
    """
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            data['price_min'] = message.text
        bot.set_state(message.chat.id, UserInputStateAdvanced.priceMax)
        bot.send_message(message.chat.id, 'Введите максимальную стоимость отеля в долларах США:')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state=UserInputStateAdvanced.priceMax)
def input_price_max(message: Message) -> None:
    """
    Ввод максимальной стоимости отеля и проверка чтобы это было число. Максимальное число не может
    быть меньше минимального.
    : param message : Message
    : return : None
    """
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            if int(data['price_min']) < int(message.text):
                data['price_max'] = message.text
                data["filters"] = {"price": {
                    "max": int(data['price_max']),
                    "min": int(data['price_min'])
                }}
                keyboards.inline.photo_need.show_photo_need_buttons(message)
            else:
                bot.send_message(message.chat.id, 'Максимальная цена должна быть больше минимальной. Повторите ввод!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state=UserInputStateAdvanced.photo_count)
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


@bot.message_handler(state=UserInputStateAdvanced.landmarkIn)
def input_landmark_in(message: Message) -> None:
    """
    Ввод начала диапазона расстояния до центра
    : param message : Message
    : return : None
    """

    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            data['landmark_in'] = message.text
        bot.set_state(message.chat.id, UserInputStateAdvanced.landmarkOut)
        bot.send_message(message.chat.id, 'Введите конец диапазона расстояния от центра (в милях).')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state=UserInputStateAdvanced.landmarkOut)
def input_landmark_out(message: Message) -> None:
    """
    Ввод конца диапазона расстояния до центра
    : param message : Message
    : return : None
    """
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            data['landmark_out'] = message.text
            print_info(message, data)
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


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

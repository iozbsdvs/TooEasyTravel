from telebot import types
from database.add_to_db import Query, User
from database.read_from_db import read_query, get_history_response
from loader import bot
from loguru import logger
from states.user_states import UserInputState


@bot.message_handler(commands=['history'])
def history(message: types.Message) -> None:
    """
    Обрабатывает команду /history. Отправляет пользователю историю его поисковых запросов.

    :param message: types.Message, входное сообщение от пользователя.
    :return: None
    """

    logger.info('Выбрана команда history!')
    user = User.get(User.chat_id == message.chat.id)
    queries = read_query(user)
    if queries:
        for query in queries:
            bot.send_message(message.chat.id,
                             f"({query.id}). Дата и время: {query.date_time}. Вы вводили город: {query.input_city}")
        bot.set_state(message.chat.id, UserInputState.history_select)
        bot.send_message(message.from_user.id, "Введите номер интересующего вас варианта: ")
    else:
        bot.send_message(message.chat.id, "У вас нет истории поиска.")


@bot.message_handler(state=UserInputState.history_select)
def input_city(message: types.Message) -> None:
    """
    Обрабатывает ввод пользователя в состоянии history_select.
    Если пользователь ввел число, это считается идентификатором поискового запроса,
    и функция отправляет информацию об этом запросе. Если пользователь ввел не число,
    функция отправляет сообщение об ошибке.

    :param message: types.Message, входное сообщение от пользователя.
    :return: None
    """

    if message.text.startswith("/"):
        return

    if message.text.isdigit():
        query_id = int(message.text)
        query = Query.get_by_id(query_id)
        if not query.photo_need:
            bot.send_message(message.chat.id, 'Пользователь выбирал вариант "без фото"')
        history_dict = get_history_response(query_id)
        logger.info('Выдаем результаты выборки из базы данных')
        for hotel_id, hotel in history_dict.items():
            medias = []
            caption = f"Название отеля: {hotel['name']}\n Адрес отеля: {hotel['address']}" \
                      f"\nСтоимость проживания в сутки $: {hotel['price']}\nРасстояние до центра: {hotel['distance']}"
            if query.photo_need:
                for number, url in enumerate(hotel['images']):
                    if number == 0:
                        medias.append(types.InputMediaPhoto(media=url, caption=caption))
                    else:
                        medias.append(types.InputMediaPhoto(media=url))
                bot.send_media_group(message.chat.id, medias)
            else:
                bot.send_message(message.chat.id, caption)
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')

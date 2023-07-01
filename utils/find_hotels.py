import random
import api.core
from database.add_to_db import add_response
from loader import bot
from telebot.types import Message, Dict, InputMediaPhoto



def find_and_show_hotels(message: Message, data: Dict) -> None:
    """
        Функция для поиска и вывода информации об отелях с помощью API сервиса hotels4.p.rapidapi.com.

        :param message: объект сообщения, инициировавшего вызов функции.
        :type message: telebot.types.Message

        :param data: словарь с параметрами для поиска отелей. Содержит следующие ключи:
            'destination_id' - идентификатор места назначения,
            'checkInDate' - дата заезда в формате {'day': день, 'month': месяц, 'year': год},
            'checkOutDate' - дата выезда в формате {'day': день, 'month': месяц, 'year': год},
            'sort' - параметры сортировки результатов поиска,
            'filters' - фильтры для получения определенных отелей,
            'quantity_hotels' - количество отелей для вывода информации,
            'photo_count' - количество фотографий отеля для вывода.
        :type data: dict

        :return: None
        """
    payload = {
        "currency": "RUB",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": data['destinationId']},
        "checkInDate": {
            'day': int(data['checkInDate']['day']),
            'month': int(data['checkInDate']['month']),
            'year': int(data['checkInDate']['year'])
        },
        "checkOutDate": {
            'day': int(data['checkOutDate']['day']),
            'month': int(data['checkOutDate']['month']),
            'year': int(data['checkOutDate']['year'])
        },
        "rooms": [
            {
                "adults": 2,
                "children": [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 30,
        "sort": data["sort"],
        "filters": data["filters"]
    }

    url = 'https://hotels4.p.rapidapi.com/properties/v2/list'

    response_hotels = api.core.request('POST', url, payload)

    if response_hotels.status_code == 200:
        hotels = api.request_processing.get_hotels.get_hotels(response_hotels.text)

        if 'error' in hotels:
            bot.send_message(message.chat.id, hotels['error'])
            bot.send_message(message.chat.id, 'Попробуйте осуществить поиск с другими параметрами')
            bot.send_message(message.chat.id, '')

        count = 0
        for hotel in hotels.values():
            # Нужен дополнительный запрос, чтобы получить детальную информацию об отеле.
            # Цикл будет выполняться, пока не достигнет числа отелей, которое запросил пользователь.
            if count < int(data['quantity_hotels']):
                count += 1
                summary_payload = {
                    "currency": "RUB",
                    "eapid": 1,
                    "locale": "ru_RU",
                    "siteId": 300000001,
                    "propertyId": hotel['id']
                }
                summary_url = "https://hotels4.p.rapidapi.com/properties/v2/get-summary"
                get_summary = api.core.request('POST', summary_url, summary_payload)

                if get_summary.status_code == 200:
                    summary_info = api.request_processing.get_summary.get_summary(get_summary.text)

                    caption = f'Название: {hotel["name"]}\n ' \
                              f'Адрес: {summary_info["address"]}\n' \
                              f'Стоимость проживания: {round(hotel["price"], 2)} $\n ' \
                              f'Расстояние до центра: {round(hotel["distance"], 2)} mile.\n'

                    medias = []
                    links_to_images = []

                    # сформируем рандомный список из ссылок на фотографии, ибо фоток много, а надо только 10
                    try:
                        for random_url in range(int(data['photo_count'])):
                            links_to_images.append(summary_info['images']
                                                   [random.randint(0, len(summary_info['images']) - 1)])
                    except IndexError:
                        continue

                    data_to_db = {hotel['id']: {'name': hotel['name'], 'address': summary_info['address'],
                                                'price': hotel['price'], 'distance': round(hotel["distance"], 2),
                                                'date_time': data['date_time'], 'images': links_to_images}}
                    add_response(data_to_db)

                    # Если количество фотографий > 0: создаем медиа группу с фотками и выводим ее в чат
                    if int(data['photo_count']) > 0:
                        # формируем MediaGroup с фотографиями и описанием отеля и посылаем в чат
                        for number, url in enumerate(links_to_images):
                            if number == 0:
                                medias.append(InputMediaPhoto(media=url, caption=caption))
                            else:
                                medias.append(InputMediaPhoto(media=url))

                        bot.send_media_group(message.chat.id, medias)

                    else:
                        # если фотки не нужны, то просто выводим данные об отеле
                        bot.send_message(message.chat.id, caption)
                else:
                    bot.send_message(message.chat.id, f'Что-то пошло не так, код ошибки: {get_summary.status_code}')
            else:
                break
    else:
        bot.send_message(message.chat.id, f'Что-то пошло не так, код ошибки: {response_hotels.status_code}')
    bot.send_message(message.chat.id, 'Поиск завершен!')

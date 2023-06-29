import json
from telebot.types import Dict


def get_hotels(response_text: str) -> Dict:
    """
       Функция для получения информации об отелях из ответа на запрос к API сервиса бронирования отелей.
       Принимает выбранную команду сортировки, а так же пределы диапазона расстояния от центра города.
       Возвращает отсортированный словарь, в зависимости от команды сортировки.

       :param response_text: текст ответа на запрос
       :type response_text: str
       :param command: команда для выбора сортировки отелей
       :type command: str
       :param landmark_in: нижняя граница расстояния до центра города, в котором ищутся отели
       :type landmark_in: str
       :param landmark_out: верхняя граница расстояния до центра города, в котором ищутся отели
       :type landmark_out: str
       :return: словарь с данными об отелях
       :rtype: dict
       """
    data = json.loads(response_text)
    if not data:
        raise LookupError('Запрос пуст..')
    # Проверка на возможные ошибки:
    if 'errors' in data.keys():
        return {'error': data['errors'][0]['message']}

    hotels_data = {}
    for hotel in data['data']['propertySearch']['properties']:
        try:
            hotels_data[hotel['id']] = {
                'name': hotel['name'], 'id': hotel['id'],
                'distance': hotel['destinationInfo']['distanceFromDestination']['value'],
                'unit': hotel['destinationInfo']['distanceFromDestination']['unit'],
                'price': hotel['price']['lead']['amount']
            }
        except (KeyError, TypeError):
            continue
    return hotels_data

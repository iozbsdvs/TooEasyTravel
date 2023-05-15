import json
from telebot.types import Dict


def get_summary(hotels_request: str) -> Dict:
    """
        Функция получения основной информации об отеле по API-запросу.

        :param hotels_request: Ответ API-запроса в виде строки JSON.
        :type hotels_request: str
        :return: Словарь с информацией об отеле: ID, название, адрес, координаты, список ссылок на фотографии.
        :rtype: dict
        :raises LookupError: Если запрос пустой.
        """
    data = json.loads(hotels_request)
    if not data:
        raise LookupError('Запрос пуст..')

    hotel_data = {
        'id': data['data']['propertyInfo']['summary']['id'], 'name': data['data']['propertyInfo']['summary']['name'],
        'address': data['data']['propertyInfo']['summary']['location']['address']['addressLine'],
        'coordinates': data['data']['propertyInfo']['summary']['location']['coordinates'],
        'images': [
            url['image']['url'] for url in data['data']['propertyInfo']['propertyGallery']['images']
        ]
    }

    return hotel_data

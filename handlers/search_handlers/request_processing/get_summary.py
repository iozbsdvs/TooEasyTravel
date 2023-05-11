import json
from telebot.types import Dict


def get_hotels(hotels_request: str) -> Dict:
    data = json.loads(hotels_request)
    if not data:
        raise LookupError('Запрос пуст..')

    hotel_data = {
        'id': data['data']['propertyInfo']['summary']['id'], 'name': data['data']['propertyInfo']['summary']['name'],
        'address': data['data']['propertyInfo']['summary']['location']['address']['addressLine'],
        'coordinates': data['data']['propertyInfo']['summary']['location']['coordinates'],
        'images': [
            url['image']['url'] for url in data['data']['propertyInfo']['propertyGallery']['images']
        ], 'url': data['data']['propertyInfo']['summary']['url']
    }

    return hotel_data

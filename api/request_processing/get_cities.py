import json
from telebot.types import Dict


def get_cities(response_text: str) -> Dict:
    """
       Функция принимает текст ответа от API, содержащего информацию о возможных городах,
       и возвращает словарь с информацией о найденных городах.

       :param response_text : Текст ответа от API.
       :type response_text: str

       :return possible_cities : Словарь с информацией о найденных городах,
       где ключом является идентификатор города, а значением - словарь с информацией о городе,
       содержащий следующие поля:
       - "gaiaId": int - идентификатор города;
       - "regionNames": str - название региона.
       :rtype: dict
       """

    possible_cities = {}
    data = json.loads(response_text)
    if not data:
        raise LookupError('Запрос пуст..')
    for id_place in data["sr"]:
        try:
            possible_cities[id_place["gaiaId"]] = {
                "gaiaId": id_place["gaiaId"],
                "regionNames": id_place["regionNames"]["fullName"]
            }
        except KeyError:
            continue
    return possible_cities

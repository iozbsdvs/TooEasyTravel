import requests
from config_data import config

headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": config.RAPID_API_KEY,
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}


def request(method: str, url: str, querystring: dict) -> requests.Response:
    """
    Отправляем запрос к серверу

    :param method: str
    :param url: str
    :param querystring: dict
    :return: requests.Response
    """

    if method == "GET":
        response_get = requests.request(method="GET", url=url, params=querystring, headers=headers)
        return response_get
    elif method == "POST":
        response_post = requests.request(method="POST", url=url, json=querystring, headers=headers)
        return response_post

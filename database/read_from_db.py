from loguru import logger
from database.add_to_db import Query, Response, Image


def read_query(user: int):
    try:
        logger.info('Читаем из таблицы query')
        records = Query.select().where(Query.user_id == user)
        return records
    except Exception as e:
        logger.error(f"Ошибка при чтении из таблицы Query: {e}")
        return []


def get_history_response(query_id: int):
    try:
        logger.info('Читаем из таблицы response.')
        responses = Response.select().where(Response.query_id == query_id)
        history = {}
        for response in responses:
            images = Image.select().where(Image.response == response)
            links = [image.link for image in images]
            history[response.hotel_id] = {
                'name': response.name,
                'address': response.address,
                'price': response.price,
                'distance': response.distance,
                'images': links
            }
        return history
    except Exception as e:
        logger.error(f"Ошибка при чтении из таблицы Response: {e}")
        return {}

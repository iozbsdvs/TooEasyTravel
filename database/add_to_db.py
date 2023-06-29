from peewee import *
from loguru import logger

db = SqliteDatabase('database/history.sqlite3')


class BaseModel(Model):
    """
    Базовый класс для моделей базы данных. Все другие модели наследуются от него.
    """

    class Meta:
        database = db


class User(BaseModel):
    """
    Модель для пользователей. Содержит поля для хранения информации о пользователях.

    :param chat_id: int, уникальный идентификатор чата
    :param username: str, имя пользователя
    :param full_name: str, полное имя пользователя
    """

    chat_id = IntegerField(unique=True)
    username = CharField(null=True)
    full_name = CharField(null=True)


class Query(BaseModel):
    """
    Модель для поисковых запросов. Содержит поля для хранения информации о запросах.

    :param user: ссылка на пользователя, который сделал запрос
    :param date_time: дата и время выполнения запроса
    :param input_city: город, введенный пользователем для поиска
    :param destination_id: идентификатор назначения поиска
    :param photo_need: флаг, указывающий, требуются ли фотографии или нет
    """

    user = ForeignKeyField(User, backref='queries')
    date_time = DateTimeField()
    input_city = CharField()
    destination_id = CharField()
    photo_need = BooleanField()


class Response(BaseModel):
    """
    Модель для ответов на поисковые запросы. Содержит поля для хранения информации об ответах.

    :param query: ссылка на запрос, на который был дан ответ
    :param hotel_id: идентификатор отеля
    :param name: название отеля
    :param address: адрес отеля
    :param price: цена за ночь в отеле
    :param distance: расстояние до центра города
    """

    query = ForeignKeyField(Query, backref='responses')
    hotel_id = CharField()
    name = CharField()
    address = CharField()
    price = FloatField()
    distance = FloatField()


class Image(BaseModel):
    """
    Модель для изображений. Содержит поля для хранения ссылок на изображения.

    :param response: ссылка на ответ, к которому относится изображение
    :param link: ссылка на изображение
    """

    response = ForeignKeyField(Response, backref='images')
    link = TextField()


db.connect()
db.create_tables([User, Query, Response, Image])


def add_user(chat_id: int, username: str, full_name: str) -> None:
    """
    Добавляет нового пользователя в базу данных.

    :param chat_id: int, уникальный идентификатор чата
    :param username: str, имя пользователя
    :param full_name: str, полное имя пользователя
    :return: None
    """

    try:
        User.create(chat_id=chat_id, username=username, full_name=full_name)
        logger.info('Добавлен новый пользователь.')
    except IntegrityError:
        logger.info('Данный пользователь уже существует')


def add_query(query_data: dict) -> None:
    """
    Добавляет новый поисковый запрос в базу данных.

    :param query_data: dict, словарь с данными запроса, включая идентификатор чата, введенный город,
                       флаг наличия фотографии, идентификатор назначения и дату/время.
    :return: None
    """

    user = User.get(User.chat_id == query_data['chat_id'])
    try:
        Query.create(user_id=user, input_city=query_data['input_city'],
                     photo_need=query_data['photo_need'], destination_id=query_data['destinationId'],
                     date_time=query_data['date_time'])
        logger.info('Добавлен в БД новый запрос.')

        query_to_delete = (Query
                           .select()
                           .where(Query.user_id == user)
                           .order_by(Query.date_time)
                           .offset(5)
                           .first())
        if query_to_delete is not None:
            query_to_delete.delete_instance()
    except IntegrityError:
        print('Запрос с такой датой и временем уже существует')


def add_response(search_result: dict) -> None:
    """
    Добавляет новый ответ на поисковый запрос в базу данных, а также добавляет соответствующие изображения.

    :param search_result: dict, словарь с результатами поиска, включая дату и время запроса, идентификатор отеля,
                          имя отеля, адрес отеля, цену и расстояние до центра.
    :return: None
    """

    for item in search_result.items():
        query = Query.select().where(Query.date_time == item[1]['date_time']).get()
        new_response = Response.create(query=query, hotel_id=item[0], name=item[1]['name'],
                                       address=item[1]['address'],
                                       price=item[1]['price'], distance=item[1]['distance'])
        logger.info('Добавлены в БД данные отеля.')
        for link in item[1]['images']:
            Image.create(response=new_response, link=link)
        logger.info('Добавлены в БД ссылки на фотографии отеля.')
        # Обновляем запрос с id ответа
        query.response = new_response
        query.save()

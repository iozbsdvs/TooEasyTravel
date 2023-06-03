from datetime import datetime
from peewee import *
from config_data.config import db


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    """
       Модель, представляющая пользователя Telegram.

       :param chat_id: уникальный идентификатор чата пользователя
       :type chat_id: int

       :param username: никнейм пользователя
       :type username: str

       :param full_name: полное имя пользователя
       :type full_name: str or None

       :cvar Meta.database: база данных, используемая для хранения объектов модели
       :type Meta.database: peewee.Database

       """

    chat_id = IntegerField(unique=True)
    username = CharField(null=True)
    full_name = CharField(null=True)


class Response(BaseModel):
    """
       Модель, представляющая отель, возвращенный в результате запроса.

       :param hotel_id: уникальный идентификатор отеля, связанный с ответом
       :type hotel_id: str
       :param name: название отеля
       :type name: str
       :param address: адрес отеля
       :type address: str
       :param price: цена за проживание в отеле
       :type price: float
       :param distance: расстояние от отеля до центра города
       :type distance: float
       """

    hotel_id = CharField(unique=True)
    name = CharField()
    address = CharField()
    price = FloatField()
    distance = FloatField()


class Image(BaseModel):
    response = ForeignKeyField(Response, backref='images')
    link = CharField()


class Query(BaseModel):
    """
    Модель запроса, содержащая информацию о запросах пользователей.

    :param user: пользователь, отправивший запрос
    :type user: int

    :param date_time: дата и время создания запроса
    :type date_time: datetime.datetime

    :param input_city: название города, из которого запрашивается информация
    :type input_city: str

    :param destination_id: ID города, для которого запрашивается информация
    :type destination_id: str

    :param photo_need: необходимость получения фотографии города
    :type photo_need: bool

    :param response: ответ на запрос
    :type response: int
    """

    user = ForeignKeyField(User, backref='queries')
    date_time = CharField(default=datetime.now)
    input_city = CharField()
    destination_id = CharField()
    photo_need = BooleanField(default=False)
    response = ForeignKeyField(Response, backref='queries', null=True, on_delete='CASCADE')


db.connect()
db.create_tables([User, Response, Image, Query])

def add_user(chat_id: int, username: str, full_name: str) -> None:
    user, created = User.get_or_create(chat_id=chat_id, defaults={'username': username, 'full_name': full_name})
    if created:
        print('Добавлен новый пользователь.')
    else:
        print('Данный пользователь уже существует')


def add_query(query_data: dict) -> None:
    user = User.get(User.chat_id == query_data['chat_id'])
    query = Query.create(user=user,
                         input_city=query_data['input_city'],
                         destination_id=query_data['destination_id'],
                         photo_need=query_data['photo_need'])
    print('Добавлен в БД новый запрос.')

    # Оставляем только последние 5 записей для каждого пользователя
    if user.queries.count() > 5:
        oldest_query = user.queries.order_by(Query.date_time).first()
        oldest_query.delete_instance()


def add_response(search_result: dict) -> None:
    for item in search_result.items():
        response = Response.create(hotel_id=item[0],
                                   name=item[1]['name'],
                                   address=item[1]['address'],
                                   price=item[1]['price'],
                                   distance=item[1]['distance'])
        for link in item[1]['images']:
            image = Image.create(response=response, link=link)
        print('Добавлены в БД данные отеля и ссылки на фотографии.')

    # Обновляем последний запрос данными ответа
    query = Query.select().order_by(Query.date_time.desc()).get()
    query.response = response
    query.save()
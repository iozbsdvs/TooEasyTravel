from datetime import datetime
from peewee import *

db = SqliteDatabase('database/history.sqlite3')


class User(Model):
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
    username = CharField()
    full_name = CharField(null=True)

    class Meta:
        database = db


class Query(Model):

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
    date_time = DateTimeField(default=datetime.now)
    input_city = CharField()
    destination_id = CharField()
    photo_need = BooleanField(default=False)
    response = ForeignKeyField('Response', backref='queries', null=True, on_delete='CASCADE')

    class Meta:
        database = db


class Response(Model):
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

    hotel_id = CharField(primary_key=True)
    name = CharField()
    address = CharField()
    price = FloatField()
    distance = FloatField()

    class Meta:
        database = db


class Image(Model):
    response = ForeignKeyField(Response, backref='images')
    link = CharField()

    class Meta:
        database = db


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
    query.save()
    print('Добавлен в БД новый запрос.')
    # Нам не нужно очень много записей историй поиска, поэтому для каждого пользователя
    # будем хранить только 5 последних записей, лишние - удалим.
    if user.queries.count() > 5:
        oldest_query = user.queries.order_by(Query.date_time).first()
        oldest_query.delete_instance()


def add_response(search_result: dict) -> None:
    response_list = []
    for item in search_result.items():
        response = Response.create(hotel_id=item[0],
                                   name=item[1]['name'],
                                   address=item[1]['address'],
                                   price=item[1]['price'],
                                   distance=item[1]['distance'])
        response_list.append(response)
        for link in item[1]['images']:
            image = Image.create(response=response, link=link)
            image.save()
        print('Добавлены в БД ссылки на фотографии отеля.')
    Query.update(response=response_list[-1]).where(
        Query.date_time == search_result[response_list[-1].hotel_id]['date_time']).execute()
    print('Добавлены в БД данные отеля.')

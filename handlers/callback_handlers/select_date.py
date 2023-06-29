from loader import bot
from utils.info import print_info
from states.user_states import get_state_class_based_on_sort, UserInputStateAdvanced
from keyboards.calendar.calendar import CallbackData, Calendar
from handlers import search_handlers
from telebot.types import CallbackQuery
import datetime

calendar = Calendar()
calendar_callback = CallbackData("calendar", "action", "year", "month", "day")


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_callback.prefix))
def input_date(call: CallbackQuery) -> None:
    """
    Функция обрабатывает выбор пользователем даты заезда и выезда в календаре.

    :param call: Объект CallbackQuery, содержащий информацию о нажатии кнопки календаря.
    :type call: CallbackQuery

    :return: None
    """
    name, action, year, month, day = call.data.split(calendar_callback.sep)
    calendar.calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
    )

    if action == 'DAY':
        month = check_month_day(month)
        day = check_month_day(day)
        select_date = year + month + day

        now_year, now_month, now_day = datetime.datetime.now().strftime('%Y.%m.%d').split('.')
        now = now_year + now_month + now_day

        with bot.retrieve_data(call.message.chat.id) as data:
            StateClass = get_state_class_based_on_sort(data)
            bot.set_state(call.message.chat.id, StateClass.input_date)

            if 'checkInDate' in data:
                checkin = int(data['checkInDate']['year'] + data['checkInDate']['month'] + data['checkInDate']['day'])
                if int(select_date) > checkin:
                    data['checkOutDate'] = {'day': day, 'month': month, 'year': year}

                    if data['sort'] == 'DISTANCE':
                        bot.set_state(call.message.chat.id, UserInputStateAdvanced.landmarkIn)
                        bot.send_message(call.message.chat.id, 'Введите начало диапазона расстояния от центра '
                                                               '(от 0 миль).')
                    else:
                        print_info(call.message, data)
                else:
                    bot.send_message(call.message.chat.id, 'Дата выезда должна быть больше даты заезда! '
                                                           'Повторите выбор даты!')
                    search_handlers.lowprice.calendar(call.message, 'выезда')
            else:
                if int(select_date) >= int(now):

                    data['checkInDate'] = {'day': day, 'month': month, 'year': year}
                    search_handlers.lowprice.calendar(call.message, 'выезда')
                else:
                    bot.send_message(call.message.chat.id, 'Дата заезда должна быть больше или равна сегодняшней дате!'
                                                           'Повторите выбор даты!')
                    search_handlers.lowprice.calendar(call.message, 'заезда')


def check_month_day(number: str) -> str:
    """
    Преобразование формата числа месяца или дня из формата 1..9 в формат 01..09
    : param number : str, число месяца или дня
    : return number : str
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if int(number) in numbers:
        number = '0' + number
    return number

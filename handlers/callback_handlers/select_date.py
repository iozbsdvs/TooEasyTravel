from loader import bot
import datetime
from states.user_states import LowPriceInputState
from keyboards.calendar.calendar import CallbackData, Calendar
from handlers import search_handlers
from telebot.types import CallbackQuery

calendar = Calendar()
calendar_callback = CallbackData("calendar", "action", "year", "month", "day")


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_callback.prefix))
def input_date(call: CallbackQuery) -> None:
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

        bot.set_state(call.message.chat.id, LowPriceInputState.input_date)
        with bot.retrieve_data(call.message.chat.id) as data:
            if 'checkInDate' in data:
                checkin = int(data['checkInDate']['year'] + data['checkInDate']['month'] + data['checkInDate']['day'])
                if int(select_date) > checkin:
                    data['checkOutDate'] = {'day': day, 'month': month, 'year': year}

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

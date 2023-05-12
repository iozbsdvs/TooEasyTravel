from loader import bot
from telebot.types import Message


@bot.message_handler(func=lambda message: True)
def send_text(message: Message):
    if message.text == "Привет":
        bot.send_message(message.chat.id, 'Привет-привет!')
    else:
        bot.send_message(message.chat.id, 'Такую команду я еще не знаю..')


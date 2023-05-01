from TelegramBot import bot
from telebot.types import Message


@bot.message_handler(content_types=['text'])
def send_text(message: Message):
    if message.text == "Привет":
        bot.send_message(message.chat.id, 'Привет-привет!')

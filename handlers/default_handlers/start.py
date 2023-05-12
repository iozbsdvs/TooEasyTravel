from telebot.types import Message
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Функция-обработчик команды /start.
    Приветствует пользователя и запускает бота.

    :param message: объект сообщения от пользователя
    """
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")


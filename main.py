from TelegramBot import bot
from handlers.start import bot_start
from handlers.text import send_text

if __name__ == '__main__':
    bot.polling(non_stop=True)
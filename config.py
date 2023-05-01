import os
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')

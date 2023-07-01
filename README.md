<h1 align="center">🌇 Too Easy Travel 🌇

[![Telegram URL](https://www.dampftbeidir.de/mediafiles/tpl/icon-telegram.png)](https://t.me/Too_easy_hotels_travel_bot) 
</h1>


---
## Описание

### Возможности бота:
🏨 Поиск отелей по заданному городу.

🏨 Сортировка отелей по цене (от низкой к высокой или наоборот).

🏨 Поиск лучших предложений в рамках заданных параметров: цена, расстояние от центра.

🏨 Вывод фотографий отелей.

🏨 История поиска отелей.

---
## Инструкция по развертыванию

- `python3 -m venv venv_name` - создание виртуального окружения.
- `source venv_name/bin/activate` - активация виртуального окружения.
- `pip install -r requirements.txt` - подключить все библиотеки проекта.

---
## Инструкция по запуску

- Создайте бота в Telegram через BotFather и получите токен для использования API.
- Зарегистрируйтесь на RapidAPI и получите ключ для API hotels.com.
- `touch .env` - создайте файл .env, подробнее написано в .env.template.
- `echo "BOT_TOKEN=your_bot_token" >> .env` - добавьте в `.env` Токен вашего бота.
- `echo "RAPIDAPI_KEY=your_rapidapi_key" >> .env` - добавьте в `.env` ключ для RapidAPI.
- Запустите файл `main.py`.

---
## Инструкция по использованию

### Команда /lowprice
1. Введите /lowprice.
2. В ответ на запрос бота, введите название города, где вы хотите найти отели.
3. Затем бот запросит количество отелей, которое вы хотите увидеть в результате. Введите число, которое не превышает максимальное количество, заданное в боте.
4. Бот попросит вас решить, хотите ли вы видеть фотографии отелей. Ответьте "Да" или "Нет".
5. Если вы ответите "Да", бот спросит вас, сколько фотографий каждого отеля вы хотите увидеть. Введите число, которое не превышает максимальное количество, заданное в боте.

### Команда /highprice
1. Введите /highprice.
2. Следуйте тем же шагам, что и в команде /lowprice.

### Команда /bestdeal
1. Введите /bestdeal.
2. Введите название города, как в предыдущих командах.
3. Введите диапазон цен для поиска отелей. Например, "500-1000" для поиска отелей с ценами от 500 до 1000.
4. Затем бот запросит у вас диапазон расстояния от центра города, на котором вы хотите найти отели. Например, "0-10" для поиска отелей, расположенных от 0 до 10 км от центра.
5. Далее, следуйте тем же шагам, что и в команде /lowprice, относительно количества отелей и фотографий.

### Команда /history
1. Введите /history.
2. Бот предоставит вам историю поиска отелей, включающую команды, которые вы вводили, дату и время ввода команд, а также отели, которые были найдены.

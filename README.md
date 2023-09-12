Great people telegram bot
===================

Great people telegram bot - бот, имитирующий общение с известными личностями. Хотели бы вы узнать что думает о 
большом адронном коллайдере Альберт Эйнштейн? Или выяснить из первых уст, каково на самом деле - прыгать по гигантским грибам
небезызвестному Марио? Для получения ответов просто подключите бота и начните с ним общение.  
Бот реализован на `Python 3.10`
---



Для запуска:
-----------
1. Необходимо создать config.py и прописать свои ключи API от telegram и ChatGPT:

```python
TOKEN = 'свой ключ API telegram'
OPENAI_API_KEY = 'свой ключ API ChatGPT'
```

2. Нужно разместить html страницу с выбором персонажей - character.html на хостинге, или в GitHub Pages.
Указать для нее адрес в функции клавиатуры модуля `app.py`:
```python
def keyboard() -> ReplyKeyboardMarkup:
    """ Клавиатура выбора персонажа """
    keyboard = ReplyKeyboardMarkup.from_button(
        resize_keyboard=True,
        button=KeyboardButton(
                text="Выбрать персонажа",
                web_app=WebAppInfo(url="ВАШ_АДРЕС/character.html")))
    return keyboard
```

3. Далее установить виртуальное окружение и зависимости из `requirements.txt`.
В активированном виртуальном окружении запустите:

```shell
python app.py
```

Если все успешно, бот начнет выводить в консоль логи о событиях.